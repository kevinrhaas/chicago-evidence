#!/usr/bin/env python3
"""UNRUN. Explicit supervised finalization only, after real frozen-v1 closure.
No browser/gate/owner/publish/merge and no automatic retry is performed.
"""
import argparse
import json
import subprocess
import sys
import time
from h3_composite_proof_binding_v2 import *
from h3_composite_proof_binding_v2 import _closed


def save_state(phase,tool_sha,**extra):
    value={'phase':phase,'head':HEAD,'tools_manifest_sha256':tool_sha,'observed_unix':time.time(),**extra}
    temporary=NEW_TAIL_STATE.with_name(NEW_TAIL_STATE.name+'.tmp')
    temporary.write_text(json.dumps(value,indent=2)+'\n')
    temporary.replace(NEW_TAIL_STATE)
    print(phase,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute-reviewed-finalization',action='store_true')
    parser.add_argument('--v2-tools-sha256',required=True)
    args=parser.parse_args()
    need(args.execute_reviewed_finalization,'ROOT explicit reviewed finalization required')
    verify_finalization_tools(args.v2_tools_sha256)
    need(not NEW_TAIL_STATE.exists() and not NEW_PROOF.exists(),'Preserve previous finalization state/proof')
    need(not any(LOG.glob(NEW_VERIFIER_PREFIX.name+'.*')),'Use only a NEW independent verifier prefix')
    driver=LOG/'70b-tls-repair-continuation1-driver'
    verifier=LOG/'70b-tls-repair-continuation1-independent-verifier'
    pipeline=LOG/'70b-tls-repair-continuation1-pipeline'
    try:
        save_state('WAITING: actual frozen460d driver0 and specific original verifier/pipeline closure; no browser launch',args.v2_tools_sha256)
        started=time.monotonic()
        while True:
            need(time.monotonic()-started<50000,'Closure wait expired; ROOT must review, no retry')
            verify_finalization_tools(args.v2_tools_sha256)
            driver_result=Path(str(driver)+'.result.json')
            if driver_result.exists():
                result=read(driver_result)
                need(result.get('returncode')==0 and result.get('timed_out') is False,
                     'Actual continuation driver failed; never reinterpret a native failure')
            closure_files=[Path(str(p)+s) for p in [driver,verifier,pipeline] for s in ['.result.json','.cleanup.json']]
            if all(p.exists() for p in closure_files):
                break
            time.sleep(.5)
        # This is the first current-source/native evidence inspection: all old
        # owned processes have now actually exited and their real receipts exist.
        common,coverage,evidence=verify_expected_frozen_stop(args.v2_tools_sha256)
        save_state('RUNNING: new independent JSON-normalized complete24 verifier; original NONPASS preserved',args.v2_tools_sha256)
        subprocess.run([sys.executable,str(common.old.SUPERVISOR),'--prefix',str(NEW_VERIFIER_PREFIX),
                        '--cwd',str(common.old.APP),'--timeout','600','--',sys.executable,
                        str(HERE/'verify_h3_composite_json_normalized_v2.py'),
                        '--v2-tools-sha256',args.v2_tools_sha256],check=True)
        closed=_closed(NEW_VERIFIER_PREFIX,HERE/'verify_h3_composite_json_normalized_v2.py',
                       ['--v2-tools-sha256',args.v2_tools_sha256],600)
        proof=read(NEW_PROOF)
        need(proof.get('schema')==ENVELOPE_SCHEMA and proof.get('result')=='PASS' and
             proof.get('coverage_proof')==coverage and
             proof.get('frozen_v1_serialization_stop')==evidence['frozen_serialization_stop'] and
             proof.get('finalization_tools_manifest_sha256')==args.v2_tools_sha256,
             'Actual new normalized verifier output differs')
        save_state(TAIL_PASS,args.v2_tools_sha256,independent_proof=str(NEW_PROOF),
                   independent_proof_sha256=digest(NEW_PROOF),verifier_prefix=str(NEW_VERIFIER_PREFIX),
                   actual_closed_verifier=closed,original_failures_preserved=True)
        return 0
    except BaseException as error:
        save_state('STOPPED: actual finalization failure retained; no retry/no browser rerun',args.v2_tools_sha256,error=str(error))
        raise


if __name__=='__main__':raise SystemExit(main())
