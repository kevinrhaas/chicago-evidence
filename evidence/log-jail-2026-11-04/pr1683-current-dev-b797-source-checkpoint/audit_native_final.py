from pathlib import Path
import subprocess,json,sys,hashlib,time,os
P=Path(__file__).parent/'latest-dev-final/native-audit';P.mkdir(exist_ok=True);W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';sys.path.insert(0,str(A/'generators'));import mesh_inputs
sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(W),*a]);prior=Path('/tmp/jail-pr1683-native9af-pickup-20261104/jail272-current-input-fixture');expected=json.loads((prior/'ALL272-CURRENT-INPUTS.json').read_text())['rows'];native=json.loads((prior/'PRIOR272-OUTPUT-CODE-BINDINGS.json').read_text())['bindings'];m=json.loads((A/'assets/manifest.json').read_text())['assets'];out=[]
for e in expected:
 name=e['asset'];row=m[name];st=json.loads((A/'data/structures'/(row['structure_id']+'.json')).read_bytes());ph=next(p for p in st['phases']if p['id']==row['phase_id']);actual=mesh_inputs.structure_inputs_sha(st,ph,row['archetype']);assert actual==row['inputs_sha256']==e['actual_inputs_sha256'],('inputs',name)
 for family in ['gltf','web']:
  path='chicago/4d/assets/'+family+'/'+name;b=(W/path).read_bytes();oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert oid==native[path]['current9af'],('actualoutput',path)
 out.append({'asset':name,'actual_inputs_sha256':actual})
for path,binding in native.items():
 if '/assets/' not in path:assert git('hash-object','--',path).decode().strip()==binding['current9af'],('nativecode',path)
foreign=[];D='c9fe751aed817eb9390238703307902e9a8810e4'
for file,key in [('assets/manifest.json','assets'),('assets/manifest.web.json','masters')]:
 dev=json.loads(git('show',D+':chicago/4d/'+file));now=json.loads((A/file).read_bytes());assert set(now[key])==set(dev[key])|{'log_jail_keeper_house__frame_1835.glb'},file
 changes=[]
 for name,before in dev[key].items():
  after=now[key][name]
  if before!=after:
   assert key=='assets' and after['archetype']=='frame_dwelling' and name in {e['asset']for e in expected},('foreignrow',file,name)
   assert {k:v for k,v in before.items()if k!='inputs_sha256'}=={k:v for k,v in after.items()if k!='inputs_sha256'},('foreignmetadata',name)
   changes.append(name)
 assert len(changes)==(271 if key=='assets' else 0)
 foreign.append({'file':file,'all_outside_owned_native_family_exact_dev':True,'count':len(dev[key]),'existing271family_changes_only_genuine_native_qualified_inputs_hash':changes})
rows243=json.load(open('/tmp/first-fort-finish-1685-20261104/NATIVE243-CURRENT-INTEGRATION-EXACT.json'))['rows'];web243={r['file']:r for r in json.load(open('/tmp/first-fort-finish-1685-20261104/NATIVE243-WEB-CURRENT-EXACT.json'))['rows']};n=[]
for e in rows243:
 name=e['file'];row=m[name];st=json.loads((A/'data/structures'/(row['structure_id']+'.json')).read_bytes());ph=next(p for p in st['phases']if p['id']==row['phase_id']);actual=mesh_inputs.structure_inputs_sha(st,ph,row['archetype']);assert actual==row['inputs_sha256']==e['inputs_sha256'],('foreign243input',name);assert sha((A/'assets/gltf'/name).read_bytes())==e['master_sha256'];assert sha((A/'assets/web'/name).read_bytes())==web243[name]['sha256'];n.append({'asset':name,'inputs':actual})
assert len(out)==272 and len(n)==243
for name,expectedsha in [('gltf/log_jail_keeper_house__frame_1835.glb','431dc44f37bdcb2c7f705a5b17b65fe6a1cf748d077c337b699094c9b41752a8'),('web/log_jail_keeper_house__frame_1835.glb','15eb2fba')]:assert sha((A/'assets'/name).read_bytes()).startswith(expectedsha),(name,sha((A/'assets'/name).read_bytes()))
result={'current_head':git('rev-parse','HEAD').decode().strip(),'merged_dev':D,'all272_current_native_inputs_match':True,'all544_actual_outputs_match_genuine_native':True,'all9_native_geometry_code_paths_exact':True,'all243_current_dev_native_inputs_outputs_retained':True,'all_foreign_manifest_entries_exact':foreign,'rows272':out,'rows243':n,'keeper_master_sha256':sha((A/'assets/gltf/log_jail_keeper_house__frame_1835.glb').read_bytes()),'keeper_web_sha256':sha((A/'assets/web/log_jail_keeper_house__frame_1835.glb').read_bytes()),'core_master_sha256':sha((A/'assets/gltf/log_jail__log_1833.glb').read_bytes()),'qualification':'Exact genuine prior native reuse, no new Blender execution. Actual3f target runtime boundedqualified; later foreign integration requires scoped consumer proof and new exacthead whole8. OriginalpartialOPEN.'};(P/'CURRENT-NATIVE-BINDINGS-PASS.json').write_text(json.dumps(result,indent=2)+'\n');print('CURRENT272/544 + FOREIGN243 + FULL FOREIGN REGISTRY PASS',flush=True)
