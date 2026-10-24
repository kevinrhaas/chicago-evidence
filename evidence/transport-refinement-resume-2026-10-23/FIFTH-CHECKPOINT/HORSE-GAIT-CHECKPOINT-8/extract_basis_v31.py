from pathlib import Path
import json,hashlib,sys,resource
import numpy as np
r=Path(__file__).parent;d=r/'V31-SPLIT-PORTABLE-CREEPING-PROTOTYPE';sys.path.insert(0,str(r/'V28-PERIODIC-TEMPORAL-CORRECTION'));from actual_model import Model
old=r/'CHECKPOINT-7/V30-PORTABLE-CREEPING-PROTOTYPE/creeping-015mps-PORTABLE-STUDY-NOT-APP.glb';a=Model(old);assert hashlib.sha256(a.raw).hexdigest()=='8fc20cf20549d9588c56202d93315dc9f718531fc7a285de2208ce4e36ba9a7b';base=Model(Path('/workspace/shared/T2800-V16-PLANTED-STANDING-GLB-EXPORT-ACTUAL-20261023/horse-sevket-v16-planted-standing-v1.glb'));assert hashlib.sha256(base.raw).hexdigest()=='b479442cb03ac46eb13c19da15a79cdfaf28dbdf356b116f78de7ce7ecdc60be';assert a.bin[:len(base.bin)]==base.bin
for field in ['materials','images','textures','samplers','skins','scenes','scene']:assert a.g.get(field)==base.g.get(field)
assert a.g['accessors'][:len(base.g['accessors'])]==base.g['accessors'];assert a.g['bufferViews'][:len(base.g['bufferViews'])]==base.g['bufferViews'];assert a.g['animations'][:-1]==base.g['animations']
for ni,(before,after)in enumerate(zip(base.g['nodes'],a.g['nodes'])):
 after=after.copy()
 if ni==27:after.pop('weights')
 assert after==before
for mi,(before,after)in enumerate(zip(base.g['meshes'],a.g['meshes'])):
 after=json.loads(json.dumps(after))
 if mi==a.g['nodes'][27]['mesh']:after.pop('weights');after['primitives'][0].pop('targets')
 assert after==before
targets=a.g['meshes'][a.g['nodes'][27]['mesh']]['primitives'][0]['targets'];assert len(targets)==15;fields={};pins=[]
for i,t in enumerate(targets):
 row={}
 for att in ['POSITION','NORMAL']:
  v=a.accessor(t[att]);assert v.dtype==np.dtype('<f4')and v.shape==(4313,3);fields[f'{i:02d}_{att}']=v;row[att]=hashlib.sha256(v.tobytes()).hexdigest()
 pins.append(row)
np.savez(d/'EXACT-SELECTED-15-BINDLOCAL-BASIS.npz',**fields)
payload=a.bin[len(base.bin):];(d/'SELECTED-BASIS-AND-ANIMATION.bin').write_bytes(payload);(d/'SERIALIZATION-BOUNDARY-JSON.json').write_text(json.dumps(a.g,separators=(',',':'))+'\n')
source=r/'CHECKPOINT-7/encode_portable_v30.py';receipt=json.loads((r/'CHECKPOINT-7/V30-PORTABLE-CREEPING-PROTOTYPE/ACTUAL-UNIT-RECEIPT.json').read_text());assert hashlib.sha256(source.read_bytes()).hexdigest()==receipt['source_sha256']['encode_portable_v30.py'];source_screen=r/'CHECKPOINT-7/V30-PORTABLE-CREEPING-PROTOTYPE/ACTUAL-COHERENT-RANK-AND-SOURCE129-SCREEN.json';screen=json.loads(source_screen.read_text());assert screen['total_morph_targets']==15 and screen['CPU_source129_screen']['PASS']
out={'status':'EXACT_SELECTED_BASIS_BOUNDARY_EXTRACTION_NOT_PORTABLE_ACCEPTANCE','original_V30_resource_FAIL_retained':True,'source_glb_sha256':hashlib.sha256(a.raw).hexdigest(),'source_encoder_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source129_report_sha256':hashlib.sha256(source_screen.read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256(base.raw).hexdigest(),'target_count':15,'per_target_float32_field_sha256':pins,'appended_payload_sha256':hashlib.sha256(payload).hexdigest(),'json_boundary_sha256':hashlib.sha256((d/'SERIALIZATION-BOUNDARY-JSON.json').read_bytes()).hexdigest(),'extracted_basis_sha256':hashlib.sha256((d/'EXACT-SELECTED-15-BINDLOCAL-BASIS.npz').read_bytes()).hexdigest(),'baseline_BIN_exact':True,'baseline_rest_skin_geometry_materials_clips_protected':True,'maximum_RSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024};(d/'ACTUAL-BASIS-EXTRACTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['maximum_RSS_bytes']<=536870912
