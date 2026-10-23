import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
import base64

spec = importlib.util.spec_from_file_location('validator', '/workspace/shared/validate_transport_split_smoke.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
SHA = '1b3c73d22016596d07b133019df24422c2b54790'

def manifest():
    return {'repository': 'kevinrhaas/chicago', 'sha': SHA,
            'workflow': '.github/workflows/chicago-4d-smoke.yml',
            'runs': [{'run_id': i + 1, 'attempt': 1, 'viewport': view, 'stage': stage}
                     for i, (view, stage) in enumerate((view, stage) for view in v.LABELS for stage in v.RANGES)]}

def log(view='mobile', stage='1-2'):
    label = v.LABELS[view]
    lines = ['node tools/smoke_renderer.mjs --published',
             'serving /site/4d on 4187 — PUBLISHED mirror (compressed assets)',
             f'NOT THE FULL GATE — viewports filtered to "{view}"',
             f'NOT THE FULL GATE — stages filtered to "{stage}" of 15', label + ':']
    names = [x.replace('{label}', label) for x in v.GUARDS]
    names[9:9] = [label + ': section check ' + str(i) for i in range(3)]
    lines += ['  pass  ' + n for n in names]
    lines += ['16 passed, 0 failed', f'3 staged-section check(s) (stage {stage} of 15), 13 always-on check(s)',
              f'2 m 01 s for stage {stage} at {view} — ceiling', 'SMOKE PASS']
    return '\n'.join('smoke\tRun smoke\t2026-10-18T00:00:00.000Z ' + x for x in lines)

class StrictValidation(unittest.TestCase):
    def test_valid_eighteen_cells_and_audit(self):
        m = manifest(); v.manifest_check(m)
        records = [{**r, 'parts': v.parts(r['stage']), 'status': 'completed', 'conclusion': 'success',
                    'head_sha': SHA, 'path': m['workflow'], 'event': 'workflow_dispatch', 'run_attempt': 1, 'accepted': True, **v.parse_log(log(r['viewport'], r['stage']), r['viewport'], r['stage'])}
                   for r in m['runs']]
        result = v.aggregate(m, records, {'frozen': 'verified'})
        self.assertTrue(result['coverage_proof_passed'])
        self.assertEqual(result['workflow_successes_at_sha'], 18)
        self.assertEqual(result['viewports']['mobile']['executed_sections'], 27)
        self.assertEqual(result['viewports']['mobile']['raw_assertion_executions'], 144)
        self.assertEqual(result['viewports']['mobile']['equivalent_unique_guard_total'], 40)

    def test_successful_workflows_do_not_prove_bad_logs(self):
        m = manifest();records = [{**r, 'parts': v.parts(r['stage']), 'status': 'completed',
            'conclusion': 'success', 'head_sha': SHA, 'path': m['workflow'], 'event': 'workflow_dispatch', 'run_attempt': 1, 'accepted': False, 'error': 'missing summary'} for r in m['runs']]
        result = v.aggregate(m, records, {})
        self.assertEqual(result['workflow_successes_at_sha'], 18)
        self.assertFalse(result['coverage_proof_passed'])

    def test_missing_or_duplicate_cell_rejected(self):
        m = manifest(); m['runs'][-1]['stage'] = '14'
        with self.assertRaises(ValueError): v.manifest_check(m)

    def test_duplicate_run_rejected(self):
        m = manifest(); m['runs'][-1]['run_id'] = 1
        with self.assertRaises(ValueError): v.manifest_check(m)

    def test_log_failure_rejected_even_with_green_footer(self):
        text = log().replace('  pass  mobile 390x780: section check 0', '  FAIL  mobile 390x780: section check 0')
        with self.assertRaisesRegex(ValueError, 'assertion failures'): v.parse_log(text, 'mobile', '1-2')

    def test_timeout_missing_tail_rejected(self):
        with self.assertRaises(ValueError): v.parse_log(log().replace('SMOKE PASS', ''), 'mobile', '1-2')

    def test_guard_and_counter_mismatch_rejected(self):
        for text in [log().replace('13 always-on', '12 always-on'),
                     log().replace('mobile 390x780: zero page errors', 'mobile 390x780: other check'),
                     log().replace('16 passed, 0 failed', '15 passed, 0 failed')]:
            with self.subTest(text=text[-120:]):
                with self.assertRaises(ValueError): v.parse_log(text, 'mobile', '1-2')

    def test_wrong_viewport_range_and_source_rejected(self):
        for text in [log('desktop'), log(stage='3-4'), log().replace(' — PUBLISHED mirror', ' — source tree')]:
            with self.assertRaises(ValueError): v.parse_log(text, 'mobile', '1-2')

    def test_metadata_wrong_head_rejected_before_log_download(self):
        m = manifest();meta = {'head_sha': '0'*40, 'status': 'completed', 'conclusion': 'success'}
        with patch.object(v, 'api', return_value=meta), patch.object(v, 'gh') as gh:
            result = v.collect_run(m['repository'], SHA, m['workflow'], m['runs'][0], Path('/tmp'))
        self.assertFalse(result['accepted']);gh.assert_not_called()

    def test_cancelled_run_rejected_before_log_download(self):
        m = manifest();meta = {'head_sha': SHA, 'event': 'workflow_dispatch', 'path': m['workflow'],
            'run_attempt': 1, 'status': 'completed', 'conclusion': 'cancelled'}
        with patch.object(v, 'api', return_value=meta), patch.object(v, 'gh') as gh:
            result = v.collect_run(m['repository'], SHA, m['workflow'], m['runs'][0], Path('/tmp'))
        self.assertFalse(result['accepted']);gh.assert_not_called()

    def test_actual_frozen_source_contract_without_network(self):
        paths = ['.github/workflows/chicago-4d-smoke.yml', '.github/workflows/chicago-4d-bake.yml', 'chicago/4d/tools/smoke_renderer.mjs']
        blobs = {str(i): subprocess.check_output(['git', '-C', '/workspace/chicago', 'show', SHA + ':' + p]) for i, p in enumerate(paths)}
        tree = {'tree': [{'path': p, 'type': 'blob', 'sha': str(i)} for i, p in enumerate(paths)]}
        def api(path):
            if '/git/trees/' in path:return tree
            data = blobs[path.rsplit('/', 1)[1]]
            return {'encoding': 'base64', 'content': base64.b64encode(data).decode()}
        with patch.object(v, 'api', side_effect=api):
            result = v.frozen_sources('kevinrhaas/chicago', SHA)
        self.assertEqual(len(result), 3)

    def test_real_failed_unfiltered_mobile_log_not_accepted_as_leg(self):
        with self.assertRaises(ValueError):
            v.parse_log(Path('/tmp/transport-mobile-full-failed-39164260098.log').read_text(), 'mobile', '5')

if __name__ == '__main__': unittest.main()
