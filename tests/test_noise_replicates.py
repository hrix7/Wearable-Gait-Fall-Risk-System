import copy,hashlib,json,unittest
import pipeline as p
class NoiseReplicateTests(unittest.TestCase):
 def setUp(self):self.c=json.loads((p.ROOT/'config.json').read_text())
 def test_recompute_each_seed_metrics_and_summary_without_config_mutation(self):
  before=copy.deepcopy(self.c);seeds=[8001,8002,8003];r=p.noise_replicate_probe(self.c,120,.12,seeds)
  values=[];truths=[]
  for row in r['replicates']:
   truth,x=p.generate({**self.c,'seed':row['seed']},120,.12);truths.append(truth)
   idx=p.detect_steps(x,self.c['sample_rate_hz'],self.c['min_interval_seconds'],self.c['prominence_g'])
   m=p.event_metrics(truth,[i/self.c['sample_rate_hz'] for i in idx],self.c['match_tolerance_seconds'])
   self.assertEqual(m,row['metrics']);values.append(m['f1']);self.assertEqual(row['signal_sha256'],hashlib.sha256(p.encode(x)).hexdigest())
  self.assertTrue(all(t==truths[0] for t in truths));self.assertEqual(self.c,before)
  self.assertEqual(r['f1_mean'],sum(values)/3);self.assertEqual((r['f1_min'],r['f1_max']),(min(values),max(values)))
  self.assertEqual(len({r['signal_sha256'] for r in r['replicates']}),3)
 def test_zero_noise_is_seed_invariant_and_default_seed_grid_is_fixed(self):
  r=p.noise_replicate_probe(self.c,120,0)
  self.assertEqual([r['seed'] for r in r['replicates']],list(range(self.c['seed']+1000,self.c['seed']+1010)))
  self.assertEqual(len({r['signal_sha256'] for r in r['replicates']}),1)
 def test_bad_seed_specification(self):
  for seeds in [[],[1],[1,1],[True,2],iter([1,2])]:
   with self.assertRaises(ValueError):p.noise_replicate_probe(self.c,120,.12,seeds)
