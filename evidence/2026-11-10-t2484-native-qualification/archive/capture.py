#!/usr/bin/env python3
"""Compute live native scope or pin a clean source BEFORE binding, read-only checkout."""
import argparse,collections,datetime,hashlib,json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
TARGETS={'kinzie_house_1812','kinzie_house_1812_green'}
EXPECTED_FAMILIES={'log_dwelling','palisade'}
EXPECTED_COUNTS={'selected_defaults':83,'selected_variants':0,'selected_structure_ids':83,'selected_geometry_target_asset_rows':2,'selected_control_asset_rows':81}
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(d):return json.dumps(d,sort_keys=True,separators=(',',':')).encode()
def write(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,default=Path('/tmp/nov10-kinzie-completion'));ap.add_argument('--asset-root',type=Path,required=True);ap.add_argument('--prepared-scope',type=Path);ap.add_argument('--pin-head');ap.add_argument('--output-dir',type=Path,default=HERE);args=ap.parse_args()
 repo=args.repo.resolve();app=repo/'chicago/4d';asset_root=args.asset_root.resolve();out=args.output_dir.resolve();assert not out.is_relative_to(repo);out.mkdir(parents=True,exist_ok=True)
 git=lambda *argv:subprocess.check_output(['git',*argv],cwd=repo)
 head=git('rev-parse','HEAD').decode().strip();status=git('status','--porcelain').decode()
 if args.pin_head:assert head==args.pin_head and not status,(head,status)
 from asset_overlay import FrozenAssetOverlay
 overlay=FrozenAssetOverlay(repo,asset_root,head).install()
 sys.path.insert(0,str(app/'generators'));from mesh_inputs import structure_inputs_doc,structure_inputs_sha
 from common import versions
 manifest_names=['manifest.json','manifest.web.json','manifest.versions.json'];raw={n:(asset_root/n).read_bytes()for n in manifest_names};registry_git_blobs={}
 for n,b in raw.items():
  logical='chicago/4d/assets/'+n;oid=git('rev-parse',head+':'+logical).decode().strip();actual_oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert actual_oid==oid,('canonical asset-root registry differs from frozen SOURCE Git blob',logical,oid,actual_oid);registry_git_blobs[n]=oid
 regs={n:json.loads(b)for n,b in raw.items()};defaults=regs['manifest.json']['assets'];web=regs['manifest.web.json']['masters'];variants=regs['manifest.versions.json']['assets'];assert set(defaults)==set(web)
 allrows=[];sourcepaths=set();problems=[]
 for kind,registry in [('default',defaults),('variant',variants)]:
  for key,row in sorted(registry.items()):
   sid=row.get('structure_id');doc=None;current=None;source=None
   if sid:
    source=app/'data/structures'/f'{sid}.json'if kind=='default'else app/'data/structures/versions'/sid/(row['version_label']+'.json')
    record=json.loads(source.read_text());phase=next(p for p in record['phases']if p['id']==row['phase_id']);doc=structure_inputs_doc(record,phase,row['archetype']);current=structure_inputs_sha(record,phase,row['archetype']);assert current==sha(json.dumps(doc,sort_keys=True).encode())
    sourcepaths.add(str(source.relative_to(repo)));sourcepaths.update('chicago/4d/generators/'+p for p in doc['code']);sourcepaths.update('chicago/4d/'+p for group in ['textures','component_data']for p in doc.get(group,{}))
   stale=current is not None and current!=row.get('inputs_sha256')
   allrows.append({'kind':kind,'asset_key':key,'structure_id':sid,'phase_id':row.get('phase_id'),'archetype':row.get('archetype'),'source_path':str(source.relative_to(repo))if source else None,'current_inputs_sha256':current,'registered_inputs_sha256':row.get('inputs_sha256'),'stale':stale,'intentional_geometry_target':sid in TARGETS,'current_inputs_doc':doc,'old_registry_row':row})
 selected_ids=sorted({x['structure_id']for x in allrows if x['stale']});selected=[x for x in allrows if x['structure_id']in selected_ids];stale=[x for x in allrows if x['stale']]
 # --only selects IDs: every registered phase/variant of that ID must be bound.
 for x in selected:x['selected_due_to_stale_input']=x['stale']
 families=set(x['archetype']for x in stale);assert families<=EXPECTED_FAMILIES,('unexpected stale families',sorted(families-EXPECTED_FAMILIES))
 missing=TARGETS-set(selected_ids);assert not missing,('intended target absent from native scope',sorted(missing))
 count=lambda rows:dict(sorted(collections.Counter(x['archetype']for x in rows).items()))
 counts={'default_registry':len(defaults),'variant_registry':len(variants),'actual_stale_defaults':sum(x['kind']=='default'for x in stale),'actual_stale_variants':sum(x['kind']=='variant'for x in stale),'selected_defaults':sum(x['kind']=='default'for x in selected),'selected_variants':sum(x['kind']=='variant'for x in selected),'selected_structure_ids':len(selected_ids),'selected_geometry_target_asset_rows':sum(x['intentional_geometry_target']for x in selected),'selected_control_asset_rows':sum(not x['intentional_geometry_target']for x in selected),'foreign_defaults':sum(x['kind']=='default'and x['structure_id']not in selected_ids for x in allrows),'foreign_variants':sum(x['kind']=='variant'and x['structure_id']not in selected_ids for x in allrows)}
 assert all(counts[k]==v for k,v in EXPECTED_COUNTS.items()),('exact Kinzie scope count mismatch',counts,EXPECTED_COUNTS)
 assert count(selected)=={'log_dwelling':82,'palisade':1},('unexpected selected family counts',count(selected))
 prepared_path=args.prepared_scope or app/'docs/RESEARCH/kinzie-completion-T-2484/NATIVE-SCOPE-PREPARED.json';prepared=json.loads(prepared_path.read_bytes());assert set(prepared['assets'])=={x['asset_key'] for x in selected},'prepared vs actual selected asset membership mismatch';assert set(prepared['physical_targets'])==TARGETS,'prepared physical targets mismatch'
 codepaths=set(sourcepaths);sourcepaths.update(['chicago/4d/generators/mesh_inputs.py','chicago/4d/generators/code_inputs.py','chicago/4d/generators/blender.pin','chicago/4d/generators/build.py','chicago/4d/generators/emit.py','chicago/4d/tools/bake.sh','chicago/4d/tools/bake_ref.py','chicago/4d/tools/web_derivatives.sh','.github/workflows/chicago-4d-bake.yml']);sourcepaths.update(str(p.relative_to(repo))for p in (app/'generators/archetypes').glob('*_params.py'))
 sourcefiles={p:{'sha256':sha((repo/p).read_bytes()),'bytes':(repo/p).stat().st_size}for p in sorted(sourcepaths)}
 report={'status':'CLEAN_HEAD_PINNED_BEFORE_BINDING'if args.pin_head else 'PROVISIONAL_LIVE_SCOPE_ONLY_NOT_A_HEAD_PIN','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'observed_HEAD':head,'source_checkout':str(repo),'pinned_HEAD':head if args.pin_head else None,'worktree_status_at_start':status,'counts':counts,'actual_stale_by_family':count(stale),'selected_by_family':count(selected),'intended_geometry_structure_ids':sorted(TARGETS),'selected_variant_keys':[x['asset_key']for x in selected if x['kind']=='variant'],'selected_structure_ids':selected_ids,'only':','.join(selected_ids),'source_files':sourcefiles,'actual_readonly_asset_root':str(asset_root),'SOURCE_git_authenticated_asset_input_overlay':overlay.reads,'asset_root_registry_SOURCE_HEAD_git_blob_ids':registry_git_blobs,'prepared_scope_path':str(prepared_path),'prepared_scope_sha256':sha(prepared_path.read_bytes()),'manifest_sha256':{n:sha(b)for n,b in raw.items()},'claim_limit':'Read-only input computation. No native output, GPU/image acceptance or publish claimed. Scope derives from actual manifests and current structure_inputs_doc/sha, not a presumed family count.'}
 (out/'only.txt').write_text(report['only']+'\n');(out/'asset-keys.txt').write_text('\n'.join(x['asset_key']for x in selected)+'\n')
 write(out/'SCOPE-REPORT.json',report);write(out/'SCOPE-ROWS.json',allrows)
 if args.pin_head:
  def receipt(p):
   b=p.read_bytes();rel=p.relative_to(asset_root);return {'path':'chicago/4d/assets/'+rel.as_posix(),'actual_read_path':str(p),'bytes':len(b),'sha256':sha(b)}
  for x in allrows:
   key=x['asset_key'];x['before_master']=receipt(asset_root/'gltf'/key);x['before_web_outputs']=[receipt(asset_root/'web'/key)]+[receipt(asset_root/'web'/lk)for lk in versions.lod_asset_keys(key).values()];row=x['old_registry_row'];assert x['before_master']['bytes']==row['bytes'],key
   if x['kind']=='default':x['web_receipt_master_sha256']=web[key];assert x['before_master']['sha256']==web[key],key
   else:assert x['before_master']['sha256']==row['web_master_sha256'],key
  affected=[x for x in allrows if x['structure_id']in selected_ids];foreign=[x for x in allrows if x['structure_id']not in selected_ids]
  for n,b in raw.items():(out/('BEFORE-'+n)).write_bytes(b)
  write(out/'BEFORE-FOREIGN.json',foreign)
  pin=(app/'generators/blender.pin').read_text();binding={**report,'captured_HEAD':head,'source_branch':git('branch','--show-current').decode().strip(),'affected':affected,'foreign_rows_file':'BEFORE-FOREIGN.json','foreign_rows_canonical_sha256':sha(canon(foreign)),'registry_files':{'assets/'+n:receipt(asset_root/n)for n in manifest_names},'pin':{'version':re.search(r'^BLENDER_VERSION=(.*)$',pin,re.M)[1],'archive_sha256':re.search(r'^BLENDER_SHA256=(.*)$',pin,re.M)[1],'raw':pin},'baseline_claim':'Every actual registered default and variant MASTER/WEB/declared LOD was read and hashed from the clean bound parent. No export generated. Physical asset reads came from the explicit canonical asset root; SOURCE code/records and exact manifest Git blobs came from the pinned isolated source checkout.'}
  assert head==git('rev-parse','HEAD').decode().strip()and not git('status','--porcelain').decode()
  assert all(sha((asset_root/n).read_bytes())==sha(b)for n,b in raw.items())
  assert all(sha((repo/p).read_bytes())==v['sha256']for p,v in sourcefiles.items())
  write(out/'BEFORE-BINDING.json',binding)
 else:
  assert head==git('rev-parse','HEAD').decode().strip(),'HEAD changed while preparing provisional scope; rerun'
  assert all(sha((repo/p).read_bytes())==v['sha256']for p,v in sourcefiles.items()),'Bound geometry source changed while preparing scope; rerun'
 print(json.dumps({'status':report['status'],'observed_HEAD':head,'source_checkout':str(repo),'pinned_HEAD':report['pinned_HEAD'],'counts':counts,'stale_by_family':report['actual_stale_by_family'],'selected_variants':report['selected_variant_keys'],'scope_report':str(out/'SCOPE-REPORT.json'),'only_file':str(out/'only.txt')},indent=2))
if __name__=='__main__':main()
