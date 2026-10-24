#!/usr/bin/env python3
"""Prepared endgame only. ROOT executes explicitly; no import-time operations."""
import argparse, hashlib, importlib.util, json, os, re, subprocess, sys, time
from pathlib import Path

ROOT=Path('/workspace/chicago'); APP=ROOT/'chicago/4d'
LOG=Path('/workspace/.cloud-setup/logs/transport-recovery')
H='1b70cdbd85b18c124870d6274d2ffffd4ca5979b'
B='70bcc4366a455a15f1e54e3edfce50c046c0ddce'
TESTED_Q='a2963c13cbd1d270aaa84987da8a5b9955ab6d79'
TREE='9fa9511eabff9a0e42da32410edf09a8e3608889'
APP_TREE='da9f71f6749ebf52e09ad51f673a9e4debbf4478'
MATRIX=LOG/'70b-transport-ui-matrix-run1'
PREP=LOG/'70b-transport-ui-matrix-preparation-v1'
TOOL_HASHES={
 'dev70b_transport_ui_matrix_common.py':'6e42184a1f4f2bf6cbc3a3628d73c22460fe7c8ddcc10a37ce3a63187316276c',
 'dev70b_transport_ui_matrix_driver.py':'d4033c207d33d211a3fa3b25e47e07e2209d6c83e017ed2f1ae092b418e012c7',
 'dev70b_transport_ui_matrix_verify.py':'19bdcbb2ab3bc53501221456ee16d47120b7791dd148f0084d6bb050c13c1a4f'}
HTTP=LOG/'70b-transport-ui-post-dev-http-preparation-v2/verify-post-dev-selected-bytes-h3-v2.py'
HTTP_SHA='030ecc16be875793014427186eb007af50cea7f4af8de268b8924e1c5bd2e93b'
PIPELINE=Path('/workspace/.cloud-setup/70b-browser-pipeline-attempt2.py')
PIPELINE_SHA='456069bcd238a51eea5e521eef3fa325543d046f1ddc258c617f4ac31b16d633'
PIPELINE_PREFIX=LOG/'70b-transport-ui-browser-pipeline-attempt2'
PIPELINE_STATE=LOG/'70b-browser-pipeline-attempt2-state.json'
DRIVER_PREFIX=LOG/'70b-transport-ui-matrix-run1-driver'
VERIFIER_PREFIX=LOG/'70b-transport-ui-independent-final-24-verifier'
INDEPENDENT_PROOF=LOG/'70b-transport-ui-independent-final-24.json'
FOCUS_PREFIX=LOG/'70b-transport-ui-focused-wrapping-attempt2'
FOCUS_OUTPUT=LOG/'70b-transport-ui-focused-wrapping-attempt2-output'
CI_BINDING_SHA='e5cd244d57231ba52ac973ea52e80bf8ef833912395508992e6bbf1e8b4ade74'
SOURCE_BINDING_SHA='a22695bd181321df8427de336ebd4595500c1b017a0bc630f9f07c57f2432def'
PREFLIGHT_RESULT_SHA='bf469e30542eb904bb182ce45e664817679bbcb7f870354144b85648c2763dcf'
PREFLIGHT_CLEANUP_SHA='5f8df5c64844fbe7044d4726e54c27411a6145ced3c08dd0a5514638b7d2bf91'
EXPECTED_PREFLIGHT_COMMAND=['env','BASE='+B,'bash','tools/preflight.sh']
CI_RUNS={40138225825,40138225852}
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'}
env.pop('GH_REST_MERGE_BLIND',None);env.pop('CHICAGO_TICKETS_DIR',None);env.pop('GH_REPO',None);env['GH_HOST']='github.com'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def save(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def run(cmd,cwd=ROOT):return subprocess.check_output(cmd,cwd=cwd,env=env,stderr=subprocess.PIPE)
def git(*a):return run(['git',*a]).decode().strip()
def blob(c,p):return run(['git','show',c+':'+p])
def ref(p):p=Path(p).resolve();return {'path':str(p),'sha256':sha(p.read_bytes())}
def bound(p,digest):
 need(re.fullmatch('[0-9a-f]{64}',digest),'Full artifact SHA256 required')
 need(sha(Path(p).read_bytes())==digest,'Input artifact changed: '+str(p));return read(p)
def receipt(prefix,tool,required_args=()):
 r=read(str(prefix)+'.result.json');c=read(str(prefix)+'.cleanup.json')
 need(r.get('returncode')==0 and r.get('timed_out') is False,'Actual outer result is not successful: '+str(prefix))
 need(c.get('cleanup_complete') is True and c.get('remaining_owned_children')==[],'Actual cleanup is incomplete: '+str(prefix))
 command=r.get('command',[]);need(any(Path(str(v)).name==tool for v in command),'Wrong actual command receipt: '+str(prefix))
 for flag,value in required_args:
  need(flag in command and command[command.index(flag)+1]==str(value),'Actual command argument differs: '+flag)
 return {'result':ref(str(prefix)+'.result.json'),'cleanup':ref(str(prefix)+'.cleanup.json')}
def semantic_proof(p):
 d=json.loads(json.dumps(p));d.pop('verified_unix',None);d['final_source'].pop('checked_unix',None);return d
def main():
 need(re.fullmatch('[0-9a-f]{64}',CI_BINDING_SHA),'Final actual successful H3 CI binding is missing or malformed; no execution eligible')
 q=argparse.ArgumentParser(description=__doc__)
 q.add_argument('--execute-after-full-matrix',action='store_true')
 for name in ['out','independent-proof','independent-proof-sha256','verifier-prefix','driver-prefix','owned-lease-sha','lease-owner','lease-acquisition-log','lease-acquisition-sha256','ci-binding','ci-binding-sha256','accepted-source-binding','accepted-source-binding-sha256','evidence-url']:
  q.add_argument('--'+name,required=True)
 a=q.parse_args();need(a.execute_after_full_matrix,'Preparation only; ROOT must explicitly execute after full matrix')
 need(re.fullmatch('[0-9a-f]{40}',a.owned_lease_sha),'Full own lease SHA required')
 out=Path(a.out).resolve();need(out.parent==LOG and not out.exists(),'Use a NEW direct child directory of transport-recovery')
 need(Path(a.independent_proof).resolve()!=MATRIX/'FINAL-24-LEG-VERIFICATION.json','Independent proof must be a separate actual verifier output')
 need(a.lease_owner.strip() and len(a.lease_owner)>=8,'Supply actual recognizable owner string from own acquired marker')
 need(re.fullmatch(r'https://github\.com/kevinrhaas/chicago-evidence/tree/[0-9a-f]{40}/evidence/[A-Za-z0-9_./-]+',a.evidence_url),'ROOT must supply its actual pushed final proof checkpoint as a full-commit-pinned evidence URL')
 need(re.fullmatch(r'(?:https://(?:[^/@]+@)?github\.com/|git@github\.com:|ssh://git@github\.com/)kevinrhaas/chicago(?:\.git)?',git('remote','get-url','origin')),'Primary origin is not the named Chicago repository')
 acquisition=Path(a.lease_acquisition_log).read_bytes();need(sha(acquisition)==a.lease_acquisition_sha256 and b'PR #1279: lap/pr-1279 taken' in acquisition,'Actual successful own lap acquisition log required')
 need(sha(HTTP.read_bytes())==HTTP_SHA,'Reviewed future H3 HTTP verifier changed')
 need(sha(PIPELINE.read_bytes())==PIPELINE_SHA,'Actual reviewed enclosing browser pipeline changed')
 need(Path(a.driver_prefix).resolve()==DRIVER_PREFIX and Path(a.verifier_prefix).resolve()==VERIFIER_PREFIX and Path(a.independent_proof).resolve()==INDEPENDENT_PROOF,'Use only actual H3 run1 pipeline driver/verifier/proof paths')
 pipeline_receipts=receipt(PIPELINE_PREFIX,PIPELINE.name)
 pipeline_result=read(str(PIPELINE_PREFIX)+'.result.json');need(str(PIPELINE) in pipeline_result.get('command',[]),'Enclosing receipt did not run the actual reviewed pipeline path')
 pipeline_state=read(PIPELINE_STATE);need(pipeline_state.get('phase')=='PASS: actual focused/full24/independent verifier and all owned cleanup CLOSED; DEV merge still pending' and pipeline_state.get('head')==H and pipeline_state.get('run_dir')==str(MATRIX) and pipeline_state.get('driver_prefix')==str(DRIVER_PREFIX) and pipeline_state.get('verifier_prefix')==str(VERIFIER_PREFIX) and pipeline_state.get('independent_proof')==str(INDEPENDENT_PROOF) and pipeline_state.get('independent_proof_sha256')==a.independent_proof_sha256,'Actual enclosing pipeline has not closed successfully on matching full24/independent evidence')
 for name,digest in TOOL_HASHES.items():need(sha((PREP/name).read_bytes())==digest,'Reviewed matrix helper changed: '+name)
 sys.path.insert(0,str(PREP));spec=importlib.util.spec_from_file_location('dev70b_transport_ui_matrix_common',PREP/'dev70b_transport_ui_matrix_common.py');common=importlib.util.module_from_spec(spec);spec.loader.exec_module(common)
 need(not common.busy_processes(),'An actual matrix/browser is active; no endgame while it runs')
 actual=common.verify_complete(MATRIX,H) # hashes all receipts/manifests; never launches a test/browser
 independent=bound(a.independent_proof,a.independent_proof_sha256)
 need(semantic_proof(actual)==semantic_proof(independent),'Independent complete proof differs from current re-read')
 internal=read(MATRIX/'FINAL-24-LEG-VERIFICATION.json');need(semantic_proof(internal)==semantic_proof(independent),'Driver final proof differs from independent verification')
 state=read(MATRIX/'MATRIX-STATE.json');need(state.get('config',{}).get('focused_prefix')==str(FOCUS_PREFIX) and state.get('config',{}).get('focused_output')==str(FOCUS_OUTPUT),'Matrix must bind successful attempt2 focused receipts; failed attempt1 cannot qualify');need(state.get('zero_inherited_results') is True and state.get('status')=='PASS: fresh all15parts/bothviewports, final verification complete' and state.get('verification_sha256')==sha((MATRIX/'FINAL-24-LEG-VERIFICATION.json').read_bytes()),'Driver did not finish its exact fresh24 final state')
 driver_receipts=receipt(a.driver_prefix,'dev70b_transport_ui_matrix_driver.py',[('--head',H),('--out',MATRIX)])
 verifier_receipts=receipt(a.verifier_prefix,'dev70b_transport_ui_matrix_verify.py',[('--head',H),('--run-dir',MATRIX),('--receipt',a.independent_proof)])
 need(a.ci_binding_sha256==CI_BINDING_SHA and a.accepted_source_binding_sha256==SOURCE_BINDING_SHA,'Use the exact independently audited actual H3 CI/source artifacts')
 ci=bound(a.ci_binding,a.ci_binding_sha256)
 need(ci.get('schema')=='chicago-pr1279-h3-ordinary-ci-safe-proof-v1' and ci.get('repository')=='kevinrhaas/chicago','Wrong actual final CI safeproof schema/repository')
 need((ci.get('PR'),ci.get('H'),ci.get('tested_Q'),ci.get('tested_base'),ci.get('tree'),ci.get('APP'))==(1279,H,TESTED_Q,B,TREE,APP_TREE),'Actual H3 CI source/base/Q/tree/APP binding differs')
 ci_objects=ci.get('native_git_objects',{});need(set(ci_objects)=={H,TESTED_Q},'Final safeproof lacks exact native H3/Q objects')
 need(all(ci_objects[c].get('tree')==TREE and ci_objects[c].get('APP')==APP_TREE for c in [H,TESTED_Q]) and set(ci_objects[TESTED_Q].get('parents',[]))=={B,H} and B in ci_objects[H].get('parents',[]),'Safe native object source trees/accepted parents differ')
 ci_runs=ci.get('runs',[]);need(len(ci_runs)==2 and {r.get('run_id') for r in ci_runs}==CI_RUNS and {r.get('kind') for r in ci_runs}=={'gate','moving'},'Actual gate/moving run identity differs')
 need(all(r.get('head_sha')==H and r.get('event')=='pull_request' and r.get('conclusion')=='success' and r.get('all_actual_steps_success') is True and r.get('actual_stdout_available') is True and r.get('actual_stdout_checkout_Q')==TESTED_Q and r.get('official_job_log_requests')==1 for r in ci_runs),'Actual successful native jobs/stdout source proof is incomplete')
 need({(r['kind'],r['run_id'],r.get('job_id')) for r in ci_runs}=={('gate',40138225825,121004216204),('moving',40138225852,121004216043)},'Actual final H3 run/job pair differs')
 gate_stdout=ci.get('gate_stdout',{});moving_stdout=ci.get('moving_stdout',{})
 need(gate_stdout.get('bytes')==1853833 and gate_stdout.get('raw_sha256')=='5dd71f09e93845442da2a141a01da983257aa10844bdcd1d922183caa7e32707' and gate_stdout.get('actual_CHECK_PASS_steps')==1066 and gate_stdout.get('actual_self_tests')==384,'Actual gate stdout/count proof differs')
 need(moving_stdout.get('bytes')==84791 and moving_stdout.get('raw_sha256')=='2b598fcee2191f68e9160195abfa9c068bd85078975e7115666126059aa486cd' and moving_stdout.get('actual_every_moving_frame_inside_ceiling') is True and moving_stdout.get('actual_upload_release_checks')==32,'Actual moving stdout/budget/upload proof differs')
 for stdout in [gate_stdout,moving_stdout]:
  lines=stdout.get('actual_checkout_lines',[]);need(any(TESTED_Q in line for line in lines) and any(('Merge '+H+' into '+B) in line for line in lines),'Actual native stdout does not bind tested Q/H3/accepted70b')
 accepted=bound(a.accepted_source_binding,a.accepted_source_binding_sha256)
 need(accepted.get('head')==H and accepted.get('tree')==TREE and accepted.get('app_subtree')==APP_TREE and accepted.get('incoming_dev')==B and accepted.get('expected_preflight_command')==EXPECTED_PREFLIGHT_COMMAND,'Actual committed H3 proper-base source binding differs')
 need(accepted.get('preflight_prefix')==str(LOG/'70b-transport-ui-full-preflight-before-commit') and accepted.get('preflight_result')==0 and accepted.get('cleanup_complete') is True and accepted.get('remaining_owned_children')==0,'Actual committed proper-base full gate/cleanup not successful')
 actual_gate=Path(accepted['preflight_prefix']+'.result.json');actual_gate_cleanup=Path(accepted['preflight_prefix']+'.cleanup.json');need(sha(actual_gate.read_bytes())==PREFLIGHT_RESULT_SHA and sha(actual_gate_cleanup.read_bytes())==PREFLIGHT_CLEANUP_SHA,'Actual explicit-base preflight receipts changed')
 gate=read(actual_gate);gate_cleanup=read(actual_gate_cleanup);need(gate.get('command')==EXPECTED_PREFLIGHT_COMMAND and gate.get('cwd')==str(APP) and gate.get('returncode')==0 and gate.get('timed_out') is False and gate_cleanup.get('cleanup_complete') is True and gate_cleanup.get('remaining_owned_children')==[],'Actual proper-base preflight/cleanup is not successful')
 for c in [H,B,TESTED_Q,a.owned_lease_sha]:need(git('rev-parse',c+'^{commit}')==c,'Root must separately materialize the reviewed commit/lease object: '+c)
 need(ci_objects[H].get('parents')==accepted.get('parents'),'Actual CI native H3 parent proof differs from committed source binding')
 need(git('show','-s','--format=%P',H).split()==accepted.get('parents') and subprocess.run(['git','merge-base','--is-ancestor',B,H],cwd=ROOT,env=env,capture_output=True).returncode==0,'Actual H3 does not contain accepted base70b/source binding parents')
 need(git('rev-parse',TESTED_Q+'^{tree}')==TREE and set(git('show','-s','--format=%P',TESTED_Q).split())=={B,H},'Actual tested hosted Q is not the exact H3 whole-tree/accepted-base merge')
 candidate=git('merge-tree','--write-tree',B,H).splitlines()[0] # object only; no index/worktree merge
 need(candidate==TREE and git('rev-parse',candidate+':chicago/4d')==APP_TREE and git('diff','--name-only',H,candidate)=='','Computed candidate ENTIRE tree is not exactly tested H3; no workflow or app exception')
 out.mkdir();summary={'state':'preparing actual guarded ordinary merge','head':H,'base':B,'candidate_tree':candidate,'tested_tree':TREE,'app_subtree':APP_TREE,'ci_tested_checkout':TESTED_Q,'ci_tested_base':B,'current_base_merged_CI_verified':True,'enclosing_pipeline_receipts':pipeline_receipts,'enclosing_pipeline_state':ref(PIPELINE_STATE),'driver_receipts':driver_receipts,'independent_verifier_receipts':verifier_receipts,'independent_proof':ref(a.independent_proof),'ci_binding':ref(a.ci_binding),'source_manifest':ref(MATRIX/'PUBLISHED-MANIFEST-AFTER.json'),'owned_lease_acquisition':ref(a.lease_acquisition_log),'remote_mutations':[]}
 def record():save(out/'ENDGAME-STATE.json',summary)
 def command(cmd,stem,cwd=ROOT):
  p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True);(out/(stem+'.stdout')).write_bytes(p.stdout);(out/(stem+'.stderr')).write_bytes(p.stderr);save(out/(stem+'.command.json'),{'command':cmd,'returncode':p.returncode,'cwd':str(cwd),'time_unix':time.time()});need(p.returncode==0,'Command failed; stop, preserve actual evidence: '+stem);return p.stdout
 def api(path,stem,method=None,body=None):
  args=['gh','api','--hostname','github.com','repos/kevinrhaas/chicago/'+path]
  if method:args+=['--method',method]
  if body is not None:save(out/(stem+'.request.json'),body);args+=['--input',str(out/(stem+'.request.json'))]
  if method in ['PATCH','PUT']:
   summary['remote_mutations'].append('ATTEMPT '+method+' '+path+'; actual outcome is in retained command/API receipts');record()
  raw=command(args,stem);d=json.loads(raw);save(out/(stem+'.json'),d);return d
 def native(stem):
  raw=command(['git','ls-remote','origin','refs/heads/dev','refs/pull/1279/head','refs/pull/1279/merge','refs/heads/lap/pr-1279'],stem)
  refs={r.split()[1]:r.split()[0] for r in raw.decode().splitlines()};need(refs.get('refs/heads/dev')==B and refs.get('refs/pull/1279/head')==H and refs.get('refs/heads/lap/pr-1279')==a.owned_lease_sha,'Native B/head/owned lease changed; stop before remote write')
  return refs
 def source():
  need(git('rev-parse','HEAD')==H and git('rev-parse','HEAD^{tree}')==TREE and git('diff','--cached','--name-only','HEAD')=='' and git('diff','--name-only','HEAD')=='' and git('ls-files','--others','--exclude-standard')=='','Primary source/index changed; stop before remote write')
  rows=common.manifest();need(common.value_hash(rows)==independent['published_manifest_digest'],'Published mirror changed after full matrix')
 def guard(stem,ready=False):
  source();before=native(stem+'-native-before');lease_text=git('show','-s','--format=%B',a.owned_lease_sha);age=(time.time()-int(git('show','-s','--format=%ct',a.owned_lease_sha)))/3600
  need(a.lease_owner in lease_text and 'lap PR #1279' in lease_text and 0<=age<=3,'Own lap marker is unrecognized or stale; ROOT must acquire normally, never force')
  p=api('pulls/1279',stem+'-pr');need(p.get('number')==1279 and p.get('state')=='open' and p['head']['sha']==H and p['base']['sha']==B and p['base']['ref']=='dev' and p['head']['repo']['full_name']==p['base']['repo']['full_name']=='kevinrhaas/chicago','Actual PR identity/base/head differs')
  need(p.get('mergeable') is True and p.get('mergeable_state')=='clean' and not any(x['name'].lower()=='hold' for x in p.get('labels',[])) and p.get('auto_merge') is None,'GitHub does not report ordinary clean/unheld/manual merge eligibility')
  if ready:need(p.get('draft') is False,'PR remains draft')
  reviews=api('pulls/1279/reviews?per_page=100',stem+'-reviews');need(len(reviews)<100,'Review pagination needs explicit reassessment')
  latest={}
  for r in sorted(reviews,key=lambda x:(x.get('submitted_at') or '',x['id'])):
   if r.get('state') in ['APPROVED','CHANGES_REQUESTED','DISMISSED']:latest[r['user']['login']]=r['state']
  need('CHANGES_REQUESTED' not in latest.values(),'An actual reviewer still requests changes')
  cr=api('commits/'+H+'/check-runs?per_page=100',stem+'-checks');checks=cr['check_runs'];need(cr['total_count']==len(checks) and 0<len(checks)<100,'Check pagination/empty state requires review')
  need(all(c.get('head_sha')==H and c.get('status')=='completed' and c.get('conclusion') in ['success','neutral','skipped'] for c in checks),'Current H has unfinished/red/wrong-head checks')
  need(all(any(c['name']==name and c['conclusion']=='success' for c in checks) for name in ['gate','moving-frames']),'Actual current H gate/moving success missing')
  statuses=api('commits/'+H+'/status?per_page=100',stem+'-statuses');need(statuses.get('total_count')==len(statuses.get('statuses',[])),'Legacy status pagination needs review')
  need(all(s.get('state')=='success' for s in statuses.get('statuses',[])),'A legacy commit status is unfinished/red')
  runs=[]
  for runid in sorted(CI_RUNS):
   r=api('actions/runs/'+str(runid),stem+'-run-'+str(runid));need(r.get('head_sha')==H and r.get('status')=='completed' and r.get('conclusion')=='success','Actual bound hosted CI run is no longer successful H');runs.append(r['id'])
  Q=before.get('refs/pull/1279/merge');need(Q and p.get('merge_commit_sha')==Q,'PR and native test-merge metadata disagree')
  need(git('rev-parse',Q+'^{tree}')==TREE and set(git('show','-s','--format=%P',Q).split())=={B,H},'Current native Q is not full-tree-equivalent to tested H3 with the actual B/H parents; ROOT must separately materialize it')
  after=native(stem+'-native-after');need(before==after,'Native refs changed during guard; no automatic retry')
  source();g={'native_refs':after,'checks':[{'name':c['name'],'status':c['status'],'conclusion':c['conclusion'],'id':c['id']} for c in checks],'run':runs,'head':H,'merge':Q,'tree':candidate,'base':B,'blind_override_unset':True,'owned_live_lease':a.owned_lease_sha,'lease_age_hours':age,'ci_tested_checkout':TESTED_Q,'ci_tested_base':B,'current_native_Q_equals_tested_Q':Q==TESTED_Q,'current_native_Q_entire_tree_equals_tested_H':True,'current_base_merged_CI_verified':True,'initial_candidate_entire_tree_exactly_H':True,'initial_candidate_APP_exactly_H':True,'review_blocks':False,'guarded_at_unix':time.time()};save(out/(stem+'-guard.json'),g);return p,g
 try:
  record();pre,_=guard('pre-ready')
  body='''Round the catalogue Brougham lamps, repair the planted horse’s eye UVs, add a safe Western Hotel yard viewpoint, and keep release-note text inside the Navigator.

- T-3083 rounds only the Brougham lamp form; near/mid exports preserve the vehicle’s other geometry, materials, contacts and runtime policy. V17 history stays archived.
- T-3086 delivers the separately versioned d454 eye-UV derivative; geometry, rig, weights, animation, materials and six embedded images remain preserved.
- T-3087 adds E-124/N-292/yaw221.19. All 19 viewpoints remain dry and outside roofs; the previous 18 and actor placement are retained.
- T-3125 lets the existing release-note grids shrink and wrap intact long text, without shrinking the font or hiding overflow. The same visitor entry carries all four bounded changes.

Original transport commits and historical liberty/licence decisions are retained. Shared records document the group; incoming source/assets, protected feature bytes and original ROADMAP bytes are preserved. Broader carriage acceptance stays open on T-3084/T-3085, and horse photographic/native/gait acceptance on T-3088/T-3089. Tack, team, occupant and riding work stays with its existing tickets. T-2794/T-2800 remain split; T-2803/T-2804 remain open, and unresolved T-3113 photo acceptance is outside this PR.

Fresh combined full preflight passed 1,066 steps / 384 self-tests, with complete owned cleanup. The exact committed source passed a fresh 24-leg matrix covering all 15 parts once at each viewport, plus all-row normal/140% release-note layout checks at both widths. An independent final verifier re-read every result, cleanup and full published-file census. Runs longer than the 600-second foreground budget are retained as measured budget misses; no budget PASS is inferred.

Current H: `'''+H+'''`, tested tree `'''+TREE+'''`. Ordinary hosted gate40138225825 and moving40138225852 passed on actual checkout `'''+TESTED_Q+'''` against pinned accepted70b. That hosted checkout and the local complete matrix bind the same entire source tree as H3. The current candidate must preserve the entire tested tree. Earlier-head passes, interrupted runs and operational timeouts remain historical and are excluded from this matrix.

This is DEV integration only. Public DEV build/assets, the folded visitor entry and final normal-UI yard view are verified separately after acceptance. No production promotion or wider photographic/gait approval is claimed.
'''
  body+='\nEvidence: '+a.evidence_url+'\n'
  (out/'PR1279-MERGE-READY-BODY.md').write_text(body);guard('before-body-write');api('pulls/1279','body-update','PATCH',{'title':'Round transport lamps, repair horse eyes and wrap release notes','body':body});summary['remote_mutations'].append('ordinary PR title/body update');record()
  p,_=guard('before-ready')
  if p['draft']:
   summary['remote_mutations'].append('ATTEMPT normal gh pr ready; actual outcome is in retained command receipts');record()
   command(['gh','pr','ready','1279','--repo','kevinrhaas/chicago'],'ready');summary['remote_mutations'].append('normal gh pr ready');record()
  p,g=guard('final',ready=True);save(out/'premerge-pr.json',p)
  # REST pins H, not B. The immediately repeated native check detects observed movement;
  # the service offers no base-SHA compare-and-swap. Actual M parent/tree are checked after.
  source();native('immediately-before-merge');response=api('pulls/1279/merge','merge','PUT',{'sha':H,'merge_method':'squash'});summary['remote_mutations'].append('ordinary REST SHA-pinned squash request');summary['actual_merge_response']=response;record()
  need(response.get('merged') is True and re.fullmatch('[0-9a-f]{40}',str(response.get('sha',''))),'Service did not accept merge; no automatic retry')
  M=response['sha'];commit=api('git/commits/'+M,'postmerge-commit');need([p['sha'] for p in commit['parents']]==[B] and commit['tree']['sha']==candidate,'MERGE ACCEPTED BUT SOURCE IDENTITY MISMATCH: actual M parent/tree differ; stop, do not certify or undo')
  post=api('pulls/1279','postmerge-pr');need(post.get('merged') is True and post.get('state')=='closed' and post.get('merged_at') and post.get('merge_commit_sha')==M and post['head']['sha']==H,'Actual postmerge PR metadata does not bind successful H/M')
  artifacts={'premerge_pr':ref(out/'premerge-pr.json'),'postmerge_pr':ref(out/'postmerge-pr.json'),'merge_request':ref(out/'merge.request.json'),'merge_result':ref(out/'merge.json'),'normal_merge_guard':ref(out/'final-guard.json'),'accepted_source_binding':ref(a.accepted_source_binding)}
  canonical={'schema':'chicago-pr1279-sha-pinned-squash-70b-h3-v1','state':'actual_service_receipts','repository':'kevinrhaas/chicago','pr':1279,'tested_head':H,'accepted_base':B,'merge_commit':M,'artifacts':artifacts,'actual_postmerge_commit':ref(out/'postmerge-commit.json'),'actual_M_tree':candidate,'actual_M_app_subtree':APP_TREE,'initial_M_APP_exactly_H':True,'initial_M_entire_tree_exactly_H':True,'M_sole_parent_B':True,'H_ancestor_M_required':False,'matrix_proof':ref(a.independent_proof),'source_manifest':ref(MATRIX/'PUBLISHED-MANIFEST-AFTER.json')};save(out/'PR1279-SQUASH-RECEIPT.json',canonical)
  summary.update(state='ACTUAL ORDINARY MERGE ACCEPTED; M source identity verified; public DEV remains unverified',merge_head=M,canonical_receipt=ref(out/'PR1279-SQUASH-RECEIPT.json'),lease_released=False);record()
  # Normal repository release, only after actual acceptance and only if still OUR marker.
  lease_raw=command(['git','ls-remote','origin','refs/heads/lap/pr-1279'],'before-own-lease-release').decode().strip()
  if lease_raw and lease_raw.split()[0]==a.owned_lease_sha:
   summary['remote_mutations'].append('ATTEMPT normal own ticket lap release; actual outcome is in retained command receipts');record()
   command(['node','tools/ticket.mjs','lap','1279','--release'],'normal-own-lease-release',APP)
   remaining=command(['git','ls-remote','origin','refs/heads/lap/pr-1279'],'after-own-lease-release').decode().strip();summary['lease_released']=not remaining;summary['remote_mutations'].append('normal own ticket lap release')
  else:summary['lease_release_note']='Own marker absent or changed; no stranger marker was deleted. ROOT must inspect normal status.'
  record();print(json.dumps(summary));return 0
 except BaseException as e:
  summary.update(state='STOPPED; actual prior actions remain recorded; no retry/rebase/override',error=str(e));record();raise
if __name__=='__main__':raise SystemExit(main())
