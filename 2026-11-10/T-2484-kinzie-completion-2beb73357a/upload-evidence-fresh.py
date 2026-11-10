import pathlib,subprocess,json,base64,hashlib,time,concurrent.futures
BASE=pathlib.Path('/tmp/nov10-kinzie-ui');ROOT=BASE/'public-packet';PREFIX='2026-11-10/T-2484-kinzie-completion-2beb73357a';REPO='repos/kevinrhaas/chicago-evidence'
import importlib.util
spec=importlib.util.spec_from_file_location('fresh','/tmp/nov10-kinzie-source/fresh-github-api.py');fresh=importlib.util.module_from_spec(spec);spec.loader.exec_module(fresh)
def api(endpoint,body=None,method=None):
 return fresh.api(REPO+'/'+endpoint,body,method)
files=sorted(p for p in ROOT.rglob('*')if p.is_file());journal=BASE/'EVIDENCE-UPLOAD-JOURNAL.json';done=json.loads(journal.read_text())if journal.exists()else{}
def upload(p):
 n=p.relative_to(ROOT).as_posix();b=p.read_bytes();sha=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
 if done.get(n,{}).get('sha')!=sha:
  r=api('git/blobs',{'content':base64.b64encode(b).decode(),'encoding':'base64'});assert r['sha']==sha
 return n,{'sha':sha,'bytes':len(b)}
entries=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for n,x in pool.map(upload,files):
  done[n]=x;journal.write_text(json.dumps(done,indent=2)+'\n');entries.append({'path':PREFIX+'/'+n,'mode':'100644','type':'blob','sha':x['sha']});print('UPLOADED',n,x['bytes'],flush=True)
for attempt in range(5):
 parent=api('git/ref/heads/main')['object']['sha'];tree=api('git/trees',{'base_tree':api('git/commits/'+parent)['tree']['sha'],'tree':entries})['sha'];commit=api('git/commits',{'message':'T-2484: qualify actual published Kinzie1812 desktop and default phone completion with bounded source and native evidence','tree':tree,'parents':[parent]})['sha']
 try:r=api('git/refs/heads/main',{'sha':commit,'force':False},'PATCH')
 except RuntimeError:
  if attempt==4:raise
  continue
 read=api('git/ref/heads/main')['object']['sha'];assert read==commit
 receipt={'repository':'kevinrhaas/chicago-evidence','commit':commit,'parent':parent,'files':len(entries),'path':PREFIX,'url':'https://github.com/kevinrhaas/chicago-evidence/tree/'+commit+'/'+PREFIX,'force':False,'readback':read}
 (BASE/'PUBLIC-EVIDENCE-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True);break
