from pathlib import Path
import os,subprocess,json,hashlib,time
P=Path(__file__).parent;F=P/'fixture';F.mkdir(exist_ok=True);W=Path('/tmp/wolf-poster-source-20261103/chicago/4d');O=Path('/tmp/cobweb-face-correspondence-review-20261104');S=P.parent
expected={'camera':'07f94fa8654e1c0469ad4d3df2c0c01414e15ce5cfabcdadde9260a942ea4977','source':'624d8f1f52a75bf30653e8cbf37a388478b0ddf5a02f1fadf727cf2144b84c3f','before':'af1f33c0f5d75fc8c40e6cbb589adfd7d29d551572c2775e236bb260f6ee561f','after':'4f42207be5fcb2391fda58672ce8442b02aba9510f3096db8c2934b695fe7bea'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def link(p,target):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.is_symlink():assert p.resolve()==target.resolve()
 else:assert not p.exists();p.symlink_to(target,target_is_directory=target.is_dir())
camera=(O/'camera/agency_1831_private.json').read_bytes();assert hashlib.sha256(camera).hexdigest()==expected['camera'];source=O/'source/original-full-panorama.jpg';assert sha(source)==expected['source']
link(F/'renderers',W/'renderers');link(F/'tools',W/'tools');link(F/'node_modules',Path('/workspace/shared/node/node_modules'))
link(F/'chicago/chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg',source)
for label in ['before','after']:
 g=S/(label+'-gltf.glb');assert sha(g)==expected[label];link(F/(label+'.glb'),g);c=F/('camera-'+label)/'agency_1831_private.json';c.parent.mkdir(exist_ok=True);assert not c.exists()or c.read_bytes()==camera;c.write_bytes(camera)
paths=[W/'tools/photo_match.mjs',W/'tools/photo_match_group.mjs',W/'tools/photo_match_flora.mjs',W/'tools/photo_match_enclosures.mjs',W/'renderers/web/js/keith-stone.js']+list((W/'renderers/web/vendor/three-0.185.1').rglob('*.js'))
guard={str(p):sha(p)for p in paths};(P/'PRE-INPUT-GUARD.json').write_text(json.dumps({'expected':expected,'tool_sources':guard,'diagnostic_only':True,'camera_source_bytes_unmodified':True},indent=2));E=dict(os.environ);E['TMPDIR']='/tmp/cb1690';Path(E['TMPDIR']).mkdir(exist_ok=True)
results=[]
for label in ['before','after']:
 cmd=['timeout','--signal=TERM','--kill-after=15s','260s','node',str(W/'tools/photo_match.mjs'),str(F/('camera-'+label)/'agency_1831_private.json'),'--glb',label+'.glb','--out',str(P/('out-'+label))]
 start=time.monotonic()
 with(P/(label+'.log')).open('w')as log:r=subprocess.run(cmd,cwd=F,env=E,stdout=log,stderr=subprocess.STDOUT)
 row={'label':label,'command':cmd,'exit':r.returncode,'seconds':time.monotonic()-start};results.append(row);(P/'RESULTS.json').write_text(json.dumps(results,indent=2));assert r.returncode==0,row
 assert guard=={str(p):sha(p)for p in paths},'source changed'
 assert sha(F/('camera-'+label)/'agency_1831_private.json')==expected['camera'];assert sha(source)==expected['source'];assert sha(S/(label+'-gltf.glb'))==expected[label]
 rec=json.load(open(F/('camera-'+label)/'agency_1831_private.match.json'));assert rec['camera_sha256']==expected['camera']and rec['glb_sha256']==expected[label]and rec['photo_sha256']==expected['source'];assert rec['verdict']=='unreviewed'
(P/'FINAL-GUARD.json').write_text(json.dumps({'all_fixed_inputs_exact':True,'tool_sources_exact':True,'only_glb_changed_between_passes':True,'no_canonical_or_source_repo_writes':True,'diagnostic_only':True,'new_calibration_RMS_or_match_claim':False,'results':results},indent=2));print(json.dumps(results),flush=True)
