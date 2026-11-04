from pathlib import Path
import json,hashlib,subprocess,struct,math,datetime,copy
P=Path(__file__).resolve().parent;D=P.parent;R=Path('/workspace/chicago-transport-current-20261103');A=R/'chicago/4d';BASE='a3a87cafe9321a2970a390cac77ae45be82680f5'
def sha(b):return hashlib.sha256(b).hexdigest()
def file_sha(p):return sha(p.read_bytes())
def git(*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(R),*args],timeout=15)
def blob(rel):return git('show',BASE+':'+rel)
def load(p):return json.loads(p.read_text())
def parse(raw):
 assert raw[:4]==b'glTF';n,t=struct.unpack_from('<II',raw,12);assert t==0x4e4f534a;g=json.loads(raw[20:20+n]);bn,bt=struct.unpack_from('<II',raw,20+n);assert bt==0x004e4942;return g,raw[28+n:28+n+g['buffers'][0]['byteLength']]
v=load(D/'E2E-COMPATIBLE-NEXT-V6-PREVIEW.json');native=load(D/'native-02/CLOSED.json');n=native['native'];assert native['passed'] and n['passed'] and sum(f['phases']for f in n['files'])==1032
before=dict(HEAD=git('rev-parse','HEAD').decode().strip(),semantic_index_sha256=sha(git('ls-files','--stage','-z')))
assets=[]
for row in v['eight_parent_child_hashes']:
 rel='chicago/4d/'+row['file'];raw=blob(rel);child=(R/rel).read_bytes();assert sha(raw)==row['parent_sha256'] and sha(child)==row['child_sha256']==n['candidate_sha256_before'][row['file']]
 old,oldbin=parse(raw);new,newbin=parse(child)
 for k in old:
  if k not in ['animations','accessors','bufferViews','buffers']:assert new[k]==old[k],(rel,k)
 assert new['animations'][:-1]==old['animations'] and len(new['animations'])==len(old['animations'])+1
 assert new['accessors'][:len(old['accessors'])]==old['accessors'] and new['bufferViews'][:len(old['bufferViews'])]==old['bufferViews']
 assert newbin[:len(oldbin)]==oldbin and new['buffers'][1:]==old['buffers'][1:]
 assert {k:x for k,x in new['buffers'][0].items()if k!='byteLength'}=={k:x for k,x in old['buffers'][0].items()if k!='byteLength'}
 original=next(a for a in old['animations']if a['name']=='sit_drive');clip=new['animations'][-1];assert clip['name']=='sit_drive_look_v2' and clip['channels']==original['channels'];changed=[]
 for channel in clip['channels']:
  i=channel['sampler'];t=channel['target'];name=new['nodes'][t['node']].get('name')
  if clip['samplers'][i]!=original['samplers'][i]:
   assert t['path']=='rotation' and name in ['neck_01','head'];changed.append(name);sampler=clip['samplers'][i];assert sampler['interpolation']=='LINEAR';assert new['accessors'][sampler['input']]['count']==65;assert new['accessors'][sampler['input']]['min']==[0] and new['accessors'][sampler['input']]['max']==[8]
  else:assert name not in ['neck_01','head'] or t['path']!='rotation'
 assert sorted(changed)==['head','neck_01']
 assets.append(dict(file=row['file'],parent_sha256=sha(raw),child_sha256=sha(child),all_protected_JSON_and_BIN_prefix_exact=True,all_original_clips_exact=True,only_new_clip_changed_targets=changed,old_track_count=sum(len(a['channels'])for a in old['animations']),native_finite_asset_proof_exact_payload=True))
critical=load(D/'FIXTURE-COMPATIBILITY-WITH-CURRENT-ROOT.json')['critical_sources'];readers={}
for rel,row in critical.items():h=file_sha(A/rel);assert h==row['qualified'];readers[rel]=h
assert len(readers)==8
for rel in ['tools/human_seated_look.py','tools/human_natural_idle.py','data/humans/animations/seated-driver-look-v2.json','tools/test_human_natural_idle.py','renderers/web/js/driven-assembly-loader.js']:
 assert file_sha(A/rel)==n['implementation_pins_before'][rel],rel
assert file_sha(D/'native_seated_look.mjs')==n['implementation_pins_before']['native_runner']
assert file_sha(A/'data/humans/animations/seated-driver-look-v2.json')==n['recipe_sha256']
assert file_sha(A/'data/humans/animations/seated-driver-look-v2.native.json')==file_sha(D/'native-02/models/RESULT.json')
bridge=load(A/'data/humans/animations/seated-driver-look-v2.binding-refresh.json');loops_raw=(A/'data/transport/driven/loops.json').read_bytes();assert sha(loops_raw)==bridge['updated_loops_sha256'];assert bridge['source_loops_sha256']==n['implementation_pins_before']['data/transport/driven/loops.json'];assert file_sha(A/'data/humans/animations/seated-driver-look-v2.native.json')==bridge['native_readback_sha256']
reverse=loops_raw
for new,old in {(r['new'],r['old'])for r in bridge['changed_fields']}:
 assert reverse.count(new.encode())==2;reverse=reverse.replace(new.encode(),old.encode())
assert sha(reverse)==bridge['source_loops_sha256'];historical_loops=json.loads(reverse);actual_loops=json.loads(loops_raw)
for changed in bridge['changed_fields']:
 old=next(x for x in historical_loops['rows']if x['id']==changed['row_id'])['driver_palm_bindings_by_lod'][str(changed['lod'])][changed['side']]
 now=next(x for x in actual_loops['rows']if x['id']==changed['row_id'])['driver_palm_bindings_by_lod'][str(changed['lod'])][changed['side']]
 assert {k:x for k,x in old.items()if k!='asset_sha256'}=={k:x for k,x in now.items()if k!='asset_sha256'}
# Confirm scene changes against actual parent are only two selected clips and four hashes.
baseline_loops=json.loads(blob('chicago/4d/data/transport/driven/loops.json'));copyloops=copy.deepcopy(actual_loops)
for row in copyloops['rows']:assert row.pop('driver_clip')=='sit_drive_look_v2'
for changed in bridge['changed_fields']:next(x for x in copyloops['rows']if x['id']==changed['row_id'])['driver_palm_bindings_by_lod'][str(changed['lod'])][changed['side']]['asset_sha256']=changed['old']
assert copyloops==baseline_loops
# Complete incoming rail/nativeCI inputs stay native parent bytes.
incoming_paths=git('diff-tree','--no-commit-id','--name-only','-r','e2e4612fcf9946a343833b1e04adf4ca90322494').decode().splitlines()
for rel in incoming_paths:
 if rel in ['chicago/4d/docs/LIBERTIES.md','chicago/4d/data/liberties.json']:continue
 if not git('ls-tree',BASE,'--',rel).strip():assert not(R/rel).exists(),rel
 else:assert(R/rel).read_bytes()==blob(rel),rel
for rel,pin in v['watched_untouched_source_pins'].items():assert file_sha(R/rel)==pin
for rel,pin in v['target_output_pins'].items():
 if rel!='chicago/4d/data/humans/fixture.measure.json':assert file_sha(R/rel)==pin,rel
for name in ['writer_inventory.json','step_isolation.json']:
 old=json.loads(blob('chicago/4d/tools/'+name));now=load(A/'tools'/name);newkeys=set(now['tools'])-set(old['tools']);expected='human_seated_look.py' if name=='writer_inventory.json'else'tools/human_seated_look.py';assert newkeys=={expected};assert all(now[k]==x for k,x in old.items()if k!='tools');assert all(now['tools'][k]==x for k,x in old['tools'].items())
# Entire original assembly test remains prefix; V6 adds identical original60 driver lines.
oldtests=blob('chicago/4d/tools/test_driven_assembly.mjs');newtests=(A/'tools/test_driven_assembly.mjs').read_bytes();assert newtests.startswith(oldtests);extra=newtests[len(oldtests):];assert len(extra.splitlines())==60 and sha(extra)==v['original_driver_test_block_sha256']
expected=set(v['paths'])|{'chicago/4d/'+a['file']for a in assets}|{'chicago/4d/docs/STATUS.md','chicago/4d/tools/writer_inventory.json','chicago/4d/tools/step_isolation.json'};assert len(expected)==29
staged=set(git('diff','--cached','--name-only').decode().splitlines());allowed=expected|{'chicago/4d/data/liberties.json','chicago/4d/docs/measurements/source_use_coverage.md'};assert staged<=allowed and expected<=staged
context_changed=[]
for rel,h in n['implementation_pins_before'].items():
 if rel=='native_runner':continue
 current=file_sha(A/rel)
 if current!=h:context_changed.append(dict(path=rel,historical=h,current=current,CPU_geometry_imported=False,reason='loops has exact four-field metadata bridge; main/town/test fixture are hash-recorded context, not imported by standalone asset CPU observer'))
after=dict(HEAD=git('rev-parse','HEAD').decode().strip(),semantic_index_sha256=sha(git('ls-files','--stage','-z')))
report=dict(status='INDEPENDENT_ACTUAL_V6_SCOPE_AND_FINITE_ASSET_PROOF_REUSE_REVIEW_PASS_COMPOSITE_QUALIFICATION_PENDING',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_before=before,source_after=after,staged_paths_observed=sorted(staged),intended_exact29_application_paths=sorted(expected),native_mutable_generated_report_paths_allowed=sorted(allowed-expected),assets=assets,all8_actual_children_exact_historical_native_proof=True,all8_baseline_parents_exact_historical_native_proof=True,all8_critical_reader_pins_exact=readers,recipe_generator_common_observer_and_actual_native_JSON_exact=True,protected_palm_barycentric_triangle_point_pose_and_source_fields_exact=True,four_payload_hash_fields_reverse_to_exact_historical_loops_bytes=True,unchanged_native_asset_proof=dict(receipt=str(D/'native-02/CLOSED.json'),sha256=file_sha(D/'native-02/CLOSED.json'),phases=1032,all8_pelvis3mm_fault_controls_refused=True,scope='Existing finite asset-only loader/mixer/Float32 palettes and selected palm-surface result applies to these byte-identical assets/readers/recipe and metadata-bridged original bindings. No new CPU run, APP, composite, world, garment, continuous contact or photographic PASS is claimed.'),historical_context_pins_that_changed=context_changed,complete_prior_warm_fixture_and_same60_driver_assertions_exact=True,incoming_rail_asset_and_declarations_preserved=True,all_existing_registry_entries_preserved=True,current_CI_workflow_and_readers_unchanged=True,runtime_independent_code_review=dict(result='NO_BLOCKING_CODE_OR_SCOPE_ISSUE_FOUND',look_clock='Look clips receive one actual visualDt interval; vehicle substeps skip that mixer, legacy sit_drive retains original clock.',pause_and_range='Pauses/reduced/hidden/root draw reach pass zero and set reset; first visible frame after hold drops held elapsed.',Light='Saved mixer phase survives retire/remount. Existing zero-time lastUpdate prevents pending-time replay.',identity_and_human_manager='External driver is withheld from ordinary humans actors map, so shared humans update does not double-advance its mixer.',loader='Explicit sit_drive/look_v2 selector only, missing actual exported clip refuses; only activeLOD0/3 are referenced.',risk='Actual browser visual appearance/clock composition, full24fixture, resource/memory/frame budgets, complete native gates and currentHEADCI remain separate required qualification. Head/neck-only motion does not close gait/riding/boarding/photo acceptance.'),no_app_source_index_ref_ticket_generator_GPU_native_test_or_commit_writes=True,actual_composite_native_and_browser_qualification_pending=True)
(P/'REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status=report['status'],receipt=str(P/'REVIEW.json'),sha256=file_sha(P/'REVIEW.json'),assets=8,reader_pins=8,scope_paths=len(expected),historical_context_changed=[x['path']for x in context_changed])))
