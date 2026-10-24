from pathlib import Path
import contextlib,copy,hashlib,io,json,runpy,shutil
P=Path(__file__).resolve().parent;Q=P/'CANONICAL-INTAKE-PROPOSAL';N=Q/'new/chicago/4d'
A=Path('/workspace/chicago-waistcoat/chicago/4d');AUTH='assets/authored/transport/horse_standing/';DATA='data/transport/parked/standing-horse-planted/'
sha=lambda b:hashlib.sha256(b).hexdigest()
TARGET='d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914'
BASE='b479442cb03ac46eb13c19da15a79cdfaf28dbdf356b116f78de7ce7ecdc60be'
NEW='horse-sevket-v16-planted-standing-eye-uv-v1.glb';OLD='horse-sevket-v16-planted-standing-v1.glb'
R=P/'PORTABLE-GENERATOR-ACTUAL-ONCE'
assert sha((R/NEW).read_bytes())==TARGET
genreceipt=json.loads((R/'ACTUAL-RECEIPT.json').read_text());assert genreceipt['candidate_sha256']==TARGET
assert genreceipt['source_sha256']==sha((N/AUTH/'generate_eye_uv_v1.py').read_bytes())

# Run the proposed independent source test without modifying app/proposal inputs.
V=P/'PORTABLE-BOUNDARY-VALIDATION';assert not V.exists();V.mkdir()
for rel,source in [
 ('tools/test_standing_horse_eye_uv_boundary.py',N/'tools/test_standing_horse_eye_uv_boundary.py'),
 (AUTH+OLD,A/AUTH/OLD),
 ('renderers/web/transport/standing-horse/'+NEW,N/'renderers/web/transport/standing-horse'/NEW),
]:
 f=V/rel;f.parent.mkdir(parents=True,exist_ok=True)
 if rel.startswith('tools/'):shutil.copyfile(source,f)
 else:f.symlink_to(source)
captured=io.StringIO()
with contextlib.redirect_stdout(captured):runpy.run_path(str(V/'tools/test_standing_horse_eye_uv_boundary.py'),run_name='__main__')
boundary=json.loads(captured.getvalue());assert boundary['status']=='PASS_INDEPENDENT_UV_ONLY_CHANGE_BOUNDARY'
assert len(boundary['negative_controls'])==5 and all(x['rejected'] for x in boundary['negative_controls'])
(V/'ACTUAL.json').write_text(json.dumps(boundary,indent=2)+'\n')

# Explicit current-SHA verifier lineage, avoiding an ambiguous old-proof label.
summary_path=N/DATA/'eye-uv-v1-loaded129-summary.json';summary=json.loads(summary_path.read_text())
summary['protected_input_bridge_diff_sha256']=summary.pop('old_proof_sha256')
old=Path('/workspace/shared/T2800-1904-RESUME-20261023-2245/FRESH-CLONE129/proof.mjs')
summary['unchanged_physical_verifier_original_sha256']=sha(old.read_bytes())
summary['fresh_identity_bridge_proof_sha256']=sha((P/'D454-FRESH-CLONE129/proof.mjs').read_bytes())
summary['root_release_sha256']=sha((P/'D454-FRESH-CLONE129/ROOT-RELEASE.json').read_bytes())
summary_path.write_text(json.dumps(summary,indent=2)+'\n');qsha=sha(summary_path.read_bytes())
receipt_path=N/AUTH/'eye-uv-v1-derivation-receipt.json';receipt=json.loads(receipt_path.read_text())
receipt.update(loaded_qualification_sha256=qsha,portable_reproduction_actual_status=genreceipt['state'],portable_reproduction_candidate_sha256=genreceipt['candidate_sha256'],portable_reproduction_actual_receipt_sha256=sha((R/'ACTUAL-RECEIPT.json').read_bytes()),portable_boundary_actual_status=boundary['status'],portable_boundary_actual_sha256=sha((V/'ACTUAL.json').read_bytes()),portable_boundary_test_sha256=sha((N/'tools/test_standing_horse_eye_uv_boundary.py').read_bytes()))
receipt_path.write_text(json.dumps(receipt,indent=2)+'\n');rsha=sha(receipt_path.read_bytes())
(N/DATA/'eye-uv-v1-derivation-receipt.json').write_bytes(receipt_path.read_bytes())
for rel in ['data/transport/parked/horse-sevket-sidecar.json',AUTH+'SOURCE.json']:
 f=N/rel;j=json.loads(f.read_text());r=j['runtime_asset']if 'runtime_asset'in j else j['runtime_derivative'];r['eye_uv_derivation_receipt_sha256']=rsha
 if 'idle'in j:j['idle']['loaded_qualification_sha256']=qsha
 f.write_text(json.dumps(j,indent=2)+'\n')

original_idle=(A/'renderers/web/js/standing-horse-planted-idle.js').read_text()
new_idle=(N/'renderers/web/js/standing-horse-planted-idle.js').read_text()
assert new_idle.replace(TARGET,BASE).replace('3784176','3783600')==original_idle
original_contract=(A/'tools/test_planted_standing_horse_contract.mjs').read_text()
assert (N/'tools/test_planted_standing_horse_contract.mjs').read_text().replace(NEW,OLD)==original_contract
bs=json.loads((A/'data/transport/parked/horse-sevket-sidecar.json').read_text());cs=json.loads((N/'data/transport/parked/horse-sevket-sidecar.json').read_text())
for key in ['budget_proposal','contact_mesh','capabilities','source_inventory','runtime_scale_m_per_unit','runtime_origin_m','runtime_bounds_m']:
 assert bs[key]==cs[key],key
bm=json.loads((A/'data/transport/parked/standing-horses.json').read_text());cm=json.loads((N/'data/transport/parked/standing-horses.json').read_text());assert bm['scenes']==cm['scenes']
assert cs['idle']['actual_yard_native_visual_world_GPU_qualified']is False
assert cs['capabilities']['photographic_master_complete']is False
assert cs['idle']['historical_b479_qualification']['asset_sha256']==BASE
assert cs['idle']['loaded_qualification_sha256']==qsha
assert sha((N/'renderers/web/transport/standing-horse'/NEW).read_bytes())==TARGET
assert (N/'renderers/web/transport/standing-horse'/NEW).read_bytes()==(N/AUTH/NEW).read_bytes()
assert not (N/AUTH/OLD).exists()

inventory=[]
for f in sorted(N.rglob('*')):
 if not f.is_file():continue
 assert not f.is_symlink()
 rel=f.relative_to(N);old=A/rel
 inventory.append({'path':'chicago/4d/'+str(rel),'operation':'modify'if old.exists()else'add','preimage_sha256':sha(old.read_bytes())if old.exists()else None,'preimage_bytes':old.stat().st_size if old.exists()else None,'proposed_sha256':sha(f.read_bytes()),'proposed_bytes':f.stat().st_size})
(Q/'CHANGED-FILES.json').write_text(json.dumps(inventory,indent=2)+'\n')
readme=Q/'ROOT-INTEGRATION.md';s=readme.read_text();s=s.replace('Portable generator must be executed once to a fresh owned output and compared to d454 before this proposal is treated as ready.','Portable generator was executed once to fresh PORTABLE-GENERATOR-ACTUAL-ONCE and reproduced exact d454 in0.274seconds. Proposed independent boundary test was executed in an external source-only validation overlay and passed all five meaningful negative controls. No Node contract or app gates were executed for this proposal while root owns the gate lane.')
readme.write_text(s)
report={'status':'PORTABLE_INTAKE_SOURCE_AUDIT_PASS_ONLY','portable_generator_sha256':sha((N/AUTH/'generate_eye_uv_v1.py').read_bytes()),'portable_reproduced_sha256':TARGET,'portable_boundary_controls':boundary['negative_controls'],'runtime_module_identity_only_diff':True,'existing_contract_filename_only_diff':True,'all_existing_scene_rows_unchanged':True,'budgets_contacts_capabilities_scale_bounds_unchanged':True,'no_duplicate_original_glb':True,'historical_b479_results_unchanged':True,'new_summary_sha256':qsha,'derivation_receipt_sha256':rsha,'inventory_sha256':sha((Q/'CHANGED-FILES.json').read_bytes()),'app_modified':False,'native_or_photographic_acceptance':False,'full_gate_run':False,'changed_file_count':len(inventory)}
(Q/'ACTUAL-SOURCE-AUDIT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
