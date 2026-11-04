"""Generic exact final committed checkpoint observer; no older world PASS transfer."""
from pathlib import Path
import argparse,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys
P=Path(__file__).resolve().parent;RUNTIME=P.parents[1]
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
FIELDS=['HEAD','TREE','APP','semantic_index_sha256']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'),timeout=30)
def val(repo,*args):return git(repo,*args).decode().strip()
def reference(ref):
 assert set(ref)=={'path','sha256'}and re.fullmatch('[a-f0-9]{64}',ref['sha256'])
 assert sha(ref['path'])==ref['sha256'];return load(ref['path'])
def index_map(repo,tree):
 rows=[]
 for row in git(repo,'ls-tree','-r','-z',tree).split(b'\0'):
  if row:
   info,path=row.split(b'\t',1);mode,kind,oid=info.split();rows.append((path,mode+b' '+oid+b' 0\t'+path+b'\0'))
 return b''.join(record for path,record in sorted(rows))
def metadata(repo,head):
 assert re.fullmatch('[a-f0-9]{40}',head)
 tree=val(repo,'rev-parse',head+'^{tree}')
 return dict(HEAD=head,TREE=tree,APP=val(repo,'rev-parse',head+':chicago/4d'),semantic_index_sha256=hashlib.sha256(index_map(repo,tree)).hexdigest())
def committed_source(repo,expected):
 assert set(expected)==set(FIELDS)
 for k in ['HEAD','TREE','APP']:assert re.fullmatch('[a-f0-9]{40}',expected[k])
 assert re.fullmatch('[a-f0-9]{64}',expected['semantic_index_sha256'])
 assert not git(repo,'ls-files','-u').strip()and not git(repo,'diff','--name-only').strip(),'No unmerged/unstaged source permitted'
 assert not git(repo,'ls-files','--others','--exclude-standard').strip(),'Unexpected untracked source'
 merge_path=Path(val(repo,'rev-parse','--git-path','MERGE_HEAD'))
 if not merge_path.is_absolute():merge_path=repo/merge_path
 assert not merge_path.exists(),'An actual committed checkpoint is required'
 assert val(repo,'rev-parse','HEAD')==expected['HEAD']and metadata(repo,expected['HEAD'])==expected
 assert git(repo,'ls-files','--stage','-z')==index_map(repo,expected['TREE']),'Index must equal exact approved committed tree'
 return dict(expected)
def valid_native(row,cap=None,expected_code=0):
 r=row['result'];c=row['cleanup'];assert r['returncode']==expected_code and not r['timed_out']and r['timeout_override_reason']is None
 assert r['requested_timeout_seconds']==r['effective_timeout_seconds']
 if cap is not None:assert r['effective_timeout_seconds']==cap
 assert c['cleanup_complete']and not c['remaining_owned_children']and row['resources']['accepted']
POSITIVE_CHECKPOINTS={'ACTUAL_NATIVE_CURRENT_DEV_CHECKPOINT_NORMAL_PUSH_PASS_FULL_GATE_WORLD_PENDING','ACTUAL_REVIEWED_CI_FIX_QA_PUBLISH_PUSH_PASS_FULL_GATE_WORLD_PENDING','ACTUAL_SINGLE_REVIEWED_DEV_CHECKPOINT_PASS_FULL_GATE_WORLD_PENDING'}
def qa_rows(doc,receipt_path):
 base=doc['qa_base_SHA'];assert re.fullmatch('[a-f0-9]{40}',base)
 expected=[('entry',['node','tools/check-changelog-entry.mjs',base,'HEAD']),('identifiers',['node','tools/resolve_id_collisions.mjs','--base',base,'--check']),('changelog',['node','tools/check-changelog.mjs']),('pending-entry',['node','tools/changelog-entries.mjs','--check']),('history',['node','tools/changelog-history.mjs','--base',base])]
 for suffix,command in expected:
  labels={'final-HEAD-'+suffix,'HEAD-'+suffix};rows=[r for r in doc['ledger']if r.get('label',r.get('name'))in labels and r['result']['command']==command];assert len(rows)==1
  row=rows[0];valid_native(row,120);label=row.get('label',row.get('name'));assert sha(row.get('log',str(Path(receipt_path).parent/(label+'.log'))))==row['log_sha256']
 push=['git','push','origin','HEAD:refs/heads/steward/t3088-horse-photoquality-20261026'];rows=[r for r in doc['ledger']if r['result']['command']==push];assert len(rows)==1;valid_native(rows[0],120)
def publication_proof(ref,source,chain_ref):
 pub=reference(ref);assert pub['status']=='ACTUAL_NATIVE_CURRENT_DEV_PUBLICATION_PASS_NOT_FULL_GATE'
 assert pub['source_before']==pub['source_after']==source and pub['parent_chain_receipt']==chain_ref and pub['resources']['accepted']
 assert pub['native_build_stamp_exact_committed_HEAD']==source['HEAD'][:10]and len(pub['ledger'])==2
 for row,command,cap in zip(pub['ledger'],[['bash','tools/publish.sh'],['node','tools/check_published.mjs']],[180,120]):valid_native(row,cap);assert row['result']['command']==command
 return dict(path=ref['path'],sha256=ref['sha256'],source=source,native_build_stamp_exact_committed_HEAD=pub['native_build_stamp_exact_committed_HEAD'])
def prior_checkpoint(ref,repo,seen=None):
 seen=set()if seen is None else seen;identity=(ref['path'],ref['sha256']);assert identity not in seen;seen.add(identity)
 doc=reference(ref);assert doc['status']in POSITIVE_CHECKPOINTS
 assert doc['normal_push_verified']and doc['push_command_succeeded']and doc['Git_remote_readback_verified']and doc['source_guard_verified']and doc['all_five_HEAD_QA_PASS']
 assert doc['error']is None and doc['source_error']is None and metadata(repo,doc['source']['HEAD'])==doc['source']
 assert val(repo,'show','-s','--format=%P',doc['source']['HEAD']).split()==doc['parents']
 qa_rows(doc,ref['path']);publication_proof(doc['publication_receipt'],doc['source'],doc['parent_chain_receipt'])
 chain=reference(doc['parent_chain_receipt']);assert chain['final_commit']==doc['source']['HEAD']and chain['final_source']==doc['source']and chain['final_parents']==doc['parents']
 proofs=[]
 previous=doc.get('prior_checkpoint_receipt')or doc.get('parent_checkpoint_receipt')
 if previous:
  prior,nodes=prior_checkpoint(previous,repo,seen);assert doc['parents'][0]==prior['source']['HEAD'];proofs.extend(nodes)
 # A sealed positive integration receipt is the admission anchor. Its recorded
 # source/parents/QA/publication are checked; historical owner graphs/worlds are
 # neither replayed nor promoted to the new source.
 proofs.append(dict(path=ref['path'],sha256=ref['sha256'],status=doc['status'],source=doc['source'],parents=doc['parents'],actual_QA_push_publication_verified=True,prior_world_PASS_transferred=False))
 return doc,proofs
def owner_proof(binding,repo,source):
 c=reference(binding['checkpoint_receipt']);o=reference(binding['targeted_owner_receipt']);pins=reference(binding['owned17_pin_receipt'])['files']
 assert len(pins)==17 and o['status']=='TARGETED_FIXTURES_AND_NATIVE_OWNERS_PASS_NOT_FULL_PREFLIGHT'and o['resources']['accepted']
 assert o['fix_pins']==pins and o['native_tail_fixedpoint_PASS_claimed']is False
 staged=o['source_after'];assert set(staged)=={'HEAD','MERGE_HEAD','TREE','APP','semantic_index_sha256'}
 assert staged['HEAD']==binding['expected_prior_HEAD']and staged['MERGE_HEAD']==binding['expected_incoming_SHA']
 assert all(staged[k]==source[k]for k in ['TREE','APP','semantic_index_sha256'])and c['source_before']==staged
 expected=[(['python3','tools/compile_liberties.py'],120),(['python3','tools/compile_source_use.py'],120),(['node','tools/test_transport_loop.mjs'],5),(['node','tools/test_driven_assembly.mjs'],5),(['node','tools/test_navigator.mjs'],5),(['node','tools/test_parked_transport_empty_scene.mjs','--self-test'],120),(['bash','tools/test_check_harness.sh'],120),(['node','--check','renderers/web/js/main.js'],5),(['python3','tools/bake_warranted.py','--self-test'],120),(['python3','tools/compile_liberties.py','--check'],120),(['python3','tools/compile_source_use.py','--check'],120),(['python3','tools/validate.py','--all'],120),(['python3','tools/check_structure_clearance.py'],120)]
 assert len(o['ledger'])==len(expected)
 for row,(command,cap)in zip(o['ledger'],expected):valid_native(row,cap);assert row['result']['command']==command
 for rel,pin in pins.items():
  assert sha(repo/rel)==pin and hashlib.sha256(git(repo,'show',staged['HEAD']+':'+rel)).hexdigest()==pin
  assert git(repo,'ls-tree',staged['HEAD'],'--',rel)==git(repo,'ls-tree',source['HEAD'],'--',rel),'Owned17 mode/blob changed during integration'
 return dict(path=binding['targeted_owner_receipt']['path'],sha256=binding['targeted_owner_receipt']['sha256'],source_after=staged,committed_source=source,owned17_pin_receipt=binding['owned17_pin_receipt'],owned17_bytes_and_modes_exact=True,all13_current_native_commands_PASS=True,not_full_preflight=True,prior_world_PASS_transferred=False)
def checkpoint_bridge(binding,repo,source):
 c=reference(binding['checkpoint_receipt']);assert c['status']=='ACTUAL_SINGLE_REVIEWED_DEV_CHECKPOINT_PASS_FULL_GATE_WORLD_PENDING'
 assert c['source']==source and c['normal_push_verified']and c['push_command_succeeded']and c['Git_remote_readback_verified']and c['source_guard_verified']and c['all_five_HEAD_QA_PASS']
 assert c['error']is None and c['source_error']is None and c['full_native_gate_pending']is True and c['current_source_world_interaction_status']=='PENDING'and not c['CI_green_claimed']and not c['DEV_merged']
 for key in ['prior_checkpoint_receipt','parent_chain_receipt','owned17_pin_receipt']:assert c[key]==binding[key]
 assert c['native_owner_receipt']==binding['targeted_owner_receipt']
 prior,prior_proofs=prior_checkpoint(binding['prior_checkpoint_receipt'],repo)
 assert prior['source']['HEAD']==binding['expected_prior_HEAD']
 parents=[binding['expected_prior_HEAD'],binding['expected_incoming_SHA']]
 for head in parents:assert re.fullmatch('[a-f0-9]{40}',head)
 assert c['parents']==parents==val(repo,'show','-s','--format=%P',source['HEAD']).split()and c['qa_base_SHA']==parents[1]
 owner=owner_proof(binding,repo,source);chain=reference(binding['parent_chain_receipt'])
 assert chain['prior_checkpoint_receipt']==binding['prior_checkpoint_receipt']and chain['final_commit']==source['HEAD']and chain['final_parents']==parents and chain['final_source']==source
 assert chain['owner_staged_source']==owner['source_after']and chain['native_owner_receipt']==binding['targeted_owner_receipt']and chain['owned17_pin_receipt']==binding['owned17_pin_receipt']
 assert chain['prior_source']==prior['source']and chain['prior_chain_receipt']==prior['parent_chain_receipt']and chain['owned17_anchor']==parents[0]and chain['incoming_SHA']==parents[1]
 qa_rows(c,binding['checkpoint_receipt']['path']);assert all(sha(path)==h for path,h in c['execution_pins'].items())
 rows=[r for r in c['ledger']if r['result']['command']==['python3','tools/validate.py','--all']];assert len(rows)==1;valid_native(rows[0],120)
 rows=[r for r in c['ledger']if r.get('label',r.get('name'))=='final-HEAD-whitespace'];assert len(rows)==1;valid_native(rows[0],120);assert rows[0]['result']['command']==['git','show','--check','--format=oneline','HEAD']
 pub=publication_proof(c['publication_receipt'],source,binding['parent_chain_receipt'])
 return dict(path=binding['checkpoint_receipt']['path'],sha256=binding['checkpoint_receipt']['sha256'],source=source,parents=parents,prior_checkpoint_admissions=prior_proofs,current_native_owner=owner,all_five_final_HEAD_QA_PASS=True,normal_push_verified=True,current_source_world_pending=True,prior_world_PASS_transferred=False,initial_current_source_publication=pub)
def targeted_owner(binding,repo,source):return owner_proof(binding,repo,source)
def prepare_guard(binding):
 assert not binding['template_only']and binding['mode']=='CHECKPOINT_COMMITTED_DIAGNOSTIC_FULL_PREFLIGHT_PENDING'
 for f in [SUP,RUNTIME/'resource_guard.py',RUNTIME/'RESTORED-RUNTIME-BASELINE.json']:assert sha(f)==binding['guard_pins'][str(f)]
 lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('current_committed_world_guard',RUNTIME/'resource_guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
 return lock,guard

def main():
 p=argparse.ArgumentParser();p.add_argument('--binding',type=Path,required=True);p.add_argument('--year',choices=['1835','1904'],required=True);p.add_argument('--viewport',choices=['desktop','mobile'],required=True);p.add_argument('--scope',choices=['A','B','C'],required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();b=load(a.binding)
 assert b['ROOT_EXPLICIT_CHECKPOINT_WORLD_SCOPE_GO']is True;R=Path(b['repo']);A=R/'chicago/4d';site=R/'site/4d';O=a.out;assert not O.exists();lock,guard=prepare_guard(b)
 before=committed_source(R,b['source']);checkpoint=checkpoint_bridge(b,R,before);owner=targeted_owner(b,R,before)
 pr=b['publication_receipt'];assert sha(pr['path'])==pr['sha256'];pub=load(pr['path']);assert pub['status']=='ACTUAL_NATIVE_CURRENT_DEV_PUBLICATION_PASS_NOT_FULL_GATE'
 assert pub['source_before']==pub['source_after']==before and pub['parent_chain_receipt']==b['parent_chain_receipt']and pub['resources']['accepted']and len(pub['ledger'])==2
 for row,cmd,cap in zip(pub['ledger'],[['bash','tools/publish.sh'],['node','tools/check_published.mjs']],[180,120]):valid_native(row,cap);assert row['result']['command']==cmd
 stamp=load(site/'build.json')['version'];assert stamp==before['HEAD'][:10],'Native published build must stamp the actual new committed HEAD'
 rb=guard.snapshot();assert guard.check(rb)['accepted'];O.mkdir(parents=True)
 pins={str(p):sha(p)for p in (A/'renderers/web/js').rglob('*.js')}
 for folder in ['data/transport','assets/humans']:
  for f in (A/folder).rglob('*'):
   if f.is_file()and f.suffix in['.json','.glb']:pins[str(f)]=sha(f)
 for rel in ['renderers/web/index.html','renderers/web/css/walk.css','data/humans/fixture.measure.json','data/sidecars/'+a.year+'/index.json','data/sidecars/'+a.year+'/people.json','data/liberties.json','renderers/web/transport/driven/horse-current26-inplace-full.glb','renderers/web/transport/wagon-driver/wagon-w01.glb','renderers/web/transport/parked-brougham/brougham-near.glb']:pins[str(A/rel)]=sha(A/rel)
 helpers={f.name:sha(f)for f in P.iterdir()if f.suffix in['.py','.cjs']}
 cfg=dict(template_only=False,root_explicit_world_interaction_GO=True,root=str(site),output=str(O/'frames'),scene=a.year,tree='published',touch=a.viewport=='mobile',scope=a.scope,check_light=a.scope=='C',recheck_whole_route=a.scope=='A',actual_route_probe=str(P/'probe-native-world-route.cjs'),actual_source_HEAD_or_staged_TREE=before,actual_source_pins=pins,boot_ready_ms=240000,mount_ready_ms=300000,native_phase_seconds=600,native_image_sharpness='Low (1)',native_stored_boot_detail='balanced'if a.viewport=='mobile'else'full',harness_pins=helpers,diagnostic_mode=b['mode'],native_build_stamp_exact_committed_HEAD=stamp,delivery_acceptance=False)
 save(O/'ROOT-BOUND-WORLD-CONFIG.json',cfg);save(O/'SOURCE-BEFORE.json',before)
 env=dict(os.environ,PW_EXECUTABLE='/workspace/.cloud-setup/transport-browser141-20261103/chromium_headless_shell-1194/chrome-linux/headless_shell',PLAYWRIGHT_BROWSERS_PATH='/workspace/.cloud-setup/transport-browser141-20261103',PYTHONDONTWRITEBYTECODE='1');prefix=O/'world';result={};cleanup={};report={};error=None
 try:
  q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(P),'--timeout','600','--','node',str(P/'observe-one-world-case.cjs'),str(O/'ROOT-BOUND-WORLD-CONFIG.json')],env=env,stdout=(O/'world.stdout').open('xb'),stderr=subprocess.STDOUT)
  result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');rp=O/'frames/WORLD-CASE-RESULT.json';report=load(rp)if rp.exists()else{}
  passed=q.returncode==result['returncode']==0 and not result['timed_out']and result['requested_timeout_seconds']==result['effective_timeout_seconds']==600 and result['timeout_override_reason']is None and cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and report.get('status')=='ACTUAL_WORLD_INTERACTION_SCOPE_PASS'and report.get('probe',{}).get('scope')==a.scope
 except BaseException as ex:passed=False;error=repr(ex)
 after=committed_source(R,b['source']);resources=guard.pair(rb,guard.snapshot());passed=passed and before==after and resources['accepted']and all(sha(P/name)==digest for name,digest in helpers.items())
 closed=dict(status='ACTUAL_CHECKPOINT_PUBLISHED_SCOPE_PASS_FULL_PREFLIGHT_PENDING'if passed else'ACTUAL_CHECKPOINT_PUBLISHED_SCOPE_NONPASS_FULL_PREFLIGHT_PENDING',mode=b['mode'],scene=a.year,viewport=a.viewport,scope=a.scope,predicate_ids=report.get('probe',{}).get('predicate_ids',[]),source_before=before,source_after=after,targeted_owner_APP_bridge=owner,checkpoint_commit_bridge=checkpoint,publication_receipt=pr,native_build_stamp_exact_committed_HEAD=stamp,harness_pins=helpers,result=result,cleanup=cleanup,resources=resources,native_report=str(O/'frames/WORLD-CASE-RESULT.json'),failure=error,full_all4_commit_CI_DEV_delivery_or_photo_qualification=False)
 save(O/'CLOSED.json',closed);print(json.dumps({'status':closed['status'],'receipt':str(O/'CLOSED.json')}));raise SystemExit(0 if passed else 1)

