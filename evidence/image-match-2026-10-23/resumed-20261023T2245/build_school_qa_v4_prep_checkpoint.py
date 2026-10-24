from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-published-qa-v4-20261024');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='8ba6e0f8966e5b2273798708caea9d28477eb3ba6cb8357fadb111703bb7180c'
author=json.loads(manifest.read_text());assert len(author['files'])==9 and sum(r['bytes'] for r in author['files'])==38823
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-QA-v4-exact14-notice-guard-PREPARED-NO-BROWSER',mod.author_manifest(root,manifest),'Exact9 closed external QA v4 preparation files plus manifest. Root approved exact14 review-notice comparison; raw notices retained, unknown problems/errors still fail. Owner wording: review_required/touches_removal flags do not block released status or create a new consultation requirement (AGENTS130-146); failed-v3 legacy messages remain historical. Syntax/dry/mutation guards only at prep capture. Actual granted ten-case v4 retry runs separately and is excluded until closed; no photo grant or photo/image-match claim.')
