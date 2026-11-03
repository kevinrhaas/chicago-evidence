from pathlib import Path
import subprocess,json,hashlib,gzip,datetime,os
R=Path('/workspace/chicago-transport-current-20261103');Q=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence');D=Q/'transport-pr1649-memory-repairs-2026-11-03-2000Z';D.mkdir(parents=True,exist_ok=False);P=Q/'transport-pr1649-recovery-2026-11-03-1935Z'
def git(*a):return subprocess.check_output(['git','-C',str(R),*a],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),timeout=60)
def val(*a):return git(*a).decode().strip()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def gz(p,b):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(gzip.compress(b,mtime=0))
assert not git('ls-files','-u').strip() and not git('diff','--name-only').strip()
head=val('rev-parse','HEAD');incoming=val('rev-parse','MERGE_HEAD');tree=val('write-tree');sem=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()
assert head=='ae762df51dad3bd48e7d5307e0bda3cd0ce05e31' and incoming=='073a337e4ed89b362469246c1c5aa927c70975cd'
assert tree=='c6d84d690f862e7a90650e2fc4bd584783937169' and sem=='3ac3907f6e50ae317e23c239682450b328d290d863fcdccb689952b642a5aff6'
source=dict(HEAD=head,MERGE_HEAD=incoming,TREE=tree,APP=val('rev-parse',tree+':chicago/4d'),semantic_index_sha256=sem,pending_merge=True)
raw=git('ls-tree','-r','-z','--full-tree',tree);gz(D/'SOURCE-SNAPSHOT/TREE.ls-tree.z.gz',raw)
def parse(b):
 out=[]
 for ent in b.split(b'\0'):
  if not ent:continue
  meta,path=ent.split(b'\t',1);mode,typ,oid=meta.decode().split();out.append((mode,typ,oid,path.decode()))
 return out
priorraw=gzip.decompress((P/'SOURCE-SNAPSHOT/TREE.ls-tree.z.gz').read_bytes());priormeta=json.loads((P/'SOURCE-SNAPSHOT/CLOSED-SOURCE-RECOVERY-MAP.json').read_text());assert priormeta['source']['TREE']=='4cbd54078ab4a6dda0c19bbe15ba0a4d90aa7a40'
parents={x[2] for x in parse(priorraw) if x[1]=='blob'}
for p in [head,incoming]:parents|={x[2] for x in parse(git('ls-tree','-r','-z','--full-tree',p)) if x[1]=='blob'}
entries=parse(raw);novels=sorted({x[2] for x in entries if x[1]=='blob'}-parents);rows=[]
for oid in novels:
 b=git('cat-file','blob',oid);assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==oid
 p=D/('SOURCE-SNAPSHOT/novel-blobs/'+oid+'.blob.gz');gz(p,b)
 rows.append(dict(oid=oid,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),gzip_bytes=p.stat().st_size,paths=[x[3] for x in entries if x[2]==oid]))
old={x[3]:(x[0],x[2]) for x in parse(priorraw)};new={x[3]:(x[0],x[2]) for x in entries};changed=sorted(p for p in set(old)|set(new) if old.get(p)!=new.get(p))
assert len(changed)==5,changed
recipe=dict(status='IMMUTABLE_UNCOMMITTED_SOURCE_CAPTURE_NOT_GATE_QUALIFIED_NOT_MERGED',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=source,public_parents=[head,incoming],public_prior_packet=dict(commit='0b7d232b7c232cee0927ecb6a40dcc30d2cc6fe7',topic=str(P.relative_to(Q.parent)),TREE=priormeta['source']['TREE'],manifest_sha256=hashlib.sha256((P/'MANIFEST.json').read_bytes()).hexdigest()),entry_count=len(entries),source_tree_listing_sha256=hashlib.sha256(raw).hexdigest(),source_changes_from_prior=changed,blob_union_with_prior_count=len(parents),novel_blobs=rows,no_duplicate_prior_or_parent_asset_payloads=True,lossless_full_tree_reconstruction_with_public_prior_packet=True,app_commit_created=False,DEV_merge_performed=False,tickets_marked_done=False)
save(D/'SOURCE-SNAPSHOT/CLOSED-SOURCE-RECOVERY-MAP.json',recipe);save(Path('/workspace/.cloud-setup/transport-current-20261103/periodic-evidence-memory/CAPTURED-IMMUTABLE.json'),dict(packet=str(D),**recipe))
print(json.dumps(dict(packet=str(D),source=source,entries=len(entries),changed_paths=changed,novel_blob_count=len(rows),raw_novel_bytes=sum(r['bytes'] for r in rows),gzip_novel_bytes=sum(r['gzip_bytes'] for r in rows)),indent=2))
