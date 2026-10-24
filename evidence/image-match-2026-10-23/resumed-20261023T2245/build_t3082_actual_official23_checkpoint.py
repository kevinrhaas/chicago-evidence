from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-official23-closed-20261024T0109');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='b2797709e38d6e723c83ea9d46010ef426897116b8309cc6509ca067ec4bb8ff'
author=json.loads(manifest.read_text());assert len(author['files'])==72 and sum(r['bytes'] for r in author['files'])==5802030
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-ACTUAL-official23-masters-web-PASS-UNCOMMITTED-GATES-PENDING',mod.author_manifest(root,manifest),'Exact72 closed actual production files plus manifest:46GLBs/native manifests, frozen binding, orchestration/phase commands/logs/exit0 receipts, authored snapshot/diff and exact semantic review. Official23masters+web complete:22non-target master+web outputs byteexact3fa; target master+web each change only3roofRGB scalars to exact quarter, binary/other JSON exact. UNCOMMITTED at capture; downstream/native review/fullgates/PR pending. Original T2385 open/claimed/DIFFERS, flag research unadopted and rights unchanged. Heavy clear; no live tree/run outputs or held Glessner cache selected.')
