from pathlib import Path
import hashlib, importlib.util, json, os, resource, stat, subprocess, sys, time

P = Path(__file__).resolve().parent
plan = json.loads((P/'PLAN.json').read_text())
out = Path(plan['output'])
def pins():
    for row in plan['pins']:
        file = Path(row['file'])
        assert stat.S_ISREG(file.lstat().st_mode) and not file.is_symlink(), str(file)
        assert hashlib.sha256(file.read_bytes()).hexdigest() == row['sha256'], str(file)
    root = Path(plan['candidate_packet'])
    for prefix in ('candidate', 'protected'):
        found = {f.relative_to(root).as_posix() for f in (root/prefix).rglob('*') if f.is_file() or f.is_symlink()}
        assert found == set(plan['closed_overlay_members'][prefix]), 'Overlay membership changed: '+prefix
def save(name, data):
    with (out/name).open('x') as stream: json.dump(data, stream, indent=2); stream.write('\n')
pins()
spec = importlib.util.spec_from_file_location('reviewed_s2_postgate', plan['source_guard'])
guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
os.chdir(guard.APP)
freeze, aggregate = guard.qualified_gate()
guard.verify_worktree(freeze, plan['source_head'], True)
source = dict(head=plan['source_head'], tree=guard.TREE, frozen_files=len(freeze['rows']),
    protected_primary=guard.PRIMARY, native8_fixture_preserved=True,
    guard_chain_SHA256=hashlib.sha256(Path(plan['source_guard']).read_bytes()).hexdigest(),
    candidate_patch_SHA256=plan['candidate_patch_SHA256'], candidate19_and_protected7_unchanged=True)
save('SOURCE-BEFORE.json', source)
def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
command = [sys.executable, '-B', str(P/'test_entry.py')]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
    PYTHONPATH=plan['candidate_tools']+os.pathsep+plan['canonical_tools'])
record = dict(command=command, source_only=True, inner_wall_seconds=60,
    CPU_limit_seconds=30, address_space_limit_bytes=512*1024*1024,
    returncode=None, timed_out=False, automatic_retry=False)
started = time.monotonic()
try:
    with (out/'tests.log').open('xb') as log:
        try:
            result = subprocess.run(command, cwd=plan['candidate_tools'], env=env,
                stdout=log, stderr=subprocess.STDOUT, timeout=60, preexec_fn=limits)
            record['returncode'] = result.returncode
        except subprocess.TimeoutExpired:
            record.update(returncode=124, timed_out=True)
finally:
    record['test_subprocess_seconds'] = time.monotonic()-started
    try:
        guard.qualified_gate(); guard.verify_worktree(freeze, plan['source_head'], True); pins()
        save('SOURCE-AFTER.json', source)
        record['source_301_head_tree_primary_native8_fixture_candidate19_protected7_preserved'] = True
    except BaseException as error:
        record['source_301_head_tree_primary_native8_fixture_candidate19_protected7_preserved'] = False
        record['source_closing_error'] = repr(error)
    entry = out/'TEST-ENTRY-RESULT.json'
    record['test_entry'] = json.loads(entry.read_text()) if entry.exists() else None
    record['native_fit_accepted'] = False
    save('TEST-RESULT.json', record)
    print((out/'tests.log').read_text(errors='replace'), end='')
    print(json.dumps(record))
accepted = (record['returncode'] == 0 and not record['timed_out']
    and record['source_301_head_tree_primary_native8_fixture_candidate19_protected7_preserved']
    and record['test_entry'] is not None and record['test_entry']['success'])
raise SystemExit(0 if accepted else 1)
