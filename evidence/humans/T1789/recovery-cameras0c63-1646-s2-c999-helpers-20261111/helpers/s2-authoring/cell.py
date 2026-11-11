"""Prepared only: actual accepted S2 -> fresh separate metadata-only driver/request."""
from pathlib import Path
import subprocess,json,hashlib,datetime,re,runpy,os,stat
P=Path(__file__).resolve().parent
ROOT=Path('/dev/shm/chicago-t1789-charles-gate-20261110');APP=ROOT/'chicago/4d'
POST=Path('/tmp/ROOT-T1789-LINEN-S2-POSTGATE-PREP-20261111')
POST_CHAIN_SHA='dc6448b4749e89667403edf384450d0d3f8c2fdf3bbe8ee9cf663bb8332a9c37'
POST_PINS_SHA='1555682f34915060e1f33855babb2952f4201ad2846584941a5fcc11efff52d4'
OLD='3d2d9b356db02deed9d406422f754af4de7aa5f0'
INCOMING='900d9166e5adf7bcff84214c78fd5f0fdda634b9'
TREE='1dced78ea49426b9f4c4b9f52ef79db47f06facf'
FREEZE_SHA='97a2d891a72d62898170279ace4c2832fe76dd36e4719c84a3fd68e408f7133f'
BRANCH='steward/t1789-1812-loose-linen-seat-20261111'
OWNER_SHA='d70e00fa9984b72303f57a00b5e036ab6803f6840bcd51f94f5f724ad892b943'
TEMPLATE_SHA='83ba2447416107faa1d4a40813b5d414eda35343df6818979217fe7d52ffff79'
WORKFLOW_SHA='5efef07605ae5446c8d6084f65d9c58035f27ee3893de4b937e4ae6ec0844e88'
DRIVER=P/'driver';OUTPUT=P/'request'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,body):
    path=P/name;assert not path.exists(),str(path)
    path.write_text(json.dumps(body,indent=2)+'\n')
assert sha(POST/'chain.py')==POST_CHAIN_SHA and sha(POST/'SOURCE-PINS.json')==POST_PINS_SHA
for name,pin in json.loads((POST/'SOURCE-PINS.json').read_text()).items():assert sha(POST/name)==pin,name
# Verified future import defines helpers only; its phase main guard is not executed.
C=runpy.run_path(str(POST/'chain.py'),run_name='prepared_postgate_library')
d,a=C['qualified_gate']()
receipts={};proof={}
for phase,name in [('COMMIT','COMMIT'),('PREFLIGHT','PREFLIGHT'),('PUSH','PUSH'),('REMOTE-VERIFY','REMOTE')]:
    closed_path=POST/phase/'CLOSED.json';closed=json.loads(closed_path.read_text())
    r,k,g=closed['result'],closed['cleanup'],closed['resources']
    assert closed['accepted'] and r['returncode']==0 and not r['timed_out']
    assert r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None
    assert k['cleanup_complete'] and not k['remaining_owned_children'] and g['accepted']
    receipt=C['prior'](phase,name);receipts[phase]=receipt
    proof[phase]={'CLOSED_SHA256':sha(closed_path),'receipt_SHA256':closed['receipt_SHA256']}
commit=receipts['COMMIT'];source=commit['head']
assert re.fullmatch(r'[0-9a-f]{40}',source) and source!=OLD
assert commit['parents']==[OLD,INCOMING] and commit['tree']==TREE and commit['freeze_SHA256']==FREEZE_SHA
assert commit['all16_source_parts_pass'] and commit['frozen301_preserved'] and commit['native8_fixture_unchanged']
assert all(v['head']==source and v['tree']==TREE for v in receipts.values())
preflight=receipts['PREFLIGHT'];assert preflight['changelog_question'] and preflight['ID_collision_question']
pushed=receipts['PUSH'];assert pushed['branch']==BRANCH and pushed['remote_expected_before']==pushed['advertised_remote_oid']==OLD and pushed['force'] is False
remote=receipts['REMOTE-VERIFY'];assert remote['parents']==[OLD,INCOMING] and remote['freeze_SHA256']==FREEZE_SHA and remote['all301_local_frozen_SHA256_bytes_modes_preserved']
C['verify_worktree'](d,source,True)
assert C['git']('show','-s','--format=%P','HEAD').split()==[OLD,INCOMING]
assert C['remote_head'](BRANCH)==source,'immutable S2 branch changed before authoring'
assert sha(ROOT/'.github/workflows/chicago-4d-humans.yml')==WORKFLOW_SHA
assert not DRIVER.exists() and not OUTPUT.exists() and not (P/'AUTHORING.json').exists()
assert not P.resolve().is_relative_to(ROOT.resolve()) and not P.is_symlink()
save('AUTHORING-INTENT.json',{'status':'METADATA_ONLY_INCOMPLETE','source':source,'definition':source,'tree':TREE,'freeze_SHA256':FREEZE_SHA,'postgate_receipts':proof,'geometry_producer':False,'dispatch':False,'APP_writes':False})
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
assert C['git']('show','-s','--format=%P','HEAD').split()==[OLD,INCOMING]
assert git(DRIVER,'rev-parse','HEAD')==source and git(DRIVER,'status','--porcelain=v1')==''
assert all(sha(DAPP/f)==sha(APP/f) for f in files)
assert C['remote_head'](BRANCH)==source,'immutable S2 branch changed during authoring'
rows=[{'file':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(OUTPUT.rglob('*')) if f.is_file()]
receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXTERNAL_S2_REQUEST_GENERATED_FOR_ROOT_REVIEW_NOT_DISPATCHED',
 'source_commit':source,'definition_commit':source,'parents':[OLD,INCOMING],'tree':TREE,'source_app':str(APP),'driver_app':str(DAPP),'physically_separate_checkouts':True,
 'freeze_SHA256':FREEZE_SHA,'all16_source_parts_verified':True,'frozen301_prepost_verified':True,'old_native8_and_fixture_preserved':True,'postgate_receipts':proof,
 'template_sha256':TEMPLATE_SHA,'owner_sha256':OWNER_SHA,'workflow_sha256':WORKFLOW_SHA,'definition_ref':definition_ref,'driver_checkedout_files':files,
 'selected_unique_input_bindings':245,'review_request_H2':H,'files':rows,'source_or_driver_tracked_file_mutation':False,'geometry_producer_executed':False,
 'bake_or_browser':False,'dispatch':False,'DEV_merge':False,'production':False,'release':False,'install':False,'native_fit_accepted':False}
save('AUTHORING.json',receipt);print(json.dumps(receipt))
