from pathlib import Path
import subprocess,json,os,time,hashlib
P=Path(__file__).parent/'gt26-final/owners';P.mkdir(exist_ok=True);W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';E=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',C4D_GATE_REQUIRE_READERS='1')
def git(*a):return subprocess.check_output(['git','-C',str(W),*a])
rows=[]
for tag,cmd in [('liberties',['python','tools/compile_liberties.py']),('scene-all',['python','tools/compile_scene.py','--all']),('source-use',['python','tools/compile_source_use.py']),('derivatives',['python','tools/stale_derivatives.py']),('validate-all',['python','tools/validate.py','--all'])]:
 with(P/(tag+'.log')).open('xb')as log:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(P/(tag+'-REAPER.json')),'--','timeout','--signal=TERM','--kill-after=15s','600s','nice','-n','19','taskset','-c','2',*cmd],cwd=A,env=E,stdout=log,stderr=subprocess.STDOUT)
 proof=json.loads((P/(tag+'-REAPER.json')).read_text());assert r.returncode==0 and proof['all_children_reaped']and not proof['leftover_cleanup'],(tag,r.returncode);rows.append({'tag':tag,'command':cmd,'reaper':proof});print(tag,'PASS',flush=True)
for name in ['data/liberties.json','data/sidecars/1835/sources/index.json','docs/measurements/source_use_coverage.md']:
 path=A/name;assert b'<<<<<<<'not in path.read_bytes();subprocess.run(['git','-C',str(W),'add','chicago/4d/'+name],check=True)
assert not git('diff','--name-only','--diff-filter=U')
(P/'OWNERS-PASS.json').write_text(json.dumps({'dev':'26f6b8dfe96e9af96d7137b8e7b8a8d4061512c0','owners':rows,'note':'Fresh merged owners; actual3f six executions carried only after exactconsumer/inputaudit, newwhole8 still required; originalpartialOPEN'},indent=2)+'\n')
print('ALL OWNERS PASS',flush=True)
