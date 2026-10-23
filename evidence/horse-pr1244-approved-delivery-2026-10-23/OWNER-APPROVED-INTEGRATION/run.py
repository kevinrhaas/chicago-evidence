import os,sys,pathlib,json,datetime,hashlib,re
sys.path.insert(0,'/workspace/shared')
import owned_child_reaper_20261023 as owned
R=pathlib.Path('/workspace/chicago-waistcoat');A=R/'chicago/4d';D=pathlib.Path(__file__).resolve().parent
H0='eb1cafe12b796ff3b63aecc74a9fa4ba946ca609';B='ea22b3c3055d0c6d40f213273138103fbc98cee3';T='5e7406c5d29f8a2be26e77cf098127dad5a6049d';BR='steward/t2800-planted-standing-v16-dev-20261023'
env=os.environ.copy();env['PATH']='/workspace/shared/w01-python-sum-recovery-20261022/venv311/bin:/workspace/shared/chicago-tools/usr/bin:'+env['PATH'];env.update(CHECK_JOBS='1',NODE_OPTIONS='--v8-pool-size=1 --disable-sigusr1',UV_THREADPOOL_SIZE='1',GOMAXPROCS='1',GIT_CONFIG_COUNT='3',GIT_CONFIG_KEY_0='index.threads',GIT_CONFIG_VALUE_0='1',GIT_CONFIG_KEY_1='pack.threads',GIT_CONFIG_VALUE_1='1',GIT_CONFIG_KEY_2='core.preloadIndex',GIT_CONFIG_VALUE_2='false')
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def run(n,cmd,cwd=A,timeout=180):
 p=D/(n+'.log');assert not p.exists();r=owned.run(cmd,cwd,env,p,timeout);r['new_owned_orphans_reaped_count']=len(r.pop('new_owned_orphans_reaped',[]));save(n+'.json',r);print(json.dumps({'step':n,**r}),flush=True);assert r['returncode']==0,p.read_text()[-4000:];return p.read_text().strip()
def git(n,*a):return run(n,['git','-C',str(R),*a])
def guard(tag):
 assert git(tag+'-head','rev-parse','HEAD')==H0 and git(tag+'-merge','rev-parse','MERGE_HEAD')==B
 assert git(tag+'-tree','write-tree')==T and git(tag+'-branch','branch','--show-current')==BR
 for suff,args in [('unstaged',['diff','--name-only']),('unmerged',['ls-files','-u']),('untracked',['ls-files','--others','--exclude-standard'])]:assert not git(tag+'-'+suff,*args)
owned.enable()
try:
 auth=json.loads((D/'OWNER-AUTHORIZATION.json').read_text());assert auth['authorized_one_integration_commit'] and auth['reviewed_tree']==T and not auth['GitHub_gate_bypass_authorized']
 guard('01')
 assert json.loads(run('02-current-DEV',['gh','api','--method','GET','repos/kevinrhaas/chicago/git/ref/heads/dev']))['object']['sha']==B
 pr=json.loads(run('03-current-PR',['gh','api','--method','GET','repos/kevinrhaas/chicago/pulls/1244']));assert pr['head']['sha']==H0 and pr['head']['ref']==BR and pr['draft'] and pr['state']=='open' and pr['base']['ref']=='dev' and pr['auto_merge'] is None
 assert git('04-current-remote','ls-remote','origin','refs/heads/'+BR).split()[0]==H0
 paths=git('05-PR-paths','diff','--cached','--name-only',B).splitlines();assert len(paths)==43
 for rel in paths:
  if rel not in ['chicago/4d/data/liberties.json','chicago/4d/data/sidecars/1812/sources/uses.json','chicago/4d/data/sidecars/1835/sources/index.json','chicago/4d/data/sidecars/1904/sources/uses.json','chicago/4d/docs/LIBERTIES.md','chicago/4d/docs/measurements/source_use_coverage.md']:
   # The original horse changes are already committed; compare object IDs without copying assets.
   import subprocess
   old=subprocess.check_output(['git','-C',str(R),'rev-parse',H0+':'+rel],env=env,text=True).strip();new=subprocess.check_output(['git','-C',str(R),'rev-parse',':'+rel],env=env,text=True).strip();assert old==new,rel
 message='T-2800: integrate current DEV with the planted standing horse\n\nPreserve both authored liberty additions and rebuild the five generated provenance outputs with their canonical owners. Retain all horse and incoming DEV source and geometry.\n\nThe original horse source passed all 1054 local checks. Combined local G11 validation disconnected and stopped after spawnSync git EAGAIN; no combined local PASS is claimed. The owner explicitly approved this one pre-commit exception so fresh normal GitHub CI can validate this reviewed integration. DEV merge remains conditional on green checks.\n'
 (D/'COMMIT-MESSAGE.txt').write_text(message)
 candidate=git('06-candidate','commit-tree',T,'-p',H0,'-p',B,'-F',str(D/'COMMIT-MESSAGE.txt'))
 run('07-candidate-changelog',['node','tools/check-changelog-entry.mjs',B,candidate]);run('08-candidate-IDs',['node','tools/resolve_id_collisions.mjs','--base',B,'--check']);git('09-candidate-whitespace','diff','--check',B,candidate)
 guard('10')
 run('11-normal-merge-commit',['git','commit','-F',str(D/'COMMIT-MESSAGE.txt')]);H=git('12-actual-head','rev-parse','HEAD');assert git('13-actual-tree','rev-parse','HEAD^{tree}')==T and git('14-actual-parents','show','-s','--format=%P',H)==H0+' '+B
 assert not git('15-clean','status','--porcelain');save('COMMITTED.json',{'head':H,'tree':T,'parents':[H0,B],'at':now(),'owner_exception':True,'combined_local_gate_PASS':False})
 run('16-normal-push',['git','push','-u','origin','HEAD:refs/heads/'+BR]);assert git('17-verify-push','ls-remote','origin','refs/heads/'+BR).split()[0]==H;save('PUSHED.json',{'head':H,'tree':T,'branch':BR,'at':now(),'force':False})
 for name,cmd in [('18-HEAD-changelog',['node','tools/check-changelog-entry.mjs',B,H]),('19-HEAD-IDs',['node','tools/resolve_id_collisions.mjs','--base',B,'--check']),('20-HEAD-whitespace',['git','diff','--check',B,H]),('21-publish',['bash','tools/publish.sh']),('22-mirror',['node','tools/check_published.mjs']),('23-site',['python3','tools/validate.py','--site'])]:run(name,cmd,timeout=240)
 assert not git('24-clean-after-publish','status','--porcelain');build=json.loads((R/'site/4d/build.json').read_text());assert H.startswith(build['version'])
 body='Adds one selectable reconstructed horse to the 1835 Western Hotel yard, with a 12-second planted weight shift, provenance card, bounded drawn-yard support and host visibility/pause/resource ownership. Modern CC BY 4.0 model credit is separate from reconstructed historical appearance and placement.\n\nIntegrates DEV '+B+' while preserving both authored liberty additions, rebuilding five generated provenance outputs and retaining all 37 horse-only and 156 upstream-only source files. Source tree `'+T+'`; actual pushed head `'+H+'`.\n\nValidation: original horse source eb1cafe12 passed all 1054 local checks (382 self-tests). The combined G11 local run disconnected and stopped after actual `spawnSync git EAGAIN`; it has no complete local PASS. The owner explicitly authorized one pre-commit exception for this reviewed integration. Actual committed-HEAD changelog, ID, whitespace, publisher, mirror and site checks passed. Fresh normal GitHub CI is required before DEV merge. Standard-loader/Mixer planted checks passed 65 keys and 64 midpoints; unchanged horse/runtime bytes retain that bounded proof.\n\nThis is a standing increment, not photographic completion. Fresh yard capture is pending. Anatomy, eyes/coat/hair, walking/trotting, tack, teams, drivers and riding remain open under T-2800/T-2803. Earlier nonpasses are preserved in chicago-evidence; no geometry, viewport or frame limits were relaxed.\n'
 (D/'PR-BODY.md').write_text(body);save('PR-BODY-REQUEST.json',{'body':body})
 current=json.loads(run('25-verify-updated-PR',['gh','api','--method','GET','repos/kevinrhaas/chicago/pulls/1244']));assert current['head']['sha']==H and current['draft'] and current['state']=='open'
 updated=json.loads(run('26-update-PR-body',['gh','api','--method','PATCH','repos/kevinrhaas/chicago/pulls/1244','--input',str(D/'PR-BODY-REQUEST.json')]));assert updated['head']['sha']==H and updated['draft']
 save('TERMINAL.json',{'status':'PUSHED_PUBLISHED_OWNER_APPROVED_INTEGRATION','head':H,'tree':T,'parents':[H0,B],'PR':1244,'fresh_normal_CI':'PENDING','merged':False,'combined_local_gate_PASS':False,'at':now()});print('INTEGRATION PUSHED '+H,flush=True)
finally:
 cleanup=owned.finish();save('OWNED-CLEANUP.json',cleanup);print('OWNED CLEANUP '+json.dumps(cleanup),flush=True)
