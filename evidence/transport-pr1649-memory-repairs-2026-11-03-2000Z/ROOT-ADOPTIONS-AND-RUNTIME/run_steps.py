"""Run explicitly supplied native commands with owned cleanup and resource receipts."""
from pathlib import Path
import argparse, fcntl, importlib.util, json, os, subprocess, sys

p=argparse.ArgumentParser()
p.add_argument('--cwd', required=True)
p.add_argument('--out', required=True)
p.add_argument('--steps', required=True, help='JSON list of [label, original timeout seconds, argv]')
a=p.parse_args()
d=Path(a.out); d.mkdir(exist_ok=False)
here=Path(__file__).parent
spec=importlib.util.spec_from_file_location('guard',here/'resource_guard.py')
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
rows=[]; errors=[]
try:
    for label, cap, cmd in json.loads(a.steps):
        before=g.snapshot(); assert g.check(before)['accepted']
        prefix=d/label
        with Path(str(prefix)+'.stdout').open('xb') as f:
            r=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py',
                '--prefix',str(prefix),'--cwd',a.cwd,'--timeout',str(cap),'--',*cmd],stdout=f,stderr=subprocess.STDOUT)
        result=json.loads(Path(str(prefix)+'.result.json').read_text())
        cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text())
        resources=g.pair(before,g.snapshot())
        rows.append(dict(label=label, result=result, cleanup=cleanup, resources=resources))
        (d/'LEDGER.json').write_text(json.dumps(rows,indent=2)+'\n')
        assert r.returncode==result['returncode']==0, label
        assert not result['timed_out'] and result['effective_timeout_seconds']==cap
        assert result['timeout_override_reason'] is None and cleanup['cleanup_complete']
        assert not cleanup['remaining_owned_children'] and resources['accepted']
except BaseException as e:
    errors.append(repr(e))
(d/'CLOSED.json').write_text(json.dumps(dict(status='PASS' if not errors else 'NONPASS', rows=rows, errors=errors),indent=2)+'\n')
print(json.dumps(dict(output=str(d), errors=errors)))
raise SystemExit(1 if errors else 0)
