from pathlib import Path
import ast,datetime as dt,hashlib,json,sys
r=Path(__file__).resolve().parent;app=Path('/tmp/chicago-west-wicket-20261109/chicago/4d');b=json.load(open(r/'BEFORE-BINDING.json'));sys.path.insert(0,str(app/'generators'))
from common.phases import drawn_by_another_layer
from common.versions import asset_key,load_versions
source=(app/'generators/build.py').read_text();tree=ast.parse(source);f=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='resolve_phase');module=ast.Module(body=[f],type_ignores=[]);ns={'dt':dt};exec(compile(module,'<actual build.py resolve_phase>','exec'),ns);resolve=ns['resolve_phase'];scenes=[(p,json.loads(p.read_text()))for p in sorted((app/'data/scenes').glob('*.json'))];dates=[dt.date.fromisoformat(j['target_date'])for p,j in scenes];ids=set(b['selected_structure_ids']);actual=[]
def phases(st):
 out={}
 for date in dates:
  ph=resolve(st,date)
  if ph is not None and not drawn_by_another_layer(ph):out[ph['id']]=ph
 return list(out.values())
for sid in sorted(ids):
 st=json.loads((app/'data/structures'/f'{sid}.json').read_text())
 for ph in phases(st):actual.append(('default',f"{sid}__{ph['id']}.glb"))
for v in load_versions():
 if v['id']in ids:
  for ph in phases(v['record']):actual.append(('variant',asset_key(v['id'],v['label'],ph['id'])))
expected={(x['kind'],x['asset_key'])for x in b['affected']};assert set(actual)==expected,{'actual_only':sorted(set(actual)-expected),'binding_only':sorted(expected-set(actual))}
receipt={'status':'PASS_EXACT_BUILD_SELECTION_CLOSURE','pinned_HEAD':b['captured_HEAD'],'actual_build_resolver_extracted_from':'generators/build.py resolve_phase AST (no bpy/build import/execution)','selected_structure_ids':len(ids),'actual_all_scene_default_phase_outputs':sum(k=='default'for k,p in actual),'actual_all_scene_variant_phase_outputs':sum(k=='variant'for k,p in actual),'exactly_frozen_manifest_scope':True,'scene_date_inputs':[{'path':str(p.relative_to(app)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'target_date':j['target_date']}for p,j in scenes],'claim_limit':'Read-only selection simulation using the actual builder date resolver. No Blender/native dispatch or export.'};(r/'SCOPE-BUILD-CLOSURE.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items()if k!='scene_date_inputs'},indent=2))
