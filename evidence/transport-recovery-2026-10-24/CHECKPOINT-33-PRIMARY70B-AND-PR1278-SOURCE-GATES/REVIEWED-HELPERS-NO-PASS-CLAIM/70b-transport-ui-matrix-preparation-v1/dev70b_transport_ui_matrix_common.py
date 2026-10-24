"""External source-bound matrix contracts. Importing this module launches nothing."""
from __future__ import annotations
import hashlib,json,os,re,socket,subprocess,time
from collections import Counter
from pathlib import Path
ROOT=Path('/workspace/chicago'); APP=ROOT/'chicago/4d'; SITE=ROOT/'site/4d'
LOG=Path('/workspace/.cloud-setup/logs/transport-recovery')
BASE='70bcc4366a455a15f1e54e3edfce50c046c0ddce'
TREE='9fa9511eabff9a0e42da32410edf09a8e3608889'; APP_TREE='da9f71f6749ebf52e09ad51f673a9e4debbf4478'
SUPERVISOR=Path('/workspace/.cloud-setup/transport-supervise.py')
SUPERVISOR_SHA='a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c'
SOURCE_BINDING=LOG/'70b-transport-ui-preflight-source-binding.json'
EXPECTED_PREFLIGHT_PREFIX=LOG/'70b-transport-ui-full-preflight-before-commit'
EXPECTED_PREFLIGHT_COMMAND=['env','BASE='+BASE,'bash','tools/preflight.sh']
SMOKE_SHA='4586e7101000910cde7743048b72b72b3b04f7896417f5fe1a97af14e1e941bd'
FOCUSED_HELPER_SHA='6468cda54428199b8c5b6b627b326a35215d993062183040a6a779e692ffcf06'
LEGS=[('mobile',s) for s in ['1-2','3-4','5-6','7-8','9-10','11-12','13','14','15']]+[('desktop',str(n)) for n in range(1,16)]
def need(condition,message):
 if not condition: raise RuntimeError(message)
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def digest(path):
 with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def value_hash(value):return hashlib.sha256(canonical(value)).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def save(path,value):
 path=Path(path);tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(path)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},stderr=subprocess.PIPE).decode().strip()
def timeout_for(viewport,stage):
 if viewport=='desktop' and stage=='13':return 10800
 if stage in ['13','14']:return 3600
 if viewport=='desktop' and stage in ['9','10','11','12']:return 3600
 return 1800
def timeout_reason(viewport,stage):
 if viewport=='desktop' and stage=='13':return 'Accepted actual desktop13 body7767s; explicit10800s bound, no source assertion change.'
 if viewport=='desktop' and stage=='14':return 'Accepted actual desktop14 body3331s; old local1800s attempt timed out. Explicit3600s bound.'
 if viewport=='mobile' and stage in ['13','14']:return 'Requested3600s bounds; mobile13 actual prior1356.9s, preserve long-readiness behavior.'
 if viewport=='desktop' and stage in ['9','10','11','12']:return 'Accepted combined desktop9-12 cost2216s; individual distribution unknown, allow3600s each without truncating based on guess.'
 return 'Prior matching mobile groups and containing desktop groups/part15 completed below1373s;1800s is an operational bound, not a600s budget claim.'
def parts(stage):
 v=list(map(int,stage.split('-')));return list(range(v[0],v[-1]+1))
def manifest():
 rows=[]
 for p in sorted(SITE.rglob('*')):
  need(not p.is_symlink(),'Published symlink unsupported: '+str(p))
  if p.is_file():rows.append({'path':p.relative_to(SITE).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)})
 need(rows,'Published mirror is empty');return sorted(rows,key=lambda r:r['path'])

def source_snapshot(head,published_digest=None):
 need(re.fullmatch('[0-9a-f]{40}',head) is not None,'Use complete expected commit SHA')
 need(git('rev-parse','HEAD')==head,'HEAD moved')
 need(subprocess.run(['git','merge-base','--is-ancestor',BASE,head],cwd=ROOT,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True).returncode==0,'Expected head does not contain the pinned accepted70b intake')
 need(git('rev-parse','HEAD^{tree}')==TREE,'Candidate tree changed')
 need(git('rev-parse','HEAD:chicago/4d')==APP_TREE,'App subtree changed')
 need(git('diff','--name-only','HEAD')=='' and git('diff','--name-only')=='' and git('diff','--cached','--name-only')=='','Tracked index/worktree is dirty')
 need(git('ls-files','--others','--exclude-standard')=='','Untracked source exists; inspect it before continuing')
 need(digest(APP/'tools/smoke_renderer.mjs')==SMOKE_SHA,'Canonical smoke source changed')
 build=read(SITE/'build.json');need(build['version']==git('rev-parse','--short',head),'Published build does not match expectedHEAD')
 binding=read(SOURCE_BINDING);need(binding['candidate_tree']==TREE and binding['app_subtree']==APP_TREE and binding['incoming_dev']==BASE,'Preflight source binding differs')
 rows=manifest();mh=value_hash(rows)
 if published_digest is not None:need(mh==published_digest,'Published mirror bytes changed')
 return {'head':head,'tree':TREE,'app_subtree':APP_TREE,'accepted_base':BASE,'published_build':build,'published_manifest_digest':mh,'published_files':len(rows),'published_bytes':sum(r['bytes'] for r in rows),'index_sha256':digest(ROOT/'.git/index'),'smoke_sha256':SMOKE_SHA,'checked_unix':time.time()},rows

def receipt(prefix,tool):
 prefix=Path(prefix);r=read(str(prefix)+'.result.json');c=read(str(prefix)+'.cleanup.json')
 need(r['returncode']==0 and r['timed_out'] is False,'Failed or timed-out '+tool+' receipt')
 need(r.get('cwd')==str(APP),'Wrong cwd in '+tool+' receipt')
 need(any(Path(x).name==tool for x in r.get('command',[])),'Wrong command in '+tool+' receipt')
 need(c['cleanup_complete'] is True and c['remaining_owned_children']==[],'Incomplete owned cleanup for '+tool)
 return {'prefix':str(prefix),'result_sha256':digest(str(prefix)+'.result.json'),'cleanup_sha256':digest(str(prefix)+'.cleanup.json'),'seconds':r['seconds']}

def prerequisites(config):
 need('CHICAGO_TICKETS_DIR' not in os.environ,'Unset CHICAGO_TICKETS_DIR')
 need(Path(config['preflight_prefix']).resolve()==EXPECTED_PREFLIGHT_PREFIX,'Use the actual new70b full-preflight prefix')
 for key in ['publish_prefix','focused_prefix','focused_output']:
  target=Path(config[key]).resolve();need(target.parent==LOG and target.name.startswith('70b-transport-ui-'),'Use fresh actual70b prerequisite prefixes/output, never oldC4 receipts')
 need(digest(SUPERVISOR)==SUPERVISOR_SHA,'Reviewed supervisor changed before launch')
 results={'preflight':receipt(config['preflight_prefix'],'preflight.sh'),'publish':receipt(config['publish_prefix'],'publish.sh')}
 binding=read(SOURCE_BINDING);actual_preflight=read(str(EXPECTED_PREFLIGHT_PREFIX)+'.result.json')
 need(binding.get('preflight_prefix')==str(EXPECTED_PREFLIGHT_PREFIX) and binding.get('expected_preflight_command')==EXPECTED_PREFLIGHT_COMMAND and actual_preflight.get('command')==EXPECTED_PREFLIGHT_COMMAND,'The actual70b preflight must explicitly pin BASE in the exact root-bound command')
 # Focused layout proof covers all rows, unlike canonical matrix's Settings-only layout audit.
 focus=read(Path(config['focused_output'])/'FOCUSED-CURRENT-NOTES-RESULT.json')
 need(focus['expected_head']==config['head'] and focus['staged_tree']==TREE,'Focused proof belongs to another source')
 need(focus['result']=='PASS' and focus['final_bindings_verified'] is True and focus.get('final_viewport_errors_verified') is True,'Focused wrapping proof not complete/green')
 need(all(focus['components'][k]['result']=='PASS' for k in ['CanonicalNewsFlow','CurrentNotesPresentation']),'Focused component failed')
 need(len(focus['viewports'])==2 and all(v['errors']==[] and not v.get('cleanup_error') for v in focus['viewports']),'Focused errors/cleanup differ')
 need(sorted(v['label'] for v in focus['viewports'])==['desktop1280x800','mobile390x780'],'Focused required viewport identities differ')
 fp=Path(config['focused_prefix']);fr=read(str(fp)+'.result.json');fc=read(str(fp)+'.cleanup.json')
 need(fr['returncode']==0 and not fr['timed_out'] and fc['cleanup_complete'] and fc['remaining_owned_children']==[],'Focused supervisor failed')
 need('--output' in fr['command'] and fr['command'][fr['command'].index('--output')+1]==config['focused_output'],'Focused output/command mismatch')
 need('--expected-head' in fr['command'] and fr['command'][fr['command'].index('--expected-head')+1]==config['head'],'Focused expectedHEAD mismatch')
 for flag,key in [('--preflight-prefix','preflight_prefix'),('--publish-prefix','publish_prefix')]:
  need(flag in fr['command'] and fr['command'][fr['command'].index(flag)+1]==config[key],'Focused command names another prerequisite: '+flag)
  need(focus.get(key)==config[key],'Focused report names another prerequisite: '+key)
 for tool,result_field,cleanup_field in [('preflight','preflight_receipt_sha256','preflight_cleanup_sha256'),('publish','publisher_receipt_sha256','publisher_cleanup_sha256')]:
  need(focus.get(result_field)==results[tool]['result_sha256'] and focus.get(cleanup_field)==results[tool]['cleanup_sha256'],'Focused proof does not bind the same actual '+tool+' result/cleanup receipts')
 focused_scripts=[Path(x) for x in fr['command'] if str(x).endswith('.mjs')];need(len(focused_scripts)==1 and digest(focused_scripts[0])==FOCUSED_HELPER_SHA,'Focused receipt did not execute reviewed guarded v2 helper')
 fb=Path(config['focused_output'])/'PUBLISHED-MANIFEST-BEFORE.json';fa=Path(config['focused_output'])/'PUBLISHED-MANIFEST-AFTER.json'
 raw_focused_before=read(fb);raw_focused_after=read(fa)
 node_digest=hashlib.sha256(json.dumps(raw_focused_before,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
 need(node_digest==focus['published_manifest_digest'] and len(raw_focused_before)==focus['published_files'],'Focused manifest does not match the reviewed report digest/count')
 focused_before=sorted(raw_focused_before,key=lambda r:r['path']);focused_after=sorted(raw_focused_after,key=lambda r:r['path'])
 need(focused_before==focused_after and focused_after,'Focused published manifests changed or empty')
 need(len({r['path'] for r in focused_after})==len(focused_after),'Duplicate focused manifest paths')
 results['focused']={'prefix':str(fp),'output':config['focused_output'],'report_sha256':digest(Path(config['focused_output'])/'FOCUSED-CURRENT-NOTES-RESULT.json'),'result_sha256':digest(str(fp)+'.result.json'),'cleanup_sha256':digest(str(fp)+'.cleanup.json'),'manifest_before_file_sha256':digest(fb),'manifest_after_file_sha256':digest(fa),'published_manifest_digest':value_hash(focused_after),'reported_node_manifest_digest':node_digest,'published_files':len(focused_after)}
 return results

def busy_processes():
 found=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit() or int(p.name)==os.getpid():continue
  try:
   stat=(p/'stat').read_text().rsplit(')',1)[1].split();argv=(p/'cmdline').read_bytes().split(b'\0');argv=[x.decode(errors='replace') for x in argv if x]
   if stat[0]=='Z' or not argv:continue
   names=[Path(x).name for x in argv[:5]];exe=names[0]
   browser=exe in ['chromium','chromium-browser','chrome','chrome-headless-shell','headless_shell']
   smoke='smoke_renderer.mjs' in names
   driver=any(x in ['de91-integrated-smoke.py','de91-integrated-smoke-continuation.py','resume-transport-smoke.py','resume-transport-smoke-after-restart.py','transport-smoke-batch.sh','latest-dev-transport-smoke-batch.sh','resume-transport-smoke-deferred-images.py','abb1_transport_ui_matrix_driver.py','dev6ab_transport_ui_matrix_driver.py','dev70b_transport_ui_matrix_driver.py'] for x in names)
   focus=any('focused' in x and ('wrapping' in x or 'current-notes' in x) and x.endswith('.mjs') for x in names)
   if browser or smoke or driver or focus:found.append({'pid':int(p.name),'executable':exe,'category':'browser' if browser else 'smoke' if smoke else 'continuation' if driver else 'focused helper'})
  except (OSError,ValueError,IndexError):pass
 return found

def child_command(viewport,stage):
 return ['env','SMOKE_VIEWPORT='+viewport,'SMOKE_STAGE='+stage,'SMOKE_TIMING=1','SMOKE_YEAR=1835','SMOKE_TARGET=published','SMOKE_ROOT='+str(SITE),'SMOKE_ENTRY=/walk/','SMOKE_PORT=4187','node','tools/smoke_renderer.mjs','--published']

def parse_transcript(text,viewport,stage):
 label='mobile 390x780' if viewport=='mobile' else 'desktop 1280x800'
 counts=re.findall(r'^(\d+) passed, (\d+) failed\s*$',text,re.M);need(len(counts)==1,'Missing/duplicate canonical summary')
 passed,failed=map(int,counts[0]);need(passed>0 and failed==0,'Smoke assertions failed or none ran')
 sections=re.findall(r'^(\d+) staged-section check\(s\).*$',text,re.M);need(len(sections)==1 and int(sections[0])>0,'No actual staged checks')
 need(text.rstrip().endswith('SMOKE PASS'),'Missing completed SMOKE PASS footer')
 need('PUBLISHED mirror (compressed assets, visitor layout)' in text,'Wrong published target')
 need('viewports filtered to "'+viewport+'"' in text and 'stages filtered to "'+stage+'" of 15' in text,'Wrong stage/viewport filters')
 need(re.findall(r'^(mobile 390x780|desktop 1280x800):\s*$',text,re.M)==[label],'Unexpected/missing viewport body')
 for name in ['the suite body ran to completion','zero page errors']:
  need(re.search(r'^\s*pass\s+(?:\[\d+:\d+\]\s+)?'+re.escape(label+': '+name)+r'\s*$',text,re.M) is not None,'Missing actual pass: '+name)
 need(not re.search(r'^\s*FAIL\s+',text,re.M),'Actual FAIL line present')
 timing=re.findall(r'^(\d+) m (\d+) s for stage '+re.escape(stage)+' at '+viewport+r' —',text,re.M);need(len(timing)==1,'Missing actual stage timing footer')
 return {'passed':passed,'failed':failed,'staged_checks':int(sections[0]),'body_seconds':int(timing[0][0])*60+int(timing[0][1]),'zero_page_errors':True,'body_completed':True}

def validate_leg(prefix,viewport,stage):
 prefix=Path(prefix);r=read(str(prefix)+'.result.json');c=read(str(prefix)+'.cleanup.json');text=Path(str(prefix)+'.log').read_text(errors='replace')
 need(r['returncode']==0 and r['timed_out'] is False,'Command failed/timed out')
 need(r.get('cwd')==str(APP) and r['command']==child_command(viewport,stage),'Actual leg command/cwd mismatch')
 bound=timeout_for(viewport,stage);need(r['requested_timeout_seconds']==bound and r['effective_timeout_seconds']==bound,'Timeout differs from reviewed bound')
 need(c['cleanup_complete'] is True and c['remaining_owned_children']==[],'Owned descendants remain')
 p=parse_transcript(text,viewport,stage);elapsed=r.get('command_seconds',r['seconds'])
 return {**p,'command_seconds':elapsed,'wrapper_seconds':r['seconds'],'resource_pause_seconds':r.get('resource_pause_seconds',0),'timeout_seconds':bound,'foreground_budget_seconds':600,'fits_foreground_budget':elapsed<=600 and r['seconds']<=600 and p['body_seconds']<=600,'budget_note':'Functional SMOKE PASS is distinct from fitting the600s foreground budget. Longer actual runs are never called budgetPASS.','receipt_hashes':{suffix:digest(str(prefix)+suffix) for suffix in ['.log','.result.json','.cleanup.json']}}

def verify_complete(run_dir,head):
 run_dir=Path(run_dir);state=read(run_dir/'MATRIX-STATE.json');need(state['config']['head']==head,'Verifier expectedHEAD differs');need(state['fresh_results_only'] is True and state.get('zero_inherited_results') is True and state.get('accepted_base')==BASE,'Inherited results or changed accepted-base state forbidden')
 need(state['planned_legs']==[list(x) for x in LEGS],'Leg plan differs from24specification');need(len(state['completed'])==24,'Not all24legs completed')
 need(not state.get('active'),'An active leg remains recorded')
 for name,want in state['tool_hashes'].items():
  tool=SUPERVISOR if name==SUPERVISOR.name else Path(__file__).with_name(name);need(digest(tool)==want,'Reviewed helper/supervisor bytes changed before final verification')
 need([(r['viewport'],r['stage']) for r in state['completed']]==LEGS,'Missing/duplicate/reordered legs')
 prereq=prerequisites(state['config']);need(prereq==state['prerequisites'],'Prerequisite receipt changed')
 before=read(run_dir/'PUBLISHED-MANIFEST-BEFORE.json');after=read(run_dir/'PUBLISHED-MANIFEST-AFTER.json');need(before==after,'Global published manifests differ');mh=value_hash(before)
 focused_manifest=read(Path(state['config']['focused_output'])/'PUBLISHED-MANIFEST-AFTER.json');need(sorted(focused_manifest,key=lambda r:r['path'])==before,'Focused and matrix mirror snapshots differ')
 need(mh==prereq['focused']['published_manifest_digest'],'Final matrix digest differs from the completed focused proof')
 rows=[];coverage={v:Counter() for v in ['mobile','desktop']}
 for saved,(viewport,stage) in zip(state['completed'],LEGS):
  prefix=run_dir/f'70b-transport-ui-matrix-{viewport}-{stage}';need(saved['prefix']==str(prefix),'Leg evidence points outside this fresh run')
  proof=validate_leg(prefix,viewport,stage);need(proof==saved['proof'],'Leg receipt/transcript changed')
  for suffix in ['.binding.before.json','.binding.after.json']:
   bd=read(str(prefix)+suffix);need(bd['head']==head and bd['tree']==TREE and bd['app_subtree']==APP_TREE and bd.get('accepted_base')==BASE and bd['published_manifest_digest']==mh,'Per-leg source/mirror binding mismatch')
   need(digest(str(prefix)+suffix)==saved['binding_hashes'][suffix],'Per-leg binding changed')
  need(saved['outer_returncode']==0,'Supervisor outer exit was not successful')
  coverage[viewport].update(parts(stage));rows.append({'viewport':viewport,'stage':stage,**proof})
 for viewport,c in coverage.items():need(c==Counter(range(1,16)),'Coverage not exactly1..15once: '+viewport)
 snapshot,current=source_snapshot(head,mh);need(current==after,'Current mirror differs after matrix')
 return {'result':'PASS','scope':'Fresh all15parts at both published viewports, source-bound24legs; no inherited results. Not production promotion or photographic acceptance.','head':head,'tree':TREE,'app_subtree':APP_TREE,'accepted_base':BASE,'leg_count':24,'coverage':{v:dict(c) for v,c in coverage.items()},'staged_totals':{v:sum(r['staged_checks'] for r in rows if r['viewport']==v) for v in coverage},'passed_totals_with_repeated_always_on':{v:sum(r['passed'] for r in rows if r['viewport']==v) for v in coverage},'actual_over600s_legs':[{'viewport':r['viewport'],'stage':r['stage'],'command_seconds':r['command_seconds']} for r in rows if not r['fits_foreground_budget']],'final_source':snapshot,'published_manifest_digest':mh,'verified_unix':time.time()}
