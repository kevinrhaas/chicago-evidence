"""S4 recoverable source-capture CHECKPOINT ONLY; final fresh-DEV integration/gates required."""
from pathlib import Path
import base64, hashlib, json, os, re, stat, subprocess, sys, urllib.request

P = Path(__file__).resolve().parent
ROOT = Path('/dev/shm/chicago-t1789-charles-gate-20261110')
APP = ROOT / 'chicago/4d'
GATE = Path('/tmp/t1789-settler-s4-source-full-gate-prep-20261111')
APPLY = Path('/tmp/ROOT-T1789-S4-PW-DOCKER-APPLY-PREP-20261111/APPLY-RECEIPT.json')
BASE = Path('/tmp/t1789-settler-s3-source-full-gate-prep-20261111/FREEZE.json')
BASE_SHA = '6944115f9392d917e16bcc4fe0c1adf490bc58ec64373b09d25467118084fa41'
OLD = '0a57979840bea7c37ba41ba4e24133a9510b59b9'
SOURCE_TREE = '60695ea8050960aa8c7f9c7570992ebf5ed60057'
SOURCE_FREEZE_SHA = 'aad9166c694b9df7708071918f901f7afc52726f908db997b9fb0779ab2edb8f'
SOURCE_APPLY_SHA = 'f3149153c18c50c1d65814e90459897026eb888f821993d3a097cc124e3062c1'
BRANCH = 'steward/t1789-1812-loose-linen-seat-20261111'
PROTECTED = 'refs/heads/steward/t1789-charles-woven-coat-20261110'
PRIMARY = '9453fa44842225bdb9de2c687cf7dca2f8a8211d'
CHANGED = frozenset(('.github/workflows/chicago-4d-humans.yml',
    'chicago/4d/docs/STATUS.md', 'chicago/4d/docs/ROADMAP.md'))
METADATA_ONLY = frozenset(n for n in CHANGED if '/docs/' in n)
NATIVE = frozenset(f'chicago/4d/assets/humans/{web}settler_1812.lod{lod}.glb'
                   for web in ('', 'web/') for lod in range(4))
NATIVE_FIXTURE = NATIVE | {'chicago/4d/data/humans/fixture.measure.json'}
ENV = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0')
READ_ENV = dict(ENV)
READ_ENV.pop('GIT_NO_LAZY_FETCH', None)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, env=ENV):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], env=env).decode().strip()


def save(path, body):
    assert not path.exists(), str(path)
    path.write_text(json.dumps(body, indent=2) + '\n')


def original_closure(c, timeout):
    assert c['accepted'] is True
    r, k, g = c['result'], c['cleanup'], c['resources']
    assert r['returncode'] == 0 and r['timed_out'] is False
    assert r['requested_timeout_seconds'] == r['effective_timeout_seconds'] == timeout
    assert r['timeout_override_reason'] is None
    assert k['cleanup_complete'] and not k['remaining_owned_children'] and g['accepted']
    assert g['before']['accepted'] and g['after']['accepted']


def prior(phase, name):
    c = json.loads((P / phase / 'CLOSED.json').read_text())
    original_closure(c, 120)
    assert c['binding_SHA256'] == BINDING_SHA
    path = P / phase / (name + '-RECEIPT.json')
    assert sha(path) == c['receipt_SHA256']
    return json.loads(path.read_text())


def remote_head(branch):
    rows = git('ls-remote', 'origin', 'refs/heads/' + branch, env=READ_ENV).splitlines()
    assert len(rows) == 1 and rows[0].split()[1] == 'refs/heads/' + branch
    return rows[0].split()[0]


def ancestor(a, b):
    r = subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', a, b], env=ENV)
    assert r.returncode in (0, 1)
    return r.returncode == 0


def qualified_gate():
    assert sha(GATE / 'SOURCE-PINS.json') == 'f8dc2877f8047b4f991f58ca2ed98654343e0c2c39c87af4750b3c3e5593eb54'
    for name, pin in json.loads((GATE / 'SOURCE-PINS.json').read_text()).items():
        assert sha(GATE / name) == pin, name
    assert sha(BASE) == BASE_SHA
    assert sha(APPLY) == B['apply_receipt_SHA256']
    assert sha(APPLY.parent / 'CLOSED.json') == '26a98226e460b0ffccdf8348825e30775798a05fcab59aa49ec6ebaf0f7d94be'
    apply_closed = json.loads((APPLY.parent / 'CLOSED.json').read_text())
    original_closure(apply_closed, 120)
    assert apply_closed['receipt_SHA256'] == B['apply_receipt_SHA256']
    apply = json.loads(APPLY.read_text())
    assert apply['head'] == OLD and apply['index_tree'] == TREE
    assert set(apply['staged_paths']) == CHANGED
    assert apply['baseline301_SHA256'] == BASE_SHA
    assert apply['native8_and_fixture_unchanged'] and apply['primary_ref_unchanged']
    freeze = GATE / 'FREEZE.json'
    assert sha(freeze) == FREEZE_SHA
    d = json.loads(freeze.read_text())
    before = json.loads(BASE.read_text())
    assert d['head'] == OLD and d['index_tree'] == TREE and d['branch'] == BRANCH
    assert d.get('incoming_dev') is None and not d.get('deleted_paths', [])
    assert d['root'] == str(ROOT) and d['protected_ref'] == PROTECTED
    assert d['protected_ref_head'] == PRIMARY and d['baseline301_SHA256'] == BASE_SHA
    assert d['frozen_file_count'] == len(d['rows']) == 301 and d['parts'] == 16
    assert d['CHECK_JOBS'] == 4 and set(d['expected_staged_paths']) == CHANGED
    assert d['old_native8_and_current_fixture_byte_exact'] and not d['native_asset_adoption']
    assert d['apply_receipt'] == str(APPLY) and d['apply_receipt_SHA256'] == B['apply_receipt_SHA256']
    assert sha(Path(d['wrapper'])) == d['wrapper_SHA256']
    assert json.loads((GATE / 'READY.json').read_text())['freeze_SHA256'] == FREEZE_SHA
    assert sha(GATE / 'FREEZE-CLOSED.json') == '85feff52b94e3a7868ae1e090e118d9cda30367e24b678e77838551cc5dee0f6'
    freeze_closed = json.loads((GATE / 'FREEZE-CLOSED.json').read_text())
    original_closure(freeze_closed, 120)
    assert freeze_closed['freeze_SHA256'] == FREEZE_SHA
    by = {r['file']: r for r in d['rows']}
    old = {r['file']: r for r in before['rows']}
    assert len(by) == len(old) == 301 and set(by) == set(old)
    assert NATIVE_FIXTURE <= set(d['protected_native_and_fixture_paths'])
    for name in set(old) - CHANGED:
        assert by[name] == old[name], name
    a_path = GATE / 'AGGREGATE.json'
    assert sha(a_path) == B['aggregate_SHA256']
    a = json.loads(a_path.read_text())
    assert a['status'] == 'ALL16_S4_SOURCE_GATE_PARTS_PASS_NOT_NATIVE_QUALIFICATION'
    assert a['head'] == OLD and a['branch'] == BRANCH and a['index_tree'] == TREE
    assert a['freeze_SHA256'] == FREEZE_SHA and a['frozen_files'] == 301
    assert a['protected_primary_ref'] == PROTECTED and a['protected_primary_head'] == PRIMARY
    assert a['native8_fixture_unchanged'] and a['prior_S2_gate_claims_reused'] is False and a['prior_S3_gate_claims_reused'] is False
    assert len(a['parts']) == a['partition_count'] == 16 and a['CHECK_JOBS'] == 4
    assert not a.get('deleted_paths', []) and a.get('incoming_dev') is None
    total = 0
    for i in range(1, 17):
        path = GATE / f'part{i}.CLOSED.json'
        c = json.loads(path.read_text())
        part = a['parts'][i - 1]
        assert part['part'] == i and sha(path) == part['CLOSED_SHA256']
        original_closure(c, 600)
        assert c['part'] == i and c['freeze_SHA256'] == FREEZE_SHA
        assert c['CHECK_JOBS'] == 4 and c['partition_count'] == 16
        log = GATE / f'part{i}.log'
        assert sha(log) == c['log_SHA256']
        assert log.read_text(errors='replace').count('S4_SOURCE_VERIFIED ' + FREEZE_SHA) == 2
        assert len(c['actual_final_markers']) == 1
        match = re.fullmatch(r'CHECK PASS — part ' + str(i) + r'/16: (\d+) steps, none red\.',
                             c['actual_final_markers'][0])
        assert match and int(match.group(1)) == part['steps']
        total += part['steps']
    assert total == a['sum_part_executions']
    return d, a


def verify_worktree(d, head, committed):
    assert Path.cwd() == APP and git('branch', '--show-current') == BRANCH
    assert git('rev-parse', 'HEAD') == head and git('rev-parse', '--verify', PROTECTED) == PRIMARY
    assert not (Path(git('rev-parse', '--absolute-git-dir')) / 'MERGE_HEAD').exists()
    assert git('ls-files', '-u') == '' and git('diff', '--name-only') == ''
    assert git('write-tree') == TREE
    if committed:
        assert git('status', '--porcelain=v1', '--untracked-files=no') == ''
        assert git('rev-parse', 'HEAD^{tree}') == TREE
        assert git('show', '-s', '--format=%P', 'HEAD').split() == [OLD]
    else:
        assert set(git('diff', '--cached', '--name-only').splitlines()) == CHANGED
    for row in d['rows']:
        path = ROOT / row['file']
        info = path.lstat()
        assert stat.S_ISREG(info.st_mode) and not path.is_symlink()
        assert info.st_size == row['bytes'] and sha(path) == row['sha256'], row['file']
        assert ('100755' if info.st_mode & stat.S_IXUSR else '100644') == row['Git_mode']


def fresh_dev():
    gitdir = Path(git('rev-parse', '--absolute-git-dir'))
    assert (gitdir / 'objects').stat().st_dev == ROOT.stat().st_dev
    subprocess.run(['git', '-C', str(ROOT), 'fetch', '--no-tags', '--filter=blob:none',
                    'origin', 'refs/heads/dev:refs/remotes/origin/dev'], env=READ_ENV, check=True)
    value = git('rev-parse', 'origin/dev')
    assert value == remote_head('dev'), 'DEV advanced during fetch: STOP, no current-base question claimed'
    return value


def pr_questions(dev, head):
    base = git('merge-base', 'origin/dev', head)
    subprocess.run(['node', 'tools/check-changelog-entry.mjs', base, head], cwd=APP, env=READ_ENV, check=True)
    subprocess.run(['node', 'tools/resolve_id_collisions.mjs', '--base', 'origin/dev', '--check'], cwd=APP, env=READ_ENV, check=True)
    assert remote_head('dev') == dev, 'DEV advanced during questions: STOP'
    return dict(fresh_DEV=dev, merge_base=base, changelog_question=True, ID_collision_question=True,
                source_includes_fresh_DEV=ancestor(dev, head), DEV_advanced_since_binding=dev != B['expected_DEV'],
                source_checkpoint_only=True, needs_final_DEV_integration=True, merge_ready=False)


def commit_phase(d, a):
    out = P / 'COMMIT'
    verify_worktree(d, OLD, False)
    assert remote_head(BRANCH) == OLD
    dev = fresh_dev()  # Metadata observation only; the frozen source tree stays unchanged.
    git('diff', '--cached', '--check')
    message = out / 'COMMIT-MESSAGE.txt'
    assert not message.exists()
    message.write_text('Checkpoint the pinned Playwright container path for humans CI\n\n'
        'Run the existing browser checks in the matching pinned Playwright container to avoid runner apt mirror DNS failures.\n'
        'Retain native build and render ownership, the canonical eight capture files, producer arguments and caps.\n'
        'All sixteen source partitions passed this exact three-path source tree; old native parents and fixture remain unchanged.\n'
        'Recoverable draft source-capture checkpoint only: latest DEV is not yet integrated.\n'
        'Final asset adoption must integrate fresh DEV, then pass the final asset/source gate and published smoke before merge.\n'
        'The three failed canonical captures remain recorded; no new native assets or fit acceptance is claimed.\n\n'
        'Changelog: none — workflow browser runtime repair only; no human assets, measurements or rendered garment change.\n')
    subprocess.run(['git', '-C', str(ROOT), 'commit', '--file', str(message)], env=ENV, check=True)
    head = git('rev-parse', 'HEAD')
    save(out / 'LOCAL-HEAD-CHECKPOINT.json', dict(head=head, parents_expected=[OLD], tree_expected=TREE, push=False))
    assert git('show', '-s', '--format=%P', 'HEAD').split() == [OLD]
    assert set(git('diff', '--name-only', OLD, head).splitlines()) == CHANGED
    verify_worktree(d, head, True)
    save(out / 'COMMIT-RECEIPT.json', dict(status='NORMAL_ONE_PARENT_S4_SOURCE_CAPTURE_CHECKPOINT_NOT_PUSHED',
        head=head, parents=[OLD], tree=TREE, APP_tree=git('rev-parse', 'HEAD:chicago/4d'),
        freeze_SHA256=FREEZE_SHA, aggregate_SHA256=B['aggregate_SHA256'], binding_SHA256=BINDING_SHA,
        all16_source_parts_pass=True, frozen301_preserved=True, native8_fixture_unchanged=True,
        protected_primary_ref=PROTECTED, protected_primary_head=PRIMARY, remote_feature_before_commit=OLD,
        DEV_reference_at_binding=B['expected_DEV'], fresh_DEV_observed=dev,
        source_includes_fresh_DEV=ancestor(dev, head), source_checkpoint_only=True, needs_final_DEV_integration=True,
        source_only=True, native_qualification='PENDING',
        push=False, DEV_merge=False, merge_ready=False))


def preflight_phase(d, a):
    c = prior('COMMIT', 'COMMIT')
    verify_worktree(d, c['head'], True)
    questions = pr_questions(fresh_dev(), c['head'])
    verify_worktree(d, c['head'], True)
    save(P / 'PREFLIGHT' / 'PREFLIGHT-RECEIPT.json', dict(
        status='BOTH_ACTUAL_S4_CHECKPOINT_PR_EVENT_QUESTIONS_PASS_NOT_FINAL_QUALIFICATION', head=c['head'], tree=TREE,
        **questions, binding_SHA256=BINDING_SHA, all16_source_parts_pass_exact_tree=True,
        source_files_written=False, push=False, DEV_merge=False, native_qualification='PENDING'))


def push_phase(d, a):
    c, p = prior('COMMIT', 'COMMIT'), prior('PREFLIGHT', 'PREFLIGHT')
    assert p['head'] == c['head'] and p['changelog_question'] and p['ID_collision_question']
    verify_worktree(d, c['head'], True)
    assert ancestor(OLD, c['head'])
    dev = fresh_dev()
    questions = p if dev == p['fresh_DEV'] else pr_questions(dev, c['head'])
    assert remote_head(BRANCH) == OLD
    save(P / 'PUSH' / 'LOCAL-HEAD-CHECKPOINT.json', dict(head=c['head'], parents=[OLD], tree=TREE,
         branch=BRANCH, remote_expected=OLD, before_push=True))
    hooks = subprocess.run(['git', '-C', str(ROOT), 'config', '--path', '--get', 'core.hooksPath'],
                           env=ENV, capture_output=True, text=True)
    assert hooks.returncode in (0, 1)
    if hooks.returncode == 0:
        hp = Path(hooks.stdout.strip())
        hp = hp if hp.is_absolute() else ROOT / hp
    else:
        hp = Path(git('rev-parse', '--git-common-dir'))
        hp = (hp if hp.is_absolute() else ROOT / hp) / 'hooks'
    original = hp / 'pre-push'
    original_path = str(original.resolve()) if original.is_file() and os.access(original, os.X_OK) else ''
    env = dict(READ_ENV, T1789_EXPECTED_SOURCE_HEAD=c['head'], T1789_EXPECTED_REF='refs/heads/' + BRANCH,
               T1789_EXPECTED_OLD_HEAD=OLD, T1789_ORIGINAL_PRE_PUSH=original_path)
    attempt = dict(head=c['head'], destination='refs/heads/' + BRANCH, remote_expected=OLD,
                   fresh_DEV=dev, force=False, original_pre_push=original_path)
    save(P / 'PUSH' / 'PUSH-ATTEMPT.json', attempt)
    result = subprocess.run(['git', '-C', str(ROOT), '-c', 'core.hooksPath=' + str(P / 'PUSH/hooks'),
                             'push', 'origin', 'HEAD:refs/heads/' + BRANCH], env=env, check=False)
    if result.returncode:
        save(P / 'PUSH' / 'PUSH-FAILED.json', dict(**attempt, returncode=result.returncode,
             local_head_preserved=git('rev-parse', 'HEAD'), automatic_retry=False))
        raise SystemExit(result.returncode)
    advertised = json.loads((P / 'PUSH' / 'ADVERTISED-EXPECTED-OLD.json').read_text())
    assert advertised['remote_oid'] == OLD and advertised['head'] == c['head']
    assert remote_head(BRANCH) == c['head']
    verify_worktree(d, c['head'], True)
    save(P / 'PUSH' / 'PUSH-RECEIPT.json', dict(status='NORMAL_OWN_FEATURE_FAST_FORWARD_S4_SOURCE_CHECKPOINT_PUSH_VERIFIED',
        head=c['head'], parents=[OLD], tree=TREE, branch=BRANCH, remote_expected_before=OLD,
        advertised_remote_oid=OLD, fresh_DEV_before_push=dev, preflight=questions,
        source_includes_fresh_DEV=questions['source_includes_fresh_DEV'], source_checkpoint_only=True, needs_final_DEV_integration=True,
        remote_DEV_after_push=remote_head('dev'), binding_SHA256=BINDING_SHA, force=False,
        DEV_push_or_merge=False, merge_ready=False, production=False, native_qualification='PENDING'))


def remote_phase(d, a):
    c, p = prior('COMMIT', 'COMMIT'), prior('PUSH', 'PUSH')
    assert p['head'] == c['head']
    verify_worktree(d, c['head'], True)
    assert remote_head(BRANCH) == c['head']
    calls, cache = [], {}
    def get(endpoint, limit=1048576):
        req = urllib.request.Request('https://api.github.com/repos/kevinrhaas/chicago/' + endpoint,
              headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'codex-S4-remote-proof'})
        with urllib.request.urlopen(req, timeout=20) as response:
            assert response.status == 200
            raw = response.read(limit + 1)
        assert len(raw) <= limit
        calls.append(dict(endpoint=endpoint, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
        return json.loads(raw)
    commit = get('git/commits/' + c['head'])
    assert commit['sha'] == c['head'] and commit['tree']['sha'] == TREE
    assert [r['sha'] for r in commit['parents']] == [OLD]
    def directory(oid):
        if oid not in cache:
            tree = get('git/trees/' + oid)
            assert tree['sha'] == oid and not tree.get('truncated')
            assert len({r['path'] for r in tree['tree']}) == len(tree['tree'])
            cache[oid] = {r['path']: r for r in tree['tree']}
        return cache[oid]
    def entry_for(name):
        oid, parts = TREE, name.split('/')
        for part in parts[:-1]:
            entry = directory(oid)[part]
            assert entry['type'] == 'tree'
            oid = entry['sha']
        return directory(oid)[parts[-1]]
    rows = {r['file']: r for r in d['rows']}
    verified = []
    for name in sorted(CHANGED):
        entry, row = entry_for(name), rows[name]
        assert entry['type'] == 'blob' and entry['sha'] == row['Git_blob_OID']
        assert entry['mode'] == row['Git_mode'] and entry['size'] == row['bytes']
        result = dict(file=name, Git_blob_OID=entry['sha'], Git_mode=entry['mode'],
                      bytes=entry['size'], local_SHA256=row['sha256'], remote_body_verified=False)
        if name not in METADATA_ONLY:
            assert row['bytes'] <= 65536
            body = get('git/blobs/' + entry['sha'], 131072)
            assert body['encoding'] == 'base64'
            raw = base64.b64decode(body['content'])
            assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
            assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == entry['sha']
            result['remote_body_verified'] = True
        verified.append(result)
    assert len(verified) == 3 and sum(r['remote_body_verified'] for r in verified) == 1
    assert {r['file'] for r in verified if not r['remote_body_verified']} == METADATA_ONLY
    assert remote_head(BRANCH) == c['head']
    verify_worktree(d, c['head'], True)
    save(P / 'REMOTE-VERIFY' / 'REMOTE-RECEIPT.json', dict(
        status='EXACT_S4_SOURCE_CHECKPOINT_PARENT_TREE_THREE_ENTRIES_ONE_WORKFLOW_BODY_VERIFIED', head=c['head'],
        parents=[OLD], tree=TREE, freeze_SHA256=FREEZE_SHA, binding_SHA256=BINDING_SHA,
        all301_local_frozen_SHA256_bytes_modes_preserved=True, remote_changed_entries=verified,
        API_GETs=calls, large_docs_or_assets_downloaded=False, all301_remote_raw_bodies_claimed=False,
        protected_primary_ref=PROTECTED, protected_primary_head=PRIMARY, remote_DEV_observed=remote_head('dev'),
        source_only=True, source_checkpoint_only=True, needs_final_DEV_integration=True,
        source_includes_fresh_DEV=p['source_includes_fresh_DEV'], fresh_DEV_basis_for_ancestry=p['fresh_DEV_before_push'],
        merge_ready=False, source_request_H4=None, native_qualification='PENDING',
        DEV_merge=False, production=False))


if __name__ == '__main__':
    phase = sys.argv[1]
    assert phase in ('COMMIT', 'PREFLIGHT', 'PUSH', 'REMOTE-VERIFY')
    BINDING_SHA = os.environ['T1789_S4_POSTGATE_BINDING_SHA256']
    assert re.fullmatch('[0-9a-f]{64}', BINDING_SHA)
    assert sha(P / 'BINDING.json') == BINDING_SHA
    B = json.loads((P / 'BINDING.json').read_text())
    assert B['status'] == 'ROOT_REVIEWED_ACTUAL_S4_ALL16_POSTGATE_BINDING'
    assert B['expected_head'] == OLD and B['expected_branch'] == BRANCH
    for key in ('freeze_SHA256', 'aggregate_SHA256', 'apply_receipt_SHA256'):
        assert re.fullmatch('[0-9a-f]{64}', B[key])
    for key in ('index_tree', 'expected_DEV'):
        assert re.fullmatch('[0-9a-f]{40}', B[key])
    assert B['source_checkpoint_only'] is True and B['needs_final_DEV_integration'] is True and B['merge_ready'] is False
    TREE, FREEZE_SHA = B['index_tree'], B['freeze_SHA256']
    assert TREE == SOURCE_TREE and FREEZE_SHA == SOURCE_FREEZE_SHA and B['apply_receipt_SHA256'] == SOURCE_APPLY_SHA
    d, a = qualified_gate()
    {'COMMIT': commit_phase, 'PREFLIGHT': preflight_phase, 'PUSH': push_phase,
     'REMOTE-VERIFY': remote_phase}[phase](d, a)
