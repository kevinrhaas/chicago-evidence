from pathlib import Path
import hashlib,json,subprocess,datetime,base64
w=Path('/tmp/chicago-resumed-evidence-20261023T2245');repo=w/'remote-evidence';hold=Path('/workspace/chicago-archive-emergency-move-20261024')
anchor='1ee6dc2f96700553ea66f5b73dd84daa3f8160bf';rel='evidence/image-match-2026-10-23/resumed-20261023T2245/archives/'
def git(args):return subprocess.check_output(['git',*args],cwd=repo)
assert git(['status','--porcelain'])==b''
head=git(['rev-parse','HEAD']).decode().strip();assert head==anchor
rows=json.loads((w/'ARCHIVES.json').read_text())[:92];assert len(rows)==92
readbacks={}
for p in sorted((w/'publications').glob('*.json')):
 d=json.loads(p.read_text())
 for r in d.get('remote_readback',[]):
  if r.get('status')=='PASS' and r['path'].endswith('.tar.gz'):
   readbacks[(r['path'],r['sha256'])]={'published_commit':d['commit'],'published_at':d['published_at'],'receipt_file':str(p),'receipt_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),**r}
fresh={'commit':anchor,'published_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_readback':[]}
for r in rows:
 path=rel+Path(r['archive']).name
 if (path,r['sha256']) in readbacks:continue
 blob=git(['rev-parse',head+':'+path]).decode().strip()
 reply=json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago-evidence/git/blobs/'+blob]))
 assert reply['encoding']=='base64'
 data=base64.b64decode(reply['content']);assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
 fresh['remote_readback'].append({'path':path,'git_blob':blob,'bytes':len(data),'sha256':r['sha256'],'status':'PASS'})
if fresh['remote_readback']:
 freshpath=hold/'FRESH-INDEPENDENT-READBACKS.json';freshpath.write_text(json.dumps(fresh,indent=2)+'\n')
 for r in fresh['remote_readback']:
  readbacks[(r['path'],r['sha256'])]={'published_commit':anchor,'published_at':fresh['published_at'],'receipt_file':str(freshpath),'receipt_sha256':hashlib.sha256(freshpath.read_bytes()).hexdigest(),**r}
files=[]
for r in rows:
 name=Path(r['archive']).name;path=rel+name;p=hold/name;assert p.is_file() and not p.is_symlink()
 assert p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 rb=readbacks[(path,r['sha256'])];assert rb['bytes']==r['bytes']
 blob=git(['rev-parse',head+':'+path]).decode().strip();assert blob==rb['git_blob']
 stage=git(['ls-files','--stage','--',path]).decode().strip().split();assert stage[:3]==['100644',blob,'0']
 data=git(['cat-file','blob',blob]);assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
 files.append({'name':name,'local_archive_path':str(w/'archives'/name),'worktree_path':str(repo/path),'git_path':path,'sha256':r['sha256'],'bytes':r['bytes'],'git_blob':blob,'verified_committed_at':head,'reversible_payload_copy':str(p),'independent_remote_readback':rb,'restore_url':'https://github.com/kevinrhaas/chicago-evidence/blob/'+rb['published_commit']+'/'+path})
ledger={'status':'AUTHORIZED_EXACT92_REMOTE_VERIFIED_ARCHIVE_TAR_OMISSIONS','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'anchor_commit':anchor,'repository':'kevinrhaas/chicago-evidence','observed_remote_main':git(['ls-remote','origin','refs/heads/main']).decode().split()[0],'count':92,'bytes_per_duplicate_set':sum(r['bytes'] for r in files),'scope':'Only redundant exact tar payloads may be absent; all metadata/current queue/raw source packets retained. Every historical independent GitHub readback PASS is hash-bound here. Publisher must verify committed/index blob and full SHA256 before accepting an absent payload. Reversible emergency copies remain in workspace.','files':files}
for p in [w/'STORAGE-ARCHIVE-OMISSIONS.json',hold/'REMOTE-VERIFIED-OMISSIONS.json']:
 p.write_text(json.dumps(ledger,indent=2)+'\n')
print(json.dumps({'ledger':str(w/'STORAGE-ARCHIVE-OMISSIONS.json'),'count':len(files),'bytes_per_duplicate_set':ledger['bytes_per_duplicate_set'],'historical_remote_readbacks_all_pass':True,'current_commit_index_blob_fullhash_all_pass':True}))
