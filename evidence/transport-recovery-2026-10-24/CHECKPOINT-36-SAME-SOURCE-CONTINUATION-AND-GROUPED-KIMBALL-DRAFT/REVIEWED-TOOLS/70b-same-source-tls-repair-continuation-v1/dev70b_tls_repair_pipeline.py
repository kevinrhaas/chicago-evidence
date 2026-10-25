#!/usr/bin/env python3
import argparse
import subprocess
import sys
from dev70b_tls_repair_common import *
p=argparse.ArgumentParser();p.add_argument('--execute-reviewed-continuation',action='store_true');p.add_argument('--tools-sha256',required=True);a=p.parse_args()
need(a.execute_reviewed_continuation,'Explicit ROOT authorization required');tools(a.tools_sha256);quiet()
need(not PIPELINE_STATE.exists(),'Preserve existing pipeline attempt')
for prefix in [DRIVER_PREFIX,VERIFIER_PREFIX]:
 need(not any(old.LOG.glob(prefix.name+'.*')),'Never reuse supervised attempt prefix')
def phase(label,**extra): save(PIPELINE_STATE,{'phase':label,'head':HEAD,'run_dir':str(RUN),'tools_manifest_sha256':a.tools_sha256,'observed_unix':time.time(),**extra})
def supervised(prefix,cap,script,extra):
 subprocess.run([sys.executable,str(old.SUPERVISOR),'--prefix',str(prefix),'--cwd',str(old.APP),'--timeout',str(cap),'--',sys.executable,str(HERE/script),*extra,'--tools-sha256',a.tools_sha256],check=True);closed(prefix)
try:
 phase('RUNNING: explicit same-H3 TLS-repair continuation; original attempt remains NONPASS')
 supervised(DRIVER_PREFIX,43200,'dev70b_tls_repair_driver.py',['--execute-reviewed-continuation'])
 phase('VERIFYING: continuation driver actually closed0/cleanup0')
 supervised(VERIFIER_PREFIX,600,'dev70b_tls_repair_verify.py',[])
 phase('PASS: composite24/independent verifier closed0/cleanup0; enclosing outer still must close; DEV merge pending',independent_proof=str(PROOF),independent_proof_sha256=digest(PROOF),driver_prefix=str(DRIVER_PREFIX),verifier_prefix=str(VERIFIER_PREFIX))
except BaseException as exc:
 phase('STOPPED: actual continuation failure preserved; no automatic retry',error=str(exc));raise
