from pathlib import Path
import ast,json,tempfile,copy
p=Path('/tmp/chicago-resumed-evidence-20261023T2245/publish_checkpoint.py');tree=ast.parse(p.read_text())
allowed={'WORK','REPO','REL','DEST','sha'}
nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id in allowed for t in n.targets)]
ns={'__file__':str(p)};exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),str(p),'exec'),ns)
w=ns['WORK'];ledger=json.loads((w/'STORAGE-ARCHIVE-OMISSIONS.json').read_text());row=json.loads((w/'ARCHIVES.json').read_text())[0]
with tempfile.TemporaryDirectory(dir='/workspace',prefix='archive-storage-guard-') as tmp:
 root=Path(tmp);ns['WORK']=root
 def check(change=None,expected_pass=False):
  doc=copy.deepcopy(ledger);doc['files']=doc['files'][:1]
  if change:change(doc)
  (root/'ARCHIVES.json').write_text(json.dumps([row]));(root/'STORAGE-ARCHIVE-OMISSIONS.json').write_text(json.dumps(doc))
  try:result=ns['verify_archive_availability']()
  except (AssertionError,KeyError):assert not expected_pass;return
  assert expected_pass and len(result)==1
 check(expected_pass=True)
 check(lambda d:d.update(files=[]))
 check(lambda d:d['files'][0].update(sha256='0'*64))
 check(lambda d:d['files'][0]['independent_remote_readback'].update(status='UNVERIFIED'))
 check(lambda d:d['files'][0].update(git_blob='0'*40))
 orig=ns['run']
 class Bad:stdout='100755 wrong 0 path'
 ns['run']=lambda args,check=True:Bad() if args[:2]==['git','ls-files'] else orig(args,check)
 check();ns['run']=orig
print('PASS: verified absent archive accepted; unknown/mismatched-hash/unverified-remote/wrong-blob/uncertain-index refusals all enforced.')
