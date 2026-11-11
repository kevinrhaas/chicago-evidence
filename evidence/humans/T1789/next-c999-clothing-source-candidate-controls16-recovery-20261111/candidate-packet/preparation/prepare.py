from pathlib import Path
import ast, difflib, hashlib, json, os, subprocess

P = Path(__file__).resolve().parent
OUT = Path('/tmp/T1789-NEXT-CLOTHING-C999-SOURCE-CANDIDATE-20261111')
HEAD = 'c9990d8b32517612a94e339a98bd5700436b5689'
OLD = '59914c3f279705cd94e4c9ad5252383ee2d940d2'
GIT = Path('/tmp/T1789-1812-MEMORY-READONLY-DIAGNOSIS-20261111/readonly-objects.git')
ENV = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')
APP = Path('/dev/shm/chicago-t1789-charles-gate-20261110/chicago/4d')
BUNDLE = Path('/tmp/T1789-CLOTHING-BUNDLE-SOURCE-CANDIDATE-20261111')
OLD_WORK = Path('/tmp/chicago-t1789-clothing-bundle-next-20261111')
MALE = Path('/tmp/T1789-MALE-STOCK-RIM-SOURCE-CANDIDATE-20261111')
PREFIX = 'chicago/4d/'
LINEN = {PREFIX+n for n in ['data/humans/recipes/settler_1812.json',
    'tools/human_linen_seat.py', 'tools/human_settler_1812.py', 'tools/test_human_linen_seat.py']}

def sha(raw): return hashlib.sha256(raw).hexdigest()
def oid(raw): return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def git(*args):
    r = subprocess.run(['git', '--git-dir='+str(GIT), *args], env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with (P/'IMMUTABLE-OBJECT-READS.log').open('ab') as stream:
        stream.write((json.dumps(list(args))+'\n').encode()); stream.write(r.stderr)
    if r.returncode: raise RuntimeError('Immutable object read failed: '+repr(args))
    return r.stdout
def entry(ref, name):
    raw = git('ls-tree', '-z', ref, '--', name)
    if not raw: return None
    assert raw.count(b'\0') == 1
    header, actual = raw[:-1].split(b'\t'); mode, kind, obj = header.decode().split()
    assert actual.decode() == name and mode in ('100644', '100755') and kind == 'blob'
    data = git('cat-file', 'blob', obj)
    assert oid(data) == obj
    return dict(mode=mode, Git_blob_OID=obj, bytes=len(data), sha256=sha(data), data=data)
def facts(row): return {k:v for k,v in row.items() if k != 'data'} if row else None
def write(name, raw):
    target = OUT/name; target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream: stream.write(raw)
def save(name, value): write(name, (json.dumps(value, indent=2)+'\n').encode())

assert not OUT.exists(), 'Fresh offline candidate only; no overwrite'
OUT.mkdir()
bundle = json.loads((BUNDLE/'CANDIDATE.json').read_text())
assert sha((BUNDLE/'COMBINED-SOURCE.patch').read_bytes()) == 'd666641863d5a10d0da9606dd99fdcf5dde5477aad98caff36abfe669237fc9e'
assert sha((MALE/'candidate.patch').read_bytes()) == 'a58ce83921261b68bd1703100cb3471dbd9ee687d9f6996ad264085efa7e6f20'
assert sha((MALE/'MANIFEST.json').read_bytes()) == '64db97267e938d8370524021d69f64c2ddc94b943b07611ad00563fa48f2bb78'
assert git('rev-parse', HEAD+'^{tree}').decode().strip() == '1dced78ea49426b9f4c4b9f52ef79db47f06facf'
changes = []; excluded = []; protected = []; imported = {}
for row in bundle['candidate_files']:
    name = row['file']; raw = (OLD_WORK/name).read_bytes()
    assert len(raw) == row['bytes'] and sha(raw) == row['sha256'], name
    if name in LINEN:
        base = entry(HEAD, name); assert base is not None
        assert (APP/name.removeprefix(PREFIX)).read_bytes() == base['data']
        write('protected/'+name, base['data'])
        excluded.append(dict(file=name, reason='Existing S2 linen retained byte-exact; no old hunk imported',
            current_c999=facts(base), old_bundle_candidate_sha256=sha(raw),
            old_bundle_candidate_equals_c999=raw == base['data']))
        continue
    old = entry(OLD, name); base = entry(HEAD, name)
    if base is not None and base['data'] == raw:
        excluded.append(dict(file=name, reason='Already exact in c999', current_c999=facts(base)))
        continue
    if (old is None) != (base is None) or old is not None and old['data'] != base['data']:
        save('CONFLICT-STOP.json', dict(file=name, old_base=facts(old), current_base=facts(base),
            reason='Baseline differs; no unreviewed merge or scope expansion'))
        raise SystemExit('STOP: concrete component baseline conflict '+name)
    imported[name] = (raw, base, 'prior remaining clothing bundle')

for name in ['tools/human_merchant_1835.py', 'tools/human_collar_rim.py', 'tools/test_human_collar_rim.py']:
    full = PREFIX+name; base = entry(HEAD, full); raw = (MALE/'candidate'/name).read_bytes()
    expected_before = MALE/'before'/name
    assert full not in imported
    assert (base is None and not expected_before.exists()) or (base is not None and expected_before.read_bytes() == base['data'])
    imported[full] = (raw, base, 'male stock-rim candidate')

patch = []
for name, (raw, base, origin) in sorted(imported.items()):
    if base is not None:
        assert (APP/name.removeprefix(PREFIX)).read_bytes() == base['data'], name
        write('before/'+name, base['data'])
    else:
        assert not (APP/name.removeprefix(PREFIX)).exists(), name
    write('candidate/'+name, raw)
    mode = base['mode'] if base else '100644'
    after = dict(mode=mode, Git_blob_OID=oid(raw), bytes=len(raw), sha256=sha(raw))
    changes.append(dict(file=name, origin=origin, before=facts(base), after=after))
    patch.append('diff --git a/'+name+' b/'+name+'\n')
    if base is None: patch.append('new file mode '+mode+'\n')
    patch.extend(difflib.unified_diff((base['data'].decode() if base else '').splitlines(True),
        raw.decode().splitlines(True), fromfile='a/'+name if base else '/dev/null', tofile='b/'+name))
    if name.endswith('.py'): ast.parse(raw, filename=name)
    if name.endswith('.json'): json.loads(raw)
write('NEXT-SOURCE.patch', ''.join(patch).encode())
assert len(changes) == 19 and len([r for r in excluded if r['file'] in LINEN]) == 4
assert not LINEN & {r['file'] for r in changes}

for name in ['data/humans/materials/charles-coat-woven-v1.json',
    'data/humans/materials/charles-coat-woven-v1.admission.json',
    'data/humans/materials/charles-coat-woven-v1.derivation.json']:
    full = PREFIX+name; base = entry(HEAD, full); assert base is not None
    assert (APP/name).read_bytes() == base['data']
    write('protected/'+full, base['data']); protected.append(dict(file=full, **facts(base)))
save('PATH-BEFORE-AFTER.json', changes)
save('LINEN-EXCLUDED-UNCHANGED.json', excluded)
save('FROZEN-FINEWOOL-V1-UNCHANGED.json', protected)
save('PREPARED-COMPOSITION.json', dict(status='SOURCE_ONLY_COMPOSED_NO_TESTS_OR_NATIVE_RUN',
    base=HEAD, base_tree='1dced78ea49426b9f4c4b9f52ef79db47f06facf', changed_paths=len(changes),
    patch_sha256=sha((OUT/'NEXT-SOURCE.patch').read_bytes()), linen_preserved=len(LINEN),
    unchanged_finewool_v1_files=len(protected), APP_Git_index_refs_or_source_writes=False,
    source_AST_and_JSON_parse_only=True, tests_run=False, native_fit_accepted=False))
print(json.dumps(dict(output=str(OUT), paths=len(changes), patch_sha256=sha((OUT/'NEXT-SOURCE.patch').read_bytes()),
    linen_preserved=4, finewool_v1_preserved=3, tests_run=False)))
