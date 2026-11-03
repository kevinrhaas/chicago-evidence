"""PREP ONLY. Three explicit phases: fresh native all4, checked commit/HEAD QA, normal draft push."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,time
sys.dont_write_bytecode=True
D=Path(__file__).parent

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['gate','commit','push']);ap.add_argument('--root-go',required=True);a=ap.parse_args();C=read(a.root_go)
 assert not C['template_only'] and C['controller_sha256']==digest(__file__)
 assert C[{'gate':'ROOT_EXPLICIT_FRESH_ALL4_GO','commit':'ROOT_EXPLICIT_CHECKED_COMMIT_AND_HEAD_QA_GO','push':'ROOT_EXPLICIT_NORMAL_DRAFT_PUSH_GO'}[a.phase]]is True
 R=Path(C['repo']);A=R/'chicago/4d';E=C['source'];H=E['HEAD'];N=E['MERGE_HEAD'];REF=C['private_base_ref'];SUP=Path(C['supervisor']);GP=Path(C['resource_guard'])
 assert sys.version_info[:2]==(3,11) and subprocess.check_output(['node','--version']).decode().startswith('v22.')
 assert digest(SUP)==C['supervisor_sha256'] and digest(GP)==C['resource_guard_sha256'] and digest(GP.with_name('RESTORED-RUNTIME-BASELINE.json'))==C['resource_baseline_sha256']
 env=dict(os.environ,CHECK_JOBS='4',C4D_GATE_REQUIRE_READERS='1',C4D_GATE_REQUIRE_BASE='1',C4D_RULINGS_BASE=REF,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='0',PYTHONDONTWRITEBYTECODE='1',PW_EXECUTABLE=C['browser'],PLAYWRIGHT_BROWSERS_PATH=C['browser_root'])
 for k in ['CHICAGO_TICKETS_DIR','CHECK_PART','BASE']:env.pop(k,None)
 def git(*args,repo=R):return subprocess.check_output(['git','-c','gc.auto=0','-c','maintenance.auto=false','-C',str(repo),*args],env=env,timeout=30)
 def val(*args,repo=R):return git(*args,repo=repo).decode().strip()
 def protect():
  assert val('rev-parse','HEAD',repo=Path('/workspace/chicago'))==C['protected_parent_HEAD']
  assert digest('/workspace/chicago/.git/index')==C['protected_parent_index_sha256']
  assert val('rev-parse','refs/remotes/origin/dev',repo=Path('/workspace/chicago'))==C['protected_parent_origin_dev']
 base_initialized=a.phase!='gate'
 def source(head,pending):
  protect();
  if base_initialized:assert val('rev-parse','refs/remotes/origin/dev')==N
  assert val('rev-parse','HEAD')==head and val('rev-parse',REF)==N and val('symbolic-ref','HEAD')=='refs/heads/'+C['branch']
  if pending:assert val('rev-parse','MERGE_HEAD')==N
  else:
   assert subprocess.run(['git','-C',str(R),'rev-parse','--verify','-q','MERGE_HEAD'],env=env,stdout=subprocess.DEVNULL).returncode!=0
   assert val('rev-parse','HEAD^{tree}')==E['TREE'] and val('rev-parse','HEAD:chicago/4d')==E['APP']
  assert not git('ls-files','-u').strip() and not git('diff','--name-only').strip() and not git('ls-files','--others','--exclude-standard').strip()
  if not pending:assert not git('diff','--cached','--name-only').strip()
  assert hashlib.sha256(git('ls-files','--stage','-z')).hexdigest()==E['semantic_index_sha256']
  for rel,pin in C['execution_pins'].items():assert digest(R/rel)==pin
  return dict(HEAD=head,MERGE_HEAD=N if pending else None,TREE=E['TREE'],APP=E['APP'],semantic_index_sha256=E['semantic_index_sha256'],pending_merge=pending)
 def fields(s):return {k:s[k]for k in ['TREE','APP','semantic_index_sha256']}
 def valid(row,cap=None):
  r=row['result'];cl=row['cleanup'];assert r['returncode']==0 and not r['timed_out'] and r['timeout_override_reason']is None
  if cap is not None:assert r['requested_timeout_seconds']==r['effective_timeout_seconds']==cap
  assert cl['cleanup_complete'] and not cl['remaining_owned_children'] and row['resources']['accepted']
 lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('restored_epoch_resource_guard',GP);guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
 G=Path(C['gate_output']);Q=Path(C['delivery_output']);out=G if a.phase=='gate'else Q
 if a.phase in ['gate','commit']:assert not out.exists();out.mkdir()
 else:assert out.is_dir()
 assert out.parent==Path('/dev/shm')
 ledger=[];state=dict(status='RUNNING_'+a.phase.upper()+'_NOT_PASS',phase=a.phase,source=E,resource_epoch_baseline_sha256=C['resource_baseline_sha256'])
 def persist():save(out/('GATE-LEDGER.json'if a.phase=='gate'else'HEAD-QA-LEDGER.json'if a.phase=='commit'else'PUSH-LEDGER.json'),ledger);save(out/'STATE.json',state)
 def run(label,cmd,cwd,cap,head,pending):
  before=source(head,pending);r0=guard.snapshot();assert guard.check(r0)['accepted'];p=out/label;state.update(active_label=label,command=cmd);persist()
  with Path(str(p)+'.supervisor.stdout').open('xb',buffering=0)as f:q=subprocess.run([sys.executable,str(SUP),'--prefix',str(p),'--cwd',str(cwd),'--timeout',str(cap),'--',*cmd],env=env,stdout=f,stderr=subprocess.STDOUT)
  result=read(str(p)+'.result.json');cleanup=read(str(p)+'.cleanup.json');resources=guard.pair(r0,guard.snapshot())
  after=None if label=='normal-checked-integration-commit'else source(head,pending)
  row=dict(label=label,command=cmd,result=result,cleanup=cleanup,resources=resources,source_before=before,source_after=after,log=str(p)+'.log',log_sha256=digest(str(p)+'.log'));ledger.append(row);persist();valid(row,cap);assert q.returncode==result['returncode'] and result['command']==cmd and result['cwd']==str(cwd);protect();return row
 def footer(body,part,want):
  body=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',body)
  f=re.findall(r'^CHECK PASS[^\n]*part '+str(part)+r'/4:\s*(\d+) steps, none red\.$',body,re.M)
  o=re.findall(r'^  This is part '+str(part)+r' of 4; the other (\d+) steps are in the other parts\.',body,re.M)
  s=re.findall(r'^  (\d+) of them are self-tests that prove a gate by breaking it;',body,re.M)
  assert len(f)==len(o)==len(s)==1 and not re.search(r'^CHECK FAIL',body,re.M)
  got=dict(selected_steps=int(f[0]),selftests=int(s[0]),elsewhere_steps=int(o[0]));assert got==want
  assert 'green only when every part is: tools/check.sh --part 1/4 through --part 4/4.'in body;return got
 scratch=None;owned_scratch=False
 try:
  if a.phase=='gate':
   source(H,True)
   roll=read(C['roll_closure']);adopt=read(C['adoption_closure']);assert roll['status']=='NORMAL_DEV_ROLLFORWARD_NATIVE_OWNERS_PASS_FULL_GATE_NOT_RUN'
   assert adopt['parent_TREE']==roll['source_after']['TREE'] and adopt['all_other_blobs_and_modes_exact'] and adopt['source_after']==E
   for p,pin in C['source_receipt_pins'].items():assert digest(p)==pin
   memory=read(C['actual_mobile_PASS']);assert memory['status']=='ACTUAL_NATIVE_1904_MOBILE_MEMORY_PASS' and memory['browser_version']=='Chromium 141.0.7390.37'
   assert all(memory['source_before'][k]==memory['source_after'][k]==E[k]for k in E)
   assert len(memory['ledger'])==3
   for row,cap in zip(memory['ledger'],[180,120,600]):valid(row,cap)
   assert memory['ledger'][-1]['command'][:8]==['node','tools/measure_memory.mjs','--gate','--year','1904','--only','mobile','--json']
   mr=memory['native_memory_report']['rows'];assert len(mr)==1 and mr[0]['totals']['total']<=419430400 and not mr[0]['errors']
   # Count declarations from this exact native source, including its indented preview step.
   text=(A/'tools/check.sh').read_text();rows=re.findall(r'(?m)^[ \t]*(?:(every_part)\s+)?(step|selftest)\s+',text)
   assert len(rows)==1150 and sum(kind=='selftest'for _,kind in rows)==400 and sum(bool(e)for e,_ in rows)==3
   assert (R/'.github/chicago-4d-dev-preview.mjs').is_file()
   expected={str(k):dict(selected_steps=0,selftests=0,elsewhere_steps=0)for k in range(1,5)}
   for ordinal,(every,kind)in enumerate(rows,1):
    for k in range(1,5):
     if every or(ordinal-1)%4+1==k:expected[str(k)]['selected_steps']+=1;expected[str(k)]['selftests']+=kind=='selftest'
     else:expected[str(k)]['elsewhere_steps']+=1
   ref=subprocess.run(['git','-C',str(R),'show-ref','--verify','--hash','refs/remotes/origin/dev'],env=env,capture_output=True,text=True)
   if ref.returncode:assert C['ALLOW_RECOVERED_H_ONLY_ORIGIN_DEV_INITIALIZATION'];git('update-ref','refs/remotes/origin/dev',N);protect()
   else:assert ref.stdout.strip()==N
   base_initialized=True
   save(out/'ELIGIBILITY.json',dict(source=E,source_receipts=C['source_receipt_pins'],actual_current_mobile_PASS=dict(path=C['actual_mobile_PASS'],sha256=digest(C['actual_mobile_PASS'])),expected_parts=expected,native_distinct_steps=1150,selftests=400,no_historical_parts_or_memory_or_world_retargeted=True,H_only_origin_dev=N))
   scratch=Path(C['native_TMPDIR']);assert scratch.parent==Path('/dev/shm')and not scratch.exists();s=guard.snapshot();assert guard.check(s)['accepted']and s['available_memory_bytes']-1569931807>=4*1024**3 and shutil.disk_usage('/dev/shm').free>1569931807;scratch.mkdir(mode=0o700);owned_scratch=True;env['TMPDIR']=str(scratch)
   probe=subprocess.run([sys.executable,'-c',"import tempfile,pathlib;d=tempfile.TemporaryDirectory(prefix='native-gate-probe-');p=pathlib.Path(d.name)/'probe';p.write_bytes(b'native');assert p.read_bytes()==b'native';d.cleanup()"],env=env,capture_output=True,timeout=5);assert probe.returncode==0
   run('explicit-pinned-ID-base',['node','tools/resolve_id_collisions.mjs','--base',REF,'--check'],A,120,H,True)
   run('explicit-pinned-history-base',['node','tools/changelog-history.mjs','--base',REF],A,120,H,True)
   for k in range(1,5):
    row=run('native-part-'+str(k),['bash','tools/check.sh','--part',str(k)+'/4'],A,600,H,True);row['native_footer_counts']=footer(Path(row['log']).read_text(errors='replace'),k,expected[str(k)]);persist()
   parts=ledger[2:];assert len(parts)==4 and sum(v['native_footer_counts']['selected_steps']for v in parts)-9==1150 and sum(v['native_footer_counts']['selftests']for v in parts)==400
   state.update(status='PASS_ALL_FOUR_NATIVE_PARTS_SAME_FINAL_SOURCE',source_after=source(H,True),distinct_steps=1150,selftests=400,actual_total_native_part_seconds=sum(v['result']['seconds']for v in parts),original_foreground_cap_each_part_seconds=600,current_world_PASS=False,commit_push_performed=False)
  elif a.phase=='commit':
   closed=read(G/'CLOSED.json');assert closed['status']=='PASS_ALL_FOUR_NATIVE_PARTS_SAME_FINAL_SOURCE'and fields(closed['source_after'])==fields(E)and closed['distinct_steps']==1150 and closed['selftests']==400 and closed['owned_TMPDIR_cleanup_complete']
   assert len(closed['ledger'])==6
   for row in closed['ledger']:valid(row);assert digest(row['log'])==row['log_sha256']
   assert [v['command']for v in closed['ledger'][2:]]==[['bash','tools/check.sh','--part',str(k)+'/4']for k in range(1,5)]
   source(H,True);assert digest(C['commit_message'])==C['commit_message_sha256']
   run('normal-checked-integration-commit',['git','-c','gc.auto=0','-c','maintenance.auto=false','commit','--file',C['commit_message']],R,120,H,True)
   new=val('rev-parse','HEAD');assert val('show','-s','--format=%P',new).split()==[H,N];committed=source(new,False)
   binding=dict(schema='chicago-t3088-checked-integration-commit-v1',status='COMMITTED_EXACT_FOUR_PART_SOURCE_HEAD_QA_PENDING',source=committed,parents=[H,N],gate=dict(path=str(G/'CLOSED.json'),sha256=digest(G/'CLOSED.json'),distinct_steps=1150,selftests=400),current_world_PASS=False,remote_push_performed=False)
   save(out/'ACTUAL-COMMITTED-SOURCE-BINDING.json',binding)
   cmds=[('HEAD-check-changelog-entry',['node','tools/check-changelog-entry.mjs',REF,'HEAD']),('HEAD-resolve-ID-collisions',['node','tools/resolve_id_collisions.mjs','--base',REF,'--check']),('HEAD-check-changelog',['node','tools/check-changelog.mjs']),('HEAD-changelog-entries',['node','tools/changelog-entries.mjs','--check']),('HEAD-changelog-history',['node','tools/changelog-history.mjs','--base',REF]),('HEAD-whitespace',['git','diff','--check',REF,'HEAD'])]
   for label,cmd in cmds:run(label,cmd,A,120,new,False)
   qa=dict(status='PASS_FIVE_ACTUAL_HEAD_QUESTIONS_AND_WHITESPACE',source=source(new,False),commit_binding_sha256=digest(out/'ACTUAL-COMMITTED-SOURCE-BINDING.json'),ledger=ledger,remote_push_performed=False);save(out/'ACTUAL-FIVE-HEAD-QA-AND-WHITESPACE-CLOSED.json',qa);state.update(status=qa['status'],source_after=qa['source'])
  else:
   b=read(Q/'ACTUAL-COMMITTED-SOURCE-BINDING.json');qa=read(Q/'ACTUAL-FIVE-HEAD-QA-AND-WHITESPACE-CLOSED.json');new=b['source']['HEAD'];assert qa['status']=='PASS_FIVE_ACTUAL_HEAD_QUESTIONS_AND_WHITESPACE'and qa['source']==b['source'];assert qa['commit_binding_sha256']==digest(Q/'ACTUAL-COMMITTED-SOURCE-BINDING.json');source(new,False)
   for row in qa['ledger']:valid(row,120)
   def api(label,path):
    q=subprocess.run(['gh','api','--method','GET','repos/kevinrhaas/chicago/'+path],env=env,capture_output=True,text=True,timeout=30);(out/(label+'.stdout.json')).write_text(q.stdout);assert q.returncode==0;return json.loads(q.stdout)
   branch=C['branch'];pr=api('PR-BEFORE-PUSH','pulls/1649');ref=api('REF-BEFORE-PUSH','git/ref/heads/'+branch);assert pr['head']['sha']==ref['object']['sha']==H and pr['draft']is True and pr['state']=='open'and pr['base']['ref']=='dev'and pr['head']['ref']==branch and pr['head']['repo']['full_name']=='kevinrhaas/chicago'
   run('normal-feature-push',['git','-c','gc.auto=0','-c','maintenance.auto=false','push','origin','HEAD:refs/heads/'+branch],R,120,new,False)
   assert git('ls-remote','--exit-code','origin','refs/heads/'+branch).decode().split()[0]==new
   for attempt in range(3):
    pr=api('PR-AFTER-PUSH-'+str(attempt),'pulls/1649');ref=api('REF-AFTER-PUSH-'+str(attempt),'git/ref/heads/'+branch);assert pr['draft']is True and pr['state']=='open'and pr['base']['ref']=='dev'and pr['head']['ref']==branch and pr['head']['repo']['full_name']=='kevinrhaas/chicago'
    if pr['head']['sha']==ref['object']['sha']==new:break
    assert pr['head']['sha']in [H,new]and ref['object']['sha']in [H,new]
    if attempt<2:time.sleep(2)
   else:raise AssertionError('Read-only API propagation pending; never retry the push')
   state.update(status='NORMAL_FEATURE_PUSH_EXISTING_DRAFT_PR_UPDATED',source_after=source(new,False),PR=dict(number=1649,url=pr['html_url'],draft=True,HEAD=new),parents=[H,N],gate=b['gate'],five_HEAD_QA=dict(path=str(Q/'ACTUAL-FIVE-HEAD-QA-AND-WHITESPACE-CLOSED.json'),sha256=digest(Q/'ACTUAL-FIVE-HEAD-QA-AND-WHITESPACE-CLOSED.json')),DEV_merge_performed=False,PR_ready_performed=False,current_world_PASS=False)
  persist()
 except BaseException as ex:state.update(status='NONPASS_NO_AUTOMATIC_RETRY',failure=repr(ex));persist();raise
 finally:
  if owned_scratch:
   assert scratch.is_dir()and not scratch.is_symlink();shutil.rmtree(scratch);state['owned_TMPDIR_cleanup_complete']=not scratch.exists();assert state['owned_TMPDIR_cleanup_complete']
  persist();final=dict(**state,ledger=ledger)
  save(out/('CLOSED.json'if a.phase=='gate'and state['status'].startswith('PASS_')else'CHECKED-DRAFT-DELIVERY-CLOSED.json'if a.phase=='push'and state['status']=='NORMAL_FEATURE_PUSH_EXISTING_DRAFT_PR_UPDATED'else'PHASE-'+a.phase.upper()+'-CLOSED.json'),final)
 print(json.dumps(state),flush=True)
if __name__=='__main__':main()
