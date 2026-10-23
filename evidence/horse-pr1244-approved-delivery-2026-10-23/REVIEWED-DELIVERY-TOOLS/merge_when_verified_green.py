import os,sys,pathlib,json,datetime,hashlib
sys.path.insert(0,'/workspace/shared');import owned_child_reaper_20261023 as owned
R=pathlib.Path('/workspace/chicago-waistcoat');D=pathlib.Path(__file__).resolve().parent/'NORMAL-GREEN-MERGE';C=pathlib.Path('/workspace/shared/T2800-HORSE-PR1244-f225b8ae54-APPLICABLE-NORMAL3-TERMINAL-GET-owner1')
H='f225b8ae541173e2dde6e576bb20c103f4c87106';T='43665a4b692d5283defba96f236aed14b3c02623';B='eb1a0d11a96767a715a136ee43d94097ddf5b9cd';Q='60f4fb6100c93ae984d73fc3e427aa0e0bfdb84b';BR='steward/t2800-planted-standing-v16-dev-20261023'
assert sys.argv[1:]==['--root-authorized-green-merge'];proofs=json.loads((C/'AUDITED-JOBS.json').read_text());terminal=json.loads((C/'TERMINAL.json').read_text());assert len(proofs)==3 and {p['run_id']for p in proofs}=={40004752292,40004752222,40004742266} and all(p['PASS'] is True and p['source']==H for p in proofs);assert terminal['terminal_collected']==3 and terminal['strict_success']==3
# Add to existing proof checks before D.mkdir/any API write:
SOURCE_PARENTS=['92ee0214878d0c40960b0e6239cbe415756e0e0a']
assert terminal['source']==H and terminal['source_tree']==T and terminal['source_parents']==SOURCE_PARENTS
assert terminal['expected_testmerge']==Q and terminal['expected_testmerge_tree']==T and terminal['reviewed_base']==B
EXPECTED={40004752292:('.github/workflows/chicago-4d-check.yml','pull_request'),40004752222:('.github/workflows/chicago-4d-moving-frames.yml','pull_request'),40004742266:('.github/workflows/chicago-4d-pr-stuck.yml','push')}
for proof in proofs:
 assert (proof['workflow_path'],proof['event'])==EXPECTED[proof['run_id']] and proof['run_conclusion']=='success'
 assert proof['actual_checkout_tree']==T and proof['actual_checkout_parents']==(SOURCE_PARENTS if proof['event']=='push' else [B,H])

assert all(p['actual_checkout_sha']==(H if p['event']=='push' else Q) for p in proofs);D.mkdir(exist_ok=False);env=os.environ.copy();env['GOMAXPROCS']='1';env.update(GIT_CONFIG_COUNT='3',GIT_CONFIG_KEY_0='index.threads',GIT_CONFIG_VALUE_0='1',GIT_CONFIG_KEY_1='pack.threads',GIT_CONFIG_VALUE_1='1',GIT_CONFIG_KEY_2='core.preloadIndex',GIT_CONFIG_VALUE_2='false')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def run(n,cmd):
 p=D/(n+'.log');r=owned.run(cmd,R,env,p,90);save(n+'.json',{k:v for k,v in r.items() if k!='new_owned_orphans_reaped'});print(n,r['returncode'],flush=True);assert r['returncode']==0,p.read_text()[-2000:];return p.read_text().strip()
def api(n,method,route,body=None):
 args=['gh','api','--method',method,'repos/kevinrhaas/chicago/'+route]
 if body is not None:save(n+'-request.json',body);args+=['--input',str(D/(n+'-request.json'))]
 out=run(n,args);return json.loads(out) if out else None
def valid_pr(p):
 assert p['head']['sha']==H and p['head']['ref']==BR and p['head']['repo']['full_name']=='kevinrhaas/chicago' and p['base']['ref']=='dev' and p['state']=='open' and p['auto_merge'] is None
owned.enable()
try:
 assert run('01-local-head',['git','rev-parse','HEAD'])==H and run('02-local-tree',['git','rev-parse','HEAD^{tree}'])==T and not run('03-clean',['git','status','--porcelain'])
 p=api('04-current-PR','GET','pulls/1244');valid_pr(p);assert api('05-current-DEV','GET','git/ref/heads/dev')['object']['sha']==B,'DEV advanced; preserve evidence and review before merge'
 checks=api('06-all-current-check-runs','GET','commits/'+H+'/check-runs?per_page=100');assert checks['total_count']==len(checks['check_runs']) and checks['total_count']>=3;assert all(c['head_sha']==H and c['status']=='completed' and c['conclusion']in['success','neutral','skipped']for c in checks['check_runs']),'Current check pending or red'
 statuses=api('07-legacy-statuses','GET','commits/'+H+'/status?per_page=100');assert statuses['total_count']==len(statuses['statuses']);assert all(s['state']=='success'for s in statuses['statuses']),'Legacy status pending or red'
 body='Adds one selectable reconstructed horse to the 1835 Western Hotel yard, with a 12-second planted weight shift, provenance card, bounded drawn-yard support and host visibility/pause/resource ownership. Modern CC BY 4.0 model credit is separate from reconstructed historical appearance and location.\n\nFinal source `'+H+'`, tree `'+T+'`, integrates DEV `'+B+'`. Canonical owners rebuilt the generated provenance metadata after the ordinary GitHub branch update; source/geometry and all existing people, vehicles and UI are preserved.\n\nFresh normal CI passed on this exact source: [gate](https://github.com/kevinrhaas/chicago/actions/runs/40004752292), [moving frames](https://github.com/kevinrhaas/chicago/actions/runs/40004752222), [report](https://github.com/kevinrhaas/chicago/actions/runs/40004742266). Actual PR checkout `'+Q+'` has parents [DEV, source] and tree `'+T+'`; the report checked out the source itself. Human workflow has zero matches among 43 changed paths and is N/A, never counted as a fourth pass. Actual committed-HEAD changelog/ID/whitespace/publisher/mirror/site and planted-standing contract checks pass.\n\nOriginal horse source eb1cafe passed all 1054 local checks/382 self-tests. Combined local G11 disconnected and stopped after spawnSync git EAGAIN; the owner explicitly approved using normal GitHub CI for this reviewed integration. That failed local run remains preserved, not relabelled.\n\nOne original mobile yard inspection failed before any appframe because Chromium could not create threads. Zero apprequests/captures; inputs unchanged and final owned-process cleanup proven. This is not visual or photographic acceptance. Standard-loader/Mixer proof covers 65 planted keys and 64 midpoints only. Photographic anatomy/eyes/coat/hair, full gaits, tack, teams, drivers and riding remain open under T-2800/T-2803.\n'
 api('08-update-final-description','PATCH','pulls/1244',{'title':'T-2800, T-2803: add a planted standing horse to the Western Hotel yard','body':body})
 if p['draft']:run('09-ready',['gh','pr','ready','1244','--repo','kevinrhaas/chicago'])
 if any(x['name']=='hold'for x in p['labels']):api('10-remove-hold','DELETE','issues/1244/labels/hold')
 final=api('11-current-ready-PR','GET','pulls/1244');valid_pr(final);assert not any(label['name']=='hold' for label in final['labels']);assert not final['draft'] and final['mergeable'] is True and final['mergeable_state']=='clean','GitHub has not allowed the normal green merge'
 assert api('12-final-DEV','GET','git/ref/heads/dev')['object']['sha']==B,'DEV changed during final verification'
 result=api('13-normal-head-pinned-squash','PUT','pulls/1244/merge',{'sha':H,'merge_method':'squash','commit_title':'T-2800, T-2803: add a planted standing horse to the Western Hotel yard (#1244)'})
 assert result['merged'] is True;M=result['sha'];save('MERGED.json',{'source':H,'source_tree':T,'reviewed_base':B,'merge_commit':M,'at':now(),'method':'ordinary API squash with expected source SHA','normal_runs':[p['run_id']for p in proofs],'no_admin_or_bypass':True})
 actual=api('14-verify-merged-PR','GET','pulls/1244');assert actual['merged'] and actual['state']=='closed' and actual['head']['sha']==H and actual['base']['ref']=='dev' and actual['merge_commit_sha']==M
 commit=api('15-actual-merge-commit','GET','git/commits/'+M);assert commit['tree']['sha']==T and [x['sha']for x in commit['parents']]==[B]
 save('TERMINAL.json',{'status':'MERGED_VERIFIED','PR':1244,'source':H,'source_tree':T,'DEV_merge_commit':M,'merge_tree':commit['tree']['sha'],'merge_parents':[B],'at':now(),'preview_delivery':'PENDING','photographic_completion':False});print('MERGED DEV '+M,flush=True)
finally:
 cleanup=owned.finish();save('OWNED-CLEANUP.json',cleanup);print('cleanup',cleanup,flush=True)
