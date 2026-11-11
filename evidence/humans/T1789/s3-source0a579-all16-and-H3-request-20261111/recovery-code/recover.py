"""Fresh remote reconciliation; never retries the completed push or repairs its missing closure."""
from pathlib import Path
import argparse,hashlib,json,types
P=Path(__file__).resolve().parent
POST=Path('/tmp/ROOT-T1789-LINEN-S3-CHECKPOINT-POSTGATE-PREP-20261111')
S='0a57979840bea7c37ba41ba4e24133a9510b59b9'
OLD='c9990d8b32517612a94e339a98bd5700436b5689'
TREE='3229a20188497ff74d9d1af51d13b886cadb1315'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 assert p.is_file() and not p.is_symlink() and p.stat().st_size<=1048576,str(p)
 return json.loads(p.read_bytes())
def source_context(binding_sha):
 pins=load(P/'SOURCE-PINS.json')
 for n,h in pins.items():assert sha(P/n)==h,n
 I=load(P/'INPUTS.json');assert I['source']==S and I['tree']==TREE and I['parent']==OLD
 assert binding_sha==I['binding_SHA256']==sha(POST/'BINDING.json')
 assert sha(POST/'chain.py')==I['postgate_chain_SHA256']=='b2340e11d629185d231042819c9e7f967fedcd1a10674173a5355bd1a1b613d6'
 assert sha(POST/'SOURCE-PINS.json')==I['postgate_source_pins_SHA256']
 for n,h in load(POST/'SOURCE-PINS.json').items():assert sha(POST/n)==h,n
 for n,r in I['original_files'].items():
  q=Path(r['path']);assert q==POST/n and q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],n
 for n in I['must_remain_missing']:assert not (POST/n).exists(),'Original interrupted proof changed; review rather than overwrite'
 B=load(POST/'BINDING.json');assert B['source_checkpoint_only'] and B['needs_final_DEV_integration'] and not B['merge_ready']
 library=types.ModuleType('actual_s3_remote_reconciliation_library');library.__file__=str(POST/'chain.py')
 exec(compile((POST/'chain.py').read_bytes(),str(POST/'chain.py'),'exec'),library.__dict__)
 C=library.__dict__;C.update(B=B,BINDING_SHA=binding_sha,TREE=TREE,FREEZE_SHA=B['freeze_SHA256'])
 for n in ['qualified_gate','prior','verify_worktree','remote_phase']:assert C[n].__globals__ is C
 assert TREE==C['SOURCE_TREE'] and B['freeze_SHA256']==C['SOURCE_FREEZE_SHA'] and B['apply_receipt_SHA256']==C['SOURCE_APPLY_SHA']
 d,a=C['qualified_gate']();C['verify_worktree'](d,S,True)
 docs={n:C['prior'](n,n)for n in ['COMMIT','PREFLIGHT']}
 c,f=docs['COMMIT'],docs['PREFLIGHT'];assert c['head']==f['head']==S and c['tree']==f['tree']==TREE and c['parents']==[OLD]
 assert f['changelog_question'] and f['ID_collision_question']
 push=load(POST/'PUSH/PUSH-RECEIPT.json');attempt=load(POST/'PUSH/PUSH-ATTEMPT.json');hook=load(POST/'PUSH/ADVERTISED-EXPECTED-OLD.json')
 assert push['head']==attempt['head']==hook['head']==S and push['tree']==TREE and push['parents']==[OLD]
 assert push['remote_expected_before']==push['advertised_remote_oid']==attempt['remote_expected']==hook['remote_oid']==OLD
 assert attempt['destination']==hook['remote_ref']=='refs/heads/'+C['BRANCH'] and push['branch']==C['BRANCH']
 assert push['force'] is False and attempt['force'] is False and hook['force'] is False and hook['normal_expected_old_fast_forward']
 assert hook['existing_hook_returncode']==(0 if hook['existing_hook'] else None)
 assert all(v['source_checkpoint_only'] and v['needs_final_DEV_integration'] and not v['merge_ready'] for v in [c,f,push])
 assert push['binding_SHA256']==binding_sha and not push['DEV_push_or_merge'] and not push['production']
 assert push['preflight']['changelog_question'] and push['preflight']['ID_collision_question']
 assert push['preflight']['head']==S and push['preflight']['tree']==TREE
 assert C['remote_head'](C['BRANCH'])==S
 docs['PUSH']=push
 proof=dict(original_accepted_phases=['COMMIT','PREFLIGHT'],original_PUSH_status='INTERRUPTED_WITH_COMPLETE_PUSH_RECEIPT_BUT_NO_SUPERVISOR_CLOSURE',original_PUSH_supervised_returncode=None,original_PUSH_cleanup_complete=None,original_PUSH_closure_accepted=False,original_missing_paths=I['must_remain_missing'],original_file_SHA256={n:r['sha256']for n,r in I['original_files'].items()},source=S,tree=TREE,parents=[OLD],binding_SHA256=binding_sha,all16_actual_source_parts_verified=True,source301_native8_fixture_protected9453_verified_now=True,push_retried=False,source_checkpoint_only=True,needs_final_DEV_integration=True,merge_ready=False)
 return C,d,a,docs,proof

def main(binding_sha):
 assert not any((P/n).exists()for n in ['RECONCILIATION-RECEIPT.json','REMOTE-VERIFY']),'One fresh reconciliation only'
 C,d,a,docs,proof=source_context(binding_sha)
 # This explicit prior is a reconciliation input, never a fabricated PUSH/CLOSED.
 def reconciled_prior(phase,name):
  assert (phase,name) in [('COMMIT','COMMIT'),('PUSH','PUSH')]
  return docs[phase]
 C['prior']=reconciled_prior;C['P']=P
 (P/'REMOTE-VERIFY').mkdir()
 C['remote_phase'](d,a)
 remote=P/'REMOTE-VERIFY/REMOTE-RECEIPT.json';r=load(remote)
 assert r['head']==S and r['tree']==TREE and r['parents']==[OLD] and r['all301_local_frozen_SHA256_bytes_modes_preserved']
 assert len(r['remote_changed_entries'])==4 and sum(x['remote_body_verified']for x in r['remote_changed_entries'])==2
 C['verify_worktree'](d,S,True)
 for n in proof['original_missing_paths']:assert not (POST/n).exists()
 proof.update(status='FRESH_S3_REMOTE_RECONCILIATION_COMPLETE_NOT_ORIGINAL_PUSH_CLOSURE',remote_proof=str(remote),remote_proof_SHA256=sha(remote),remote_feature_verified=S,remote_four_entries_two_source_bodies_verified=True,DEV_merge=False,production=False,native_fit_accepted=False)
 (P/'RECONCILIATION-RECEIPT.json').write_text(json.dumps(proof,indent=2)+'\n')
 print(json.dumps(proof))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--binding-sha256',required=True);args=parser.parse_args();main(args.binding_sha256)
