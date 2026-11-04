from pathlib import Path
import os,subprocess,json,hashlib,time,re,shutil
P=Path(__file__).parent;R=Path('/workspace/chicago-bridge-increment-20261102');A=R/'chicago/4d';S=P/'check-scratch';S.mkdir(exist_ok=True);E=dict(os.environ)
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES','CHICAGO_TICKETS_DIR']:E.pop(k,None)
E.update(GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1',CHECK_JOBS='4',C4D_GATE_REQUIRE_READERS='1',TMPDIR=str(S),OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
# Preserve project's native local-promisor test while forbidding source lazy fetch.
shim=P/'fixture-env';shim.mkdir(exist_ok=True)
b=Path('/tmp/lake-house-source-checks-20261103/strict-fixture-env/git').read_text().replace('/tmp/lake-house-check-scratch-20261103',str(S));(shim/'git').write_text(b);(shim/'git').chmod(0o755);E['PATH']=str(shim)+os.pathsep+E['PATH']
def git(*x):return subprocess.check_output(['/usr/local/bin/git','-C',str(R),*x],env=E)
def state():return {'HEAD':git('rev-parse','HEAD').decode().strip(),'index_tree':git('write-tree').decode().strip(),'diff_sha256':hashlib.sha256(git('diff','--binary')).hexdigest(),'cached_diff_sha256':hashlib.sha256(git('diff','--cached','--binary')).hexdigest()}
start=state();(P/'SOURCE4-BEFORE.json').write_text(json.dumps(start,indent=2)+'\n');rows=[]
for n in range(1,5):
 assert state()==start
 assert shutil.disk_usage('/workspace').free>536870912 and shutil.disk_usage('/tmp').free>1800000000
 tag=f'part{n}';t=time.monotonic()
 with(P/(tag+'.log')).open('xb')as log:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(P/(tag+'-REAPER.json')),'--','timeout','--signal=TERM','--kill-after=15s','600s','taskset','-c','0,1,3,4','./tools/check.sh','--part',f'{n}/4'],cwd=A,env=E,stdout=log,stderr=subprocess.STDOUT)
 proof=json.loads((P/(tag+'-REAPER.json')).read_bytes());tail=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',(P/(tag+'.log')).read_text(errors='replace')).splitlines()[-14:];same=state()==start
 row={'part':n,'exit':r.returncode,'seconds':time.monotonic()-t,'reaper':proof,'source_exact':same,'tail':tail};rows.append(row);(P/'SOURCE4-PROGRESS.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(row),flush=True)
 assert r.returncode==0 and proof['command_exit']==0 and proof['all_children_reaped'] and not proof['leftover_cleanup'] and same
 assert any(f'CHECK PASS — part {n}/4' in line for line in tail)
(P/'SOURCE4-PASS.json').write_text(json.dumps({'source':start,'parts':rows,'all4_green':True},indent=2)+'\n')
