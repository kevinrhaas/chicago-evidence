from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-future-public-head-plan-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='b4a02973185c7f4f02678672f9de7cae01b3eec24cd9a170ee36c49277851716'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==13
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==30726
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-future-public-head-migration-PLAN-ONLY-TARGET-NULL',mod.author_manifest(root,manifest),'Exact13 closed futuremigration plan files plus manifest. TargetdeliberatelyNULLuntilrootpublichead,no mutable-rootread/composition/sourcewrite/claim/merge/heavy. Approved3wordingpatchcomponents,4roof/ownsuffixguards;futureinversewording-byteproof preserves incomingdiagnosticv3/fullbbox/body/38controls,82logs/23genuineoutputs/fullhistory. Oldnative5globaloutputs backupNOTtransplant. Currentwholefc80backup separatelycaptured,remoteproofrequiredbeforeclearing. PLANONLY,nofutureheadadoption/gate/browser/imageacceptance.')
