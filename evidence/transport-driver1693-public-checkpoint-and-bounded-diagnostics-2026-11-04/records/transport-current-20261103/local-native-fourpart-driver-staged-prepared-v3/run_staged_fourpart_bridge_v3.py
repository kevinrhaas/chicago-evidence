#!/usr/bin/env python3
"""Explicitly admitted, exact staged-source, native coverage with reviewed test-only source bridge.

Adapted from the existing run_fourpart_preflight_v2.py ownership/resource/footer
logic. Executes the native check directly; does not update refs or stage changes.
"""
from pathlib import Path
import argparse, datetime, fcntl, hashlib, importlib.util, json, os, re, shutil, subprocess, sys

RUNTIME = Path('/workspace/.cloud-setup/transport-current-20261103')
SUP = Path('/workspace/.cloud-setup/transport-supervise.py')
LOCK = Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
ANSI = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path): return json.loads(Path(path).read_text())
def save(path, value): Path(path).write_text(json.dumps(value, indent=2) + '\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binding', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    binding = load(args.binding)
    binding_sha256 = sha(args.binding)
    assert binding['template_only'] is False and binding['ROOT_EXPLICIT_CURRENT_FOURPART_GO'] is True
    assert binding['status'] == 'PREPARED_REVIEWED_FIXTURE_ONLY_NATIVE_BRIDGE_V3_NOT_EXECUTED'
    repo = Path(binding['repo']); app = repo / 'chicago/4d'; out = args.out.resolve()
    assert not out.exists(), 'Preserve previous receipts; use a fresh output directory'
    assert sys.version_info[:2] == (3, 11)
    assert subprocess.check_output(['node', '--version'], timeout=5).decode().startswith('v22.')
    for path, digest in binding['execution_pins'].items(): assert sha(path) == digest
    assert sha(__file__) == binding['runner_sha256']
    lock = LOCK.open('a+'); fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    spec = importlib.util.spec_from_file_location('current_fourpart_resource_guard', RUNTIME / 'resource_guard.py')
    guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1',
               CHECK_JOBS='4', C4D_GATE_REQUIRE_READERS='1', C4D_GATE_REQUIRE_BASE='1',
               C4D_RULINGS_BASE=binding['reviewed_base_SHA'])
    for key in ['GIT_NO_LAZY_FETCH', 'CHICAGO_TICKETS_DIR', 'CHECK_PART', 'BASE', 'CHECK_TIMINGS']: env.pop(key, None)
    for key in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']:
        assert env.get(key) == '1', 'Source transport-activate.sh before launching'
    metadata_env = dict(env, GIT_NO_LAZY_FETCH='1')
    assert 'GIT_NO_LAZY_FETCH' not in env
    assert binding['resume_native_parts'] == [3, 4]
    def git(*argv):
        return subprocess.check_output(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false',
            '-C', str(repo), *argv], env=metadata_env, timeout=60)
    def val(*argv): return git(*argv).decode().strip()
    assert val('rev-parse', binding['reviewed_base_SHA'] + '^{commit}') == binding['reviewed_base_SHA']
    assert subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor',
        binding['reviewed_base_SHA'], binding['source']['HEAD']], env=metadata_env, timeout=30).returncode == 0
    def source():
        assert not git('ls-files', '-u').strip(), 'Unmerged source refused'
        assert not git('diff', '--name-only').strip(), 'Tracked working-tree edits refused'
        assert git('diff', '--cached', '--name-only').strip(), 'This precommit gate requires actual staged changes'
        assert val('branch', '--show-current') == binding['branch'], 'Branch changed'
        assert not git('ls-files', '--others', '--exclude-standard').strip(), 'Untracked source refused'
        merge = Path(val('rev-parse', '--git-path', 'MERGE_HEAD'))
        if not merge.is_absolute(): merge = repo / merge
        assert not merge.exists(), 'Staged precommit source must have no unresolved merge owner'
        head = val('rev-parse', 'HEAD'); tree = val('write-tree')
        profile = dict(HEAD=head, TREE=tree, APP=val('rev-parse', tree + ':chicago/4d'),
            semantic_index_sha256=hashlib.sha256(git('ls-files', '--stage', '-z')).hexdigest())
        assert profile == binding['source'], 'Actual source differs from explicit ROOT binding'
        return profile
    original = source()
    declarations = re.findall(r'(?m)^[ \t]*(?:(every_part)\s+)?(step|selftest)\s+', (app / 'tools/check.sh').read_text())
    assert len(declarations) == binding['native_distinct_steps']
    assert sum(kind == 'selftest' for _,kind in declarations) == binding['native_selftests']
    assert sum(bool(every) for every,_ in declarations) == binding['every_part_steps']
    expected = {str(k): dict(selected_steps=0, selftests=0, elsewhere_steps=0) for k in range(1, 5)}
    for ordinal, (every, kind) in enumerate(declarations, 1):
        for k in range(1, 5):
            row = expected[str(k)]
            if every or (ordinal - 1) % 4 + 1 == k:
                row['selected_steps'] += 1; row['selftests'] += int(kind == 'selftest')
            else: row['elsewhere_steps'] += 1
    assert expected == binding['expected_parts']
    def footer(text, part):
        text = ANSI.sub('', text)
        counts = re.findall(r'^CHECK PASS[^\n]*part ' + str(part) + r'/4:\s*(\d+) steps, none red\.$', text, re.M)
        other = re.findall(r'^  This is part ' + str(part) + r' of 4; the other (\d+) steps are in the other parts\.', text, re.M)
        selftests = re.findall(r'^  (\d+) of them are self-tests that prove a gate by breaking it;', text, re.M)
        assert len(counts) == len(other) == len(selftests) == 1 and not re.search(r'^CHECK FAIL', text, re.M)
        assert 'green only when every part is: tools/check.sh --part 1/4 through --part 4/4.' in text
        actual = dict(selected_steps=int(counts[0]), selftests=int(selftests[0]), elsewhere_steps=int(other[0]))
        assert actual == expected[str(part)], (actual, expected[str(part)])
        return actual
    def referenced(name):
        ref = binding[name]
        assert set(ref) == {'path','sha256'} and sha(ref['path']) == ref['sha256']
        return load(ref['path'])
    def valid_native(row, command, cap, code=0):
        result=row['result'];cleanup=row['cleanup']
        assert result['command']==command and result['returncode']==code and not result['timed_out']
        assert result['requested_timeout_seconds']==result['effective_timeout_seconds']==cap
        assert result['timeout_override_reason']is None
        assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and row['resources']['accepted']
    prior = referenced('prior_native_coverage_receipt')
    assert prior['status']=='NONPASS_NO_AUTOMATIC_RETRY'and prior['source_error']is None and len(prior['ledger'])==3
    old_source=prior['source_before'];assert prior['source_after']==old_source
    assert old_source['HEAD']==original['HEAD']==binding['reviewed_base_SHA']
    assert old_source['TREE']!=original['TREE'] and old_source['APP']!=original['APP']
    changed='chicago/4d/tools/test_working_driver_1904.mjs'
    assert git('diff-tree','--no-commit-id','--name-only','-r',old_source['TREE'],original['TREE']).decode().splitlines()==[changed]
    assert git('show',old_source['TREE']+':chicago/4d/tools/check.sh')==git('show',original['TREE']+':chicago/4d/tools/check.sh')
    prior_parts=prior['ledger'][:2];stopped=prior['ledger'][2]
    required={k:env[k]for k in ['CHECK_JOBS','C4D_GATE_REQUIRE_READERS','C4D_GATE_REQUIRE_BASE','C4D_RULINGS_BASE']}
    assert prior['required_environment']==required and prior['native_GIT_NO_LAZY_FETCH_absent']is True
    assert prior['metadata_git_GIT_NO_LAZY_FETCH']=='1'and prior['resume_native_parts']==[2,3,4]
    old_binding=referenced('prior_original_binding')
    assert prior['binding_sha256']==binding['prior_original_binding']['sha256']
    assert prior['runner_sha256']==old_binding['runner_sha256']==binding['prior_runner']['sha256']
    assert sha(binding['prior_runner']['path'])==binding['prior_runner']['sha256']
    assert old_binding['source']==old_source and old_binding['expected_parts']==expected
    for part,row in enumerate(prior_parts,1):
        valid_native(row,['./tools/check.sh','--part',str(part)+'/4'],600)
        assert row['part']==part and row['source_before']==row['source_after']==old_source and row['source_error']is None
        assert row['resources']==guard.pair(row['resource_before'],row['resource_after'])
        evidence=binding['prior_positive_part_evidence'][str(part)]
        for ref in evidence.values():assert set(ref)=={'path','sha256'}and sha(ref['path'])==ref['sha256']
        assert evidence['log']['path']==row['log']and evidence['log']['sha256']==row['log_sha256']
        body=Path(row['log']).read_text(errors='replace');assert footer(body,part)==row['native_footer_counts']==expected[str(part)]
        assert load(evidence['result']['path'])==row['result']and load(evidence['cleanup']['path'])==row['cleanup']
        assert Path(evidence['raw_footer']['path']).read_text()=='\n'.join(ANSI.sub('',body).splitlines()[-12:])+'\n'
    valid_native(stopped,['./tools/check.sh','--part','3/4'],600,130)
    assert stopped['source_before']==stopped['source_after']==old_source and stopped['source_error']is None
    inherited=prior['prior_part1_admission'];ref=inherited['original_negative_receipt']
    assert sha(ref['path'])==ref['sha256']and load(ref['path'])['ledger'][0]==prior_parts[0]
    for name in ['prior_original_binding','prior_runner','part1_log','part1_raw_footer','part1_result','part1_cleanup']:
        ref=inherited[name];assert sha(ref['path'])==ref['sha256']
    audit=referenced('independent_bridge_audit')
    assert audit['status']=='INDEPENDENT_FIXTURE_ONLY_SOURCE_BRIDGE_REVIEW_PASS_NOT_FULL_GATE'
    assert audit['prior_source']==old_source and audit['current_source']==audit['source_after']==original
    assert audit['changed_paths']==[changed]and audit['all_original_fixture_bytes_outside_replaced_assertion_retained']is True
    assert audit['original_three_clips_required_all_LODs']is True and audit['new_look_only_active_LOD0_and3_master_and_web']is True
    assert audit['affected_native_command']==dict(ordinal=167,part=3,kind='step',command='node tools/test_working_driver_1904.mjs')
    assert audit['concrete_other_unqualified_affected_step']is None and audit['resources']['accepted']
    assert hashlib.sha256(git('show',old_source['TREE']+':'+changed)).hexdigest()==audit['old_fixture_sha256']
    assert sha(repo/changed)==audit['new_fixture_sha256']
    assert audit['supplemental_receipt']==binding['current_1904_fixture_receipt']
    fixture=referenced('current_1904_fixture_receipt')
    assert fixture['status']=='ACTUAL_ORIGINAL_1904_FIXTURE_AND_GENERIC_AUDIT_PASS_WITH_STRONGER_ACTIVE_CLIP_EXPECTATION'
    assert fixture['source_before']==fixture['source_after']==original and fixture['resources']['accepted']
    assert fixture['all_original_geometry_seat_foot_palm_LOD_assertions_retained']is True and fixture['whole_gate_PASS']is False
    required_supplements=[(['node','--check','tools/test_working_driver_1904.mjs'],5),
        (['node','tools/test_working_driver_1904.mjs'],120),
        (['python3','tools/audit_check_gates.py','--self-test'],120)]
    assert len(fixture['ledger'])==len(required_supplements)
    for row,(command,cap)in zip(fixture['ledger'],required_supplements):
        valid_native(dict(row,resources=fixture['resources']),command,cap)
        assert sha(row['log'])==row['log_sha256']
    envrepair=referenced('native_git_env_repair_receipt')
    assert envrepair['status']=='ACTUAL_FAILED_NATIVE_FIXTURE_PASS_WITH_CORRECT_NATIVE_GIT_ENV_NOT_FULL_GATE'
    assert envrepair['source_before']==envrepair['source_after']==old_source
    valid_native(envrepair,['node','tools/test_repo_file.mjs'],120)
    admission=dict(prior_native_coverage_receipt=binding['prior_native_coverage_receipt'],
        prior_source=old_source,current_source=original,changed_paths=[changed],
        prior_positive_parts=[1,2],fresh_required_native_parts=[3,4],
        prior_positive_part_evidence=binding['prior_positive_part_evidence'],
        independent_bridge_audit=binding['independent_bridge_audit'],current_1904_fixture_receipt=binding['current_1904_fixture_receipt'],
        unchanged_native_declarations=True,all_four_same_TREE=False,
        qualification='Actual prior nativeparts1/2 retain their original TREE in their ledger rows. Only the reviewed fixture selected by part3 changed; all other source inputs are byte-identical. Original part3 stopped negative is retained. Fresh original parts3/4 must actually pass on current staged source. Current PR CI will run the complete exact current tree.')
    assert source()==original
    before_all = guard.snapshot(); assert guard.check(before_all)['accepted']
    out.mkdir(parents=True); scratch = out / 'native-tmp'; scratch.mkdir(mode=0o700); env['TMPDIR'] = str(scratch)
    state = dict(status='RUNNING_NOT_PASS', created_utc=utc(), source_before=original,
        branch=binding['branch'], binding_path=str(args.binding), binding_sha256=binding_sha256, execution_pins=binding['execution_pins'],
        runner_sha256=sha(__file__), original_cap_per_part_seconds=600, expected_parts=expected,
        required_environment={k:env[k] for k in ['CHECK_JOBS','C4D_GATE_REQUIRE_READERS','C4D_GATE_REQUIRE_BASE','C4D_RULINGS_BASE']},
        native_distinct_steps=len(declarations), native_selftests=sum(kind=='selftest' for _,kind in declarations),
        ledger=prior_parts, prior_part1_admission=prior['prior_part1_admission'],
        reviewed_fixture_only_source_bridge=admission, prior_native_coverage_receipt=binding['prior_native_coverage_receipt'],
        current_1904_fixture_receipt=binding['current_1904_fixture_receipt'],
        independent_bridge_audit=binding['independent_bridge_audit'], native_git_env_repair_receipt=binding['native_git_env_repair_receipt'],
        prior_source=old_source, current_source=original, all_four_same_TREE=False,
        native_GIT_NO_LAZY_FETCH_absent=True, metadata_git_GIT_NO_LAZY_FETCH='1',
        resume_native_parts=[3,4], source_error=None, error=None)
    save(out / 'SOURCE-BEFORE.json', original); save(out / 'STATE.json', state)
    in_flight = False
    try:
        for part in range(3, 5):
            assert source() == original
            assert sha(args.binding) == binding_sha256
            for path, digest in binding['execution_pins'].items(): assert sha(path) == digest
            assert sha(__file__) == binding['runner_sha256']
            before = guard.snapshot(); assert guard.check(before)['accepted']
            command = ['./tools/check.sh', '--part', str(part) + '/4']; prefix = out / ('native-part-' + str(part))
            state.update(active_part=part, active_command=command); save(out / 'STATE.json', state)
            in_flight = True
            with Path(str(prefix) + '.supervisor.stdout').open('xb', buffering=0) as log:
                completed = subprocess.run([sys.executable, str(SUP), '--prefix', str(prefix), '--cwd', str(app),
                    '--timeout', '600', '--', *command], env=env, stdout=log, stderr=subprocess.STDOUT)
            result = load(str(prefix) + '.result.json'); cleanup = load(str(prefix) + '.cleanup.json')
            in_flight = not (cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'])
            after = guard.snapshot(); resources = guard.pair(before, after)
            try: after_source = source(); source_error = None
            except BaseException as error: after_source = None; source_error = repr(error)
            row = dict(part=part, command=command, result=result, cleanup=cleanup, resources=resources,
                resource_before=before, resource_after=after, source_before=original, source_after=after_source,
                source_error=source_error, log=str(prefix)+'.log', log_sha256=sha(str(prefix)+'.log'))
            body = Path(str(prefix)+'.log').read_text(errors='replace')
            (out / ('part-' + str(part) + '-RAW-FOOTER.txt')).write_text('\n'.join(ANSI.sub('',body).splitlines()[-12:])+'\n')
            state['ledger'].append(row); save(out / 'STATE.json', state)
            assert completed.returncode == result['returncode'] == 0 and not result['timed_out']
            assert result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 600
            assert result['timeout_override_reason'] is None
            assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted']
            assert after_source == original, source_error
            row['native_footer_counts'] = footer(body, part)
            save(out / 'STATE.json', state)
        overlap = 3 * sum(bool(every) for every,_ in declarations)
        selftest_overlap = 3 * sum(bool(every) and kind=='selftest' for every,kind in declarations)
        assert len(state['ledger']) == 4
        assert sum(row['native_footer_counts']['selected_steps'] for row in state['ledger']) - overlap == len(declarations)
        assert sum(row['native_footer_counts']['selftests'] for row in state['ledger']) - selftest_overlap == state['native_selftests']
        assert sha(args.binding) == binding_sha256 and sha(__file__) == binding['runner_sha256']
        for path, digest in binding['execution_pins'].items(): assert sha(path) == digest
        state.update(status='FULL_NATIVE_COVERAGE_PASS_WITH_REVIEWED_FIXTURE_ONLY_SOURCE_BRIDGE', source_after=source(),
            fresh_native_part_seconds=sum(row['result']['seconds'] for row in state['ledger'][2:]),
            every_part_execution_overlap=overlap, total_native_part_seconds=sum(row['result']['seconds'] for row in state['ledger']))
    except BaseException as error:
        state.update(status='NONPASS_NO_AUTOMATIC_RETRY', error=repr(error))
        try: state['source_after'] = source()
        except BaseException as source_error: state['source_error'] = repr(source_error)
    finally:
        state['resources'] = guard.pair(before_all, guard.snapshot())
        if not state['resources']['accepted']: state['status'] = 'NONPASS_RESOURCE_GUARD'
        safe_cleanup = not in_flight and all(row['cleanup']['cleanup_complete'] and not row['cleanup']['remaining_owned_children'] for row in state['ledger'])
        if safe_cleanup and scratch.exists(): shutil.rmtree(scratch)
        state.update(owned_TMPDIR_cleanup_complete=not scratch.exists(), closed_utc=utc())
        if scratch.exists(): state['status'] = 'NONPASS_OWNED_NATIVE_SCRATCH_RETAINED'
        save(out / 'STATE.json', state); save(out / 'CLOSED.json', state)
    print(json.dumps(dict(status=state['status'], receipt=str(out/'CLOSED.json'))), flush=True)
    return 0 if state['status'] == 'FULL_NATIVE_COVERAGE_PASS_WITH_REVIEWED_FIXTURE_ONLY_SOURCE_BRIDGE' else 1

if __name__ == '__main__':
    raise SystemExit(main())
