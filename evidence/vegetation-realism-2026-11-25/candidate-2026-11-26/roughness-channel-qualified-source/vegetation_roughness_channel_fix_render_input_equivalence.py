"""Keep the measured source identity while inspecting ordinary upstream changes."""
import hashlib,json,subprocess
from pathlib import Path
from vegetation_roughness_channel_fix_lap_proof import qualify as qualify_lap
def qualify(proof):
 r=Path(proof['repo']);a=proof['native_candidate_tree'];b=proof['final_tree']
 def raw(*args):return subprocess.check_output(['git',*args],cwd=r)
 assert qualify_lap(proof)['complete']
 changed=raw('diff','--name-only',a,b).decode().splitlines()
 release_ui={'chicago/4d/renderers/web/css/walk.css','chicago/4d/renderers/web/js/changelog.js','chicago/4d/renderers/web/js/whatsnew.js','chicago/4d/renderers/web/js/strings/whatsnew.js','chicago/4d/renderers/web/js/strings/es/sections.js'}
 frontend={p for p in changed if p.startswith('chicago/4d/renderers/web/')}
 assert frontend<=release_ui,frontend
 for path in frontend:assert raw('show',b+':'+path)==raw('show',proof['actual_dev']+':'+path),path
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
  'all_default1835_geometry_materials_scene_renderer_and_benchmark_bytes_unchanged':True,
  'all_frontend_code_html_css_identical_except_release_literals':not bool(frontend-{'chicago/4d/renderers/web/js/changelog.js'}),
  'inspected_upstream_release_panel_paths':sorted(frontend),'release_panel_exception':'T3813 changes only the unopened What\'s New panel, its own strings and wn-prefixed CSS. Its exact upstream bytes are preserved. No scene renderer, shader, material or benchmark code differs.',
  'asset_registries':registry,'benchmark':helpers,'inspected_upstream_data_paths':sorted(set(changed)&allowed_data),
  'citation_metadata_exception':'The changed1835/sources files are the global catalogue and1904 building citation backlinks; no1835 geometry or material record changed. Liberties and the pending release note are metadata.',
  'new_source_timing_execution_claimed':False,
  'scope':'The full corrected6b working-source benchmark retains its actual source and CPU identity. The ordinary Dev integration carries inspected1904 houses, their metadata and the unopened release-panel update. Fresh current-head CI separately measures the complete stock grid and all published browser sections; no older-source pass replaces it.'}
