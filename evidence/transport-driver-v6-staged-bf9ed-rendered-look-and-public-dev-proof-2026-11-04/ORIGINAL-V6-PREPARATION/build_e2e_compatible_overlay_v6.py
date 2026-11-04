"""Prepare a620 driver proposal using immutable Git blobs and external text scratch.

Never modifies ROOT checkout/index or generates assets or qualification results.
"""
from pathlib import Path
import datetime,difflib,hashlib,json,subprocess,tempfile
P=Path(__file__).resolve().parent
R=Path('/workspace/chicago-transport-current-20261103')
OLD='a6207b493f7ce06052e9e211245631a1e07f8df1'
HEAD='e2e4612fcf9946a343833b1e04adf4ca90322494'
DEV='e2e4612fcf9946a343833b1e04adf4ca90322494'
PREFIX='E2E-COMPATIBLE-NEXT-V6'
LIB='chicago/4d/docs/LIBERTIES.md'
CHECK='chicago/4d/tools/check.sh'
TEST='chicago/4d/tools/test_driven_assembly.mjs'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text())
def blob(c,p,optional=False):
 q=subprocess.run(['git','--no-optional-locks','-C',str(R),'show',c+':'+p],capture_output=True,timeout=8)
 if optional and q.returncode==128 and (b'does not exist' in q.stderr or b'but not in' in q.stderr): return None
 assert q.returncode==0,(p,q.stderr.decode(errors='replace'))
 return q.stdout
def put(root,p,b):
 if b is not None:
  f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
def get(root,p): return (root/p).read_bytes() if (root/p).exists() else None
def apply(root,patch,*args):
 q=subprocess.run(['git','apply',*args,str(patch)],cwd=root,capture_output=True,timeout=8)
 assert q.returncode==0,q.stderr.decode(errors='replace')
def main():
 prior=P/'NEXT-INCREMENT-INTEGRATION-PREPARED-A620-V5.json'
 prior_raw=prior.read_bytes();prior_doc=load(prior)
 for name,h in prior_doc['files'].items(): assert sha((P/name).read_bytes())==h
 previous=load(P/'A620-COMPATIBLE-NEXT-V5-PREVIEW.json')
 previous_profile=load(P/'A620-COMPATIBLE-NEXT-V5-PROFILE.json')
 previous_patch=P/'A620-COMPATIBLE-NEXT-V5-18-PATH.patch'
 paths=previous['paths']
 old={p:blob(OLD,p,True) for p in paths}
 source={p:blob(HEAD,p,True) for p in paths}
 assert {p:sha(b) if b is not None else None for p,b in old.items()}==previous['target_file_pins']
 changed=[p for p in paths if old[p]!=source[p]]
 assert changed==[LIB],changed
 with tempfile.TemporaryDirectory(prefix='driver-e2e-v6-text-',dir=P) as scratch:
  scratch=Path(scratch);before=scratch/'old';after=scratch/'current';before.mkdir();after.mkdir()
  for p in paths: put(before,p,old[p]);put(after,p,source[p])
  apply(before,previous_patch)
  old_outputs={p:get(before,p) for p in paths}
  assert {p:sha(b) for p,b in old_outputs.items()}==previous['target_output_pins']
  outputs={p:old_outputs[p] for p in paths}
  apply(after,previous_patch,'--include='+CHECK,'--include='+LIB)
  outputs[CHECK]=get(after,CHECK);outputs[LIB]=get(after,LIB)
  apply(after,previous_patch,'--reverse','--include='+CHECK,'--include='+LIB)
  assert get(after,CHECK)==source[CHECK] and get(after,LIB)==source[LIB]
  driver_tests=old_outputs[TEST][len(old[TEST]):]
  assert len(driver_tests.splitlines())==60 and outputs[TEST].startswith(source[TEST])
  assert outputs[TEST][len(source[TEST]):]==driver_tests
  assert b"eligible driver prepares the exact Navigator app code" in source[TEST]
  assert b"navigatorUi?.preload?.('inspect') ?? import('./apps/inspect-view.js')" in source['chicago/4d/renderers/web/js/main.js']
  incoming_check=blob(HEAD,CHECK).split(b'# T-3353.',1)[1].split(b'# T-3242.',1)[0]
  assert incoming_check in outputs[CHECK]
  parts=[]
  for p in paths:
   pre,post=source[p],outputs[p]
   parts.append(f'diff --git a/{p} b/{p}\n')
   if pre is None: parts.append('new file mode 100644\n')
   parts.extend(difflib.unified_diff((pre or b'').decode().splitlines(keepends=True),post.decode().splitlines(keepends=True),fromfile='/dev/null' if pre is None else 'a/'+p,tofile='b/'+p,n=3))
  patch=P/(PREFIX+'-18-PATH.patch');assert not patch.exists();patch.write_bytes(''.join(parts).encode())
  apply(after,patch,'--check');apply(after,patch)
  assert {p:get(after,p) for p in paths}==outputs
  apply(after,patch,'--reverse')
  assert {p:get(after,p) for p in paths}==source
 assets=[];derivation=load(P/'generated/DERIVATION.json')
 assert sha((P/'generated/DERIVATION.json').read_bytes())==previous_profile['generated_receipt_sha256']
 for row in derivation['files']:
  path='chicago/4d/'+row['file'];parent=blob(HEAD,path);child=(P/'generated'/row['file']).read_bytes()
  assert parent==blob(OLD,path) and sha(parent)==row['parent_sha256']
  assert sha(child)==row['sha256'] and len(child)==row['bytes']
  assets.append(dict(file=row['file'],parent_sha256=sha(parent),child_sha256=sha(child),child_bytes=len(child),receiving_parent_equals_V5=True))
 watched=list(previous['watched_untouched_source_pins'])+['.github/workflows/chicago-4d-check.yml','chicago/4d/AGENTS.md','chicago/4d/tools/test_check_harness.sh','chicago/4d/tools/test_parked_transport_empty_scene.mjs']
 watched_pins={p:sha(blob(HEAD,p)) for p in watched}
 fixture={p:sha(blob(HEAD,'chicago/4d/'+p)) for p in previous['critical_fixture_source_pins']}
 assert fixture==previous['critical_fixture_source_pins']
 registry_pins={p:sha(blob(HEAD,'chicago/4d/tools/'+p)) for p in ['writer_inventory.json','step_isolation.json']}
 rows=load(P/'EXACT-MEASURED-REGISTRY-ROWS.json')
 registry_preservation={}
 for name,section in [('writer_inventory.json','writer_inventory'),('step_isolation.json','step_isolation')]:
  original=json.loads(blob(HEAD,'chicago/4d/tools/'+name));entry=rows[section];assert entry['key'] not in original['tools']
  simulated=json.loads(json.dumps(original));simulated['tools'][entry['key']]=entry['entry']
  assert all(simulated[k]==v for k,v in original.items() if k!='tools')
  assert all(simulated['tools'][k]==v for k,v in original['tools'].items())
  registry_preservation[name]=dict(all_current_entries_retained=True,current_tools=len(original['tools']),proposed_tools=len(simulated['tools']),new_key=entry['key'])
 tree=subprocess.check_output(['git','--no-optional-locks','-C',str(R),'rev-parse',HEAD+'^{tree}'],timeout=8).decode().strip()
 assert tree=='9accbe84f035d8a7ff0b548aa2559bd59efe2cc7'
 preview=dict(status='IMMUTABLE_E2E_TEXT_PATCH_COMPATIBILITY_PREP_PASS_NOT_APPLIED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),receiving_commit=HEAD,receiving_TREE=tree,paths=paths,patch_sha256=sha(patch.read_bytes()),target_file_pins={p:sha(b) if b is not None else None for p,b in source.items()},target_output_pins={p:sha(b) for p,b in outputs.items()},watched_untouched_source_pins=watched_pins,critical_fixture_source_pins=fixture,registry_input_pins=registry_pins,all_eight_critical_sources_same_as_historical=True,changed_overlay_context_since_V5=changed,all_current_LIBERTIES_bytes_and_entry_location_preserved=True,complete_current_GUI_preload_and_assembly_test_prefix_exact=True,same_original_sixty_driver_test_lines=True,original_driver_test_block_sha256=sha(driver_tests),all_79_new_Navigator_test_lines_preserved_untouched=True,incoming_T3353_native_check_exact=True,registry_simulation=registry_preservation,all_overlay_changes_reverse_to_exact_receiving_bytes=True,eight_parent_child_hashes=assets,previous_V5_prepared_sha256=sha(prior_raw),all_previous_V5_artifacts_exact=True,historical_qualifications_not_retargeted=True,fresh_current_fixture_world_gate_CI_required=True,no_ROOT_source_or_index_writes=True,no_generation_heavy_qualification_commit_push_or_DEV_claim=True)
 preview_path=P/(PREFIX+'-PREVIEW.json');assert not preview_path.exists();preview_path.write_text(json.dumps(preview,indent=2)+'\n')
 profile=dict(previous_profile)
 profile.update(status='IMMUTABLE_E2E_OVERLAY_PREP_ONLY_HISTORICAL_QUALIFICATIONS_NOT_RETARGETED',receiving_checkpoint=HEAD,receiving_TREE=tree,reviewed_dev=DEV,source_profile='A620-COMPATIBLE-NEXT-V5-PROFILE.json',source_profile_sha256=sha((P/'A620-COMPATIBLE-NEXT-V5-PROFILE.json').read_bytes()),text_patch=patch.name,text_patch_sha256=sha(patch.read_bytes()),text_patch_current_root_readonly_preview=preview_path.name,preview_sha256=sha(preview_path.read_bytes()),registry_input_pins=registry_pins)
 profile_path=P/(PREFIX+'-PROFILE.json');assert not profile_path.exists();profile_path.write_text(json.dumps(profile,indent=2)+'\n')
 print(json.dumps(dict(status=preview['status'],patch_sha256=preview['patch_sha256'],profile_sha256=sha(profile_path.read_bytes()),changed_overlay_context_since_V5=changed,eight_parents_and_children_exact=True,original_sixty_driver_assertions_exact=True)))
if __name__=='__main__': main()
