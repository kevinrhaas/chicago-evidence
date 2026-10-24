from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T2375-standing-envelope-independent-review');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='a50d035fec0525bc975b3650d7a0f5948fc9fe148005c0afa25a41b0997d1c17'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==7
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==23072
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T2375-standing-envelope-INDEPENDENT-ANALYTIC-SCOPE-ONLY',mod.author_manifest(root,manifest),'Exact7 closed independent review files plus manifest. ApprovesONLYexactsource/schema-validrealnumber analyticrefusalscope,independentlysame3.056324m/all768normalizedLERP/source transforms. Gamma4096engineeringmargin NOTcertifiedGPU/worlderrorbound;browser/happyload/GPUUNRUN. Ownmalformedplacementcontrolsdemonstrateunchangedoriginalnative/v2/followup missingarraythrow/nonnumericsilentbehavior,no fix/expandedpolicy. Authorbridgepackets/canonicaluntouched;no fulladoption/nativepage/bake/fullgate/imageacceptance.')
