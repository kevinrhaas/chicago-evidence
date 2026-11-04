#!/usr/bin/env python3
"""One ROOT-admitted NEW single-skin garment rebind prototype; no source writes."""
import argparse,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,d):Path(p).write_text(json.dumps(d,indent=2)+'\n')
def git(root,*args,check=True):return subprocess.run(['git','--no-optional-locks','-C',str(root),*args],check=check,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'),timeout=30)
def source(root,expected):
 assert set(expected)=={'HEAD','TREE','APP','semantic_index_sha256'}
 for k in ['HEAD','TREE','APP']:assert re.fullmatch('[a-f0-9]{40}',expected[k])
 assert git(root,'rev-parse','HEAD').stdout.decode().strip()==expected['HEAD']
 assert git(root,'rev-parse','--verify','MERGE_HEAD',check=False).returncode!=0
 assert git(root,'diff','--quiet',check=False).returncode==0,'Unstaged source differs'
 assert not git(root,'ls-files','--others','--exclude-standard','-z').stdout,'Untracked source'
 rows=[]
 for raw in git(root,'ls-tree','-r','-z',expected['TREE']).stdout.split(b'\0'):
  if raw:
   info,path=raw.split(b'\t',1);mode,kind,oid=info.split();rows.append((path,mode+b' '+oid+b' 0\t'+path+b'\0'))
 staged=b''.join(row for _,row in sorted(rows))
 assert git(root,'ls-files','--stage','-z').stdout==staged,'Exact staged TREE admission differs'
 assert hashlib.sha256(staged).hexdigest()==expected['semantic_index_sha256']
 assert git(root,'rev-parse',expected['TREE']+':chicago/4d').stdout.decode().strip()==expected['APP']
 return dict(expected)
def main():
 p=argparse.ArgumentParser(description='ROOT-only NEW single-skin garment derivation with native rest-weighted rebind; existing1e-6m residual bound and exact protected rig/body/images; original120s. Prototype only.')
 p.add_argument('--root',type=Path,required=True);p.add_argument('--go',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 root=a.root.resolve();app=root/'chicago/4d';out=a.out.resolve();assert not out.is_relative_to(root)and not out.is_relative_to(D)
 go=load(a.go);m=load(D/'MANIFEST.json');assert go['approved']is True and go['policy']=='ROOT_AUTHORIZED_SINGLE_SKIN_GARMENT_REBIND_PROTOTYPE_V3';assert go['manifest_sha256']==sha(D/'MANIFEST.json')
 for n,h in m['fixture_pins'].items():assert sha(D/n)==h,(n,'fixture changed')
 for n,h in m['input_pins'].items():assert sha(n)==h,(n,'input changed')
 assert go['source']==m['source']and m['maximum_position_residual_m']==1e-6
 before=source(root,go['source'])
 lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('guard','/workspace/.cloud-setup/transport-current-20261103/resource_guard.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 rb=g.snapshot();assert g.check(rb)['accepted'];out.mkdir(exist_ok=False);save(out/'SOURCE-BEFORE.json',before)
 cfg=dict(go,app=str(app),cases=m['cases'],input_pins=m['input_pins'],native_canvas_module=m['native_canvas_module'],original_negative_receipt=m['original_negative_receipt'],diagnosis_raw_arrays=m['diagnosis_raw_arrays'],maximum_position_residual_m=m['maximum_position_residual_m']);save(out/'CONFIG.json',cfg)
 prefix=out/'single-skin-rebind';env=dict(os.environ);env.pop('CHICAGO_TICKETS_DIR',None);error=None;result=cleanup=resources=report=after=None
 try:
  q=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(D),'--timeout','120','--','node',str(D/'derive_single_skin.mjs'),str(out/'CONFIG.json'),str(out/'prototype')],env=env,stdout=(out/'SUPERVISOR.stdout').open('xb'),stderr=subprocess.STDOUT)
  result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');resources=g.pair(rb,g.snapshot());report=load(out/'prototype/PROTOTYPE-RECEIPT.json')
  assert q.returncode==result['returncode']==0 and not result['timed_out'];assert result['requested_timeout_seconds']==result['effective_timeout_seconds']==120 and result['timeout_override_reason']is None
  assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted'];assert report['passed']and len(report['files'])==2 and report['native_resources_disposed']
  assert all(r['old_BIN_prefix_exact']and r['encoded_and_native_decoded_images_exact']and r['all_protected_non_garment_streams_palettes_and_world_vertices_exact']and r['native_one_skeleton']for r in report['files']);after=source(root,go['source']);assert before==after
 except BaseException as e:error=repr(e)
 try:after=source(root,go['source'])
 except BaseException as e:error=(error+'; 'if error else'')+'source_after: '+repr(e)
 if resources is None:resources=g.pair(rb,g.snapshot())
 save(out/'CLOSED.json',dict(status='NEW_SINGLE_SKIN_GARMENT_REBIND_PROTOTYPES_CREATED_STRICT_RESIDUAL_AND_PROTECTED_INVARIANTS_PASS_NOT_PHOTO_OR_WORLD_PASS'if error is None else'NONPASS_PROTOTYPES_NOT_ADMITTED',error=error,source_before=before,source_after=after,manifest_sha256=sha(D/'MANIFEST.json'),ROOT_GO_sha256=sha(a.go),result=result,cleanup=cleanup,resources=resources,report=report,new_derived_garment_prototype_only=True,current_assets_written=False,original_single_skin_and_rig_unchanged=True,images_encoded=False,full_optimizer_used=False,browser_or_GPU=False,production_or_photo_acceptance=False))
 print(json.dumps(dict(passed=error is None,out=str(out),error=error)));return 0 if error is None else 1
if __name__=='__main__':raise SystemExit(main())
