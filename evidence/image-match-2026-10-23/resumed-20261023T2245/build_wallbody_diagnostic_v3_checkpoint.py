from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-wall-body-diagnostic-proposal-v3');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='34ed756367aaa3d9ca5c4031b9c7e68cbed473cde2a0a0754dd338c6bc9b4b0f'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==28
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==3153476
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-body-diagnostic-v3-storedPosition-PROPOSAL-UNAPPLIED',mod.author_manifest(root,manifest),'Exact28 closed v3proposal files plus manifest. Onlynewv3difference packedpositionlocalp renamedstoredPosition toavoid nativeplacementaliasfalsepositive;helper/smokeexactv2,38CPUPASS. Focusedunchangedcheck_sidecar_contractPASS;oldv2fouraliaserrors/syntheticmissingfieldnegativeguardsstillFAIL. UNAPPLIEDbyproducer,noheavy/canonical/modelchanges. Parentactualpreflight03FAIL1/1060 separatelypreserved beforelatestdevreconciliation/adoption. No actualbrowserv3/nativefullgate or borrowingearlierbrowserproof;originalv1/v2frozen.')
