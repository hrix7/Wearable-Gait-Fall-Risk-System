import unittest,math
from gait_summary import summarize_steps
class VariabilityTests(unittest.TestCase):
 def test_single_interval_does_not_claim_sample_variability(self):
  r=summarize_steps([0,50],50);self.assertEqual(r['interval_count'],1)
  self.assertEqual(r['interval_cv_percent'],0);self.assertIsNone(r['sample_interval_cv_percent'])
 def test_sample_and_population_cv_have_explicit_distinct_denominators(self):
  r=summarize_steps([0,10,30],10)
  self.assertEqual(r['interval_count'],2);self.assertAlmostEqual(r['interval_cv_percent'],100/3)
  self.assertAlmostEqual(r['sample_interval_cv_percent'],100*math.sqrt(.5)/1.5)
 def test_too_few_steps_expose_zero_intervals(self):
  for indices in ([],[20]):
   r=summarize_steps(indices,50);self.assertEqual(r['interval_count'],0);self.assertIsNone(r['sample_interval_cv_percent'])
