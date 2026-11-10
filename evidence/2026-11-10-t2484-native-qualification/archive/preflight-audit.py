#!/usr/bin/env python3
"""Read genuine pinned BEFORE objects to prove reader compatibility, not rebuilt acceptance."""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
b=json.loads((HERE/'BEFORE-BINDING.json').read_bytes());repo=Path(b['source_checkout']);base=b['captured_HEAD'];asset_root=Path(b['actual_readonly_asset_root'])
need=lambda ok,msg:None if ok else (_ for _ in ()).throw(AssertionError(msg))
need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==base,'SOURCE HEAD changed')
need(not subprocess.check_output(['git','status','--porcelain'],cwd=repo),'SOURCE checkout no longer clean')
spec=importlib.util.spec_from_file_location('audit',HERE/'audit-retained.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
controls=[];targets=[]
for x in b['affected']:
 for row in [x['before_master'],*x['before_web_outputs']]:
  path=Path(row['actual_read_path']);need(path==asset_root/Path(row['path']).relative_to('chicago/4d/assets'),'Actual read root/path mismatch');raw=path.read_bytes();need(len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'],'Pinned BEFORE physical asset changed')
 raw=Path(x['before_master']['actual_read_path']).read_bytes();web=Path(x['before_web_outputs'][0]['actual_read_path']).read_bytes()
 if not x['intentional_geometry_target']:
  row=m.compare_control(x['asset_key'],raw,raw,web);need(row['master_bytes_identical'],'Identity control failed');controls.append(x['asset_key'])
 else:
  summary,*_=m.geometry_summary(raw);row={'asset_key':x['asset_key'],'triangles':summary['triangles'],'primitives':summary['primitives']}
  if x['structure_id']=='kinzie_house_1812':
   from kinzie_checks import door_profile
   profile=door_profile(raw,x['current_inputs_doc']['params']['fields'],m.parse);need(abs(profile['target']['top']-1.95)<1e-4,'Genuine BEFORE end door differs from expected legacy1.95m head');row['actual_before_door_profile']=profile
  targets.append(row)
paths=list(b['source_files']);tree=subprocess.check_output(['git','ls-tree','-r','-z',base,'--',*paths],cwd=repo);oids={}
for row in tree.split(b'\0'):
 if row:
  meta,path=row.split(b'\t',1);oids[path.decode()]=meta.split()[2].decode()
for path,entry in b['source_files'].items():
 alias=b['SOURCE_git_authenticated_asset_input_overlay'].get(path);actual=Path(alias['actual_read_path'])if alias else repo/path;raw=actual.read_bytes();need(hashlib.sha256(raw).hexdigest()==entry['sha256'],'Bound SOURCE input changed '+path);need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oids[path],'Input bytes are not frozen SOURCE Git blob '+path)
for name,oid in b['asset_root_registry_SOURCE_HEAD_git_blob_ids'].items():
 raw=(asset_root/name).read_bytes();need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==oid,'Canonical registry no longer frozen SOURCE blob '+name)
receipt={'status':'PASS_READER_PREFLIGHT_NOT_NATIVE_ACCEPTANCE','pinned_HEAD':base,'binding_sha256':hashlib.sha256((HERE/'BEFORE-BINDING.json').read_bytes()).hexdigest(),'actual_control_MASTER_readers_exercised':len(controls),'actual_target_before_summaries':targets,'bound_SOURCE_input_files_Git_blob_and_SHA256_authenticated':len(paths),'canonical_asset_root':str(asset_root),'claim_limit':'Controls compare actual existing BEFORE files to themselves only for reader compatibility. Sparse source inputs were authenticated by frozen Git tree OIDs and actual bytes without source hydration. No rebuilt equality, native output or picture acceptance claimed.'}
(HERE/'AUDIT-READER-PREFLIGHT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
