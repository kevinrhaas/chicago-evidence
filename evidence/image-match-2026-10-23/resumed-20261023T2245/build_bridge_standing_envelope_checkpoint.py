from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T-2375-standing-envelope-followup');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='c0809c3650382df650af7a2bb1b369ae60eea75008ed208fa68ebafe4612a3e6'
author=json.loads(manifest.read_text());rows=author if isinstance(author,list) else author['files'];assert len(rows)==16
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T2375-standing-horse-envelope-ANALYTIC-UNQUALIFIED-UNRUN',mod.author_manifest(root,manifest),'Exact16 closed standinghorse followup files plus manifest. Source-derived exactasset analytic3.056324m bound/APIcontrols/nativecontractPASS;numeric/independent/fullhappyasset/browser/GPU/nativeacceptanceUNQUALIFIED/UNRUN. Independentreviewofscopeassumptions/preexistingmalformedplacementbehavior futureseparate,originalimmutable. No canonical/heavy/adoption/imageacceptance or borrowedactualproof;livefuture reviewexcluded.')
