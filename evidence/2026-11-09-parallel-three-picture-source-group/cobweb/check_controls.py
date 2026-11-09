import sys,types,json,subprocess,hashlib,dataclasses,inspect
from pathlib import Path
ROOT=Path('/tmp/nov9-group-cobweb/chicago/4d'); REPO=ROOT.parents[1]; FULL=Path('/tmp/chicago-resume-20261109/chicago/4d'); OUT=Path('/tmp/nov9-cobweb-group')
sys.path.insert(0,str(ROOT/'generators'));sys.modules.setdefault('bpy',types.ModuleType('bpy'))
from archetypes import log_dwelling as new
from archetypes import log_dwelling_params as params
from common.mesh import MeshBuilder

def load_old(name,rel):
 m=types.ModuleType(name);m.__file__=str(ROOT/rel);sys.modules[name]=m
 src=subprocess.check_output(['git','show','HEAD:chicago/4d/'+rel],cwd=REPO).decode();exec(compile(src,m.__file__,'exec'),m.__dict__);return m
oldp=load_old('cobweb_baseline_params','generators/archetypes/log_dwelling_params.py')
old=load_old('cobweb_baseline_builder','generators/archetypes/log_dwelling.py')
def mat(name,rgba,**kw):return [name,list(rgba),kw]
old.simple_material=new.simple_material=mat
MeshBuilder.to_object=lambda self,mats:dict(verts=self.verts,faces=self.faces,conf=self.conf,mat_index=self.mat_index,named=self.named,mats=mats)
def digest(r):return hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert [(f.name,f.kw_only,f.default) for f in dataclasses.fields(params.LogDwellingParams) if f.name!='compound_clapboard_height_m']==[(f.name,f.kw_only,f.default) for f in dataclasses.fields(oldp.LogDwellingParams)]
legacy=inspect.signature(oldp.LogDwellingParams);current=inspect.signature(params.LogDwellingParams)
assert [(n,p.kind,p.default) for n,p in current.parameters.items() if n!='compound_clapboard_height_m']==[(n,p.kind,p.default) for n,p in legacy.parameters.items()]
manifest=json.loads((FULL/'assets/manifest.json').read_text());web=json.loads((FULL/'assets/manifest.web.json').read_text());versions=json.loads((FULL/'assets/manifest.versions.json').read_text());rows=[]
for key,row in manifest['assets'].items():
 if row.get('archetype')!='log_dwelling':continue
 sid=row['structure_id'];pid=row['phase_id'];path=ROOT/'data/structures'/f'{sid}.json';nr=json.loads(path.read_text());br=json.loads(subprocess.check_output(['git','show','HEAD:chicago/4d/data/structures/'+path.name],cwd=REPO));np=next(p for p in nr['phases'] if p['id']==pid);bp=next(p for p in br['phases'] if p['id']==pid);newp=params.from_phase(np,nr);beforep=oldp.from_phase(bp,br)
 a,b=old.build(beforep,key.removesuffix('.glb')),new.build(newp,key.removesuffix('.glb'))
 pd=dataclasses.asdict(newp);pd.pop('compound_clapboard_height_m');pd['confidence'].pop('compound_clapboard_height_m',None);assert pd==dataclasses.asdict(beforep),sid
 if sid!='cobweb_castle':assert a==b,sid
 else:
  for name in ['verts','faces','conf','mat_index']:assert b[name][:len(a[name])]==a[name],name
  for name in ['mats','named']:assert a[name]==b[name]
 master=FULL/'assets/gltf'/key;w=FULL/'assets/web'/key
 rows.append({'asset_key':key,'structure_id':sid,'phase':pid,'intentional_target':sid=='cobweb_castle','before_snapshot_sha256':digest(a),'after_snapshot_sha256':digest(b),'geometry_material_confidence_identical':a==b,'before_vertices':len(a['verts']),'after_vertices':len(b['verts']),'before_faces':len(a['faces']),'after_faces':len(b['faces']),'master_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'master_bytes':master.stat().st_size,'web_sha256':hashlib.sha256(w.read_bytes()).hexdigest(),'web_bytes':w.stat().st_size,'registry_row':row,'web_registry_row':web['masters'].get(key)})
assert len(rows)==82,len(rows)
versionrows={k:v for k,v in versions['assets'].items() if v.get('archetype')=='log_dwelling'};assert not versionrows,versionrows
receipt={'status':'ACTUAL_81_PREEXPORT_CONTROLS_IDENTICAL_TARGET_APPEND_ONLY','base':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO).decode().strip(),'total_defaults':len(manifest['assets']),'affected_defaults':len(rows),'affected_versions':len(versionrows),'unchanged_controls':sum(r['geometry_material_confidence_identical'] for r in rows),'old_positional_and_keyword_parameters_preserved':True,'blender_or_native_executed':False,'rows':rows}
(OUT/'82-FAMILY-CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='rows'}));print('TARGET',json.dumps(next({k:v for k,v in r.items() if k not in ['registry_row','web_registry_row']} for r in rows if r['intentional_target'])))
