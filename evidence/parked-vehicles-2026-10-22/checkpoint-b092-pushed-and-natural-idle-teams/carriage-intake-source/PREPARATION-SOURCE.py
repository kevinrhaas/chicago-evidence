from pathlib import Path
import json,hashlib,shutil,struct,importlib.util,difflib,ast
R=Path('/workspace/shared/brougham-v14-APP-INTAKE-TEXT-HELD-20261022');R.mkdir(exist_ok=True);P=R/'proposed/chicago/4d';P.mkdir(parents=True,exist_ok=True)
APP=Path('/workspace/chicago/chicago/4d');V14=Path('/workspace/shared/brougham-v14-footplates-ACTUAL-20261022');OLD=Path('/workspace/shared/brougham-parked-integration-TEXT-V2-HELD-20261022/proposed/chicago/4d')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(rel,data):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data if isinstance(data,bytes) else data.encode("utf-8","surrogateescape"));return p
# Safely import definitions only, never invoke the old V13 canonical check().
vpath=Path('/workspace/shared/brougham-v13-portable-intake-20261022/proposed/chicago/4d/tools/transport/brougham/check_portable.py');spec=importlib.util.spec_from_file_location('reader',vpath);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g,b=v.read(V14/'portable-near/brougham-near.glb');world=v.world_nodes(g)
def subtree(i):
 yield i
 for c in g['nodes'][i].get('children',[]):yield from subtree(c)
def points(i):
 out=[]
 for k in subtree(i):
  n=g['nodes'][k]
  if 'mesh' not in n:continue
  for p in g['meshes'][n['mesh']]['primitives']:
   ps=v.values(g,b,p['attributes']['POSITION']);ids=[r[0] for r in v.values(g,b,p['indices'])] if 'indices' in p else range(len(ps))
   out += [[ps[q][axis]+world[k][axis] for axis in range(3)] for q in ids]
 return out
def bounds(ps):return {'min':[min(p[k] for p in ps) for k in range(3)],'max':[max(p[k] for p in ps) for k in range(3)]}
wheel=[]
for i,n in enumerate(g['nodes']):
 if n['name'].startswith('vehicle_wheel_'):
  ps=points(i);bb=bounds(ps);low=[q for q in ps if abs(q[1]-bb['min'][1])<1e-7];assert abs(bb['min'][1])<1e-6
  wheel.append({'node':n['name'],'node_index':i,'center_root_m':world[i],'actual_indexed_triangle_bounds_root_m':bb,'lowest_triangle_vertices_root_m':sorted(set(tuple(q) for q in low)),'nominal_contact_xz_m':[world[i][0],world[i][2]],'plane_y_m':bb['min'][1]})
side=json.loads((V14/'portable-near/brougham.json').read_text(errors="surrogateescape"));rawside=json.loads((V14/'raw/brougham.json').read_text(errors="surrogateescape"))
part=next(x for x in rawside['parts'] if x['name']=='parked_pole_ground_shoe');meshnode=next(i for i,n in enumerate(g['nodes']) if n['name']=='surface_vehicle_team_pole_4');prim=g['meshes'][g['nodes'][meshnode]['mesh']]['primitives'][0];ids=[q[0] for q in v.values(g,b,prim['indices'])];ps=v.values(g,b,prim['attributes']['POSITION']);ids=ids[part['triangle_start_in_batch']*3:(part['triangle_start_in_batch']+part['triangles'])*3];shoe=[[ps[i][k]+world[meshnode][k] for k in range(3)] for i in ids];shoe_bottom=sorted(set(tuple(q) for q in shoe if abs(q[1])<1e-7));assert len(shoe_bottom)==4
assert all(any(max(abs(a-b) for a,b in zip(x,y))<1e-6 for y in shoe_bottom) for x in side['static_pole_ground_shoe_contact_root_m'])
math={'scope':'Read-only actual indexed-near accessor/hierarchy arithmetic, not terrain or visual proof','reader_path':str(vpath),'reader_sha256':h(vpath),'old_V13_check_not_called':True,'source_near_sha256':h(V14/'portable-near/brougham-near.glb'),'source_raw_sha256':h(V14/'raw/brougham.glb'),'frame':side['frame'],'actual_global_bounds_m':v.decoded_bounds(g,b,world),'wheel_rows':wheel,'actual_shoe_bottom_corners_root_m':shoe_bottom,'actual_shoe_bounds_root_m':bounds(shoe),'fixed_pole_not_hinged':True,'has_vehicle_tongue':any(n['name']=='vehicle_tongue' for n in g['nodes']),'hitch_parked_root_m':next(world[i] for i,n in enumerate(g['nodes']) if n['name']=='vehicle_hitch_team'),'terrain_and_obstacle_clearance':'UNKNOWN for this V14 at proposed world stand; must use actual1904carriagewayHeight for wheels and all shoe points, plus actual full-pole/body clearance in bounded integrated view. No ownership/force/hitch or working-height proof.'}
(R/'ACTUAL-NATIVE-CONTACT-READBACK.json').write_text(json.dumps(math,indent=2)+'\n')
# Exact reusable V2 text changes, with only V14-near delivery declaration, no invented mid/far.
paths=['data/transport/parked/placements.json','renderers/web/js/parked-transport.js','tools/transport/check_parked_placements.py','tools/transport/wagon_covered/check.py','tools/transport/wagon_covered/test_identity.py']
for rel in paths:put(rel,(OLD/rel).read_bytes())
r=json.loads((P/paths[0]).read_text(errors="surrogateescape"));r['_doc']='Parked type reconstructions. Existing1835 stands retained. The separate1904Brougham cites an evidenced1893catalogue design, not an attested local specimen or owner. L-parked-vehicles-2979; L-covered-wagons-2980; L-brougham-parked-2794.'
s=r['models']['studebaker_brougham_1893'];s['delivery_lods']={'near':'transport/parked-brougham/brougham-near.glb','runtime_distance_selection_enabled':False};s['basis']+=' V14 separates the two near-side footplates with opposite-side symmetry reconstructed; source/main/published/phone and photographic review remain open. Only the exact indexed near is proposed; no V14mid/far delivery is claimed.'
put(paths[0],json.dumps(r,indent=2)+'\n')
p=P/'tools/transport/check_parked_placements.py';s=p.read_text(errors="surrogateescape");s=s.replace("{'near':'transport/parked-brougham/brougham-near.glb','mid':'transport/parked-brougham/brougham-mid.glb','far':'transport/parked-brougham/brougham-far.glb','runtime_distance_selection_enabled':False}","{'near':'transport/parked-brougham/brougham-near.glb','runtime_distance_selection_enabled':False}");put('tools/transport/check_parked_placements.py',s)
# Keep supported source chain verbatim, not a rewrite or run.
for name in ['generate.py','source_details.py','index_streams.py','static_master.py','parameters.json','lods.json','LICENSE']:
 put('tools/transport/brougham/'+name,(V14/'source'/name).read_bytes())
for name in ['brougham.json','BUILD-RECEIPT.json','LICENSE']:
 put('renderers/web/transport/parked-brougham/'+name,(V14/'portable-near'/name).read_bytes())
# Append-only prose; these are candidate texts, not a claim of an executed intake.
lib='''\n\n### L-brougham-parked-2794 — separate catalogue-guided1904Brougham\n\n**Decision:** Propose one additional empty closed Brougham at localENU E1397.9,N−3240,bearing178.99 in1904, without replacing or branding generic C02. The1893Studebaker catalogue leaf0095 (source `studebaker_1893_illustrated_souvenir`, actual plateSHA256 `b458565ec06ba1e8e59d1455cc2d3f277c2371910b3085c2085749fc59a68abe`) attests a maker/type design before1904. It does not attest this individual vehicle, Chicago/Prairie presence, ownership, a Pullman/Glessner connection or this stop. `belongs_to` remains null.\n\n**Reconstructed:** all absolute metres, unseen sides/interior/construction, material optics, colors as pigment, hardware attachment/strength, pad thickness/hidden opposite-side symmetry and world stand. V14 source geometry has two separated rounded footplates per side and a fixed parked-down paired-team pole with original ground shoe; it is not single-horse shafts or an invented hinge. Only the indexednear is proposed. ExactV14near source/main/published/phone photographs, all actual wheel/shoe/carriageway and body/pole/obstacle clearance, card/pick/tier/disposal and ordinary release checks remain pending; no visual/full-LOD/photographic acceptance is asserted by this entry.\n\n**Unsupported:** occupants, live boarding, doors/steering, horses/hitch coupling/reins, collisions/physics and traffic. Native hitch[0,.037,3.8]m is a parked-down datum, not a usable working-height team interface. Existing30mmwheel-plane bound and Full100m/Balanced65m/Light0 remain unchanged; static shoe guard refuses nonfinite ground, >1mm penetration or >30mmgap on the same rendered surface. No automatic stand move, model tilt, hitch adjustment or hidden fallback qualifies a failed stand.\n\n**Ticket:** T-2794. Photographic/occupied completion remains OPEN.\n'''
put('docs/LIBERTIES.md',(APP/'docs/LIBERTIES.md').read_text(errors="surrogateescape")+lib)
for name in ['STATUS','ROADMAP']:
 put('docs/'+name+'.md',(APP/('docs/'+name+'.md')).read_text(errors="surrogateescape")+'''\n\n## T-2794 — V14 catalogue Brougham intake candidate (HELD)\n\nExact near13fe72e8 (1,213,592B/32,830tri) and original rawed15f009 (2,445,452B) preserve native metres/+Y/+Z, 41nodes/24meshes/6materials and original source continuity. A separate1904Prairie stand E1397.9,N−3240,bearing178.99 is proposed, without replacing genericC02 or assigning any household owner.1893Studebakerleaf0095 supports the catalogue maker/type, not this specimen, dimensions or location. Onlynear exists for thisV14delivery; mid/far and distanceLOD selection are not claimed. App/public intake and actual V14source/main/published/phone imagery, terrain/shoe/pole/body clearance, card/picking/tier/disposal and normal qualification are pending. Footplates remain original reconstructed solids, with static sources/anchors and all occupied/doors/hitch/collision/traffic capabilities off. Photographic finish and fullT-2794 remain OPEN.\n''')
license_note='''\n\n## V14 separate catalogue-guided Brougham — proposed1904parked intake (T-2794)\n\nOriginal project GPL-3.0-or-later producer/source and generated geometry: tools/transport/brougham/{generate.py,source_details.py,index_streams.py,static_master.py,parameters.json,lods.json,LICENSE}; rawmastered15f00934809cf04f7946377c18a6d3c2c0a5501041ebcd5ff257b96a1d8f8e, indexednear13fe72e80ad746e697088255dd0b8984bc8c4eafdd41ceb0ba4962a2001bf133, sidecar/build receipt and LICENSE under transport/parked-brougham. No third-party model, texture or image pixels; solid proceduralPBR only. Exact source is original geometry guided by public-domain US1893Studebakercatalogue0095, source studebaker_1893_illustrated_souvenir /plateb458565ec06ba1e8e59d1455cc2d3f277c2371910b3085c2085749fc59a68abe. Maker/type availability is evidenced; local specimen, owner, metres, hidden construction and optical materials are reconstructed. No new file under assets/ is proposed. Original rawmaster/source must ship in reviewable source delivery; no binary artifact is a substitute for source. NoV14mid/far, photorealism or active occupied interface accepted.\n'''
put('renderers/web/transport/LICENSES.md',(APP/'renderers/web/transport/LICENSES.md').read_text(errors="surrogateescape")+license_note)
# Source master/near binaries deliberately not duplicated, root must install exact files after acceptance.
delivery=[]
for a,d in [('portable-near/brougham-source.glb','renderers/web/transport/parked-brougham/brougham-source.glb'),('portable-near/brougham-near.glb','renderers/web/transport/parked-brougham/brougham-near.glb')]:
 f=V14/a;delivery.append({'source':str(f),'target':d,'bytes':f.stat().st_size,'sha256':h(f),'copied_or_installed':False})
(R/'EXACT-UNINSTALLED-BINARY-DELIVERY.json').write_text(json.dumps(delivery,indent=2)+'\n')
# Structural preservation and syntax only; no app/source generation/checkgate/browser.
base=json.loads((APP/'data/transport/parked/placements.json').read_text(errors="surrogateescape"));new=json.loads((P/'data/transport/parked/placements.json').read_text(errors="surrogateescape"));assert new['scenes']['1835']==base['scenes']['1835'];assert new['scenes']['1904'][:-1]==base['scenes']['1904'];assert all(new['models'][k]==z for k,z in base['models'].items());assert new['scenes']['1904'][-1]['belongs_to'] is None
for f in P.rglob('*.json'):json.loads(f.read_text(errors="surrogateescape"))
for f in P.rglob('*.py'):ast.parse(f.read_text(errors="surrogateescape"))
patch=[];pins=[]
for f in sorted(P.rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(P);base=APP/rel;a=base.read_text(errors="surrogateescape").splitlines(True) if base.exists() else [];z=f.read_text(errors="surrogateescape").splitlines(True)
 patch.extend(difflib.unified_diff(a,z,fromfile='a/chicago/4d/'+str(rel) if base.exists() else '/dev/null',tofile='b/chicago/4d/'+str(rel)))
 pins.append({'path':'chicago/4d/'+str(rel),'base_sha256':h(base) if base.exists() else None,'candidate_sha256':h(f),'candidate_bytes':f.stat().st_size})
(R/'CANDIDATE-UNAPPLIED.patch').write_bytes(''.join(patch).encode('utf-8','surrogateescape'))
(R/'BASE-AND-DELTA-PINS.json').write_text(json.dumps({'status':'HELD_SOURCE_TEXT_ONLY_NOT_READY_TO_APPLY','changes':pins,'retained_catalogue_source_sha256':h(APP/'data/sources/studebaker_1893_illustrated_souvenir.json'),'binary_delivery_not_installed':delivery,'prior_V2_guard_reused':'Same-provider static shoe check retained verbatim; only near delivery declaration narrowed. No old V13 canonical checker/check.sh registration copied because it pins wrong master/tri count and requires missing3LODs.','structural_checks':'All existing model/row values and entire1835scene byte-structure exact; C02 unchanged. JSONparse/PythonAST passed; no production tests or generation executed.','old_V2_manifest':h(Path('/workspace/shared/brougham-parked-integration-TEXT-V2-HELD-20261022/BASE-AND-DELTA-PINS.json'))},indent=2)+'\n')
print(json.dumps({'output':str(R),'patch_sha256':h(R/'CANDIDATE-UNAPPLIED.patch'),'native_readback':math,'files':len(pins)},indent=2))
