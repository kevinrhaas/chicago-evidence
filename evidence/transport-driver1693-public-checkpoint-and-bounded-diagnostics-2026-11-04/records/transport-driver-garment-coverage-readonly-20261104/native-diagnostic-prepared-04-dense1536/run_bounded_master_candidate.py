#!/usr/bin/env python3
"""One separately authorized 120-second master prototype window, after diagnosis."""
from pathlib import Path
import argparse, fcntl, hashlib, importlib.util, json, os, subprocess, sys
sys.dont_write_bytecode = True
from run_bounded_diagnostic import public_source_bridge

P = Path(__file__).resolve().parent
RUNTIME = Path('/workspace/.cloud-setup/transport-current-20261103')
SUP = Path('/workspace/.cloud-setup/transport-supervise.py')
LOCK = Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def save(p, value): Path(p).write_text(json.dumps(value, indent=2)+'\n')

def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--binding', type=Path, required=True); p.add_argument('--out', type=Path, required=True)
    a = p.parse_args(); cfg = load(a.binding); binding_sha256 = sha(a.binding)
    assert cfg['template_only'] is False and cfg['ROOT_EXPLICIT_MASTER_GARMENT_PROTOTYPE_GO'] is True
    assert cfg['schema'] == 'CURRENT_LOD0_GARMENT_TO_LOD3_MASTER_RETENTION_PROTOTYPE_V1'
    assert cfg['native_cap_seconds'] == 120 and cfg['production_web_generation_enabled'] is False
    repo = Path(cfg['repo']).resolve(); app = Path(cfg['app']).resolve(); out = a.out.resolve()
    assert app == repo/'chicago/4d'
    assert out != repo and repo not in out.parents and not out.exists(), 'Fresh external output only, before writes.'
    assert sys.version_info[:2] == (3, 11)
    assert sha(__file__) == cfg['candidate_runner_SHA256']
    for file, digest in cfg['input_pins'].items(): assert sha(file) == digest, file
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', UV_THREADPOOL_SIZE='1'); env.pop('GIT_NO_LAZY_FETCH', None)
    git_env = dict(env, GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1')
    def git(*argv): return subprocess.check_output(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', '-C', str(repo), *argv], env=git_env, timeout=30)
    def source():
        merge = Path(git('rev-parse', '--git-path', 'MERGE_HEAD').decode().strip())
        if not merge.is_absolute(): merge = repo/merge
        assert not merge.exists() and not git('status', '--porcelain').strip()
        return dict(HEAD=git('rev-parse', 'HEAD').decode().strip(), TREE=git('rev-parse', 'HEAD^{tree}').decode().strip(),
            semantic_index_sha256=hashlib.sha256(git('ls-files', '--stage', '-z')).hexdigest())
    before = source(); assert before == cfg['source']
    bridge = public_source_bridge(cfg, before, git)
    lock = LOCK.open('a+'); fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    spec = importlib.util.spec_from_file_location('garment_candidate_guard', RUNTIME/'resource_guard.py')
    guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
    baseline = guard.snapshot(); assert guard.check(baseline)['accepted']
    out.mkdir(parents=True, exist_ok=False); save(out/'SOURCE-BEFORE.json', before)
    prefix = out/'candidate-owner'; result = {}; cleanup = {}; prototype = {}; error = None; passed = False
    try:
        with (out/'candidate.stdout').open('xb') as log:
            q = subprocess.run([sys.executable, str(SUP), '--prefix', str(prefix), '--cwd', str(P), '--timeout', '120', '--',
                sys.executable, str(P/'prepare_master_garment_candidate.py'), '--recipe', str(a.binding.resolve()), '--out', str(out/'prototype')],
                env=env, stdout=log, stderr=subprocess.STDOUT)
        result = load(str(prefix)+'.result.json'); cleanup = load(str(prefix)+'.cleanup.json')
        proto = out/'prototype/PROTOTYPE-RECEIPT.json'
        if proto.exists(): prototype = load(proto)
        passed = (q.returncode == result['returncode'] == 0 and not result['timed_out']
            and result['requested_timeout_seconds'] == result['effective_timeout_seconds'] == 120
            and result['timeout_override_reason'] is None and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
            and prototype.get('status') == 'GARMENT_MASTER_RETENTION_PROTOTYPES_ONLY_NATIVE_POSE_AND_WORLD_UNQUALIFIED')
    except BaseException as ex: error = repr(ex)
    after = None; source_error = None
    try:
        after = source(); assert after == before
        for file, digest in cfg['input_pins'].items(): assert sha(file) == digest, file
        for path, digest in bridge['admitted_receipt_pins'].items(): assert sha(path) == digest
        for key in ['actual_native_diagnostic_closed', 'actual_native_diagnostic_report']:
            assert sha(cfg[key]['path']) == cfg[key]['sha256']
        assert sha(a.binding) == binding_sha256 == prototype.get('recipe_SHA256', binding_sha256)
    except BaseException as ex: source_error = repr(ex); passed = False
    resources = guard.pair(baseline, guard.snapshot()); passed = passed and resources['accepted']
    closed = dict(status='MASTER_GARMENT_PROTOTYPE_CREATED_NOT_NATIVE_FIT_OR_PRODUCTION_PASS' if passed else 'MASTER_GARMENT_PROTOTYPE_NONPASS',
        source_before=before, source_after=after, public_source_bridge=bridge, recipe_SHA256=sha(a.binding),
        result=result, cleanup=cleanup, resources=resources, error=error, source_error=source_error,
        prototype_receipt=str(out/'prototype/PROTOTYPE-RECEIPT.json'), current_assets_written=False,
        production_web_generated=False, garment_native_pose_contact_photo_or_world_acceptance=False)
    save(out/'CLOSED.json', closed); print(json.dumps(dict(status=closed['status'], receipt=str(out/'CLOSED.json'))))
    raise SystemExit(0 if passed else 1)

if __name__ == '__main__':
    main()
