"""Prepared only: actual accepted checkpoint-only S3 -> fresh separate metadata-only driver/request."""
from pathlib import Path
import subprocess,json,hashlib,datetime,re,types,os,stat,argparse
P=Path(__file__).resolve().parent
ROOT=Path('/dev/shm/chicago-t1789-charles-gate-20261110');APP=ROOT/'chicago/4d'
POST=Path('/tmp/ROOT-T1789-LINEN-S3-CHECKPOINT-POSTGATE-PREP-20261111')
POST_CHAIN_SHA='b2340e11d629185d231042819c9e7f967fedcd1a10674173a5355bd1a1b613d6'
POST_PINS_SHA='cb40a9f5d4fb57ffc2407fcb6191b814ebc3735bb850f86af534506ced38d6e8'
OLD='c9990d8b32517612a94e339a98bd5700436b5689'
BRANCH='steward/t1789-1812-loose-linen-seat-20261111'
OWNER_SHA='efcd568ebf5cfb16609666aa1bd4e0411b34b390deaa680773f8653b24faefb5'
TEMPLATE_SHA='83ba2447416107faa1d4a40813b5d414eda35343df6818979217fe7d52ffff79'
WORKFLOW_SHA='5efef07605ae5446c8d6084f65d9c58035f27ee3893de4b937e4ae6ec0844e88'
DRIVER=P/'driver';OUTPUT=P/'request'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,body):
    path=P/name;assert not path.exists(),str(path)
    path.write_text(json.dumps(body,indent=2)+'\n')
# Actual independent recovery closes its own 120s cell; original PUSH stays interrupted.
RECOVERY=Path('/tmp/ROOT-T1789-S3-RECOVER-REMOTE-PREP-20261111')
RECOVERY_CODE_SHA='da6fa673f462ffe7be1d6c111dc84fff557e7711f6357cff3bf5e2304cd03e53'
RECOVERY_PINS_SHA='ee3dbf1fe5b8a8a3bbc8aa8357569248046c82e6e6989d6fb9fc3ebb7db5ab15'
RECOVERY_CLOSED_SHA='24d7d5ba28522790dd76aeefadf3343883325d51b543f49df6c1035275a7d437'
RECONCILIATION_SHA='6d6e22d3b09fd9d6255ceb7168ab91c435d4dd2ecd90901ddbc9b4213aa8691c'
SOURCE='0a57979840bea7c37ba41ba4e24133a9510b59b9'
parser=argparse.ArgumentParser();parser.add_argument('--binding-sha256',required=True);args=parser.parse_args()
BINDING_SHA=args.binding_sha256
assert BINDING_SHA=='31d8a21d37faadccbb49fd6819604003ad5e12c0a3df580ecfb0412ddd3d1f4e'
assert sha(RECOVERY/'recover.py')==RECOVERY_CODE_SHA and sha(RECOVERY/'SOURCE-PINS.json')==RECOVERY_PINS_SHA
recovery_library=types.ModuleType('t1789_s3_recovered_authoring_library');recovery_library.__file__=str(RECOVERY/'recover.py')
exec(compile((RECOVERY/'recover.py').read_bytes(),str(RECOVERY/'recover.py'),'exec'),recovery_library.__dict__)
R=recovery_library.__dict__;assert R['__name__']!='__main__' and R['source_context'].__globals__ is R
C,d,a,receipts,interruption=R['source_context'](BINDING_SHA)
B=C['B'];TREE=C['TREE'];FREEZE_SHA=C['FREEZE_SHA']
for name in ('qualified_gate','prior','verify_worktree'):assert C[name].__globals__ is C
closed_path=RECOVERY/'CLOSED.json';reconciliation_path=RECOVERY/'RECONCILIATION-RECEIPT.json'
assert sha(closed_path)==RECOVERY_CLOSED_SHA and sha(reconciliation_path)==RECONCILIATION_SHA
closed=R['load'](closed_path);C['original_closure'](closed,120)
assert closed['binding_SHA256']==BINDING_SHA and closed['reconciliation_receipt_SHA256']==RECONCILIATION_SHA
reconciliation=R['load'](reconciliation_path)
for key,value in interruption.items():assert reconciliation[key]==value,key
assert reconciliation['status']=='FRESH_S3_REMOTE_RECONCILIATION_COMPLETE_NOT_ORIGINAL_PUSH_CLOSURE'
assert reconciliation['source']==SOURCE and reconciliation['tree']==TREE and reconciliation['parents']==[OLD]
assert reconciliation['all16_actual_source_parts_verified'] and reconciliation['source301_native8_fixture_protected9453_verified_now']
for q in (closed,reconciliation):
    assert q['original_PUSH_closure_accepted'] is False and q['original_PUSH_supervised_returncode'] is None and q['original_PUSH_cleanup_complete'] is None
    assert q['push_retried'] is False
assert reconciliation['remote_feature_verified']==SOURCE and reconciliation['remote_four_entries_two_source_bodies_verified']
assert reconciliation['source_checkpoint_only'] is True and reconciliation['needs_final_DEV_integration'] is True and reconciliation['merge_ready'] is False
remote_path=RECOVERY/'REMOTE-VERIFY/REMOTE-RECEIPT.json'
assert reconciliation['remote_proof']==str(remote_path) and sha(remote_path)==reconciliation['remote_proof_SHA256']
remote=R['load'](remote_path)
assert remote['head']==SOURCE and remote['tree']==TREE and remote['parents']==[OLD] and remote['binding_SHA256']==BINDING_SHA
assert remote['freeze_SHA256']==FREEZE_SHA and remote['all301_local_frozen_SHA256_bytes_modes_preserved']
assert len(remote['remote_changed_entries'])==4 and sum(r['remote_body_verified'] for r in remote['remote_changed_entries'])==2
assert remote['source_checkpoint_only'] is True and remote['needs_final_DEV_integration'] is True and remote['merge_ready'] is False
assert not remote['DEV_merge'] and not remote['production']
proof={}
for phase in ('COMMIT','PREFLIGHT'):
    original_closed=R['load'](POST/phase/'CLOSED.json')
    proof[phase]={'CLOSED_SHA256':sha(POST/phase/'CLOSED.json'),'receipt_SHA256':original_closed['receipt_SHA256']}
recovery_proof={'directory':str(RECOVERY),'recover_code_SHA256':RECOVERY_CODE_SHA,'source_pins_SHA256':RECOVERY_PINS_SHA,'CLOSED_SHA256':RECOVERY_CLOSED_SHA,'RECONCILIATION_SHA256':RECONCILIATION_SHA,'remote_proof_SHA256':sha(remote_path),'original_PUSH_closure_accepted':False}
commit=receipts['COMMIT'];source=commit['head'];assert source==SOURCE
assert commit['parents']==[OLD] and commit['tree']==TREE and commit['freeze_SHA256']==FREEZE_SHA and commit['aggregate_SHA256']==B['aggregate_SHA256']
assert commit['all16_source_parts_pass'] and commit['frozen301_preserved'] and commit['native8_fixture_unchanged']
assert all(v['head']==source and v['tree']==TREE for v in receipts.values())
assert all(v['source_checkpoint_only'] is True and v['needs_final_DEV_integration'] is True and v['merge_ready'] is False for v in receipts.values())
preflight=receipts['PREFLIGHT'];assert preflight['changelog_question'] and preflight['ID_collision_question']
pushed=receipts['PUSH'];assert pushed['branch']==BRANCH and pushed['remote_expected_before']==pushed['advertised_remote_oid']==OLD and pushed['force'] is False
C['verify_worktree'](d,source,True)
assert C['git']('show','-s','--format=%P','HEAD').split()==[OLD]
assert C['remote_head'](BRANCH)==source,'immutable S3 branch changed before authoring'
assert sha(ROOT/'.github/workflows/chicago-4d-humans.yml')==WORKFLOW_SHA
assert not DRIVER.exists() and not OUTPUT.exists() and not (P/'AUTHORING.json').exists()
assert not P.resolve().is_relative_to(ROOT.resolve()) and not P.is_symlink()
save('AUTHORING-INTENT.json',{'status':'METADATA_ONLY_INCOMPLETE','source':source,'definition':source,'tree':TREE,'freeze_SHA256':FREEZE_SHA,'postgate_receipts':proof,'push_interruption':interruption,'remote_reconciliation':recovery_proof,'postgate_binding_SHA256':BINDING_SHA,'geometry_producer':False,'dispatch':False,'APP_writes':False})
read_env=C['READ_ENV']
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],env=read_env).decode().strip()
def command(args):subprocess.run(args,env=read_env,check=True)
command(['git','clone','--depth','1','--filter=blob:none','--single-branch','--branch',BRANCH,'--no-checkout','https://github.com/kevinrhaas/chicago.git',str(DRIVER)])
command(['git','-C',str(DRIVER),'fetch','--depth','1','--filter=blob:none','origin',source])
files=['tools/human_clothing_capture_v2.py','data/humans/studies/clothing-capture-v2.json','generators/blender.pin',
 'tools/human_teamster_blend.py','tools/human_export.py','tools/human_export.sh','tools/human_skin_canonicalize.py',
 'tools/human_web_texture_inputs.py','tools/web_derivatives.sh','tools/human_contract.py']
command(['git','-C',str(DRIVER),'sparse-checkout','set','--no-cone',*['/chicago/4d/'+r for r in files]])
command(['git','-C',str(DRIVER),'checkout','--detach',source])
assert git(DRIVER,'rev-parse','HEAD')==source and git(DRIVER,'status','--porcelain=v1')==''
assert git(DRIVER,'rev-parse','HEAD^{tree}')==TREE and git(DRIVER,'rev-parse','--show-toplevel')==str(DRIVER.resolve())
DAPP=DRIVER/'chicago/4d';owner=DAPP/'tools/human_clothing_capture_v2.py';template=DAPP/'data/humans/studies/clothing-capture-v2.json'
assert not DRIVER.resolve().is_relative_to(ROOT.resolve()) and not ROOT.resolve().is_relative_to(DRIVER.resolve())
actual={f.relative_to(DAPP).as_posix() for f in DAPP.rglob('*') if f.is_file()}
assert actual==set(files) and all(not (DAPP/f).is_symlink() and stat.S_ISREG((DAPP/f).lstat().st_mode) for f in files)
assert all(sha(DAPP/f)==sha(APP/f) for f in files),'all ten actual driver/source files must agree'
assert sha(owner)==sha(APP/'tools/human_clothing_capture_v2.py')==OWNER_SHA
assert sha(template)==sha(APP/'data/humans/studies/clothing-capture-v2.json')==TEMPLATE_SHA
assert sha(ROOT/'.github/workflows/chicago-4d-humans.yml')==WORKFLOW_SHA
definition_ref='kevinrhaas/chicago/.github/workflows/chicago-4d-humans.yml@refs/heads/'+BRANCH
command(['python',str(owner),'--refresh-request','--source',source,'--source-app',str(APP),
 '--definition-sha',source,'--definition-ref',definition_ref,'--manifest-sha256',TEMPLATE_SHA,'--output',str(OUTPUT)])
assert {f.name for f in OUTPUT.iterdir()}=={'REFRESH.json','clothing-capture-v2.json'}
request=OUTPUT/'clothing-capture-v2.json';raw=request.read_bytes();doc=json.loads(raw);H=hashlib.sha256(raw).hexdigest()
assert doc['basis_revision']==source and doc['schema']=='t1789_clothing_capture_request_v2' and doc['status']=='SOURCE_ONLY_LINEN_CAPTURE_REQUEST'
assert doc['release'] is False and doc['install'] is False and doc['native_fit_accepted'] is False and doc['material_admission'] is None
assert doc['families']==[{'recipe':'data/humans/recipes/settler_1812.json','variant':'settler_1812','assembly':'settler_1812_v1','liberty':'L418'}]
assert len(doc['inputs'])==len({r['file'] for r in doc['inputs']})==245
assert {r['file'] for r in doc['inputs']}=={r['file'] for r in json.loads(template.read_bytes())['inputs']}
refresh=json.loads((OUTPUT/'REFRESH.json').read_bytes())
assert refresh['source_sha']==refresh['driver_sha']==source and refresh['request_sha256']==H and refresh['source_inputs']==245
assert refresh['template_sha256']==TEMPLATE_SHA and refresh['producer_run'] is False and refresh['release'] is False and refresh['install'] is False
C['verify_worktree'](d,source,True)
assert C['git']('show','-s','--format=%P','HEAD').split()==[OLD]
assert git(DRIVER,'rev-parse','HEAD')==source and git(DRIVER,'status','--porcelain=v1')==''
assert all(sha(DAPP/f)==sha(APP/f) for f in files)
assert C['remote_head'](BRANCH)==source,'immutable S3 branch changed during authoring'
rows=[{'file':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(OUTPUT.rglob('*')) if f.is_file()]
receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXTERNAL_S3_REQUEST_GENERATED_FOR_ROOT_REVIEW_NOT_DISPATCHED',
 'source_commit':source,'definition_commit':source,'parents':[OLD],'tree':TREE,'source_app':str(APP),'driver_app':str(DAPP),'physically_separate_checkouts':True,
 'freeze_SHA256':FREEZE_SHA,'all16_source_parts_verified':True,'frozen301_prepost_verified':True,'old_native8_and_fixture_preserved':True,'postgate_receipts':proof,'push_interruption':interruption,'remote_reconciliation':recovery_proof,'postgate_binding_SHA256':BINDING_SHA,'aggregate_SHA256':B['aggregate_SHA256'],
 'template_sha256':TEMPLATE_SHA,'owner_sha256':OWNER_SHA,'workflow_sha256':WORKFLOW_SHA,'definition_ref':definition_ref,'driver_checkedout_files':files,
 'selected_unique_input_bindings':245,'input_binding_scope':'245 selected physical bindings plus exact clean source Git identity; not a complete consumed-dependency claim','review_request_H3':H,'files':rows,'source_or_driver_tracked_file_mutation':False,'geometry_producer_executed':False,
 'source_checkpoint_only':True,'needs_final_DEV_integration':True,'merge_ready':False,
 'DEV_observations_from_actual_checkpoint_phases':{'commit':commit['fresh_DEV_observed'],'preflight':preflight['fresh_DEV'],'push':pushed['fresh_DEV_before_push'],'remote_proof':remote['remote_DEV_observed']},
 'source_includes_DEV_at_push':pushed['source_includes_fresh_DEV'],
 'bake_or_browser':False,'dispatch':False,'DEV_merge':False,'production':False,'release':False,'install':False,'native_fit_accepted':False}
save('AUTHORING.json',receipt);print(json.dumps(receipt))
