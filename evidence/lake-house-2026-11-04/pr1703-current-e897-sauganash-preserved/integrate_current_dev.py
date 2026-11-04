from pathlib import Path
import base64,hashlib,json,subprocess,datetime
P=Path(__file__).parent;R=Path('/workspace/chicago-bridge-increment-20261102');Q=P/'integration-ce094';Q.mkdir(exist_ok=True);repo='repos/kevinrhaas/chicago/';oldhead='189e95d9b07d6c8c5237bde12c896a13f5df1459';oldbase='0a14eb07bc6630ace4ce8bec12b87e9fa1a4b0d4';branch='steward/t2379-editorial-proposal-20261104'
def api(p,b=None,m=None):
 c=['gh','api',repo+p]
 if m:c+=['--method',m]
 if b is not None:c+=['--input','-']
 return json.loads(subprocess.check_output(c,input=None if b is None else json.dumps(b).encode()))
def save(n,v):(Q/n).write_text(json.dumps(v,indent=2)+'\n')
def blob(path,ref):
 d=api('contents/'+path+'?ref='+ref);raw=base64.b64decode(d['content']) if d.get('encoding')=='base64' else base64.b64decode(api('git/blobs/'+d['sha'])['content']);assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==d['sha'];return raw,d['sha']
assert not (Q/'REF-ADVANCED.json').exists()
pr=api('pulls/1703');assert pr['head']['sha']==oldhead and not pr['merged'];dev=api('git/ref/heads/dev')['object']['sha'];assert dev.startswith('ce094fbe'),dev
comparison=api('compare/'+oldbase+'...'+dev);save('INCOMING-COMPARE.json',comparison);assert comparison['status']=='ahead' and comparison['behind_by']==0
files=json.loads((P/'SOURCE-FILE-BINDINGS.json').read_text());nodes=[];bindings={}
for rel in files:
 path='chicago/4d/'+rel;own=(R/path).read_bytes()
 if rel.startswith('docs/'):
  baseline=subprocess.check_output(['git','show',oldbase+':'+path],cwd=R);assert own.endswith(baseline);prefix=own[:-len(baseline)];incoming,incomingblob=blob(path,dev);out=prefix+incoming;assert out.endswith(incoming)
 elif rel=='changelog.d/T-2379.json':out=own;assert not any(f['filename']==path for f in comparison['files'])
 else:
  before=subprocess.check_output(['git','show',oldbase+':'+path],cwd=R);incoming,incomingblob=blob(path,dev);assert incoming==before,('Lake authored/compiled input changed concurrently',path);out=own
 dest=Q/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(out);expected=hashlib.sha1(b'blob '+str(len(out)).encode()+b'\0'+out).hexdigest();b=api('git/blobs',{'encoding':'base64','content':base64.b64encode(out).decode()});assert b['sha']==expected;nodes.append({'path':path,'mode':'100644','type':'blob','sha':expected});bindings[rel]={'git_blob':expected,'sha256':hashlib.sha256(out).hexdigest()}
basecommit=api('git/commits/'+dev);newtree=api('git/trees',{'base_tree':basecommit['tree']['sha'],'tree':nodes});save('TREE.json',newtree)
commit=api('git/commits',{'message':'Merge current dev into T-2379 notes correction; preserve Sauganash qualified outputs','tree':newtree['sha'],'parents':[oldhead,dev]});save('COMMIT.json',commit)
# Ordinary fast-forward of own branch only; no source branch force push.
assert api('git/ref/heads/'+branch)['object']['sha']==oldhead
result=api('git/refs/heads/'+branch,{'sha':commit['sha'],'force':False},'PATCH');save('REF-ADVANCED.json',result);assert result['object']['sha']==commit['sha']
read=api('pulls/1703');save('PR-READBACK.json',read);assert read['head']['sha']==commit['sha']
scope=api('compare/'+dev+'...'+commit['sha']);save('OWN-SCOPE-COMPARE.json',scope);assert {f['filename']for f in scope['files']}==set('chicago/4d/'+r for r in files)
audit={'old_source_execution':oldhead,'integrated_head':commit['sha'],'tree':newtree['sha'],'base_dev':dev,'incoming_sauganash_and_all_foreign_postimages_preserved_by_dev_base_tree':True,'exact_same3LakeJSONoutputs':all(bindings[r]==files[r] for r in files if r.endswith('.json')),'raw_history_docs':True,'whole_source_gate':'PENDING_CURRENT_HEAD8','no_native_no_browser_execution':True,'scoped_validation_carry':'All Lake authored/compiled/geometry inputs and owner code remain exact; incoming foreign source qualified by1701; current full hosted8 still mandatory.'};save('SOURCE-SCOPE-CARRY.json',audit);save('SOURCE-FILE-BINDINGS.json',bindings);print(json.dumps(audit))
