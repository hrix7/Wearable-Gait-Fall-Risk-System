import unittest,json,math,hashlib
from pathlib import Path
import pipeline as p
class JitterTests(unittest.TestCase):
 def setUp(self):self.c=json.loads((p.ROOT/'config.json').read_text())
 def test_bounded_ordered_repeatable_event_truth(self):
  nominal,_=p.generate(self.c,120,0);truth,x=p.generate(self.c,120,.06,.06)
  self.assertTrue(all(abs(a-b)<=.06 for a,b in zip(nominal,truth)))
  self.assertNotEqual(nominal,truth);self.assertEqual((truth,x),p.generate(self.c,120,.06,.06))
  self.assertTrue(all(a<b for a,b in zip(truth,truth[1:])))
 def test_noise_channel_independent_of_jitter(self):
  _,a=p.generate(self.c,120,.06,0);_,b=p.generate(self.c,120,0,0)
  _,c=p.generate(self.c,120,.06,.06);_,d=p.generate(self.c,120,0,.06)
  for aa,bb,cc,dd in zip(a,b,c,d):self.assertAlmostEqual(aa-bb,cc-dd,places=13)
 def test_noiseless_jitter_recovery_and_invalid_width(self):
  ref,x=p.generate(self.c,120,0,.06);idx=p.detect_steps(x,50)
  self.assertEqual(p.event_metrics(ref,[i/50 for i in idx],.15)['f1'],1)
  for width in (-1,float('nan'),.125):
   with self.assertRaises(ValueError):p.generate(self.c,120,0,width)
 def test_jitter_samples_have_manifest_and_result_fingerprint(self):
  files=p.experiment();r=json.loads(files['results.json']);m=json.loads(files['manifest.json'])
  self.assertEqual(len(r['jitter_conditions']),9)
  digest=hashlib.sha256(files['jitter_data.csv']).hexdigest()
  self.assertEqual(r['jitter_data_sha256'],digest);self.assertEqual(m['jitter_data.csv'],digest)
