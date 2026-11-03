from pathlib import Path
import os,subprocess,json,hashlib
R=Path('/workspace/chicago-bridge-increment-20261102');P=Path('/tmp/combined-changed-safe-objects');(P/'pack').mkdir(parents=True,exist_ok=True)
E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
paths=[p for p in subprocess.check_output(['git','diff','--name-only','-z','HEAD'],cwd=R,env=E).split(b'\0')if p]
oids=set()
for rel in paths:
 p=R/os.fsdecode(rel)
 if p.is_file():oids.add(subprocess.check_output(['git','hash-object','--',str(p)],cwd=R,env=E,text=True).strip())
text=''.join(s+'\n'for s in sorted(oids));q=subprocess.run(['git','cat-file','--batch-check=%(objectname) %(objecttype) %(objectsize)'],cwd=R,env=E,input=text,text=True,capture_output=True,check=True)
existing=[l.split()[0]for l in q.stdout.splitlines()if not l.endswith(' missing')]
idx=R/'.git/index';before=hashlib.sha256(idx.read_bytes()).hexdigest();work=dict(E,GIT_OBJECT_DIRECTORY=str(P),GIT_ALTERNATE_OBJECT_DIRECTORIES=str(R/'.git/objects'))
pack=P/'pack/temp.pack'
with pack.open('xb')as out:subprocess.run(['git','pack-objects','--stdout','--compression=1','--no-reuse-delta','--no-reuse-object','--window=0','--depth=0'],cwd=R,env=work,input=''.join(s+'\n'for s in existing).encode(),stdout=out,check=True)
ix=P/'pack/temp.idx';sha=subprocess.check_output(['git','index-pack','-o',str(ix),str(pack)],cwd=R,env=work,text=True).strip()
final=P/'pack'/f'pack-{sha}.pack';index=P/'pack'/f'pack-{sha}.idx';pack.rename(final);ix.rename(index)
local=R/'.git/objects/pack'
for p in [final,index]:(local/p.name).symlink_to(p)
(local/(final.stem+'.keep')).write_text('Changed-existing-object cache; private TMP backing.\n')
assert hashlib.sha256(idx.read_bytes()).hexdigest()==before
x={'status':'CHANGED_EXISTING_OBJECTS_CACHED_LOCALLY','paths':len(paths),'oids':len(oids),'existing_packed':len(existing),'new_missing_are_safe_to_write':len(oids)-len(existing),'pack':str(final),'bytes':final.stat().st_size,'real_index_unchanged':True}
Path('/workspace/wolf-safe-live-cache-20261102/CHANGED-READY.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x),flush=True)
