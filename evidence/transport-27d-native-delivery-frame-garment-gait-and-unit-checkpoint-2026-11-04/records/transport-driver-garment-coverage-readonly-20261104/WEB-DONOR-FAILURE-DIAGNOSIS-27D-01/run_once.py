from pathlib import Path
import importlib.util,json,hashlib,subprocess,sys,os
D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
save=lambda p,j:Path(p).write_text(json.dumps(j,indent=2)+'\n')
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
prior=Path('/workspace/.cloud-setup/transport-current-20261103/actual-27d527-web-donor-preflight-01');closed=load(prior/'CLOSED.json');cfg=load(prior/'CONFIG.json');root=Path(cfg['app']).parents[1]
admit=module('admission',D.parent/'WEB-DONOR-PREFLIGHT-V1/run.py');guard=module('guard','/workspace/.cloud-setup/transport-current-20261103/resource_guard.py');before=admit.source(root,closed['source_before']);rb=guard.snapshot();assert guard.check(rb)['accepted']
files=[dict(asset=c['asset'],lod=lod,**c['web'+str(lod)])for c in cfg['cases']for lod in [0,3]];decoder=Path(cfg['app'])/'renderers/web/vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js';expected=cfg['input_pins'][str(decoder)];assert sha(decoder)==expected
config=dict(authorized_scope='FOUR_RAW_IBM_ACCESSORS_ONLY',files=files,decoder=dict(path=str(decoder),sha256=expected),source=before,failed_receipt=dict(path=str(prior/'CLOSED.json'),sha256=sha(prior/'CLOSED.json')),worker_sha256=sha(D/'extract_ibms.mjs'))
save(D/'CONFIG.json',config);prefix=D/'raw-IBM';error=None;result=cleanup=resources=after=None
try:
 with (D/'SUPERVISOR.stdout').open('xb')as out:
  q=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(D),'--timeout','30','--','node',str(D/'extract_ibms.mjs'),str(D/'CONFIG.json'),str(D/'raw')],stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ))
 result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');resources=guard.pair(rb,guard.snapshot())
 assert q.returncode==result['returncode']==0 and not result['timed_out'];assert result['requested_timeout_seconds']==result['effective_timeout_seconds']==30 and result['timeout_override_reason']is None
 assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted']
 after=admit.source(root,closed['source_before']);assert before==after
except BaseException as e:error=repr(e)
try:after=admit.source(root,closed['source_before'])
except BaseException as e:error=(error+'; 'if error else'')+repr(e)
if resources is None:resources=guard.pair(rb,guard.snapshot())
save(D/'CLOSED.json',dict(status='LIGHT_FOUR_IBM_READONLY_EXTRACTION_COMPLETE'if error is None else'NONPASS',error=error,source_before=before,source_after=after,config_sha256=sha(D/'CONFIG.json'),result=result,cleanup=cleanup,resources=resources,GLTFLoader_or_image_or_pose_or_browser_GPU_or_asset_generation=False))
print(json.dumps(dict(passed=error is None,error=error,out=str(D))));sys.exit(0 if error is None else 1)
