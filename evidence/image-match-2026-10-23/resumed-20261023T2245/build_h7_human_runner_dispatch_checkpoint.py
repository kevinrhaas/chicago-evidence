from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-H7-human-runner-dispatch-closed');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='0b134ca232cbbab88e8f6f7a4fb82fd8cf237f4569d1079fae01af2bd365db8e'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==8
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==50708
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-H7-human-job-Ubuntu24-ONLY-ONE-DISPATCH-NOT-PASS',mod.author_manifest(root,manifest),'Exact8 closed H7platformonly/dispatchpayloads plus manifest. Normalpushed18f7fa1cchangesONLYhumansjobUbuntu24,full4d66a68treeEXACTda65119/fixtures-measure-exporter-assertionsuntouched. ONEactualworkflowdispatchboundrun40081409169,frozenpacketNOTfinalPASS. Laterliveverify/installmetadataawaitsseparateclosedwholejobproof,noborrowingliveSUCCESS. No humanassetrefresh/fixureupdate/waiver/source4dchange;oldFAILpacketsretainedandnoenvironmentalbaselineclaim. No livecanonical/watchoutputselected.')
