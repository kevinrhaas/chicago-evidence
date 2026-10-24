from pathlib import Path
import hashlib,importlib.util,json,zipfile,stat,gzip
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-fort-integration/T-3105/closed-export-native-milestone');manifest=root/'RECOVERY.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='debadafbc0fdfd36dbabf7a9f68056afe8189a02c5b7365c21376d78e242240f'
author=json.loads(manifest.read_text());assert len(author['files'])==2
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
z=root/'export-native-checkpoint.zip';members=[]
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 seen=set()
 for info in f.infolist():
  name=info.filename;p=Path(name);assert name not in seen and not p.is_absolute() and '..' not in p.parts;seen.add(name)
  assert not any(s in p.parts for s in ['node_modules','__pycache__','.git']) and p.suffix!='.pyc'
  assert not stat.S_ISLNK(info.external_attr>>16)
  data=f.read(info);assert len(data)==info.file_size
  members.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'crc32':format(info.CRC,'08x')})
 assert len(members)==42 and sum(r['bytes'] for r in members)==3050559
 assert f.read('source-manifest-derived.patch.gz')==(root/'source-manifest-derived.patch.gz').read_bytes()
gzip.decompress((root/'source-manifest-derived.patch.gz').read_bytes())
ledger=WORK/'FORT-T3105-ZIP-READBACK.json';ledger.write_text(json.dumps({'status':'PASS_FULL42_ZIP_MEMBER_CRC_HASH_READBACK','author_recovery_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'exact_external_patch_matches_zip_member':True,'gzip_patch_full_decompression':'PASS','forbidden_paths_symlinks_caches':'NONE','members':members},indent=2)+'\n')
entries=mod.author_manifest(root,manifest);entries.append((ledger,'FORT-T3105-ZIP-READBACK.json',hashlib.sha256(ledger.read_bytes()).hexdigest()))
mod.archive('T3105-ACTUAL25-official-export-native-PASS-QA-GATES-PENDING',entries,'ExactclosedRECOVERY-boundZIP/patchgzip plus originalRECOVERY and explicitfull42memberZIPreadbackledger. Actualofficial25Blender4.5.3+real25derivatives4.5.0PASSwithpreservednpmcachewrapperfailure/resume;seven targets/18physical-material-confidence defaults exact,13defaultbyteexact/fiveUV-only/threelegitimatesizepassthroughs. Native744lib/fullstale/publish/scene/sourceuse/entrance/closingPASS,61tail2laps;26population/105recipes/210assets/Hogan4/policyguardsexactperfrozenreceipts. AppQA/newcomparisons/fullpreflight/PRPENDING,originalT3041/T2387openDIFFERS. Onlyclosedfolder/ZIPread,no changingfortcanonical/liveQAoutputsorimageacceptance.')
