from pathlib import Path
import contextlib, hashlib, importlib.util, io, json, stat, zipfile
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
S = lambda b: hashlib.sha256(b).hexdigest()
r = Path('/workspace/T3122-T3123-T3124-integration-20261024/closed-T3122-genuine25-native-before-check')
p = r / 'MANIFEST.json'
assert S(p.read_bytes()) == '980703ee2a80fb97fd9d65e6f72518c19621bbea8396eea91347f22b5ee0d1c7'
rows = json.loads(p.read_text())['files']
assert len(rows) == 18 and sum(z['bytes'] for z in rows) == 18006740
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and S(b) == z['sha256']
binding = json.loads((r / 'SOURCE-BINDING.json').read_text())
ziprows = []
with zipfile.ZipFile(r / 'UNCOMMITTED-NATIVE-SOURCE.zip') as z:
    assert z.testzip() is None
    names = [i.filename for i in z.infolist()]
    assert len(names) == len(set(names)) == 47 and set(names) == set(binding['paths'])
    for i in z.infolist():
        rel = Path(i.filename)
        assert not rel.is_absolute() and '..' not in rel.parts
        assert not i.is_dir() and not stat.S_ISLNK(i.external_attr >> 16)
        b = z.read(i)
        assert len(b) == i.file_size and S(b) == binding['paths'][i.filename]
        ziprows.append({'path': i.filename, 'bytes': len(b), 'sha256': S(b), 'mode': oct(i.external_attr >> 16)})
zipproof = W / 'T3122-ACTUAL25-NATIVE-ZIP-ARCHIVIST-READBACK.json'
assert not zipproof.exists()
zipproof.write_text(json.dumps({'status': 'PASS_EXACT47_MEMBERS_CRC_PATH_MODE_AND_ALL_SOURCE_BINDING_SHA256',
    'manifest_sha256': S(p.read_bytes()), 'zip_sha256': S((r/'UNCOMMITTED-NATIVE-SOURCE.zip').read_bytes()),
    'HEAD': binding['HEAD'], 'MERGE_HEAD': binding['MERGE_HEAD'], 'files': ziprows,
    'no_extract_or_apply_to_any_project': True}, indent=2) + '\n')
entries = m.author_manifest(r, p) + [(zipproof, zipproof.name, S(zipproof.read_bytes()))]
name = 'T3122-GENUINE25-NEUTRAL-ALIAS-NATIVE-PASS-UNCOMMITTED-FULLGATE-PENDING'
note = ('Exact18 author payloads+manifest and independent nestedZIP validation receipt. Source47-memberZIP allCRC/path/'
    'mode/SHA256 match SOURCE-BINDING inclincomingAbb/Ames provenance; no extraction/application. UNCOMMITTED on checked '
    'Sbd316 plus actualincomingAbb/Ames. Pinned genuine25masters/nativeweb PASS: onlylighthouse8021, prototypephysical/PBR/'
    'confidence/tone/normals exact under explicitconditionalneutralalias; all24defaultmasters/web BYTEEXACT. Firstscriptpath '
    'failure/duplicate-material bootstrap failure retained. Finalnative202+7population+57stabletail PASS clears3registered '
    'conflicts;105recipes fresh,341protected/955incomingnonfortrows/bothactualAbbworkbooks exact. Policy exactlyapproved '
    '3pointerchanges. T3124piazza NOTadopted. Requiredreaderfullcheck/percommitchecks/app/sourcecomparisons/finalPR/CI '
    'pending atclosure, no originalpictureacceptance, originals2373/2379/2388 OPEN/DIFFERS. Livegate/tree/cache excluded.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, entries, note)
assert row['bytes'] < 50000000
p = W / 'write_index.py';s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- The closed T3122 genuine25/native checkpoint preserves18 author payloads plus manifest and a separate '
    'archivist nested-ZIP readback. All47 source-ZIP members pass CRC, safe-path/type/mode and SOURCE-BINDING SHA256 '
    'checks; nothing is extracted or applied. Source remains **UNCOMMITTED**, on checked Sbd316 plus actual incoming '
    'Abb/Ames provenance. Final producer a0bcd0e genuinely exports all25 masters with pinned Blender4.5.3 and supported '
    'web derivatives: the lighthouse becomes8021 triangles with prototype physical/PBR/confidence/tone/normal faces '
    'preserved under the explicit conditional neutral-stone alias; **all24 default master and web files are byte exact**. '
    'First relative-script launch and duplicate-material bootstrap failures remain intact. Native202+7 population+'
    '57 stable-tail passes and clears the three registered conflicts; all25 recipes are fresh. The341 protected raw '
    'guards,955 incoming nonfort rows and both actual incoming Abb workbooks remain exact, with serialization restored '
    'only after XML/nonXML semantic proof, never old7a workbook replacement. Policy matches the approved whole predicted '
    'JSON with exactly three lighthouse pointer changes. T3124 piazza is **not adopted**. The required-reader fullcheck '
    'and committed-head checks, final app/source comparisons, latest bridge/dev integration, PR/CI and picture acceptance '
    'are still pending at this closure; original2373/2379/2388 stay OPEN/DIFFERS. Live gate, canonical tree and cache '
    'remain outside the selection.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
    'zip_members': 47, 'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
