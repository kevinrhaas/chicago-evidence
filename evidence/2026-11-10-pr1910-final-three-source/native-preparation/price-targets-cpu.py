from pathlib import Path
from unittest.mock import patch
import collections,hashlib,importlib,importlib.util,json,subprocess,sys,types
r=Path(__file__).resolve().parent;repo=Path('/tmp/chicago-west-wicket-20261109');app=repo/'chicago/4d';sys.path.insert(0,str(app/'generators'));sys.modules.setdefault('bpy',types.ModuleType('bpy'))
from mesh_inputs import resolve_params,structure_inputs_sha
from common.mesh import MeshBuilder
spec=importlib.util.spec_from_file_location('audit',r/'audit-retained.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
rows=[x for x in json.load(open(r/'SCOPE-ROWS.json'))if x['stale']and x['intentional_geometry_target']];base='2dcdf91df70ae52c5d121162939cfe2aa4617152';priced=[]
for row in rows:
 sid=row['structure_id'];arch=row['archetype'];key=row['asset_key'];record=json.load(open(app/'data/structures'/f'{sid}.json'));oldrecord=json.loads(subprocess.check_output(['git','show',f'{base}:chicago/4d/data/structures/{sid}.json'],cwd=repo));phase=next(p for p in record['phases']if p['id']==row['phase_id']);oldphase=next(p for p in oldrecord['phases']if p['id']==row['phase_id']);builder=importlib.import_module('archetypes.'+arch);p=resolve_params(arch,phase,record);oldp=resolve_params(arch,oldphase,oldrecord)
 actual=(app/'assets/gltf'/key).read_bytes();summary,*_=audit.geometry_summary(actual)
 contexts=[patch.object(MeshBuilder,'to_object',lambda b,mats=None:(b,mats)),patch.object(builder,'simple_material',lambda n,*a,**k:(n,a,k))]
 if hasattr(builder,'TonedBuilder'):contexts.append(patch.object(builder.TonedBuilder,'to_object',lambda b,mats=None:(b,mats)))
 if hasattr(builder,'_lay_period_brick'):contexts.append(patch.object(builder,'_lay_period_brick',lambda *a,**k:None))
 if hasattr(builder,'_configure_cage_glass'):contexts.append(patch.object(builder,'_configure_cage_glass',lambda *a,**k:None))
 for c in contexts:c.start()
 try:oldmesh,_=builder.build(oldp,sid+'__'+phase['id']);newmesh,_=builder.build(p,sid+'__'+phase['id'])
 finally:
  for c in reversed(contexts):c.stop()
 count=lambda mesh:sum(max(0,len(f)-2)for f in mesh.faces)
 oldcount,newcount=count(oldmesh),count(newmesh);assert oldcount==summary['triangles'],(key,'old CPU/native triangle mismatch',oldcount,summary['triangles'])
 changed_params=audit.diff(oldrecord['phases'],record['phases'])
 priced.append({'structure_id':sid,'archetype':arch,'asset_key':key,'candidate_resolved_inputs_sha256':structure_inputs_sha(record,phase,arch),'candidate_record_sha256':hashlib.sha256((app/'data/structures'/f'{sid}.json').read_bytes()).hexdigest(),'before_registered_inputs_sha256':row['registered_inputs_sha256'],'before_native_MASTER_bytes':len(actual),'before_native_MASTER_sha256':summary['sha256'],'before_native_triangles':summary['triangles'],'before_native_vertices':summary['vertices_including_export_splits'],'old_CPU_polygon_triangulation_count':oldcount,'old_CPU_count_equals_actual_old_native':True,'new_CPU_polygon_triangulation_upper_bound':newcount,'conservative_maximum_triangle_delta':newcount-summary['triangles'],'positive_delta_without_crediting_reductions':max(0,newcount-summary['triangles']),'changed_source_phase_paths':[x['path']for x in changed_params],'price_limits':'Real current CPU accumulator faces; polygon n-2 bounds final triangulation absent topology-changing modifiers. UV/material/tone export is bypassed for count only. This is not a native export, visibility/shadow/instancing sweep or a frame/payload FITS price.'})
result={'status':'CPU_TARGET_TRIANGLE_BOUNDS_WITH_ACTUAL_OLD_NATIVE_COUNTS','source_base_for_old_records':base,'target_count':len(priced),'before_native_target_triangles_total':sum(x['before_native_triangles']for x in priced),'new_CPU_target_triangle_upper_bounds_total':sum(x['new_CPU_polygon_triangulation_upper_bound']for x in priced),'sum_positive_triangle_increments_no_reduction_credit':sum(x['positive_delta_without_crediting_reductions']for x in priced),'targets':priced,'claim_limit':'Five single MASTER geometry counts only; not worst-stand draw/triangle, boot bytes, GPU time, Light acceptance or an assurance of budget fit. Final native and actual camera/viewport pricing remain authoritative.'};(r/'TARGET-CPU-COST-BOUNDS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
