"""One normal SHA-guarded squash, only after exact-head eight-part gate+aggregate success."""
from pathlib import Path
import subprocess,json,hashlib,datetime
P=Path(__file__).parent;Q=P/'merge62f';Q.mkdir(exist_ok=True);W=Path('/tmp/wolf-poster-source-20261103');H='62f4546114e252c867dc2b43f2e6cac5503b0577';BASE='26f6b8dfe96e9af96d7137b8e7b8a8d4061512c0';TREE='6c8baae9f38833e6fa7266c9426bf7af1eab7544';RUN=41782679351
read=lambda p:json.loads(Path(p).read_bytes());git=lambda *a:subprocess.check_output(['git','-C',str(W),*a]);sha=lambda b:hashlib.sha256(b).hexdigest()
def api(path,body=None,method=None):
 cmd=['gh','api','repos/kevinrhaas/chicago/'+path]
 if method:cmd+=['--method',method]
 if body is not None:cmd+=['--input','-']
 return json.loads(subprocess.check_output(cmd,input=json.dumps(body).encode()if body is not None else None))
def save(name,data):(Q/name).write_text(json.dumps(data,indent=2)+'\n')
assert not(Q/'MERGE-ATTEMPT-INTENT.json').exists()and not(Q/'MERGE-RESPONSE.json').exists(),'Already attempted merge: inspect actual PR and saved intent/response before any repeat'
assert git('rev-parse','HEAD').decode().strip()==H and git('write-tree').decode().strip()==TREE and not git('status','--porcelain')
for n in ['OWNERS-REAPER.json','NATIVE-AUDIT-REAPER.json','SCOPE-TYPED-ROSTER-REAPER.json','PUBLISH-REAPER.json','CHECK-PUBLISHED-REAPER.json','PUBLISHED-TARGET-REAPER.json']:
 r=read(P/'gt26-final'/n);assert r['command_exit']==0 and r['all_children_reaped']and not r['leftover_cleanup']
assert read('/tmp/jail-c9fe-peer-review-20261104/GT26-FOCUSED-ADDENDUM.json')['head']==H
run=api('actions/runs/'+str(RUN));jobs=api('actions/runs/'+str(RUN)+'/jobs?per_page=100');save('GATE-ACTUAL.json',{'run':run,'jobs':jobs})
assert run['head_sha']==H and run['name']=='Chicago 4D — gate'
assert run['status']=='completed'and run['conclusion']=='success','WAIT: current gate is not completed SUCCESS'
expected={'gate'}|{'gate part '+str(i)+'/8'for i in range(1,9)};actual={j['name']:j for j in jobs['jobs']};assert expected<=set(actual)
assert all(actual[n]['status']=='completed'and actual[n]['conclusion']=='success'for n in expected),'WAIT: named parts/aggregate not all success'
pr=api('pulls/1683');save('PR-PRE-MERGE.json',pr);assert pr['head']['sha']==H and pr['base']['ref']=='dev'and pr['state']=='open'and not pr['draft']and not pr['merged']and pr['mergeable']is True
lap=api('git/ref/heads/lap/pr-1683');save('OWN-LAP-PRE-MERGE.json',lap);assert lap['object']['sha']=='3b1947a8e2a0d97008b4a986a7fab35fff30aca0','Own lap changed; do not merge over another holder'
base=api('git/ref/heads/dev')['object']['sha'];comp=api('compare/'+BASE+'...'+base);save('CURRENT-DEV-FOLD-COMPARE.json',comp);assert comp['behind_by']==0
allowed={'chicago/4d/changelog.d/T-2376.json','chicago/4d/renderers/web/js/changelog.js'};assert {f['filename']for f in comp['files']}<=allowed,'New non-fold base work requires separate review before merge'
files={}
for line in git('ls-tree','-rz','HEAD').split(b'\0'):
 if not line:continue
 pre,path=line.split(b'\t',1);mode,typ,oid=pre.split();files[path.decode()]={'mode':mode.decode(),'sha':oid.decode()}
def root_hash(fs):
 dirs={'':{}}
 for path,row in fs.items():
  parts=path.split('/');parent=''
  for part in parts[:-1]:
   child=parent+'/'+part if parent else part;dirs.setdefault(parent,{})[part]={'dir':child};dirs.setdefault(child,{});parent=child
  dirs[parent][parts[-1]]=row
 def tree(path):
  raw=b''
  for name,row in sorted(dirs[path].items(),key=lambda x:(x[0]+('/'if'dir'in x[1]else'')).encode()):
   mode='40000'if'dir'in row else row['mode'].lstrip('0');oid=tree(row['dir'])if'dir'in row else row['sha'];raw+=mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid)
  return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 return tree('')
assert root_hash(files)==TREE
for row in comp['files']:
 name=row['filename']
 if row['status']=='removed':assert name in files;del files[name]
 else:assert name in files;files[name]['sha']=row['sha']
expected_tree=root_hash(files);save('PRE-MERGE-COMPOSITION.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':H,'source_tree':TREE,'current_dev':base,'changes_since_integrated_dev':'Only automatic T2376 changelog fold; no native/runtime data change','expected_normal_squash_tree':expected_tree,'expected_file_count':len(files),'gate_run':RUN,'all8_and_namedaggregate_actualSUCCESS':True,'all_source_audits_and_peer_reviews_qualified':True})
# Ordinary GitHub PR merge; exact head SHA, no force/admin/bypass option.
save('MERGE-ATTEMPT-INTENT.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':H,'base':base,'expected_tree':expected_tree,'method':'ordinary squash','uncertain_response_policy':'Do not repeat PUT; read actual PR state and recover result from GitHub if response is lost'})
response=api('pulls/1683/merge',{'sha':H,'merge_method':'squash','commit_title':pr['title'],'commit_message':'Bounded keeper-house/compound increment. Actual target runtime and independent current consumer/native audits are saved in the PR evidence; all eight current source gate parts and aggregate pass. Original T-2380 remains partial/open with documented image, material and visibility differences.'},'PUT');save('MERGE-RESPONSE.json',response);assert response['merged']is True,response
merged=api('pulls/1683');save('PR-MERGED.json',merged);assert merged['merged']and merged['head']['sha']==H and merged['merge_commit_sha']==response['sha']
commit=api('git/commits/'+response['sha']);save('MERGE-COMMIT.json',commit);assert commit['tree']['sha']==expected_tree and [r['sha']for r in commit['parents']]==[base],('Actual merge composition differs; report immediately',commit['tree'],expected_tree)
save('MERGE-COMPOSITION-PASS.json',{'merged_head':response['sha'],'tree':commit['tree']['sha'],'parent':base,'actual_tree_exact_expected_source62f_plus_only_T2376_fold':True,'source_head_still':git('rev-parse','HEAD').decode().strip(),'original_T2380':'partial/open; no ticket metadata touched','public_source_checkpoint':'74a1dadc2fe5609c3ed762525eee6ea89c352644','gate_actual_run':RUN});print('NORMAL SQUASH MERGED',response['sha'],'TREE COMPOSITION EXACT',commit['tree']['sha'],flush=True)
