#!/usr/bin/env python3
"""Read-only final audit, writing only an explicitly new external verification receipt."""
import argparse,json
from pathlib import Path
from dev6ab_transport_ui_matrix_common import *
def main():
 p=argparse.ArgumentParser();p.add_argument('--head',required=True);p.add_argument('--run-dir',required=True);p.add_argument('--receipt',required=True);a=p.parse_args();out=Path(a.receipt).resolve();need(str(out).startswith(str(LOG)+'/') and not out.exists(),'Use a new external verification receipt');need(not busy_processes(),'A browser or matrix driver is still active; do not declare final coverage yet')
 result=verify_complete(a.run_dir,a.head);save(out,result);print(json.dumps(result,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
