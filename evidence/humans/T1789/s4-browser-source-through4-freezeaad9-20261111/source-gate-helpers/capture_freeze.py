"""Capture actual S4 three-path staged source, never a guessed tree."""
from pathlib import Path
import argparse,hashlib,json,runpy
P=Path(__file__).resolve().parent
AP=Path('/tmp/ROOT-T1789-S4-PW-DOCKER-APPLY-PREP-20261111')
EXPECTED={'.github/workflows/chicago-4d-humans.yml','chicago/4d/docs/STATUS.md','chicago/4d/docs/ROADMAP.md'}
BASE_SHA='6944115f9392d917e16bcc4fe0c1adf490bc58ec64373b09d25467118084fa41'
HEAD='0a57979840bea7c37ba41ba4e24133a9510b59b9'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--apply-cell-sha256',required=True);parser.add_argument('--apply-receipt-sha256',required=True);parser.add_argument('--apply-closed-sha256',required=True);a=parser.parse_args()
 assert not any((P/n).exists() for n in ['FREEZE.json','READY.json'])
 assert sha(AP/'cell.py')==a.apply_cell_sha256
 c=runpy.run_path(str(AP/'cell.py'),run_name='s4_apply_definitions_only')
 assert c['HEAD']==HEAD and c['BASE_SHA']==BASE_SHA and c['EXPECTED']==EXPECTED
 closed_path=AP/'CLOSED.json';assert sha(closed_path)==a.apply_closed_sha256;closed=json.loads(closed_path.read_bytes());r,k,g=closed['result'],closed['cleanup'],closed['resources']
 assert closed['accepted'] and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None and k['cleanup_complete'] and not k['remaining_owned_children'] and g['accepted']
 receipt=AP/'APPLY-RECEIPT.json';assert sha(receipt)==closed['receipt_SHA256']==a.apply_receipt_sha256;ap=json.loads(receipt.read_bytes())
 assert ap['head']==c['HEAD'] and ap['baseline301_SHA256']==c['BASE_SHA'] and set(ap['staged_paths'])==c['EXPECTED'] and ap['deleted_paths']==[] and ap['native8_and_fixture_unchanged'] and ap['primary_ref_unchanged'] and ap['controls']['actual_existing_workflow_checks_PASS']
 ad=c['admission'](Path(ap['admission']),ap['admission_SHA256']);after={r['file']:r for r in ap['rows']};assert set(after)==c['EXPECTED']
 rows=c['verify'](after);base=c['baseline']();tree=c['git']('write-tree');assert tree==ap['index_tree']
 protected=set(base['protected_native_and_fixture_paths']);assert c['NATIVE']<=protected and not protected&c['EXPECTED']
 wrapper=Path(base['wrapper']);assert sha(wrapper)==base['wrapper_SHA256']
 freeze=dict(status='S4_REVIEWED_SOURCE_FIXES_GATE_PENDING',head=c['HEAD'],incoming_dev=None,index_tree=tree,branch=c['BRANCH'],root=str(c['ROOT']),protected_ref=c['PROTECTED'],protected_ref_head=c['PRIMARY'],wrapper=str(wrapper),wrapper_SHA256=base['wrapper_SHA256'],frozen_file_count=len(rows),rows=rows,expected_staged_paths=sorted(c['EXPECTED']),deleted_paths=[],baseline301_SHA256=c['BASE_SHA'],baseline_preserved_except_explicit_staged_paths=True,old_source_exceptions=sorted(c['EXPECTED']),protected_native_and_fixture_paths=sorted(protected),old_native8_and_current_fixture_byte_exact=True,native_asset_adoption=False,no_new_native_changelog_entry=True,apply_cell=str(AP/'cell.py'),apply_cell_SHA256=a.apply_cell_sha256,apply_receipt=str(receipt),apply_receipt_SHA256=sha(receipt),apply_closed=str(closed_path),apply_closed_SHA256=sha(closed_path),admission=ap['admission'],admission_SHA256=ap['admission_SHA256'],parts=16,CHECK_JOBS=4,failed_prior_capture_runs=[43000644195,43018920928,43053758545],source_gate='PENDING_ALL16',future_S4_H4_run='UNKNOWN_UNTIL_ACTUAL_NEW_COMMIT_AND_REVIEW',native_bake_fixture_pose_photo='PENDING',commit=False,push=False)
 assert len(rows)==301
 (P/'FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n');pin=sha(P/'FREEZE.json');(P/'READY.json').write_text(json.dumps(dict(freeze_SHA256=pin,index_tree=tree,frozen_file_count=301,parts=16,CHECK_JOBS=4),indent=2)+'\n');print(json.dumps(dict(freeze_SHA256=pin,index_tree=tree,files=301,parts=16,CHECK_JOBS=4)))
