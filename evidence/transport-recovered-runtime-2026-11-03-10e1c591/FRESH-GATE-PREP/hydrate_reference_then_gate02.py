from pathlib import Path
import json,hashlib,subprocess,os,sys,importlib.util
sys.dont_write_bytecode=True
P=Path(__file__).parent;C=json.loads((P/'ROOT-ACTUAL-GO.json').read_text());R=Path(C['repo']);D=Path('/dev/shm/ROOT-RECOVERED-5918-COMMITTED-REFERENCE-HYDRATION-20261103');D.mkdir();env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='0',PYTHONDONTWRITEBYTECODE='1');env.pop('CHICAGO_TICKETS_DIR',None)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();read=lambda p:json.loads(Path(p).read_text());save=lambda p,x:Path(p).write_text(json.dumps(x,indent=2)+'\n')
def git(*args,input=None):return subprocess.check_output(['git','-c','gc.auto=0','-c','maintenance.auto=false','-C',str(R),*args],env=env,input=input,timeout=120)
def source():
 x=C['source'];assert git('rev-parse','HEAD').decode().strip()==x['HEAD'] and git('rev-parse','MERGE_HEAD').decode().strip()==x['MERGE_HEAD'];assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==x['semantic_index_sha256'];assert git('write-tree').decode().strip()==x['TREE'];assert not git('diff','--name-only').strip() and not git('ls-files','-u').strip();assert sha('/workspace/chicago/.git/index')==C['protected_parent_index_sha256'];return x
initial=source();spec=importlib.util.spec_from_file_location('guard',C['resource_guard']);guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard);r0=guard.snapshot();assert guard.check(r0)['accepted'];save(D/'SOURCE-BEFORE.json',initial)
p=D/'native-sparse-add-reference';cmd=['git','-c','gc.auto=0','-c','maintenance.auto=false','sparse-checkout','add','--no-cone','/chicago/reference/']
with Path(str(p)+'.supervisor.stdout').open('xb')as log:q=subprocess.run([sys.executable,C['supervisor'],'--prefix',str(p),'--cwd',str(R),'--timeout','180','--',*cmd],env=env,stdout=log,stderr=subprocess.STDOUT)
r=read(str(p)+'.result.json');cl=read(str(p)+'.cleanup.json');pair=guard.pair(r0,guard.snapshot());save(D/'NATIVE-HYDRATION-RESOURCES.json',pair);assert q.returncode==r['returncode']==0 and not r['timed_out'] and cl['cleanup_complete'] and not cl['remaining_owned_children'] and pair['accepted'];source()
rows=[];normal=[]
for rec in git('ls-files','--stage','-z','--','chicago/reference/').split(b'\0'):
 if not rec:continue
 meta,path=rec.split(b'\t',1);mode,blob,stage=meta.decode().split();path=path.decode();assert stage=='0' and '\n'not in path;f=R/path;assert f.exists()or f.is_symlink(),path
 if mode=='120000':
  data=os.readlink(f).encode();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
 else:assert f.is_file() and not f.is_symlink();normal.append((path,blob))
 rows.append(dict(path=path,mode=mode,git_blob=blob,bytes=f.lstat().st_size))
values=git('hash-object','--stdin-paths',input=('\n'.join(p for p,b in normal)+'\n').encode()).decode().splitlines();assert len(values)==len(normal) and all(a==b for a,(p,b)in zip(values,normal));source();save(D/'VERIFIED-COMMITTED-REFERENCE-MANIFEST.json',dict(files=rows,file_count=len(rows),bytes=sum(x['bytes']for x in rows),all_git_blob_hashes_exact=True,source=initial))
save(D/'CLOSED.json',dict(status='COMMITTED_REFERENCE_DEPENDENCIES_HYDRATED_ALL_BLOBS_EXACT_SOURCE_UNCHANGED',source_before=initial,source_after=source(),result=r,cleanup=cl,resources=pair,file_count=len(rows),total_file_bytes=sum(x['bytes']for x in rows),manifest_sha256=sha(D/'VERIFIED-COMMITTED-REFERENCE-MANIFEST.json'),source_or_research_regeneration=False));print(json.dumps(dict(status='HYDRATION_PASS',files=len(rows),bytes=sum(x['bytes']for x in rows))),flush=True)
# The existing reviewed controller/code is unchanged. Only output differs from failed01.
C['gate_output']='/dev/shm/ROOT-RECOVERED-5918-FRESH-ALL4-ACTUAL-20261103-02';go=P/'ROOT-ACTUAL-GO-02.json';assert not go.exists();save(go,C)
assert sha(P/'run_checked_delivery.py')==C['controller_sha256'];os.execv(sys.executable,[sys.executable,'-u',str(P/'run_checked_delivery.py'),'gate','--root-go',str(go)])
