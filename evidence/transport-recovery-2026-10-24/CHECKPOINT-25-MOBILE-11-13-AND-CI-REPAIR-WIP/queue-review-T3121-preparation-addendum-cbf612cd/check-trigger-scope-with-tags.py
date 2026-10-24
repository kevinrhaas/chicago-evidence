import yaml,pathlib,subprocess,copy,json,hashlib,time
start=time.monotonic();repo=pathlib.Path('/workspace/chicago-smoke-infra-t3121');path='.github/workflows/chicago-4d-smoke.yml';base='33a99a557bd53aa637cc7173589d610f8a15f14b'
oldbytes=subprocess.check_output(['git','show',base+':'+path],cwd=repo);newbytes=(repo/path).read_bytes();old=yaml.load(oldbytes,Loader=yaml.BaseLoader);new=yaml.load(newbytes,Loader=yaml.BaseLoader)
# Parse actual full workflow; semantic comparison permits exactly the new dev branch filter.
assert old['on']['push']=={'paths':[path]},old['on']['push']
assert new['on']['push']=={'branches':['dev'],'paths':[path]},new['on']['push']
expected=copy.deepcopy(old);expected['on']['push']['branches']=['dev'];assert new==expected,'unexpected workflow semantic change'
assert new['on']['workflow_dispatch']==old['on']['workflow_dispatch']
assert new['on']['workflow_dispatch']['inputs']['viewport']['default']==''
assert new['on']['workflow_dispatch']['inputs']['stage']['default']==''
assert new['jobs']==old['jobs'],'job/step/env/timeout/assertion change'
smoke=new['jobs']['smoke'];assert smoke['timeout-minutes']=='150';assert smoke['runs-on']=='ubuntu-24.04'
assert any(s.get('run')=='bash tools/publish.sh' for s in smoke['steps'])
assert any(s.get('run')=='node tools/smoke_renderer.mjs --published' and s.get('env')=={'SMOKE_VIEWPORT':'${{ inputs.viewport }}','SMOKE_STAGE':'${{ inputs.stage }}'} for s in smoke['steps'])
# Bounded documented push semantics: branch+path AND, with GitHub's tag exception.
# Source: https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore
# "Path filters are not evaluated for pushes of tags."
def fires(config,kind,ref,paths):
 push=config['on']['push']
 if kind=='tag':return 'branches' not in push and 'tags' not in push
 return ('branches' not in push or ref in push['branches']) and any(p in push['paths'] for p in paths)
cases=[('dev-workflow-edit','branch','dev',[path],True,True),('dev-content-only','branch','dev',['chicago/4d/data/structures/hogan_store.json'],False,False),('PR-own-workflow-edit','branch','steward/t3121-dev-only-full-smoke-trigger',[path],True,False),('PR-DEV-merge-carrying-workflow','branch','steward/t3113-1812-balcony-panel',[path,'chicago/4d/docs/LIBERTIES.md'],True,False),('main-workflow-edit','branch','main',[path],True,False),('tag-with-workflow-edit','tag','release-example',[path],True,False),('tag-without-workflow-edit','tag','release-example',['chicago/4d/data/structures/hogan_store.json'],True,False)]
for label,kind,ref,paths,before,after in cases:
 assert fires(old,kind,ref,paths)==before,(label,'old')
 assert fires(new,kind,ref,paths)==after,(label,'new')
proof={'base':base,'path':path,'base_sha256':hashlib.sha256(oldbytes).hexdigest(),'WIP_sha256':hashlib.sha256(newbytes).hexdigest(),'parsed_yaml':'PASS PyYAML BaseLoader preserves on as a string key','only_semantic_change':'on.push.branches=[dev]','all_jobs_steps_env_timeout_and_workflow_dispatch_unchanged':True,'default_both_viewports_all_parts_published_mirror_preserved':True,'trigger_cases':[{'name':n,'ref_kind':k,'ref':r,'paths':p,'before_expected':b,'after_expected':a,'result':'PASS'} for n,k,r,p,b,a in cases],'limits':'Static YAML/content and branch/path AND plus documented tag-push truth table only; no real event dispatched, workflow run, browser, full gate or merge executed. Existing old-head checks remain attached; a later normal push must receive fresh ordinary gate checks.','seconds':time.monotonic()-start}
(pathlib.Path(__file__).parent/'STATIC-WORKFLOW-PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
