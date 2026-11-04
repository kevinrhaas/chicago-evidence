"""External, unapplied material-only proposal. No Blender, source writes or rendering."""
from pathlib import Path
import json,hashlib,subprocess,sys,difflib,ast,copy,math,datetime
sys.dont_write_bytecode=True
P=Path(__file__).parent;W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(W),*a]);source=lambda:{'head':git('rev-parse','HEAD').decode().strip(),'tree':git('write-tree').decode().strip(),'status':git('status','--porcelain').decode(),'diff_sha256':sha(git('diff','--binary'))}
before=source();assert not before['status'];raw=(A/'generators/archetypes/frame_dwelling.py').read_text()
old='''    return b.add_gable_roof(x0 + EAVE_M, y0, x1 - EAVE_M, y1, eave_z,
                            p.roof_pitch_deg, conf, M_ROOF, overhang=EAVE_M,
                            ridge_along_x=True)
'''
new='''    first_roof_face = len(b.faces)
    ridge_z = b.add_gable_roof(x0 + EAVE_M, y0, x1 - EAVE_M, y1, eave_z,
                             p.roof_pitch_deg, conf, M_ROOF, overhang=EAVE_M,
                             ridge_along_x=True)
    if p.picture_layout == "keeper_gale_1902":
        # T-2380: the pictured east gable is wall infill, not roof covering.
        # Preserve the complete roof envelope, unpictured west end and loft light.
        east_faces = [i for i in range(first_roof_face, len(b.faces))
                      if len(b.faces[i]) == 3 and all(
                          abs(b.verts[v][0] - x1) < 1e-9 for v in b.faces[i])]
        if len(east_faces) != 1 or b.mat_index[east_faces[0]] != M_ROOF:
            raise ValueError("keeper east gable must be one native roof-end triangle")
        b.mat_index[east_faces[0]] = M_WALL
    return ridge_z
'''
assert raw.count(old)==1;candidate=raw.replace(old,new);ast.parse(candidate);(P/'frame_dwelling.material-only-candidate.py').write_text(candidate);patch=''.join(difflib.unified_diff(raw.splitlines(True),candidate.splitlines(True),fromfile='a/chicago/4d/generators/archetypes/frame_dwelling.py',tofile='b/chicago/4d/generators/archetypes/frame_dwelling.py'));(P/'UNAPPLIED-keeper-east-gable.patch').write_text(patch)
# Ask the real recipe owner to project changed source bytes without changing files.
sys.path.insert(0,str(A/'generators'));import mesh_inputs
m=json.loads((A/'assets/manifest.json').read_bytes())['assets'];rows=[];orig=mesh_inputs._sha_file;target=(A/'generators/archetypes/frame_dwelling.py').resolve();candidate_sha=sha(candidate.encode());only_layout=[]
for name,r in m.items():
 if r.get('archetype')!='frame_dwelling':continue
 st=json.loads((A/'data/structures'/(r['structure_id']+'.json')).read_bytes());phase=next(x for x in st['phases']if x['id']==r['phase_id']);old_doc=mesh_inputs.structure_inputs_doc(st,phase,r['archetype']);actual=mesh_inputs.structure_inputs_sha(st,phase,r['archetype']);assert actual==r['inputs_sha256'],('baseline not current',name)
 mesh_inputs._sha_file=lambda path: candidate_sha if Path(path).resolve()==target else orig(path)
 try:projected_doc=mesh_inputs.structure_inputs_doc(st,phase,r['archetype']);projected=mesh_inputs.structure_inputs_sha(st,phase,r['archetype'])
 finally:mesh_inputs._sha_file=orig
 assert projected!=actual and old_doc['params']==projected_doc['params'];changed=[k for k,v in old_doc['code'].items()if projected_doc['code'][k]!=v];assert changed==['archetypes/frame_dwelling.py'];layout=old_doc['params']['fields'].get('picture_layout')
 if layout=='keeper_gale_1902':only_layout.append(name)
 rows.append({'asset':name,'structure_id':r['structure_id'],'current_native_inputs_sha256':actual,'PROJECTED_UNBUILT_candidate_inputs_sha256':projected,'only_recipe_code_change':changed,'resolved_params_and_derived_properties_exact':True,'picture_layout':layout,'current_MASTER_bytes':(A/'assets/gltf'/name).stat().st_size,'current_WEB_bytes':(A/'assets/web'/name).stat().st_size})
assert len(rows)==272 and only_layout==['log_jail_keeper_house__frame_1835.glb']
versions=json.loads((A/'assets/manifest.versions.json').read_bytes());assert 'frame_dwelling'not in json.dumps(versions)
# Pure 4-face roof contract check only: execute extracted existing accumulator methods,
# not build()/emit/Blender or a mesh exporter. No files/models are generated.
mesh_ast=ast.parse((A/'generators/common/mesh.py').read_text());klass=next(n for n in mesh_ast.body if isinstance(n,ast.ClassDef)and n.name=='MeshBuilder');methods=[n for n in klass.body if isinstance(n,ast.FunctionDef)and n.name in ['__init__','add_poly','add_gable_roof']];mini=ast.ClassDef(name='Accumulator',bases=[],keywords=[],body=copy.deepcopy(methods),decorator_list=[]);ns={'math':math};exec(compile(ast.fix_missing_locations(ast.Module(body=[mini],type_ignores=[])),'<existing-pure-roof-accumulator>','exec'),ns)
def roof_fn(text):
 node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name=='_roof');node.returns=None
 for arg in node.args.args:arg.annotation=None
 env={'EAVE_M':.25,'M_ROOF':1,'M_WALL':0};exec(compile(ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[])),'<unapplied-roof-proposal>','exec'),env);return env['_roof']
oldroof,newroof=roof_fn(raw),roof_fn(candidate);checks=[]
from types import SimpleNamespace
for layout in [None,'keeper_gale_1902']:
 param=SimpleNamespace(roof_type='gable',roof_pitch_deg=25.,picture_layout=layout);a,b=ns['Accumulator']('old'),ns['Accumulator']('candidate');ra=oldroof(a,param,0,0,6.4,4.6,2.65,1.);rb=newroof(b,param,0,0,6.4,4.6,2.65,1.);assert ra==rb and a.verts==b.verts and a.faces==b.faces and a.conf==b.conf
 changed=[i for i,(x,y)in enumerate(zip(a.mat_index,b.mat_index))if x!=y];assert changed==([]if layout is None else[3]);checks.append({'layout':layout,'vertices_faces_confidence_ridge_exact':True,'material_only_changed_faces':changed,'old_materials':a.mat_index,'candidate_materials':b.mat_index,'NOT_NATIVE_GENERATION':True})
# Existing foreign frame_tavern source and target assets are merely bound, not modified.
foreign={n:sha((A/n).read_bytes())for n in ['generators/archetypes/frame_tavern.py','generators/archetypes/frame_tavern_params.py','assets/gltf/green_tree_tavern__frame_1833.glb','assets/web/green_tree_tavern__frame_1833.glb','assets/gltf/sauganash_hotel__frame_1831.glb','assets/web/sauganash_hotel__frame_1831.glb','assets/gltf/log_jail__log_1833.glb','data/enclosures/log_jail_palisade.json','data/enclosures/log_jail_keeper_link.json']if(A/n).exists()}
assert source()==before
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'UNAPPLIED_EXTERNAL_PREP_ONLY','source_before_after_exact':before,'producer_baseline_sha256':sha(raw.encode()),'candidate_producer_sha256':candidate_sha,'patch_sha256':sha(patch.encode()),'one_visible_change':'Only the existing keeper-layout east gable triangle material index changes from roof_shingle to the existing wall material. No new board-course geometry, vertices, dimensions, normals, confidence, roof slope/west end or loft geometry are proposed.','actual_current_native_family':272,'projected_changed_recipes':272,'projected_only_existing_native_keeper_geometry_material_change':1,'expected_default_native_MASTER_byte_equivalence_requires_real_regeneration':271,'frame_dwelling_versions':0,'pure_contract_checks_NOT_NATIVE':checks,'all_projected_recipe_changes_only_one_archetype_codehash':True,'all_current_resolved_params_derived_properties_unchanged':True,'current_family_MASTER_total_bytes':sum(r['current_MASTER_bytes']for r in rows),'current_family_WEB_total_bytes':sum(r['current_WEB_bytes']for r in rows),'untouched_foreign_and_compound_bindings':foreign,'rows':rows,'native_GPU_source_ticket_claim_actions':'NONE; no new native outputs, asset registrations, fingerprint stamping or claimed native qualification'};(P/'PROJECTED-RECIPE-INVENTORY.json').write_text(json.dumps(result,indent=2)+'\n');print('EXTERNAL PREP ONLY:',len(rows),'projected changed recipes;',len(only_layout),'opt-in target; actual source unchanged',flush=True)
