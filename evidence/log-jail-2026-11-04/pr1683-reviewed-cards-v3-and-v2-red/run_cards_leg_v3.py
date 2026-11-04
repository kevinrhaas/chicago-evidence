"""One foreground Jail published UI leg, immutable source/pub guard, no retries."""
from pathlib import Path
import argparse,json,hashlib,os,subprocess,tempfile,shutil,time
P=Path(__file__).parent;W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';S=W/'site/4d';ap=argparse.ArgumentParser();ap.add_argument('--viewport',choices=['desktop','mobile'],required=True);ap.add_argument('--leg',choices=['cards'],required=True);q=ap.parse_args();tag=q.viewport+'-'+q.leg;O=P/'current-ui-cards-v3'/tag;O.mkdir(parents=True,exist_ok=False);E=dict(os.environ)
for key in list(E):
 if key.startswith('SMOKE_')or key in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES','CHICAGO_TICKETS_DIR']:E.pop(key,None)
scratch=Path(tempfile.mkdtemp(prefix='jlui-',dir='/tmp'));E.update(PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK='1',TMPDIR=str(scratch),TMP=str(scratch),TEMP=str(scratch),NODE_COMPILE_CACHE=str(scratch/'node-cache'))
sha=lambda b:hashlib.sha256(b).hexdigest();pf=lambda p:sha(Path(p).read_bytes());g=lambda *a:subprocess.check_output(['git','-C',str(W),*a],env=E);dump=lambda n,d:(O/n).write_text(json.dumps(d,indent=2)+'\n')
def floor():
 d={r:shutil.disk_usage(r).free for r in ['/workspace','/tmp']};assert d['/workspace']>=536870912 and d['/tmp']>=1800000000,d;return d
def source():return{'HEAD':g('rev-parse','HEAD').decode().strip(),'index_tree':g('write-tree').decode().strip(),'working_diff_sha256':sha(g('diff','--binary')),'staged_diff_sha256':sha(g('diff','--cached','--binary')),'untracked':g('ls-files','--others','--exclude-standard').decode()}
def pubmap():return{p.relative_to(S).as_posix():{'bytes':p.stat().st_size,'sha256':pf(p)}for p in sorted(S.rglob('*'))if p.is_file()}
def bindings():
 files={P/'jail_cards_probe_v3.mjs',Path(__file__)}
 for root in [A/'renderers/web',S/'walk']:
  for ext in ['*.js','*.mjs','*.css','*.html']:files.update(root.rglob(ext))
 for id,phase in [('log_jail','log_1833'),('log_jail_keeper_house','frame_1835')]:
  files.update([A/'data/structures'/(id+'.json'),A/'data/sidecars/1835'/(id+'.json'),S/'data/sidecars/1835'/(id+'.json'),A/'assets/gltf'/(id+'__'+phase+'.glb'),A/'assets/web'/(id+'__'+phase+'.glb'),S/'data/gltf'/(id+'__'+phase+'.glb')])
 for rel in ['assets/manifest.json','assets/manifest.web.json','data/enclosures/log_jail_palisade.json','data/enclosures/log_jail_keeper_link.json','data/reference_views/log_jail/gale_1902.json','data/reference_views/log_jail/andreas_1884_context.json','data/sources/trowbridge_first_jail_gale_1902.json','tools/smoke_renderer.mjs','data/pictures/1835.json']:files.add(A/rel)
 files.add(S/'data/pictures/1835.json')
 return{str(p):{'bytes':p.stat().st_size,'sha256':pf(p)}for p in sorted(files)}
review=json.loads((P/'FINAL-CARDS-V3-PEER-REVIEW.json').read_bytes());assert review['root_approved'];
for n,h in review['hashes_exact'].items():assert pf(P/n)==h,('unreviewed cards helper drift',n)
lease=json.loads((P/'GPU-LEASE.json').read_bytes());assert lease['root_explicit_release']and lease['source_root']==str(W)
assert json.loads((P/'PUBLISH-REAPER.json').read_bytes())['command_exit']==0
before=source();pub=pubmap();inputs=bindings();assert len(pub)>5000;floor();plan={'expected_head':before['HEAD'],'source_guard':before,'site_parent':str(W/'site'),'input_bindings':inputs,'source_scope_sha256':sha(json.dumps(inputs,sort_keys=True).encode()),'full_publication_map_sha256':sha(json.dumps(pub,sort_keys=True).encode()),'full_publication_members':len(pub),'expected_picture_rows':{id:json.loads((S/'data/pictures/1835.json').read_bytes())['by_structure'].get(id,[])for id in ['log_jail','log_jail_keeper_house']},'expected_sources':{id:next(c for c in json.loads((S/'data/sidecars/1835'/(id+'.json')).read_bytes())['citations']if c['source_id']==sid)for id,sid in [('log_jail','andreas_1884_v1'),('log_jail_keeper_house','trowbridge_first_jail_gale_1902')]},'scope':'Current immutable Jail keeper partial increment, actual UI only; no original match closure'};dump('PLAN.json',plan);dump('PUBLICATION-MAP.json',pub)
def guard():assert source()==before and pubmap()==pub and bindings()==inputs,'Source/publication/helper drift';floor()
E.update(GT_PROBE_PLAN=str(O/'PLAN.json'),GT_PROBE_OUT=str(O/'actual'),GT_PROBE_VIEWPORT=q.viewport,JAIL_PROBE_LEG=q.leg);start=time.monotonic();error=None
try:
 guard()
 with(O/'native.log').open('xb')as log:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(O/'NATIVE-REAPER.json'),'--','timeout','--signal=TERM','--kill-after=15s','560s','nice','-n','19','taskset','-c','0-4','node',str(P/'jail_cards_probe_v3.mjs')],cwd=A,env=E,stdout=log,stderr=subprocess.STDOUT)
 rr=json.loads((O/'NATIVE-REAPER.json').read_bytes());assert r.returncode==rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup']and rr['interrupted_signal']is None
 result=json.loads((O/'actual/RESULT.json').read_bytes());assert result['status']=='ACTUAL_JAIL_'+q.leg.upper()+'_PASS';guard()
except BaseException as exc:error=repr(exc)
finally:
 try:guard();exact=True
 except BaseException as exc:exact=False;error=(error+'; 'if error else'')+'Finalguard:'+repr(exc)
 dump('CLOSURE.json',{'status':'JAIL_CURRENT_'+tag.upper()+'_PASS'if error is None else'NOT_QUALIFIED','source':before,'source_publication_helpers_exact':exact,'error':error,'seconds':time.monotonic()-start,'resources':floor(),'no_retry':True});print(json.dumps({'tag':tag,'error':error}),flush=True)
raise SystemExit(0 if error is None else 1)
