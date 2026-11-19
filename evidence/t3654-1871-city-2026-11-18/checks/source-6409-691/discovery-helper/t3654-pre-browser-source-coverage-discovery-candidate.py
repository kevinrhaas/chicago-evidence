#!/usr/bin/env python3
"""Verify exact-current source coverage for browser queueing, never for merging.

Reads immutable native-part receipts and logs; writes only its own /tmp report.
The dispatcher MUST additionally check live remote head/base and live workflow
job conclusions. The canonical hosted gate and all merge requirements are untouched.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

# Identity and evidence are explicit reviewed input, never inferred from prior runs.
DEFAULT_BINDINGS = Path('/tmp/t3654-pre-browser-bindings-871698.json')
BINDINGS = None
BINDING_ARTIFACT = None

ANSI = re.compile(r'\x1b\[[0-9;]*m')
STAMP = re.compile(r'^\d{4}-\d\d-\d\dT\S+Z ')


class Refusal(ValueError):
    pass


def require(ok, why):
    if not ok:
        raise Refusal(why)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bound(path, expected=None):
    path = Path(path)
    value = digest(path)
    require(expected is None or value == expected, f'Changed artifact: {path}')
    return {'path': str(path), 'sha256': value}


def reverify_bound_artifacts(value):
    """Reject evidence changed after its earlier parsing, including nested exit bundles."""
    if isinstance(value, dict):
        if 'path' in value and 'sha256' in value:
            bound(value['path'], value['sha256'])
        for child in value.values():
            reverify_bound_artifacts(child)
    elif isinstance(value, list):
        for child in value:
            reverify_bound_artifacts(child)


def read_json(path):
    return json.loads(Path(path).read_text())


def configure(path):
    global ROOT, APP, TMP, OUTPUT, HEAD, TREE, BASE, CI_COMMIT, REPO, BRANCH, PR, RUN
    global DECL_SHA, COUNT, PART_COUNT, BINDINGS, BINDING_ARTIFACT
    d = read_json(path)
    require(d['schema'] == 't3654-pre-browser-bindings-v1', 'Unknown bindings schema')
    for key in ('source_commit', 'source_tree', 'included_dev_base', 'actual_hosted_checkout'):
        require(bool(re.fullmatch(r'[0-9a-f]{40}', d[key])), f'Invalid bound identity: {key}')
    require(bool(re.fullmatch(r'[0-9a-f]{64}', d['declaration_sha256'])), 'Invalid declaration digest')
    require(1 <= d['hosted_partition_count'] <= 32 and d['declared_steps'] > 0 and
            d['pull_request'] > 0 and d['hosted_run_id'] > 0, 'Invalid bound counts')
    require(set(d['harness_sha256']) == {'tools/check.sh', 'tools/check_harness.sh', 'tools/test_check_harness.sh'} and
            d['harness_sha256']['tools/check.sh'] == d['declaration_sha256'], 'Incomplete harness bindings')
    for key in ('accepted_local_receipts', 'accepted_hosted_metadata'):
        require(isinstance(d[key], list) and len({x['path'] for x in d[key]}) == len(d[key]),
                f'Duplicate or invalid bound evidence: {key}')
    require(isinstance(d['qualified_local_exits'], list) and isinstance(d['excluded_hosted_timeouts'], list),
            'Exit/timeout exceptions must be explicit lists, including when empty')
    require(len({x['job_id'] for x in d['excluded_hosted_timeouts']}) == len(d['excluded_hosted_timeouts']),
            'Duplicate timeout exception')
    ROOT, TMP = Path(d['root']), Path(d['artifact_directory'])
    APP, OUTPUT = ROOT / d['app_relative'], Path(d['output'])
    require(ROOT.is_absolute() and TMP.is_absolute() and TMP.is_relative_to(Path('/tmp')) and OUTPUT.parent == TMP,
            'Bindings must use absolute repository/artifact paths and an artifact-only output')
    patterns = d.get('local_receipt_globs', ['t3654-source-fallback-*.receipt.json'])
    require(isinstance(patterns, list) and patterns and len(set(patterns)) == len(patterns) and
            all(isinstance(g, str) and '/' not in g and '..' not in g and g.endswith('.receipt.json')
                for g in patterns), 'Receipt discovery must use unique flat receipt filename patterns')
    require(all(Path(x['path']).parent == TMP and Path(x['path']).resolve().parent == TMP.resolve() and
                any(Path(x['path']).match(g) for g in patterns) for x in d['accepted_local_receipts']),
            'An admitted receipt is outside the real artifact directory or discovery patterns')
    HEAD, TREE, BASE, CI_COMMIT = (d[k] for k in ('source_commit', 'source_tree', 'included_dev_base', 'actual_hosted_checkout'))
    REPO, BRANCH, PR, RUN = (d[k] for k in ('repository', 'branch', 'pull_request', 'hosted_run_id'))
    DECL_SHA, COUNT, PART_COUNT = d['declaration_sha256'], d['declared_steps'], d['hosted_partition_count']
    BINDINGS, BINDING_ARTIFACT = d, bound(path)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def plain_log(path):
    return '\n'.join(STAMP.sub('', line) for line in
                     ANSI.sub('', Path(path).read_text()).splitlines())


def declarations(text):
    rows = []
    for line_no, line in enumerate(text.splitlines(), 1):
        m = re.match(r'^\s*(every_part )?(step|selftest) "((?:\\.|[^"\\])*)"', line)
        if m:
            # Literal double-quoted shell labels unescape only these characters;
            # never evaluate labels or run command substitutions from source text.
            label = re.sub(r'\\([$`"\\])', r'\1', m[3])
            rows.append({'ordinal': len(rows) + 1, 'line': line_no,
                         'every_part': bool(m[1]), 'kind': m[2], 'label': label})
    return rows


def selected(rows, part):
    require(bool(re.fullmatch(r'[1-9][0-9]?/[1-9][0-9]?', part)), 'Invalid part')
    k, n = map(int, part.split('/'))
    require(1 <= k <= n <= 32, 'Part outside native range')
    return [r for r in rows if r['every_part'] or (r['ordinal'] - 1) % n + 1 == k]


STRICT_SOURCE_LABELS = {
    'readers': 'the gate can ask what it claims to ask (raster readers present)',
    'changelog_base': 'changelog contract',
    'rulings_base': 'no land-sale ruling has left the file without saying so',
}


def verify_required_source_context(text, chosen):
    """A sandbox warning is not proof that reader/base-dependent work executed."""
    labels = {r['label'] for r in chosen}
    for kind, label in STRICT_SOURCE_LABELS.items():
        if label not in labels:
            continue
        marker = f'== {label}\n'
        require(text.count(marker) == 1, f'Ambiguous required source context: {kind}')
        block = text.split(marker, 1)[1].split('\n== ', 1)[0]
        if kind == 'readers':
            ok = re.search(r"^   ok    every raster reader the gate's steps need is installed: .+$", block, re.M)
        elif kind == 'changelog_base':
            ok = re.search(r'^changelog contract OK — .+; held to origin/dev at ' + re.escape(BASE[:9]) + r': [0-9]+ shipped entries$', block, re.M)
        else:
            ok = re.search(r'^   ok    base origin/dev at ' + re.escape(BASE[:9]) + r'$', block, re.M)
        require(ok is not None, f'Required reader/base assertion did not execute against the bound context: {kind}')


def verify_transcript(text, part, rows):
    chosen = selected(rows, part)
    matches = re.findall(r'^CHECK PASS — part (\d+/\d+): (\d+) steps, none red\.$', text, re.M)
    require(matches == [(part, str(len(chosen)))], f'No unique exact terminal PASS for {part}')
    require(not re.search(r'^CHECK FAIL\b|^   \^ .+ failed$', text, re.M), f'Assertion failure in {part}')
    labels = {r['label'] for r in rows}
    headers = []
    for line in text.splitlines():
        if line.startswith('== '):
            label = line[3:].removesuffix(' (self-test: the assertions below are meant to fire)')
            if label in labels:
                headers.append(label)
    require(headers == [r['label'] for r in chosen], f'Actual declaration headings differ for {part}')
    selftests = re.findall(r'^  (\d+) of them are self-tests that prove a gate by breaking it; their$', text, re.M)
    require(selftests == [str(sum(r['kind'] == 'selftest' for r in chosen))], f'Self-test count differs for {part}')
    verify_required_source_context(text, chosen)
    return [r['ordinal'] for r in chosen]


def verify_kernel_exit(receipt, receipt_path):
    candidates = [x for x in BINDINGS['qualified_local_exits'] if x['receipt']['path'] == str(receipt_path)]
    require(len(candidates) == 1, 'Alternate exit provenance is not explicitly allowed for this receipt')
    approval = candidates[0]
    bound(receipt_path, approval['receipt']['sha256'])
    require(approval['part'] == receipt['part'], 'Alternate-exit part differs')
    bundle_path = Path(approval['bundle']['path'])
    bound(bundle_path, approval['bundle']['sha256'])
    bundle = read_json(bundle_path)
    require(bundle['head'] == HEAD and bundle['part'] == receipt['part'] and bundle['exit_code'] == 0,
            'Kernel-exit bundle identity differs')
    for item in bundle['files']:
        bound(item['path'], item['sha256'])
    bundled_paths = {x['path'] for x in bundle['files']}
    require({str(receipt_path), receipt['log'], approval['kernel_path'], approval['repair_path']} <= bundled_paths,
            'Kernel-exit bundle omits a required raw proof')
    kernel = read_json(approval['kernel_path'])
    repair = read_json(approval['repair_path'])
    require(repair['original_wrapper'] in bundled_paths, 'Kernel-exit bundle omits original wrapper')
    fields = kernel['raw_proc_stat'].split(') ', 1)[1].split()
    require(fields[0] == 'Z' and int(fields[49]) == 0 and
            kernel['proc_state'] == 'Z' and kernel['proc_exit_code_wait_status'] == 0 and
            kernel['exit_code'] == 0 and os.waitstatus_to_exitcode(int(fields[49])) == 0,
            'No successful exited GNU timeout process')
    require(kernel['process_pid'] == int(kernel['raw_proc_stat'].split()[0]) and
            any(x['pid'] == kernel['process_pid'] and x['inode'] == repair['original_inode']
                for x in repair['open_stdout_fd_evidence']), 'Kernel PID/stdout identity differs')
    require(repair['gate_command_and_inputs_changed'] is False and
            repair['restoration_pending'] is False and
            repair['final_log_sha256'] == receipt['log_sha256'], 'Transcript restoration binding differs')
    wrapper = Path(repair['original_wrapper']).read_text()
    bound(repair['original_wrapper'], repair['original_wrapper_sha256'])
    require(f'timeout --kill-after=5s 590s env CHECK_PART={receipt["part"]} CHECK_JOBS=4' in wrapper and
            'bash tools/check.sh' in wrapper, 'Recovered process was not the recorded native gate')
    return {'kind': 'kernel_exit_0_with_original_transcript_identity',
            'bundle': bound(bundle_path), 'raw_artifacts': bundle['files'], 'duration_is_approximate': True}


def verify_local(path, rows, harness):
    d = read_json(path)
    if d.get('start_snapshot', {}).get('head') != HEAD:
        return None, 'other_head'
    if d.get('status') != 'pass' or d.get('exit_code') != 0:
        if d.get('status') in ('running', 'timeout', 'pass_from_terminal_log'):
            return None, 'no_complete_successful_process'
        raise Refusal(f'Unresolved current local failure: {path}')
    for stage in ('start_snapshot', 'end_snapshot'):
        s = d[stage]
        require(s['head'] == HEAD and s['tree'] == TREE and s['status_porcelain'] == '',
                f'Changed/dirty local snapshot: {path}')
        require(s['harness_sha256'] == harness, f'Changed local harness: {path}')
    require(d.get('head_changed_during_call') is False and
            d['declaration_snapshot'] == DECL_SHA and d['declared_steps'] == COUNT,
            f'Local declaration identity differs: {path}')
    log = bound(d['log'], d['log_sha256'])
    ordinals = verify_transcript(plain_log(d['log']), d['part'], rows)
    require(d['selected_ordinals'] == ordinals, f'Claimed local ordinals differ: {path}')
    if d.get('process_receipt'):
        process = read_json(d['process_receipt'])
        process_bound = bound(d['process_receipt'], d['process_receipt_sha256'])
        require(process['part'] == d['part'] and process['exit_code'] == 0 and
                process['end_epoch_ns'] >= process['start_epoch_ns'], f'Invalid process exit: {path}')
        require(process['end_epoch_ns'] / 1e9 == d['end_epoch_s'] and
                round((process['end_epoch_ns'] - process['start_epoch_ns']) / 1e9, 3) == d['duration_s'] and
                d['start_epoch_s'] <= process['start_epoch_ns'] / 1e9 <= d['end_epoch_s'],
                f'Process exit belongs to a different attempt or timing interval: {path}')
        exit_proof = {'kind': 'original_process_exit_0', 'artifact': process_bound}
    else:
        exit_proof = verify_kernel_exit(d, path)
    return {'kind': 'local', 'part': d['part'], 'receipt': bound(path), 'log': log,
            'exit_proof': exit_proof, 'ordinals': ordinals}, None


def verify_meta_identity(meta):
    require(meta['headSha'] == HEAD and meta['headBranch'] == BRANCH and
            meta['url'] == f'https://github.com/{REPO}/actions/runs/{RUN}', 'Hosted metadata identity differs')


def verify_checkout(text):
    require(f'[command]/usr/bin/git log -1 --format=%H\n{CI_COMMIT}' in text,
            'Actual hosted checkout not proved by git log')


def verify_hosted(path, rows, verified_parts):
    m = re.fullmatch(rf't3654-support-{RUN}-part([1-9][0-9]?)-complete-meta.json', path.name)
    require(m is not None, 'Unexpected hosted metadata path')
    part = f'{m[1]}/{PART_COUNT}'
    meta = read_json(path)
    verify_meta_identity(meta)
    jobs = [j for j in meta['jobs'] if j['name'] == f'gate part {part}']
    require(len(jobs) == 1, f'Missing/duplicate hosted job for {part}')
    job = jobs[0]
    require(job['status'] == 'completed' and job['conclusion'] == 'success', f'Hosted {part} not successful')
    require(all(any(s['name'] == name and s['status'] == 'completed' and s['conclusion'] == 'success'
                    for s in job['steps']) for name in
                ('Run the gate', 'Does this change carry a changelog entry?')), 'Hosted required steps did not succeed')
    log_path = TMP / f't3654-support-{RUN}-job{int(job["databaseId"])}.log'
    recorded = verified_parts.get(job['databaseId'])
    require(recorded is not None and recorded.get('verified_pass') is True and
            recorded.get('part') == part and recorded.get('status') == 'completed' and
            recorded.get('conclusion') == 'success' and recorded.get('log') == str(log_path),
            f'Hosted {part} has no independently recorded successful log binding')
    log_binding = bound(log_path, recorded['log_sha256'])
    text = plain_log(log_path)
    verify_checkout(text)
    require('C4D_GATE_REQUIRE_READERS: 1' in text and 'C4D_GATE_REQUIRE_BASE: 1' in text,
            'Hosted required read/base environment missing')
    require(f'node chicago/4d/tools/check-changelog-entry.mjs "{BASE}" "{HEAD}"' in text and
            re.search(r'^changelog entry: present — ', text, re.M), 'Exact PR-only changelog success missing')
    return {'kind': 'hosted', 'part': part, 'job_id': job['databaseId'], 'metadata': bound(path),
            'log': log_binding, 'ordinals': verify_transcript(text, part, rows),
            'actual_checkout': CI_COMMIT, 'pr_only_changelog_pass': True}


def verify_timeout_exclusion(exception):
    path = Path(exception['metadata']['path'])
    bound(path, exception['metadata']['sha256'])
    meta = read_json(path)
    verify_meta_identity(meta)
    job_id, part = exception['job_id'], exception['part']
    selected([], part)  # Validate the native partition syntax without giving credit.
    jobs = [j for j in meta['jobs'] if j['databaseId'] == job_id]
    require(len(jobs) == 1 and jobs[0]['name'] == f'gate part {part}' and
            jobs[0]['status'] == 'completed' and jobs[0]['conclusion'] == 'failure',
            'Original timeout job identity differs')
    log = Path(exception['log']['path'])
    binding = bound(log, exception['log']['sha256'])
    text = plain_log(log)
    verify_checkout(text)
    require('##[error]Process completed with exit code 124.' in text and
            not re.search(r'^CHECK (?:PASS|FAIL)\b|^   \^ .+ failed$', text, re.M), 'Known timeout is not a verdict-free timeout without a recorded assertion failure')
    return {'job_id': job_id, 'part': part, 'metadata': bound(path), 'log': binding,
            'coverage_credit': False, 'reason': '600-second timeout before a final native verdict; no assertion pass inferred'}


def audit():
    require(git('rev-parse', 'HEAD') == HEAD and git('rev-parse', 'HEAD^{tree}') == TREE and
            git('status', '--porcelain') == '', 'Current source checkout changed or dirty')
    require(git('rev-parse', 'origin/dev') == BASE and git('merge-base', 'origin/dev', 'HEAD') == BASE,
            'Current local integration base differs')
    require(git('rev-parse', f'{CI_COMMIT}^{{tree}}') == TREE and
            git('show', '-s', '--format=%P', CI_COMMIT).split() == [BASE, HEAD], 'Hosted/source trees or parents differ')
    harness = {p: digest(APP / p) for p in ('tools/check.sh', 'tools/check_harness.sh', 'tools/test_check_harness.sh')}
    require(harness == BINDINGS['harness_sha256'], 'Current harness/declaration bytes changed')
    rows = declarations((APP / 'tools/check.sh').read_text())
    require(len(rows) == COUNT, 'Current declaration count changed')
    require(all(sum(r['label'] == label for r in rows) == 1 for label in STRICT_SOURCE_LABELS.values()),
            'Required reader/base declarations changed; explicit verifier review required')
    prerequisites = [r['ordinal'] for r in rows if r['every_part']]
    require(prerequisites == BINDINGS['prerequisite_ordinals'], 'Native prerequisites changed')
    hosted_index_path = Path(BINDINGS['hosted_evidence_index']['path'])
    bound(hosted_index_path, BINDINGS['hosted_evidence_index']['sha256'])
    hosted_index_bytes = hosted_index_path.read_bytes()
    hosted_index = json.loads(hosted_index_bytes)
    require(hosted_index['source_commit'] == HEAD and hosted_index['included_dev_base'] == BASE and
            hosted_index['repository'] == REPO and hosted_index['pull_request'] == PR and
            hosted_index['run_id'] == RUN, 'Hosted evidence index belongs to another source/base/run')
    timeout_ids = {x['job_id'] for x in BINDINGS['excluded_hosted_timeouts']}
    verified_parts = {}
    for item in hosted_index['parts']:
        require(item['job_id'] not in verified_parts, 'Duplicate hosted job identity in evidence index')
        if item.get('status') == 'completed' and item.get('conclusion') != 'success':
            require(item['job_id'] in timeout_ids and item.get('conclusion') == 'failure',
                    f'Unresolved hosted failure/cancellation: {item["job_id"]}')
        verified_parts[item['job_id']] = item
    accepted, excluded = [], []
    local_bindings = {x['path']: x['sha256'] for x in BINDINGS['accepted_local_receipts']}
    # Flat filename globs intentionally do not recurse into synthetic fixture
    # directories. Every admitted real receipt must belong to this same scope.
    patterns = BINDINGS.get('local_receipt_globs', ['t3654-source-fallback-*.receipt.json'])
    local_paths = {p for pattern in patterns for p in TMP.glob(pattern)} | {Path(p) for p in local_bindings}
    for path in sorted(local_paths):
        if str(path) in local_bindings:
            bound(path, local_bindings[str(path)])
        item, why = verify_local(path, rows, harness)
        if item and str(path) in local_bindings:
            accepted.append(item)
        elif item:
            excluded.append({'path': str(path), 'reason': 'successful_receipt_not_explicitly_bound', 'coverage_credit': False})
        else:
            excluded.append({'path': str(path), 'reason': why, 'coverage_credit': False})
    for binding in BINDINGS['accepted_hosted_metadata']:
        path = Path(binding['path'])
        bound(path, binding['sha256'])
        accepted.append(verify_hosted(path, rows, verified_parts))
    timeouts = [verify_timeout_exclusion(x) for x in BINDINGS['excluded_hosted_timeouts']]
    counts = Counter(i for item in accepted for i in item['ordinals'])
    require(all(set(prerequisites) <= set(item['ordinals']) for item in accepted), 'A successful part omitted its prerequisites')
    covered = [i for i in range(1, COUNT + 1) if counts[i]]
    missing = [i for i in range(1, COUNT + 1) if not counts[i]]
    require(not set(counts) - set(range(1, COUNT + 1)), 'Unknown declaration credited')
    pr_checks = any(item.get('pr_only_changelog_pass') for item in accepted)
    complete = not missing and pr_checks
    ordinary = {r['ordinal'] for r in rows if not r['every_part']}
    # The application tree can remain unchanged while dev advances. Such a proof
    # remains dated evidence, but must never authorize a queue against the old base.
    branch_ref = f'refs/heads/{BRANCH}'
    remote_listing = git('ls-remote', 'origin', branch_ref, 'refs/heads/dev')
    remote = {}
    for line in remote_listing.splitlines():
        sha, ref = line.split()
        require(bool(re.fullmatch(r'[a-f0-9]{40}', sha)) and ref not in remote, 'Invalid remote ref response')
        remote[ref] = sha
    require(set(remote) == {branch_ref, 'refs/heads/dev'}, 'Remote head/base could not both be read')
    blockers = []
    if remote[branch_ref] != HEAD:
        blockers.append('live_branch_head_changed')
    if remote['refs/heads/dev'] != BASE:
        blockers.append('live_dev_base_changed')
    require(git('rev-parse', 'HEAD') == HEAD and git('rev-parse', 'HEAD^{tree}') == TREE and
            git('status', '--porcelain') == '' and git('rev-parse', 'origin/dev') == BASE and
            all(digest(APP / p) == value for p, value in harness.items()),
            'Source changed during the coverage audit')
    reverify_bound_artifacts([accepted, timeouts, BINDINGS, BINDING_ARTIFACT])
    index_sha = hashlib.sha256(hosted_index_bytes).hexdigest()
    index_snapshot = TMP / f't3654-pre-browser-hosted-index-{index_sha[:16]}.json'
    if index_snapshot.exists():
        require(index_snapshot.read_bytes() == hosted_index_bytes, 'Hosted index snapshot collision')
    else:
        index_snapshot.write_bytes(hosted_index_bytes)
    return {'schema': 't3654-pre-browser-source-coverage-v1', 'recorded_utc': datetime.now(timezone.utc).isoformat(),
            'source_commit': HEAD, 'source_tree': TREE, 'included_dev_base': BASE,
            'repository': REPO, 'branch': BRANCH, 'pull_request': PR,
            'hosted_run_id': RUN, 'hosted_run_url': f'https://github.com/{REPO}/actions/runs/{RUN}',
            'actual_hosted_checkout': CI_COMMIT, 'declaration_sha256': DECL_SHA,
            'harness_sha256': harness, 'declared_steps': COUNT, 'ordinary_steps': len(ordinary),
            'strict_source_context_checks': STRICT_SOURCE_LABELS,
            'prerequisite_ordinals': prerequisites, 'covered_ordinals': covered, 'missing_ordinals': missing,
            'ordinary_covered': len(ordinary & set(covered)), 'ordinary_missing': len(ordinary & set(missing)),
            'overlap_ordinals': sorted(i for i in ordinary if counts[i] > 1),
            'overlap_policy': 'Repeated successful assertions are retained as evidence but credited once; counts are never summed as coverage.',
            'accepted_parts': accepted, 'excluded_local_receipts': excluded,
            'hosted_evidence_index': {'source_path': str(hosted_index_path), **bound(index_snapshot, index_sha)},
            'bindings': BINDING_ARTIFACT,
            'excluded_hosted_timeout_job_ids': sorted(timeout_ids), 'preserved_timeouts': timeouts,
            'pr_only_checks_pass': pr_checks, 'source_check_coverage_complete': complete,
            'live_remote_refs': remote, 'live_remote_ref_listing': remote_listing,
            'live_identity_blockers': blockers, 'ready_for_browser_queue': complete and not blockers,
            'live_dispatch_checks_required': True,
            'hosted_gate_required_before_merge': True, 'merge_authorized_by_this_proof': False,
            'scope': 'Exact-current successful source-declaration coverage for browser sequencing only; not a hosted aggregate success or a single whole-run verdict.',
            'dispatcher_requirements': ['Reverify this helper and all raw artifacts immediately before dispatch.',
                'Read live remote branch and dev base; require the exact frozen head/base.',
                'Read live hosted run/job metadata; reject unknown failures/cancellations, assertion failures or a changed run identity. Only the preserved timeout ID above is excluded.',
                'Keep complete hosted parts+aggregate and all browser/supporting checks mandatory before merge.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true')
    parser.add_argument('--bindings', type=Path, default=DEFAULT_BINDINGS)
    args = parser.parse_args()
    try:
        configure(args.bindings)
        result = audit()
    except (Refusal, OSError, ValueError, KeyError, TypeError, IndexError, subprocess.CalledProcessError) as exc:
        # Refusal always exits nonzero. Do not leave a stale ready report at the
        # active output path once the trusted binding has been loaded successfully.
        if BINDINGS is not None:
            refusal = {'schema': 't3654-pre-browser-source-coverage-v1',
                       'source_commit': HEAD, 'source_tree': TREE, 'included_dev_base': BASE,
                       'bindings': BINDING_ARTIFACT, 'recorded_utc': datetime.now(timezone.utc).isoformat(),
                       'ready_for_browser_queue': False, 'source_check_coverage_complete': False,
                       'verification_refused': str(exc), 'merge_authorized_by_this_proof': False}
            OUTPUT.write_text(json.dumps(refusal, indent=2) + '\n')
        print(f'REFUSED: {exc}', file=sys.stderr)
        return 2
    result['verifier_sha256'] = digest(__file__)
    pending = OUTPUT.with_suffix('.next.json')
    pending.write_text(json.dumps(result, indent=2) + '\n')
    pending.replace(OUTPUT)
    print(json.dumps({k: result[k] for k in ('source_commit', 'ordinary_covered', 'ordinary_missing',
          'pr_only_checks_pass', 'source_check_coverage_complete', 'live_identity_blockers', 'ready_for_browser_queue')}, indent=2))
    return 0 if not args.require_complete or result['ready_for_browser_queue'] else 1


if __name__ == '__main__':
    sys.exit(main())
