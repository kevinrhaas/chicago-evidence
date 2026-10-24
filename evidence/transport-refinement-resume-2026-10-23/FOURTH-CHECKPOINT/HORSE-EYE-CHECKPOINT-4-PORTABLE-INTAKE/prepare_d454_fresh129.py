from pathlib import Path
import json,hashlib,shutil,difflib
P=Path(__file__).resolve().parent
old=Path('/workspace/shared/T2800-1904-RESUME-20261023-2245/FRESH-CLONE129')
new=P/'D454-FRESH-CLONE129';assert not new.exists();new.mkdir()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
base='b479442cb03ac46eb13c19da15a79cdfaf28dbdf356b116f78de7ce7ecdc60be'
candidate=P/'V4-CINF-LINEAR-RESERVE-UV/ACTUAL-ONE-UV-ONLY-CANDIDATE/horse-sevket-v16-planted-standing-ocular-uv-CANDIDATE.glb'
target='d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914';assert sha(candidate)==target
b=json.loads((old/'ROOT-RELEASE.json').read_text())
files=list(b['source_sha256'])+['SIDECAR.json','IMAGE-DIMENSION-ONLY-SHIM-INPUTS.json']
for f in files:
 dst=new/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old/f,dst)
spec=json.loads((new/'SIDECAR.json').read_text());spec['runtime_asset'].update(sha256=target,bytes=candidate.stat().st_size,file='transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb')
spec['idle']['actual_loaded_mixer_accepted']=False
spec['idle']['loaded_qualification_status']='FRESH_D454_CPU_CHECK_PENDING_NO_NATIVE_ACCEPTANCE'
(new/'SIDECAR.json').write_text(json.dumps(spec,indent=2)+'\n')
f=new/'modules/standing-horse-planted-idle.js';s=f.read_text();assert s.count(base)==1;s=s.replace(base,target).replace('3783600','3784176');f.write_text(s)
f=new/'proof.mjs';s=f.read_text();assert s.count(base)==1;s=s.replace(base,target);s=s.replace("const report={status:","const report={selected_asset_sha256:'"+target+"',historical_b479_qualification_not_inherited:true,status:");f.write_text(s)
f=new/'run_once.py';s=f.read_text().replace('768*1024*1024','256*1024*1024').replace('RSS_LIMIT_768_MiB','RSS_LIMIT_256_MiB');f.write_text(s)
def rebase(x):return str(x).replace(str(old),str(new))
b['maximum_rss_bytes']=256*1024*1024;b['paths']={k:rebase(v) for k,v in b['paths'].items()};b['paths']['asset']=str(candidate)
inputs={}
for path in b['inputs']:
 q=Path(rebase(path))
 if path==json.loads((old/'ROOT-RELEASE.json').read_text())['paths']['asset']:q=candidate
 inputs[str(q)]={'sha256':sha(q),'bytes':q.stat().st_size}
b['inputs']=inputs;b['source_sha256']={f:sha(new/f) for f in b['source_sha256']}
template=dict(b);template['released']=False
(new/'BINDING-RELEASED-FALSE.json').write_text(json.dumps(template,indent=2)+'\n')
(new/'ROOT-RELEASE.json').write_text(json.dumps(b,indent=2)+'\n')
diff=''.join(''.join(difflib.unified_diff((old/f).read_text().splitlines(True),(new/f).read_text().splitlines(True),fromfile='original/'+f,tofile='d454/'+f)) for f in files if (old/f).read_bytes()!=(new/f).read_bytes())
(new/'EXACT-BRIDGE.diff').write_text(diff)
(new/'SCOPE.md').write_text('One root-authorized fresh d454 production GLTFLoader / SkeletonUtils clone / Mixer129 CPU check. Original 129-frame physical predicates, negative controls, image shim and lifecycle checks are unchanged. Only selected asset identity, sidecar pending qualification, explicit report identity and stricter RSS cap differ. External 1904 fixture is not canonical scene activation. All native/GPU/world/photo acceptance remains false. Original b479 results remain historical. Root authorization received in parent message; one run only, 20 seconds, 256 MiB.\n')
print(json.dumps({'directory':str(new),'source_sha256':b['source_sha256'],'release_sha256':sha(new/'ROOT-RELEASE.json')},indent=2))
