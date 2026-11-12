"""Deterministic synthetic gait event benchmark, not a clinical fall-risk model."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'src'))
from step_detection import detect_steps
from gait_summary import summarize_steps


def encode(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def ordered_times(values):
    values = list(values)
    if any(not math.isfinite(v) or v < 0 for v in values) or any(b <= a for a,b in zip(values,values[1:])):
        raise ValueError('event times must be finite, nonnegative and strictly increasing')
    return values


def match_events(reference, detected, tolerance):
    """Ordered one-to-one alignment: maximize matches, then minimize total error."""
    ref,det = ordered_times(reference),ordered_times(detected)
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError('tolerance must be finite and nonnegative')
    # Store (match_count, negative_error, matched_index_pairs). Deterministic
    # tie handling preserves the first equally optimal ordered alignment.
    dp = [[(0,0.0,()) for _ in range(len(det)+1)] for _ in range(len(ref)+1)]
    for i in range(1,len(ref)+1):
        for j in range(1,len(det)+1):
            choices = [dp[i-1][j],dp[i][j-1]]
            error = abs(ref[i-1]-det[j-1])
            if error <= tolerance:
                count,neg_error,pairs = dp[i-1][j-1]
                choices.append((count+1,neg_error-error,pairs+((i-1,j-1),)))
            dp[i][j] = max(choices,key=lambda x:(x[0],x[1]))
    return list(dp[-1][-1][2])


def event_metrics(reference, detected, tolerance):
    ref,det = ordered_times(reference),ordered_times(detected)
    pairs = match_events(ref,det,tolerance)
    tp = len(pairs)
    errors = [abs(ref[i]-det[j]) for i,j in pairs]
    return dict(true_positives=tp,false_positives=len(det)-tp,false_negatives=len(ref)-tp,
                precision=tp/len(det) if det else None,recall=tp/len(ref) if ref else None,
                f1=2*tp/(len(ref)+len(det)) if ref or det else None,
                timing_mae_seconds=sum(errors)/tp if tp else None)


def validate(config):
    for name in ('sample_rate_hz','duration_seconds','pulse_amplitude_g','pulse_width_seconds',
                 'min_interval_seconds','prominence_g','match_tolerance_seconds'):
        v=config[name]
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v <= 0:
            raise ValueError(name+' must be finite and positive')
    if type(config['sample_rate_hz']) is not int or config['sample_rate_hz'] < 10:
        raise ValueError('sample_rate_hz must be an integer >=10')
    if config['duration_seconds'] < 3:
        raise ValueError('duration_seconds must be >=3')
    for name in ('cadences_spm','noise_sd_g'):
        values=config[name]
        if not values or len(set(values))!=len(values):
            raise ValueError(name+' must be nonempty and unique')
        if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v < 0 for v in values):
            raise ValueError(name+' must contain finite nonnegative numbers')
    if any(v <= 0 or v >= config['sample_rate_hz']*30 for v in config['cadences_spm']):
        raise ValueError('cadences must be positive and have at least two samples per step')
    if type(config['seed']) is not int:
        raise ValueError('seed must be an integer')


def generate(config, cadence, noise):
    # Analytic pulse centers define truth independently of the detector.
    fs=config['sample_rate_hz']; count=round(config['duration_seconds']*fs)
    truth=[]; t=.75
    while t < config['duration_seconds']-.5:
        truth.append(t); t=.75+len(truth)*60/cadence
    rng=random.Random(config['seed'])
    samples=[1+sum(config['pulse_amplitude_g']*math.exp(-.5*((i/fs-t)/config['pulse_width_seconds'])**2)
                   for t in truth)+rng.gauss(0,noise) for i in range(count)]
    return truth,samples


def experiment():
    config_bytes=(ROOT/'config.json').read_bytes();config=json.loads(config_bytes);validate(config)
    stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(['cadence_spm','noise_sd_g','sample','time_seconds','acceleration_g','detected_step'])
    conditions=[];chart=[]
    for cadence in config['cadences_spm']:
        for noise in config['noise_sd_g']:
            truth,samples=generate(config,cadence,noise);fs=config['sample_rate_hz']
            indices=detect_steps(samples,fs,config['min_interval_seconds'],config['prominence_g']).tolist()
            times=[i/fs for i in indices]
            metrics=event_metrics(truth,times,config['match_tolerance_seconds'])
            summary=summarize_steps(indices,fs)
            metrics.update(summary)
            metrics['cadence_absolute_error_spm']=abs(summary['cadence_spm']-cadence) if summary['cadence_spm'] is not None else None
            condition=dict(cadence_spm=cadence,noise_sd_g=noise,reference_steps=len(truth),metrics=metrics)
            conditions.append(condition)
            marked=set(indices)
            for i,v in enumerate(samples):writer.writerow([cadence,noise,i,format(i/fs,'.12g'),format(v,'.12g'),int(i in marked)])
            chart.append(dict(cadence_spm=cadence,noise_sd_g=noise,reference_times=truth,detected_times=times,
                              samples=samples[:fs*5],sample_rate_hz=fs))
    data=stream.getvalue().encode()
    sources={name:digest((ROOT/name).read_bytes()) for name in ('pipeline.py','src/step_detection.py','src/gait_summary.py')}
    result=dict(schema_version=1,data_kind='synthetic',config=config,config_sha256=digest(config_bytes),
                source_sha256=sources['pipeline.py'],source_files_sha256=sources,data_sha256=digest(data),
                conditions=conditions,chart=chart,
                limitations='Gaussian pulse acceleration surrogate with known event centers. Not measured walking, participant validation or clinical fall-risk prediction.')
    report='# Synthetic gait event benchmark\n\nKnown pulse centers are reference events. All values below are measured by the detector; no clinical validity is claimed.\n\n'
    report+='| Cadence (steps/min) | Noise SD (g) | TP | FP | FN | F1 | Timing MAE (s) | Cadence error (steps/min) |\n|---|---|---|---|---|---|---|---|\n'
    show=lambda x:'undefined' if x is None else format(x,'.4g')
    for c in conditions:
        m=c['metrics']
        report+='| '+' | '.join(show(x) for x in [c['cadence_spm'],c['noise_sd_g'],m['true_positives'],m['false_positives'],m['false_negatives'],m['f1'],m['timing_mae_seconds'],m['cadence_absolute_error_spm']])+' |\n'
    report+='\nOne-to-one matching maximizes event matches within the fixed tolerance, then minimizes total absolute timing error. Cadence uses the interval between detected steps, not total record duration. See DATA_PROVENANCE.md for assumptions, source versions and limitations.\n'
    result_bytes=encode(result)
    report+='\nResult SHA-256: `'+digest(result_bytes)+'`\n'
    files={'data.csv':data,'results.json':result_bytes,'report.md':report.encode()}
    files['manifest.json']=encode({name:digest(content) for name,content in files.items()})
    return files


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true')
    parser.add_argument('--output',type=Path,default=ROOT/'results');args=parser.parse_args()
    files=experiment()
    if args.verify:
        for name,content in files.items():
            if not (args.output/name).exists() or (args.output/name).read_bytes()!=content:
                raise SystemExit('Verification failed: '+name)
        print('Verified all synthetic gait data, metrics, report and checksums')
    else:
        args.output.mkdir(parents=True,exist_ok=True)
        for name,content in files.items():(args.output/name).write_bytes(content)
        print('Generated synthetic gait benchmark')

if __name__=='__main__':main()
