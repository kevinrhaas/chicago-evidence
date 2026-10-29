import os,json,hashlib,subprocess,shutil,time
from pathlib import Path
R=Path('/tmp/chicago-transport-resume-20261029');A=R/'chicago/4d';M=R/'site/4d';O=Path(__file__).resolve().parent
HEAD='a3971c9a638e03216945fc52ce57d7453596187e';TREE='e873ea8531ab1a8f8bb74434976ace6234c3d6e6';APP='8906d01e088f79614fb8020a119ec20e6aa6cf49'
F=Path('/workspace/.cloud-setup/logs/transport-recovery/T1789-SIGNOFF-REPORT-REPAIR-20261029/FROZEN-19-SOURCE-BINDING.json');B=json.loads(F.read_text())
def git(*a):return subprocess.check_output(['git',*a],cwd=R).decode().strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,j):(O/n).write_text(json.dumps(j,indent=2)+'\n')
def guard():
 assert git('rev-parse','HEAD')==HEAD and git('rev-parse','HEAD^{tree}')==TREE and git('write-tree')==TREE
 assert not git('status','--porcelain') and not git('ls-files','-u')
 for row in B['all_staged_paths']:assert sha(R/row['path'])==row['sha256']
 assert shutil.disk_usage('/tmp').free>=256*1024**2
S=Path('/tmp/p29s');assert S.is_dir();env=dict(os.environ,TMPDIR=str(S));env.pop('GIT_NO_LAZY_FETCH',None)
assert shutil.disk_usage('/tmp').free>=512*1024**2
guard();write('BEFORE.json',dict(HEAD=HEAD,TREE=TREE,APP=APP,source19_binding_sha256=sha(F),tmp_free=shutil.disk_usage('/tmp').free))
rows=[]
for label,args in [('NATIVE-FINAL-PUBLISH',['bash','tools/publish.sh']),('NATIVE-MIRROR-CHECK',['node','tools/check_published.mjs']),('NATIVE-YEARPACKS-CHECK',['node','tools/write_year_packs.mjs','--check','../../site/4d'])]:
 guard();start=time.monotonic();print('START '+label,flush=True)
 with(O/(label+'.log')).open('wb',buffering=0)as out:q=subprocess.run(args,cwd=A,env=env,stdout=out,stderr=subprocess.STDOUT)
 row=dict(label=label,command=args,returncode=q.returncode,seconds=time.monotonic()-start);rows.append(row);write('COMMANDS.json',rows);guard();assert q.returncode==0,row;print(json.dumps(row),flush=True)
files=[]
for p in sorted(M.rglob('*')):
 assert not p.is_symlink(),str(p)
 if p.is_file():files.append(dict(path=p.relative_to(M).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
assert len(files)==5630,len(files)
write('FULL-MIRROR.json',dict(files=files));guard()
result=dict(result='PASS checked source-feature HEAD native publication/mirror/yearpacks',HEAD=HEAD,TREE=TREE,APP=APP,source19_exact=True,source_index_clean=True,mirror_files=len(files),mirror_manifest_sha256=sha(O/'FULL-MIRROR.json'),mirror_bytes=sum(r['bytes']for r in files),commands=rows,tmp_free=shutil.disk_usage('/tmp').free,workspace_free=shutil.disk_usage('/workspace').free,limits='Canonical people Blender builds/assets, ordinary PR CI, ready, DEV merge and dispatch remain unrun.')
write('RESULT.json',result);print(json.dumps(result),flush=True)
