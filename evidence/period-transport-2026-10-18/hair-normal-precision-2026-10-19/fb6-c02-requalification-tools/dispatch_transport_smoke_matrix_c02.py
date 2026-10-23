#!/usr/bin/env python3
"""Dispatch the existing smoke grid at one verified frozen branch head. One-shot."""
import datetime,json,pathlib,re,subprocess,sys,time
repo='kevinrhaas/chicago';branch='steward/period-transport-2793';workflow='chicago-4d-smoke.yml'
def api(endpoint,body=None):
    cmd=['gh','api',endpoint]
    if body is not None:cmd+=['--method','POST','--input','-']
    r=subprocess.run(cmd,input=None if body is None else json.dumps(body),text=True,capture_output=True,check=True)
    return json.loads(r.stdout) if r.stdout.strip() else None
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def head():return api(f'repos/{repo}/git/ref/heads/{branch}')['object']['sha']
def runs():return api(f'repos/{repo}/actions/workflows/{workflow}/runs?event=workflow_dispatch&per_page=100')['workflow_runs']
PRIORITY = [('desktop','13'),('desktop','14'),('desktop','9-12'),('mobile','13')]
RANGES = ['1-2','3-4','5','6-7','8','9-12','13','14','15']
def cells():
    grid=[(v,s)for v in ['mobile','desktop']for s in RANGES]
    ordered=PRIORITY+[c for c in grid if c not in PRIORITY]
    if len(ordered)!=18 or len(set(ordered))!=18 or set(ordered)!=set(grid):raise ValueError('exact18uniquegridcellsrequired')
    return ordered

def main():
    if len(sys.argv)==2 and sys.argv[1]=='--plan':
        print(json.dumps({'priority_cells':cells(),'dispatch':False}));return
    if len(sys.argv)!=2 or not re.fullmatch('[0-9a-f]{40}',sys.argv[1]):raise SystemExit('pass exact committed/pushed SHA')
    global sha,out
    sha=sys.argv[1];out=pathlib.Path('/workspace/shared')/('transport-smoke-dispatch-c02-'+sha[:9]+'.json')
    if out.exists():raise SystemExit('receipt exists; reconcile it before any further dispatch')
    if head()!=sha:raise SystemExit('remote branch head differs; do not dispatch')
    before={r['id']for r in runs()}
    receipt={'repository':repo,'branch':branch,'sha':sha,'workflow':workflow,'started_utc':now(),'before_run_ids':sorted(before),'dispatches':[],'discovered_runs':[],'coverage_status':'UNPROVEN: scheduled partial legs only'}
    def save():out.write_text(json.dumps(receipt,indent=2)+'\n')
    save()
    for viewport,stage in cells():
        if head()!=sha:raise SystemExit('remote branch head changed before POST; reconcile receipt, do not redispatch')
        record={'viewport':viewport,'stage':stage,'requested_utc':now(),'post_succeeded':False};receipt['dispatches'].append(record);save()
        api(f'repos/{repo}/actions/workflows/{workflow}/dispatches',{'ref':branch,'inputs':{'viewport':viewport,'stage':stage}})
        record['post_succeeded']=True;save()
    for attempt in range(4):
        new=[r for r in runs()if r['id']not in before and r['head_sha']==sha]
        receipt['discovered_runs']=[{k:r[k]for k in ['id','head_sha','run_attempt','status','conclusion','created_at','html_url']}for r in new];save()
        if len(new)==18:break
        if attempt<3:time.sleep(2)
    receipt['finished_utc']=now();receipt['remote_head_after']=head();save()
    if receipt['remote_head_after']!=sha or len(receipt['discovered_runs'])!=18:raise SystemExit('dispatch receipt saved; reconcile incomplete discovery without redispatching')
    print(json.dumps({'receipt':str(out),'sha':sha,'run_ids':[r['id']for r in receipt['discovered_runs']],'coverage':'UNPROVEN until actual log/union validation'}))

if __name__=='__main__':main()
