import unittest,math,json
from pathlib import Path
import pipeline as p
class BaselineTests(unittest.TestCase):
 def test_chronological_refractory_and_plateau_first_sample(self):
  self.assertEqual(p.fixed_height_baseline([0,1,1,0,0,2,0],10,.31),[1,5])
  self.assertEqual(p.fixed_height_baseline([0,1,0,2,0],10,.31),[1])
 def test_offset_invariance_and_noiseless_recovery(self):
  self.assertEqual(p.fixed_height_baseline([100,101,100,100],50,.3),[1])
  c=json.loads((Path(p.ROOT)/'config.json').read_text());ref,x=p.generate(c,120,0)
  pred=p.fixed_height_baseline(x,50,.3)
  m=p.event_metrics(ref,[i/50 for i in pred],.15);self.assertEqual(m['f1'],1)
 def test_invalid_and_flat(self):
  self.assertEqual(p.fixed_height_baseline([1]*10,50,.3),[])
  for x,fs,dt in [([1,float('nan'),1],50,.3),([1,2,1],0,.3),([1,2,1],50,-1)]:
   with self.assertRaises(ValueError):p.fixed_height_baseline(x,fs,dt)
