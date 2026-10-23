from pathlib import Path
import ast,collections,copy,hashlib,json,shutil,sys
BASE=Path(__file__).resolve().parent
APP=Path('/workspace/chicago-waistcoat/chicago/4d');DST=BASE/'REGISTRATION/chicago/4d';TOOLS=DST/'tools/transport/brougham';ASSET=DST/'renderers/web/transport/parked-brougham'
assert not DST.exists(),'One staged registration only; preserve previous states'
shutil.copytree(APP/'tools/transport/brougham',TOOLS,ignore=shutil.ignore_patterns('__pycache__'))
shutil.copytree(APP/'renderers/web/transport/parked-brougham',ASSET,ignore=shutil.ignore_patterns('__pycache__'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Preserve all superseded active registration/producer/metadata text exactly.
archive=TOOLS/'archive-v17';archive.mkdir()
for n in ['generate.py','check_near.py','check_mid.py','near-contract.json','mid-contract.json']:
 shutil.copy2(TOOLS/n,archive/n)
for n in ['brougham.json','BUILD-RECEIPT.json','MID-BUILD-RECEIPT.json']:
 shutil.copy2(ASSET/n,archive/n)
(archive/'README.md').write_text('Original V17 producer, strict near/mid gates/contracts and delivery metadata preserved byte-exact before V18 lamp registration. Its original GLBs remain Git-history assets from merged PR1175. These files are historical V17 predicates/evidence; active V18 uses a separately measured new contract. No old gate/result is relabelled.\n')
shutil.copy2(BASE/'source/generate.py',TOOLS/'generate.py')
for n in ['brougham-source.glb','brougham-near.glb','brougham-mid-source.glb','brougham-mid.glb','brougham.json']:
 shutil.copy2(BASE/'ACTUAL/delivery'/n,ASSET/n)
proof=json.loads((BASE/'ACTUAL/NATIVE-RESULT.json').read_text());terminal=json.loads((BASE/'ACTUAL/TERMINAL.json').read_text());assert proof['pass'] and terminal['pass'];rows=proof['rows'];assert [x['triangles']for x in rows]==[33374,11706]
side=json.loads((ASSET/'brougham.json').read_text());side['native_variant']='V18_rounded_coach_lamps';side['status']='Rounded coach-lamp native geometry validated; source-matched browser comparison and world/photographic qualification pending';side['near_actual_visual_evidence']='Current V18 default source8 attempt failed before page due Chromium thread exhaustion; no visual acceptance. Earlier V17 images retained as baseline only.'
(ASSET/'brougham.json').write_text(json.dumps(side,indent=2)+'\n')
receipt={'variant':'V18_rounded_coach_lamps','source_generated_twice_deterministic':True,'generation_invocations':4,'near_lossless_PN_exact':True,'mid_lossless_PN_exact':True,'actual_native_unit_seconds':terminal['elapsed_seconds'],'rows':[{k:v for k,v in r.items()if k in ['detail','triangles','parts','protected_parts','source_bytes','indexed_bytes','expanded_triangle_PN_sha256','source_sha256','indexed_sha256','lossless_indexing','meshopt_or_quantization','bounds_m','unchanged_raw_mesh_batches']}for r in rows],'material_definitions_exact':7,'nodes_exact':42,'raw_mesh_batches_exact':25,'source8_or_world_or_photo_accepted':False,'native_differential_checker_sha256':sha(BASE/'check_lamp_delta_HELD.py'),'native_terminal_sha256':sha(BASE/'ACTUAL/TERMINAL.json'),'negative_controls':proof['negative_controls']}
(ASSET/'BUILD-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
midreceipt={k:rows[1][k]for k in ['source_bytes','indexed_bytes','expanded_triangle_PN_sha256','source_sha256','indexed_sha256','lossless_indexing','meshopt_or_quantization']};midreceipt.update(variant='V18_rounded_coach_lamps',near_and_mid_new_lamp_geometry='Exact fixed heads/lower bodies; existing finial follows unchanged tessellation recipes')
(ASSET/'MID-BUILD-RECEIPT.json').write_text(json.dumps(midreceipt,indent=2)+'\n')
for suffix in ['near-raw','near-indexed','mid-raw','mid-indexed']:shutil.copy2(BASE/'ACTUAL'/('khronos-'+suffix+'.json'),TOOLS/'archived-khronos'/('V18-'+suffix+'.json'))
# The numeric lamp surface predicates are copied verbatim from the actually passed differential checker.
src=(BASE/'check_lamp_delta_HELD.py').read_text();tree=ast.parse(src);names=['require','keyed','protected','digest_rows','vector','dot','cross','average','point_rows','native_box','contained','lamp_surfaces']
helper='''# SPDX-License-Identifier: GPL-3.0-or-later\n"""V18 exact lamp surface and protected V17 stream readback; original numerical guards retained."""\nimport collections,hashlib,json,math,struct\nfrom check_mid import bind_parts\n'''
for n in tree.body:
 if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name)and x.id in ['OLD','NEW','EXPECTED_OWNED','EXPECTED_MATERIAL']for x in n.targets):helper+=ast.get_source_segment(src,n)+'\n'
 elif isinstance(n,ast.FunctionDef)and n.name in names:helper+='\n'+ast.get_source_segment(src,n)+'\n'
helper+='''\ndef protected_signatures_v18(j,b):\n rows=keyed(j,b);kept=protected(rows,NEW)\n require(len(kept)==450,'Exact protected V17 non-lamp occurrence inventory')\n require(not any(k[0]in OLD-{'lamp_finial'} for k in rows),'Superseded lamp family returned')\n parents={c:i for i,n in enumerate(j['nodes'])for c in n.get('children',[])};nodes={n['mesh']:i for i,n in enumerate(j['nodes'])if 'mesh'in n}\n h=hashlib.sha256();streams=0\n for i,m in enumerate(j['meshes']):\n  prim=m['primitives'][0]\n  if(parents[nodes[i]],prim['material'])in[(1,3),(1,4),(1,5)]:continue\n  h.update(json.dumps([i,m['name']],separators=(',',':')).encode())\n  for kind in ['POSITION','NORMAL']:\n   a=j['accessors'][prim['attributes'][kind]];v=j['bufferViews'][a['bufferView']];require(a['componentType']==5126 and a['type']=='VEC3'and not v.get('byteStride'),'Actual raw float32 source stream')\n   off=v.get('byteOffset',0)+a.get('byteOffset',0);h.update(b[off:off+a['count']*12]);streams+=1\n require(streams==44,'Exactly22 protected non-lamp raw batches')\n return{'parts':len(kept),'protected_part_PN_sha256':digest_rows(kept),'mesh_streams':streams,'protected_mesh_PN_sha256':h.hexdigest()}\n'''
(TOOLS/'lamp_geometry.py').write_text(helper);compile(helper,str(TOOLS/'lamp_geometry.py'),'exec')
sys.path.insert(0,str(TOOLS));from check_near import read,expanded
from lamp_geometry import protected_signatures_v18,lamp_surfaces,keyed
nearj,nearb=read(ASSET/'brougham-source.glb');midj,midb=read(ASSET/'brougham-mid-source.glb');oldj,oldb=read(APP/'renderers/web/transport/parked-brougham/brougham-source.glb')
# Independent canonical signature has identical non-lamp rows/batches to actual V17 baseline.
# Build this comparison using the same digest with OLD filtering for baseline.
import lamp_geometry
oldnew=lamp_geometry.NEW
try:
 lamp_geometry.NEW=lamp_geometry.OLD
 oldsig=protected_signatures_v18(oldj,oldb)
finally:lamp_geometry.NEW=oldnew
sig=protected_signatures_v18(nearj,nearb);assert sig==oldsig and sig['protected_part_PN_sha256']==rows[0]['protected_PN_sha256']
# Actual report data, not symbolic source counts, bind the active contracts.
near=json.loads((archive/'near-contract.json').read_text());near.update(scope='Exact33374 V18 rounded-coach-lamp near delivery with independently pinned11706 mid; photographic/source8/world acceptance remains pending',raw_sha256=rows[0]['source_sha256'],near_sha256=rows[0]['indexed_sha256'],raw_bytes=rows[0]['source_bytes'],near_bytes=rows[0]['indexed_bytes'],triangles=33374,expanded_PN_sha256=rows[0]['expanded_triangle_PN_sha256'],protected_V17_streams=sig,static_master=side['static_master'],protected_baseline_raw_sha256=sha(APP/'renderers/web/transport/parked-brougham/brougham-source.glb'),baseline_compared_at_preparation_only=True)
for n in ['protected_V15_streams','source_part_index_map_from_V15']:near.pop(n,None)
near['native_variant']='V18_rounded_coach_lamps';near['source_files']['generate.py']=sha(TOOLS/'generate.py');near['source_files']['lamp_geometry.py']=sha(TOOLS/'lamp_geometry.py')
near['delivery_metadata_files']={n:sha(ASSET/n)for n in ['BUILD-RECEIPT.json','LICENSE','brougham.json']}
near['archived_khronos']=[]
for suffix,filename in [('near-raw','brougham-source.glb'),('near-indexed','brougham-near.glb')]:
 report='V18-'+suffix+'.json';near['archived_khronos'].append({'report':report,'report_sha256':sha(TOOLS/'archived-khronos'/report),'bound_file':filename,'actual_input_sha256':sha(ASSET/filename)})
(TOOLS/'near-contract.json').write_text(json.dumps(near,indent=2)+'\n')
mid=json.loads((archive/'mid-contract.json').read_text());mid.update(scope='Exact source-tessellated V18 ring16 distance-mid11706; rounded lamp surfaces retain strict native/winding/seam guards',raw_sha256=rows[1]['source_sha256'],raw_bytes=rows[1]['source_bytes'],indexed_sha256=rows[1]['indexed_sha256'],indexed_bytes=rows[1]['indexed_bytes'],expanded_triangle_PN_sha256=rows[1]['expanded_triangle_PN_sha256'],unchanged_near_sha256=rows[0]['indexed_sha256'],subdivision_records_near=480,subdivision_records_mid=314,build_receipt_sha256=sha(ASSET/'MID-BUILD-RECEIPT.json'))
mid['native_variant']='V18_rounded_coach_lamps';mid['physical_category_triangle_counts']=dict(sum((collections.Counter({p['name']:p['triangles']})for p in midj['extras']['parts']),collections.Counter()))
mid['archived_current_validator_reports']={('V18-'+suffix+'.json'):sha(TOOLS/'archived-khronos'/('V18-'+suffix+'.json'))for suffix in ['mid-raw','mid-indexed']}
(TOOLS/'mid-contract.json').write_text(json.dumps(mid,indent=2)+'\n')
# Register exact new variant numbers. All old V17 predicates are preserved verbatim in archive-v17.
s=(archive/'check_near.py').read_text().replace('V17','V18').replace('33502','33374').replace("==468","==480").replace('protected_V15_streams','protected_V17_streams').replace('464part/46stream role-mapped V15 baseline','450part/44stream exact V17 non-lamp baseline')
a=s.index('def protected_signatures(j,b):');z=s.index('\ndef subtree(',a)
s=s[:a]+"def protected_signatures(j,b):\n    from lamp_geometry import protected_signatures_v18\n    return protected_signatures_v18(j,b)\n"+s[z:]
s=s.replace("    params=json.loads((source_directory/'parameters.json').read_text());extra=j['extras'];assert extra['parameters']==params", "    params=json.loads((source_directory/'parameters.json').read_text());extra=j['extras'];assert extra['parameters']==params\n    from lamp_geometry import keyed,lamp_surfaces\n    assert lamp_surfaces(keyed(j,b),params)==456, 'Actual rounded-lamp winding/recessed aperture seams'")
s=s.replace("EXPECTED_CONTRACT='860b7df7c8d25e1aa372a0a4250f92e4dfffb2c7cfbd14450b9db329cf5fc910'","EXPECTED_CONTRACT='"+sha(TOOLS/'near-contract.json')+"'")
(TOOLS/'check_near.py').write_text(s);compile(s,str(TOOLS/'check_near.py'),'exec')
s=(archive/'check_mid.py').read_text().replace("9f094861d08398d4a2a5e6bba3611c23af98d8db7c73554df1df1ec4950fcab4",sha(TOOLS/'mid-contract.json')).replace('33502','33374').replace('==468','==480').replace('==302','==314').replace("'subdivision_records_before':468","'subdivision_records_before':480").replace("'subdivision_records_after':302","'subdivision_records_after':314")
s=s.replace("    before=bind_parts(old,ob);after=bind_parts(new,nb);assert len(before)==480 and len(after)==314", "    before=bind_parts(old,ob);after=bind_parts(new,nb);assert len(before)==480 and len(after)==314\n    from lamp_geometry import keyed,lamp_surfaces\n    assert lamp_surfaces(keyed(new,nb),new['extras']['parameters'])==424, 'Actual mid rounded-lamp winding/recessed aperture seams'")
(TOOLS/'check_mid.py').write_text(s);compile(s,str(TOOLS/'check_mid.py'),'exec')
# Readback telemetry and native LOD tests register measured new near triangle count only.
p=DST/'renderers/web/js/parked-transport.js';p.parent.mkdir(parents=True);p.write_text((APP/'renderers/web/js/parked-transport.js').read_text().replace('33502','33374'))
p=TOOLS/'test_lod.mjs';p.write_text(p.read_text().replace('33502','33374'))
files=[]
for p in sorted(DST.rglob('*')):
 if p.is_file() and '__pycache__'not in p.parts:
  rel=p.relative_to(DST);old=APP/rel
  if not old.exists() or p.read_bytes()!=old.read_bytes():files.append({'path':str(rel),'bytes':p.stat().st_size,'sha256':sha(p),'preimage_sha256':sha(old)if old.exists()else None})
(BASE/'REGISTRATION/CHANGED-FILES.json').write_text(json.dumps(files,indent=2)+'\n')
(BASE/'REGISTRATION/README.md').write_text('''# Scoped V18 registration candidate — NOT APP INSTALLED\n\nActual native geometry passed5.068s with4fresh Khronos reports/eight corruptions rejected. Default source8 browser failed before page due thread exhaustion; no image/app/photographic acceptance. Root must review actual image results before intake.\n\nComplete active V18 near/mid contracts register actual33374/11706 triangles and480/314parts, exact source/delivery hashes and reports. Original V17 producer/gates/contracts/metadata are preserved byte-exact in tools/transport/brougham/archive-v17; original archived Khronos reports remain untouched. All unit-normal1e-4, squared-area1e-20, complete wheel/shoe/pole contacts, bounds, anchors, proxy containment, near/mid category/stream, source/license/date and sidecar predicates retain their numerical limits. New lamp winding/recessed-aperture seam checks are verbatim from the actually passed native differential checker.450 original nonlamp occurrences and22raw batches remain protected by exact V17-compared P/N signatures. No actor/reach/LOD selection logic changed; two runtime telemetry and three actual loader-test metrics register actualnewnearcount.\n\nCHANGED-FILES.json is the exact copy/intake inventory including preimage pins. Canonical provenance/liberties/docs/changelog, fullgate, preflight, browser/world/mobile budgets and PR handling remain root work. No new licence/source image; GPL producer and catalogue public-domain reference remain unchanged.\n''')
print('Prepared scoped V18 registration',len(files),'changed/new files; contract',sha(TOOLS/'near-contract.json'),sha(TOOLS/'mid-contract.json'))
