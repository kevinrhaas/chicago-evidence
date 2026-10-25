#!/usr/bin/env python3
import argparse
from dev70b_tls_repair_common import *
p=argparse.ArgumentParser();p.add_argument('--tools-sha256',required=True);a=p.parse_args()
quiet();tools(a.tools_sha256);driver=closed_driver(a.tools_sha256)
need(not PROOF.exists(),'Preserve existing independent proof')
proof=verify_selected(RUN,a.tools_sha256)
need(proof==read(RUN/'INTERNAL-COMPOSITE-PROOF.json'),'Independent re-read differs from closed internal composite proof')
save(PROOF,{'schema':'chicago-h3-independent-tls-repair-composite-v1','result':'PASS','coverage_proof':proof,'actual_closed_continuation_driver':{'prefix':str(DRIVER_PREFIX),'hashes':driver},'internal_proof_sha256':digest(RUN/'INTERNAL-COMPOSITE-PROOF.json'),'verified_unix':time.time()})
print('PASS: independently reread24 selected actual same-H3 leg executions; original failure retained',flush=True)
