from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packets=[('/workspace/T3082-final-drift-audit-ef41-20261024','CLOSED-MANIFEST.json','32279afd84739610ef584edf9084f68780f7ad4d93544101b9ee87916ec128cf',6,31697,'T3082-pinned85-toef41-dev38-LIGHT-drift-NOT-FRESHNESS-PASS','Exact6 closed LIGHT pinned-object audit payloads plus original manifest.123paths audit85a-toef41/38, noJS delta except changelog;105records/210assets and26population parity. Four changed1904assets need fresh actual browser validation. This is source/object parity only, NOT current freshness/browser/gatePASS. No heavy/browser/bind/source writes; parent owns future actual run after gate. No live mutable tree/watch output selected.'),('/workspace/PR1260-dev38-1904-probe-v1-prepared-20261024','PREPARED-MANIFEST.json','f8423ea50f45ddec579be29457c98f2ed31821fdbd1230ba93c0fbb742f6a5e6',6,25009,'PR1260-dev38-1904-probe-v1-PREPARED-UNRUN-NO-BIND','Exact6 closed prepared probe files plus original manifest. PREPARED_UNRUN helper/bind-controller/config,node-python syntax and dry only, no actualbrowser/bind or currentheadPASS. Desktop budget fails closed before cards;streamedGLBhash avoids CDPlargebody ambiguity. Root owns future run aftergate. Generated__pycache__ excluded by original selection, no hidden future outputs/canonical source read, old failures/actualDAresults unchanged.')]
for directory,filename,expected,count,total,name,note in packets:
 root=Path(directory);manifest=root/filename;assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
 author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==count
 if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
 assert sum(r['bytes'] for r in rows)==total
 for row in rows:
  p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 mod.archive(name,mod.author_manifest(root,manifest),note)
