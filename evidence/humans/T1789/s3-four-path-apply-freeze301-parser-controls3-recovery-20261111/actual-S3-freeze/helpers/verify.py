from pathlib import Path
import hashlib,json,runpy
P=Path(__file__).resolve().parent;AP=Path('/tmp/ROOT-T1789-S3-CODEC-PARSER-APPLY-PREP-20261111')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(AP/'cell.py')=='1c19a8fe2ceb98a52e1f7c2ae9da1214eec6b1535ac20a4bf6abb73e9f3064db'
c=runpy.run_path(str(AP/'cell.py'),run_name='s3_apply_definitions_only')
raw=(P/'FREEZE.json').read_bytes();pin=hashlib.sha256(raw).hexdigest();d=json.loads(raw)
assert pin==json.loads((P/'READY.json').read_bytes())['freeze_SHA256'] and d['head']==c['HEAD'] and d['parts']==16 and d['CHECK_JOBS']==4 and d['deleted_paths']==[] and d['incoming_dev'] is None
assert len(d['rows'])==d['frozen_file_count']==301 and set(d['expected_staged_paths'])==c['EXPECTED']
assert sha(Path(d['apply_receipt']))==d['apply_receipt_SHA256'] and sha(Path(d['apply_closed']))==d['apply_closed_SHA256']
after={r['file']:r for r in d['rows'] if r['file'] in c['EXPECTED']};rows=c['verify'](after)
assert rows==d['rows'] and c['git']('write-tree')==d['index_tree']
assert sha(Path(d['wrapper']))==d['wrapper_SHA256'] and c['NATIVE']<=set(d['protected_native_and_fixture_paths'])
print('S3_SOURCE_VERIFIED '+pin+' native8_fixture_primary_ref_unchanged parts16')
