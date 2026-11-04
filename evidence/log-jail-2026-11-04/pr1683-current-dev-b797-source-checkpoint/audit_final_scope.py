from pathlib import Path
import subprocess,json,hashlib,sys
P=Path(__file__).parent;Q=P/'latest-dev-final';W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';H='3f3e0bfcc99aad5d358fa8520da764fbe0aa68ff';D=json.loads((Q/'cache/READY.json').read_bytes())['tip'];B='5673cb959526cd6080c7ecfceb039fcb1b2c5e73';sha=lambda b:hashlib.sha256(b).hexdigest();read=lambda p:json.loads(Path(p).read_bytes());git=lambda *a:subprocess.check_output(['git','-C',str(W),*a]);old=lambda path:git('show',H+':chicago/4d/'+path)
assert read(P/'FINAL-RUNTIME-LEDGER-REAPER.json')['command_exit']==0
assert read(Q/'OWNERS-REAPER.json')['command_exit']==0 and read(Q/'NATIVE-AUDIT-REAPER.json')['command_exit']==0
assert git('rev-parse','HEAD').decode().strip()==H and git('rev-parse','MERGE_HEAD').decode().strip()==D
plan=read(P/'current-ui/desktop-body/PLAN.json');changed=[]
for path,row in plan['input_bindings'].items():
 actual=sha(Path(path).read_bytes())
 if actual!=row['sha256']:changed.append({'path':str(Path(path).relative_to(A)),'old':row['sha256'],'current':actual})
assert {r['path']for r in changed}=={'assets/manifest.json','assets/manifest.web.json','renderers/web/js/buildings.js','renderers/web/js/fort-gates.js','renderers/web/js/changelog.js'},changed
for file,key in [('assets/manifest.json','assets'),('assets/manifest.web.json','masters')]:
 before=json.loads(old(file))[key];after=read(A/file)[key]
 for asset in ['log_jail__log_1833.glb','log_jail_keeper_house__frame_1835.glb']:assert before[asset]==after[asset],('target manifest',file,asset)
rplan=read('/tmp/fort-parade-recovery-20261104/runtime/PLAN.json');rruntime=read('/tmp/fort-parade-recovery-20261104/runtime/FINAL-CLOSURE.json');assert rruntime['status']=='FINAL_FIRST_FORT_PARADE_CARDS_NATIVE3_BOTH_CLOSED_PASS'and rruntime['head']==rplan['expected_head']
qualified_renderer=[]
for rel in ['renderers/web/js/buildings.js','renderers/web/js/fort-gates.js']:
 bindings=[b for n,b in rplan['input_bindings'].items()if n.endswith('/chicago/4d/'+rel)];assert len(bindings)==1 and bindings[0]['sha256']==sha((A/rel).read_bytes()),('independent renderer qualification',rel);qualified_renderer.append({'path':rel,'actual_byte_exact_independent_R_runtime':rruntime['head'],'sha256':bindings[0]['sha256']})
# Exact changed native parade path is selected solely by two explicit IDs; Jail never enters it.
fg=(A/'renderers/web/js/fort-gates.js').read_text();mapping=fg.split('export const PARADE_GROUNDS = Object.freeze({',1)[1].split('});',1)[0];assert 'first_fort_dearborn_parade:'in mapping and 'fort_dearborn_parade:'in mapping and 'jail'not in mapping
# Both actual Jail doorstep records remain exact despite foreign town entrance additions.
rel='data/enclosures/town_entrance_aprons.json';o=json.loads(old(rel));n=read(A/rel);targets={'log_jail','log_jail_keeper_house'};assert [x for x in o['entrances']if x['structure_id']in targets]==[x for x in n['entrances']if x['structure_id']in targets]
# Every incoming file is preserved byte-exact except deterministic shared aggregates and append-only/shared prose.
shared={'assets/manifest.json','assets/manifest.web.json','data/enclosures/town_entrance_aprons.json','data/liberties.json','data/reconstruction/name_pool_keys.json','data/sidecars/1835/sources/index.json','docs/LIBERTIES.md','docs/ROADMAP.md','docs/STATUS.md','docs/measurements/source_use_coverage.md'}
foreign=[]
for path in git('diff','--name-only',B,D).decode().splitlines():
 rel=str(Path(path).relative_to('chicago/4d'))
 if rel in shared:continue
 expected=subprocess.run(['git','-C',str(W),'show',D+':'+path],capture_output=True)
 if expected.returncode:assert not(W/path).exists(),('foreign deleted path',path)
 else:assert(W/path).read_bytes()==expected.stdout,('foreign postimage',path)
 foreign.append({'path':path,'sha256':sha(expected.stdout)if expected.returncode==0 else None})
# New independently native-qualified25-family recipes remain actual-owner exact, never restamped.
sys.path.insert(0,str(A/'generators'));import mesh_inputs
producer=read('/tmp/native-pr1687-final-review-20261104/PINNED-52D-SOURCE-GUARDS.json');assert producer['immutable_head']=='52d6f631df788258a50a6e3271cca9e97ba960ac'
for row in producer['files']:assert sha((A/row['path']).read_bytes())==row['sha256'],('newforeign producer',row['path'])
recipe=read('/tmp/native-pr1687-final-review-20261104/RECIPE-REUSE-135-TO-652.json');assert recipe['reuse_condition_pass']and recipe['exact25_manifest_rows'];m=read(A/'assets/manifest.json')['assets'];native25=[]
for asset in recipe['native_family_roster']:
 row=m[asset];st=read(A/'data/structures'/(row['structure_id']+'.json'));phase=next(x for x in st['phases']if x['id']==row['phase_id']);actual=mesh_inputs.structure_inputs_sha(st,phase,row['archetype']);assert actual==row['inputs_sha256'],('foreign25 actualrecipe',asset);native25.append({'asset':asset,'actual_inputs_sha256':actual})
result={'tested_head':H,'incoming_dev':D,'all_actual_target_consumer_bindings_unchanged_except_five_classified':True,'changed_bindings':changed,'bothJail_manifestrows_value_exact':True,'both_actualJail_doorsteprecords_exact':True,'independently_runtime_qualified_renderer':qualified_renderer,'parade_scope':'Only two explicitly named parade IDs; original material-name WeakMap semantics unchanged for nonparades. Jail enters neither named parade branch. No new current runtime execution claim.','foreign_postimages_exact':foreign,'shared_aggregate_resolution':'Fresh actual liberties/scene-all/source-use/derivatives/validate-all owners; normal Git disjoint merge retains authored prose and generated owned Jail records. Native audit independently retains allforeign manifests except genuine priorqualified FrameDW inputs only.','native25_actual_current_recipes':native25,'native25_producer_sha256':sha(Path('/tmp/native-pr1687-final-review-20261104/PINNED-52D-SOURCE-GUARDS.json').read_bytes()),'actual_Jail272_544_and_outbuilding243_audit':sha((Q/'native-audit/CURRENT-NATIVE-BINDINGS-PASS.json').read_bytes()),'runtime_carry':'Root-approved scoped carry of six actual3f executions plus independent newparade/Cobweb/cupola qualification. New mergedsource whole8 still required. NOT rerun or rebinding of past execution.','original_T2380':'partial/open; records UNREVIEWED/DIFFERS; genericgable material, camera/wholecompound discrepancy retained'}
(Q/'SCOPE-CARRY.json').write_text(json.dumps(result,indent=2)+'\n');print('CURRENT TARGET CONSUMERS + FOREIGN POSTIMAGES + ACTUAL25/272/243 RECIPE SCOPE PASS',flush=True)
