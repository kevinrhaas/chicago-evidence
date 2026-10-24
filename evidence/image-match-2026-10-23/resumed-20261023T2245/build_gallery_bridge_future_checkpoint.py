from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packets=[('/tmp/chicago-next-model/T3041-gallery-front-adoption-20261024','PACKET-SHA256.json','c39aa4c7486169a44a9d796d9a2ca69b00c80b2368a40c8bf01d73f0d75190c5',59,'T3041-firstfort-gallery-front-LIGHT-UNAPPLIED-FRONTS-UNRUN','Exact59 closed LIGHT files plus manifest. Narrow14path first-fort gallery/front and two chimney-removal proposal; CPU25default/18non-target/API/source parity only. Reuses prior actual16exports/9renders, no new actual heavy work. Five individual fronts UNRUN, full21plus9 original image coverage remains open. UNAPPLIED, no canonical adoption/new builds/image acceptance.'),('/tmp/chicago-next-model/T-2375-adoption-kwonly','MANIFEST.json','0d1641dcaa8736559d5d8a9b5362bea46142b78aceb0194b5ca32f56930d6631',56,'T2375-bridge-KWonly-LIGHT-raised-profile-BLOCKED','Exact56 closed LIGHT files plus manifest. Four bridge controls keyword-only,20legacy positional/sixdefault/candidate raw parity. Raised-profile adoption BLOCKED: native walker/router stay1.2m below boards. Prior board-only actual preview remains separate; board+crib/no-rise UNRENDERED. No canonical adoption/new heavy work/build/image acceptance; original ticket coverage open.')]
for directory,filename,expected,count,name,note in packets:
 root=Path(directory);manifest=root/filename;assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
 author=json.loads(manifest.read_text());rows=author if isinstance(author,list) else author['files'];assert len(rows)==count
 for row in rows:
  p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 mod.archive(name,mod.author_manifest(root,manifest),note)
