from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-review-wording-followup-v2');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='04955ae604696ff3e5f0ed02b04c9216210725dc9622d4e56c2f2d8734dfa68e'
author=json.loads(manifest.read_text());assert len(author['files'])==21 and sum(r['bytes'] for r in author['files'])==3001217
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-review-notice-wording-v2-UNAPPLIED-followup',mod.author_manifest(root,manifest),'Exact21 closed files plus manifest. UNAPPLIED3path wording-only followup on captured6bfHEAD, intended for coordinated T3082 followup rather thanPR1260 mutation. Corrects stale popup consultation/release diagnostics under existing ownerAGENTS ruling while preserving flags/full reasons/confidence/gates. README binds authority/source/tests and futureexact14 notices; currentv4 untouched. No canonical/liveQA/native/browser/fullgate run; previousv1 frozen, v2 selected future adoption. No current adoption/readiness/image-match claim.')
