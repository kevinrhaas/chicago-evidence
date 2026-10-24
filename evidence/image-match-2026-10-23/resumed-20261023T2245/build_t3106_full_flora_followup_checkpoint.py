from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3106-full-flora-prerequisite-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='79166cf32427414e297e03a858bc5ff07c966ea1348d1d94c39f5f8ca77cf3c0'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==35
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==16193308
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3106-Full1812-uniform-keep0525-ACTUAL-one-desktop-PASS-ROOT-REVIEW',mod.author_manifest(root,manifest),'Exact35 closed Full followup payloads plus original manifest, including exact prior5doc/source snapshots. Runtime increment only1812Full existing uniformkeep0.700to0.525; caps/Light/Balanced/other scenes/guards/72statedplantings unchanged. One actual desktopFullPASS3738of4700trees/north1117.747/zero flora errors/all72plantings exact. Original canonicalFullFAIL preserved; no unrun cleanDAFull claim. Root runtimeincrement/newlibertyappend review pending at capture, no codecommit/push/PR/fullgate/merge/image acceptance. Separate from prior Light397dc/baseline2d0f, heavyCLEAR,no livecanonical/read.')
