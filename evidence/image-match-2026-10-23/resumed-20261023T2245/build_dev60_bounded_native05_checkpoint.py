from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-dev60-bounded-native05-closed');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='ac8401024f12bf0e90526fa69cf6bba2516e777d02e5235b4c8563041ea51eda'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==19
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-dev60-bounded-native05-PASS-NOT-FULLGATE-BUDGET-UNRUN',mod.author_manifest(root,manifest),'Exact19 closed latest60boundednative files plus manifest. Normalmerge60atoppublic4606,only3LIB/sourceuseconflicts,rawincomingprefixpreserved/ownsuffixexact. Wheeler1904placement/footprint/stories/dates unchanged;onlymanifestwriters142/146/150 needed.9native/check/publish/datasetallstale phasesPASS,26populationmodels/105records/210assets/recipes exact;wholepatchsaved. NOTfullgate05/smoke,actuallatest60budgetUNRUN,Glessner4mbaselineunchanged/2mcandidateUNAPPLIED. SeparateexclusivebudgetA/Bfuturework/livefolderexcluded;no currentreadiness/imageacceptance.')
