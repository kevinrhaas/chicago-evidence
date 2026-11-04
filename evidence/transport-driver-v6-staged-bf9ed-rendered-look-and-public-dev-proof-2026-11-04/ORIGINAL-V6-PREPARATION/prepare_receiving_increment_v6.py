"""Preview exact DEV-E2E driver-look bytes; apply after actual PR1649 merge and ROOT GO.

Read-only by default. Never generates, stages, commits, pushes, runs owners or
claims fresh native/browser/world/photo qualification. All receiving file pins
must match the explicitly reviewed profile; later source changes are refused.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,re,shutil,subprocess,tempfile,time
P=Path(__file__).resolve().parent
PROFILE_PREFIX='E2E-COMPATIBLE-NEXT-V6'
PROFILE_SHA='12ccdb98256a1e5a8f00534fe2f2ae84c9970f0c40b7fda43cea0f8657f344c2'
PATCH_SHA='b41848eeb940bb8e852a6f5a5ea104305eb932b1ddab075ae7ba4dca3c320c7e'
REQUIRED_DEV='e2e4612fcf9946a343833b1e04adf4ca90322494'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()if p.exists()else None
def git(target,*args,check=True):return subprocess.run(['git','--no-optional-locks','-C',str(target),*args],check=check,capture_output=True,text=True,timeout=8)
def load(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--target',type=Path,required=True);ap.add_argument('--expected-head',required=True);ap.add_argument('--root-go',type=Path);ap.add_argument('--receipt',type=Path,required=True);ap.add_argument('--apply',action='store_true');a=ap.parse_args()
 target=a.target.resolve();receipt=a.receipt.resolve();assert not receipt.is_relative_to(target),'Keep receipt outside application checkout';assert not receipt.exists(),'Preserve previous receipts';assert re.fullmatch('[0-9a-f]{40}',a.expected_head)
 prefix,profile_sha,patch_sha,required_dev=PROFILE_PREFIX,PROFILE_SHA,PATCH_SHA,REQUIRED_DEV;pf=P/(prefix+'-PROFILE.json');assert sha(pf)==profile_sha;profile=load(pf);preview_path=P/profile['text_patch_current_root_readonly_preview'];preview=load(preview_path);assert sha(preview_path)==profile['preview_sha256'];patch=P/profile['text_patch'];assert sha(patch)==patch_sha==profile['text_patch_sha256']==preview['patch_sha256']
 assert sha(P/'generated/DERIVATION.json')==profile['generated_receipt_sha256'];deriv=load(P/'generated/DERIVATION.json');head=git(target,'rev-parse','HEAD').stdout.strip();assert head==a.expected_head,('Receiving HEAD changed',head)
 assert git(target,'remote','get-url','origin').stdout.strip()=='https://github.com/kevinrhaas/chicago.git'
 for path,h in preview['target_file_pins'].items():assert sha(target/path)==h,('Reviewed text target changed; refresh exact profile before adoption',path)
 for path,h in preview['watched_untouched_source_pins'].items():assert sha(target/path)==h,('Watched UI/startup source changed',path)
 for path,h in preview['transport_checkpoint_17_input_pins'].items():assert sha(target/path)==h,('Original17checkpoint receiving input changed',path)
 for row in deriv['files']:
  assert sha(target/'chicago/4d'/row['file'])==row['parent_sha256'],('Recipe parent changed',row['file'])
  child=P/'generated'/row['file'];assert sha(child)==row['sha256']and child.stat().st_size==row['bytes'],('Prepared child changed',row['file'])
 for path,h in preview['critical_fixture_source_pins'].items():assert sha(target/'chicago/4d'/path)==h,('Reviewed actuala620 fixture-critical source changed; fresh profile and qualification required',path)
 supplement=(P/profile['status_append']).read_bytes();status_path=target/'chicago/4d/docs/STATUS.md';previous_status=status_path.read_bytes();assert supplement not in previous_status,'Supplement already present'
 for name,h in preview['registry_input_pins'].items():assert sha(target/'chicago/4d/tools'/name)==h,('Current registry context changed; refresh profile before adoption',name)
 operations=[];rows=load(P/profile['registry_rows'])
 for section,filename in [('writer_inventory','writer_inventory.json'),('step_isolation','step_isolation.json')]:
  path=target/'chicago/4d/tools'/filename;old=load(path);row=rows[section];assert row['key']not in old['tools'],('Registry row already exists',row['key']);new=json.loads(json.dumps(old));new['tools'][row['key']]=row['entry'];operations.append((path,old,new))
 with tempfile.TemporaryDirectory(prefix='driver-v6-guard-preview-',dir=P)as temporary:
  snapshot=Path(temporary)
  for path in preview['paths']:
   src=target/path
   if src.exists():dst=snapshot/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
  subprocess.run(['git','apply','--check',str(patch)],cwd=snapshot,check=True,capture_output=True,timeout=8)
  subprocess.run(['git','apply',str(patch)],cwd=snapshot,check=True,capture_output=True,timeout=8)
  assert all(sha(snapshot/path)==h for path,h in preview['target_output_pins'].items()),'Actual patch output differs from reviewed output pins'
 affected=preview['paths']+['chicago/4d/docs/STATUS.md']+[str(p.relative_to(target))for p,_,_ in operations]+['chicago/4d/'+r['file']for r in deriv['files']]
 def source():
  index=subprocess.check_output(['git','--no-optional-locks','-C',str(target),'ls-files','--stage','-z'],timeout=8)
  return dict(HEAD=git(target,'rev-parse','HEAD').stdout.strip(),TREE=git(target,'rev-parse','HEAD^{tree}').stdout.strip(),APP=git(target,'rev-parse','HEAD:chicago/4d').stdout.strip(),semantic_index_sha256=hashlib.sha256(index).hexdigest())
 original_source=source()
 before={path:sha(target/path)for path in affected};watched={path:sha(target/path)for path in preview['watched_untouched_source_pins']};present=git(target,'merge-base','--is-ancestor',required_dev,'HEAD',check=False).returncode==0
 result=dict(status='READ_ONLY_V6_ADOPTION_PREVIEW_PASS_NOT_APPLIED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=head,profile='DEV-E2E-V6',profile_sha256=profile_sha,preview_sha256=sha(preview_path),patch_sha256=patch_sha,required_dev=required_dev,required_dev_is_ancestor=present,original_eight_parent_and_child_hashes_exact=True,actual_reviewed_critical_fixture_sources_exact=True,critical_readers_same_as_historical=preview['all_eight_critical_sources_same_as_historical'],all_reviewed_receiving_text_and_watched_UI_pins_exact=True,actual_patch_output_pins_verified_in_external_scratch=True,before=before,must_regenerate_on_receiving_base=profile['receiving_owner_commands_original120_each'],historical_native_browser_results_not_retargeted=True,fresh_current_native_fixture_world_gate_CI_and_DEV_acceptance_pending=True,no_gate_world_photo_commit_push_or_DEV_claim=True)
 if a.apply:
  assert a.root_go is not None and not a.root_go.resolve().is_relative_to(target),'Explicit ROOT GO outside app required after1649merge'
  go=load(a.root_go)
  assert go['policy']=='ROOT_AUTHORIZED_NEXT_DRIVER_V6_APPLICATION_AFTER_PR1649_MERGE'and go['approved']is True
  assert Path(go['target_repo']).resolve()==target and go['profile_sha256']==PROFILE_SHA and go['guard_sha256']==sha(Path(__file__).resolve())
  assert go['source']==original_source,'ROOT GO must bind actual clean receiving HEAD/tree/app/index'
  branch=git(target,'symbolic-ref','--short','HEAD').stdout.strip()
  assert branch.startswith('steward/')and branch!='steward/t3088-horse-photoquality-20261026','Use a new receiving feature branch after1649merge'
  assert go['branch']==branch and go['fresh_claim_and_rival_reviewed']is True
  assert present,'Receiving HEAD must include reviewed DEV62'
  assert not git(target,'status','--porcelain','--untracked-files=no').stdout,'Receiving tracked tree must be clean'
  assert git(target,'rev-parse','--verify','-q','MERGE_HEAD',check=False).returncode==1,'Finish current merge first'
  pr=json.loads(subprocess.check_output(['gh','api',f'repos/kevinrhaas/chicago/pulls/1649?driver_adoption={int(time.time())}'],timeout=30))
  assert pr['number']==1649 and pr['merged']is True and pr['state']=='closed'and pr['base']['ref']=='dev'and pr['base']['repo']['full_name']=='kevinrhaas/chicago','PR1649 must actually be merged into DEV before applying'
  merged_sha=pr['merge_commit_sha'];assert re.fullmatch('[0-9a-f]{40}',merged_sha)and go['pr1649_merge_sha']==merged_sha
  assert git(target,'merge-base','--is-ancestor',merged_sha,'HEAD',check=False).returncode==0,'Receiving HEAD must contain actual merged PR1649'
  assert git(target,'rev-parse','HEAD').stdout.strip()==head
  assert before=={path:sha(target/path)for path in affected}and source()==original_source,'Receiving source changed during review'
  subprocess.run(['git','apply',str(patch)],cwd=target,check=True,capture_output=True,timeout=8)
  assert all(sha(target/path)==h for path,h in preview['target_output_pins'].items())
  status_path.write_bytes(previous_status+(b'\n'if previous_status.endswith(b'\n')else b'\n\n')+supplement)
  for path,old,new in operations:
   path.write_text(json.dumps(new,indent=2)+'\n');actual=load(path)
   assert all(actual[k]==v for k,v in old.items()if k!='tools')
   assert all(actual['tools'][k]==v for k,v in old['tools'].items())
  for row in deriv['files']:shutil.copyfile(P/'generated'/row['file'],target/'chicago/4d'/row['file'])
  assert status_path.read_bytes().startswith(previous_status);assert watched=={path:sha(target/path)for path in watched}
  result.update(status='APPLIED_EXACT_V6_PAYLOADS_FRESH_OWNERS_FIXTURE_WORLD_GATE_CI_PENDING',verified_pr1649_merge_sha=merged_sha,after={path:sha(target/path)for path in affected})
 else:
  assert before=={path:sha(target/path)for path in affected},'Target changed during read-only preview'
  assert watched=={path:sha(target/path)for path in watched},'Watched target changed during read-only preview'
  assert source()==original_source,'Source metadata changed during read-only preview'
 result.update(source_before=original_source,apply_branch_executed=a.apply,actual_PR1649_merge_and_ROOT_GO_required=True)
 receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in['status','head','profile','required_dev_is_ancestor']}))
if __name__=='__main__':main()
