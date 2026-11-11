"""Future finite metadata/raw-WEB copy only; ROOT must admit after actual intake closes."""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess
P=Path(__file__).resolve().parent
APP=Path('/dev/shm/chicago-t1789-charles-gate-20261110/chicago/4d')
D=Path('/tmp/T1789-SETTLER-BEFORE-OBSERVATION-PREP-20261111')
Q=Path('/tmp/T1789-SETTLER-SEAT-METADATA-COMPACT-SOURCE-CANDIDATE-20261111')
# Actual S2 intake preparation is sealed; future intake/data facts remain unknown.
I=Path('/tmp/T1789-SETTLER-S2-CAPTURE-INTAKE-20261111/attempt1')
IP=Path('/tmp/T1789-SETTLER-S2-CAPTURE-INTAKE-PREP-20261111')
EXPECTED_SHA='90a44671c3eff3a816a2135a5f5b49abc5a7c94ae4d7377f3826dd0dc498afd0'
OUT=Path('/tmp/T1789-SETTLER-S2-AFTER-OBSERVATION-PREP-20261111')
OLD_S='3d2d9b356db02deed9d406422f754af4de7aa5f0'
S='c9990d8b32517612a94e339a98bd5700436b5689';H='a0ec4b8f47218a9b3e72f1939a84c78960637e70c8f3fb9c2a90148f97bef761'
INCOMING='900d9166e5adf7bcff84214c78fd5f0fdda634b9'
TREE='1dced78ea49426b9f4c4b9f52ef79db47f06facf'
PRIMARY='9453fa44842225bdb9de2c687cf7dca2f8a8211d'
LINEN='494362d1bee5cd0088be4239d3e2bac0d0f95b1686a9dd1d0f45f244ce0ecaa2'
OVERLAY='d9b77de6c203bfbb94a2b513edc051909482a561af856065c95a96bf71341fd1'
BEFORE=[('lod0',[0],Q/'observation-lod0/seat-review.json','0c63bd1fc745611b1b018e243b4019f06ad206bc9c5c9ad0986507461083947a',Path('/tmp/ROOT-T1789-SETTLER-BEFORE-LOD0-OBSERVE-PREP-20261111-03/CLOSED.json'),'9bf1b35c50f8439b2ec642ed7c2bc99d3797f3ca38e4d3f2044d7e0e68ee1862'),('lod123',[1,2,3],Path('/tmp/ROOT-T1789-SETTLER-BEFORE-LOD123-OBSERVE-PREP-20261111/observation-lod123/seat-review.json'),'1646a59976631858362fcf0ac0e354d2b0b719b015eeb46a297da854c0033365',Path('/tmp/ROOT-T1789-SETTLER-BEFORE-LOD123-OBSERVE-PREP-20261111/CLOSED.json'),'68e2a50866a318c77cd5b4cc204a8fc8399e339672bdd485a41a55dcc219cd35')]
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def load(p,limit=8*1024**2):
 assert p.is_file() and not p.is_symlink() and p.stat().st_size<=limit,str(p)
 return json.loads(p.read_bytes())
def fixed(p,h):assert sha(p.read_bytes())==h,str(p)
def facts(p):
 info=p.lstat();assert stat.S_ISREG(info.st_mode) and not p.is_symlink(),str(p)
 h=hashlib.sha256();g=hashlib.sha1(b'blob '+str(info.st_size).encode()+b'\0')
 with p.open('rb') as f:
  while raw:=f.read(1024*1024):h.update(raw);g.update(raw)
 return dict(bytes=info.st_size,sha256=h.hexdigest(),git_blob=g.hexdigest())
def same(p,r):
 value=facts(p);assert all(value[k]==r[k] for k in ('bytes','sha256')),str(p)
def dump(p,d):
 assert not p.exists();p.write_text(json.dumps(d,indent=2)+'\n')
def source_current():
 env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
 def git(*a):return subprocess.check_output(['git','-C',str(APP),*a],env=env,text=True).strip()
 assert git('rev-parse','HEAD')==S and git('status','--porcelain=v1','--untracked-files=no')==''
 assert git('show','-s','--format=%P','HEAD').split()==[OLD_S,INCOMING] and git('rev-parse','HEAD^{tree}')==TREE
 assert git('rev-parse','refs/heads/steward/t1789-charles-woven-coat-20261110')==PRIMARY
 f=Path('/tmp/t1789-settler-s2-source-full-gate-prep-20261111/FREEZE.json');fixed(f,'97a2d891a72d62898170279ace4c2832fe76dd36e4719c84a3fd68e408f7133f');freeze=load(f);rows=freeze['rows'];assert len(rows)==301 and freeze['head']==OLD_S and freeze['incoming_dev']==INCOMING and freeze['index_tree']==TREE
 for r in rows:
  q=APP.parents[1]/r['file'];same(q,r);assert ('100755' if q.stat().st_mode&stat.S_IXUSR else '100644')==r['Git_mode']
 for name in freeze['deleted_paths']:assert not (APP.parents[1]/name).exists() and not (APP.parents[1]/name).is_symlink()
 post=Path('/tmp/ROOT-T1789-LINEN-S2-POSTGATE-PREP-20261111')
 proofs=[('COMMIT','COMMIT','f23d522314644a09b352a76323b65967047d6851574a6c1296dd330879fc8197'),('PREFLIGHT','PREFLIGHT','ceac2412b051bcbf0b2d6b5b26509fdab155005496ce70b1c95a55b723482f64'),('PUSH','PUSH','a2e5177a4eb300f764c69c76769861ce3c63bfb893c9a62b19ab8e2dd8a7404f'),('REMOTE-VERIFY','REMOTE','c34c7d644ba46e05b1b83497601fddabb71c52278c567412b1e7ea741026c758')]
 for phase,name,h in proofs:
  q=post/phase/'CLOSED.json';fixed(q,h);c=load(q);assert c['accepted']
  receipt=post/phase/(name+'-RECEIPT.json');fixed(receipt,c['receipt_SHA256']);r=load(receipt);assert r['head']==S and r['tree']==TREE
 author=Path('/tmp/ROOT-T1789-LINEN-S2-REQUEST-AUTHORING-PREP-20261111')
 fixed(author/'CLOSED.json','d26ea775ba94a0674710ae25cd311fc2b6c8b7560e52459004a9cf9d66835c2b');assert load(author/'CLOSED.json')['accepted']
 fixed(author/'AUTHORING.json','74283e0192980920f492b004991a4159b8541599c86d34a91ab92f1ab91c3860');ar=load(author/'AUTHORING.json');assert ar['source_commit']==ar['definition_commit']==S and ar['review_request_H2']==H and ar['tree']==TREE
 fixed(author/'request/clothing-capture-v2.json',H);assert load(author/'request/clothing-capture-v2.json')['basis_revision']==S
 fixed(D/'MANIFEST.json','3f101f517e9c54ee20a7c25474fa4131a50e4543135977f6f78c40b50579f3c1');old=load(D/'MANIFEST.json');assert old['source_commit']==OLD_S
 for r in old['old_eight']:same(APP/r['file'],r);same(D/'old-eight'/r['file'],r)
 fixed(D/'fixture-baseline.json','22a4b9f10a7093b3b1fe5f2d1414365b984d4c85fb4e556f81a5843e08d576fa');assert sha((APP/'data/humans/fixture.measure.json').read_bytes())==sha((D/'fixture-baseline.json').read_bytes())
 return dict(current_source_commit=S,historical_before_source_commit=OLD_S,tree=TREE,clean_tracked=True,all301_current_frozen_bytes_modes=True,protected_primary_ref=PRIMARY,actual_old8_fixture_and_private8_unchanged=True)

def main():
 assert IP is not None and I is not None and isinstance(EXPECTED_SHA,str),'sealed Storage intake binding required'
 V=I/'validated8'
 assert not OUT.exists(),'fresh output only; preserve any first failed preparation'
 # Require actual accepted intake. No archive download/extraction/GLB decode here.
 fixed(IP/'EXPECTED.json',EXPECTED_SHA)
 e=load(IP/'EXPECTED.json');assert e['source']==S and e['request_SHA256']==H and e['run_id']==43018920928
 closed=load(IP/'validate.CLOSED.json');intake=load(I/'INTAKE.json')
 assert closed['mode']=='validate' and closed['accepted'] and closed['result']['returncode']==0 and not closed['result']['timed_out'] and closed['result']['requested_timeout_seconds']==closed['result']['effective_timeout_seconds']==120 and closed['result']['timeout_override_reason'] is None
 assert closed['cleanup']['cleanup_complete'] and not closed['cleanup']['remaining_owned_children'] and closed['resources']['accepted']
 assert intake['status']=='CANONICAL_PARENTS_RECEIVED_VERIFIED_UNINSTALLED' and intake['source']==S and intake['request_SHA256']==H and intake['run_id']==43018920928
 assert intake['all_inventory_members_CRC_SHA256_GitOID_verified'] and intake['APP_changes'] is False and intake['native_install'] is False and intake['native_geometry_decode'] is False and intake['pose_photo_fit_accepted'] is False
 assert V.is_dir() and not V.is_symlink() and (V/'CAPTURE.json').is_file() and not (V/'CAPTURE.json').is_symlink() and (V/'CAPTURE.json').stat().st_size<=4*1024**2
 capture_raw=(V/'CAPTURE.json').read_bytes();assert sha(capture_raw)==intake['CAPTURE_SHA256'];capture=json.loads(capture_raw)
 assert capture['schema']=='t1789_canonical_parent_capture_v2' and capture['status']=='CANONICAL_PARENT_CAPTURE_ONLY' and capture['phase']=='CLOSED' and 'error' not in capture and 'closing_error' not in capture
 assert capture['source_sha']==capture['driver_sha']==capture['definition_sha']==S and capture['manifest_sha256']==H
 assert capture['definition_ref']==e['definition_ref'] and capture['request_template_sha256']==e['template_SHA256'] and capture['capture_owner_sha256']==e['owner_SHA256'] and capture['canonical_owner_blobs']==e['canonical_owner_blobs']
 assert all(capture[k] is False for k in ['release','install','material_applied','production_eligible','native_fit_accepted','photo_accepted'])
 assert capture['source_before'] is not None and capture['source_before']==capture['source_after'] and capture['driver_before'] is not None and capture['driver_before']==capture['driver_after']
 assert all(capture['workflow_run'][k]==v for k,v in e['workflow_lineage'].items())
 expected=set(e['parent_paths']);parents={r['file']:r for r in capture['parent_hashes']};selected={r['file']:r for r in intake['selected8']}
 assert len(capture['parent_hashes'])==len(parents)==len(intake['selected8'])==len(selected)==8 and set(parents)==set(selected)==expected
 assert {p.relative_to(V).as_posix() for p in V.rglob('*') if p.is_file()}==expected|{'CAPTURE.json'}
 actual=[]
 for name,r in sorted(parents.items()):
  assert all(r[k]==selected[name][k] for k in ['bytes','sha256','git_blob']) and facts(V/name)=={k:r[k] for k in ['bytes','sha256','git_blob']}
  file=name.removeprefix('settler_1812/parents/');assert file.startswith('assets/humans/')
  if '/web/' in file:assert r['bytes']<=16*1024**2
  actual.append(dict(file=file,bytes=r['bytes'],sha256=r['sha256']))
 before=source_current()
 fixed(Q/'before-request.json','59e3c230439e5ff64b739da24ae3935403e54d30f256c5df5505997bde18e5d0');base=load(Q/'before-request.json');fixed(Q/'SOURCE.patch',OVERLAY)
 assert base['source_commit']==base['observer_base_commit']==base['runtime_base_commit']==OLD_S and base['observer_overlay']['base_commit']==OLD_S and base['observer_overlay']['patch_sha256']==OVERLAY and len(base['observer_files'])==7
 for r in base['observer_files']:same(Q/'observer/chicago/4d'/r['file'],r);same(APP/r['file'],r)
 for label,lods,path,h,closure,ch in BEFORE:
  fixed(path,h);fixed(closure,ch);assert load(closure)['accepted'];b=load(path)
  assert b['status']=='NATIVE_SAMPLED_OBSERVATION_COMPLETE' and b['native_fit_accepted'] is False and b['selected_lods']==lods and b['request']['role']=='before' and b['request']['source_commit']==OLD_S and b['request']['observer_files']==base['observer_files'] and len(b['runs'])==2*len(lods)
 fixed(D/'runtime-inventory.json','f8c8a49eac5c53ecf128acee4524bf0df1f4ba7d9203eb5fcc520a61c49ccec3');old_runtime=load(D/'runtime-inventory.json');modules=[r for r in old_runtime['files'] if r['file'].startswith('walk/')]
 assert len(modules)==16 and sum(r['bytes'] for r in modules)==2452425
 for r in modules:same(D/'runtime'/r['file'],r);same(APP/r['file'].replace('walk/','renderers/web/',1),r)
 runtime_rows=[dict(r) for r in modules]+[dict(file=r['file'].replace('assets/humans/','data/humans/',1),bytes=r['bytes'],sha256=r['sha256']) for r in actual if '/web/' in r['file']]
 total=sum(r['bytes'] for r in runtime_rows);assert len(runtime_rows)==20 and total<=32*1024**2,'raw published projection32MiB bound'
 # Current original guard snapshot is admitted by run.py; reserve future copying too.
 guard=load(P/'copy.before.json');reserve=total+len(capture_raw)+1024**2
 assert guard['available_memory_bytes']-reserve>=4*1024**3 and guard['tmp_free_bytes']-reserve>=1024**3 and guard['workspace_free_bytes']>=512*1024**2
 OUT.mkdir();runtime=OUT/'runtime';runtime.mkdir()
 for r in runtime_rows:
  src=APP/r['file'].replace('walk/','renderers/web/',1) if r['file'].startswith('walk/') else V/'settler_1812/parents'/r['file'].replace('data/humans/','assets/humans/',1)
  dst=runtime/r['file'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);dst.chmod(0o444);same(dst,r)
 receipt=OUT/'CAPTURE.json';receipt.write_bytes(capture_raw);receipt.chmod(0o444)
 inventory=dict(schema='t1789_native_runtime_inventory_v1',runtime_base_commit=S,scope='Actual validated canonical captured raw WEBs plus exact unchanged16 baseline runtime modules; no asset install or DEV publication',files=sorted(runtime_rows,key=lambda r:r['file']))
 dump(OUT/'runtime-inventory.json',inventory);inventory_sha=sha((OUT/'runtime-inventory.json').read_bytes());commands=[]
 for label,lods,before_path,before_sha,closure,ch in BEFORE:
  request=dict(base);request.update(role='after',source_commit=S,definition_commit=S,observer_base_commit=S,runtime_base_commit=S,source_patch_sha256=LINEN,receipt_kind='canonical_capture',receipt_sha256=sha(capture_raw),runtime_inventory_sha256=inventory_sha,parents=actual,before_observation_sha256=before_sha)
  req=OUT/('after-request-'+label+'.json');dump(req,request);request_sha=sha(req.read_bytes())
  argv=['node',str(APP/'tools/human_teamster.mjs'),'--published',str(runtime),'--asset-ids','settler_1812','--lods',','.join(map(str,lods)),'--seat-review-request',str(req),'--seat-review-request-sha256',request_sha,'--seat-review-receipt',str(receipt),'--seat-review-runtime-inventory',str(OUT/'runtime-inventory.json'),'--seat-review-before-observation',str(before_path),'--output',str(OUT/('observation-'+label))]
  cmd=dict(status='PREPARED_ACTUAL_AFTER_COMMAND_NOT_EXECUTED',argv=argv,selected_lods=lods,original_supervisor_timeout_seconds=600,requires_ROOT_sole_lock_V2_original_resource_guard_pair_cleanup=True,maximum_pictures=26*len(lods),maximum_output_bytes=8*1024**2*len(lods),expected_runs=2*len(lods),expected_total_poses=18*len(lods),matching_before_sha256=before_sha)
  name='OBSERVE-'+label.upper()+'-COMMAND.json';dump(OUT/name,cmd);commands.append(dict(command=name,command_sha256=sha((OUT/name).read_bytes()),request=req.name,request_sha256=request_sha,before_sha256=before_sha))
 after=source_current();assert before==after
 assert {p.relative_to(runtime).as_posix() for p in runtime.rglob('*') if p.is_file()}=={r['file'] for r in runtime_rows}
 for r in runtime_rows:same(runtime/r['file'],r)
 assert sha((V/'CAPTURE.json').read_bytes())==sha(capture_raw)
 for r in capture['parent_hashes']:assert facts(V/r['file'])=={k:r[k] for k in ['bytes','sha256','git_blob']}
 manifest=dict(status='ACTUAL_AFTER_BINDINGS_PREPARED_NATIVE_OBSERVATIONS_UNRUN',source_commit=S,definition_commit=S,historical_before_source_commit=OLD_S,capture_run_id=43018920928,capture_request_H=H,capture_sha256=sha(capture_raw),intake_sha256=sha((I/'INTAKE.json').read_bytes()),intake_validate_closed_sha256=sha((IP/'validate.CLOSED.json').read_bytes()),captured_parents=actual,observer_overlay_origin_base=OLD_S,actual_observer_execution_source=S,observer_overlay_patch_sha256=OVERLAY,garment_source_patch_sha256=LINEN,runtime_inventory_sha256=inventory_sha,runtime_projection_bytes=total,source_before=before,source_after=after,commands=commands,release=False,install=False,native_fit_accepted=False,photographic_accepted=False,browser_run=False,glb_decode=False)
 dump(OUT/'MANIFEST.json',manifest);print(json.dumps(dict(output=str(OUT),manifest_sha256=sha((OUT/'MANIFEST.json').read_bytes()),runtime_bytes=total,capture_sha256=sha(capture_raw),commands=commands)))
if __name__=='__main__':main()
