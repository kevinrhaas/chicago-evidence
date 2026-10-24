from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T3041-native-readiness-20261024');manifest=root/'RECEIPTS.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='e19cb876e6c322a9796db6eef2625bcd2a72f149d88879559f2336088ab3e7dd'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==12
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3041-native-readiness-LIGHT-25CPU-NO-WRITERS-ADOPTION',mod.author_manifest(root,manifest),'Exact12 closed LIGHT readiness files plus verbatim RECEIPTS.json author manifest(e19cb8); filename verified,not PACKET-SHA256/MANIFEST. Committed6bf/dev8e source guards,25CPU/API checks and ordered native impact/readiness plan only. Front comparisons remain UNRUN,no new render/export/canonical write/native/heavy/adoption. Disposablepublished6bf/gitobject testtree and symlinks to earlier packet explicitly excluded; earlieractual trials remain historical,originalcoverageopen. No gate/readiness-to-merge/imageacceptance.')
