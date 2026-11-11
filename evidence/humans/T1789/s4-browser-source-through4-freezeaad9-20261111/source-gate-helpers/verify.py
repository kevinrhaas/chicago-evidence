from pathlib import Path
import hashlib,json,runpy
P=Path(__file__).resolve().parent;AP=Path('/tmp/ROOT-T1789-S4-PW-DOCKER-APPLY-PREP-20261111')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=(P/'FREEZE.json').read_bytes();pin=hashlib.sha256(raw).hexdigest();d=json.loads(raw)
assert Path(d['apply_cell'])==AP/'cell.py' and sha(AP/'cell.py')==d['apply_cell_SHA256']
c=runpy.run_path(str(AP/'cell.py'),run_name='s4_apply_definitions_only')
assert c['HEAD']=='0a57979840bea7c37ba41ba4e24133a9510b59b9' and c['BASE_SHA']=='6944115f9392d917e16bcc4fe0c1adf490bc58ec64373b09d25467118084fa41'
assert c['EXPECTED']=={'.github/workflows/chicago-4d-humans.yml','chicago/4d/docs/STATUS.md','chicago/4d/docs/ROADMAP.md'}
assert pin==json.loads((P/'READY.json').read_bytes())['freeze_SHA256'] and d['head']==c['HEAD'] and d['parts']==16 and d['CHECK_JOBS']==4 and d['deleted_paths']==[] and d['incoming_dev'] is None
assert len(d['rows'])==d['frozen_file_count']==301 and set(d['expected_staged_paths'])==c['EXPECTED']
assert sha(Path(d['apply_receipt']))==d['apply_receipt_SHA256'] and sha(Path(d['apply_closed']))==d['apply_closed_SHA256']
after={r['file']:r for r in d['rows'] if r['file'] in c['EXPECTED']};rows=c['verify'](after)
assert rows==d['rows'] and c['git']('write-tree')==d['index_tree']
assert sha(Path(d['wrapper']))==d['wrapper_SHA256'] and c['NATIVE']<=set(d['protected_native_and_fixture_paths'])
print('S4_SOURCE_VERIFIED '+pin+' native8_fixture_primary_ref_unchanged parts16')
