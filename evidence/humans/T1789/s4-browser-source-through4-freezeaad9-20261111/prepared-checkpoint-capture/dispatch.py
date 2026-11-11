"""Exactly one ROOT-reviewed S4/H4 artifact-only dispatch; never retries a POST."""
from pathlib import Path
import argparse,base64,datetime,hashlib,json,re,subprocess,time,urllib.parse
P=Path(__file__).resolve().parent
AUTHOR=Path('/tmp/ROOT-T1789-LINEN-S4-CHECKPOINT-REQUEST-AUTHORING-PREP-20261111')
POST=Path('/tmp/ROOT-T1789-LINEN-S4-CHECKPOINT-POSTGATE-PREP-20261111')
BRANCH='steward/t1789-1812-loose-linen-seat-20261111'
TREE='60695ea8050960aa8c7f9c7570992ebf5ed60057'
PARENTS=['0a57979840bea7c37ba41ba4e24133a9510b59b9']
WF='4a73bb1b454dcb7d8d40e01bc1d801d635573465fd400b5f356e9eed8a535c53'
OWNER='efcd568ebf5cfb16609666aa1bd4e0411b34b390deaa680773f8653b24faefb5'
TEMPLATE='83ba2447416107faa1d4a40813b5d414eda35343df6818979217fe7d52ffff79'
REPO='repos/kevinrhaas/chicago'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    assert p.stat().st_size<=1048576;return json.loads(p.read_bytes())
def save(name,value):
    q=P/name;assert not q.exists(),str(q);q.write_text(json.dumps(value,indent=2)+'\n')
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def accepted(c):
    r,k,g=c['result'],c['cleanup'],c['resources']
    assert c['accepted'] and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None
    assert k['cleanup_complete'] and not k['remaining_owned_children'] and g['accepted']
def get(endpoint,name=None,cap=1048576):
    r=subprocess.run(['gh','api','--hostname','github.com','--method','GET',REPO+'/'+endpoint],capture_output=True,timeout=20)
    assert r.returncode==0,r.stderr.decode(errors='replace')[:300];assert len(r.stdout)<=cap
    if name:assert not (P/name).exists();(P/name).write_bytes(r.stdout)
    return json.loads(r.stdout)
def dispatch_runs():
    value=get('actions/workflows/chicago-4d-humans.yml/runs?event=workflow_dispatch&branch='+urllib.parse.quote(BRANCH,safe='')+'&per_page=100')
    assert value['total_count']==len(value['workflow_runs'])<=100,'complete bounded branch dispatch page'
    return value
parser=argparse.ArgumentParser();parser.add_argument('--reviewed-h4',required=True);parser.add_argument('--reviewed-source',required=True);args=parser.parse_args()
S=args.reviewed_source;assert re.fullmatch('[0-9a-f]{40}',S) and S not in PARENTS
assert re.fullmatch('[0-9a-f]{64}',args.reviewed_h4)
assert not any((P/n).exists() for n in ['DISPATCH-INTENT.json','DISPATCH.json','REGISTERED.json']),'one POST attempt only'
closed=load(AUTHOR/'CLOSED.json');accepted(closed)
a=load(AUTHOR/'AUTHORING.json');assert sha(AUTHOR/'AUTHORING.json')==closed['AUTHORING_SHA256']
assert closed['cell_SHA256']=='567fdc0add16adf0268bb3d3a20f6eaeb6ac158cce06db12f2ec4acf2d0b6496'
assert sha(AUTHOR/'SOURCE-PINS.json')=='a9455c71f685a4b6ab59bf55db091732450424d8ef082c2211def3fa17bd33c9'
for n,h in load(AUTHOR/'SOURCE-PINS.json').items():assert sha(AUTHOR/n)==h,n
review=load(AUTHOR/'ROOT-REQUEST-REVIEW.json')
assert review['status']=='ROOT_REVIEWED_ACTUAL_S4_H4_CANONICAL_CAPTURE_REQUEST' and review['source']==review['definition']==S and review['H4']==args.reviewed_h4
assert a['source_commit']==a['definition_commit']==S and a['parents']==PARENTS and a['tree']==TREE
assert a['all16_source_parts_verified'] and a['frozen301_prepost_verified'] and a['old_native8_and_fixture_preserved']
assert a['owner_sha256']==review['owner_sha256']==OWNER and a['template_sha256']==review['template_sha256']==TEMPLATE and a['workflow_sha256']==review['workflow_sha256']==WF
assert a['selected_unique_input_bindings']==review['inputs']==245
assert review['one_artifact_only_capture_authorized'] is True and review['automatic_POST_retry'] is False
assert review['AUTHORING_SHA256']==closed['AUTHORING_SHA256'] and review['CLOSED_SHA256']==sha(AUTHOR/'CLOSED.json')
for doc in (a,review):
    assert doc['source_checkpoint_only'] is True and doc['needs_final_DEV_integration'] is True and doc['merge_ready'] is False
for phase,name in [('COMMIT','COMMIT'),('PREFLIGHT','PREFLIGHT'),('PUSH','PUSH'),('REMOTE-VERIFY','REMOTE')]:
    c=load(POST/phase/'CLOSED.json');accepted(c);r=POST/phase/(name+'-RECEIPT.json');doc=load(r)
    assert sha(POST/phase/'CLOSED.json')==a['postgate_receipts'][phase]['CLOSED_SHA256']
    assert sha(r)==c['receipt_SHA256']==a['postgate_receipts'][phase]['receipt_SHA256'] and doc['head']==S and doc['tree']==TREE
    assert doc['source_checkpoint_only'] is True and doc['needs_final_DEV_integration'] is True and doc['merge_ready'] is False
assert set(a['postgate_receipts'])=={'COMMIT','PREFLIGHT','PUSH','REMOTE-VERIFY'}
remote=load(POST/'REMOTE-VERIFY/REMOTE-RECEIPT.json')
assert remote['parents']==PARENTS and remote['all301_local_frozen_SHA256_bytes_modes_preserved']
assert len(remote['remote_changed_entries'])==3 and sum(r['remote_body_verified'] for r in remote['remote_changed_entries'])==1
assert {r['file'] for r in remote['remote_changed_entries'] if r['remote_body_verified']}=={'.github/workflows/chicago-4d-humans.yml'}
assert {r['file'] for r in a['files']}=={'request/REFRESH.json','request/clothing-capture-v2.json'}
for row in a['files']:
    f=AUTHOR/row['file'];assert f.stat().st_size==row['bytes'] and sha(f)==row['sha256']
f=AUTHOR/'request/clothing-capture-v2.json';request=load(f);H=sha(f)
assert H==args.reviewed_h4==a['review_request_H4'] and request['basis_revision']==S
assert len(request['inputs'])==len({r['file'] for r in request['inputs']})==245
assert request['families']==[review['family']]==[{'recipe':'data/humans/recipes/settler_1812.json','variant':'settler_1812','assembly':'settler_1812_v1','liberty':'L418'}]
assert request['release'] is False and request['install'] is False and request['native_fit_accepted'] is False and request['material_admission'] is None
commit=get('git/commits/'+S,'remote-commit.json');assert commit['sha']==S and commit['tree']['sha']==TREE and [r['sha'] for r in commit['parents']]==PARENTS
remote={}
for name,path,pin in [('workflow','.github/workflows/chicago-4d-humans.yml',WF),('owner','chicago/4d/tools/human_clothing_capture_v2.py',OWNER),('template','chicago/4d/data/humans/studies/clothing-capture-v2.json',TEMPLATE)]:
    v=get('contents/'+path+'?ref='+S,name+'-remote-api.json',262144);raw=base64.b64decode(v['content']);assert hashlib.sha256(raw).hexdigest()==pin
    (P/(name+'-remote.raw')).write_bytes(raw);remote[name]={'file':path,'Git_blob':v['sha'],'SHA256':pin}
assert {r['file'] for r in request['inputs']}=={r['file'] for r in json.loads((P/'template-remote.raw').read_bytes())['inputs']}
assert get('git/ref/heads/'+BRANCH,'branch-before.json')['object']['sha']==S
before=dispatch_runs();save('runs-before.json',before)
assert not [r for r in before['workflow_runs'] if r['head_sha']==S and r['head_branch']==BRANCH],'duplicate S4 dispatch exists'
assert sha(f)==H and sha(AUTHOR/'AUTHORING.json')==closed['AUTHORING_SHA256']
inputs={'build_clothing_capture_v2':True,'clothing_source_ref':S,'clothing_manifest_sha256':H,'build_teamsters':False,'build_seated_driver_study':False,'build_dress_study':False,'source_ref':'','render_library_stills':False,'library_source_run':''}
payload={'ref':BRANCH,'inputs':inputs};save('dispatch-input.json',payload)
save('REQUEST-SOURCE-REVIEW.json',{'at':stamp(),'status':'ACTUAL_ACCEPTED_S4_H4_AND_FRESH_REMOTE_BINDINGS_VERIFIED','source':S,'definition':S,'H4':H,'AUTHORING_SHA256':closed['AUTHORING_SHA256'],'ROOT_review_SHA256':sha(AUTHOR/'ROOT-REQUEST-REVIEW.json'),'input_count':245,'remote':remote,'release':False,'install':False,'native_fit_accepted':False})
save('DISPATCH-INTENT.json',{'at':stamp(),'source':S,'definition':S,'H4':H,'payload_SHA256':sha(P/'dispatch-input.json'),'attempt':1,'old_failed_runs':[43000644195,43018920928,43053758545],'new_source_distinct_from_old_failed_capture':S!=PARENTS[0],'automatic_retry':False})
try:
    r=subprocess.run(['gh','api','--hostname','github.com','--method','POST','--include',REPO+'/actions/workflows/chicago-4d-humans.yml/dispatches','--input',str(P/'dispatch-input.json')],capture_output=True,timeout=30)
except BaseException as e:
    save('POST-TRANSPORT-ERROR.json',{'at':stamp(),'error':type(e).__name__+': '+str(e),'acceptance_unknown':True,'automatic_retry':False});raise
(P/'dispatch-response.txt').write_bytes(r.stdout);(P/'dispatch-stderr.txt').write_bytes(r.stderr)
status=r.stdout.decode(errors='replace').splitlines()[0] if r.stdout else ''
record={'at':stamp(),'returncode':r.returncode,'HTTP_status':status,'accepted_204':r.returncode==0 and '204' in status,'source':S,'definition':S,'H4':H,'payload':payload,'automatic_retry':False,'release':False,'install':False,'production':False}
save('DISPATCH.json',record);print(json.dumps(record),flush=True)
assert record['accepted_204'],'REFUSAL/UNKNOWN: stop; no fallback or automatic second POST'
found=[]
for i in range(5):
    runs=dispatch_runs();found=[r for r in runs['workflow_runs'] if r['head_branch']==BRANCH and r['head_sha']==S]
    if found:break
    if i<4:time.sleep(2)
assert len(found)==1,'POST accepted but unique run pending/ambiguous; metadata GET only, never re-POST'
run=found[0];assert run['id'] not in (43000644195,43018920928,43053758545) and run['event']=='workflow_dispatch' and run['run_attempt']==1
save('run-created.json',run);jobs=get('actions/runs/'+str(run['id'])+'/jobs?per_page=100','jobs-created.json')
registered={'at':stamp(),'status':'ONE_NEW_S4_CANONICAL_ARTIFACT_ONLY_CAPTURE_REGISTERED','run_id':run['id'],'html_url':run['html_url'],'event':run['event'],'run_status':run['status'],'run_conclusion':run['conclusion'],'source_SHA':S,'definition_expected_SHA':S,'runtime_definition_binding_pending':True,'H4':H,'head_branch':BRANCH,'workflow_path':'.github/workflows/chicago-4d-humans.yml','workflow_SHA256':WF,'inputs':inputs,'fixture_cap_minutes':45,'capture_cap_minutes':30,'jobs':[{'id':j['id'],'name':j['name'],'status':j['status'],'conclusion':j['conclusion']} for j in jobs['jobs']],'old_failed_runs_retained':[43000644195,43018920928,43053758545],'release':False,'install':False,'native_fit_accepted':False,'production':False,'automatic_retry':False}
save('REGISTERED.json',registered);print(json.dumps(registered),flush=True)
