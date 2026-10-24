"""Strict, root-operated eye intake installer. Preparation never mutates app/Git.

Dry run checks all 24 original preimages, permits one pinned LIBERTIES merge,
and excludes the T-2800 changelog. Apply requires the exact reviewed manifest,
rechecks every byte before any write, backs up original files, and atomically
replaces only its explicit 23-file allowlist. No Git/index/network/subprocess use.
"""
from pathlib import Path
import argparse,copy,difflib,hashlib,json,os,stat,tempfile

HERE=Path(__file__).resolve().parent
PROPOSAL=HERE.parent/'CANONICAL-INTAKE-PROPOSAL'
INVENTORY_SHA='bdb545850c92837e36cc28be602f106f8e530121cd33c73d61352e4a4eae1c35'
LIB='docs/LIBERTIES.md'
SKIP='changelog.d/T-2800.json'
BASE=Path('/workspace/shared/ROOT-TRANSPORT-INTAKE-20261023-2315/CARRIAGE-VIEWPOINT-SOURCE-CHECKPOINT/files/chicago/4d/docs/LIBERTIES.md')
BASE_SHA='ec8d8efe519dee1aaf07249798127bfc1bfc6c89c268f57e65b189db10375ba4'
INCOMING_LIB_SHA='346fd35e1ea7b7e1e1711ef5fa13ff36f9fb3a8e38c0922ce0605bb1c3803ae4'
EXPECTED_APP=Path('/workspace/chicago-waistcoat/chicago/4d')
sha=lambda b:hashlib.sha256(b).hexdigest()

def need(ok,why):
 if not ok:raise ValueError(why)

def maybe_file(p):
 need(not p.is_symlink(),f'Symlink refused: {p}')
 if not p.exists():return None
 need(p.is_file(),f'Expected regular file: {p}')
 return p.read_bytes()

def paths(app,entry):
 rel=Path(entry['path']).relative_to('chicago/4d')
 need(not rel.is_absolute() and '..'not in rel.parts,'Unsafe inventory path')
 dest=app/rel;source=PROPOSAL/'new/chicago/4d'/rel
 need(dest.parent.resolve().is_relative_to(app),'Target parent escapes app')
 return str(rel),dest,source

def three_way(base,proposed,current):
 """Insert only the exact UV amendment into the unchanged horse liberty entry.

 This is intentionally bounded, not a generic fuzzy conflict resolver. Incoming
 Glessner changes are opaque bytes preserved verbatim. If the horse entry itself
 changed, this installer refuses rather than guessing a merge.
 """
 heading=b'### L-standing-horse-development-2800'
 need(base.count(heading)==1,'Original horse liberty must be unique')
 start=base.index(heading);end=base.find(b'\n### ',start+len(heading))
 need(end>start,'Expected following liberty boundary')
 entry=base[start:end]
 need(proposed.startswith(base[:end]),'Proposal altered historical prefix')
 need(proposed.endswith(base[end:]),'Proposal altered historical suffix')
 addition=proposed[end:len(proposed)-len(base[end:])]
 need(len(addition)==1367 and addition.startswith(b'\n\n**2026-10-23 eye-UV-v1 amendment (T-2800).**'),'Unexpected UV amendment payload')
 need(proposed==base[:end]+addition+base[end:],'Proposal must be one pure insertion')
 need(current.count(entry)==1,'Incoming horse entry changed or is ambiguous')
 need(b'**2026-10-23 eye-UV-v1 amendment (T-2800).**'not in current,'UV amendment already present')
 at=current.index(entry)+len(entry)
 merged=current[:at]+addition+current[at:]
 need(merged[:at]+merged[at+len(addition):]==current,'Incoming bytes were not preserved')
 return merged,addition,at

def build_plan(app):
 need(app==EXPECTED_APP and app.is_dir(),'Only the explicit root app is supported')
 inventory=(PROPOSAL/'CHANGED-FILES.json').read_bytes()
 need(sha(inventory)==INVENTORY_SHA,'Frozen inventory drift')
 entries=json.loads(inventory);need(len(entries)==24,'Expected all 24 preimages')
 base=BASE.read_bytes();need(sha(base)==BASE_SHA,'Root three-way base drift')
 rows=[];problems=[];blobs={};incoming=None;merged=None;addition=None
 for entry in entries:
  rel,dest,source=paths(app,entry)
  proposed=maybe_file(source);need(proposed is not None,'Proposal source missing: '+rel)
  need(sha(proposed)==entry['proposed_sha256'] and len(proposed)==entry['proposed_bytes'],'Proposal payload drift: '+rel)
  current=maybe_file(dest);current_sha=sha(current)if current is not None else None
  row={'path':entry['path'],'relative_path':rel,'action':'skip_group_changelog'if rel==SKIP else'install','original_preimage_sha256':entry['preimage_sha256'],'current_sha256':current_sha,'current_bytes':len(current)if current is not None else None,'source_sha256':sha(proposed),'source_bytes':len(proposed),'install_sha256':None,'install_bytes':None,'original_mode':stat.S_IMODE(dest.stat().st_mode)if current is not None else None}
  if rel==LIB:
   need(entry['preimage_sha256']==BASE_SHA and entry['preimage_bytes']==len(base),'LIBERTIES original preimage not exact root base')
   if current_sha!=INCOMING_LIB_SHA:problems.append({'path':entry['path'],'reason':'Unreviewed incoming LIBERTIES drift','expected_sha256':INCOMING_LIB_SHA,'actual_sha256':current_sha})
   else:
    incoming=current;merged,addition,at=three_way(base,proposed,current)
    row.update(action='install_exact_three_way_insertion',merge_base_sha256=BASE_SHA,incoming_bytes_preserved=True,amendment_bytes=len(addition),amendment_sha256=sha(addition),amendment_offset=at)
    blobs[rel]=merged;row['install_sha256']=sha(merged);row['install_bytes']=len(merged)
  else:
   if current_sha!=entry['preimage_sha256'] or (current is not None and len(current)!=entry['preimage_bytes']):
    problems.append({'path':entry['path'],'reason':'Preimage drift','expected_sha256':entry['preimage_sha256'],'actual_sha256':current_sha})
   if rel!=SKIP:
    blobs[rel]=proposed;row['install_sha256']=sha(proposed);row['install_bytes']=len(proposed)
  rows.append(row)
 need(len(rows)==24 and len({r['relative_path']for r in rows})==24,'Incomplete/duplicate inventory')
 report={'schema':'strict_root_eye_intake_plan_v1','status':'DRY_RUN_READY_NO_APP_WRITES'if not problems else'DRY_RUN_REFUSED_NO_APP_WRITES','app_root':str(app),'proposal_root':str(PROPOSAL),'installer_sha256':sha(Path(__file__).read_bytes()),'inventory_sha256':INVENTORY_SHA,'base_path':str(BASE),'base_sha256':BASE_SHA,'pinned_incoming_LIBERTIES_sha256':INCOMING_LIB_SHA,'all_24_preimages_compared':True,'install_count':sum(r['action']!='skip_group_changelog'for r in rows),'skipped_count':1,'skipped_path':'chicago/4d/'+SKIP,'Git_or_index_mutations':False,'app_written':False,'runtime_checks_performed':False,'problems':problems,'files':rows}
 return report,blobs,(base,incoming,merged,addition)

def require_external_out(out):
 out=out.resolve();need(out.is_relative_to(HERE),'Output must be in owned installer directory')
 need(not out.exists(),'Use a fresh output directory; no overwrite')
 return out

def dry_run(app,out):
 report,blobs,merge=build_plan(app);out=require_external_out(out);out.mkdir(parents=True)
 (out/'REVIEW-MANIFEST.json').write_text(json.dumps(report,indent=2)+'\n')
 base,incoming,merged,addition=merge
 if incoming is not None:
  (out/'LIBERTIES-MERGED.md').write_bytes(merged)
  (out/'UV-AMENDMENT.md').write_bytes(addition)
  for name,before,after,oldlabel,newlabel in [
   ('INCOMING-CHANGES.diff',base,incoming,'original root base','current incoming Glessner'),
   ('UV-ONLY-INSTALL.diff',incoming,merged,'current incoming Glessner','merged plus eye UV amendment')]:
   (out/name).write_text(''.join(difflib.unified_diff(before.decode().splitlines(True),after.decode().splitlines(True),fromfile=oldlabel,tofile=newlabel)))
 print(json.dumps({'status':report['status'],'review_manifest':str(out/'REVIEW-MANIFEST.json'),'review_manifest_sha256':sha((out/'REVIEW-MANIFEST.json').read_bytes()),'install_count':report['install_count'],'skip_count':report['skipped_count'],'problems':report['problems']},indent=2))
 return 0 if not report['problems']else 2

def write_atomic(path,data,mode):
 need(path.parent.is_dir(),'Existing target parent required')
 fd,temp=tempfile.mkstemp(prefix='.eye-intake-',dir=path.parent)
 try:
  with os.fdopen(fd,'wb')as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.chmod(temp,mode);os.replace(temp,path)
 finally:
  if os.path.exists(temp):os.unlink(temp)

def apply(app,manifest_path,review_sha,out):
 manifest_path=manifest_path.resolve();need(manifest_path.is_relative_to(HERE),'Review manifest must be owned')
 raw=manifest_path.read_bytes();need(sha(raw)==review_sha,'Reviewed manifest hash mismatch')
 reviewed=json.loads(raw);need(reviewed['status']=='DRY_RUN_READY_NO_APP_WRITES','Refused plan cannot be applied')
 fresh,blobs,merge=build_plan(app)
 need(not fresh['problems'] and fresh==reviewed,'Inputs/source/app changed since dry run; no writes')
 out=require_external_out(out);out.mkdir(parents=True)
 originals={};installed=[]
 for r in reviewed['files']:
  if r['action']=='skip_group_changelog':continue
  rel=r['relative_path'];old=maybe_file(app/rel);originals[rel]=old
  if old is not None:
   backup=out/'preimages'/rel;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(old)
 (out/'REVIEW-MANIFEST.json').write_bytes(raw)
 receipt={'schema':'strict_root_eye_intake_apply_v1','status':'APPLY_IN_PROGRESS','review_manifest_sha256':review_sha,'Git_or_index_mutations':False,'runtime_checks_performed':False,'installed':installed,'skipped_path':'chicago/4d/'+SKIP,'owned_rollback':None}
 try:
  # All preimages were checked before writes; each file is rechecked immediately.
  for r in reviewed['files']:
   if r['action']=='skip_group_changelog':continue
   rel=r['relative_path'];dest=app/rel;current=maybe_file(dest)
   need((sha(current)if current is not None else None)==r['current_sha256'],'Concurrent pre-write drift: '+rel)
   data=blobs[rel];need(sha(data)==r['install_sha256'],'Prepared output drift')
   write_atomic(dest,data,r['original_mode']if r['original_mode']is not None else 0o644)
   installed.append(rel)
   need(sha(dest.read_bytes())==r['install_sha256'],'Installed readback mismatch: '+rel)
  for r in reviewed['files']:
   current=maybe_file(app/r['relative_path'])
   expect=r['current_sha256']if r['action']=='skip_group_changelog'else r['install_sha256']
   need((sha(current)if current is not None else None)==expect,'Final readback mismatch: '+r['relative_path'])
  receipt['status']='APPLIED_23_FILES_GROUP_CHANGELOG_SKIPPED_NO_GIT_OR_RUNTIME_CHECKS'
 except BaseException as error:
  receipt.update(status='APPLY_FAILED_OWNED_ROLLBACK_ATTEMPTED',error=repr(error));rollback=[]
  # Never overwrite a concurrent change: rollback only exact bytes we installed.
  for rel in reversed(installed):
   dest=app/rel
   if dest.exists()and sha(dest.read_bytes())==sha(blobs[rel]):
    if originals[rel]is None:dest.unlink()
    else:write_atomic(dest,originals[rel],next(r['original_mode']for r in reviewed['files']if r['relative_path']==rel))
    rollback.append({'path':rel,'restored':True})
   else:rollback.append({'path':rel,'restored':False,'reason':'Concurrent drift preserved'})
  receipt['owned_rollback']=rollback
  raise
 finally:(out/'APPLY-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'status':receipt['status'],'receipt':str(out/'APPLY-RECEIPT.json'),'installed_count':len(installed),'runtime_checks_performed':False},indent=2))
 return 0

def main():
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--dry-run',action='store_true');g.add_argument('--apply',action='store_true')
 p.add_argument('--app-root',required=True,type=Path);p.add_argument('--out-dir',required=True,type=Path);p.add_argument('--review-manifest',type=Path);p.add_argument('--review-sha256')
 args=p.parse_args();app=args.app_root.resolve()
 if args.dry_run:
  need(args.review_manifest is None and args.review_sha256 is None,'Review binding only belongs to apply')
  return dry_run(app,args.out_dir)
 need(args.review_manifest is not None and args.review_sha256 is not None,'Apply requires exact reviewed manifest/hash')
 return apply(app,args.review_manifest,args.review_sha256,args.out_dir)
if __name__=='__main__':raise SystemExit(main())
