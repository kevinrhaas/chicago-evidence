#!/usr/bin/env python3
"""External only: original whole check.sh, original1200, owned ephemeral SHM scratch."""
import argparse,datetime,hashlib,importlib.util,json,os,re,resource,shutil,stat,subprocess,sys,tempfile,time
from pathlib import Path
OWNED=Path('/dev/shm/chicago-transport-gates-20261030')
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
SUP_SHA='a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c'
POLICY=Path('/workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/PINNED-EC16-INTAKE-PRESERVED/OWNED-WAGON-BOUND-REPAIR-20261029/resource_admission_v10.py')
POLICY_SHA='eebdd83e057f31bc44f76e0b85acf037f28e4d06807c1070346e4e2802b6d65d'
CONFIG={
'H':dict(repo='/tmp/chicago-horse-20261029',head='ddb77c3191c6fbf28953b8b96f2477bf91f088cb',tree='4278fa10062c3593ea2cf65f7bf41a4bee7d39b0',app='bfc9fcdd77e694e9deb3f5d514d0f45b8fb559cf',guard='/tmp/horse-quiet-head-neck-v6-phaseB-installed-source-freeze-20261030-01.json',guard_sha='f513a58c00b17223fcd46ebae68076bf7288fec6c2832e00fa25e8cb68c4e053',source_count=116,relative_to_repo=True),
'P':dict(repo='/tmp/chicago-transport-resume-20261029',head='9400c662b24909598fa6afdea2df4d3b89e7f25d',tree='eee92b422b653b68593fbfeab11c3c4b37122247',app='44d9d0908178710474c4003e1631dcb8f01f8f84',guard='/tmp/human-world-motion-v4-20261030/CURRENT-UNCHANGED-SOURCE-GUARD.json',guard_sha='0cacf9f7ebc8b650b139a6ef7c9e5148180b87ed0142dbbe5bd0812ef3ea4948',source_count=53,relative_to_repo=False)}

def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,data):p.write_text(json.dumps(data,indent=2)+'\n')
def pin(p,expected=None):
 p=Path(p);assert p.is_file()and not p.is_symlink(),p;b=p.read_bytes();h=sha(b);assert expected is None or h==expected,('Code/guard pin changed',str(p));return dict(path=str(p),bytes=len(b),sha256=h)
def policy():
 pin(POLICY,POLICY_SHA);spec=importlib.util.spec_from_file_location('transport_gate_resource10',POLICY);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.trusted_baseline();return m

def active_owners():
 rows=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:
   exe=Path(os.readlink(p/'exe')).name;words=(p/'cmdline').read_bytes().split(b'\0');words=[os.fsdecode(x)for x in words if x]
   if exe in {'chrome','chromium','headless_shell','chrome-headless-shell'}or any(Path(x).name in {'check.sh','preflight.sh','rederive.mjs','smoke_renderer.mjs','publish.sh'}for x in words[:5]):rows.append(dict(pid=int(p.name),executable=exe,command_prefix=words[:5]))
  except (OSError,ValueError):pass
 return rows

def filesystem_state(p):
 s=os.statvfs(p);return dict(path=str(p),available_bytes=s.f_bavail*s.f_frsize,capacity_bytes=s.f_blocks*s.f_frsize,block_bytes=s.f_frsize)
def owned_scratch(label):
 assert str(OWNED)=='/dev/shm/chicago-transport-gates-20261030'
 OWNED.mkdir(mode=0o700,exist_ok=True);st=OWNED.lstat();assert stat.S_ISDIR(st.st_mode)and not OWNED.is_symlink()and st.st_uid==os.getuid(),'Owned authorized root only'
 p=Path(tempfile.mkdtemp(prefix=label+'-',dir=OWNED));assert p.parent==OWNED and not p.is_symlink();return p

def scratch_probe(scratch):
 # At most5child wall /2CPU each, no browser/network/native application test.
 env={**os.environ,'TMPDIR':str(scratch),'PYTHONDONTWRITEBYTECODE':'1'}
 py=scratch/'python-exec-probe';py.write_text('#!'+sys.executable+'\nimport os,tempfile\nassert tempfile.gettempdir()==os.environ["TMPDIR"]\nfd,p=tempfile.mkstemp()\nos.close(fd)\nwith open(p,"wb")as f:f.write(b"python-scratch-PASS")\nassert open(p,"rb").read()==b"python-scratch-PASS"\nos.unlink(p)\nprint("python-scratch-exec-PASS")\n');py.chmod(0o700)
 js=scratch/'node-exec-probe.mjs';js.write_text('#!/usr/bin/env node\nimport{tmpdir}from"node:os";import*as fs from"node:fs";import assert from"node:assert/strict";assert.equal(tmpdir(),process.env.TMPDIR);const p=tmpdir()+"/node-probe-value";fs.writeFileSync(p,"node-scratch-PASS");assert.equal(fs.readFileSync(p,"utf8"),"node-scratch-PASS");fs.unlinkSync(p);process.stdout.write("node-scratch-exec-PASS\\n");\n');js.chmod(0o700)
 def cap():resource.setrlimit(resource.RLIMIT_CPU,(2,2))
 rows=[]
 for p in [py,js]:
  result=subprocess.run([str(p)],env=env,capture_output=True,text=True,timeout=5,preexec_fn=cap);rows.append(dict(command=[str(p)],returncode=result.returncode,stdout=result.stdout,stderr=result.stderr,CPU_limit_seconds=2,wall_timeout_seconds=5));assert result.returncode==0,rows[-1]
 return dict(at=now(),state='ACTUAL_NODE_PYTHON_EXECUTABLE_OWNED_SCRATCH_PROBE_ONLY_PASS',TMPDIR=str(scratch),filesystem=filesystem_state(scratch),rows=rows,browser_or_application_test=False)

def git(c,*args):
 env={**os.environ,'GIT_NO_LAZY_FETCH':'1','GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'};return subprocess.check_output(['git',*args],cwd=c['repo'],env=env)
def source_snapshot(c):
 pin(c['guard'],c['guard_sha']);g=json.loads(Path(c['guard']).read_bytes());repo=Path(c['repo']);app=repo/'chicago/4d';assert git(c,'rev-parse','HEAD').decode().strip()==c['head'];assert git(c,'rev-parse',c['tree']+':chicago/4d').decode().strip()==c['app']
 index=git(c,'ls-files','--stage','-z');actual=[]
 for entry in index.split(b'\0'):
  if not entry:continue
  meta,path=entry.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0';actual.append((path,mode,oid))
 expected=[]
 for entry in git(c,'ls-tree','-r','-z',c['tree']).split(b'\0'):
  if not entry:continue
  meta,path=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();expected.append((path,mode,oid))
 assert actual==expected,'Complete semantic index must equal pinned whole stagedTREE';assert not git(c,'diff','--name-only','-z','--').strip(),'Unstaged tracked source changed';assert not git(c,'ls-files','--others','--exclude-standard','-z').strip(),'Unexpected untracked source'
 rows=g['source_files'];assert len(rows)==c['source_count'];base=repo if c['relative_to_repo']else app
 for r in rows:
  p=base/r['path'];b=p.read_bytes();assert p.is_file()and not p.is_symlink()and len(b)==r['bytes']and sha(b)==r['sha256'],p
 if c['relative_to_repo']:assert sha(index)==g['semantic_index_sha256']
 else:assert [(os.fsencode(r['path']),r['mode'],r['object'])for r in g['semantic_index']]==actual
 return dict(head=c['head'],tree=c['tree'],app_tree=c['app'],source_files=rows,source_guard=pin(c['guard']),semantic_index_sha256=sha(index),semantic_index_entries=len(actual),unstaged_tracked_changes=False,untracked_files=False),index

def mirror_snapshot(c):
 root=Path(c['repo'])/'site/4d';assert root.is_dir()and not root.is_symlink();rows=[]
 for p in sorted(root.rglob('*')):
  assert not p.is_symlink(),p
  if p.is_file():b=p.read_bytes();rows.append(dict(path=str(p.relative_to(root)),bytes=len(b),sha256=sha(b)))
 assert len(rows)>=5630;return dict(root=str(root),files=rows,files_count=len(rows),bytes=sum(x['bytes']for x in rows))
def copy_demand(c):
 app=Path(c['repo'])/'chicago/4d';roots=[]
 for relative in ['data','docs/RESEARCH']:
  fs=[p for p in(app/relative).rglob('*')if p.is_file()];assert not any(p.is_symlink()for p in(app/relative).rglob('*'));roots.append(dict(path=relative,files=len(fs),allocated_copy_bytes=sum(((p.stat().st_size+4095)//4096)*4096 for p in fs)))
 return dict(roots=roots,mandatory_native_synthesis_copy_bytes=sum(x['allocated_copy_bytes']for x in roots),scratch_reserve_bytes=512*1024**2)

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='operation',required=True);p=sub.add_parser('probe');p.add_argument('--out',type=Path,required=True);p=sub.add_parser('run');p.add_argument('--worker',choices=['H','P'],required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--root-slot-go',action='store_true',required=True);a=parser.parse_args();out=a.out.resolve();assert out.is_relative_to(Path('/tmp'))and not any(out.is_relative_to(Path(c['repo']))for c in CONFIG.values()),'Durable proof directory outside every worker and SHM';out.mkdir(mode=0o700,exist_ok=False)
 assert sys.version_info[:3]==(3,11,17),'Use reviewed Python3.11.17 transport runtime';assert subprocess.check_output(['node','--version'],timeout=5).decode().strip()=='v22.22.0','Use reviewed Node22.22.0 transport runtime'
 pin(SUP,SUP_SHA);m=policy();codepins=dict(wrapper=pin(__file__),supervisor=pin(SUP),shared_resource10=pin(POLICY),trusted_initial_baseline=pin(m.BASELINE_PATH),native_timeout_seconds=1200,resource_floor_RAM=m.MEMORY_FLOOR,workspace=m.WORKSPACE_FLOOR,tmp=m.TMP_FLOOR);save(out/'WRAPPER-CODE-PINS.json',codepins)
 if a.operation=='probe':
  scratch=owned_scratch('probe')
  try:save(out/'PROBE-RESULT.json',scratch_probe(scratch))
  finally:
   assert scratch.parent==OWNED and not scratch.is_symlink();shutil.rmtree(scratch)
  return 0
 c=CONFIG[a.worker];app=Path(c['repo'])/'chicago/4d';resources_before=m.snapshot();assert m.check_snapshot(resources_before)['accepted'];owners=active_owners();save(out/'RESOURCES-BEFORE.json',dict(snapshot=resources_before,assessment=m.check_snapshot(resources_before),active_owners=owners));assert not owners,'Root must allocate an actual closed browser/heavy gap'
 before,index=source_snapshot(c);save(out/'SOURCE-BEFORE.json',before);(out/'COMPLETE-INDEX-BEFORE.z').write_bytes(index);save(out/'MIRROR-BEFORE.json',mirror_snapshot(c));demand=copy_demand(c);scratch=owned_scratch(a.worker.lower());admission=filesystem_state(scratch);admission.update(demand);save(out/'ACTUAL-SHM-SCRATCH-ADMISSION.json',admission)
 native_prefix=out/'native-check';native_result=None;native_cleanup=None;after=None;pair=None;errors=[];started=time.monotonic();native_rc=None;probe=None;env=None;native_attempted=False
 try:
  assert admission['block_bytes']==4096,'Actual SHM filesystem4KiB allocation must match nativecopy census';assert admission['available_bytes']>=demand['mandatory_native_synthesis_copy_bytes']+demand['scratch_reserve_bytes'],'Fresh actual SHM nativecopy plus unchanged512MiB reserve'
  probe=scratch_probe(scratch);save(out/'ACTUAL-SHM-NODE-PYTHON-EXECUTABLE-PROBE.json',probe)
  env={**os.environ,'TMPDIR':str(scratch),'C4D_GATE_REQUIRE_READERS':'1','C4D_GATE_REQUIRE_BASE':'1','CHECK_JOBS':'4','CHECK_TIMINGS':str(out/'NATIVE-CHECK-TIMINGS.tsv'),'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'}
  # Source metadata reads above stay offline. The native gate retains normal promisor fetching.
  env.pop('GIT_NO_LAZY_FETCH',None);native_attempted=True;native_rc=subprocess.run([sys.executable,str(SUP),'--prefix',str(native_prefix),'--cwd',str(app),'--timeout','1200','--','bash','tools/check.sh'],cwd=app,env=env).returncode
  native_result=json.loads(Path(str(native_prefix)+'.result.json').read_bytes());native_cleanup=json.loads(Path(str(native_prefix)+'.cleanup.json').read_bytes());assert native_result['requested_timeout_seconds']==native_result['effective_timeout_seconds']==1200 and native_result['timeout_override_reason']is None and native_result['command']==['bash','tools/check.sh']and native_result['cwd']==str(app);assert native_cleanup['cleanup_complete']and native_cleanup['remaining_owned_children']==[],'Actual owned cleanup required'
 except BaseException as error:errors.append(repr(error))
 finally:
  try:
   after,after_index=source_snapshot(c);assert after==before and after_index==index;save(out/'SOURCE-AFTER.json',after);save(out/'MIRROR-AFTER.json',mirror_snapshot(c))
  except BaseException as error:errors.append('SOURCE/MIRROR: '+repr(error))
  # Only this owned temporary tree, in this same process/mount namespace. All proof logs remain under /tmp.
  try:
   assert scratch.parent==OWNED and not scratch.is_symlink();save(out/'SHM-BEFORE-OWNED-SCRATCH-CLEANUP.json',filesystem_state(scratch))
   if not native_attempted or (native_cleanup is not None and native_cleanup['cleanup_complete']and native_cleanup['remaining_owned_children']==[]):
    shutil.rmtree(scratch);save(out/'SHM-AFTER-OWNED-SCRATCH-CLEANUP.json',filesystem_state(OWNED))
   else:
    save(out/'SHM-RETAINED-NATIVE-CLEANUP-NOT-CLOSED.json',dict(path=str(scratch),native_attempted=native_attempted,native_cleanup=native_cleanup,reason='No removal while actual native owned-child closure is unproven'));errors.append('Native owned-child closure unproven; scratch retained')
  except BaseException as error:errors.append('OWNED SCRATCH CLEANUP: '+repr(error))
  try:
   assert pin(__file__)==codepins['wrapper'];pin(SUP,SUP_SHA);pin(POLICY,POLICY_SHA)
   resources_after=m.snapshot();pair=m.check_pair(resources_before,resources_after);owners_after=active_owners();save(out/'RESOURCES-AFTER.json',dict(snapshot=resources_after,pair_assessment=pair,active_owners=owners_after));assert pair['accepted']and not owners_after,'Actual sharedresource10 bothends and empty ownedslot required'
  except BaseException as error:errors.append('RESOURCE10: '+repr(error))
 text=Path(str(native_prefix)+'.log').read_text(errors='replace')if Path(str(native_prefix)+'.log').exists()else'';plain=re.sub(r'\x1b\[[0-9;]*m','',text);summaries=re.findall(r'^CHECK (PASS|FAIL) — (.+)$',plain,re.M);last=summaries[-1]if summaries else None
 passed=not errors and native_rc==0 and native_result is not None and native_result['returncode']==0 and not native_result['timed_out']and native_cleanup is not None and native_cleanup['cleanup_complete']and not native_cleanup['remaining_owned_children']and after==before and pair is not None and pair['accepted']and last is not None and last[0]=='PASS'
 result=dict(at=now(),status='ACTUAL_FULL_NATIVE_CHECK_SH_PASS_SOURCE_AND_RESOURCE10_EXACT'if passed else'NONPASS_FULL_NATIVE_CHECK_SH_OR_SOURCE_RESOURCE_CLOSURE',worker=a.worker,head=c['head'],tree=c['tree'],app_tree=c['app'],command=['bash','tools/check.sh'],native_timeout_seconds=1200,native_environment_explicit={k:env[k]for k in ['TMPDIR','C4D_GATE_REQUIRE_READERS','C4D_GATE_REQUIRE_BASE','CHECK_JOBS','CHECK_TIMINGS']}if env is not None else None,native_result=native_result,native_cleanup=native_cleanup,final_native_summary=last,seconds=time.monotonic()-started,source_index_unchanged=after==before,shared_resource10_pair=pair,errors=errors,mirror_rebuilt_by_required_native_publish=True,mirror_before_after_equality_claimed=False,source_feature_commit_push='UNRUN',published_both_profile_world_acceptance='SEPARATE/PENDING',DEV_merge='UNRUN')
 save(out/'ACTUAL-WHOLE-GATE-CLOSED.json',result)
 try:print(json.dumps(dict(status=result['status'],out=str(out),native_result=native_result,errors=errors)),flush=True)
 except BrokenPipeError:pass
 return 0 if passed else 1
if __name__=='__main__':sys.exit(main())
