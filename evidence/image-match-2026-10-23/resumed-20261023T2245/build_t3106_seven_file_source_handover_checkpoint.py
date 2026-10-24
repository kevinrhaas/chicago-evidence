from pathlib import Path
import hashlib,importlib.util,json,zipfile,stat
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3106-source-handover-20261024');manifest=root/'MANIFEST.json';expected='f28c611ca32f59cc42cd2b17aa77244dd378e5c4d38cb5e98702e50763911842'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
rows=json.loads(manifest.read_text())['files'];assert len(rows)==10 and sum(r['bytes'] for r in rows)==6481723
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
author=json.loads((root/'SOURCE-MANIFEST.json').read_text());handover=json.loads((root/'HANDOVER.json').read_text());sources=author['tracked_and_needed_untracked_paths'];assert len(sources)==7 and author['untracked_needed']==[]
assert handover['stash_commit']=='677a03673c6800df1121a5e6ede7f5699fafbab3' and handover['git_status_after']=='clean'
assert {r['path']:r['sha256'] for r in sources}=={r['path']:r['sha256'] for r in handover['verified_source_paths']}
assert all(r['git_mode']=='100644' and r['posix_mode_preserved_in_zip']=='0o600' for r in handover['verified_source_paths'])
z=root/'source-bundle.zip';assert hashlib.sha256(z.read_bytes()).hexdigest()==handover['source_bundle_zip_sha256']=='b1a2cfe7704020a2a55b9f9c0a81c035e795d96e3d7abac5e5210ce476fb8d99';members=[]
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None and len(f.infolist())==27 and len(set(f.namelist()))==27
 for i in f.infolist():
  p=Path(i.filename);assert not p.is_absolute() and '..' not in p.parts and not any(s in p.parts for s in ['.git','node_modules','node-compile-cache','__pycache__']) and p.suffix!='.pyc';assert not stat.S_ISLNK(i.external_attr>>16)
  data=f.read(i);members.append({'path':i.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'zip_mode':oct(stat.S_IMODE(i.external_attr>>16))})
 for row in sources:
  data=f.read('source/'+row['path']);assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'];info=f.getinfo('source/'+row['path']);assert stat.S_IMODE(info.external_attr>>16)==int(row['posix_mode'],8)
  data=f.read('preimages/'+row['path']);assert len(data)==row['preimage']['bytes'] and hashlib.sha256(data).hexdigest()==row['preimage']['sha256'];assert row['preimage']['git_mode']=='100644'
 for row in author['native_proof']:
  data=f.read('native-proof/'+row['name']);assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 for name in ['SOURCE-MANIFEST.json','all-dirty-source.patch','status-before.z']:assert f.read(name)==(root/name).read_bytes()
assert hashlib.sha256((root/'all-dirty-source.patch').read_bytes()).hexdigest()==author['all_dirty_source_patch_sha256']
ledger=WORK/'FLORA-T3106-SOURCE-ZIP-READBACK.json';ledger.write_text(json.dumps({'status':'PASS_ALL27_ZIP_MEMBERS_7SOURCES_7PREIMAGES_10NATIVE_PROOFS','author_manifest_sha256':expected,'zip_sha256':handover['source_bundle_zip_sha256'],'stash_commit':handover['stash_commit'],'source_fs_modes':'0600 preserved in ZIP','declared_verified_git_modes':'100644, separate executable-bit representation; not POSIX0600 equality','all_source_hashes_match_handover':True,'members':members},indent=2)+'\n')
entries=mod.author_manifest(root,manifest);entries.append((ledger,'FLORA-T3106-SOURCE-ZIP-READBACK.json',hashlib.sha256(ledger.read_bytes()).hexdigest()))
mod.archive('T3106-Light-Full-exact7-source-ZIP-HANDOVER-stash677a-NOT-GATE',entries,'Exact10 closed flora sourcehandover payloads plus original manifest and full27member ZIPreadback ledger. All7dirtysource+7HEADpreimages+10nativeproofs and patch/metadata retained;ZIPb1a2cfe exact/hash/CRC/source0600 modes PASS. Namedstash677a03673c6800df1121a5e6ede7f5699fafbab3 verified seven hashes/Git100644 modes separately;initial incorrectPOSIX/Gitmode comparison and correctedchecks documented. CheckoutreportedcleanatDAonunchangedbranch,ignoredsite/outputs retainedOLDandneednormalnewpublish. Root hands clean/workspace/chicago toHogandata-onlynextwork;archivist readsNOlivecheckout/doesNOstashapply. SourcehandoverONLY,priorLight/Fullpackets unchanged,no newfullgate/PR/merge/release/imageclaim.')
