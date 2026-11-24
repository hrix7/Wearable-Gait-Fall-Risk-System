import unittest
import pipeline as p
class GapSummaryTests(unittest.TestCase):
 def test_paired_sign_and_distinct_reference_populations(self):
  rows=[dict(metrics={'f1':.6},gap={'nominal_metrics':{'f1':.2},'present_metrics':{'f1':.8}}),dict(metrics={'f1':1.0},gap={'nominal_metrics':{'f1':.6},'present_metrics':{'f1':1.0}})]
  r=p.paired_gap_summary(rows)
  self.assertAlmostEqual(r['nominal']['mean_original_minus_gap'],.4)
  self.assertAlmostEqual(r['present']['mean_original_minus_gap'],-.1)
  self.assertEqual(r['nominal']['defined_pairs'],2)
 def test_undefined_pairs_do_not_become_zero(self):
  rows=[dict(metrics={'f1':None},gap={'nominal_metrics':{'f1':1},'present_metrics':{'f1':1}})]
  r=p.paired_gap_summary(rows)
  for v in r.values():self.assertEqual(v,dict(defined_pairs=0,mean_original_minus_gap=None,minimum=None,maximum=None))
