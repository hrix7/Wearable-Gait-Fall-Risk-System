import json,unittest
from pathlib import Path
import pipeline as p
class GapReplicateTests(unittest.TestCase):
 def test_each_gap_reconstructs_from_paired_signal_and_two_truth_populations(self):
  c=json.loads(Path('config.json').read_text());r=p.noise_replicate_probe(c,120,.06,seeds=[12,13])
  for row in r['replicates']:
   truth,x=p.generate({**c,'seed':row['seed']},120,.06);fs=c['sample_rate_hz'];a=.4*c['duration_seconds'];b=.5*c['duration_seconds']
   gap=[1.0 if a<=i/fs<b else v for i,v in enumerate(x)]
   self.assertEqual(row['gap']['signal_sha256'],p.digest(p.encode(gap)))
   times=[i/fs for i in p.detect_steps(gap,fs,c['min_interval_seconds'],c['prominence_g'])]
   present=[t for t in truth if not a<=t<b]
   self.assertEqual(row['gap']['nominal_metrics'],p.event_metrics(truth,times,c['match_tolerance_seconds']))
   self.assertEqual(row['gap']['present_metrics'],p.event_metrics(present,times,c['match_tolerance_seconds']))
   self.assertEqual(row['gap']['present_reference_count'],len(present))
   self.assertEqual(row['gap']['nominal_reference_count'],len(truth))
