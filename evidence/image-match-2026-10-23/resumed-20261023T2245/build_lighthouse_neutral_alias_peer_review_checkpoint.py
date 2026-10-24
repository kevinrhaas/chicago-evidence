from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/tmp/T3122-neutral-stone-alias-peer-review')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == 'fe215bf865fd25dd640d84cd33ca364e3b779d43ff573f00e82d9cf5e2678fc2'
rows = json.loads(p.read_text())['files']
assert len(rows) == 2
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
name = 'T3122-NEUTRAL-STONE-ALIAS-CONDITIONAL-PREIMPLEMENTATION-PEER-REVIEW'
note = ('Exact two closed review payloads plus original manifest. Readonly pure parameter/PBR descriptor review: '
        'current bare-stone base wall equals tone1 stone/.93 descriptor, so conditional resolved-equality alias approved. '
        'Valid whitewash/white controls differ in color/.90/.60 and disprove unconditional alias; named neutral fallback '
        'must remain for differing descriptors. PREIMPLEMENTATION only, no final patch/raw geometry/Blender/export/web/'
        'browser/native result, and no generator writes or owner heavy-lane change.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
p = W / 'write_index.py'
s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- The lighthouse neutral-stone material-alias peer review is preserved as a **preimplementation, conditional '
            'approval only**. Actual pure parameter/PBR descriptors show the current bare-stone base wall exactly matches '
            'the stone/.93 tone1 duplicate. Aliasing those face assignments is approved only when resolved color and '
            'roughness are equal. Valid whitewash and white controls differ in color and .90/.60 roughness: they are '
            'counterexamples to an unconditional alias, so differing descriptors require the named neutral fallback. '
            'The two closed review files and manifest contain no final-patch, raw geometry, Blender, export, web, browser '
            'or native proof; the owner retains its exclusive writer/heavy lane.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
                  'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
