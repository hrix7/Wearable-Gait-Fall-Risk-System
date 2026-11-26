import unittest
import pipeline as p
class GapSummaryContractTests(unittest.TestCase):
 def test_nonfinite_and_out_of_range_f1_cannot_form_summary(self):
  for bad in (float('nan'),float('inf'),-.1,1.1,True,'0.5'):
   for field in ('original','nominal','present'):
    row=dict(metrics={'f1':.5},gap={'nominal_metrics':{'f1':.5},'present_metrics':{'f1':.5}})
    (row['metrics'] if field=='original' else row['gap'][field+'_metrics'])['f1']=bad
    with self.assertRaises(ValueError):p.paired_gap_summary([row])
 def test_incomplete_records_fail_and_empty_is_explicit(self):
  for rows in (None,[{}],[{'metrics':None}]):
   with self.assertRaises(ValueError):p.paired_gap_summary(rows)
  for value in p.paired_gap_summary([]).values():self.assertEqual(value['defined_pairs'],0);self.assertIsNone(value['mean_original_minus_gap'])
