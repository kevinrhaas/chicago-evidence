from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-PR1260-published-qa');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='59ba331319268a4e1a46ffdd6be045e9c84dbb624663dfdbef0b4c390b843b67'
author=json.loads(manifest.read_text());assert len(author['files'])==11 and sum(r['bytes'] for r in author['files'])==1333635
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-PR1260-ACTUAL-published-QA-v3-FIRST-CASE-FAIL-STOPPED',mod.author_manifest(root,manifest),'Exact11 closed actual failed-v3 files plus manifest. Normal publish exit0/source clean. First mobile school case FAIL on14 intentional consultation review_required problem IDs; existing native smoke validates exactIDs, whereas v3 rejected nonempty problems. Zero page/HTTP/request/cleanup errors and remaining geometry/door/card assertions PASS; three screenshots viewed by producer. Nine other cases UNRUN, no photo pairs or image-match verdict. Failed original frozen exactly; any bounded harness correction/retry belongs to separate packet. Every heavy process closed; no live outputs selected.')
