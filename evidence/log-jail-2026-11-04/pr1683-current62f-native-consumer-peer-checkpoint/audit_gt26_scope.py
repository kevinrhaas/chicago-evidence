from pathlib import Path
import subprocess,json,hashlib,sys
P=Path(__file__).parent;Q=P/'gt26-final';W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';H='b797609f9924d39ff1df05d9abf37d02a62417f9';B='c9fe751aed817eb9390238703307902e9a8810e4';D=json.loads((P/'gt26-cache/READY.json').read_bytes())['tip'];read=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(W),*a])
assert git('rev-parse','HEAD').decode().strip()==H and git('rev-parse','MERGE_HEAD').decode().strip()==D
for n in ['OWNERS-REAPER.json','NATIVE-AUDIT-REAPER.json']:
 r=read(Q/n);assert r['command_exit']==0 and r['all_children_reaped']and not r['leftover_cleanup']
previous=read(P/'latest-dev-final/SCOPE-CARRY.json');assert previous['tested_head']=='3f3e0bfcc99aad5d358fa8520da764fbe0aa68ff'
# No nonmanifest actual runtime consumer changed since independently reviewed b797.
actual=read(P/'current-ui/desktop-body/PLAN.json');changes=[]
for path,r in actual['input_bindings'].items():
 if not path.startswith(str(A)+'/'):continue
 rel=Path(path).relative_to(A).as_posix();saved=subprocess.run(['git','-C',str(W),'show',H+':chicago/4d/'+rel],capture_output=True);after=Path(path).read_bytes()
 if saved.returncode:
  if rel=='data/pictures/1835.json':
   expected=read(P/'current-ui-phone-cards-v4/mobile-cards/PLAN.json')['expected_picture_rows'];current=json.loads(after)['by_structure'];assert all(current[k]==v for k,v in expected.items()),('actual targetpicture rows drift',rel)
  else:assert sha(after)==r['sha256'],('generated runtime consumer drift',rel)
 elif saved.stdout!=after:changes.append(rel)
assert set(changes)=={'assets/manifest.json','assets/manifest.web.json'},changes
for rel,key in [('assets/manifest.json','assets'),('assets/manifest.web.json','masters')]:
 old=json.loads(git('show',H+':chicago/4d/'+rel))[key];now=read(A/rel)[key]
 for name in ['log_jail__log_1833.glb','log_jail_keeper_house__frame_1835.glb']:assert old[name]==now[name]
shared={'assets/manifest.json','assets/manifest.web.json','data/liberties.json','docs/LIBERTIES.md','docs/STATUS.md','docs/measurements/source_use_coverage.md'};foreign=[]
for path in git('diff','--name-only',B,D).decode().splitlines():
 if Path(path).relative_to('chicago/4d').as_posix()in shared:continue
 blob=git('show',D+':'+path);assert(W/path).read_bytes()==blob,('foreignGT postimage',path);foreign.append({'path':path,'sha256':sha(blob)})
combined=read('/tmp/native-pr1684-final-review-20261104/COMBINED-CANDIDATE-AUDIT.json');assert combined['dev']==D and combined['pr_merged']and combined['default_family_count']==23 and combined['saug_producer_exact_currentdev']
for row in combined['files']:
 if row['label']=='candidate'and row['path']not in ['assets/manifest.json','assets/manifest.web.json']:assert sha((A/row['path']).read_bytes())==row['sha256'],('combinedforeign preserved',row['path'])
sys.path.insert(0,str(A/'generators'));import mesh_inputs
m=read(A/'assets/manifest.json')['assets'];rows=[]
for name,r in m.items():
 if r.get('archetype')!='frame_tavern':continue
 st=read(A/'data/structures'/(r['structure_id']+'.json'));ph=next(x for x in st['phases']if x['id']==r['phase_id']);digest=mesh_inputs.structure_inputs_sha(st,ph,r['archetype']);assert digest==r['inputs_sha256'],('actual23 recipe',name);rows.append({'asset':name,'actual_inputs_sha256':digest})
assert len(rows)==23 and m['green_tree_tavern__frame_1833.glb']['inputs_sha256']=='712cb7c9530c5c6d6fba6b83c7d2b6e2e19d49f78e94da7ebf688ee3937c6974'
(Q/'SCOPE-CARRY.json').write_text(json.dumps({'previous_qualified_head':H,'incoming_dev':D,'source_scope_parent_audit_sha256':sha((P/'latest-dev-final/SCOPE-CARRY.json').read_bytes()),'runtime_consumer_changes_since_b797':changes,'both_Jail_manifestrows_exact':True,'generated_picture_metadata':'Ignored generated globalpictures document was refreshed by current publisher and has a different whole-document hash than actual3f. Both Jail rows are independently value-exact to actualv4 captured expectedpicture rows including title/creator/archive/PD/URL. No whole-source or full-publication identity claim.','foreign_GreenTree_postimages_exact':foreign,'actual_current_frame_tavern23_recipes':rows,'Sauganash_currentproducer_and_full_versions_manifest_exact':True,'native_build_scope':'Preserves independently merged GreenTree combined candidate and published output bytes; no new bake executed or claimed. Coordinator authenticates original SDK separately.','all272_544_243_strictaudit_sha256':sha((Q/'native-audit/CURRENT-NATIVE-BINDINGS-PASS.json').read_bytes()),'runtime_carry':'Previous root/R reviewed b797 scope extends through GT-only data/manifests/docs; no Jail consumer/physicaloutput changes, and no new current runtime execution claim. New exacthead full8 required.','original_T2380':'partial/open; no match closure'},indent=2)+'\n');print('GT23 ACTUAL RECIPES + FOREIGNOUTPUTS + UNCHANGED JAILCONSUMER CARRY PASS',flush=True)
