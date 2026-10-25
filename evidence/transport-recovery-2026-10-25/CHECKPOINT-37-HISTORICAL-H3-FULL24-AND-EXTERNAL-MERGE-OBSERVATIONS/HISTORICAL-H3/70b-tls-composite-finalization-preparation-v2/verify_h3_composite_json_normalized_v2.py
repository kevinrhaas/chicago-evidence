#!/usr/bin/env python3
"""UNRUN. New independent read-only verifier; never reruns a browser leg."""
import argparse
import json
import time
from h3_composite_proof_binding_v2 import *


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--v2-tools-sha256',required=True)
    args=parser.parse_args()
    need(not NEW_PROOF.exists(),'Preserve existing v2 independent proof; no automatic retry')
    common,normalized,evidence=verify_expected_frozen_stop(args.v2_tools_sha256)
    # verify_expected_frozen_stop compares EVERY losslessly JSON-normalized field
    # with the actual internal proof after rerunning unchanged native validators.
    result={'schema':ENVELOPE_SCHEMA,'result':'PASS','coverage_proof':normalized,
            'actual_closed_continuation_driver':{'prefix':str(common.DRIVER_PREFIX),'hashes':evidence['driver_hashes']},
            'internal_proof_sha256':evidence['internal_proof']['sha256'],
            'frozen_v1_serialization_stop':evidence['frozen_serialization_stop'],
            'finalization_tools_manifest_sha256':args.v2_tools_sha256,'verified_unix':time.time()}
    with NEW_PROOF.open('x') as stream:
        json.dump(result,stream,indent=2)
        stream.write('\n')
    print('PASS: independent complete24 native evidence; only JSON representation normalized; old failures preserved',flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
