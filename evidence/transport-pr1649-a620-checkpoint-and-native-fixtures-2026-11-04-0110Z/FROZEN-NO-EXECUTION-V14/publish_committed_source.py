"""ROOT-authorized exact committed publish/check; full preflight remains pending."""
from pathlib import Path
import argparse,json,os,subprocess,sys
from run_current_world_case import SUP,sha,load,save,committed_source,checkpoint_bridge,prepare_guard,targeted_owner

def main():
 p=argparse.ArgumentParser();p.add_argument('--binding',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();b=load(a.binding)
 assert b['ROOT_EXPLICIT_CHECKPOINT_PUBLICATION_GO']is True;R=Path(b['repo']);A=R/'chicago/4d';O=a.out;assert not O.exists();lock,guard=prepare_guard(b)
 before=committed_source(R,b['source']);checkpoint=checkpoint_bridge(b,R,before);owner=targeted_owner(b,R,before);initial=guard.snapshot();assert guard.check(initial)['accepted'];O.mkdir(parents=True);ledger=[];errors=[]
 save(O/'STATE.json',dict(status='RUNNING_COMMITTED_NATIVE_PUBLICATION_NOT_PASS',mode=b['mode'],source_before=before,checkpoint_commit_bridge=checkpoint,targeted_owner_APP_bridge=owner))
 try:
  for name,cmd,cap in [('publish',['bash','tools/publish.sh'],180),('published-check',['node','tools/check_published.mjs'],120)]:
   assert committed_source(R,b['source'])==before;rb=guard.snapshot();assert guard.check(rb)['accepted'];prefix=O/name
   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
   with(O/(name+'.stdout')).open('xb')as stdout:q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(A),'--timeout',str(cap),'--',*cmd],env=env,stdout=stdout,stderr=subprocess.STDOUT)
   result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');resources=guard.pair(rb,guard.snapshot());after=committed_source(R,b['source'])
   row=dict(label=name,command=cmd,result=result,cleanup=cleanup,resources=resources,source_after=after,log=str(prefix)+'.log',log_sha256=sha(str(prefix)+'.log'));ledger.append(row);save(O/'LEDGER.json',ledger)
   assert q.returncode==result['returncode']==0 and not result['timed_out']and result['requested_timeout_seconds']==result['effective_timeout_seconds']==cap and result['timeout_override_reason']is None
   assert result['command']==cmd and result['cwd']==str(A)and cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted']and after==before
 except BaseException as ex:errors.append(repr(ex))
 try:after=committed_source(R,b['source'])
 except BaseException as ex:after=None;errors.append('final source guard: '+repr(ex))
 resources=guard.pair(initial,guard.snapshot());stamp=load(R/'site/4d/build.json').get('version')if(R/'site/4d/build.json').exists()else None
 passed=not errors and len(ledger)==2 and after==before and resources['accepted']and stamp==before['HEAD'][:10]
 closed=dict(status='ACTUAL_NATIVE_CURRENT_DEV_PUBLICATION_PASS_NOT_FULL_GATE'if passed else'ACTUAL_NATIVE_CURRENT_DEV_PUBLICATION_NONPASS_NOT_FULL_GATE',mode=b['mode'],source_before=before,source_after=after,checkpoint_receipt=b['checkpoint_receipt'],parent_chain_receipt=b['parent_chain_receipt'],checkpoint_commit_bridge=checkpoint,targeted_owner_APP_bridge=owner,ledger=ledger,resources=resources,native_build_stamp_exact_committed_HEAD=stamp,errors=errors,full_all4_commit_CI_DEV_delivery_or_photo_qualification=False)
 save(O/'CLOSED.json',closed);print(json.dumps({'status':closed['status'],'receipt':str(O/'CLOSED.json'),'sha256':sha(O/'CLOSED.json')}));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
