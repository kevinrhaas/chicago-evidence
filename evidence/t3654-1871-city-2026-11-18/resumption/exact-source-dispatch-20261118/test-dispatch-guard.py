import copy, datetime, hashlib, importlib.util, json, pathlib, sys, tempfile
path=pathlib.Path('/tmp/t3654-dispatch-smoke.py')
spec=importlib.util.spec_from_file_location('dispatch_guard',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sha='871698ae94659100fcb8894f4967d4b15c62150f';base='169404c9f99d2defeca2b05f2364c868a4f4e745'
valid={'schema':'t3654-hosted-source-gate-v1','complete':True,'source_jobs_complete':True,'source_commit':sha,'included_dev_base':base,'repository':'kevinrhaas/chicago','pull_request':2198,'run_id':44407494538,'url':'https://github.com/kevinrhaas/chicago/actions/runs/44407494538','parts':[{'part':f'{n}/8','verified_pass':True,'status':'completed','conclusion':'success','job_id':100+n} for n in range(1,9)],'aggregate':{'job_id':200,'status':'completed','conclusion':'success'}}
assert m.require_complete_source(valid,sha)==44407494538
cases=[]
def rejects(name,edit):
 x=copy.deepcopy(valid);edit(x)
 try:m.require_complete_source(x,sha)
 except SystemExit as e:cases.append({'case':name,'result':'refused','reason':str(e)})
 else:raise AssertionError(name+' wrongly accepted')
rejects('incomplete',lambda x:x.update(complete=False))
rejects('truthy nonboolean',lambda x:x.update(complete=1))
rejects('stale complete head',lambda x:x.update(source_commit='a'*40))
rejects('wrong repository',lambda x:x.update(repository='other/repo'))
rejects('wrong PR',lambda x:x.update(pull_request=2195))
rejects('missing run identity',lambda x:x.pop('run_id'))
rejects('missing dev base identity',lambda x:x.pop('included_dev_base'))
rejects('wrong run URL',lambda x:x.update(url='https://github.com/kevinrhaas/chicago/actions/runs/123'))
rejects('seven source parts',lambda x:x['parts'].pop())
rejects('duplicate part jobs',lambda x:x['parts'][1].update(job_id=101))
rejects('unverified source part',lambda x:x['parts'][4].update(verified_pass=False))
rejects('failed source part',lambda x:x['parts'][4].update(conclusion='failure'))
rejects('queued aggregate',lambda x:x['aggregate'].update(status='queued',conclusion=None))
rejects('dispatch held',lambda x:x.update(dispatch_hold='Unresolved repair'))
m.run=lambda *a: (_ for _ in ()).throw(AssertionError('external command attempted'))
m.gh=m.run
for args,label in [(['helper',sha],'actual pending source'),(['helper',sha,'--validate-checkpoint'],'removed bypass argument')]:
 sys.argv=args
 try:m.main()
 except SystemExit as e:cases.append({'case':label,'result':'refused before external command','reason':str(e)})
 else:raise AssertionError(label+' wrongly accepted')
# Main's live proof checks run against controlled read-only transport; no real gh command.
with tempfile.TemporaryDirectory(prefix='t3654-dispatch-guard-') as td:
 d=pathlib.Path(td);m.SOURCE_SUMMARY=d/'summary.json';m.SOURCE_SUMMARY.write_text(json.dumps(valid));m.LEDGER=d/'ledger.json'
 live={'headSha':sha,'headBranch':m.BRANCH,'status':'completed','conclusion':'success','url':valid['url'],'jobs':[{'databaseId':n,'status':'completed','conclusion':'success'} for n in list(range(101,109))+[200]]}
 state={'local':sha,'remote':sha,'base':base,'dirty':'','live':live}
 def fake_run(args):
  if args==['git','rev-parse','HEAD']:return state['local']
  if args==['git','status','--porcelain','--untracked-files=no']:return state['dirty']
  raise AssertionError(('unexpected command',args))
 def fake_gh(*args):
  if args[0]=='api':return state['base'] if args[1].endswith('/dev') else state['remote']
  if args[:2]==('run','view'):return json.dumps(state['live'])
  raise AssertionError(('unexpected gh mutation',args))
 m.run=fake_run;m.gh=fake_gh;sys.argv=['helper',sha]
 for label,key,bad in [('local head changed','local','a'*40),('remote branch changed','remote','b'*40),('upstream advanced','base','c'*40),('tracked tree dirty','dirty',' M runtime.js'),('live source failed','live',{**live,'conclusion':'failure'}),('live source job missing','live',{**live,'jobs':live['jobs'][:-1]})]:
  prior=state[key];state[key]=bad
  try:m.main()
  except SystemExit as e:cases.append({'case':label,'result':'refused before ledger mutation','reason':str(e)})
  else:raise AssertionError(label+' wrongly accepted')
  assert not m.LEDGER.exists()
  state[key]=prior
 m.LEDGER.write_text(json.dumps({'source_task_commit':sha,'ci_plan':[]}));m.main()
report={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper':str(path),'helper_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'positive_control':'Complete exact-head pure guard and matching simulated live proof accepted; empty test plan only.','negative_controls':cases,'actual_dispatches':0,'actual_external_commands':0,'repository_mutations':0}
p=pathlib.Path('/tmp/t3654-dispatch-source-guard-proof.json');p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'helper_sha256':report['helper_sha256'],'negative_controls':len(cases),'positive_controls':2,'actual_dispatches':0,'proof':str(p)},indent=2))
