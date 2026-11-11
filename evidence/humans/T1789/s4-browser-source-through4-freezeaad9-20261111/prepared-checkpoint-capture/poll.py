from pathlib import Path
import subprocess,json,datetime
P=Path(__file__).resolve().parent
registered=json.loads((P/'REGISTERED.json').read_bytes())
S=registered['source_SHA'];RUN=registered['run_id']
assert isinstance(S,str) and len(S)==40 and type(RUN) is int and RUN not in (43000644195,43018920928,43053758545)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
def get(endpoint):
    r=subprocess.run(['gh','api','--hostname','github.com','--method','GET','repos/kevinrhaas/chicago/'+endpoint],capture_output=True,timeout=20)
    assert r.returncode==0,r.stderr.decode(errors='replace')[:300];assert len(r.stdout)<=1048576
    return r.stdout,json.loads(r.stdout)
raw,jobs=get('actions/runs/'+str(RUN)+'/jobs?per_page=100');assert jobs['total_count']==len(jobs['jobs'])<=100
(P/('jobs-'+stamp+'.json')).write_bytes(raw)
raw,run=get('actions/runs/'+str(RUN));assert run['id']==RUN and run['head_sha']==S and run['run_attempt']==1 and run['event']=='workflow_dispatch'
(P/('run-'+stamp+'.json')).write_bytes(raw)
summary=[];stop=run['status']=='completed'
for j in jobs['jobs']:
    assert j['head_sha']==S and j['run_id']==RUN and j['run_attempt']==1
    bad=j['name'] in ['humans','clothing-capture-v2'] and j['conclusion'] not in (None,'success','skipped')
    stop=stop or bad
    summary.append({'id':j['id'],'name':j['name'],'status':j['status'],'conclusion':j['conclusion'],'active_steps':[v['name'] for v in j['steps'] if v['status']=='in_progress'],'failed_steps':[v['name'] for v in j['steps'] if v['conclusion']=='failure']})
print(json.dumps({'UTC':stamp,'run':RUN,'status':run['status'],'conclusion':run['conclusion'],'jobs':summary,'stop':stop}))
