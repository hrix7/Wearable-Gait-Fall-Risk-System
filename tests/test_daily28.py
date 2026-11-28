import unittest
import pipeline as p
class PairedDetectors(unittest.TestCase):
 def record(self,a,b):
  return dict(gap={key:dict(f1=value) for key,value in [('nominal_metrics',a),('present_metrics',b),('fixed_height_nominal_metrics',b),('fixed_height_present_metrics',a)]})
 def test_pairing_sign_counts_and_undefined(self):
  result=p.paired_detector_summary([self.record(.75,.5),self.record(.25,.5),self.record(.5,.5),self.record(None,.5)])
  for row in result.values():
   self.assertEqual(row['defined_pairs'],3);self.assertEqual(row['mean_prominence_minus_fixed_height_f1'],0)
   self.assertEqual((row['prominence_higher'],row['fixed_height_higher'],row['ties']),(1,1,1))
   self.assertEqual((row['minimum'],row['maximum']),(-.25,.25))
  self.assertIsNone(p.paired_detector_summary([])['nominal']['minimum'])
 def test_invalid_f1(self):
  for v in (True,-.1,1.1,float('nan')):
   with self.assertRaises(ValueError):p.paired_detector_summary([self.record(v,.5)])
