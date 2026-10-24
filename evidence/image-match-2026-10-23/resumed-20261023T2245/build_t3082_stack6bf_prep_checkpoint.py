from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-stack6bf-prep-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='d67582eb1b30bd14dee06fe4925b297cc245e98f06c39df4a02f80e73a88ffe9'
author=json.loads(manifest.read_text());assert len(author['files'])==23 and sum(r['bytes'] for r in author['files'])==6481899
for row in author['files']:
 p=root/row['path'];assert len(Path(row['path']).parts)==1;assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-stack6bf-LIGHT-actual-migration-GATES-PENDING',mod.author_manifest(root,manifest),'Exact23 closed top-level LIGHT files plus manifest,candidate fixture excluded. Previous whole state independently remote86136555 before clearing. v4 exact6bf committedPR1260base,no new merge/commit;4guarded edits/docs/entry reapplied and targetfixtures alreadyexact left untouched.23native recipes/docs exact twice before46genuine frame/23rows transfer;164incoming log asset Gitblob/SHA256 and82rows/webhashes preserved,unrelated/versionsexact. Raw targetdocs retained as full prefix then own suffix once. No heavy/native/fullgate/publish; originalT2385DIFFERS/open,rights unchanged,flagresearchunadopted. No live tree/held source/cache selected.')
