from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,stat,subprocess
W=Path(__file__).resolve().parent;R=W/'remote-evidence';REL='evidence/image-match-2026-10-23/resumed-20261023T2245';S=lambda b:hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
assert not git('status','--porcelain')
head=git('rev-parse','HEAD').decode().strip();stages=git('ls-files','--stage');refs=git('show-ref');free0=os.statvfs('/workspace').f_bavail*os.statvfs('/workspace').f_frsize
ledger=json.loads((W/'STORAGE-ARCHIVE-OMISSIONS.json').read_text());old_names={x['name'] for x in ledger['files']};rows=json.loads((W/'ARCHIVES.json').read_text());proofs={}
for p in sorted((W/'publications').glob('*.json')):
 rec=json.loads(p.read_text())
 for proof in rec.get('remote_readback',[]):
  if proof['status']=='PASS':proofs[proof['path']]=(p,rec,proof)
selected=[]
for row in rows:
 src=Path(row['archive'])
 if not src.is_file():continue
 assert src.name not in old_names and not src.is_symlink()
 path=REL+'/archives/'+src.name;dst=R/path
 assert dst.is_file() and not dst.is_symlink()
 b=src.read_bytes();assert len(b)==row['bytes'] and S(b)==row['sha256'] and dst.read_bytes()==b
 indexed=git('ls-files','--stage','--',path).decode().split();blob=git('rev-parse',head+':'+path).decode().strip();assert indexed[:3]==['100644',blob,'0']
 assert git('cat-file','blob',blob)==b
 p,rec,proof=proofs[path];assert proof['git_blob']==blob and proof['sha256']==row['sha256'] and proof['bytes']==row['bytes']
 assert git('merge-base','--is-ancestor',rec['commit'],head)==b''
 selected.append({'name':src.name,'local_archive_path':str(src),'worktree_path':str(dst),'git_path':path,'sha256':row['sha256'],'bytes':row['bytes'],'git_blob':blob,'verified_committed_at':head,'local_mode':oct(stat.S_IMODE(src.stat().st_mode)),'working_mode':oct(stat.S_IMODE(dst.stat().st_mode)),'independent_remote_readback':{'published_commit':rec['commit'],'published_at':rec['published_at'],'receipt_file':str(p),'receipt_sha256':S(p.read_bytes()),**proof},'restore_url':'https://github.com/kevinrhaas/chicago-evidence/blob/'+head+'/'+path,'restoration':'git show HEAD:<git_path> > chosen-output; sparse working copy via removing exact exclusion and sparse-checkout reapply'})
assert len(selected)==83 and sum(x['bytes'] for x in selected)==170772813
receipt={'at_utc':datetime.now(timezone.utc).isoformat(),'status':'PREVERIFIED_PENDING_SPARSE_CACHE_EVICTION','authorization':'Parent expressly authorized reversible sparse dematerialization of old independently remote-verified publisher/archive cache duplicates, no source/Git object/ref/index-entry/archive-history loss.','head':head,'stage_entries_sha256':S(stages),'refs_sha256':S(refs),'status_before':'clean','free_workspace_before':free0,'files':selected,'bytes_per_duplicate_set':sum(x['bytes'] for x in selected),'sets':2,'no_unique_source_or_git_object_cleanup':True}
(W/'STORAGE-EXTENDED-SPARSE-CACHE-20261024.json').write_text(json.dumps(receipt,indent=2)+'\n')
ledger['files']+=selected;ledger.update({'status':'AUTHORIZED_EXACT175_REMOTE_VERIFIED_ARCHIVE_TAR_OMISSIONS','count':len(ledger['files']),'extended_at':receipt['at_utc'],'scope':'Original92 bounded sparse omissions remain;83 newly exact HEAD/index/local/cache/prior independent remote API readback-verified tar copies may also be absent. All175 committed Git objects/index entries/refs/metadata/raw source packets retained. Restore any payload using Git blob or immutable remote URL. Future new archives materialize normally.'})
(W/'STORAGE-ARCHIVE-OMISSIONS.json').write_text(json.dumps(ledger,indent=2)+'\n')
sparse=R/'.git/info/sparse-checkout';before=sparse.read_text();receipt['sparse_before_sha256']=S(before.encode());after=before+''.join('!/'+x['git_path']+'\n' for x in selected);sparse.write_text(after)
subprocess.run(['git','sparse-checkout','reapply'],cwd=R,check=True)
assert not git('status','--porcelain') and git('ls-files','--stage')==stages and git('show-ref')==refs and git('rev-parse','HEAD').decode().strip()==head
for x in selected:
 assert not Path(x['worktree_path']).exists()
 p=Path(x['local_archive_path']);assert S(p.read_bytes())==x['sha256'];p.unlink()
 assert S(git('cat-file','blob',x['git_blob']))==x['sha256']
assert not git('status','--porcelain') and git('ls-files','--stage')==stages and git('show-ref')==refs
receipt.update({'status':'SPARSE_CACHE_DEMATERIALIZED_GIT_OBJECTS_REFS_STAGE_ENTRIES_EXACT','sparse_after_sha256':S(after.encode()),'head_after':head,'status_after':'clean','free_workspace_after':os.statvfs('/workspace').f_bavail*os.statvfs('/workspace').f_frsize,'index_skip_worktree_bits_only_changed':True,'all_new83_committed_payloads_full_sha256_read_back_after_eviction':True})
(W/'STORAGE-EXTENDED-SPARSE-CACHE-20261024.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='files'},indent=2))
