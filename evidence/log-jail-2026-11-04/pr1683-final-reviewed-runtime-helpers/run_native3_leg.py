"""One actual published native Stage3 viewport with immutable source/publication guard."""
from pathlib import Path
import argparse,json,hashlib,subprocess,os,tempfile,shutil,re,time
P=Path(__file__).parent;W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';S=W/'site/4d';ap=argparse.ArgumentParser();ap.add_argument('--viewport',choices=['desktop','mobile'],required=True);v=ap.parse_args().viewport;O=P/'current-native3'/v;O.mkdir(parents=True,exist_ok=False);E=dict(os.environ)
for k in list(E):
 if k.startswith('SMOKE_')or k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES','CHICAGO_TICKETS_DIR']:E.pop(k,None)
scratch=Path(tempfile.mkdtemp(prefix='jln3-',dir='/tmp'));E.update(PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',TMPDIR=str(scratch),TMP=str(scratch),TEMP=str(scratch),NODE_COMPILE_CACHE=str(scratch/'node-cache'),PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK='1',SMOKE_VIEWPORT=v,SMOKE_STAGE='3',SMOKE_ROOT=str(S),SMOKE_SHOTS=str(O/'shots'))
sha=lambda b:hashlib.sha256(b).hexdigest();g=lambda *a:subprocess.check_output(['git','-C',str(W),*a],env=E);dump=lambda n,d:(O/n).write_text(json.dumps(d,indent=2)+'\n')
def floor():
 d={r:shutil.disk_usage(r).free for r in ['/workspace','/tmp']};assert d['/workspace']>=536870912 and d['/tmp']>=1800000000,d;return d
def source():return{'HEAD':g('rev-parse','HEAD').decode().strip(),'index_tree':g('write-tree').decode().strip(),'working_diff_sha256':sha(g('diff','--binary')),'staged_diff_sha256':sha(g('diff','--cached','--binary')),'untracked':g('ls-files','--others','--exclude-standard').decode()}
def pubmap():return{p.relative_to(S).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}for p in sorted(S.rglob('*'))if p.is_file()}
lease=json.loads((P/'GPU-LEASE.json').read_bytes());assert lease['root_explicit_release']and lease['source_root']==str(W);assert json.loads((P/'PUBLISH-REAPER.json').read_bytes())['command_exit']==0
before=source();assert before['HEAD'].startswith(json.loads((S/'build.json').read_bytes())['version']);assert not g('status','--porcelain');pub=pubmap();helper={'this':sha(Path(__file__).read_bytes()),'native_smoke':sha((A/'tools/smoke_renderer.mjs').read_bytes())};assert len(pub)>5000;floor();dump('PLAN.json',{'source':before,'publication_map_sha256':sha(json.dumps(pub,sort_keys=True).encode()),'publication_members':len(pub),'helpers':helper,'viewport':v,'stage':'3','expected_native_passed':107,'expected_native_failed':0,'scope':'Actual current published native Stage3 only; no full15 claim'})
def guard():
 assert source()==before and pubmap()==pub and sha(Path(__file__).read_bytes())==helper['this']and sha((A/'tools/smoke_renderer.mjs').read_bytes())==helper['native_smoke'],'Source/publication/helper drift';floor()
error=None;start=time.monotonic()
try:
 guard()
 with(O/'native.log').open('xb')as log:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(O/'NATIVE-REAPER.json'),'--','timeout','--signal=TERM','--kill-after=15s','560s','nice','-n','19','taskset','-c','0-4','node','tools/smoke_renderer.mjs','--published'],cwd=A,env=E,stdout=log,stderr=subprocess.STDOUT)
 rr=json.loads((O/'NATIVE-REAPER.json').read_bytes());text=(O/'native.log').read_text(errors='replace');counts=re.findall(r'(\d+) passed, (\d+) failed',text);assert r.returncode==rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup']and rr['interrupted_signal']is None;assert counts and counts[-1]==('107','0')and'SMOKE PASS'in text;guard()
except BaseException as exc:error=repr(exc)
finally:
 try:guard();exact=True
 except BaseException as exc:exact=False;error=(error+'; 'if error else'')+'Finalguard:'+repr(exc)
 dump('CLOSURE.json',{'status':'CURRENT_PUBLISHED_NATIVE_STAGE3_'+v.upper()+'_107_PASS'if error is None else'NOT_QUALIFIED','source':before,'source_publication_helpers_exact':exact,'error':error,'seconds':time.monotonic()-start,'resources':floor(),'no_retry':True,'full15':'NOT_RUN'});print(json.dumps({'viewport':v,'error':error}),flush=True)
raise SystemExit(0 if error is None else 1)
