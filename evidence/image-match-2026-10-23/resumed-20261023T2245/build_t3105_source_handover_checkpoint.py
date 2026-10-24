from pathlib import Path
import hashlib,importlib.util,json,zipfile,stat,gzip
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/chicago-fort-integration/T-3105/closed-source-handover-20261024');manifest=root/'MANIFEST.json';expected='7001e621523dcbeffaad067e60da83c2e6e628debd09ac0f36da6eb6cdeaff0d'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
rows=json.loads(manifest.read_text())['files'];assert len(rows)==14 and sum(r['bytes'] for r in rows)==5103769
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
checkpoint=json.loads((root/'SOURCE-CHECKPOINT.json').read_text());assert len(checkpoint['source_files'])==59
z=root/'exact-dirty-source.zip';assert z.stat().st_size==checkpoint['source_zip_bytes']==4142471 and hashlib.sha256(z.read_bytes()).hexdigest()==checkpoint['source_zip_sha256']
source_rows={r['path']:r for r in checkpoint['source_files']};members=[]
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None and len(f.infolist())==59 and set(f.namelist())==set(source_rows)
 for i in f.infolist():
  p=Path(i.filename);assert not p.is_absolute() and '..' not in p.parts and not any(s in p.parts for s in ['.git','node_modules','node-compile-cache','__pycache__']) and p.suffix!='.pyc';assert not stat.S_ISLNK(i.external_attr>>16)
  row=source_rows[i.filename];data=f.read(i);assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'];assert stat.S_IMODE(i.external_attr>>16)==int(row['mode'],8)
  members.append({'path':i.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'mode':row['mode'],'public_base_sha256_declared':row.get('public_base_sha256')})
patch=root/'tracked-source.patch.gz';assert hashlib.sha256(patch.read_bytes()).hexdigest()==checkpoint['tracked_patch_gzip_sha256'];gzip.decompress(patch.read_bytes())
handover=Path('/tmp/chicago-fort-integration/T-3105/HANDOVER-RECEIPT.json');handover_sha='b6d73f646219a0cb3a565670240e103b41168833480cd69a51bf001b87733fa1';assert hashlib.sha256(handover.read_bytes()).hexdigest()==handover_sha
h=json.loads(handover.read_text());assert h['source_checkpoint_manifest_sha256']==expected and h['stash_commit']=='7338fd715a021ac3df9776cd208d83d88074d511' and h['git_status_porcelain']=='' and set(h['stash_exact_paths'])==set(source_rows)
ledger=WORK/'FORT-SOURCE-HANDOVER-ZIP-READBACK.json';ledger.write_text(json.dumps({'status':'PASS_ALL59_ZIP_BYTES_MODES_CRC_AND_BOUND_STASH_PATHS','author_manifest_sha256':expected,'source_zip_sha256':checkpoint['source_zip_sha256'],'patch_gzip_sha256':checkpoint['tracked_patch_gzip_sha256'],'patch_full_decompression':'PASS','public_base':checkpoint['base'],'public_base_preimages':'Author-declared in frozen SOURCE-CHECKPOINT; no borrowed live tree read.','stash_commit':h['stash_commit'],'separate_author_handover_sha256':handover_sha,'members':members},indent=2)+'\n')
entries=mod.author_manifest(root,manifest);entries.append((ledger,'FORT-SOURCE-HANDOVER-ZIP-READBACK.json',hashlib.sha256(ledger.read_bytes()).hexdigest()))
mod.archive('T3105-T3106-exact59-source-handover-ZIP-UNCOMMITTED-NOT-RELEASE-READY',entries,'Exact14 closed source-handover payloads plus original manifest and full59member ZIP byte/mode/CRC readback ledger. SourceZIP55 tracked modifications+4 new files, binary tracked gzip patch, publicDA base/preimage declarations/current hashes and compact official/native/photo/partialQA receipts retained. Exact stash7338fd715a021ac3df9776cd208d83d88074d511 binds all59paths; root may borrow clean tree. UNCOMMITTED/NOT_RELEASE_READY:16photosDIFFERS,7mobilePASS+firstFullFAIL,fullgate/PR/image acceptance pending/original21+9obligations open. Old fixture symlinks may follow borrowed tree, so execute no old bindings; exactZIP+publicDA recover assets/records. No canonical/live tree read.')
mod.archive('T3105-T3106-separate-author-SAFE-HANDOVER-RECEIPT',[(handover,'HANDOVER-RECEIPT.json',handover_sha)],'Exact frozen standalone author HANDOVER-RECEIPT, SHA256b6d73f646219a0cb3a565670240e103b41168833480cd69a51bf001b87733fa1. Records clean DA branch/stash7338fd/all59paths, previous stash and guarded restoration conditions. Apply exact stash commit only on original clean DA fort branch, never primary; do not pop/drop until59hashes match. Snapshot/history only,no stash application/source mutation by archivist; root borrowed tree is live and excluded. No source commit/fullgate/PR/image acceptance claim.')
