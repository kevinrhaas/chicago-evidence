#!/usr/bin/env python3
"""Read-only GitHub validation of 18 staged published smoke legs. No dispatch/merge."""
import argparse
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

RANGES = ['1-2', '3-4', '5', '6-7', '8', '9-12', '13', '14', '15']
LABELS = {'mobile': 'mobile 390x780', 'desktop': 'desktop 1280x800'}
GUARDS = [
    '{label}: page serves', '{label}: scene reaches ready',
    '{label}: the scene declares its exact consultation blockers',
    '{label}: no unexpected loader problems', '{label}: scene has structures',
    '{label}: the human layer is mounted and draws nobody',
    '{label}: nothing under humans/ is requested for a scene that does not list it',
    '{label}: every structure that should draw, drew',
    '{label}: the liberties wait for their first reader, not for boot (T-2058)',
    '{label}: the suite body ran to completion', '{label}: zero page errors',
    'vendor: meshopt decoder loads and reports supported',
    'vendor: meshopt import raises no page error',
]
STYLE_LIBRARY_ASSERTION = "{label}: 1900 and 2115 Prairie show the Second Empire card and 1834 the Italianate one, cues dotted and the plate credited; Compare lines open the other styles' cues in place, on them and on Glessner's (T-2642)"

ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def gh(*args, binary=False):
    r = subprocess.run(['gh', *args], capture_output=True, timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.decode(errors='replace').strip() or 'gh failed')
    return r.stdout if binary else r.stdout.decode('utf-8-sig')


def api(path):
    return json.loads(gh('api', path))


def parts(stage):
    lo, *hi = stage.split('-')
    return list(range(int(lo), int(hi[0] if hi else lo) + 1))


def manifest_check(m):
    require(m.get('repository') == 'kevinrhaas/chicago', 'repository must be explicit kevinrhaas/chicago')
    require(re.fullmatch(r'[0-9a-f]{40}', m.get('sha', '')), 'sha must be a full lowercase 40-hex commit')
    require(m.get('workflow') == '.github/workflows/chicago-4d-smoke.yml', 'unexpected workflow')
    runs = m.get('runs', [])
    require(len(runs) == 18, 'manifest must select exactly 18 runs')
    require(all(isinstance(x.get('run_id'), int) and x['run_id'] > 0 for x in runs), 'run IDs must be positive integers')
    require(len({x['run_id'] for x in runs}) == 18, 'duplicate selected run ID')
    require(all(isinstance(x.get('attempt'), int) and x['attempt'] > 0 for x in runs), 'each selected attempt must be explicit')
    grid = Counter((x.get('viewport'), x.get('stage')) for x in runs)
    wanted = Counter((v, s) for v in LABELS for s in RANGES)
    require(grid == wanted, 'selected cells must equal both viewports x exact nine ranges, once each')
    for v in LABELS:
        covered = sorted(p for x in runs if x['viewport'] == v for p in parts(x['stage']))
        require(covered == list(range(1, 16)), f'{v}: stage tiling gap/overlap')
    if 'always_on_assertions' in m:
        require(m['always_on_assertions'] == GUARDS, 'guard manifest differs from reviewed 13 guards; review frozen source before adapting validator')
    return runs


def normalize(text):
    lines = []
    for line in ANSI.sub('', text).splitlines():
        # Normal gh --log format is JOB<TAB>STEP<TAB>TIMESTAMP MESSAGE.
        fields = line.split('\t', 2)
        if len(fields) == 3:
            line = fields[2]
        line = line.lstrip('\ufeff')
        line = re.sub(r'^\d{4}-\d\d-\d\dT\S+Z\s?', '', line)
        lines.append(line)
    return lines


def parse_log(text, viewport, stage):
    lines = normalize(text)
    label = LABELS[viewport]
    viewport_markers = [x for x in lines if x in [v + ':' for v in LABELS.values()]]
    require(viewport_markers == [label + ':'], 'exactly one expected viewport body required')
    require([x for x in lines if x.startswith('NOT THE FULL GATE — viewports filtered to ')] ==
            [f'NOT THE FULL GATE — viewports filtered to "{viewport}"'], 'viewport filter marker missing/mismatched')
    require([x for x in lines if x.startswith('NOT THE FULL GATE — stages filtered to ')] ==
            [f'NOT THE FULL GATE — stages filtered to "{stage}" of 15'], 'stage filter marker missing/mismatched')
    require(sum(x.startswith('serving ') and ' — PUBLISHED mirror' in x for x in lines) == 1, 'published mirror marker missing/ambiguous')
    require(not any(x.startswith('serving ') and 'source tree' in x for x in lines), 'source-tree smoke is not accepted')
    require(any('node tools/smoke_renderer.mjs --published' in x for x in lines), '--published command evidence missing')
    require(sum(x == 'SMOKE PASS' for x in lines) == 1, 'one terminal SMOKE PASS required')
    assertions = []
    for line in lines:
        match = re.match(r'^  (pass|FAIL)\s+(?:\[\d+:\d\d\]\s+)?(.*)$', line)
        if match:
            name = match[2].split(' — ', 1)[0]
            assertions.append({'verdict': match[1], 'name': name, 'line': line})
    require(assertions, 'no executed assertions')
    bad = [x['line'] for x in assertions if x['verdict'] != 'pass']
    require(not bad, 'untagged assertion failures: ' + '; '.join(bad[:8]))
    require(not any(re.search(r'##\[error\]|^FAILURES:|^Traceback \(|^Error:|^TimeoutError:', x) for x in lines), 'error/exception/cancellation evidence in log')
    summaries = [re.fullmatch(r'(\d+) passed, (\d+) failed', x) for x in lines]
    summaries = [x for x in summaries if x]
    require(len(summaries) == 1, 'one completed pass/fail summary required')
    passed, failed = map(int, summaries[0].groups())
    require(failed == 0 and passed == len(assertions), 'summary does not match assertion lines')
    audits = [re.fullmatch(r'(\d+) staged-section check\(s\) \(stage ([\d-]+) of (\d+)\), (\d+) always-on check\(s\)', x) for x in lines]
    audits = [x for x in audits if x]
    require(len(audits) == 1, 'one staged/always-on audit line required')
    sections, actual_stage, total, always = audits[0].groups()
    sections, total, always = int(sections), int(total), int(always)
    require(actual_stage == stage and total == 15, 'audit stage/part count differs')
    require(sections > 0 and always == len(GUARDS), 'empty sections or unexpected always-on guard count')
    require(passed == sections + always, 'audit arithmetic differs from total')
    expected_guards = [x.replace('{label}', label) for x in GUARDS]
    names = [x['name'] for x in assertions]
    require(all(names.count(x) == 1 for x in expected_guards), 'missing/duplicate always-on guard assertion')
    require(all(x.startswith(label + ':') or x.startswith('vendor:') for x in names), 'assertion outside selected viewport/vendor')
    section_inventory = list(names)
    for guard in expected_guards:
        section_inventory.remove(guard)
    require(len(section_inventory) == sections, 'section assertion inventory disagrees with counter')
    style_name = STYLE_LIBRARY_ASSERTION.replace('{label}', label)
    require(section_inventory.count(style_name) == (1 if 14 in parts(stage) else 0),
            'T-2642 style-library assertion missing/duplicated or executed in wrong stage')
    require(lines.index('SMOKE PASS') > max(i for i, x in enumerate(lines) if re.fullmatch(r'\d+ passed, \d+ failed', x)), 'SMOKE PASS precedes summary')
    times = [re.fullmatch(r'(\d+) m (\d+) s for stage ([\d-]+) at (mobile|desktop) — .*', x) for x in lines]
    times = [x for x in times if x]
    require(len(times) == 1 and times[0][3] == stage and times[0][4] == viewport, 'completed wall-time marker missing/mismatched')
    return {'passed': passed, 'failed': failed, 'section_checks': sections, 'always_on_checks': always,
            'wall_seconds': int(times[0][1]) * 60 + int(times[0][2]),
            'guard_assertions': expected_guards, 'section_assertions': section_inventory,
            'assertion_lines': [x['line'] for x in assertions],
            'log_sha256': hashlib.sha256(text.encode()).hexdigest()}


def frozen_sources(repo, sha):
    tree = api(f'repos/{repo}/git/trees/{sha}?recursive=1')
    require(not tree.get('truncated'), 'frozen tree listing truncated')
    wanted = ['.github/workflows/chicago-4d-smoke.yml', '.github/workflows/chicago-4d-bake.yml',
              'chicago/4d/tools/smoke_renderer.mjs']
    entries = {x['path']: x for x in tree['tree']}
    sources = {}
    evidence = {}
    for p in wanted:
        require(p in entries and entries[p]['type'] == 'blob', f'frozen source missing {p}')
        blob = api(f'repos/{repo}/git/blobs/{entries[p]["sha"]}')
        require(blob.get('encoding') == 'base64', f'unsupported blob encoding {p}')
        data = base64.b64decode(blob['content'])
        sources[p] = data.decode()
        evidence[p] = {'git_blob': entries[p]['sha'], 'sha256': hashlib.sha256(data).hexdigest()}
    bake = sources[wanted[1]]
    match = re.search(r'^  smoke:\n(.*?)(?=^  \S|\Z)', bake, re.M | re.S)
    require(match, 'bake smoke job missing')
    row = re.search(r'^        stage: \[(.*)\]$', match[1], re.M)
    views = re.search(r'^        viewport: \[(.*)\]$', match[1], re.M)
    require(row and re.findall(r"'([^']+)'", row[1]) == RANGES, 'frozen bake matrix range contract changed')
    require(views and [x.strip() for x in views[1].split(',')] == ['mobile', 'desktop'], 'frozen bake viewport contract changed')
    smoke = sources[wanted[2]]
    require(re.search(r'const PARTS\s*=\s*15\b', smoke), 'frozen smoke no longer has 15 parts')
    guards = re.findall(r'if \(stageOn\((\d+)\)\) \{\s*inStageWork = true;', smoke)
    require([int(x) for x in guards] == list(range(1, 16)), 'frozen stage work blocks no longer cover exactly 1..15')
    require('if (inStageWork) stageWorkChecks += 1;' in smoke, 'section counter contract changed')
    style_literal = STYLE_LIBRARY_ASSERTION.replace('{label}', '${label}')
    require(smoke.count(style_literal) == 1, 'frozen T-2642 style-library assertion absent/duplicated')
    preceding_blocks = re.findall(r'if \(stageOn\((\d+)\)\)', smoke[:smoke.index(style_literal)])
    require(preceding_blocks and preceding_blocks[-1] == '14', 'frozen T-2642 assertion moved out of stage 14')
    for name in GUARDS:
        require(name.replace('{label}', '${label}') in smoke, f'reviewed guard absent from frozen source: {name}')
    require('SMOKE_VIEWPORT: ${{ inputs.viewport }}' in sources[wanted[0]] and
            'SMOKE_STAGE: ${{ inputs.stage }}' in sources[wanted[0]] and
            'node tools/smoke_renderer.mjs --published' in sources[wanted[0]], 'manual workflow input/published contract changed')
    return evidence


def collect_run(repo, sha, workflow, entry, out):
    result = {**entry, 'parts': parts(entry['stage']), 'accepted': False}
    try:
        meta = api(f'repos/{repo}/actions/runs/{entry["run_id"]}')
        result.update({k: meta.get(k) for k in ['head_sha', 'status', 'conclusion', 'html_url', 'event', 'path', 'created_at', 'updated_at', 'run_attempt']})
        require(meta.get('head_sha') == sha, 'run head differs from frozen SHA')
        require(meta.get('path', '').split('@')[0] == workflow, 'unexpected workflow path')
        require(meta.get('event') == 'workflow_dispatch', 'run is not a manual workflow dispatch')
        require(meta.get('run_attempt') == entry['attempt'], 'manifest attempt is not current run attempt')
        require(meta.get('status') == 'completed' and meta.get('conclusion') == 'success', 'workflow is not completed successfully')
        text = gh('run', 'view', str(entry['run_id']), '--repo', repo, '--attempt', str(entry['attempt']), '--log')
        path = out / f'{entry["run_id"]}-attempt-{entry["attempt"]}.log'
        path.write_text(text)
        result['log_path'] = str(path)
        result.update(parse_log(text, entry['viewport'], entry['stage']))
        result['accepted'] = True
    except Exception as e:
        result['error'] = str(e)
    return result


def aggregate(m, records, source_evidence, source_error=None):
    successes = sum(r.get('status') == 'completed' and r.get('conclusion') == 'success'
                    and r.get('head_sha') == m['sha'] and (r.get('path') or '').split('@')[0] == m['workflow']
                    and r.get('event') == 'workflow_dispatch'
                    and r.get('run_attempt') == r.get('attempt') for r in records)
    errors = [f'run {r["run_id"]}: {r.get("error", "not accepted")}' for r in records if not r.get('accepted')]
    if source_error:
        errors.append('frozen source audit: ' + source_error)
    viewports = {}
    for viewport in LABELS:
        rows = [r for r in records if r['viewport'] == viewport and r.get('accepted')]
        coverage = sorted(p for r in rows for p in r['parts'])
        sections = sum(r['section_checks'] for r in rows)
        actual_checks = sum(r['passed'] + r['failed'] for r in rows)
        guard_sets = {tuple(r['guard_assertions']) for r in rows}
        if len(rows) != 9 or coverage != list(range(1, 16)) or len(guard_sets) != 1:
            errors.append(f'{viewport}: incomplete/nonuniform selected coverage')
        baseline = m.get('expected_section_totals', {}).get(viewport)
        if baseline is not None and baseline != sections:
            errors.append(f'{viewport}: {sections} section checks differ from explicit same-head expectation {baseline}')
        viewports[viewport] = {'accepted_legs': len(rows), 'covered_parts': coverage, 'executed_sections': sections,
                              'always_on_set_size': len(GUARDS), 'repeated_guard_executions': len(rows) * len(GUARDS),
                              'raw_assertion_executions': actual_checks,
                              'equivalent_unique_guard_total': sections + len(GUARDS) if len(rows) == 9 else None,
                              'same_head_unfiltered_count_comparison': 'provided by manifest' if baseline is not None else 'unavailable; no unfiltered pass claimed'}
    return {'repository': m['repository'], 'sha': m['sha'], 'workflow_successes_at_sha': successes,
            'selected_runs': len(records), 'coverage_proof_passed': not errors,
            'claim': 'complete split published smoke coverage, both viewports' if not errors else 'coverage not proven',
            'proof_basis': 'exact frozen-source stage topology, exact 18-cell tiling, successful published logs, section arithmetic, reviewed always-on guard manifest',
            'not_claimed': ['an unfiltered smoke pass', 'merge authorization', 'same-head PR/preflight checks validated by this tool'],
            'source_evidence': source_evidence, 'viewports': viewports, 'errors': errors, 'runs': records}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path)
    p.add_argument('--out', type=Path, required=True, help='outside-checkout evidence directory')
    p.add_argument('--workers', type=int, default=3, choices=range(1, 5))
    a = p.parse_args()
    m = json.loads(a.manifest.read_text())
    runs = manifest_check(m)
    out = a.out.resolve()
    require(out.is_relative_to(Path('/workspace/shared')) or out.is_relative_to(Path('/tmp')), 'output must stay outside app under /workspace/shared or /tmp')
    require(not out.exists() or not any(out.iterdir()), 'output directory must be fresh/empty; existing evidence is never overwritten')
    out.mkdir(parents=True, exist_ok=True)
    source_evidence, source_error = {}, None
    try:
        source_evidence = frozen_sources(m['repository'], m['sha'])
    except Exception as e:
        source_error = str(e)
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        records = list(pool.map(lambda x: collect_run(m['repository'], m['sha'], m['workflow'], x, out), runs))
    receipt = aggregate(m, records, source_evidence, source_error)
    (out / 'manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    (out / 'aggregate.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Workflow successes at frozen SHA: {receipt["workflow_successes_at_sha"]}/18')
    print(f'Coverage proof: {"PASS" if receipt["coverage_proof_passed"] else "NOT PROVEN"}')
    for error in receipt['errors']:
        print(' - ' + error)
    print('Receipt: ' + str(out / 'aggregate.json'))
    return 0 if receipt['coverage_proof_passed'] else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print('Validation cannot proceed: ' + str(e), file=sys.stderr)
        sys.exit(2)
