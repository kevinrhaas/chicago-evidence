"""Launch one bounded world owner in its own session, retaining explicit ownership."""
from pathlib import Path
import argparse, datetime, json, os, subprocess, sys

p=argparse.ArgumentParser()
p.add_argument('--runner',type=Path,required=True)
p.add_argument('--binding',type=Path,required=True)
p.add_argument('--year',choices=['1835','1904'],required=True)
p.add_argument('--viewport',choices=['desktop','mobile'],required=True)
p.add_argument('--scope',choices=['A','B','C'],required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
assert a.runner.is_file() and a.binding.is_file() and not a.out.exists()
receipt=a.out.with_name(a.out.name+'-LAUNCH.json')
stdout=a.out.with_name(a.out.name+'-OWNER.stdout')
assert not receipt.exists() and not stdout.exists()
cmd=[sys.executable,str(a.runner),'--binding',str(a.binding),'--year',a.year,
     '--viewport',a.viewport,'--scope',a.scope,'--out',str(a.out)]
with stdout.open('xb',buffering=0)as f:
    child=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,
        start_new_session=True,close_fds=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
stat=Path(f'/proc/{child.pid}/stat').read_text().rsplit(')',1)[1].split()
v=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),owner_pid=child.pid,
       owner_start_ticks=int(stat[19]),owner_pgid=os.getpgid(child.pid),owner_sid=os.getsid(child.pid),
       command=cmd,stdout=str(stdout),output=str(a.out),native_supervisor_timeout_seconds=600,
       state='OWNER_LAUNCHED_NOT_PASS',reason='Own session preserves the bounded Python owner across terminal/context transitions.')
assert v['owner_pgid']==v['owner_sid']==child.pid
receipt.write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps(v))
