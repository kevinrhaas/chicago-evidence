from pathlib import Path
import os,sys,json,subprocess,hashlib,fcntl,importlib.util,difflib
sys.dont_write_bytecode=True
D=Path(__file__).parent;R=Path('/workspace/chicago-bounds-proposal-20261103');SUP=Path('/workspace/.cloud-setup/transport-supervise.py');GP=Path('/workspace/.cloud-setup/transport-current-20261103/resource_guard.py');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();read=lambda p:json.loads(Path(p).read_text());save=lambda p,x:Path(p).write_text(json.dumps(x,indent=2)+'\n')
assert sha(GP.with_name('RESTORED-RUNTIME-BASELINE.json'))=='3f494df78dc3dfaeb0bc5d2c7b7c80d05b0dc82950b30375316a7125f886b3ff'
paths=['chicago/4d/renderers/web/js/batch-bounds.js','chicago/4d/tools/check_batch_bounds.mjs'];rows=[];patch=''
for p in paths:
 a=D/'BASE'/p;b=R/p;rows.append(dict(path=p,before_sha256=sha(a),after_sha256=sha(b)));patch+=''.join(difflib.unified_diff(a.read_text().splitlines(keepends=True),b.read_text().splitlines(keepends=True),fromfile='a/'+p,tofile='b/'+p));q=subprocess.run(['git','diff','--no-index','--check','--',str(a),str(b)],capture_output=True,text=True,timeout=5);assert q.returncode in[0,1]and not q.stdout and not q.stderr
save(D/'PREIMAGES.json',rows);(D/'EXACT-BOUND-CACHE.patch').write_text(patch)
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
spec=importlib.util.spec_from_file_location('guard',GP);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('CHICAGO_TICKETS_DIR',None);ledger=[]
for name,args in [('native-positive',[]),('native-original-selftest',['--self-test'])]:
 before=g.snapshot();assert g.check(before)['accepted'];p=D/name;cmd=['node','tools/check_batch_bounds.mjs',*args]
 with Path(str(p)+'.stdout').open('xb')as f:q=subprocess.run([sys.executable,str(SUP),'--prefix',str(p),'--cwd',str(R/'chicago/4d'),'--timeout','5','--',*cmd],env=env,stdout=f,stderr=subprocess.STDOUT)
 r=read(str(p)+'.result.json');c=read(str(p)+'.cleanup.json');pair=g.pair(before,g.snapshot());ledger.append(dict(prefix=str(p),command=cmd,result=r,cleanup=c,resources=pair,log_sha256=sha(str(p)+'.log')));save(D/'CPU-LEDGER.json',ledger);assert q.returncode==r['returncode']==0 and not r['timed_out']and r['requested_timeout_seconds']==r['effective_timeout_seconds']==5 and c['cleanup_complete']and not c['remaining_owned_children']and pair['accepted']
proof=dict(status='ISOLATED_WORKTREE_EXACT_BOUND_CACHE_CPU_PASS_NOT_ADOPTED_WHOLE_SCENE_MEMORY_UNRUN',base='ae762df51dad3bd48e7d5307e0bda3cd0ce05e31',worktree=str(R),patch=dict(path=str(D/'EXACT-BOUND-CACHE.patch'),sha256=sha(D/'EXACT-BOUND-CACHE.patch')),paths=rows,resource_baseline_sha256=sha(GP.with_name('RESTORED-RUNTIME-BASELINE.json')),canonical_lock=True,ledger=ledger,original_controls_and_rounding_selftest_retained=True,all_encoded_rows_compare_exact_old_F32_words=True,original_full_arrays_nulled_on_success=True,no_temporary_radius_Map_retained=True,whole_scene_savings_measured=False,browser_GPU_or_fullgate_performed=False,ROOT_index_source_site_writes=False)
save(D/'CLOSED-CPU-QUALIFICATION.json',proof);print(json.dumps(dict(status=proof['status'],patch_sha256=proof['patch']['sha256'],closed_sha256=sha(D/'CLOSED-CPU-QUALIFICATION.json'),seconds=[r['result']['seconds']for r in ledger])))
