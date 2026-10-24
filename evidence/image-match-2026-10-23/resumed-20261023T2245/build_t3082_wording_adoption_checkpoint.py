from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-review-notes-adoption-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='404bb160f08801f2c778af01aeb14d731c6a02adc4480fc651b9b1af6b8a9ac8'
author=json.loads(manifest.read_text());assert len(author['files'])==26 and sum(r['bytes'] for r in author['files'])==1524753
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert 'proposal-verification-copy' not in p.parts;assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-approved-v2-wording-adoption-LIGHT-NATIVE-GATES-PENDING',mod.author_manifest(root,manifest),'Exact26 closed files plus manifest. Actual adoption of approvedv2 three sourcefiles aftermanifest/all21/preimage guards;syntax/copied extracted reason/controlflow/filter/future14-refusal checksPASS. Originalproposal untouched. OwnSTATUS/ROADMAP suffixes,entry/PRdraft and normal ticketbodysyncb752333 recorded;23recipes/46frame outputs/164log assets/82rows exact. Disposable proposal-verification-copy excluded. No heavy/native/publish/fullgate/codecommit;originalT2385open/DIFFERS,rights unchanged,flagresearchunadopted. Dated claim ours/live2.612h,normal renewal unsupported,no force/timestamp edits;futureclaims must reread. No current readiness/image acceptance.')
