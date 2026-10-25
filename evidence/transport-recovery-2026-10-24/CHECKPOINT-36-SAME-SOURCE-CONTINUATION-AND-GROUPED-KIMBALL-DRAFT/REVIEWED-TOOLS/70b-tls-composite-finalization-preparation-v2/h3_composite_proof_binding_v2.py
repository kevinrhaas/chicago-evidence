#!/usr/bin/env python3
"""UNRUN: explicit JSON-normalized finalization and strict composite consumer binding.
No browser, gate, fetch, publish, trust change or merge is launched by this module.
Importing defines functions only. Actual verification uses immutable native checks.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
LOG = Path('/workspace/.cloud-setup/logs/transport-recovery')
HERE = Path(__file__).resolve().parent
FROZEN = LOG / '70b-same-source-tls-repair-continuation-v1'
TOOLS = FROZEN / 'TOOLS-MANIFEST.json'
TOOLS_SHA = '460d9f8bc8d3f31c76aef5c3fab2ef4ba231f1351239057322979868fdf1a112'
AUTH_SHA = '7b3cd13f09074c59bb3fe5d32df092fc3bff8fc579534ca6b65efa6b738e576a'
HEAD = '1b70cdbd85b18c124870d6274d2ffffd4ca5979b'
TREE = '9fa9511eabff9a0e42da32410edf09a8e3608889'
APP_TREE = 'da9f71f6749ebf52e09ad51f673a9e4debbf4478'
BASE = '70bcc4366a455a15f1e54e3edfce50c046c0ddce'
INDEX = '195237adc725ac313d1bce7befc622cad8c54650218648c69eb781142c13f359'
MODE = 'same-H3-TLS-environment-repair-composite'
SCHEMA = 'chicago-h3-tls-repair-consumer-binding-v2'
ENVELOPE_SCHEMA = 'chicago-h3-independent-tls-repair-composite-v2'
COVERAGE_SCHEMA = 'chicago-h3-tls-repair-composite-coverage-v1'
NEW_PROOF = LOG / '70b-tls-repair-json-normalized-independent-proof-v2.json'
NEW_VERIFIER_PREFIX = LOG / '70b-tls-repair-json-normalized-verifier-v2'
NEW_TAIL_PREFIX = LOG / '70b-tls-repair-json-normalized-finalization-v2'
NEW_TAIL_STATE = LOG / '70b-tls-repair-json-normalized-finalization-v2-state.json'
NEW_TOOLS = HERE / 'FINALIZATION-TOOLS-MANIFEST.json'
EXPECTED_FAILURE = 'RuntimeError: Independent re-read differs from closed internal composite proof'
TAIL_PASS = 'PASS: actual JSON-normalized independent verifier0/cleanup0; enclosing finalization outer must still close; DEV merge pending'
FROZEN_FILES = {
    FROZEN / 'dev70b_tls_repair_common.py': 'ac1b2bcb44577aee948b331cbf1868e571f6131a1a55117764e4aa63d36df714',
    FROZEN / 'dev70b_tls_repair_driver.py': '41e1c0c15fd2875e81420fdeedb9e2506818290fd8971da930e60d7cd0f14662',
    FROZEN / 'dev70b_tls_repair_verify.py': 'd40e7bbe97ad78e4c6ec84f582055df0a33551038a5b7a447de57f29d34070d2',
    FROZEN / 'dev70b_tls_repair_pipeline.py': '7b53996dfaab643380f7401cd0ebdd22ebea7a7a4337ed3ca50bcb4539adfe9b',
    FROZEN / 'ROOT-AUTHORIZATION.json': AUTH_SHA,
    LOG / 'onboarding-transport-bootstrap-audit-v2/probe-image-cdn-browser-final-guarded-v2.mjs': 'a5c33c7eb08b4e27950d67526935c6798daa741391c5d497e12f3adfa1f62244',
}


def need(value, message):
    if not value:
        raise RuntimeError(message)


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def reference(path):
    path = Path(path).resolve()
    return {'path': str(path), 'sha256': digest(path)}


def normalize_json_representation(value):
    # Preserve EVERY field/value. Only JSON's own representation (notably numeric
    # object keys becoming strings) is normalized; no time/metadata fields drop.
    return json.loads(json.dumps(value, allow_nan=False))


def verify_finalization_tools(expected_sha):
    need(re.fullmatch('[0-9a-f]{64}', str(expected_sha)) and digest(NEW_TOOLS) == expected_sha,
         'Exact reviewed finalization tools manifest SHA256 required')
    doc = read(NEW_TOOLS)
    expected_paths = {str(HERE / name) for name in [
        'h3_composite_proof_binding_v2.py', 'verify_h3_composite_json_normalized_v2.py',
        'finalize_h3_composite_after_v1_stop_v2.py']}
    need(doc.get('schema') == 'chicago-h3-json-normalized-finalization-tools-v2' and
         doc.get('frozen_composite_tools_sha256') == TOOLS_SHA and
         doc.get('root_authorization_sha256') == AUTH_SHA and
         isinstance(doc.get('files'), dict) and set(doc['files']) == expected_paths,
         'Finalization manifest must name exactly the reviewed three new helpers')
    for file, wanted in doc['files'].items():
        need(re.fullmatch('[0-9a-f]{64}', wanted) and digest(file) == wanted,
             'Reviewed finalization helper changed: ' + file)
    need(digest(TOOLS) == TOOLS_SHA, 'Frozen composite manifest changed')
    frozen = read(TOOLS)
    need(frozen.get('files') == {str(p): h for p, h in FROZEN_FILES.items()} and
         frozen.get('root_authorization_sha256') == AUTH_SHA, 'Frozen tool payload set differs')
    for file, wanted in FROZEN_FILES.items():
        need(digest(file) == wanted, 'Frozen composite payload changed: ' + str(file))


def _closed(prefix, script, tail, cap, expected_returncode=0):
    prefix = Path(prefix)
    result_file, cleanup_file = Path(str(prefix)+'.result.json'), Path(str(prefix)+'.cleanup.json')
    result, cleanup = read(result_file), read(cleanup_file)
    need(result.get('returncode') == expected_returncode and result.get('timed_out') is False,
         'Wrong actual supervised outcome: ' + str(prefix))
    need(cleanup.get('cleanup_complete') is True and cleanup.get('remaining_owned_children') == [],
         'Actual owned cleanup incomplete: ' + str(prefix))
    command = result.get('command', [])
    need(isinstance(command, list) and len(command) >= 2 and
         Path(command[0]).name in ['python', 'python3', 'python3.11'] and
         command[1:] == [str(script), *tail], 'Actual supervised command differs: ' + str(prefix))
    need(result.get('cwd') == '/workspace/chicago/chicago/4d' and
         result.get('requested_timeout_seconds') == cap and result.get('effective_timeout_seconds') == cap,
         'Actual supervised cwd/cap differs: ' + str(prefix))
    return {'prefix': str(prefix), 'actual_returncode': expected_returncode,
            'log': reference(str(prefix)+'.log'), 'result': reference(result_file), 'cleanup': reference(cleanup_file)}


def verify_expected_frozen_stop(finalization_tools_sha256):
    """Require real old failures and prove they are ONLY JSON representation mismatch.
    All24 native checks/current source/census are re-read unchanged before returning.
    """
    verify_finalization_tools(finalization_tools_sha256)
    spec = importlib.util.spec_from_file_location('frozen_h3_composite_contract', FROZEN/'dev70b_tls_repair_common.py')
    common = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common)
    common.quiet()
    common.tools(TOOLS_SHA)
    driver_hashes = common.closed_driver(TOOLS_SHA)
    driver = _closed(common.DRIVER_PREFIX, FROZEN/'dev70b_tls_repair_driver.py',
                     ['--execute-reviewed-continuation', '--tools-sha256', TOOLS_SHA], 43200)
    old_verifier = _closed(common.VERIFIER_PREFIX, FROZEN/'dev70b_tls_repair_verify.py',
                           ['--tools-sha256', TOOLS_SHA], 600, 1)
    old_pipeline = _closed(common.OUTER_PREFIX, FROZEN/'dev70b_tls_repair_pipeline.py',
                           ['--execute-reviewed-continuation', '--tools-sha256', TOOLS_SHA], 60000, 1)
    need(not common.PROOF.exists(), 'Original failed verifier must not supply a successful proof')
    old_log = Path(str(common.VERIFIER_PREFIX)+'.log').read_text()
    need(old_log.rstrip().endswith(EXPECTED_FAILURE) and
         re.findall(r'^RuntimeError:.*$', old_log, re.M) == [EXPECTED_FAILURE],
         'Frozen verifier failed for another reason; no generic ignore-red flag')
    old_state = read(common.PIPELINE_STATE)
    need(old_state.get('phase') == 'STOPPED: actual continuation failure preserved; no automatic retry' and
         old_state.get('head') == HEAD and old_state.get('run_dir') == str(common.RUN) and
         old_state.get('tools_manifest_sha256') == TOOLS_SHA and
         'returned non-zero exit status 1' in old_state.get('error', '') and
         str(common.VERIFIER_PREFIX) in old_state.get('error', ''),
         'Frozen pipeline did not record the actual expected verifier failure')
    internal_file = common.RUN/'INTERNAL-COMPOSITE-PROOF.json'
    internal = read(internal_file)
    raw = common.verify_selected(common.RUN, TOOLS_SHA)
    normalized = normalize_json_representation(raw)
    need(raw != internal and normalized == internal,
         'Re-read is not solely the expected lossless JSON representation mismatch')
    need(normalized.get('schema') == COVERAGE_SCHEMA and normalized.get('result') == 'PASS' and
         (normalized.get('head'), normalized.get('tree'), normalized.get('app_subtree'), normalized.get('accepted_base')) ==
         (HEAD, TREE, APP_TREE, BASE) and normalized.get('leg_count') == 24 and
         normalized.get('coverage') == {v: {str(i): 1 for i in range(1,16)} for v in ['mobile','desktop']} and
         normalized.get('zero_cross_source_results') is True and
         normalized.get('reused_same_source_leg_count') == 7 and normalized.get('new_passed_leg_count') == 17 and
         normalized.get('tools_manifest_sha256') == TOOLS_SHA and normalized.get('root_authorization_sha256') == AUTH_SHA,
         'Actual selected source/coverage/provenance differs')
    final = normalized.get('final_source_identity', {})
    need((final.get('head'), final.get('tree'), final.get('app_subtree'), final.get('accepted_base')) ==
         (HEAD, TREE, APP_TREE, BASE) and final.get('index_sha256') == INDEX and
         final.get('published_manifest_digest') == normalized.get('published_manifest_digest'),
         'Actual completed local source/index/entire mirror differs')
    expected_original = {'viewport':'mobile','stage':'14',
                         'prefix':str(common.ORIGINAL/'70b-transport-ui-matrix-mobile-14'),
                         'result':'NONPASS:139passed/1zero-page-errors TLSfailure',
                         'original_driver_returncode':1,'original_pipeline_returncode':1,
                         'original_cleanup_complete':True,'selected_for_coverage':False}
    need(normalized.get('original_failed_attempt') == expected_original,
         'Original functional TLS failure must remain NONPASS and unselected')
    state = read(common.RUN/'COMPOSITE-STATE.json')
    need(state.get('status') == 'PASS: composite24 native leg executions; original attempt remains NONPASS; independent verification pending' and
         state.get('internal_proof_sha256') == digest(internal_file), 'Closed driver state differs')
    stop = {'original_verifier':old_verifier,'original_pipeline':old_pipeline,
            'original_independent_proof_absent':True,'actual_expected_error':EXPECTED_FAILURE,
            'lossless_normalization':'json.loads(json.dumps(raw, allow_nan=False))',
            'no_fields_or_values_removed':True,'frozen_tools_manifest':reference(TOOLS),
            'original_pipeline_state':reference(common.PIPELINE_STATE)}
    return common, normalized, {'driver':driver,'driver_hashes':driver_hashes,
                                'frozen_serialization_stop':stop,'internal_proof':reference(internal_file)}


def verify_closed_composite(independent_proof, independent_sha256, finalization_tools_sha256):
    """Strict actual-v2 consumer API; return explicit typed composite, no legacy alias."""
    path = Path(independent_proof).resolve()
    need(path == NEW_PROOF and re.fullmatch('[0-9a-f]{64}', str(independent_sha256)) and
         digest(path) == independent_sha256, 'Actual named v2 independent envelope/full SHA required')
    envelope = read(path)
    need(envelope.get('schema') == ENVELOPE_SCHEMA and envelope.get('result') == 'PASS' and
         envelope.get('finalization_tools_manifest_sha256') == finalization_tools_sha256,
         'Actual v2 normalized independent envelope absent or wrong tools')
    common, coverage, evidence = verify_expected_frozen_stop(finalization_tools_sha256)
    verifier = _closed(NEW_VERIFIER_PREFIX, HERE/'verify_h3_composite_json_normalized_v2.py',
                       ['--v2-tools-sha256',finalization_tools_sha256],600)
    tail = _closed(NEW_TAIL_PREFIX, HERE/'finalize_h3_composite_after_v1_stop_v2.py',
                   ['--execute-reviewed-finalization','--v2-tools-sha256',finalization_tools_sha256],60000)
    state = read(NEW_TAIL_STATE)
    need(state.get('phase') == TAIL_PASS and state.get('head') == HEAD and
         state.get('tools_manifest_sha256') == finalization_tools_sha256 and
         state.get('independent_proof') == str(NEW_PROOF) and state.get('independent_proof_sha256') == independent_sha256 and
         state.get('verifier_prefix') == str(NEW_VERIFIER_PREFIX), 'Actual successful closed finalization tail state differs')
    need(envelope.get('coverage_proof') == coverage and
         envelope.get('internal_proof_sha256') == evidence['internal_proof']['sha256'] and
         envelope.get('actual_closed_continuation_driver') ==
         {'prefix':str(common.DRIVER_PREFIX),'hashes':evidence['driver_hashes']} and
         envelope.get('frozen_v1_serialization_stop') == evidence['frozen_serialization_stop'],
         'Actual v2 envelope differs from current full native evidence/old failures')
    source_manifest = common.RUN/'PUBLISHED-MANIFEST-AFTER.json'
    need(digest(source_manifest) == coverage.get('published_manifest_after_sha256'), 'Actual final full mirror census changed')
    qualification = {'schema':ENVELOPE_SCHEMA,'coverage_schema':COVERAGE_SCHEMA,
                     'reused_same_source_leg_count':7,'new_passed_leg_count':17,'leg_count':24,
                     'pipeline':{**tail,'state':reference(NEW_TAIL_STATE)},'driver':evidence['driver'],
                     'verifier':verifier,'tools_manifest':reference(TOOLS),'finalization_tools_manifest':reference(NEW_TOOLS),
                     'root_authorization':reference(common.AUTH),'internal_proof':evidence['internal_proof'],
                     'original_failure_preserved':True,'frozen_v1_serialization_stop':evidence['frozen_serialization_stop']}
    return {'schema':SCHEMA,'result':'PASS','qualification_mode':MODE,'independent_envelope':reference(path),
            'coverage_proof':coverage,'source_manifest':reference(source_manifest),
            'renderer_qualification':qualification,'composite_tools_manifest_sha256':TOOLS_SHA,
            'finalization_tools_manifest_sha256':finalization_tools_sha256,'root_authorization_sha256':AUTH_SHA,
            'composite_selected_sha256':coverage['selected_sha256'],'original_failure_preserved':True,
            'original_attempts_result':'NONPASS','frozen_v1_finalization_result':'NONPASS: lossless JSON comparison defect',
            'not_claimed':['Single uninterrupted original matrix/pipeline PASS','DEV merge/deployment',
                           'Folded notes/yard UI delivery or visual/photo/native/gait approval']}


def check_existing_binding(binding_file, binding_sha256, finalization_tools_sha256):
    file = Path(binding_file).resolve()
    need(re.fullmatch('[0-9a-f]{64}',str(binding_sha256)) and digest(file) == binding_sha256,
         'Actual typed composite binding changed')
    binding = read(file)
    need(binding.get('schema') == SCHEMA and binding.get('qualification_mode') == MODE,
         'Require explicit v2 typed composite binding, never a raw/legacy proof')
    ref = binding.get('independent_envelope',{})
    actual = verify_closed_composite(ref.get('path',''),ref.get('sha256',''),finalization_tools_sha256)
    need(binding == actual,'Typed binding differs from actual current full closed composite re-read')
    return actual


def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--emit-actual-closed-binding',action='store_true')
    mode.add_argument('--check-existing-binding',action='store_true')
    p.add_argument('--v2-tools-sha256',required=True)
    for name in ['independent-proof','independent-proof-sha256','binding','binding-sha256','out']:
        p.add_argument('--'+name)
    a=p.parse_args()
    if a.emit_actual_closed_binding:
        need(a.independent_proof and a.independent_proof_sha256 and a.out,'Actual proof path/hash and NEW output required')
        out=Path(a.out).resolve();need(out.parent==LOG and not out.exists(),'Use NEW direct-child external binding file')
        binding=verify_closed_composite(a.independent_proof,a.independent_proof_sha256,a.v2_tools_sha256)
        with out.open('x') as stream:json.dump(binding,stream,indent=2);stream.write('\n')
        print(json.dumps({'result':'PASS','binding':reference(out),'qualification_mode':MODE}))
    else:
        need(a.binding and a.binding_sha256 and not a.out,'Actual binding path/hash; checking never writes a file')
        print(json.dumps(check_existing_binding(a.binding,a.binding_sha256,a.v2_tools_sha256)))
    return 0

if __name__=='__main__':raise SystemExit(main())
