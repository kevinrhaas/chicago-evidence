"""Label exact-host held timings and unheld readings without changing gate policy."""
import hashlib
import json
import math
import subprocess
from pathlib import Path

W = Path('/workspace/work')


def qualify(prefix):
    p = json.loads((W/(prefix+'-final-integration-proof.json')).read_text())
    repo = Path(p['repo'])
    path = 'chicago/4d/tools/still_frame_ceilings.json'
    def raw(ref):
        return subprocess.check_output(['git', 'show', ref+':'+path], cwd=repo)
    body = raw(p['final_tree'])
    assert body == raw(p['native_candidate_tree']), 'Original performance limits changed'
    caps = json.loads(body)
    reports, missing, rows = [], [], []
    for vp in ('desktop', 'mobile'):
        name = 'still-frame-'+vp
        file = W/(prefix+'-final-ci')/'grid'/name/(name+'.json')
        if not file.exists():
            missing.append(name)
            continue
        d = json.loads(file.read_text())
        assert d['tree'] == 'published' and str(d['year']) == str(caps['year'])
        assert d['frames'] > 0 and len(d['passes']) == 1
        item = d['passes'][0]
        assert not item['errors']
        assert ('mobile' if item['viewport'].startswith('phone') else 'desktop') == vp
        assert {r['level'] for r in item['rows']} == set(caps['tiers'])
        machine = d['machine']
        held = next((m for m in caps['machines']
                     if m['cpu'] == machine['model'] and m['cores'] == machine['cores']), None)
        for r in item['rows']:
            assert r['stand'] == caps['stand'] and math.isfinite(r['frame']) and r['frame'] > 0
            limit = held.get('tiers', {}).get(r['level'], {}).get(vp) if held else None
            within = r['frame'] <= limit if isinstance(limit, (int, float)) else None
            assert within is not False, (vp, machine, r['level'], r['frame'], limit)
            rows.append({'viewport': vp, 'tier': r['level'], 'machine': machine,
                         'frame_ms': r['frame'], 'registered_limit_ms': limit,
                         'status': 'held_pass' if within else 'unheld_measurement',
                         'counts_as_registered_budget_pass': within is True})
        reports.append({'name': name, 'report_sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
    return {'complete_audit': not missing, 'head': p['final_head'],
            'source_tree': p['final_tree'], 'limits_path': path,
            'original_limits_sha256': hashlib.sha256(body).hexdigest(),
            'original_limits_unchanged': True, 'missing_reports': missing,
            'all_six_frame_rows_have_registered_limits': len(rows) == 6 and all(r['registered_limit_ms'] is not None for r in rows),
            'all_observed_registered_limits_passed': True,
            'unheld_rows': [r for r in rows if r['status'] == 'unheld_measurement'],
            'rows': rows, 'reports': reports,
            'unchanged_gate_policy': 'T-2111 reads and warns about a CPU/viewport without a registered limit; it fails only with --strict. The existing stock workflow invokes --gate without --strict. Unheld readings are measurements and never labelled registered-budget passes here. No CPU alias, limit, assertion or workflow is changed.'}
