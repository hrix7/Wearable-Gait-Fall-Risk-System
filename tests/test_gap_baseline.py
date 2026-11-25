import json,unittest
from pathlib import Path
import pipeline as p
class GapBaselineTests(unittest.TestCase):
 def test_both_reference_populations_use_same_baseline_detections(self):
  c=json.loads(Path('config.json').read_text());rows=p.noise_replicate_probe(c,120,.06,seeds=[7,8])['replicates']
  for row in rows:
   truth,x=p.generate({**c,'seed':row['seed']},120,.06);fs=c['sample_rate_hz'];a=.4*c['duration_seconds'];b=.5*c['duration_seconds'];gap=[1.0 if a<=i/fs<b else v for i,v in enumerate(x)];present=[t for t in truth if not a<=t<b]
   times=[i/fs for i in p.fixed_height_baseline(gap,fs,c['min_interval_seconds'])]
   self.assertEqual(row['gap']['fixed_height_nominal_metrics'],p.event_metrics(truth,times,c['match_tolerance_seconds']))
   self.assertEqual(row['gap']['fixed_height_present_metrics'],p.event_metrics(present,times,c['match_tolerance_seconds']))
 def test_original_zero_noise_baseline_still_has_finite_scores(self):
  c=json.loads(Path('config.json').read_text());r=p.noise_replicate_probe(c,120,0,seeds=[7,8])
  for row in r['replicates']:
   for name in ['fixed_height_nominal_metrics','fixed_height_present_metrics']:self.assertTrue(0<=row['gap'][name]['f1']<=1)
