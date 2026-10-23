"""Root-released fixed normal run IDs; source/testmerge evidence only, never merge approval."""
import argparse,base64,fnmatch,datetime,hashlib,json,os,pathlib,re,subprocess,time
from normal_helpers import NORMAL,need,audit_job,audit_human_jobs,checkout_sha
HERE=pathlib.Path(__file__).resolve().parent
HUMAN_RECORD=None
OUT=None
HEAD=None
BRANCH=None
RUNS={}
EXPECTED_WORKFLOWS={'.github/workflows/chicago-4d-check.yml': (365585053, 'pull_request'), '.github/workflows/chicago-4d-moving-frames.yml': (374947050, 'pull_request'), '.github/workflows/chicago-4d-pr-stuck.yml': (365616743, 'push')}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def main():
 global OUT,HEAD,BRANCH,RUNS,HUMAN_RECORD
 parser=argparse.ArgumentParser();parser.add_argument('--root-binding',required=True,type=pathlib.Path);args=parser.parse_args();binding_bytes=args.root_binding.read_bytes();binding=json.loads(binding_bytes)
 need(binding.get('status')=='ROOT_RELEASED_HORSE_APPLICABLE_NORMAL_THREE_GET' and binding.get('allow_get')is True,'HELD: no actual new source/explicit root GET release')
 need(binding['repository']=='kevinrhaas/chicago' and isinstance(binding['pr'],int) and binding['pr']>0,'Wrong PR/repository binding')
 HEAD=binding['source_head'];BRANCH=binding['source_branch'];SOURCE_TREE=binding['source_tree'];SOURCE_PARENTS=binding['source_parents'];MERGE=binding['testmerge_head'];MERGE_TREE=binding['testmerge_tree'];BASE=binding['reviewed_base']
 need(all(isinstance(x,str)and re.fullmatch('[a-f0-9]{40}',x)for x in [HEAD,SOURCE_TREE,MERGE,MERGE_TREE,BASE]),'Unknown/nonimmutable source/tree/testmerge/base pins')
 need(binding['root_current_base_review_accepted']is True,'HELD: root current-base review not released')
 expected=json.loads((HERE/'EXPECTED-SOURCE-PINS-UNBOUND.json').read_bytes())
 need(all(expected.get(k)==binding.get(k) for k in ['pr','source_head','source_branch','source_tree','source_parents','testmerge_head','testmerge_tree','testmerge_parents','reviewed_base']),'Actual root-reviewed immutable horse source pins differ')
 need(isinstance(SOURCE_PARENTS,list)and len(SOURCE_PARENTS)in[1,2]and all(re.fullmatch('[a-f0-9]{40}',x)for x in SOURCE_PARENTS),'Unknown source parents')
 need(binding['testmerge_parents']==[BASE,HEAD] and MERGE!=HEAD,'Reviewed testmerge parent binding differs')
 need(isinstance(BRANCH,str)and re.fullmatch('[A-Za-z0-9_./-]+',BRANCH),'Unknown source branch')
 need(binding['actual_new_push_verified']is True and binding['actual_postpublish_verified']is True,'Actual new source push/postpublication not yet verified')
 need(binding['collector_sha256']==sha(pathlib.Path(__file__).read_bytes()),'Collector byte pin differs')
 need(binding['normal_helper_sha256']=='0d960da4b79a5264d8b45f83a0788baebf7eb49a0cd5272b2dc493df99459623' and sha((HERE/'normal_helpers.py').read_bytes())==binding['normal_helper_sha256'],'Unchanged strict helper required')
 fixed_pins=json.loads((HERE/'EXPECTED-WORKFLOW-PINS.json').read_bytes());need(binding['workflow_byte_pins']==fixed_pins,'Reviewed workflow byte pins differ')
 HUMAN_RECORD=binding['human_applicability'];need(isinstance(HUMAN_RECORD,dict)and HUMAN_RECORD.get('classification')=='HUMAN_WORKFLOW_NOT_APPLICABLE_TO_HORSE_DIFF' and HUMAN_RECORD.get('status')=='NOT_TRIGGERED_BY_PATH_FILTERS' and HUMAN_RECORD.get('PASS')is None and HUMAN_RECORD.get('run_id')is None and HUMAN_RECORD.get('source_head')==HEAD and HUMAN_RECORD.get('root_classification_explicitly_approved')is True,'Actual next-head human path classification not verified; no inherited133 N/A')
 need(isinstance(binding['human_diff_base'],str)and re.fullmatch('[a-f0-9]{40}',binding['human_diff_base'])and isinstance(binding['human_changed_path_count'],int)and binding['human_changed_path_count']>0,'Unknown actual next-head human diff base/path count')
 human_proof_bytes=(HERE/'HUMANS-PATH-FILTER-SOURCE-READOUT.json').read_bytes();human_proof=json.loads(human_proof_bytes);human_workflow=(HERE/'SOURCE-HUMANS-WORKFLOW.yml').read_bytes()
 need(sha(human_proof_bytes)==HUMAN_RECORD['proof_sha256'] and sha(human_workflow)==HUMAN_RECORD['workflow_sha256']=='62048edeed40b6d5fe8c42feec1a031b7b2581a39ec7215ce0a20b170769c847','Pinned human path-filter proof/workflow bytes differ')
 need(human_proof['source']==HEAD and human_proof['reviewed_diff_base']==binding['human_diff_base'] and len(human_proof['diff_paths'])==binding['human_changed_path_count'] and human_proof['matching_changed_paths']=={},'Human exclusion proof not exact next-head zero-match scope')
 recomputed={path:[pattern for pattern in human_proof['pull_request_path_filters']if fnmatch.fnmatchcase(path,pattern)]for path in human_proof['diff_paths']};need(not any(recomputed.values()),'Human-trigger path exists: missing human workflow is unexplained; HOLD')
 need(HUMAN_RECORD['reviewed_diff_base']==binding['human_diff_base'] and HUMAN_RECORD['changed_path_count']==binding['human_changed_path_count'] and HUMAN_RECORD['matching_changed_paths']=={},'Next-head human record must match actual zero-match proof, never inherited133 metadata')
 rows=binding['normal_runs'];need(len(rows)==3 and {x['path']for x in rows}==set(EXPECTED_WORKFLOWS),'Exactly three applicable gate/moving/report workflows required; no unexplained missing workflow')
 need(all(isinstance(x['run_id'],int)and x['run_id']>0 and (x['workflow_id'],x['event'])==EXPECTED_WORKFLOWS[x['path']]for x in rows)and len({x['run_id']for x in rows})==3,'Unknown/duplicate run IDs or workflow identities')
 RUNS={x['run_id']:(x['path'],x['workflow_id'],x['event'])for x in rows}
 OUT=pathlib.Path('/workspace/shared/T2800-HORSE-PR'+str(binding['pr'])+'-'+HEAD[:10]+'-APPLICABLE-NORMAL3-TERMINAL-GET-owner1');lock=pathlib.Path(str(OUT)+'.lock');lock.mkdir(exist_ok=False);OUT.mkdir(exist_ok=False);(OUT/'ACTUAL-ROOT-BINDING.json').write_bytes(binding_bytes)
 deadline=time.monotonic()+180*60;number=0;audited={};cached={}

 state={'status':'FIXED_NORMAL_RUNS_GET_COLLECTING','started':now(),'pid':os.getpid(),'source':HEAD,'source_branch':BRANCH,'source_tree':SOURCE_TREE,'source_parents':SOURCE_PARENTS,'expected_testmerge':MERGE,'expected_testmerge_tree':MERGE_TREE,'reviewed_base':BASE,'binding_sha256':sha(binding_bytes),'collector_sha256':sha(pathlib.Path(__file__).read_bytes()),'normal_helper_sha256':binding['normal_helper_sha256'],'human_applicability':HUMAN_RECORD,'human_workflow_counted_as_success':False,'run_ids':list(RUNS),'poll_seconds':60,'maximum_minutes':180,'POSTs':0,'automatic_retries':0,'qualification_pass':False,'current_final_head_qualified':False,'scope':'Only actual fresh horse PR applicable gate/moving/report normals, exact fixed run IDs and immutable source/testmerge. Human workflow is NOT_TRIGGERED_BY_PATH_FILTERS only after exact next-head zero-match review, excluded from success counts and never PASS. No world or final merge qualification; no dispatch implied.'}
 save(OUT/'OWNER.json',state);print(json.dumps(state),flush=True)
 def api(label,route,plain=False):
  nonlocal number
  need(time.monotonic()<deadline,'Normal collection180min deadline');number+=1;p=OUT/('%04d-%s'%(number,label));r=subprocess.run(['gh','api','--method','GET','repos/kevinrhaas/chicago/'+route],capture_output=True,timeout=45);p.with_suffix('.stdout').write_bytes(r.stdout);p.with_suffix('.stderr').write_bytes(r.stderr)
  with (OUT/'GET-ATTEMPTS.jsonl').open('a')as f:f.write(json.dumps({'at':now(),'route':route,'exit':r.returncode,'stdout_sha256':sha(r.stdout),'retry':False})+'\n')
  need(r.returncode==0,'GET failed; no retry: '+label+' '+r.stderr.decode(errors='replace')[-400:]);return r.stdout.decode()if plain else json.loads(r.stdout)
 pins={}
 try:
  commit=api('actual-source-commit','git/commits/'+HEAD);need(commit['tree']['sha']==SOURCE_TREE and [x['sha']for x in commit['parents']]==SOURCE_PARENTS,'Actual new source tree/parents differ')
  merge=api('actual-testmerge-commit','git/commits/'+MERGE);need(merge['tree']['sha']==MERGE_TREE and [x['sha']for x in merge['parents']]==[BASE,HEAD],'Actual reviewed testmerge tree/parents differ')
  for path,_,_ in RUNS.values():
   content=api('source-workflow-'+pathlib.Path(path).stem,'contents/'+path+'?ref='+HEAD);need(content['encoding']=='base64','Source workflow encoding differs');pins[path]=sha(base64.b64decode(content['content']));need(pins[path]==fixed_pins[path],'Actual source workflow differs from reviewed byte pin')
  save(OUT/'SOURCE-WORKFLOW-BYTE-PINS.json',pins)
  while time.monotonic()<deadline:
   tick=time.monotonic()
   for ident,(path,wid,event)in RUNS.items():
    if ident in audited:continue
    run=api('run-'+str(ident),'actions/runs/'+str(ident));cached[ident]=run
    need(run['id']==ident and run['head_sha']==HEAD and run['head_branch']==BRANCH and run['event']==event and run['path']==path and run['workflow_id']==wid and run['run_attempt']==1 and run['repository']['full_name']=='kevinrhaas/chicago','Fixed normal run identity drift')
    if run['status']!='completed':continue
    save(OUT/('RUN-'+str(ident)+'.json'),run);jobs=api('jobs-'+str(ident),'actions/runs/'+str(ident)+'/attempts/1/jobs?per_page=100');save(OUT/('RUN-'+str(ident)+'-JOBS.json'),jobs);need(jobs['total_count']==len(jobs['jobs']),'Incomplete jobs')
    logs={}
    for job in jobs['jobs']:
     if job['conclusion']=='skipped':continue
     logs[job['id']]=api('job-'+str(job['id'])+'-log','actions/jobs/'+str(job['id'])+'/logs',True)
    proof={'run_id':ident,'source':HEAD,'workflow_path':path,'event':event,'run_conclusion':run['conclusion'],'PASS':False,'logs':[{'job':i,'sha256':sha(t.encode())}for i,t in logs.items()]}
    try:
     need(run['conclusion']=='success','Actual normal run failed: '+str(run['conclusion']))
     if path.endswith('chicago-4d-humans.yml'):job,detail=audit_human_jobs(jobs['jobs'],run,HEAD)
     else:
      need(len(jobs['jobs'])==1,'Unexpected normal job count');job=jobs['jobs'][0];name,steps=NORMAL[path];detail=audit_job(job,run,HEAD,name,steps)
     text=logs[job['id']];clean=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text);values=re.findall(r'(?m)^\S+Z\s*\[command\].*[/ ]git log -1 --format=%H\s*\n\S+Z\s*([a-f0-9]{40})\s*$',clean);need(len(values)==1,'Ambiguous actual checkout');checkout=checkout_sha(text,values[0]);proof['actual_checkout_sha']=checkout
     commit=api('checkout-'+str(ident),'git/commits/'+checkout);save(OUT/('RUN-'+str(ident)+'-ACTUAL-CHECKOUT-COMMIT.json'),commit);parents=[x['sha']for x in commit['parents']];proof.update(actual_checkout_tree=commit['tree']['sha'],actual_checkout_parents=parents)
     if event=='pull_request':
      need(checkout==MERGE and commit['tree']['sha']==MERGE_TREE and parents==[BASE,HEAD],'PR actual checkout/tree/parents differ from new reviewed testmerge');proof['actual_checkout_base_sha']=next(x for x in parents if x!=HEAD)
     else:need(checkout==HEAD and commit['tree']['sha']==SOURCE_TREE and parents==SOURCE_PARENTS,'Push report must checkout exact new source/tree/parents')
     wf=api('checkout-workflow-'+str(ident),'contents/'+path+'?ref='+checkout);need(wf['encoding']=='base64'and sha(base64.b64decode(wf['content']))==pins[path],'Actual checkout workflow bytes differ from source')
     proof.update(detail);proof.update(PASS=True,workflow_sha256=pins[path],actual_test_output_lines=[x for x in text.splitlines()if re.search(r'\bPASS\b|\bpassed\b|\bFAIL\b|failed|self-tests|self tests|1048|1047',x)][-40:])
    except Exception as error:proof.update(PASS=False,error=str(error),causal_lines=[x for t in logs.values()for x in t.splitlines()if re.search(r'\bFAIL\b|\bfail\b|Error:|exit code',x)][-50:])
    audited[ident]=proof;save(OUT/'AUDITED-JOBS.json',list(audited.values()));print(json.dumps({'at':now(),'new_terminal_run':ident,'proof':proof}),flush=True)
   state.update(at=now(),terminal_collected=len(audited),strict_success=sum(x['PASS']for x in audited.values()),runs=[{k:r.get(k)for k in ['id','status','conclusion']}for r in cached.values()]);save(OUT/'LATEST.json',state);print(json.dumps({k:state[k]for k in ['at','terminal_collected','strict_success','runs']}),flush=True)
   if len(audited)==3:state['status']='APPLICABLE_NORMAL_THREE_TERMINAL_SOURCE_AND_CHECKOUT_EVIDENCE_ONLY';break
   remaining=min(60-(time.monotonic()-tick),deadline-time.monotonic())
   if remaining>0:time.sleep(remaining)
  else:state['status']='BOUNDED180MIN_PARTIAL_NO_RETRY'
 except Exception as error:state.update(status='STOPPED_GET_OR_BINDING_ERROR_NO_RETRY',error=str(error))
 finally:state['ended']=now();save(OUT/'TERMINAL.json',state);save(OUT/'LATEST.json',state);print(json.dumps(state),flush=True)
 return 0 if len(audited)==3 and all(x['PASS']for x in audited.values())else 1
if __name__=='__main__':raise SystemExit(main())
