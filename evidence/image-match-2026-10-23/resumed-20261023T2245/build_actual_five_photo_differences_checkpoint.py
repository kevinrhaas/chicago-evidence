from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-PR1260-five-photo-comparisons');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='e0297409776f23677f91f53adf831a2e0a8758e805998720a3ff7437221b04d5'
author=json.loads(manifest.read_text());assert len(author['files'])==77 and sum(r['bytes'] for r in author['files'])==7277609
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-PR1260-five-ACTUAL-native-photo-pairs-ALL-DIFFERS',mod.author_manifest(root,manifest),'Exact77 closed final photo-comparison files plus manifest. Exactly5actual normal native captures exit0;direct pair/rawPNG reviews ALLDIFFERS. Staged cameras unaccepted/original tickets open;fullsource/camera/master/group bindings,byte-original PNGs/source frames,producer-unreviewed and reviewed-differs records retained. First preservation exit1 from frozenhelper hardcoded/tmp vsrootTMPDIR retained;external os.tmpdir path-only correction reused schoolPNG,no recapture. Code copied,frozenoriginalfailure retained. Sourceclean,no canonical source/camera/data/assets/rights edits;renderer substrate/light/context limits explicit. No accepted matches, no extra live work selected.')
