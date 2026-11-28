"""Keep the measured source identity while inspecting ordinary upstream changes."""
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
W=Path('/workspace/work')
from vegetation_roughness_channel_fix_lap_proof import qualify as qualify_lap
def qualify(proof):
 r=Path(proof['repo']);a=proof['native_candidate_tree'];b=proof['final_tree']
 def raw(*args):return subprocess.check_output(['git',*args],cwd=r)
 assert qualify_lap(proof)['complete']
 changed=raw('diff','--name-only',a,b).decode().splitlines()
 release_ui={'chicago/4d/renderers/web/css/walk.css','chicago/4d/renderers/web/js/changelog.js','chicago/4d/renderers/web/js/whatsnew.js','chicago/4d/renderers/web/js/strings/whatsnew.js','chicago/4d/renderers/web/js/strings/es/sections.js'}
 upstream='445b43c924dbe4594a88244bb23633829aa3a6e3';previous='a54aeaf9ae1e0e564f05f9a83af723f40dbab83b'
 assert proof['actual_dev']==upstream
 upstream_ui={p for p in raw('diff','--name-only',previous,upstream).decode().splitlines() if p.startswith('chicago/4d/renderers/web/')}
 frontend={p for p in changed if p.startswith('chicago/4d/renderers/web/')}
 assert frontend<=release_ui|upstream_ui,frontend
 main='chicago/4d/renderers/web/js/main.js'
 for path in frontend-{main}:assert raw('show',b+':'+path)==raw('show',upstream+':'+path),path
 boot_patch=raw('diff','--binary',previous,upstream,'--',main)
 # The entire reviewed upstream main.js change is imports plus guarded boot
 # setup, before the scene starts. Reversing only that exact immutable patch
 # must recover every byte of the qualified tree renderer's main module.
 with tempfile.TemporaryDirectory(prefix='vegetation-d2b-main-inputs-',dir=W) as d:
  env={**os.environ,'GIT_INDEX_FILE':d+'/index'}
  subprocess.run(['git','read-tree',b],cwd=r,env=env,check=True)
  subprocess.run(['git','apply','--cached','--reverse'],cwd=r,env=env,input=boot_patch,check=True)
  recovered=subprocess.check_output(['git','write-tree'],cwd=r,env=env).decode().strip()
  assert raw('show',recovered+':'+main)==raw('show',a+':'+main)
 guard_code="""import {gateMode} from './renderers/web/js/sign-in.js';import {SIGN_IN} from './renderers/web/js/sign-in-config.js';import {cloudSaveFor} from './renderers/web/js/cloud-save.js';import {classesFor} from './renderers/web/js/classes.js';let d={localhost:gateMode({config:SIGN_IN,hostname:'localhost',webdriver:true}),loopback:gateMode({config:SIGN_IN,hostname:'127.0.0.1',webdriver:true}),cloudSave:cloudSaveFor(undefined,SIGN_IN),classes:classesFor(undefined,SIGN_IN)};if(!['off','robot'].includes(d.localhost)||!['off','robot'].includes(d.loopback)||d.cloudSave||d.classes)throw Error('Anonymous benchmark now enters cloud features');console.log(JSON.stringify(d));"""
 guards=json.loads(subprocess.check_output([str(W/'node22/bin/node'),'--input-type=module','-e',guard_code],cwd=r/'chicago/4d',text=True))

 allowed_data={
  'chicago/4d/data/back_yards/1904.json','chicago/4d/data/components/prairie_1904/draft_prairie_1904.json',
  'chicago/4d/data/front_yards/1904.json','chicago/4d/data/humans/doors_1904.json','chicago/4d/data/jaunts/prairie-built-so-far.json','chicago/4d/data/liberties.json',
  'chicago/4d/data/reference_views/tucker_smith_house_2140_prairie/chicagology_2140_a.json',
  'chicago/4d/data/reference_views/tucker_smith_house_2140_prairie/chicagology_2140_a.match.json',
  'chicago/4d/data/reference_views/tucker_smith_house_2140_prairie/glessner_2140_vanosdel.json',
  'chicago/4d/data/reference_views/tucker_smith_house_2140_prairie/glessner_2140_vanosdel.match.json',
  'chicago/4d/data/sidecars/1835/sources/index.json','chicago/4d/data/sidecars/1835/sources/jyoti_blog_2009_cullerton_rowhouses.json',
  'chicago/4d/data/sidecars/1835/sources/sanborn_1911_chicago_v3_sheet_35.json',
  'chicago/4d/data/sidecars/1904/house_213_e20th.json','chicago/4d/data/sidecars/1904/house_215_e20th.json','chicago/4d/data/sidecars/1904/house_217_e20th.json',
  'chicago/4d/data/sidecars/1904/index.json','chicago/4d/data/sidecars/1904/jaunts/prairie-built-so-far.json',
  'chicago/4d/data/sidecars/1904/tucker_smith_house_2140_prairie.json','chicago/4d/data/sources/jyoti_blog_2009_cullerton_rowhouses.json',
  'chicago/4d/data/street_section/walk_joins_1904.json','chicago/4d/data/structures/house_213_e20th.json',
  'chicago/4d/data/structures/house_215_e20th.json','chicago/4d/data/structures/tucker_smith_house_2140_prairie.json'}
 assert {p for p in changed if p.startswith('chicago/4d/data/')}<=allowed_data
 houses={'house_213_e20th','house_215_e20th','tucker_smith_house_2140_prairie'}
 registry=[]
 for path,key in [('chicago/4d/assets/manifest.json','assets'),('chicago/4d/assets/manifest.web.json','masters')]:
  x,y=[json.loads(raw('show',ref+':'+path)) for ref in (a,b)]
  keep=lambda k:not any(h in k for h in houses)
  assert {k:v for k,v in x[key].items() if keep(k)}=={k:v for k,v in y[key].items() if keep(k)},path
  assert {k:v for k,v in x.items() if k!=key}=={k:v for k,v in y.items() if k!=key},path
  registry.append({'path':path,'all_default1835_and_other_asset_entries_unchanged':True})
 for path in changed:
  if path.startswith(('chicago/4d/assets/gltf/','chicago/4d/assets/web/')):assert any(h in path for h in houses),path
 helpers=[]
 for path in ['chicago/4d/tools/measure_still_frame.mjs','chicago/4d/tools/still_frame_ceilings.json']:
  x,y=[raw('show',ref+':'+path) for ref in (a,b)];assert x==y,path
  helpers.append({'path':path,'sha256':hashlib.sha256(x).hexdigest()})
 return {'complete':True,'measured_source_tree':a,'current_integrated_tree':b,
  'all_default1835_geometry_material_shader_frame_loop_and_benchmark_bytes_unchanged':True,'main_boot_only_patch_sha256':hashlib.sha256(boot_patch).hexdigest(),'anonymous_benchmark_guards':guards,
  'all_frontend_code_html_css_identical_except_release_literals':not bool(frontend-{'chicago/4d/renderers/web/js/changelog.js'}),
  'inspected_upstream_release_panel_paths':sorted(frontend),'upstream_ui_exception':'The exact445 cloud-save, classroom and launch UI changes are preserved. main.js changes only imports and pre-scene boot setup; reversing that exact immutable upstream patch recovers the complete qualified renderer module. Anonymous localhost/robot benchmark guards keep cloud save and classes inactive. Other scene renderer, shader, geometry and benchmark code remains byte-identical.',
  'asset_registries':registry,'benchmark':helpers,'inspected_upstream_data_paths':sorted(set(changed)&allowed_data),
  'citation_metadata_exception':'The changed1835/sources files are the global catalogue and1904 building citation backlinks; no1835 geometry or material record changed. Liberties and the pending release note are metadata.',
  'new_source_timing_execution_claimed':False,
  'scope':'The full corrected6b working-source benchmark retains its actual source and CPU identity. The ordinary Dev integration carries inspected1904 houses, the release panel and guarded cloud-save/classroom/launch UI. Fresh current-head CI separately measures the complete stock grid and all published browser sections; no older-source pass replaces it.'}
