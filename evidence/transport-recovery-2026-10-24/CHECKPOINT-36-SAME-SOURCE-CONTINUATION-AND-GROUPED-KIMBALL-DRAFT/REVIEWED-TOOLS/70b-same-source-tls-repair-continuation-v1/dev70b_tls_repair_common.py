"""Explicit same-H3 composite qualification; original NONPASS evidence is immutable."""
import importlib.util
import json
import os
from pathlib import Path
import re
import time
from collections import Counter

HERE = Path(__file__).resolve().parent
OLD_TOOLS = HERE.parent / '70b-transport-ui-matrix-preparation-v1'
spec = importlib.util.spec_from_file_location('unchanged_h3_matrix_contracts', OLD_TOOLS / 'dev70b_transport_ui_matrix_common.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
need, read, save, digest, value_hash = old.need, old.read, old.save, old.digest, old.value_hash
HEAD = '1b70cdbd85b18c124870d6274d2ffffd4ca5979b'
INDEX = '195237adc725ac313d1bce7befc622cad8c54650218648c69eb781142c13f359'
AUTH = HERE / 'ROOT-AUTHORIZATION.json'
AUTH_SHA = '7b3cd13f09074c59bb3fe5d32df092fc3bff8fc579534ca6b65efa6b738e576a'
ORIGINAL = old.LOG / '70b-transport-ui-matrix-run1'
RUN = old.LOG / '70b-transport-ui-matrix-tls-repair-continuation1'
DRIVER_PREFIX = old.LOG / '70b-tls-repair-continuation1-driver'
VERIFIER_PREFIX = old.LOG / '70b-tls-repair-continuation1-independent-verifier'
OUTER_PREFIX = old.LOG / '70b-tls-repair-continuation1-pipeline'
PROOF = old.LOG / '70b-tls-repair-continuation1-independent-proof.json'
PIPELINE_STATE = old.LOG / '70b-tls-repair-continuation1-pipeline-state.json'
MANIFEST = HERE / 'TOOLS-MANIFEST.json'
OLD_HASHES = {
 'dev70b_transport_ui_matrix_common.py': '6e42184a1f4f2bf6cbc3a3628d73c22460fe7c8ddcc10a37ce3a63187316276c',
 'dev70b_transport_ui_matrix_driver.py': 'd4033c207d33d211a3fa3b25e47e07e2209d6c83e017ed2f1ae092b418e012c7',
 'dev70b_transport_ui_matrix_verify.py': '19bdcbb2ab3bc53501221456ee16d47120b7791dd148f0084d6bb050c13c1a4f',
}

def closed(prefix, expected_returncode=0):
 r, c = read(str(prefix)+'.result.json'), read(str(prefix)+'.cleanup.json')
 need(r['returncode'] == expected_returncode and r['timed_out'] is False, 'Wrong actual outer outcome: '+str(prefix))
 need(c['cleanup_complete'] is True and c['remaining_owned_children'] == [], 'Owned cleanup incomplete: '+str(prefix))
 return {s: digest(str(prefix)+s) for s in ['.log', '.result.json', '.cleanup.json']}

def closed_driver(expected_manifest_sha):
 hashes=closed(DRIVER_PREFIX)
 r=read(str(DRIVER_PREFIX)+'.result.json')
 need(r['cwd']==str(old.APP) and r['command'][1:]==[str(HERE/'dev70b_tls_repair_driver.py'),'--execute-reviewed-continuation','--tools-sha256',expected_manifest_sha], 'Actual continuation driver command/cwd differs')
 need(r['requested_timeout_seconds']==43200 and r['effective_timeout_seconds']==43200, 'Actual continuation driver cap differs')
 return hashes

def tools(expected_manifest_sha):
 need(digest(MANIFEST) == expected_manifest_sha, 'Continuation tools manifest changed')
 m = read(MANIFEST)
 need(m['root_authorization_sha256'] == AUTH_SHA and digest(AUTH) == AUTH_SHA, 'Root authorization changed')
 for p, want in m['files'].items(): need(digest(p) == want, 'Continuation tool changed: '+p)
 for n, want in OLD_HASHES.items(): need(digest(OLD_TOOLS/n) == want, 'Original immutable validator changed')
 need(digest(old.SUPERVISOR) == old.SUPERVISOR_SHA, 'Owned supervisor changed')

def quiet():
 need(not old.busy_processes(), 'A browser/smoke/original driver survives or another heavy job started')
 for p in Path('/proc').iterdir():
  if not p.name.isdigit() or int(p.name) == os.getpid(): continue
  try:
   if (p/'stat').read_text().rsplit(')',1)[1].split()[0] == 'Z': continue
   names = [Path(x.decode(errors='replace')).name for x in (p/'cmdline').read_bytes().split(b'\0')[:5] if x]
   need('dev70b_tls_repair_driver.py' not in names, 'Another composite continuation driver is active')
  except (OSError, ValueError, IndexError): pass

def source(mh):
 snapshot, rows = old.source_snapshot(HEAD, mh)
 need(snapshot['index_sha256'] == INDEX, 'Physical primary index changed')
 return snapshot, rows

def checked_binding(prefix, suffix, mh, expected_sha):
 path = Path(str(prefix)+suffix)
 need(digest(path) == expected_sha, 'Per-leg binding changed: '+str(path))
 b = read(path)
 need(b['head'] == HEAD and b['tree'] == old.TREE and b['app_subtree'] == old.APP_TREE and b['accepted_base'] == old.BASE, 'Per-leg source identity differs')
 need(b['published_manifest_digest'] == mh and b['index_sha256'] == INDEX, 'Per-leg whole mirror or physical index differs')

def original_evidence(expected_manifest_sha):
 tools(expected_manifest_sha)
 a = read(AUTH)
 for f in a['preserved_files']:
  p = Path(f['path'])
  need(p.stat().st_size == f['bytes'] and digest(p) == f['sha256'], 'Preserved original/diagnostic evidence changed: '+str(p))
 for prefix in [old.LOG/'70b-transport-ui-matrix-run1-driver', old.LOG/'70b-transport-ui-browser-pipeline-attempt2']:
  closed(prefix, 1)
 state = read(ORIGINAL/'MATRIX-STATE.json')
 need(state['status'].startswith('STOPPED:') and len(state['completed']) == 8 and not state.get('active'), 'Original failure state differs')
 need(state['planned_legs'] == [list(x) for x in old.LEGS] and state['accepted_base'] == old.BASE, 'Original plan/base differs')
 need(state['config']['head'] == HEAD and state['tree'] == old.TREE and state['app_subtree'] == old.APP_TREE, 'Original source identity differs')
 prereq = old.prerequisites(state['config'])
 need(prereq == state['prerequisites'], 'Original prerequisite receipt chain changed')
 before = read(ORIGINAL/'PUBLISHED-MANIFEST-BEFORE.json')
 need(before == sorted(read(Path(state['config']['focused_output'])/'PUBLISHED-MANIFEST-AFTER.json'), key=lambda x:x['path']), 'Original/focused whole manifest differs')
 mh = value_hash(before)
 need(mh == prereq['focused']['published_manifest_digest'], 'Prerequisite mirror digest differs')
 need(state['initial_source']['index_sha256'] == INDEX, 'Original index identity differs')
 selected = []
 for saved, (v, stage) in zip(state['completed'][:7], old.LEGS[:7]):
  prefix = ORIGINAL/f'70b-transport-ui-matrix-{v}-{stage}'
  need(saved['prefix'] == str(prefix) and saved['outer_returncode'] == 0, 'Wrong reusable original leg')
  proof = old.validate_leg(prefix, v, stage)
  need(proof == saved['proof'], 'Reusable actual proof changed')
  for suffix, sha in saved['binding_hashes'].items(): checked_binding(prefix, suffix, mh, sha)
  need(set(saved['binding_hashes']) == {'.binding.before.json','.binding.after.json'}, 'Missing original binding')
  selected.append({**saved, 'origin':'sealed-original-same-H3'})
 failure = state['completed'][7]
 failed_prefix = ORIGINAL/'70b-transport-ui-matrix-mobile-14'
 need(failure == {'viewport':'mobile','stage':'14','prefix':str(failed_prefix),'outer_returncode':1,'proof':None}, 'Original failure selection differs')
 closed(failed_prefix, 1)
 fr = read(str(failed_prefix)+'.result.json')
 need(fr['command'] == old.child_command('mobile','14') and fr['cwd'] == str(old.APP), 'Failed original command differs')
 need(fr['requested_timeout_seconds'] == old.timeout_for('mobile','14') and fr['effective_timeout_seconds'] == old.timeout_for('mobile','14'), 'Failed original timeout differs')
 text = Path(str(failed_prefix)+'.log').read_text()
 fail_lines = re.findall(r'^\s*FAIL\s+.*$',text,re.M)
 need(len(fail_lines) == 1 and 'zero page errors' in fail_lines[0] and text.count('net::ERR_CERT_AUTHORITY_INVALID') == 4, 'Failure is not the specifically diagnosed TLS-only case')
 need(re.findall(r'^(\d+) passed, (\d+) failed\s*$',text,re.M) == [('139','1')], 'Original assertion outcome differs')
 expected_images = ['a18-gh-courtyard-watercolor-thumb.jpg','a18-rba-mf-glessner-f34-thumb.jpg','cgn-1800-glessner-1887-construction-copy-thumb.jpg','a18-gh-cornell-glessner-rear-c1887-thumb.jpg']
 need(all('https://kevinrhaas.github.io/chicago-images/prairie-1904/files/'+n in fail_lines[0] for n in expected_images), 'Original failed URLs differ')
 need('the suite body ran to completion' in text and not Path(str(failed_prefix)+'.binding.after.json').exists(), 'Original failed attempt provenance differs')
 failed_before = read(str(failed_prefix)+'.binding.before.json')
 need(failed_before['head'] == HEAD and failed_before['published_manifest_digest'] == mh and failed_before['index_sha256'] == INDEX, 'Original failed-leg starting source differs')
 diagnosis = old.LOG/'20261025-mobile14-runtime-network-diagnosis'
 closed(diagnosis/'permission-restored-browser-probe')
 probe = read(diagnosis/'permission-restored-browser-probe.json')
 need(probe['pass'] is True and probe['status'] == 200 and probe['errors'] == [] and probe['image'] == {'complete':True,'width':400,'height':218}, 'Actual normal-TLS repair probe not green')
 current, rows = source(mh)
 need(rows == before, 'Current entire mirror differs from original/focused')
 return state, prereq, before, selected, current

def verify_selected(run, expected_manifest_sha):
 need(Path(run).resolve() == RUN, 'Use the exact new continuation directory')
 original, prereq, before, sealed, current = original_evidence(expected_manifest_sha)
 s = read(RUN/'COMPOSITE-STATE.json')
 need(s['schema'] == 'chicago-h3-tls-repair-composite-state-v1' and s['tools_manifest_sha256'] == expected_manifest_sha, 'Composite schema/tools differ')
 need(s['head'] == HEAD and s['tree'] == old.TREE and s['app_subtree'] == old.APP_TREE and s['accepted_base'] == old.BASE, 'Composite source differs')
 need(s['zero_cross_source_results'] is True and s['reused_same_source_leg_count'] == 7 and s['new_required_leg_count'] == 17, 'Composite provenance differs')
 need(s['prerequisites'] == prereq and s['config'] == original['config'] and s['root_authorization_sha256'] == AUTH_SHA, 'Composite prerequisites/authorization differ')
 need(s['planned_legs'] == [list(x) for x in old.LEGS] and not s.get('active') and len(s['selected']) == 24, 'Incomplete/active composite')
 need(s['selected'][:7] == sealed, 'Sealed passing selection changed')
 expected_outcomes=[{k:x[k] for k in ['viewport','stage','prefix','outer_returncode']} for x in s['selected'][7:]]
 need(s.get('attempted_outcomes') == expected_outcomes and len(expected_outcomes) == 17, 'A new failed, extra, missing or unselected attempt exists')
 need(read(RUN/'PUBLISHED-MANIFEST-BEFORE.json') == before and read(RUN/'PUBLISHED-MANIFEST-AFTER.json') == before, 'Composite global manifests changed')
 mh = value_hash(before)
 coverage = {v:Counter() for v in ['mobile','desktop']}
 for i, (saved, (v, stage)) in enumerate(zip(s['selected'], old.LEGS)):
  need((saved['viewport'],saved['stage']) == (v,stage), 'Missing/duplicate/reordered stage')
  prefix = ORIGINAL/f'70b-transport-ui-matrix-{v}-{stage}' if i < 7 else RUN/f'70b-tls-repair-{v}-{stage}'
  need(saved['prefix'] == str(prefix) and saved['outer_returncode'] == 0, 'Wrong selected evidence prefix/outcome')
  need(saved['origin'] == ('sealed-original-same-H3' if i<7 else 'new-after-reviewed-TLS-environment-repair'), 'Wrong selected provenance')
  need(old.validate_leg(prefix,v,stage) == saved['proof'], 'Selected actual native proof changed')
  need(set(saved['binding_hashes']) == {'.binding.before.json','.binding.after.json'}, 'Missing selected source binding')
  for suffix, sha in saved['binding_hashes'].items(): checked_binding(prefix,suffix,mh,sha)
  coverage[v].update(old.parts(stage))
 need(all(c == Counter(range(1,16)) for c in coverage.values()), 'Coverage is not exactly1..15once per viewport')
 final, rows = source(mh)
 need(rows == before, 'Final complete current mirror differs')
 stable = {k:v for k,v in final.items() if k!='checked_unix'}
 return {'schema':'chicago-h3-tls-repair-composite-coverage-v1','result':'PASS','scope':'All24 required native leg executions passed on identical H3 and whole published mirror across two listed attempts. Original TLS-failed attempt remains NONPASS. No production/photo/native/gait acceptance implied.','head':HEAD,'tree':old.TREE,'app_subtree':old.APP_TREE,'accepted_base':old.BASE,'leg_count':24,'coverage':{v:dict(c) for v,c in coverage.items()},'zero_cross_source_results':True,'reused_same_source_leg_count':7,'new_passed_leg_count':17,'selected':s['selected'],'selected_sha256':value_hash(s['selected']),'original_failed_attempt':s['original_failed_attempt'],'root_authorization_sha256':AUTH_SHA,'tools_manifest_sha256':expected_manifest_sha,'prerequisites':prereq,'published_manifest_digest':mh,'published_manifest_before_sha256':digest(RUN/'PUBLISHED-MANIFEST-BEFORE.json'),'published_manifest_after_sha256':digest(RUN/'PUBLISHED-MANIFEST-AFTER.json'),'final_source_identity':stable,'actual_over600s_legs':[{'viewport':x['viewport'],'stage':x['stage'],'command_seconds':x['proof']['command_seconds']} for x in s['selected'] if not x['proof']['fits_foreground_budget']]}
