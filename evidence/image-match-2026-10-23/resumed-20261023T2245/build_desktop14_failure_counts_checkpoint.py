from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-desktop14-failure-baseline-counts');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='20105a3b4dd183e780be1dd432064318f45bf050c921ac7377d125c0b146d539'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==9
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==525930
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-desktop14-ACTUAL-FAIL-triangle-budget-NO-WAIVER',mod.author_manifest(root,manifest),'Exact9 closed read-only failure/baseline-count files plus manifest. Rawexact6bfdesktop14=139PASS1FAIL:1904spawn4600491 versus4600000budget. Historical10/16PASS is notmatchingbaseline,NOwaiver.1385tracked1904guards026-to6bf exact;2GlessnerGLBsuntracked,onlymanifestcontracts compared. Actualincoming8eKimballmaster/web114135to113414(-721triangles),exactfilehashbound;NOTnewcameraPASS. No new execution/heavy/cancel/merge/source/lap mutation or finalapproval.')
