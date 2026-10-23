import os,sys,pathlib,json,datetime,subprocess
sys.path.insert(0,'/workspace/shared');import owned_child_reaper_20261023 as owned
R=pathlib.Path('/workspace/chicago-waistcoat');A=R/'chicago/4d';D=pathlib.Path(__file__).resolve().parent/'GENERATED-REPAIR';D.mkdir(exist_ok=False)
H0='92ee0214878d0c40960b0e6239cbe415756e0e0a';B='eb1a0d11a96767a715a136ee43d94097ddf5b9cd';BR='steward/t2800-planted-standing-v16-dev-20261023';env=os.environ.copy();env['PATH']='/workspace/shared/w01-python-sum-recovery-20261022/venv311/bin:/workspace/shared/chicago-tools/usr/bin:'+env['PATH'];env.update(NODE_OPTIONS='--v8-pool-size=1 --disable-sigusr1',UV_THREADPOOL_SIZE='1',GOMAXPROCS='1',GIT_CONFIG_COUNT='3',GIT_CONFIG_KEY_0='index.threads',GIT_CONFIG_VALUE_0='1',GIT_CONFIG_KEY_1='pack.threads',GIT_CONFIG_VALUE_1='1',GIT_CONFIG_KEY_2='core.preloadIndex',GIT_CONFIG_VALUE_2='false')
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
def run(n,cmd,timeout=180):
 p=D/(n+'.log');r=owned.run(cmd,A,env,p,timeout);(D/(n+'.json')).write_text(json.dumps({k:v for k,v in r.items() if k!='new_owned_orphans_reaped'}));print(n,r['returncode'],flush=True);assert r['returncode']==0,p.read_text()[-3000:];return p.read_text().strip()
def git(n,*a):return run(n,['git','-C',str(R),*a])
owned.enable()
try:
 assert git('01-head','rev-parse','HEAD')==H0;changed=git('02-changed','diff','--name-only').splitlines();assert set(changed)=={'chicago/4d/data/liberties.json','chicago/4d/docs/measurements/source_use_coverage.md'}
 diff=git('03-exact-diff','diff','--numstat');assert all(line.startswith('1\t1\t') for line in diff.splitlines());assert not git('04-untracked','ls-files','--others','--exclude-standard') and not git('05-unmerged','ls-files','-u')
 run('06-planted-horse-contract',['node','tools/test_planted_standing_horse_contract.mjs']);git('07-whitespace','diff','--check');git('08-stage','add',*changed)
 msg='T-2800: regenerate provenance after the DEV branch update\n\nRebuild the canonical liberties source digest and source-use count after GitHub updated this integration. Only two generated metadata lines change; authored records, horse source, runtime, limits and workflow definitions stay as reviewed.\n\nThe owner authorized validating this DEV integration in fresh normal GitHub CI after local subprocess exhaustion. The earlier interrupted combined local gate remains a nonpass; DEV merge still requires green checks.\n';(D/'COMMIT-MESSAGE.txt').write_text(msg)
 run('09-normal-repair-commit',['git','commit','-F',str(D/'COMMIT-MESSAGE.txt')]);H=git('10-head','rev-parse','HEAD');T=git('11-tree','rev-parse','HEAD^{tree}');assert git('12-parent','show','-s','--format=%P','HEAD')==H0;assert not git('13-clean','status','--porcelain')
 run('14-normal-push',['git','push','origin','HEAD:refs/heads/'+BR]);ref=json.loads(run('15-verify-ref',['gh','api','--method','GET','repos/kevinrhaas/chicago/git/ref/heads/'+BR]));assert ref['object']['sha']==H
 for n,cmd in [('16-changelog',['node','tools/check-changelog-entry.mjs',B,H]),('17-IDs',['node','tools/resolve_id_collisions.mjs','--base',B,'--check']),('18-whitespace',['git','diff','--check',B,H]),('19-publish',['bash','tools/publish.sh']),('20-mirror',['node','tools/check_published.mjs']),('21-site',['python3','tools/validate.py','--site'])]:run(n,cmd,240)
 assert not git('22-clean-final','status','--porcelain');build=json.loads((R/'site/4d/build.json').read_text());assert H.startswith(build['version'])
 receipt={'head':H,'tree':T,'parents':[H0],'reviewed_base':B,'PR':1244,'normal_push_verified':True,'postpublish_verified':True,'normal_CI':'PENDING','combined_local_gate_PASS':False,'two_generated_metadata_lines_only':True,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()};(D/'TERMINAL.json').write_text(json.dumps(receipt,indent=2)+'\n');print('CURRENT PUSHED PUBLISHED '+json.dumps(receipt),flush=True)
finally:
 c=owned.finish();(D/'OWNED-CLEANUP.json').write_text(json.dumps(c));print('cleanup',c,flush=True)
