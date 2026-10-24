from pathlib import Path
import hashlib,json,shutil
P=Path(__file__).resolve().parent;C=P/'CHECKPOINT-4-PORTABLE-EYE-INTAKE';assert not C.exists();C.mkdir()
for folder in ['CANONICAL-INTAKE-PROPOSAL','D454-FRESH-CLONE129']:
 shutil.copytree(P/folder,C/folder,symlinks=True)
for name in ['prepare_d454_fresh129.py','prepare_canonical_intake.py','audit_canonical_intake.py','freeze_checkpoint4.py']:
 shutil.copyfile(P/name,C/name)
for folder in ['PORTABLE-GENERATOR-ACTUAL-ONCE','PORTABLE-BOUNDARY-VALIDATION']:
 (C/folder).mkdir()
 for f in (P/folder).glob('*.json'):shutil.copyfile(f,C/folder/f.name)
(C/'README.md').write_text('Frozen unapplied T-2800 eye-UV-v1 canonical intake. Root alone integrates and publishes. Fresh actual d454 standard GLTFLoader/production SkeletonUtils clone/Mixer129 CPU passed with unchanged physical guards in2.7935seconds,166969344bytes RSS,20second/256MiB cap; all owned children closed. Portable generator reproduced exact d454 from existing canonical b479. Independent proposed boundary test passed five controls. All24 proposed file preimages/proposed hashes are inventoried. Runtime module changes selected SHA/byte identity only; existing contract changes selected filename only. Original b479 authored/runtime GLBs and historical receipts are NOT duplicated or modified. Proposal retains current1835 scene rows; merge concurrent1904 intake structurally. No Node contract/fullgate/browser/native/photo acceptance is claimed. Original source/native failures remain preserved. Root reviewed software quarter comparisons and approved only a limited eye improvement. Earlier checkpoints retain original actual V1-V4 trials and software evidence; this checkpoint does not replace their results.\n')
items=[]
for f in sorted(C.rglob('*')):
 if f.is_file():items.append({'path':str(f.relative_to(C)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(C/'MANIFEST.json').write_text(json.dumps(items,indent=2)+'\n')
print(json.dumps({'checkpoint':str(C),'files':len(items),'bytes':sum(x['bytes']for x in items),'manifest_sha256':hashlib.sha256((C/'MANIFEST.json').read_bytes()).hexdigest()},indent=2))
