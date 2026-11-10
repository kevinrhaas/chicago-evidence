import datetime, hashlib, json, re, subprocess, sys
from pathlib import Path
REPO=Path('/tmp/chicago-west-wicket-20261109'); APP=REPO/'chicago/4d'; OUT=Path('/tmp/nov10-group-native-final')
BASE='c5382c727ae06e0ba1cd6816cc072cbfba4d963d'; OLD='42db9ce562201f64a1ba334a3ce7b4c6a9a70c07'
def git(*args): return subprocess.check_output(['git',*args],cwd=REPO)
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(d): return json.dumps(d,sort_keys=True,separators=(',',':')).encode()
def write(name,d): (OUT/name).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def file_receipt(p):
 b=p.read_bytes(); return {'path':str(p.relative_to(REPO)),'bytes':len(b),'sha256':sha(b)}
head=git('rev-parse','HEAD').decode().strip(); status=git('status','--porcelain').decode()
assert head == '5484f145fb02e51a4f43a773c4bf818ab9e46b8f',head
assert not status,status
sys.path.insert(0,str(APP/'generators'))
from mesh_inputs import structure_inputs_doc, structure_inputs_sha
from common import versions
reg={}; registry_files={}
for n in ['manifest.json','manifest.web.json','manifest.versions.json']:
 p=APP/'assets'/n; b=p.read_bytes(); old=git('show',BASE+':chicago/4d/assets/'+n)
 assert b==old,(n,'registry drift from dev')
 (OUT/('BEFORE-'+n)).write_bytes(b); reg[n]=json.loads(b)
 registry_files['assets/'+n]={**file_receipt(p),'origin_dev_blob':git('rev-parse',BASE+':chicago/4d/assets/'+n).decode().strip(),'byte_equal_origin_dev':True}
assets=reg['manifest.json']['assets']; web=reg['manifest.web.json']['masters']; variants=reg['manifest.versions.json']['assets']
rows=[]; foreign={}; foreign_versions={}; changed=[]; current_hashes={}; sourcepaths=set(); problems=[]
for key,row in sorted(assets.items()):
 sid=row.get('structure_id'); current=None; doc=None
 if sid:
  path=APP/'data/structures'/f'{sid}.json'; record=json.loads(path.read_text()); phase=next(x for x in record['phases'] if x['id']==row['phase_id'])
  doc=structure_inputs_doc(record,phase,row['archetype']); current=structure_inputs_sha(record,phase,row['archetype']); current_hashes[key]=current
 selected=row.get('archetype')=='log_dwelling' or sid=='green_tree_tavern'
 if current is not None and current!=row.get('inputs_sha256'): changed.append(key)
 master=file_receipt(APP/'assets/gltf'/key)
 web_outputs=[file_receipt(APP/'assets/web'/key)]
 for lod_key in versions.lod_asset_keys(key).values(): web_outputs.append(file_receipt(APP/'assets/web'/lod_key))
 if master['bytes']!=row['bytes']: problems.append([key,'master bytecount mismatch'])
 if master['sha256']!=web.get(key): problems.append([key,'web master receipt mismatch'])
 item={'old_registry_row':row,'old_registry_row_canonical_sha256':sha(canon(row)),'before_master':master,'before_web_outputs':web_outputs,'web_receipt_master_sha256':web.get(key)}
 if selected:
  assert doc is not None
  assert current!=row['inputs_sha256'],(key,'unexpected fresh selected')
  sourcepaths.add(str(path.relative_to(REPO)))
  sourcepaths.update('chicago/4d/generators/'+n for n in doc['code'])
  rows.append({'asset_key':key,'structure_id':sid,'phase_id':row['phase_id'],'archetype':row['archetype'],'intentional_geometry_target':sid in ['cobweb_castle','green_tree_tavern'],'current_inputs_doc':doc,'current_inputs_sha256':current,**item})
 else: foreign[key]=item
for key,row in sorted(variants.items()):
 p=APP/'data/structures/versions'/row['structure_id']/(row['version_label']+'.json'); record=json.loads(p.read_text()); phase=next(x for x in record['phases'] if x['id']==row['phase_id'])
 current=structure_inputs_sha(record,phase,row['archetype']); assert current==row['inputs_sha256'],(key,'stale foreign variant')
 master=file_receipt(APP/'assets/gltf'/key); outputs=[file_receipt(APP/'assets/web'/key)]
 for lod_key in versions.lod_asset_keys(key).values(): outputs.append(file_receipt(APP/'assets/web'/lod_key))
 assert master['bytes']==row['bytes']; assert master['sha256']==row['web_master_sha256']
 foreign_versions[key]={'row':row,'canonical_sha256':sha(canon(row)),'current_inputs_sha256':current,'before_master':master,'before_web_outputs':outputs}
ids=sorted({x['structure_id'] for x in rows}); keys=sorted(x['asset_key'] for x in rows)
assert len(assets)==1044 and len(variants)==6
assert len(rows)==83 and len(ids)==83 and len(foreign)==961 and len(foreign_versions)==6
assert len([x for x in rows if x['archetype']=='log_dwelling'])==82
assert len([x for x in rows if not x['intentional_geometry_target']])==81
assert len([x for x in rows if x['intentional_geometry_target']])==2
assert changed==keys,{'unexpected_stale':sorted(set(changed)-set(keys)),'missing_stale':sorted(set(keys)-set(changed))}
assert not any('jail' in x for x in ids)
assert not problems,problems
recipe_paths=['.github/workflows/chicago-4d-bake.yml']+['chicago/4d/'+n for n in ['generators/blender.pin','generators/build.py','generators/emit.py','generators/mesh_inputs.py','generators/archetypes/log_dwelling.py','generators/archetypes/log_dwelling_params.py','generators/archetypes/frame_tavern.py','generators/archetypes/frame_tavern_params.py','tools/bake.sh','tools/bake_ref.py','tools/web_derivatives.sh']]
sourcepaths.update(recipe_paths)
sourcepaths.update('chicago/4d/assets/'+n for n in reg)
sourcepaths.add('chicago/4d/data/enclosures/log_jail_palisade.json')
source_invariance={}
for path in sorted(sourcepaths):
 b=(REPO/path).read_bytes(); old=git('show',OLD+':'+path)
 same=b==old
 if not same:
  assert path=='chicago/4d/data/structures/cobweb_castle.json',(path,'unexpected source drift from42db')
  before=b'Exterior lower-wall fields'; after=b'The exterior lower-wall fields'
  assert old.count(before)==1 and old.replace(before,after)==b,(path,'unexpected Cobweb prose edit')
 source_invariance[path]={**file_receipt(REPO/path),'byte_equal_pre_merge_head':same,'permitted_prose_only_edit':not same}
previous=json.loads(Path('/tmp/nov10-group-native/BEFORE-BINDING.json').read_text())
assert previous['captured_HEAD']==OLD
prior={x['asset_key']:x for x in previous['affected']}
assert set(prior)==set(keys)
for row in rows:
 old=prior[row['asset_key']]
 for field in ['current_inputs_doc','current_inputs_sha256','old_registry_row','before_master','before_web_outputs','web_receipt_master_sha256']:
  assert canon(row[field])==canon(old[field]),(row['asset_key'],field,'geometry/input/baseline differs from42db')
assert sha(canon(foreign))==previous['foreign_default_rows_set_canonical_sha256']
assert sha(canon(foreign_versions))==previous['foreign_version_rows_set_canonical_sha256']
pin=(APP/'generators/blender.pin').read_text()
(OUT/'only.txt').write_text(','.join(ids)+'\n')
(OUT/'asset-keys.txt').write_text('\n'.join(keys)+'\n')
write('BEFORE-foreign-defaults.json',foreign); write('BEFORE-foreign-versions.json',foreign_versions)
endhead=git('rev-parse','HEAD').decode().strip(); endstatus=git('status','--porcelain').decode()
assert head==endhead and status==endstatus,(head,endhead,status,endstatus)
for name,r in registry_files.items(): assert file_receipt(APP/name)['sha256']==r['sha256']
binding={'status':'EXACT BEFORE BINDING; NOT A NATIVE EXPORT OR IMAGE MATCH','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'captured_HEAD':head,'source_branch':git('branch','--show-current').decode().strip(),'source_base':BASE,'pre_merge_HEAD':OLD,'source_state':{'clean_before':True,'clean_after':True,'head_unchanged_during_capture':True,'source_invariance':source_invariance,'same_83_mesh_input_docs_and_hashes_as_42db':True,'same_asset_and_registry_baselines_as_42db':True},'counts':{'default_registry':len(assets),'version_registry':len(variants),'selected_defaults':len(rows),'selected_versions':0,'selected_structure_ids':len(ids),'log_dwelling_defaults':82,'intentional_geometry_targets':2,'non_target_controls':81,'foreign_defaults':len(foreign),'foreign_versions':len(foreign_versions),'actual_stale_default_inputs':len(changed)},'structure_ids':ids,'only':','.join(ids),'affected':rows,'foreign_default_rows_file':'BEFORE-foreign-defaults.json','foreign_default_rows_set_canonical_sha256':sha(canon(foreign)),'foreign_version_rows_file':'BEFORE-foreign-versions.json','foreign_version_rows_set_canonical_sha256':sha(canon(foreign_versions)),'registry_files':registry_files,'recipes':{p:file_receipt(REPO/p) for p in recipe_paths},'pin':{'version':re.search(r'^BLENDER_VERSION=(.*)$',pin,re.M)[1],'archive_sha256':re.search(r'^BLENDER_SHA256=(.*)$',pin,re.M)[1],'raw':pin},'notes':['Actual file readback captures every default and variant MASTER and WEB bytes/hash, including opt-in LODs. No exported mesh has been generated by this capture.','All 83 selected default inputs differ from current-dev registry; all other structure inputs and all 6 variant inputs are fresh. Terrain input freshness is delegated to the literal validator log.','Jail enclosure sidecar change is intentionally excluded from native dispatch.','All 83 actual resolved mesh input documents and hashes plus asset/registry baselines equal the frozen 42db packet. All 103 bound paths equal42db except exactly the documented Cobweb prose edit Exterior lower-wall fields -> The exterior lower-wall fields. Jail picture outputs change no bound mesh inputs.']}
write('BEFORE-BINDING.json',binding)
print(json.dumps({'status':'CAPTURE PASS','head':head,'counts':binding['counts'],'only_sha256':sha((OUT/'only.txt').read_bytes()),'binding_sha256':sha((OUT/'BEFORE-BINDING.json').read_bytes())},indent=2))
