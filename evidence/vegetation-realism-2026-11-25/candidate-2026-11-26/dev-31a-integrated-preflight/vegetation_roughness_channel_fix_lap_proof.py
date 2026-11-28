"""Independently recheck every original feature edit over the integrated Dev."""
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
W=Path('/workspace/work');P='vegetation-roughness-channel-fix'
def qualify(proof):
 r=Path(proof['repo'])
 def git(*a,**kw):return subprocess.check_output(['git',*a],cwd=r,**kw)
 def raw(ref,path):return git('show',ref+':'+path)
 def digest(b):return hashlib.sha256(b).hexdigest()
 if not proof.get('standard_pr_lap_integration'):
  assert proof['exact_native_tree_after_authorship'] and proof['final_tree']==proof['native_candidate_tree']
  return {'complete':True,'exact_native_tree':True}
 original=json.loads((W/(P+'-authored-exact-source-proof.json')).read_text())
 assert original['exact_native_tree_after_authorship'] and original['final_tree']==proof['native_candidate_tree']==proof['authored_feature_tree']
 assert original['final_head']==proof['authored_feature_head']
 assert proof['all_feature_edits_preserved_after_standard_lap'] and proof['independently_applied_feature_code_verified']
 excluded={'chicago/4d/data/liberties.json','chicago/4d/docs/LIBERTIES.md','chicago/4d/docs/measurements/source_use_coverage.md'}
 patch=git('diff','--binary',original['actual_dev'],original['final_head'],'--','.',*[':(exclude)'+x for x in sorted(excluded)])
 assert (W/proof['original_feature_patch']).read_bytes()==patch
 assert digest(patch)==proof['original_feature_patch_sha256']
 with tempfile.TemporaryDirectory(prefix=P+'-recheck-lap-',dir=W) as d:
  env={**os.environ,'GIT_INDEX_FILE':d+'/index'}
  subprocess.run(['git','read-tree',proof['actual_dev']],cwd=r,env=env,check=True)
  subprocess.run(['git','apply','--cached','--check'],cwd=r,env=env,input=patch,check=True)
  subprocess.run(['git','apply','--cached'],cwd=r,env=env,input=patch,check=True)
  unresolved=git('write-tree',env=env).decode().strip()
  resolutions=proof.get('integration_resolution_patches',[])
  if resolutions:assert unresolved==proof['source_before_integration_resolution']
  for resolution in resolutions:
   assert resolution['kind']=='additional-readonly-restamp-check' and resolution['allowed_source_path']=='chicago/4d/tools/check.sh'
   body=(W/resolution['path']).read_bytes();assert digest(body)==resolution['sha256']
   path=resolution['allowed_source_path'];previous=git('write-tree',env=env).decode().strip();old=raw(previous,path)
   anchor=b'selftest "the batch re-stamps stale meshes through the emitter each entry names" \\\n  python3 tools/restamp_stale.py --self-test\n'
   addition=b'\n# The dry-run mode is a distinct contract from its parser/plan self-test.\nstep "the batch restamper checks stale meshes without emitting or changing bytes" \\\n  python3 tools/restamp_stale.py --check\n'
   assert old.count(anchor)==1 and b'python3 tools/restamp_stale.py --check' not in old
   subprocess.run(['git','apply','--cached'],cwd=r,env=env,input=body,check=True)
   after=git('write-tree',env=env).decode().strip()
   assert git('diff','--name-only',previous,after).decode().splitlines()==[path]
   assert raw(after,path)==old.replace(anchor,anchor+addition)
  before=git('write-tree',env=env).decode().strip();assert before==proof['source_before_metadata_owners']
  for path,h in original['feature_code_sha256'].items():
   assert digest(raw(original['final_tree'],path))==h,path
   assert raw(proof['final_tree'],path)==raw(before,path),path
   assert digest(raw(proof['final_tree'],path))==proof['feature_code_sha256'][path],path
  for resolution in reversed(resolutions):subprocess.run(['git','apply','--cached','--reverse'],cwd=r,env=env,input=(W/resolution['path']).read_bytes(),check=True)
  subprocess.run(['git','apply','--cached','--reverse'],cwd=r,env=env,input=patch,check=True)
  assert git('write-tree',env=env).strip()==git('rev-parse',proof['actual_dev']+'^{tree}').strip()
 lib='chicago/4d/docs/LIBERTIES.md';base=raw(original['actual_dev'],lib);ours=raw(original['final_tree'],lib)
 assert ours.startswith(base) and raw(proof['final_tree'],lib)==raw(proof['actual_dev'],lib)+ours[len(base):]
 for path,h in proof['source_sha256'].items():assert digest(raw(proof['final_tree'],path))==h,path
 for commit in proof['ticket_commits'].values():subprocess.run(['git','merge-base','--is-ancestor',commit,proof['final_head']],cwd=r,check=True)
 assert set(git('diff','--name-only',proof['actual_dev'],proof['final_tree']).decode().splitlines())==set(proof['source_sha256'])
 integrated=git('diff','--binary',proof['actual_dev'],proof['final_tree'])
 assert (W/proof['integrated_patch']).read_bytes()==integrated and digest(integrated)==proof['integrated_patch_sha256']
 for check in proof['checks']:
  assert check['exit_code']==0 and digest(Path(check['log']).read_bytes())==check['log_sha256']
 return {'complete':True,'exact_native_tree':False,'native_authored_tree':original['final_tree'],'authored_head':original['final_head'],'integrated_tree':proof['final_tree'],'actual_dev':proof['actual_dev'],'all_original_feature_code_edits_preserved':True,'every_upstream_byte_preserved_by_reverse_patch':True,'feature_code_paths':len(proof['feature_code_sha256']),'no_new_feature_authorship_after_native':True}
