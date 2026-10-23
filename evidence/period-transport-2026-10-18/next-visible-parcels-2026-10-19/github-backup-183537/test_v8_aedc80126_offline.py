import importlib.util,pathlib,json,copy
p=pathlib.Path('/workspace/shared/verify_normal_dev_gates_v8_aedc80126.py');sp=importlib.util.spec_from_file_location('v8',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);r={'scope':'OFFLINE committed source +actual attempt2 auxmetadata +synthetic negative controls; no network/main/CIgate claim','controls':[]}
def case(name,fn,want):
 try:fn();ok=True
 except Exception:ok=False
 r['controls'].append({'name':name,'expected_accept':want,'actual_accept':ok,'passed':ok==want})
case('actual committed source pins and mandatory contracts',lambda:m.source_ok({p:m.committed(p)for p in m.PINS}),True)
a=pathlib.Path('/workspace/shared/aedc80126-auxiliary-attempt2-terminal');run=m.load(a/'run.json');jobs=m.load(a/'jobs.json');case('actual attempt2 source-DAG-supported skip classification',lambda:m.auxiliary_jobs_ok(run,jobs),True)
x=copy.deepcopy(run);x['run_attempt']=1;case('old attempt1 not accepted',lambda:m.auxiliary_jobs_ok(x,jobs),False)
x=copy.deepcopy(jobs);x['jobs'][0]['conclusion']='cancelled';case('cancelled warranted refused',lambda:m.auxiliary_jobs_ok(run,x),False)
x=copy.deepcopy(jobs);x['jobs'][0]['steps'][3]['conclusion']='skipped';case('skipped q refused',lambda:m.auxiliary_jobs_ok(run,x),False)
x=copy.deepcopy(jobs);x['jobs'][0]['steps'][4]['conclusion']='failure';case('failed live refused',lambda:m.auxiliary_jobs_ok(run,x),False)
x=copy.deepcopy(jobs);x['jobs'][1]['id']=1;case('unbound child job/check ID refused',lambda:m.auxiliary_jobs_ok(run,x),False)
run={'id':m.AUTOMATIC_SMOKE_RUN,'head_sha':m.SHA,'head_branch':m.BRANCH,'event':'push','path':m.SMOKE,'run_attempt':1,'status':'completed','conclusion':'success'};j={'id':1,'run_id':m.AUTOMATIC_SMOKE_RUN,'head_sha':m.SHA,'run_attempt':1,'name':'smoke','status':'completed','conclusion':'success','steps':[{'name':n,'status':'completed','conclusion':'success'}for n in m.SMOKE_STEPS]};data={'total_count':1,'jobs':[j]};case('synthetic actual automatic published steps all success',lambda:m.automatic_smoke_ok(run,data),True)
x=copy.deepcopy(data);x['jobs'][0]['steps'][1]['conclusion']='skipped';case('automatic test skip refused',lambda:m.automatic_smoke_ok(run,x),False)
x=copy.deepcopy(data);x['jobs'][0]['steps'][1]['status']='in_progress';x['jobs'][0]['steps'][1]['conclusion']=None;case('automatic parent-success stale step refused',lambda:m.automatic_smoke_ok(run,x),False)
x=copy.deepcopy(run);x['event']='workflow_dispatch';case('selected leg cannot substitute automatic push full',lambda:m.automatic_smoke_ok(x,data),False)
x=copy.deepcopy(run);x['head_sha']='0'*40;case('automatic wronghead refused',lambda:m.automatic_smoke_ok(x,data),False)
r['PASS']=all(x['passed']for x in r['controls']);pathlib.Path('/workspace/shared/v8-aedc80126-offline-controls.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));assert r['PASS']
