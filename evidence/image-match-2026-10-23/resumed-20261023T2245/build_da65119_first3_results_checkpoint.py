from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-head-da65119-watch/closed-first3-actual-results');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='56a8a05e0dd758983cf813a08be3188590e379c058427f1153cc565010ee5259'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==11
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==210402
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-consolidatedda65119-first3of18-ACTUAL-PASS-PARTIAL',mod.author_manifest(root,manifest),'Exact11 closed actualnewconsolidatedheadfirst3resultpayloads plus manifest. Desktop15/mobile15each34PASS0FAIL,mobile8=21PASS0FAIL,exactda65119checkout/stage/viewportandzeropageerrors. ONLY3of18atcapture,15pending/hostedgate-movingstillrunning. OldH4/H5NEVERinherited,nofullcoverage/mergeapproval/imageacceptance,nodispatch/mutationbyarchivist/livewatchoutputselection.')
