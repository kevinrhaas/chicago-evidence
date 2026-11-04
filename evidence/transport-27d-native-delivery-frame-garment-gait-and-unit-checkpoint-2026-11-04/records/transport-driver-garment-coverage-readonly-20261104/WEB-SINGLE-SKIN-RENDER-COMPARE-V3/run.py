#!/usr/bin/env python3
"""One ROOT-admitted current staged-source technical browser fixture; no source writes."""
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
 p=argparse.ArgumentParser(description='ROOT-bound actual successful V3 single-skin rebind WEB parent/prototype rendered comparison; original600s/120s; no APP adoption/world/photo claim.')
 p.add_argument('--root',type=Path,required=True);p.add_argument('--go',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 root=a.root.resolve();app=root/'chicago/4d';out=a.out.resolve();assert not out.is_relative_to(root);assert not out.is_relative_to(D)
 go=load(a.go);manifest=load(D/'MANIFEST.json')
 assert go['approved']is True and go['policy']=='ROOT_AUTHORIZED_WEB_SINGLE_SKIN_REBIND_RENDER_COMPARISON_V3'
 assert go['manifest_sha256']==sha(D/'MANIFEST.json')
 assert go['candidate_closed']==manifest['actual_candidate_closed']and go['prototype_receipt']==manifest['actual_prototype_receipt']
 assert go['source']==manifest['source']
 for ref in [go['candidate_closed'],go['prototype_receipt']]:assert sha(ref['path'])==ref['sha256']
 closed=load(go['candidate_closed']['path']);receipt=load(go['prototype_receipt']['path'])
 assert closed['status']=='NEW_SINGLE_SKIN_GARMENT_REBIND_PROTOTYPES_CREATED_STRICT_RESIDUAL_AND_PROTECTED_INVARIANTS_PASS_NOT_PHOTO_OR_WORLD_PASS'and closed['error']is None
 assert closed['manifest_sha256']==manifest['derivation_manifest_sha256']and closed['report']==receipt
 assert closed['source_before']==closed['source_after']==go['source']==receipt['source']
 assert closed['resources']['accepted']and closed['cleanup']['cleanup_complete']and not closed['cleanup']['remaining_owned_children']
 assert closed['result']['returncode']==0 and not closed['result']['timed_out']
 assert closed['result']['requested_timeout_seconds']==closed['result']['effective_timeout_seconds']==120 and closed['result']['timeout_override_reason']is None
 assert receipt['passed']and len(receipt['files'])==2 and receipt['native_resources_disposed']
 assert receipt['skin_count_must_remain']==1 and receipt['existing_max_position_residual_m']==1e-6
 assert receipt['donor_geometry_bit_exact_claim']is False and receipt['old_raw_copy_requalified']is False
 for f in receipt['files']:
  assert [r['pose']for r in f['residual_readings']]==['rest',0,2.75]
  for reading in f['residual_readings']:
   assert reading['all_original_native_rig_palettes_and_non_garment_world_vertices_exact']
   assert all(r['within_existing_position_limit']and r['max_world_position_residual_m']<=1e-6 for r in reading['all_garment_residuals'])
 assert receipt['status']=='NEW_SINGLE_SKIN_GARMENT_REBIND_PROTOTYPES_CREATED_STRICT_RESIDUAL_AND_PROTECTED_INVARIANTS_PASS_NOT_PHOTO_OR_WORLD_PASS'
 cases=[]
 for expected in manifest['cases']:
  rows=[r for r in receipt['files']if r['asset']==expected['asset']];assert len(rows)==1;r=rows[0]
  assert r['parent_WEB3']==expected['parent']and r['donor_WEB0']==expected['donor']
  assert r['old_BIN_prefix_exact']and r['encoded_and_native_decoded_images_exact']and r['all_protected_non_garment_streams_palettes_and_world_vertices_exact']and r['native_one_skeleton']and r['all_original_skins_nodes_rig_IBMs_clips_materials_images_exact']
  child=Path(r['candidate_path']).resolve();assert not child.is_relative_to(root)and sha(child)==r['candidate_sha256']
  cases.append(dict(expected,prototype=dict(path=str(child),sha256=r['candidate_sha256'],bytes=r['candidate_bytes'],triangles=r['triangles_after'])))
 for name,h in manifest['fixture_pins'].items():assert sha(D/name)==h,(name,'fixture changed')
 for name,h in manifest['input_pins'].items():assert sha(name)==h,(name,'pinned input changed')
 before=source(root,go['source'])
 lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('guard','/workspace/.cloud-setup/transport-current-20261103/resource_guard.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 resources_before=g.snapshot();assert g.check(resources_before)['accepted']
 out.mkdir(exist_ok=False);save(out/'SOURCE-BEFORE.json',before)
 cfg=dict(go,browser=manifest['browser'],cases=cases,poses_seconds=manifest['poses_seconds']);save(out/'CONFIG.json',cfg)
 prefix=out/'web-v3-render';command=['node',str(D/'run_browser.cjs'),str(app),str(out/'browser'),str(out/'CONFIG.json')]
 env=dict(os.environ,PW_EXECUTABLE=manifest['browser'],PLAYWRIGHT_BROWSERS_PATH='/workspace/.cloud-setup/transport-browser141-20261103');env.pop('CHICAGO_TICKETS_DIR',None)
 error=None;result=cleanup=resources=report=after=None
 try:
  assert subprocess.check_output([manifest['browser'],'--version'],timeout=5).decode().strip()=='Chromium 141.0.7390.37'
  q=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(app),'--timeout','600','--',*command],env=env,stdout=(out/'SUPERVISOR.stdout').open('xb'),stderr=subprocess.STDOUT)
  result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');resources=g.pair(resources_before,g.snapshot());report=load(out/'browser/REPORT.json')
  assert q.returncode==result['returncode']==0 and not result['timed_out']
  assert result['requested_timeout_seconds']==result['effective_timeout_seconds']==600 and result['timeout_override_reason']is None
  assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted']
  assert report['passed']and len(report['runs'])==4 and report['browser_closed']and report['server_closed']
  for row in report['runs']:
   assert row['passed']and row['viewport_elapsed_seconds']<=120 and len(row['pairs'])==2
   for pair in row['pairs']:
    assert pair['comparison']['native_parent_prototype_exact']
    assert pair['comparison']['counts']['full_canvas_pixels']==row['viewport']['width']*row['viewport']['height']
  after=source(root,go['source']);assert before==after
 except BaseException as e:error=repr(e)
 try:after=source(root,go['source'])
 except BaseException as e:error=(error+'; 'if error else'')+'source_after: '+repr(e)
 if resources is None:resources=g.pair(resources_before,g.snapshot())
 save(out/'CLOSED.json',dict(status='WEB_V3_SINGLE_SKIN_PROTOTYPE_RENDER_COMPARISON_COMPLETE_NOT_PHOTO_WORLD_OR_PRODUCTION_PASS'if error is None else'NONPASS',error=error,source_before=before,source_after=after,manifest_sha256=sha(D/'MANIFEST.json'),ROOT_GO_sha256=sha(a.go),result=result,cleanup=cleanup,resources=resources,report=report,production_WEB_installed=False,prototype_WEB_comparison_only=True,V3_new_single_skin_derived_geometry=True,donor_bit_exact_claim=False,full_world_pass=False,whole_garment_fit_acceptance=False,photographic_acceptance=False))
 print(json.dumps(dict(passed=error is None,out=str(out),error=error)));return 0 if error is None else 1
if __name__=='__main__':raise SystemExit(main())
