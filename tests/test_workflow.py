import json
from pathlib import Path
import unittest
class WorkflowPolicy(unittest.TestCase):
 def test_untrusted_validation_is_read_only_and_actions_pinned(self):
  w=json.loads((Path(__file__).resolve().parents[1]/'.github/workflows/benchmark.yml').read_text())
  self.assertEqual(w['permissions'],{'contents':'read'})
  self.assertNotIn('pull_request_target',w['on']);self.assertIn('schedule',w['on'])
  self.assertEqual(set(w['jobs']),{'validate'})
  steps=w['jobs']['validate']['steps']
  self.assertFalse(steps[0]['with']['persist-credentials'])
  for step in steps:
   if 'uses' in step:self.assertRegex(step['uses'],r'^actions/[a-z-]+@[0-9a-f]{40}$')
  test_index=next(i for i,s in enumerate(steps) if s.get('name')=='Test')
  artifact_index=next(i for i,s in enumerate(steps) if s.get('uses','').startswith('actions/upload-artifact@'))
  self.assertLess(test_index,artifact_index)
