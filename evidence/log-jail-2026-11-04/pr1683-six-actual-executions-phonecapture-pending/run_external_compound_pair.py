from pathlib import Path
import hashlib,json,subprocess,os,time,tempfile,shutil
P=Path(__file__).parent;W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';S=W/'site/4d';Q=P/'current-compound-captures';Q.mkdir(exist_ok=True);E=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK='1');scratch=Path(tempfile.mkdtemp(prefix='jlpm-',dir='/tmp'));E.update(TMPDIR=str(scratch),TMP=str(scratch),TEMP=str(scratch),NODE_COMPILE_CACHE=str(scratch/'node-cache'));sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(W),*a]);dump=lambda n,d:(Q/n).write_text(json.dumps(d,indent=2)+'\n')
def source():return{'head':git('rev-parse','HEAD').decode().strip(),'index_tree':git('write-tree').decode().strip(),'working':sha(git('diff','--binary')),'cached':sha(git('diff','--cached','--binary')),'status':git('status','--porcelain').decode()}
def pubsha():
 m={p.relative_to(S).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}for p in sorted(S.rglob('*'))if p.is_file()};return sha(json.dumps(m,sort_keys=True).encode())
lease=json.loads((P/'GPU-LEASE.json').read_bytes());assert lease['root_explicit_release']and lease['source_root']==str(W)
for path in [P/'current-native3/mobile/CLOSURE.json',P/'current-native3/desktop/CLOSURE.json',P/'current-ui-phone-cards-v4/mobile-cards/CLOSURE.json']:
 d=json.loads(path.read_bytes());assert d['error']is None and d['source_publication_helpers_exact']
before=source();pub=pubsha();assert before['head']=='3f3e0bfcc99aad5d358fa8520da764fbe0aa68ff'and not before['status'];rows=[]
try:
 for view in ['gale_1902','andreas_1884_context']:
  assert source()==before and pubsha()==pub
  cam=P/'compound-camera-fixture/data/reference_views/log_jail'/(view+'.json');actual=A/'data/reference_views/log_jail'/(view+'.json');assert cam.read_bytes()==actual.read_bytes();out=Q/view;out.mkdir(exist_ok=False);log=Q/(view+'.log');rec=Q/(view+'-REAPER.json');cmd=['node','tools/photo_match.mjs',str(cam),'--out',str(out)]
  with log.open('xb')as f:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(rec),'--','timeout','--signal=TERM','--kill-after=15s','260s','nice','-n','19','taskset','-c','0-4',*cmd],cwd=A,env=E,stdout=f,stderr=subprocess.STDOUT)
  rr=json.loads(rec.read_bytes());assert r.returncode==rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup'];match=json.loads(cam.with_suffix('.match.json').read_bytes());assert match['verdict']=='unreviewed';assert match['camera_sha256']==sha(actual.read_bytes());assert source()==before and pubsha()==pub;rows.append({'view':view,'camera_sha256':match['camera_sha256'],'actual_source_photo_sha256':match['photo_sha256'],'actual_glb_sha256':match['glb_sha256'],'actual_group_sha256':match.get('group_sha256'),'image':str(out/(view+'-side-by-side.jpg')),'match':str(cam.with_suffix('.match.json')),'verdict':'UNREVIEWED','reaper':rr});print('Actual external fixed-camera capture closed',view,flush=True)
except BaseException as exc:
 dump('FAILURE.json',{'error':repr(exc),'rows':rows});raise
finally:dump('CLOSURE.json',{'source':before,'full_publication_sha256':pub,'source_and_publication_still_exact':source()==before and pubsha()==pub,'closed_views':rows,'scope':'Genuine current stockChromium fixed-committed-camera compound evidence only; no calibration/fullphoto-match/source-record changes','root_visual_review':'PENDING','new_native_blender_execution':False})
