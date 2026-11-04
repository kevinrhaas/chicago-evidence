from pathlib import Path
import subprocess,json,hashlib,time
out=Path('/tmp/smoke-yard-shadow-triage-20261104');root=Path('/tmp/wolf-poster-source-20261103/chicago/4d')
paths=['tools/smoke_renderer.mjs','tools/generate_yard_goods.py','tools/test_frame_tavern_picture_features.py','renderers/web/js/building-feet.js','renderers/web/js/buildings.js','data/structures/green_tree_tavern.json','data/sidecars/1835/green_tree_tavern.json','data/yard/town_trade_goods.json','assets/gltf/green_tree_tavern__frame_1833.glb','assets/web/green_tree_tavern__frame_1833.glb']
def bindings():return {r:{'sha256':hashlib.sha256((root/r).read_bytes()).hexdigest(),'bytes':(root/r).stat().st_size}for r in paths}
before=bindings();rows=[]
for label,cmd in [('OWNER-TWO-REGRESSIONS',['python3',str(out/'run_yard_owner_proposal.py')]),('SMOKE-PROPOSAL-SYNTAX',['node','--check',str(out/'smoke_renderer_PROPOSAL.mjs')])]:
 start=time.monotonic()
 with (out/(label+'.log')).open('wb')as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=30,check=False)
 rows.append({'label':label,'command':cmd,'exit':r.returncode,'seconds':time.monotonic()-start,'raw_log':str(out/(label+'.log')),'raw_sha256':hashlib.sha256((out/(label+'.log')).read_bytes()).hexdigest()})
 assert r.returncode==0
assert before==bindings(),'readonlysourcebindingschanged'
(out/'SOURCE-BASELINE-AND-OWNER-REGRESSION.json').write_text(json.dumps({'source_root':str(root),'source_bindings_before_after_exact':before,'steps':rows,'result':'PASS2 actualpureownerregressions plus Node syntax only','limits':'PublishedWEB browser smoke/fullsourcegate UNRUN; noapplicationmutations; shadowdiagnosticREJECTED_UNAPPROVED'},indent=2)+'\n')
print(json.dumps(rows,indent=2))
