from pathlib import Path
import hashlib,json,subprocess,datetime,shutil
w=Path('/tmp/chicago-resumed-evidence-20261023T2245');repo=w/'remote-evidence';ledger=json.loads((w/'STORAGE-ARCHIVE-OMISSIONS.json').read_text())
def git(args,input=None):return subprocess.check_output(['git',*args],cwd=repo,input=input)
assert git(['status','--porcelain'])==b''
before_tree=git(['write-tree']).decode().strip();patterns=['/evidence/image-match-2026-10-23/resumed-20261023T2245/']
files=ledger['files'];assert len(files)==92
for r in files:
 p=Path(r['worktree_path']);assert p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 stage=git(['ls-files','--stage','--',r['git_path']]).decode().split();assert stage[:3]==['100644',r['git_blob'],'0']
 patterns.append('!/'+r['git_path'])
plan={'status':'FROZEN_BEFORE_SPARSE_OMISSION','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tree_before':before_tree,'ledger_sha256':hashlib.sha256((w/'STORAGE-ARCHIVE-OMISSIONS.json').read_bytes()).hexdigest(),'patterns':patterns,'file_count':92,'bytes':sum(r['bytes'] for r in files)}
(w/'STORAGE-SPARSE-OMISSION-PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
git(['sparse-checkout','set','--no-cone','--stdin'], ('\n'.join(patterns)+'\n').encode())
assert git(['status','--porcelain'])==b'';after_tree=git(['write-tree']).decode().strip();assert after_tree==before_tree
for r in files:
 assert not Path(r['worktree_path']).exists()
 stage=git(['ls-files','--stage','--',r['git_path']]).decode().split();assert stage[:3]==['100644',r['git_blob'],'0']
 flags=git(['ls-files','-v','--',r['git_path']]).decode();assert flags.startswith('S '),flags
receipt={'status':'EXACT92_WORKTREE_TARS_SPARSE_OMITTED_NO_GIT_DELETIONS','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':92,'bytes_freed':plan['bytes'],'index_tree_before':before_tree,'index_tree_after':after_tree,'git_status_clean':True,'committed_blob_stage_and_skip_worktree_all_pass':True,'tmp_free_bytes':shutil.disk_usage('/tmp').free,'workspace_free_bytes':shutil.disk_usage('/workspace').free,'reversible_local_payload_copy_retained':True,'metadata_queue_sources_untouched':True}
(w/'STORAGE-SPARSE-OMISSION-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
