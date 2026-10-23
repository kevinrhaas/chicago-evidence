#!/usr/bin/env python3
"""One opt-in canonical dispatch. Plan-only unless --dispatch; no retry of POST.
Requires final reviewed workflow pin activation before any network request.
"""
import argparse,base64,datetime,hashlib,json,pathlib,re,subprocess,time
REPO='kevinrhaas/chicago';BRANCH='steward/1835-workwear-repair-20261021';WORKFLOW='chicago-4d-humans.yml'
PINNED_WORKFLOW_SHA256=None # ROOT freezes reviewed final workflow bytes before release.
INPUTS={'build_teamsters':True,'build_seated_driver_study':True}
def need(ok,why):
 if not ok:raise ValueError(why)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sha',required=True);p.add_argument('--out',required=True);p.add_argument('--dispatch',action='store_true');a=p.parse_args();need(re.fullmatch('[0-9a-f]{40}',a.sha),'full40SHArequired')
 plan={'repository':REPO,'branch':BRANCH,'sha':a.sha,'workflow':WORKFLOW,'inputs':INPUTS,'out':a.out,'execute':a.dispatch,'pinned_workflow_sha256':PINNED_WORKFLOW_SHA256}
 if not a.dispatch:print(json.dumps(plan,indent=2));return
 need(PINNED_WORKFLOW_SHA256 is not None,'final reviewed workflow pin not frozen; no execution')
 out=pathlib.Path(a.out);need(out.is_absolute() and str(out).startswith('/workspace/shared/'),'outside shared receipt required');need(not out.exists(),'receipt exists; reconcile without redispatch')
 def api(endpoint,body=None):
  args=['gh','api','--method','GET' if body is None else 'POST','repos/'+REPO+'/'+endpoint]
  if body is not None:args+=['--input','-']
  r=subprocess.run(args,input=None if body is None else json.dumps(body),text=True,capture_output=True,timeout=45);need(r.returncode==0,'normalGitHubrequestfailed; no retry');return json.loads(r.stdout) if r.stdout.strip() else None
 def head():return api('git/ref/heads/'+BRANCH)['object']['sha']
 def runs():
  r=api('actions/workflows/'+WORKFLOW+'/runs?event=workflow_dispatch&per_page=100');need(len(r['workflow_runs'])<=100,'invalidrunresponse');return r['workflow_runs']
 need(head()==a.sha,'remotehead differs beforedispatch')
 # Source code audit only: Gitblob API, never CI artifacts/logs.
 blob=api('contents/.github/workflows/'+WORKFLOW+'?ref='+a.sha);need(blob.get('encoding')=='base64','workflow code encoding');need(hashlib.sha256(base64.b64decode(blob['content'])).hexdigest()==PINNED_WORKFLOW_SHA256,'workflow source pin differs')
 before={x['id'] for x in runs()};receipt={**plan,'before_run_ids':sorted(before),'post_succeeded':False,'requested_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'coverage':'UNPROVEN until actual terminal mandatory jobs/steps'}
 with out.open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
 def save():out.write_text(json.dumps(receipt,indent=2)+'\n')
 need(head()==a.sha,'remotehead changed immediately beforePOST')
 # Ambiguous POST error MUST leave false intent receipt; never redispatch automatically.
 api('actions/workflows/'+WORKFLOW+'/dispatches',{'ref':BRANCH,'inputs':{k:'true' for k in INPUTS}});receipt['post_succeeded']=True;save()
 for n in range(10):
  found=[r for r in runs() if r['id'] not in before and r['head_sha']==a.sha and r['head_branch']==BRANCH and r['event']=='workflow_dispatch'];receipt['runs']=found;save();need(len(found)<=1,'multipleactualruns; reconcilewithoutPOST')
  if len(found)==1:break
  if n<9:time.sleep(3)
 receipt['remote_head_after']=head();save();need(receipt['remote_head_after']==a.sha and len(receipt.get('runs',[]))==1,'incomplete discovery/headchange; reconcilewithoutPOST');print(json.dumps({'receipt':str(out),'run_id':receipt['runs'][0]['id'],'sha':a.sha}))
if __name__=='__main__':main()
