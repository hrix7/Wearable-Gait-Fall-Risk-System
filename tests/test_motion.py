import hashlib,json,math,unittest
import pipeline as p
class MotionTests(unittest.TestCase):
 def test_envelope_analytic_samples_bound_and_nonmutation(self):
  samples=[1.]*200;fs=20;actual=p.motion_burst(samples,fs,2,6)
  for i,v in enumerate(actual):
   t=i/fs;expected=.4*math.sin(2*math.pi*2.7*(t-2))*math.sin(math.pi*(t-2)/4)**2 if 2<=t<6 else 0
   self.assertAlmostEqual(v-1,expected,places=14);self.assertLessEqual(abs(v-1),.4+1e-14)
  self.assertEqual(samples,[1.]*200);self.assertEqual(actual[40],1);self.assertEqual(actual[120],1)
  self.assertEqual(p.motion_burst(samples,fs,2,6,amplitude=0),samples)
 def test_invalid_windows_amplitudes_and_aliasing_rejected(self):
  for kwargs in [dict(start=-1),dict(end=20),dict(amplitude=-1),dict(frequency=10),dict(fs=0),dict(amplitude=float('nan'))]:
   args=dict(fs=20,start=2,end=6);args.update(kwargs)
   with self.assertRaises(ValueError):p.motion_burst([1.]*200,**args)
 def test_export_reconstructs_hashes_and_independent_truth(self):
  r=json.loads(p.experiment()['results.json']);self.assertEqual(len(r['motion_conditions']),9)
  protocol=r['motion_protocol']
  for row in r['motion_conditions']:
   truth,base=p.generate(r['config'],row['cadence_spm'],row['noise_sd_g']);fs=r['config']['sample_rate_hz']
   x=p.motion_burst(base,fs,protocol['start_seconds'],protocol['end_seconds'],protocol['amplitude_g'],protocol['frequency_hz'])
   self.assertEqual(row['signal_sha256'],hashlib.sha256(p.encode(x)).hexdigest())
   for detector,key in [(lambda:p.detect_steps(x,fs,r['config']['min_interval_seconds'],r['config']['prominence_g']),'metrics'),(lambda:p.fixed_height_baseline(x,fs,r['config']['min_interval_seconds']),'fixed_height_baseline_metrics')]:
    self.assertEqual(row[key],p.event_metrics(truth,[i/fs for i in detector()],r['config']['match_tolerance_seconds']))
