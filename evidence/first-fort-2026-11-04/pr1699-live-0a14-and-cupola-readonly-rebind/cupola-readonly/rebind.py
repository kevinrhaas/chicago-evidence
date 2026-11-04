from pathlib import Path
import sys,json,hashlib,ast,copy,datetime as dt,subprocess
sys.dont_write_bytecode=True
P=Path(__file__).parent;S=P/'immutable-source/chicago/4d';F=Path('/tmp/first-fort-cupola-prep-20261104');H='0a14eb07bc6630ace4ce8bec12b87e9fa1a4b0d4';sha=lambda b:hashlib.sha256(b).hexdigest();identity=json.loads((P/'SOURCE-IDENTITY.json').read_bytes());assert identity['actual_dev']==H
sys.path.insert(0,str(S/'generators'));import mesh_inputs
from common.versions import load_versions,asset_key
from common.phases import drawn_by_another_layer
manifest=json.loads((S/'assets/manifest.json').read_bytes());web=json.loads((S/'assets/manifest.web.json').read_bytes());versions=json.loads((S/'assets/manifest.versions.json').read_bytes());assert manifest['inputs_scheme']==mesh_inputs.SCHEME
source=(S/'generators/build.py').read_text();tree=ast.parse(source);resolver=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='resolve_phase');phasefn=next(n for n in ast.walk(tree)if isinstance(n,ast.FunctionDef)and n.name=='phases_in_scenes');scene_dates={f.stem:dt.date.fromisoformat(json.loads(f.read_bytes())['target_date'])for f in sorted((S/'data/scenes').glob('*.json'))};env={'dt':dt,'targets':list(scene_dates.values())};exec(compile(ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(resolver),copy.deepcopy(phasefn)],type_ignores=[])),'<actual-current-build-phase-owner>','exec'),env)
resolve=env['phases_in_scenes'];targets={f'first_fort_dearborn_blockhouse_{s}'for s in ['nw','se']};candidates={};patch=(F/'UNAPPLIED-two-blockhouse-cupolas.patch').read_bytes();assert sha(patch)=='3351d1442fa9cb27ed5e1d3d4726a4cd7be8f900b104f92ffef42039be682de2';(P/'UNAPPLIED-two-blockhouse-cupolas.patch').write_bytes(patch)
for sid in sorted(targets):
 raw=(S/f'data/structures/{sid}.json').read_bytes();assert raw==(F/(sid+'.json')).read_bytes();candidate=(F/(sid+'.candidate.json')).read_bytes();candidates[sid]=json.loads(candidate);(P/(sid+'.candidate.json')).write_bytes(candidate)
records=[json.loads(f.read_bytes())for f in sorted((S/'data/structures').glob('*.json'))];rows=[];skipped=[];family={'fort_structure','outbuilding'}
def calculate(st,ph,name,kind='default'):
 arch=st['archetype'];row=(manifest if kind=='default'else versions)['assets'][name];old=mesh_inputs.structure_inputs_doc(st,ph,arch);oldsha=mesh_inputs.structure_inputs_sha(st,ph,arch);assert oldsha==row['inputs_sha256'],('CURRENT_BASELINE_STALE',name,oldsha,row['inputs_sha256']);mesh_inputs.resolve_params(arch,ph,st).validate();candidate=candidates.get(st['id'],st);newph=next(x for x in candidate['phases']if x['id']==ph['id']);new=mesh_inputs.structure_inputs_doc(candidate,newph,arch);newsha=mesh_inputs.structure_inputs_sha(candidate,newph,arch);assert old['code']==new['code'] and old['blender_pin']==new['blender_pin'];fields=[k for k in old['params']['fields']if old['params']['fields'][k]!=new['params']['fields'][k]];changed=newsha!=oldsha;assert changed==(st['id']in targets);assert fields==(['cupola']if changed else[]),(name,fields)
 if not changed:assert old==new
 if changed:
  mesh_inputs.resolve_params(arch,newph,candidate).validate();assert ph['documented_range']==newph['documented_range'];assert st.get('position')==candidate.get('position');assert st.get('footprint')==candidate.get('footprint');assert set(old['code'])==set(new['code'])
 rows.append({'asset':name,'kind':kind,'archetype':arch,'structure_id':st['id'],'phase_id':ph['id'],'current_inputs_sha256':oldsha,'PROJECTED_UNBUILT_inputs_sha256':newsha,'changed_fields':fields,'current_manifest_row':row,'current_web_manifest_row':web.get('masters',{}).get(name),'code_unchanged':True,'no_native_output_produced':True})
for st in records:
 assert st['archetype']in family
 phases=resolve(st)
 if not phases:skipped.append({'id':st['id'],'reason':'No phase resolves at any supported scene date','phase_ids':[p['id']for p in st['phases']]})
 for ph in phases:
  if drawn_by_another_layer(ph):skipped.append({'id':st['id'],'phase':ph['id'],'reason':'Actual owner drawn_by_another_layer'});continue
  calculate(st,ph,f"{st['id']}__{ph['id']}.glb")
variant_records=[v for v in load_versions(S)if v['record'].get('archetype')in family]
for v in variant_records:
 for ph in resolve(v['record']):
  if not drawn_by_another_layer(ph):calculate(v['record'],ph,asset_key(v['id'],v['label'],ph['id']),'variant')
fort=[r for r in rows if r['archetype']=='fort_structure'];ob=[r for r in rows if r['archetype']=='outbuilding'];assert len(fort)==25 and len(ob)==243 and not variant_records;actual_manifest={k for k,v in manifest['assets'].items()if v.get('archetype')in family};assert actual_manifest=={r['asset']for r in rows};assert not any(v.get('archetype')in family for v in versions['assets'].values());changed=[r for r in rows if r['changed_fields']];assert len(changed)==2 and {r['structure_id']for r in changed}==targets
# Proposal changes no output or registration bytes; exact current physical bindings are retained, not falsely restamped as new native results.
entries=json.loads((P/'IMMUTABLE-TREE-ENTRIES.json').read_bytes());bindings=[]
for r in rows:
 names={role:('chicago/4d/assets/'+folder+'/'+r['asset'])for role,folder in [('MASTER','gltf'),('WEB','web')]};bindings.append({'asset':r['asset'],**{role:entries[path]['oid']for role,path in names.items()}})
for rel,b in identity['files'].items():assert sha((S/rel).read_bytes())==b['sha256']
result={'status':'READONLY_CURRENT_OWNER_REBIND_PASS_NOT_NATIVE_QUALIFICATION','actual_dev':H,'actual_dev_tree':identity['actual_dev_tree'],'patch_sha256':sha(patch),'source_owner':'Exact current mesh_inputs.structure_inputs_sha + AST-isolated actual build.resolve_phase/phases_in_scenes + actual common.versions.load_versions; no bpy/native','supported_scene_dates':{k:str(v)for k,v in scene_dates.items()},'raw_record_counts':identity['record_counts'],'buildable_default_fort':len(fort),'buildable_default_outbuilding':len(ob),'family_variants':len(variant_records),'all268_current_baseline_recipe_hashes_match_current_manifest':True,'projected_changed_defaults':len(changed),'unchanged_other_fort_recipes_and_manifest_WEB_rows':23,'unchanged_foreign_outbuilding_recipes_and_manifest_WEB_rows':243,'no_producer_params_common_emit_pin_or_output_manifest_changes':True,'source_bindings':{k:v for k,v in identity['files'].items()if k.startswith('generators/')},'excluded_by_actual_owner':skipped,'rows':rows,'physical_git_blob_bindings_unchanged':bindings,'target_candidate_sha256':{sid:sha((P/(sid+'.candidate.json')).read_bytes())for sid in targets},'native_execution':'NOT_RUN; two projected stale defaults require genuine Blender+WEB before adoption','pixel_acceptance':'NOT_RUN; source-current/both app viewports/whole8 still required','authorization':'No ticket claim/app mutation/source branch implementation/dispatch/workflow edit/GPU performed; await exact root GO'};(P/'CURRENT-0A14-RECIPE-REBIND.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'changed':[{'asset':r['asset'],'old':r['current_inputs_sha256'],'projected':r['PROJECTED_UNBUILT_inputs_sha256']}for r in changed],'other_fort':23,'foreign':243,'variants':0,'receipt_sha256':sha((P/'CURRENT-0A14-RECIPE-REBIND.json').read_bytes())}),flush=True)
