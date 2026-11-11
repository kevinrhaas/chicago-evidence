from pathlib import Path
import hashlib,json,os,stat,subprocess
P=Path(__file__).resolve().parent
raw=(P/'FREEZE.json').read_bytes();pin=hashlib.sha256(raw).hexdigest();d=json.loads(raw)
assert pin==json.loads((P/'READY.json').read_text())['freeze_SHA256'] and d['parts']==16
root=Path(d['root']);env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
def git(*a):return subprocess.check_output(['git','-C',str(root),*a],env=env).decode().strip()
assert len(d['rows'])==d['frozen_file_count']
for row in d['rows']:
 p=root/row['file'];s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 assert s.st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['file']
 assert ('100755' if s.st_mode&stat.S_IXUSR else '100644')==row['Git_mode'],row['file']
for path in d['deleted_paths']:assert not (root/path).exists() and not (root/path).is_symlink()
assert git('rev-parse','HEAD')==d['head'] and git('branch','--show-current')==d['branch']
assert git('rev-parse','--verify',d['protected_ref'])==d['protected_ref_head']
assert (Path(git('rev-parse','--absolute-git-dir'))/'MERGE_HEAD').read_text().strip()==d['incoming_dev']
assert git('ls-files','-u')=='' and git('diff','--name-only')==''
assert sorted(git('diff','--cached','--name-only').splitlines())==d['expected_staged_paths']
assert git('write-tree')==d['index_tree']
assert hashlib.sha256(Path(d['wrapper']).read_bytes()).hexdigest()==d['wrapper_SHA256']
print('S2_SOURCE_VERIFIED '+pin+' native8_fixture_primary_ref_unchanged parts16')
