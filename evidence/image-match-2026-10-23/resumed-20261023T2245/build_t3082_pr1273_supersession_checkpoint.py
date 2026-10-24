from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-PR1273-supersession-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='3b537d9d3e151f79131a432b25f188dbd214beb57b54314247dbdd3a1d5abc53'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==18
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==369244
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-PR1273-CLOSED-UNMERGED-superseded-by1260-LAP-FREE',mod.author_manifest(root,manifest),'Exact18 closed final1273supersessionauditpayloads plus manifest. Primaryda65119actual9f95parentRESTproofBEFOREclose,1273bodynormalCLOSEDunmerged/branchretained/lapnormallyreleasedFREE. NormalnativeCLIsettleexit0/0changes,independentcurrentmain48453exactT3082REVIEW1260proofAFTERsettle. Ownsettleverificationdispatchremainedqueued,redundantdispatchnormallycancelled/terminalCANCELLEDreadback,nohostedPASSclaim. No source/manualticket/smokeedits;primary1260final18matrix/devmergePENDING/originalsDIFFERS,nofinalapproval/imageacceptance. No livecontentselected.')
