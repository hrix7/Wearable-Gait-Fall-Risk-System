import hashlib,json,unittest
from unittest.mock import patch
import pipeline as p
class PairedMotionTests(unittest.TestCase):
 def setUp(self):self.c=json.loads((p.ROOT/'config.json').read_text())
 def test_each_motion_hash_f1_and_paired_summary_recompute(self):
  r=p.noise_replicate_probe(self.c,120,.12,[91,92]);deltas=[]
  for row in r['replicates']:
   truth,x=p.generate({**self.c,'seed':row['seed']},120,.12);fs=self.c['sample_rate_hz'];motion=p.motion_burst(x,fs,.3*self.c['duration_seconds'],.6*self.c['duration_seconds'])
   idx=p.detect_steps(motion,fs,self.c['min_interval_seconds'],self.c['prominence_g'])
   f1=p.event_metrics(truth,[i/fs for i in idx],self.c['match_tolerance_seconds'])['f1']
   self.assertEqual(row['motion_f1'],f1);self.assertEqual(row['motion_signal_sha256'],hashlib.sha256(p.encode(motion)).hexdigest());deltas.append(row['metrics']['f1']-f1)
  self.assertEqual(r['motion_paired_delta'],dict(defined_pairs=2,mean_original_minus_motion=sum(deltas)/2,minimum=min(deltas),maximum=max(deltas)))
 def test_identity_perturbation_has_exactly_zero_paired_delta(self):
  with patch.object(p,'motion_burst',side_effect=lambda x,*args:x):r=p.noise_replicate_probe(self.c,120,.12,[91,92])
  self.assertEqual(r['motion_paired_delta']['mean_original_minus_motion'],0)
  for row in r['replicates']:self.assertEqual(row['signal_sha256'],row['motion_signal_sha256'])
