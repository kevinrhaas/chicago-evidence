from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T2375-dense-deck-independent-review');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='8e0fb3a573ed78a012aaea67964d7b006f60576ff724326b984f3401259e6efe'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==24
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==2040130
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T2375-dense-deck-INDEPENDENT-nominal-planktop-ONLY',mod.author_manifest(root,manifest),'Exact24 closed independent review files plus manifest.333151rawtrianglegridpoints+296faceaffinesegmentcertificate actual8db45rawexact;shared/walker/exactrouter332969pointsPASS. Actualresolved293SAWNboards8mmgaps(not22mmpuncheon);nohitgapsremainNULL,55mmproudthresholdcounterexampleexplicit,rails/gallowsneverfloor. ApprovesONLYnominalplanktopcoherence,noactualbrowser/Blender/nativewriter/fullgate/image/contact/GPUacceptance. Nextversionprose suggestionseparate;author/canonicalunchanged,no livecontentselected.')
