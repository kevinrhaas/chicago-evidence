from pathlib import Path
import contextlib, hashlib, importlib.util, io, json

W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/T3126-runtime/closed-current-app-QA-before-baseline-20261024T194013Z')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == 'd074151916bb1be9499da306e6fc7126951d4682cfc6bb910502ecb18560f65f'
rows = json.loads(p.read_text())['files']
assert len(rows) == 89 and sum(x['bytes'] for x in rows) == 17336370
for x in rows:
    rel = Path(x['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    assert not any(z in ['.git', '__pycache__', 'node_modules'] for z in rel.parts)
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == x['bytes'] and hashlib.sha256(b).hexdigest() == x['sha256']
name = 'T3126-CURRENT-TARGETED-APP-QA-PASS-FAR-BUDGET-FAIL-BASELINE-PENDING'
note = ('Exact89 closed payloads plus manifest; independent targeted mobile and closer/steeper desktop app QA PASS, '
        'Sources DOM credits, Images/Building Liberty, grounded 2.22m contacts and desktop visible signature range. '
        'Citation/native fixedpoint, workbook semantic normalization and exact workflow-only incoming305 FF preserved; '
        'all six recipes/master/web exact prior official stage1c113407. Source UNCOMMITTED. Retains first credit/poor framing, '
        'frozen api.flying alias and broad desktop FAR Fly 3494017 over unchanged3470000 failures. Closer view is NOT a '
        'budget fix. Completed candidate same-far stable-frame measurement included; paired old-geometry baseline, mobile '
        'visible-signature supplement and live control EXCLUDED/PENDING. No full smoke/gate/PR/CI/match acceptance, '
        'original2375 OPEN/DIFFERS; reconstructed flat-deck dimensions/camera-at-bound limits remain.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r, p), note)
assert row['bytes'] < 50000000
p = W / 'write_index.py'
s = p.read_text()
needle = '- Further producer/integration work is ongoing.'
assert s.count(needle) == 1
addition = ('- The Dearborn T3126 closed targeted app-QA checkpoint preserves 89 payloads plus manifest. Independent '
            'mobile and closer/steeper desktop checks pass for the normal/ByGrade model views, Images and Building Liberty, '
            'actual Sources DOM credits and grounded 2.22m contacts; desktop visible-signature range is also retained. '
            'Both targeted runs have zero page/network/unexpected-loader errors. Citation-reader/native fixedpoint, '
            'workbook semantic normalization and the exact incoming workflow-only 305 FF are preserved, with all six '
            'recipes/master/web hashes unchanged from the genuine official stage. Source remains UNCOMMITTED. '
            '**The broad desktop FAR Fly view still fails: 3,494,017 triangles exceed the unchanged 3,470,000 cap.** '
            'The closer passing view is visual evidence, not a repair or proof that all views meet budgets. Initial '
            'credit/poor framing and frozen api.flying alias failures remain intact; later checks use live walker/HUD/intent '
            'readings. The completed candidate same-far measurement repeats the excess across three stable frames, with '
            'actual HTTP hash and decoded 13,678-triangle target. The paired old-geometry baseline and mobile visible-signature '
            'supplement are still pending and excluded, as is the live control. No full smoke, full gate, PR, CI or picture-match '
            'acceptance is claimed. Original T2375 remains OPEN/DIFFERS, including its camera-at-bound and reconstructed '
            'flat-deck limits.\n')
p.write_text(s.replace(needle, addition + needle))
print(json.dumps({'archive': name, 'bytes': row['bytes'], 'readback': 'PASS',
                  'inventory_count': len(json.loads((W / 'ARCHIVES.json').read_text()))}))
