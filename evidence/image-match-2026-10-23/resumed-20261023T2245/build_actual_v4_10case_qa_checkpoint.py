from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-PR1260-published-qa-v4');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='c038df19332a3689c9939ed840129d6dc62179b76d5319e4557dd3e253d9ecf0'
author=json.loads(manifest.read_text());assert len(author['files'])==57 and sum(r['bytes'] for r in author['files'])==19560979
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-PR1260-ACTUAL-v4-ten-mobile-desktop-cases-PASS-NO-MATCH',mod.author_manifest(root,manifest),'Exact57 closed actual-v4 files plus manifest. All10 actual mobile/desktop cases PASS,batch exit0/source clean;all30PNG screenshots viewed by producer. Exact loaded compressed assets,doors/contact/budgets/credits/sources and14retained notices validated,zero unknown/page/network/cleanup errors. Owner no-release-block semantics explicit. Honest limitations:Wolf original-frame occlusion and stale Cobweb popup consultation wording; no flags/source changes. NOphoto_match/matches or original image acceptance. Separate granted native-fly supplement live and wholly excluded; no future supplement prep/run selected.')
