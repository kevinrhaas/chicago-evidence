import copy, datetime, hashlib, importlib.util, json, pathlib, sys, tempfile
path=pathlib.Path('/tmp/t3654-dispatch-smoke.py')
spec=importlib.util.spec_from_file_location('dispatch_guard',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sha='6409dda1222e1284e111ab0efde1c471f3284d60';base='c676aa2f4ad6ee8cff0521da6ba8add70d55949c'
valid={'schema':'t3654-hosted-source-gate-v1','complete':True,'source_jobs_complete':True,'source_commit':sha,'included_dev_base':base,'repository':'kevinrhaas/chicago','pull_request':2198,'run_id':44421763389,'url':'https://github.com/kevinrhaas/chicago/actions/runs/44421763389','parts':[{'part':f'{n}/8','verified_pass':True,'status':'completed','conclusion':'success','job_id':100+n} for n in range(1,9)],'aggregate':{'job_id':200,'status':'completed','conclusion':'success'}}
assert m.require_complete_source(valid,sha)==44421763389
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
m.COVERAGE_VERIFIER=pathlib.Path('/tmp/t3654-test-intentionally-absent-verifier')
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

# Separate coverage-union path: fixtures prove the guard, never the actual source coverage.
cov={'schema':'t3654-pre-browser-source-coverage-v1','source_commit':sha,'source_tree':'eeaaefef97d3275b048f308c57c3df5514dbb028','included_dev_base':base,'repository':m.REPO,'pull_request':2198,'hosted_run_id':44421763389,'hosted_run_url':valid['url'],'declared_steps':1379,'declaration_sha256':hashlib.sha256(m.DECLARATIONS.read_bytes()).hexdigest(),'covered_ordinals':list(range(1,1380)),'missing_ordinals':[],'source_check_coverage_complete':True,'ready_for_browser_queue':True,'hosted_gate_required_before_merge':True,'live_dispatch_checks_required':True,'excluded_hosted_timeout_job_ids':[]}
cov.update(verifier_sha256=m.COVERAGE_VERIFIER_SHA256,bindings={'path':str(m.COVERAGE_BINDINGS),'sha256':m.COVERAGE_BINDINGS_SHA256})
assert m.require_complete_prebrowser(cov,sha)==44421763389
for name,edit in [
 ('union wrong head',lambda x:x.update(source_commit='a'*40)),
 ('union unreviewed verifier',lambda x:x.update(verifier_sha256='b'*64)),
 ('union unreviewed bindings',lambda x:x['bindings'].update(sha256='c'*64)),
 ('union wrong repository',lambda x:x.update(repository='other/repo')),
 ('union wrong run URL',lambda x:x.update(hosted_run_url='https://example.com')),
 ('union incomplete',lambda x:x.update(source_check_coverage_complete=False)),
 ('union unready',lambda x:x.update(ready_for_browser_queue=False)),
 ('union nonboolean readiness',lambda x:x.update(ready_for_browser_queue=1)),
 ('union missing declaration',lambda x:x['covered_ordinals'].pop()),
 ('union duplicate declaration',lambda x:x['covered_ordinals'].__setitem__(1,1)),
 ('union missing list nonempty',lambda x:x.update(missing_ordinals=[4])),
 ('union changed declared count',lambda x:x.update(declared_steps=1378)),
 ('union stale declaration hash',lambda x:x.update(declaration_sha256='a'*64)),
 ('union weakens merge requirement',lambda x:x.update(hosted_gate_required_before_merge=False)),
 ('union skips live check',lambda x:x.update(live_dispatch_checks_required=False)),
 ('union unknown timeout allowance',lambda x:x.update(excluded_hosted_timeout_job_ids=[999])),
 ('union former-head timeout allowance',lambda x:x.update(excluded_hosted_timeout_job_ids=[135167297084])),
 ('union duplicate timeout allowance',lambda x:x.update(excluded_hosted_timeout_job_ids=[135167297084]*2)),
]:
 x=copy.deepcopy(cov);edit(x)
 try:m.require_complete_prebrowser(x,sha)
 except SystemExit as e:cases.append({'case':name,'result':'refused','reason':str(e)})
 else:raise AssertionError(name+' wrongly accepted')
live_union={'headSha':sha,'headBranch':m.BRANCH,'status':'in_progress','conclusion':'','url':valid['url'],'jobs':[{'name':f'gate part {n}/8','databaseId':100+n,'status':'completed' if n in(4,5,6,7) else 'queued','conclusion':'success' if n in(4,5,6,7) else ''} for n in range(1,9)]}
m.require_live_source(live_union,cov,'pre-browser',sha)
for name,edit in [
 ('live union wrong head',lambda x:x.update(headSha='a'*40)),
 ('live union missing part',lambda x:x['jobs'].pop()),
 ('live union unknown source failure',lambda x:x['jobs'][0].update(status='completed',conclusion='failure')),
 ('live union cancellation',lambda x:x['jobs'][0].update(status='completed',conclusion='cancelled')),
 ('live union skipped source part',lambda x:x['jobs'][0].update(status='completed',conclusion='skipped')),
 ('live union new timeout is a failure',lambda x:x['jobs'][5].update(databaseId=999,conclusion='failure')),
 ('live union cancelled run',lambda x:x.update(status='completed',conclusion='cancelled')),
 ('live union unexpected job',lambda x:x['jobs'].append({'name':'unknown','databaseId':999,'status':'completed','conclusion':'success'})),
]:
 x=copy.deepcopy(live_union);edit(x)
 try:m.require_live_source(x,cov,'pre-browser',sha)
 except SystemExit as e:cases.append({'case':name,'result':'refused','reason':str(e)})
 else:raise AssertionError(name+' wrongly accepted')
with tempfile.TemporaryDirectory(prefix='t3654-dispatch-union-') as td:
 d=pathlib.Path(td);m.SOURCE_SUMMARY=d/'hosted.json';m.COVERAGE_VERIFIER=d/'verifier.py';m.COVERAGE_VERIFIER.write_text('# fixture: never executed');m.COVERAGE_PROOF=d/'proof.json';m.LEDGER=d/'ledger.json'
 m.COVERAGE_BINDINGS=d/'bindings.json';m.COVERAGE_BINDINGS.write_text('{}')
 m.COVERAGE_VERIFIER_SHA256=hashlib.sha256(m.COVERAGE_VERIFIER.read_bytes()).hexdigest();m.COVERAGE_BINDINGS_SHA256=hashlib.sha256(m.COVERAGE_BINDINGS.read_bytes()).hexdigest()
 cov.update(verifier_sha256=m.COVERAGE_VERIFIER_SHA256,bindings={'path':str(m.COVERAGE_BINDINGS),'sha256':m.COVERAGE_BINDINGS_SHA256})
 pending=copy.deepcopy(valid);pending.update(complete=False,source_jobs_complete=False);m.SOURCE_SUMMARY.write_text(json.dumps(pending));m.COVERAGE_PROOF.write_text(json.dumps(cov))
 fixture={'fresh_proof':copy.deepcopy(cov),'verifier_calls':0,'tree':cov['source_tree'],'verifier_error':False}
 def union_run(args):
  if args==[sys.executable,str(m.COVERAGE_VERIFIER),'--bindings',str(m.COVERAGE_BINDINGS),'--require-complete']:
   fixture['verifier_calls']+=1
   if fixture['verifier_error']:raise m.subprocess.CalledProcessError(1,args,output='missing source ordinals')
   m.COVERAGE_PROOF.write_text(json.dumps(fixture['fresh_proof']));return 'verified fixture'
  if args==['git','rev-parse','HEAD']:return sha
  if args==['git','status','--porcelain','--untracked-files=no']:return ''
  if args==['git','rev-parse','HEAD^{tree}']:return fixture['tree']
  raise AssertionError(('unexpected external command',args))
 def union_gh(*args):
  if args[0]=='api':return base if args[1].endswith('/dev') else sha
  if args[:2]==('run','view'):return json.dumps(live_union)
  raise AssertionError(('unexpected gh mutation',args))
 m.run=union_run;m.gh=union_gh;sys.argv=['helper',sha]
 for label,mutate,restore in [
  ('fresh verifier refusal cannot use saved ready proof',lambda:fixture.update(verifier_error=True),lambda:fixture.update(verifier_error=False)),
  ('fresh proof replaces stale ready boolean',lambda:fixture['fresh_proof'].update(ready_for_browser_queue=False),lambda:fixture['fresh_proof'].update(ready_for_browser_queue=True)),
  ('local tree differs from union',lambda:fixture.update(tree='a'*40),lambda:fixture.update(tree=cov['source_tree'])),
 ]:
  mutate()
  try:m.main()
  except SystemExit as e:cases.append({'case':label,'result':'refused before ledger mutation','reason':str(e)})
  else:raise AssertionError(label+' wrongly accepted')
  assert not m.LEDGER.exists();restore()
 for label,target in [('changed reviewed verifier',m.COVERAGE_VERIFIER),('changed reviewed bindings',m.COVERAGE_BINDINGS)]:
  original=target.read_bytes();target.write_bytes(original+b' changed')
  try:m.main()
  except SystemExit as e:cases.append({'case':label,'result':'refused before verifier or ledger mutation','reason':str(e)})
  else:raise AssertionError(label+' wrongly accepted')
  assert not m.LEDGER.exists();target.write_bytes(original)
 m.LEDGER.write_text(json.dumps({'source_task_commit':sha,'ci_plan':[]}));m.main()
 assert fixture['verifier_calls']==4
 assert json.loads(m.SOURCE_SUMMARY.read_text())['complete'] is False
 assert json.loads(m.LEDGER.read_text())['source_dispatch_authorization']['kind']=='pre-browser'
report={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper':str(path),'helper_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'positive_control':'Both hosted and separate coverage-union guards accepted exact valid fixtures; fresh raw-verifier invocation and live-status checks exercised with empty test plans only. Canonical hosted false remains unchanged on the union path.','negative_controls':cases,'actual_dispatches':0,'actual_external_commands':0,'repository_mutations':0}
p=pathlib.Path('/tmp/t3654-dispatch-source-guard-proof.json');p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'helper_sha256':report['helper_sha256'],'negative_controls':len(cases),'positive_controls':4,'actual_dispatches':0,'proof':str(p)},indent=2))
