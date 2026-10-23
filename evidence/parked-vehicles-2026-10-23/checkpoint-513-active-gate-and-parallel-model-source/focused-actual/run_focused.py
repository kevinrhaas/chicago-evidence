from pathlib import Path
import subprocess,os,time,json,datetime,hashlib
D=Path(__file__).resolve().parent
R=Path('/tmp/chicago-covered-sag/chicago/4d')
env=os.environ.copy();env['PATH']='/workspace/shared/w01-python-sum-recovery-20261022/venv311/bin:/workspace/shared/chicago-tools/usr/bin:'+env['PATH']
for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[key]='1'
env['C4D_GATE_REQUIRE_READERS']='1';env['CHECK_JOBS']='4'
checks=[
 ('full-original-card-and-native-LOD',['node','tools/test_brougham_card.mjs']),
 ('exact-near-mid-and-proxy',['python3','tools/check_brougham_near.py']),
 ('parked-placement-identity',['python3','tools/transport/check_parked_placements.py']),
 ('source-params-license-and-freshness',['python3','tools/validate.py','--params','--licenses','--stale']),
 ('liberties-freshness',['python3','tools/compile_liberties.py','--check']),
 ('smoke-syntax',['node','--check','tools/smoke_renderer.mjs']),
 ('staged-whitespace',['git','diff','--cached','--check']),
 ('changelog-contract',['node','tools/check-changelog.mjs']),
 ('single-pending-entry-contract',['node','tools/changelog-entries.mjs','--check'])
]
rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for name,cmd in checks:
 t=time.monotonic();p=D/(name+'.log')
 with p.open('wb') as f:r=subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
 row={'name':name,'command':cmd,'exit_code':r.returncode,'elapsed_seconds':time.monotonic()-t,'log':str(p),'log_sha256':hashlib.sha256(p.read_bytes()).hexdigest()};rows.append(row)
 print(name,r.returncode,round(row['elapsed_seconds'],3),flush=True)
 if r.returncode:break
out={'start':start,'terminal':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':len(rows)==len(checks) and all(x['exit_code']==0 for x in rows),'checks':rows,'site_validation':'Not run against stale previous133 publication; source params/licenses/stale all checked. Normal gate publication/site will run on released full preflight.'}
(D/'FOCUSED-TERMINAL.json').write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['pass'] else 1)
