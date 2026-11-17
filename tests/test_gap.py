import unittest,json,hashlib
import pipeline as p
class GapTests(unittest.TestCase):
 def test_mask_boundary_and_unmodified_samples(self):
  original=[2.,3.,4.,5.];out=p.flatten_gap(original,2,.5,1.5)
  self.assertEqual(out,[2.,1.,1.,5.]);self.assertEqual(original,[2.,3.,4.,5.])
 def test_invalid_gap_rejected(self):
  for a,b in [(-1,1),(1,1),(0,3),(0,float('nan'))]:
   with self.assertRaises(ValueError):p.flatten_gap([1,2,3,4],2,a,b)
 def test_export_has_separate_reference_populations_and_reproducible_signal_hash(self):
  r=json.loads(p.experiment()['results.json']);self.assertEqual(len(r['gap_conditions']),9)
  for row in r['gap_conditions']:
   truth,x=p.generate(r['config'],row['cadence_spm'],row['noise_sd_g']);masked=p.flatten_gap(x,r['config']['sample_rate_hz'],row['gap_start_seconds'],row['gap_end_seconds'])
   self.assertEqual(row['signal_sha256'],hashlib.sha256(p.encode(masked)).hexdigest())
   self.assertEqual(row['nominal_reference_count']-row['present_reference_count'],row['reference_centers_in_gap'])
   for name,n in [('nominal_event_metrics',row['nominal_reference_count']),('present_event_metrics',row['present_reference_count'])]:
    self.assertEqual(row[name]['true_positives']+row[name]['false_negatives'],n)
