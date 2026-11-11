"""Prepared only: actual accepted checkpoint-only S4 -> fresh separate metadata-only driver/request."""
from pathlib import Path
import subprocess,json,hashlib,datetime,re,types,os,stat,argparse
P=Path(__file__).resolve().parent
ROOT=Path('/dev/shm/chicago-t1789-charles-gate-20261110');APP=ROOT/'chicago/4d'
POST=Path('/tmp/ROOT-T1789-LINEN-S4-CHECKPOINT-POSTGATE-PREP-20261111')
POST_CHAIN_SHA='dba9a9bbc1277ac1b4ad8be76418961d6695531e5941b3d5aa14f81a289d9ffa'
POST_PINS_SHA='94608e792df4dbee594a7c3b19a53fede1046192f39117f371bd5af55c3f201c'
OLD='0a57979840bea7c37ba41ba4e24133a9510b59b9'
BRANCH='steward/t1789-1812-loose-linen-seat-20261111'
OWNER_SHA='efcd568ebf5cfb16609666aa1bd4e0411b34b390deaa680773f8653b24faefb5'
TEMPLATE_SHA='83ba2447416107faa1d4a40813b5d414eda35343df6818979217fe7d52ffff79'
WORKFLOW_SHA='4a73bb1b454dcb7d8d40e01bc1d801d635573465fd400b5f356e9eed8a535c53'
DRIVER=P/'driver';OUTPUT=P/'request'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,body):
    path=P/name;assert not path.exists(),str(path)
    path.write_text(json.dumps(body,indent=2)+'\n')
assert sha(POST/'chain.py')==POST_CHAIN_SHA and sha(POST/'SOURCE-PINS.json')==POST_PINS_SHA
for name,pin in json.loads((POST/'SOURCE-PINS.json').read_text()).items():assert sha(POST/name)==pin,name
parser=argparse.ArgumentParser();parser.add_argument('--binding-sha256',required=True);args=parser.parse_args()
BINDING_SHA=args.binding_sha256;assert re.fullmatch(r'[0-9a-f]{64}',BINDING_SHA)
binding_path=POST/'BINDING.json'
assert binding_path.is_file() and not binding_path.is_symlink() and sha(binding_path)==BINDING_SHA
B=json.loads(binding_path.read_text())
assert B['status']=='ROOT_REVIEWED_ACTUAL_S4_ALL16_POSTGATE_BINDING'
assert B['expected_head']==OLD and B['expected_branch']==BRANCH
assert B['source_checkpoint_only'] is True and B['needs_final_DEV_integration'] is True and B['merge_ready'] is False
for key in ('freeze_SHA256','aggregate_SHA256','apply_receipt_SHA256'):assert re.fullmatch(r'[0-9a-f]{64}',B[key])
for key in ('index_tree','expected_DEV'):assert re.fullmatch(r'[0-9a-f]{40}',B[key])
TREE,FREEZE_SHA=B['index_tree'],B['freeze_SHA256']
# One real module dictionary owns function globals; do not mutate a runpy result copy.
library=types.ModuleType('t1789_s4_postgate_authoring_library')
library.__file__=str(POST/'chain.py')
exec(compile((POST/'chain.py').read_bytes(),str(POST/'chain.py'),'exec'),library.__dict__)
C=library.__dict__
assert C['__name__']!='__main__'
C.update(B=B,BINDING_SHA=BINDING_SHA,TREE=TREE,FREEZE_SHA=FREEZE_SHA)
for name in ('qualified_gate','prior','verify_worktree'):assert C[name].__globals__ is C
assert TREE==C['SOURCE_TREE'] and FREEZE_SHA==C['SOURCE_FREEZE_SHA'] and B['apply_receipt_SHA256']==C['SOURCE_APPLY_SHA']
d,a=C['qualified_gate']()
receipts={};proof={}
for phase,name in [('COMMIT','COMMIT'),('PREFLIGHT','PREFLIGHT'),('PUSH','PUSH'),('REMOTE-VERIFY','REMOTE')]:
    closed_path=POST/phase/'CLOSED.json';closed=json.loads(closed_path.read_text())
    r,k,g=closed['result'],closed['cleanup'],closed['resources']
    assert closed['accepted'] and r['returncode']==0 and not r['timed_out']
    assert r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None
    assert k['cleanup_complete'] and not k['remaining_owned_children'] and g['accepted']
    assert closed['binding_SHA256']==BINDING_SHA
    receipt=C['prior'](phase,name);assert receipt['binding_SHA256']==BINDING_SHA;receipts[phase]=receipt
    proof[phase]={'CLOSED_SHA256':sha(closed_path),'receipt_SHA256':closed['receipt_SHA256']}
commit=receipts['COMMIT'];source=commit['head']
assert re.fullmatch(r'[0-9a-f]{40}',source) and source!=OLD
assert commit['parents']==[OLD] and commit['tree']==TREE and commit['freeze_SHA256']==FREEZE_SHA and commit['aggregate_SHA256']==B['aggregate_SHA256']
assert commit['all16_source_parts_pass'] and commit['frozen301_preserved'] and commit['native8_fixture_unchanged']
assert all(v['head']==source and v['tree']==TREE for v in receipts.values())
assert all(v['source_checkpoint_only'] is True and v['needs_final_DEV_integration'] is True and v['merge_ready'] is False for v in receipts.values())
preflight=receipts['PREFLIGHT'];assert preflight['changelog_question'] and preflight['ID_collision_question']
pushed=receipts['PUSH'];assert pushed['branch']==BRANCH and pushed['remote_expected_before']==pushed['advertised_remote_oid']==OLD and pushed['force'] is False
remote=receipts['REMOTE-VERIFY'];assert remote['parents']==[OLD] and remote['freeze_SHA256']==FREEZE_SHA and remote['all301_local_frozen_SHA256_bytes_modes_preserved']
C['verify_worktree'](d,source,True)
assert C['git']('show','-s','--format=%P','HEAD').split()==[OLD]
assert C['remote_head'](BRANCH)==source,'immutable S4 branch changed before authoring'
assert sha(ROOT/'.github/workflows/chicago-4d-humans.yml')==WORKFLOW_SHA
assert not DRIVER.exists() and not OUTPUT.exists() and not (P/'AUTHORING.json').exists()
assert not P.resolve().is_relative_to(ROOT.resolve()) and not P.is_symlink()
save('AUTHORING-INTENT.json',{'status':'METADATA_ONLY_INCOMPLETE','source':source,'definition':source,'tree':TREE,'freeze_SHA256':FREEZE_SHA,'postgate_receipts':proof,'postgate_binding_SHA256':BINDING_SHA,'geometry_producer':False,'dispatch':False,'APP_writes':False})
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
assert C['remote_head'](BRANCH)==source,'immutable S4 branch changed during authoring'
rows=[{'file':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(OUTPUT.rglob('*')) if f.is_file()]
receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXTERNAL_S4_REQUEST_GENERATED_FOR_ROOT_REVIEW_NOT_DISPATCHED',
 'source_commit':source,'definition_commit':source,'parents':[OLD],'tree':TREE,'source_app':str(APP),'driver_app':str(DAPP),'physically_separate_checkouts':True,
 'freeze_SHA256':FREEZE_SHA,'all16_source_parts_verified':True,'frozen301_prepost_verified':True,'old_native8_and_fixture_preserved':True,'postgate_receipts':proof,'postgate_binding_SHA256':BINDING_SHA,'aggregate_SHA256':B['aggregate_SHA256'],
 'template_sha256':TEMPLATE_SHA,'owner_sha256':OWNER_SHA,'workflow_sha256':WORKFLOW_SHA,'definition_ref':definition_ref,'driver_checkedout_files':files,
 'selected_unique_input_bindings':245,'input_binding_scope':'245 selected physical bindings plus exact clean source Git identity; not a complete consumed-dependency claim','review_request_H4':H,'files':rows,'source_or_driver_tracked_file_mutation':False,'geometry_producer_executed':False,
 'source_checkpoint_only':True,'needs_final_DEV_integration':True,'merge_ready':False,
 'DEV_observations_from_actual_checkpoint_phases':{'commit':commit['fresh_DEV_observed'],'preflight':preflight['fresh_DEV'],'push':pushed['fresh_DEV_before_push'],'remote_proof':remote['remote_DEV_observed']},
 'source_includes_DEV_at_push':pushed['source_includes_fresh_DEV'],
 'bake_or_browser':False,'dispatch':False,'DEV_merge':False,'production':False,'release':False,'install':False,'native_fit_accepted':False}
save('AUTHORING.json',receipt);print(json.dumps(receipt))
