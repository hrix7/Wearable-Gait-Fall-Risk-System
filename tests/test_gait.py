import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'src'))
import pipeline as p
from step_detection import detect_steps
from gait_summary import summarize_steps

class DetectorTests(unittest.TestCase):
    def test_hand_annotated_peaks(self):
        self.assertEqual(detect_steps([0,1,0,0,2,0,0,1,0],10,.2,.5).tolist(),[1,4,7])
    def test_constant_signal_has_no_steps(self):
        self.assertEqual(detect_steps([1]*100,50).tolist(),[])
    def test_invalid_detector_inputs(self):
        for data,fs,interval,prom in [([0,float('nan'),0],50,.3,.15),([0,1,0],0,.3,.15),
                                      ([0,1,0],float('inf'),.3,.15),([0,1,0],50,-1,.15),([0,1,0],50,.3,-1)]:
            with self.subTest(data=data,fs=fs):
                with self.assertRaises(ValueError):detect_steps(data,fs,interval,prom)
    def test_interval_is_not_rounded_down(self):
        signal=[0,2,0,0,1,0]
        self.assertEqual(detect_steps(signal,10,.31,.5).tolist(),[1])

class SummaryTests(unittest.TestCase):
    def test_known_cadence(self):
        result=summarize_steps([0,25,50,75],50)
        self.assertEqual(result['cadence_spm'],120)
        self.assertEqual(result['interval_cv_percent'],0)
    def test_too_few_events_are_undefined(self):
        for indices in ([],[10]):self.assertIsNone(summarize_steps(indices,50)['cadence_spm'])
    def test_invalid_indices_rejected(self):
        for values in ([1,1],[2,1],[-1,2],[1.5,2],[float('nan')],[[1,2]]):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):summarize_steps(values,50)
        with self.assertRaises(ValueError):summarize_steps([1,2],float('nan'))

class EventEvaluationTests(unittest.TestCase):
    def test_hand_calculated_metrics(self):
        m=p.event_metrics([1,2,3],[1.1,2,4],.15)
        self.assertEqual((m['true_positives'],m['false_positives'],m['false_negatives']),(2,1,1))
        self.assertAlmostEqual(m['f1'],2/3)
        self.assertAlmostEqual(m['timing_mae_seconds'],.05)
    def test_one_detection_cannot_match_two_references(self):
        self.assertEqual(len(p.match_events([1,1.2],[1.1],.2)),1)
    def test_alignment_maximizes_matches_before_timing_error(self):
        self.assertEqual(p.match_events([1,1.2],[.9,1.05],.2),[(0,0),(1,1)])
    def test_best_single_match_minimizes_error(self):
        self.assertEqual(p.match_events([1],[.8,1.05],.3),[(0,1)])
    def test_empty_events_and_invalid_order(self):
        self.assertIsNone(p.event_metrics([],[],.15)['f1'])
        m=p.event_metrics([1,2],[],.15);self.assertEqual(m['recall'],0);self.assertIsNone(m['precision'])
        with self.assertRaises(ValueError):p.match_events([2,1],[1],.1)

class BenchmarkTests(unittest.TestCase):
    def test_noiseless_reference_recovery(self):
        c=json.loads((ROOT/'config.json').read_text())
        truth,samples=p.generate(c,120,0)
        times=(detect_steps(samples,50)/50).tolist()
        m=p.event_metrics(truth,times,.15)
        self.assertEqual(m['false_positives'],0);self.assertEqual(m['false_negatives'],0)
        self.assertEqual(m['f1'],1)
    def test_deterministic_and_finite_export(self):
        a=p.experiment();self.assertEqual(a,p.experiment())
        result=json.loads(a['results.json']);self.assertEqual(len(result['conditions']),9)
        for c in result['conditions']:
            m=c['metrics'];self.assertEqual(m['true_positives']+m['false_negatives'],c['reference_steps'])
            self.assertTrue(0<=m['f1']<=1)
    def test_verifier_detects_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            cmd=[sys.executable,str(ROOT/'pipeline.py'),'--output',d]
            subprocess.run(cmd,check=True,capture_output=True)
            subprocess.run(cmd+['--verify'],check=True,capture_output=True)
            (Path(d)/'report.md').write_text('tampered')
            self.assertNotEqual(subprocess.run(cmd+['--verify'],capture_output=True).returncode,0)
    def test_invalid_config_rejected(self):
        c=json.loads((ROOT/'config.json').read_text());c['noise_sd_g']=[float('nan')]
        with self.assertRaises(ValueError):p.validate(c)
