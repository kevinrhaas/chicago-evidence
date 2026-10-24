from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-next-model/T-2375-native-surface-profile-v2');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='3bac59322a4444058475aba876f64df1ccc025167f12a85ad767ac5596fafc1d'
author=json.loads(manifest.read_text());rows=author if isinstance(author,list) else author['files'];assert len(rows)==64
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T2375-surface-profile-v2-rigid-blocker-CLOSED-HORSE-UNQUALIFIED',mod.author_manifest(root,manifest),'Exact64 closed bridgev2proposal files plus manifest. Concrete rigidparked/legacyyard blocker addressed with rawtonecache rollback/cleanup,sixdefault/API parity and unchanged native sidecar-contract readerPASS+rednegatives. Standinghorse wholeenvelope UNQUALIFIED;actualnative/page/asset/browser/fullgate acceptance UNRUN. Originalv1 remainsBLOCKEDimmutable;separatelivehorsefollowupexcluded. No canonical adoption/newbake/fullgate/imageacceptance.')
