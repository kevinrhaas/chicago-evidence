from pathlib import Path
import subprocess,json,hashlib,gzip,datetime,os
R=Path('/workspace/chicago-transport-current-20261103');D=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence/transport-pr1649-dev08-startup-repairs-2026-11-03-2200Z');D.mkdir(parents=True,exist_ok=False);T='676b7e0d6e566d3aaaa5b3cd0150b5a0637315d8';parents=['5439723317fbb6491e837911243f2f62fb35065b','08d3f3d7c85545013eaca18a9d256fe63a8e17e0']
def git(*a):return subprocess.check_output(['git','-C',str(R),*a],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),timeout=60)
def gz(p,b):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(gzip.compress(b,mtime=0))
def parse(b):
 out=[]
 for x in b.split(b'\0'):
  if x:
   meta,p=x.split(b'\t',1);mode,typ,oid=meta.decode().split();out.append((mode,typ,oid,p.decode()))
 return out
assert git('cat-file','-t',T).decode().strip()=='tree';app=git('rev-parse',T+':chicago/4d').decode().strip();assert app=='97b934f019593dedf974b0e607ada6e7551c36a8'
raw=git('ls-tree','-r','-z','--full-tree',T);entries=parse(raw);gz(D/'SOURCE-SNAPSHOT/TREE.ls-tree.z.gz',raw);union=set()
for p in parents:union|={x[2] for x in parse(git('ls-tree','-r','-z','--full-tree',p)) if x[1]=='blob'}
rows=[]
for oid in sorted({x[2] for x in entries if x[1]=='blob'}-union):
 b=git('cat-file','blob',oid);assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==oid;p=D/('SOURCE-SNAPSHOT/novel-blobs/'+oid+'.blob.gz');gz(p,b);rows.append(dict(oid=oid,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),gzip_bytes=p.stat().st_size,paths=[x[3] for x in entries if x[2]==oid]))
source=dict(HEAD=parents[0],MERGE_HEAD=parents[1],TREE=T,APP=app,semantic_index_sha256='f9c5b9ffe8743722e07c458f15a73cc11cbf4cca46016aafb9aa8e423319deaf',pending_merge=True)
x=dict(status='IMMUTABLE_GIT_TREE_CAPTURE_UNCOMMITTED_NOT_FULLGATED',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=source,public_parents=parents,entry_count=len(entries),source_tree_listing_sha256=hashlib.sha256(raw).hexdigest(),novel_blobs=rows,no_duplicate_parent_assets=True,no_live_worktree_or_index_used=True,fullgate_PASS=False,app_commit=False,DEV_merge=False,broad_ticket_done=False)
p=D/'SOURCE-SNAPSHOT/CLOSED-SOURCE-RECOVERY-MAP.json';p.write_text(json.dumps(x,indent=2)+'\n');Path('/workspace/.cloud-setup/transport-current-20261103/periodic-evidence-dev08/CAPTURED-IMMUTABLE.json').write_text(json.dumps(dict(packet=str(D),**x),indent=2)+'\n');print(json.dumps(dict(source=source,entries=len(entries),novel_blob_count=len(rows),novel_raw_bytes=sum(r['bytes'] for r in rows),novel_gzip_bytes=sum(r['gzip_bytes'] for r in rows)),indent=2))
