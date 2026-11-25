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


def generate(config, cadence, noise, jitter_half_width=0):
    # Analytic pulse centers define truth independently of the detector.
    fs=config['sample_rate_hz']; count=round(config['duration_seconds']*fs)
    truth=[]; t=.75
    while t < config['duration_seconds']-.5:
        truth.append(t); t=.75+len(truth)*60/cadence
    if not math.isfinite(jitter_half_width) or jitter_half_width<0 or jitter_half_width>=min(.25*60/cadence,.25):
        raise ValueError('jitter must be nonnegative, finite and smaller than quarter-period and 0.25 s')
    if jitter_half_width:
        timing_rng=random.Random(config['seed']+1)
        truth=[t+timing_rng.uniform(-jitter_half_width,jitter_half_width) for t in truth]
    rng=random.Random(config['seed'])
    samples=[1+sum(config['pulse_amplitude_g']*math.exp(-.5*((i/fs-t)/config['pulse_width_seconds'])**2)
                   for t in truth)+rng.gauss(0,noise) for i in range(count)]
    return truth,samples


def fixed_height_baseline(samples, fs, interval):
    """Predeclared 0.125 g height above median, chronological refractory rule.

    Independent of SciPy prominence; illustrative baseline, not tuned on results.
    """
    import statistics
    if len(samples)<3 or any(not math.isfinite(v) for v in samples):
        raise ValueError('finite samples required')
    if not math.isfinite(fs) or fs<=0 or not math.isfinite(interval) or interval<=0:
        raise ValueError('finite positive sampling and interval required')
    threshold=statistics.median(samples)+.125
    distance=max(1,math.ceil(fs*interval));indices=[]
    for i in range(1,len(samples)-1):
        if samples[i]>samples[i-1] and samples[i]>=samples[i+1] and samples[i]>=threshold and (not indices or i-indices[-1]>=distance):
            indices.append(i)
    return indices

def flatten_gap(samples,fs,start,end):
    if not samples or any(not math.isfinite(v) for v in samples) or any(not math.isfinite(v) for v in (fs,start,end)) or fs<=0 or not 0<=start<end<=len(samples)/fs:
        raise ValueError('finite signal and bounded positive gap interval required')
    return [1.0 if start<=i/fs<end else v for i,v in enumerate(samples)]

def motion_burst(samples,fs,start,end,amplitude=.4,frequency=2.7):
    if not samples or any(not math.isfinite(v) for v in samples) or any(not math.isfinite(v) for v in (fs,start,end,amplitude,frequency)) or fs<=0 or not 0<=start<end<=len(samples)/fs or amplitude<0 or not 0<frequency<fs/2:
        raise ValueError('finite signal, bounded window, nonnegative amplitude and interior frequency required')
    return [v+amplitude*math.sin(2*math.pi*frequency*(i/fs-start))*math.sin(math.pi*(i/fs-start)/(end-start))**2 if start<=i/fs<end else v for i,v in enumerate(samples)]

def paired_gap_summary(records):
    summaries={}
    for name in ('nominal','present'):
        values=[r['metrics']['f1']-r['gap'][name+'_metrics']['f1'] for r in records if r['metrics']['f1'] is not None and r['gap'][name+'_metrics']['f1'] is not None]
        summaries[name]=dict(defined_pairs=len(values),mean_original_minus_gap=sum(values)/len(values) if values else None,minimum=min(values) if values else None,maximum=max(values) if values else None)
    return summaries

def noise_replicate_probe(config,cadence,noise,seeds=None):
    seeds=list(range(config['seed']+1000,config['seed']+1010)) if seeds is None else seeds
    if not isinstance(seeds,(list,tuple)) or len(seeds)<2 or any(type(seed) is not int for seed in seeds) or len(set(seeds))!=len(seeds):
        raise ValueError('at least two unique integer noise seeds required')
    records=[]
    for seed in seeds:
        truth,x=generate({**config,'seed':seed},cadence,noise);fs=config['sample_rate_hz']
        idx=detect_steps(x,fs,config['min_interval_seconds'],config['prominence_g']).tolist()
        motion=motion_burst(x,fs,.3*config['duration_seconds'],.6*config['duration_seconds'])
        motion_idx=detect_steps(motion,fs,config['min_interval_seconds'],config['prominence_g']).tolist()
        motion_metrics=event_metrics(truth,[i/fs for i in motion_idx],config['match_tolerance_seconds'])
        start=.4*config['duration_seconds'];end=.5*config['duration_seconds']
        gap=flatten_gap(x,fs,start,end)
        gap_idx=detect_steps(gap,fs,config['min_interval_seconds'],config['prominence_g']).tolist()
        present=[t for t in truth if not start<=t<end]
        gap_baseline=fixed_height_baseline(gap,fs,config['min_interval_seconds'])
        gap_record=dict(fixed_height_nominal_metrics=event_metrics(truth,[i/fs for i in gap_baseline],config['match_tolerance_seconds']),fixed_height_present_metrics=event_metrics(present,[i/fs for i in gap_baseline],config['match_tolerance_seconds']),signal_sha256=digest(encode(gap)),nominal_reference_count=len(truth),present_reference_count=len(present),nominal_metrics=event_metrics(truth,[i/fs for i in gap_idx],config['match_tolerance_seconds']),present_metrics=event_metrics(present,[i/fs for i in gap_idx],config['match_tolerance_seconds']))
        records.append(dict(gap=gap_record,seed=seed,signal_sha256=digest(encode(x)),motion_signal_sha256=digest(encode(motion)),motion_f1=motion_metrics['f1'],metrics=event_metrics(truth,[i/fs for i in idx],config['match_tolerance_seconds'])))
    values=[row['metrics']['f1'] for row in records];defined=[v for v in values if v is not None]
    deltas=[row['metrics']['f1']-row['motion_f1'] for row in records if row['metrics']['f1'] is not None and row['motion_f1'] is not None]
    return dict(gap_paired_delta=paired_gap_summary(records),motion_paired_delta=dict(defined_pairs=len(deltas),mean_original_minus_motion=sum(deltas)/len(deltas) if deltas else None,minimum=min(deltas) if deltas else None,maximum=max(deltas) if deltas else None),cadence_spm=cadence,noise_sd_g=noise,replicates=records,defined_f1_count=len(defined),f1_mean=sum(defined)/len(defined) if defined else None,f1_min=min(defined) if defined else None,f1_max=max(defined) if defined else None)

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
            baseline=fixed_height_baseline(samples,fs,config['min_interval_seconds'])
            condition['fixed_height_baseline_metrics']=event_metrics(truth,[i/fs for i in baseline],config['match_tolerance_seconds'])
            conditions.append(condition)
            marked=set(indices)
            for i,v in enumerate(samples):writer.writerow([cadence,noise,i,format(i/fs,'.12g'),format(v,'.12g'),int(i in marked)])
            chart.append(dict(cadence_spm=cadence,noise_sd_g=noise,reference_times=truth,detected_times=times,
                              samples=samples[:fs*5],sample_rate_hz=fs))
    jitter_stream=io.StringIO(newline='');jitter_writer=csv.writer(jitter_stream,lineterminator='\n')
    jitter_writer.writerow(['cadence_spm','noise_sd_g','sample','time_seconds','acceleration_g'])
    jitter_conditions=[]
    for cadence in config['cadences_spm']:
        for noise in config['noise_sd_g']:
            jitter=min(.06,.2*60/cadence);truth,samples=generate(config,cadence,noise,jitter)
            fs=config['sample_rate_hz'];idx=detect_steps(samples,fs,config['min_interval_seconds'],config['prominence_g']).tolist()
            baseline=fixed_height_baseline(samples,fs,config['min_interval_seconds'])
            jitter_conditions.append(dict(cadence_spm=cadence,noise_sd_g=noise,jitter_half_width_seconds=jitter,reference_times=truth,detected_times=[i/fs for i in idx],metrics=event_metrics(truth,[i/fs for i in idx],config['match_tolerance_seconds']),fixed_height_baseline_metrics=event_metrics(truth,[i/fs for i in baseline],config['match_tolerance_seconds'])))
            for i,v in enumerate(samples):jitter_writer.writerow([cadence,noise,i,format(i/fs,'.12g'),format(v,'.12g')])
    gap_conditions=[];start=.4*config['duration_seconds'];end=.5*config['duration_seconds']
    for cadence in config['cadences_spm']:
        for noise in config['noise_sd_g']:
            truth,samples=generate(config,cadence,noise);fs=config['sample_rate_hz'];masked=flatten_gap(samples,fs,start,end)
            idx=detect_steps(masked,fs,config['min_interval_seconds'],config['prominence_g']).tolist();times=[i/fs for i in idx]
            present=[t for t in truth if not start<=t<end]
            gap_conditions.append(dict(cadence_spm=cadence,noise_sd_g=noise,gap_start_seconds=start,gap_end_seconds=end,nominal_reference_count=len(truth),present_reference_count=len(present),reference_centers_in_gap=len(truth)-len(present),signal_sha256=digest(encode(masked)),nominal_event_metrics=event_metrics(truth,times,config['match_tolerance_seconds']),present_event_metrics=event_metrics(present,times,config['match_tolerance_seconds'])))
    motion_conditions=[];motion_start=.3*config['duration_seconds'];motion_end=.6*config['duration_seconds']
    for cadence in config['cadences_spm']:
        for noise in config['noise_sd_g']:
            truth,samples=generate(config,cadence,noise);fs=config['sample_rate_hz']
            perturbed=motion_burst(samples,fs,motion_start,motion_end)
            idx=detect_steps(perturbed,fs,config['min_interval_seconds'],config['prominence_g']).tolist()
            baseline=fixed_height_baseline(perturbed,fs,config['min_interval_seconds'])
            motion_conditions.append(dict(cadence_spm=cadence,noise_sd_g=noise,signal_sha256=digest(encode(perturbed)),metrics=event_metrics(truth,[i/fs for i in idx],config['match_tolerance_seconds']),fixed_height_baseline_metrics=event_metrics(truth,[i/fs for i in baseline],config['match_tolerance_seconds'])))
    jitter_data=jitter_stream.getvalue().encode()
    data=stream.getvalue().encode()
    sources={name:digest((ROOT/name).read_bytes()) for name in ('pipeline.py','src/step_detection.py','src/gait_summary.py')}
    result=dict(schema_version=1,data_kind='synthetic',config=config,config_sha256=digest(config_bytes),
                source_sha256=sources['pipeline.py'],source_files_sha256=sources,data_sha256=digest(data),
                conditions=conditions,chart=chart,jitter_conditions=jitter_conditions,jitter_data_sha256=digest(jitter_data),
                jitter_protocol='Independent seed+1 uniform event offsets; half-width min(0.06 s, 0.2 periods); nominal cadence labels remain generator settings. Noise seed/channel unchanged; actual perturbed centers are truth.',
                noise_replicate_conditions=[noise_replicate_probe(config,cadence,noise) for cadence in config['cadences_spm'] for noise in config['noise_sd_g']],noise_replicate_protocol='Ten predeclared noise seeds seed+1000 through seed+1009 per cadence/noise cell, fixed regular event times and detector. Within-cell noise-only sensitivity, not subject/population uncertainty or confidence intervals. Seed realizations are paired across cells; do not pool cells as independent samples. Exact signals regenerate from config and each stored seed. Each replicate also adds the fixed motion burst to the same signal; original-minus-motion F1 summaries preserve pairing and may be negative. No confidence intervals or subject-population inference.',motion_conditions=motion_conditions,motion_protocol=dict(start_seconds=motion_start,end_seconds=motion_end,amplitude_g=.4,frequency_hz=2.7,definition='Add amplitude*sin(2*pi*frequency*(t-start))*sin(pi*(t-start)/(end-start))**2 on [start,end), zero elsewhere. Original event times and paired noise remain unchanged. Teaching motion surrogate, not measured biomechanics; reconstruct full-precision hashes from generator/config.'),gap_conditions=gap_conditions,signal_gap_protocol='Base regular-timing signals have samples in [0.4*duration,0.5*duration) replaced by constant 1 g, timestamps retained. This is a finite flattening surrogate, not real missing-value handling. Reproduce full-precision masked signals from the generator/config and stated mask. Base data.csv is rounded and does not reproduce full-precision signal hashes. Nominal references include gap centers; present references exclude them. Boundary/filter peaks can match nominal slots without recovering signal.',
                summary_interpretation='interval_cv_percent retains population SD (ddof=0). sample_interval_cv_percent uses sample SD (ddof=1) only with >=2 intervals; interval_count makes sample size explicit. Neither estimates clinical fall risk.',
                limitations='Gaussian pulse acceleration surrogate with known event centers. Not measured walking, participant validation or clinical fall-risk prediction.')
    report='# Synthetic gait event benchmark\n\nKnown pulse centers are reference events. All values below are measured by the detector; no clinical validity is claimed.\n\n'
    report+='| Cadence (steps/min) | Noise SD (g) | TP | FP | FN | F1 | Timing MAE (s) | Cadence error (steps/min) |\n|---|---|---|---|---|---|---|---|\n'
    show=lambda x:'undefined' if x is None else format(x,'.4g')
    for c in conditions:
        m=c['metrics']
        report+='| '+' | '.join(show(x) for x in [c['cadence_spm'],c['noise_sd_g'],m['true_positives'],m['false_positives'],m['false_negatives'],m['f1'],m['timing_mae_seconds'],m['cadence_absolute_error_spm']])+' |\n'
    report+='\nOne-to-one matching maximizes event matches within the fixed tolerance, then minimizes total absolute timing error. Cadence uses the interval between detected steps, not total record duration. See DATA_PROVENANCE.md for assumptions, source versions and limitations.\n'
    report+='\n## Independent fixed-height baseline\n\nPredeclared threshold: 0.125 g above record median, local maxima, chronological refractory spacing identical to the main detector. No evaluation-grid tuning. Not a clinical comparator.\n\n| Cadence | Noise SD | Baseline FP | Baseline FN | Baseline F1 |\n|---|---|---|---|---|\n'
    for c in conditions:
        b=c['fixed_height_baseline_metrics']
        report+='| '+' | '.join(show(v) for v in [c['cadence_spm'],c['noise_sd_g'],b['false_positives'],b['false_negatives'],b['f1']])+' |\n'
    report+='\n## Bounded timing jitter\n\nReference centers have independent-seed uniform offsets (half-width min(0.06 s, 0.2 periods)); observation noise stream is unchanged. Actual perturbed centers define truth, not a regular schedule. Full samples are in jitter_data.csv.\n\n| Nominal cadence | Noise SD | Half-width (s) | FP | FN | F1 |\n|---|---|---|---|---|---|\n'
    for c in jitter_conditions:
        m=c['metrics'];report+='| '+' | '.join(show(v) for v in [c['cadence_spm'],c['noise_sd_g'],c['jitter_half_width_seconds'],m['false_positives'],m['false_negatives'],m['f1']])+' |\n'
    report+='\n## Flattened-signal gap probe\n\nA separate finite dropout surrogate replaces [0.4T,0.5T) with 1 g. Nominal-reference misses include intentionally masked pulse centers; present-reference misses exclude them. This does not validate handling of real missing values. Reproduce from the regular generator and stated mask.\n\n| Cadence | Noise SD | Reference centers in gap | Nominal FN | Present FN | Present FP |\n|---|---|---|---|---|---|\n'
    for c in gap_conditions:
        report+='| '+' | '.join(show(v) for v in [c['cadence_spm'],c['noise_sd_g'],c['reference_centers_in_gap'],c['nominal_event_metrics']['false_negatives'],c['present_event_metrics']['false_negatives'],c['present_event_metrics']['false_positives']])+' |\n'
    report+='\n## Additive motion-burst probe\n\nIndependent additive 0.4 g, 2.7 Hz sinusoid under a sin-squared envelope on [0.3T,0.6T). Event truth and paired base noise remain unchanged. Teaching perturbation, not participant motion validation.\n\n| Cadence | Noise SD | Extra | Missed | Prominence F1 | Fixed-height F1 |\n|---|---|---|---|---|---|\n'
    for c in motion_conditions:
        m=c['metrics'];report+='| '+' | '.join(show(v) for v in [c['cadence_spm'],c['noise_sd_g'],m['false_positives'],m['false_negatives'],m['f1'],c['fixed_height_baseline_metrics']['f1']])+' |\n'
    report+='\n## Independent noise realizations\n\nTen predeclared noise seeds per fixed cadence/noise cell; same analytic event times and detector. Descriptive noise-only F1 range/mean, not a confidence interval or subject variability. Noise realizations are paired across cells.\n\n| Cadence | Noise SD | Defined F1 replicates | Mean F1 | Min F1 | Max F1 |\n|---|---|---|---|---|---|\n'
    for c in result['noise_replicate_conditions']:
        report+='| '+' | '.join(show(v) for v in [c['cadence_spm'],c['noise_sd_g'],c['defined_f1_count'],c['f1_mean'],c['f1_min'],c['f1_max']])+' |\n'
    result_bytes=encode(result)
    report+='\nResult SHA-256: `'+digest(result_bytes)+'`\n'
    files={'data.csv':data,'jitter_data.csv':jitter_data,'results.json':result_bytes,'report.md':report.encode()}
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
