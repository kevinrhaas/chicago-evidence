from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).parent;R=Path('/workspace/chicago-bridge-increment-20261102');D=R/'chicago/4d';base='0a14eb07bc6630ace4ce8bec12b87e9fa1a4b0d4';sha=lambda b:hashlib.sha256(b).hexdigest();old=lambda r:subprocess.check_output(['git','show',base+':chicago/4d/'+r],cwd=R)
allowed={'data/structures/lake_house_construction.json':'/function/note','data/research/newspapers/extracted/chicago_democrat_1835_06_10.json':'/claims/0/notes','data/sidecars/1835/lake_house_construction.json':'/attributes/function/note'};out={}
for rel,path in allowed.items():
 a=json.loads(old(rel));b=json.loads((D/rel).read_bytes());paths=[]
 def walk(a,b,p=''):
  if a==b:return
  if type(a)==type(b)==dict and a.keys()==b.keys():
   for k in a:walk(a[k],b[k],p+'/'+k)
  elif type(a)==type(b)==list and len(a)==len(b):
   for i,(x,y)in enumerate(zip(a,b)):walk(x,y,p+'/'+str(i))
  else:paths.append(p)
 walk(a,b);assert paths==[path],(rel,paths);out[rel]={'only_changed_json_pointer':path,'before_sha256':sha(old(rel)),'after_sha256':sha((D/rel).read_bytes())}
sys.path.insert(0,str(D/'generators'));import mesh_inputs;from archetypes import fort_structure_params
rel='data/structures/lake_house_construction.json';a=json.loads(old(rel));b=json.loads((D/rel).read_bytes());pa=fort_structure_params.from_phase(a['phases'][0],a);pb=fort_structure_params.from_phase(b['phases'][0],b);pa.validate();pb.validate();assert mesh_inputs._params_doc(pa)==mesh_inputs._params_doc(pb)
changes=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines();want={'chicago/4d/'+r for r in allowed}|{'chicago/4d/docs/STATUS.md','chicago/4d/docs/ROADMAP.md'};assert set(changes)==want,changes
for name in ['STATUS.md','ROADMAP.md']:assert (D/'docs'/name).read_bytes().endswith(old('docs/'+name))
for rel in ['data/structures/lake_house_construction.json','data/research/newspapers/extracted/chicago_democrat_1835_06_10.json']:assert (D/rel).read_bytes()==(P/'candidate'/rel).read_bytes()
result={'base':base,'changes':out,'scope':'exact2approvednotes+officialsidecar+rawhistorySTATUS/ROADMAP+newT2379changelog','resolved_params_properties_confidence_exact':True,'all_other_tracked_blobs_exact_base':True,'geometry_recipes_native_outputs_renderer_and_prior1694_preserved':True,'native_generation':False,'new_browser_execution':False,'full_source_gate':'PENDING_CURRENT_HOSTED8; local sparse source owners/params only, not a full gate','historical_red':'Initial sparse params run RED only because excluded texture profiles JSON; exact current18025byte profiles restored, distinct rerun recorded.'};(P/'SOURCE-SCOPE-AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print('SOURCE-SCOPE PASS',len(changes),'modified tracked paths plus new changelog')
