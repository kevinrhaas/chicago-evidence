import pathlib,json,subprocess,datetime,hashlib,fnmatch,tarfile,argparse,re
HERE=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--root-discovery-release',required=True,type=pathlib.Path);args=parser.parse_args();release=json.loads(args.root_discovery_release.read_bytes())
assert release.get('status')=='ROOT_RELEASED_HORSE_FINITE_NORMAL_DISCOVERY' and release.get('allow_get')is True,'HELD: no concrete current combined-source discovery release'
H=release['source_head'];T=release['source_tree'];P=release['source_parents'];knownbase=release['reviewed_base'];branch=release['source_branch'];repo='/workspace/chicago-waistcoat';i=0
assert all(isinstance(x,str)and re.fullmatch('[a-f0-9]{40}',x)for x in [H,T,knownbase]) and isinstance(P,list)and len(P)in[1,2]and all(re.fullmatch('[a-f0-9]{40}',x)for x in P),'HELD: unbound immutable source pins'
assert release.get('actual_new_push_verified')is True and isinstance(branch,str)and branch,'Actual new pushed source not verified'
D=HERE/('ACTUAL-DISCOVERY-'+H[:10]);D.mkdir(exist_ok=False)


def git(*a,check=True):
 r=subprocess.run(['git','-C',repo,*a],capture_output=True,timeout=45)
 if check:assert r.returncode==0,'Local immutable object unavailable: STOP '+str(a)
 return r
origin_before=git('rev-parse','origin/dev').stdout.decode().strip()
def api(label,route):
 global i
 i+=1;f=D/f'{i:02d}-{label}';f.with_suffix('.request.json').write_text(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'GET','route':route},indent=2)+'\n');r=subprocess.run(['gh','api','--method','GET','repos/kevinrhaas/chicago/'+route],capture_output=True,timeout=45);f.with_suffix('.stdout').write_bytes(r.stdout);f.with_suffix('.stderr').write_bytes(r.stderr);assert r.returncode==0,'GET unavailable; preserve and STOP, no retry '+str(f);return json.loads(r.stdout)
need_pr=release.get('pr');assert isinstance(need_pr,int) and need_pr>0,'HELD: actual horsePR unknown'
pr=api('ACTUAL-HORSE-PR','pulls/'+str(need_pr));assert pr['state']=='open'and pr['head']['sha']==H and pr['head']['ref']==branch and pr['head']['repo']['full_name']=='kevinrhaas/chicago'and pr['base']['ref']=='dev'and pr['auto_merge']is None,'Actual source/PR state differs'
B=api('ACTUAL-CURRENT-DEV','git/ref/heads/dev')['object']['sha'];c=api('ACTUAL-NEW-SOURCE-COMMIT','git/commits/'+H);assert c['tree']['sha']==T and [x['sha']for x in c['parents']]==P
assert api('ACTUAL-NEW-SOURCE-REF','git/ref/heads/'+pr['head']['ref'])['object']['sha']==H
runs=api('ACTUAL-NEW-SOURCE-RUNS','actions/runs?head_sha='+H+'&per_page=100');assert runs['total_count']==len(runs['workflow_runs']),'Incomplete inventory'
known={'.github/workflows/chicago-4d-check.yml':(365585053,'pull_request'),'.github/workflows/chicago-4d-moving-frames.yml':(374947050,'pull_request'),'.github/workflows/chicago-4d-pr-stuck.yml':(365616743,'push')};normal=[];other=[]
for x in runs['workflow_runs']:
 assert x['head_sha']==H,'Old source returned'
 row={k:x.get(k)for k in['id','path','workflow_id','event','run_attempt','head_sha','head_branch','status','conclusion','created_at','html_url']}
 if x['path']in known:
  assert (x['workflow_id'],x['event'])==known[x['path']]and x['head_branch']==pr['head']['ref']and x['run_attempt']==1,'New applicable normal identity differs'
  normal.append(row)
 else:other.append(row)
merge=None
if pr['merge_commit_sha']:
 m=api('ACTUAL-CURRENT-GITHUB-TESTMERGE','git/commits/'+pr['merge_commit_sha']);merge={'head':m['sha'],'tree':m['tree']['sha'],'parents':[x['sha']for x in m['parents']],'matches_current_base_and_new_source':[x['sha']for x in m['parents']]==[B,H]}
# No fetch/ref update: use existing immutable local objects when present.
newbase_inventory=None;local_base=git('cat-file','-e',B+'^{commit}',check=False).returncode==0
if B!=knownbase:
 if local_base:
  raw=git('diff','--name-status',knownbase,B).stdout;(D/'CURRENT-BASE-DELTA-NAME-STATUS.txt').write_bytes(raw);paths=[x.split('\t')[-1]for x in raw.decode().splitlines()];newbase_inventory={'from':knownbase,'to':B,'source':'immutable local Git diff','complete':True,'path_count':len(paths),'paths':paths}
 else:
  comp=api('CURRENT-BASE-FINITE-COMPARE','compare/'+knownbase+'...'+B+'?per_page=100');files=comp.get('files',[]);newbase_inventory={'from':knownbase,'to':B,'source':'one immutable GitHub compare; no fetch','complete':len(files)<300,'GitHub_files_cap':300,'path_count_returned':len(files),'paths':[x['filename']for x in files],'merge_base':comp['merge_base_commit']['sha'],'status':comp['status'],'warning':'300 returned paths would be incomplete; no full base intake performed'if len(files)>=300 else None}
if local_base:M=git('merge-base',B,H).stdout.decode().strip();merge_base_proof='immutable local git merge-base currentDEV/source'
else:
 comp=api('CURRENT-PR-IMMUTABLE-MERGEBASE','compare/'+B+'...'+H+'?per_page=100');M=comp['merge_base_commit']['sha'];merge_base_proof='immutable GitHub compare merge-base commit, independently present in local source ancestry'
assert git('merge-base','--is-ancestor',M,H).returncode==0
paths=git('diff','--name-only',M,H).stdout.decode().splitlines();workflow=git('show',H+':.github/workflows/chicago-4d-humans.yml').stdout;w=workflow.decode();block=w.split('  pull_request:\n    paths:\n',1)[1].split('  push:',1)[0];patterns=[x.strip().removeprefix('- ').strip("'")for x in block.splitlines()if x.strip().startswith('- ')];matches={path:[pat for pat in patterns if fnmatch.fnmatchcase(path,pat)]for path in paths};matches={path:patterns for path,patterns in matches.items()if patterns};(D/'SOURCE-HUMANS-WORKFLOW.yml').write_bytes(workflow)
assert not matches,'Human-trigger path exists: normal4 review required; STOP'
human={'source':H,'source_tree':T,'actual_current_DEV':B,'reviewed_diff_base':M,'immutable_merge_base_proof':merge_base_proof,'diff_paths':paths,'workflow_sha256':hashlib.sha256(workflow).hexdigest(),'pull_request_path_filters':patterns,'matching_changed_paths':matches,'status':'NOT_TRIGGERED_BY_PATH_FILTERS_CANDIDATE_ROOT_REVIEW_PENDING'if not matches else'HUMAN_TRIGGER_MATCH_PRESENT_REQUIRE_APPLICABLE_HUMAN_WORKFLOW','PASS':None,'run_id':None,'no_historical_vehicle_NA_carry':True,'source_edits':0,'ref_edits':0};(D/'HUMANS-PATH-FILTER-SOURCE-READOUT.json').write_text(json.dumps(human,indent=2)+'\n')
assert git('rev-parse','origin/dev').stdout.decode().strip()==origin_before
summary={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_head':H,'source_tree':T,'source_parents':P,'source_branch':pr['head']['ref'],'actual_current_DEV':B,'current_base_beyond_reviewed_source_review_pending':B!=knownbase,'stale_PR_API_base_field':pr['base']['sha'],'mergeable':pr['mergeable'],'mergeable_state':pr['mergeable_state'],'draft':pr['draft'],'actual_GitHub_testmerge':merge,'actual_new_applicable_normals':normal,'other_workflows':other,'normal3_inventory_complete':len(normal)==3 and len({x['path']for x in normal})==3,'human_current_diff_base':M,'human_current_changed_path_count':len(paths),'human_matching_paths':matches,'newbase_changed_path_inventory':newbase_inventory,'shared_origin_dev_unchanged':origin_before,'GitHub_GETs':i,'retries':0,'fetches':0,'ref_edits':0,'full_base_intake':False,'postpublication_binding_pending':True,'collector_started':False,'POSTs':0,'dispatches':0,'mark_ready':False,'merge_attempts':0};(D/'CANDIDATE-BINDING-READOUT.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
