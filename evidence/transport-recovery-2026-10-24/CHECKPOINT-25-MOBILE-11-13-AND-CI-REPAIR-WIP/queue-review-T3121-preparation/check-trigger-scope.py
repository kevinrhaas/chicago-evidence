import yaml,pathlib,subprocess,copy,json,hashlib,time
start=time.monotonic();repo=pathlib.Path('/workspace/chicago-smoke-infra-t3121');path='.github/workflows/chicago-4d-smoke.yml';base='de91c45b314a705a6cc2fb9430becb666dfbded6'
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
# These are bounded documented branch+path AND cases, not a replacement GitHub event engine.
def fires(branch,paths):return branch in new['on']['push']['branches'] and any(p in new['on']['push']['paths'] for p in paths)
cases=[('dev-workflow-edit','dev',[path],True),('dev-content-only','dev',['chicago/4d/data/structures/wheeler_house_1812_prairie.json'],False),('PR-own-workflow-edit','steward/t3121-dev-only-full-smoke-trigger',[path],False),('PR-DEV-merge-carrying-workflow','steward/t3113-1812-balcony-panel',[path,'chicago/4d/docs/LIBERTIES.md'],False),('main-workflow-edit','main',[path],False)]
for label,branch,paths,want in cases:assert fires(branch,paths)==want,label
proof={'base':base,'path':path,'base_sha256':hashlib.sha256(oldbytes).hexdigest(),'WIP_sha256':hashlib.sha256(newbytes).hexdigest(),'parsed_yaml':'PASS PyYAML BaseLoader preserves on as a string key','only_semantic_change':'on.push.branches=[dev]','all_jobs_steps_env_timeout_and_workflow_dispatch_unchanged':True,'default_both_viewports_all_parts_published_mirror_preserved':True,'trigger_cases':[{'name':n,'branch':b,'paths':p,'automatic_measurement_expected':w,'result':'PASS'} for n,b,p,w in cases],'limits':'Static YAML/content and branch/path AND truth table only; no real event dispatched, workflow run, browser, full gate or merge executed. Existing old-head checks remain attached; a later normal push must receive fresh ordinary gate checks.','seconds':time.monotonic()-start}
(pathlib.Path(__file__).parent/'STATIC-WORKFLOW-PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
