import argparse, datetime, hashlib, json, pathlib, shutil
P=pathlib.Path
D=P('/tmp/nov10-pr1910-completion-qualification');D.mkdir(exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--freeze',action='store_true');a=parser.parse_args()
source='af4cc3ff486a90571edb7f3bb48ee1609343ad5f'
def sha(p):return hashlib.sha256(P(p).read_bytes()).hexdigest()
def put(n,d): (D/n).write_text(json.dumps(d,indent=2)+'\n')
prior=[];known={}
for name,path in [('source','/tmp/nov10-pr1910-source-checkpoint/GITHUB-CHECKPOINT-RECEIPT.json'),('interim','/tmp/nov10-pr1910-interim-qualification/GITHUB-CHECKPOINT-RECEIPT.json')]:
 d=json.loads(P(path).read_text());assert d['exact_readbacks'];prior.append({'name':name,'commit':d['commit'],'prefix':d['prefix'],'receipt_sha256':sha(path),'files':len(d['files'])})
 for rel,row in d['files'].items():known.setdefault(row['sha256'],{'commit':d['commit'],'path':d['prefix']+rel,**row})
status={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':source,'published_build':'af4cc3ff48','source_ci':{'run':42765887507,'status':'PASS_ALL_EIGHT_AND_AGGREGATE','steps':1297},'moving_frames':{'run':42765887535,'status':'ROOT_REPORTED_SUCCESS_AWAITING_RAW_BINDING'},'published_ui':{'status':'PASS_52_DIRECTLY_REVIEWED_SCREENSHOTS','durable_interim_commit':prior[1]['commit']},'final_stage1':{'status':'PASS','desktop':'95/0','phone':'95/0'},'post_b_boot':{'status':'PASS','actual_bytes':45948374,'budget_bytes':46242201.6},'balanced_six_stands':{'status':'PASS','triangles':2597349,'triangle_ceiling':2675000,'draw_calls':6443,'draw_call_ceiling':7800},'full_native_smoke':{'status':'17_OF_18_PROVEN_DESKTOP13_PENDING','recovery_run':42765919955},'merge_tickets':{'status':'NOT_CLAIMED_ROOT_OWNED_POSTMERGE_READBACK'},'claim_limit':'This additive package does not alter either prior checkpoint. No full native-smoke, final17DONE or merge claim until actual terminal evidence is added. No whole-FITS extrapolation from boot or Balanced.'}
# Root/Sauganash may supply terminal recovery and moving-frame immutable receipt paths here.
extras=D/'EXTRA-FILES.json'
if not extras.exists():put('EXTRA-FILES.json',{})
files={};reused=[]
def add(name,p):
 p=P(p);assert p.is_file(),p
 h=sha(p)
 if h in known:reused.append({'name':name,'local_path':str(p),'sha256':h,'durable':known[h]});return
 files[name]=str(p)
for path in sorted(P('/tmp/nov10-final-three-native/final-source-ci').glob('*')):
 if path.is_file():add('final-source-ci/'+path.name,path)
for mode in ['desktop','mobile']:
 for path in sorted((P('/tmp/nov10-final-stockade-smoke')/mode).glob('*')):
  if path.is_file():add('final-stage1/'+mode+'/'+path.name,path)
add('final-stage1/GPU-RELEASE.json','/tmp/nov10-final-stockade-smoke/GPU-RELEASE.json')
for name in ['ACTUAL-BOOT.json','COMMAND-RECEIPT.json','FINAL-BOOT-RECEIPT.json','INPUT-BINDINGS.json','boot-entries.json','official-boot.stdout.log','official-boot.stderr.log','run-official.py','ACTUAL-BALANCED-SIX-STANDS.json','BALANCED-COMMAND-RECEIPT.json','FINAL-BALANCED-ASSESSMENT.json','official-balanced.stdout.log','official-balanced.stderr.log','run-balanced.py','GPU-RELEASE.json']:
 add('post-b-budget/'+name,P('/tmp/nov10-post-b-boot')/name)
for name,path in [('source','/tmp/nov10-pr1910-source-checkpoint/GITHUB-CHECKPOINT-RECEIPT.json'),('interim','/tmp/nov10-pr1910-interim-qualification/GITHUB-CHECKPOINT-RECEIPT.json')]:add('prior-checkpoints/'+name+'-receipt.json',path)
for name,path in json.loads(extras.read_text()).items():add(name,path)
# Full terminal smoke and moving-frame status can only be asserted by explicit reviewed bindings.
overrides=D/'TERMINAL-STATUS.json'
if overrides.exists():
 status.update(json.loads(overrides.read_text())); files['TERMINAL-STATUS.json']=str(overrides)
put('STATUS.json',status);put('REUSED-PUBLIC-ARTIFACTS.json',{'prior_checkpoints':prior,'exact_sha256_reuses':reused})
files['STATUS.json']=str(D/'STATUS.json');files['REUSED-PUBLIC-ARTIFACTS.json']=str(D/'REUSED-PUBLIC-ARTIFACTS.json');files['build-spec.py']=str(P(__file__).resolve());files['EXTRA-FILES.json']=str(extras)
manifest={n:{'path':p,'bytes':P(p).stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())}
put('MANIFEST.json',manifest);files['MANIFEST.json']=str(D/'MANIFEST.json')
spec={'prefix':'evidence/2026-11-10-pr1910-completion-qualification/','message':'PR1910 additive completion qualification: exact final source CI, published stage1 and actual boot/Balanced pricing; preserve prior52UI and native source checkpoint by immutable references','receipt':str(D/'GITHUB-CHECKPOINT-RECEIPT.json'),'files':dict(sorted(files.items()))}
put('SPEC-DRAFT.json',spec)
validation={'status':'DRAFT_PATHS_AND_HASHES_VALID_PENDING_TERMINAL_BINDINGS','files':len(files),'bytes':sum(P(p).stat().st_size for p in files.values()),'reused_by_exact_hash':len(reused),'spec_sha256':sha(D/'SPEC-DRAFT.json'),'pending':(['hosted desktop13 terminal evidence'] if status['full_native_smoke']['status']!='PASS_ALL_18_REQUIRED_UNITS' else [])+(['moving-frame raw run/log binding'] if status['moving_frames']['status']!='PASS_EXACT_FINAL_SOURCE' else [])+['Root final merge/tickets readbacks (separate tiny postmerge package)']}
if a.freeze:
 assert status['full_native_smoke']['status']=='PASS_ALL_18_REQUIRED_UNITS','desktop13 terminal recovery not yet proven'
 assert status['moving_frames']['status']=='PASS_EXACT_FINAL_SOURCE','moving-frame raw evidence missing'
 assert not (D/'GITHUB-CHECKPOINT-RECEIPT.json').exists(),'already published; do not mutate'
 shutil.copyfile(D/'SPEC-DRAFT.json',D/'SPEC.json');validation['status']='FROZEN_READY_TO_PUBLISH';validation['spec_sha256']=sha(D/'SPEC.json')
put('SPEC-VALIDATION.json',validation);print(json.dumps(validation))
