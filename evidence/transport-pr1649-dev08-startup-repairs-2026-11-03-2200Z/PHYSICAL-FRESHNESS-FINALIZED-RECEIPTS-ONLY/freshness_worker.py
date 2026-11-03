from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
app=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(app/'tools'))
import bake_warranted
assert bake_warranted.ROOT.resolve()==app
stale,note,count=bake_warranted.freshness()
import validate,mesh_inputs,terrain_inputs,code_inputs
assert all(m.ROOT.resolve()==app for m in [validate,mesh_inputs,terrain_inputs,code_inputs])
manifest=json.loads((app/'assets/manifest.json').read_text())
masters={name:{'bytes':(app/'assets/gltf'/name).stat().st_size,'is_file':(app/'assets/gltf'/name).is_file()} for name in manifest['assets']}
assert count==1034 and not stale and all(x['is_file'] and x['bytes']>0 for x in masters.values())
result={'native_call':'UNMODIFIED bake_warranted.freshness -> validate.run_stale_check','asset_count':count,'stale':stale,'note':note,'module_ROOTS':{m.__name__:str(m.ROOT) for m in [bake_warranted,validate,mesh_inputs,terrain_inputs,code_inputs]},'actual_physical_master_outputs':masters,'all1034_actual_physical_master_outputs':True,'sandbox_has_git':(app.parent.parent/'.git').exists()}
Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'asset_count':count,'stale':stale,'note':note,'actual_master_count':len(masters),'all_module_roots_are_sandbox':True}),flush=True)
