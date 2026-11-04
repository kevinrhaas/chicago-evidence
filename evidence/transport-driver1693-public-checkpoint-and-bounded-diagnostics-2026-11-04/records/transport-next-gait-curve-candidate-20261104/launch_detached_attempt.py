"""Launch only this frozen bounded authoring attempt with explicit session ownership."""
from pathlib import Path
import argparse,datetime,json,os,subprocess,sys
P=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--binding',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
assert a.binding.is_file()and not a.out.exists()
receipt=a.out.with_name(a.out.name+'-LAUNCH.json');stdout=a.out.with_name(a.out.name+'-OWNER.stdout');assert not receipt.exists()and not stdout.exists()
cmd=[sys.executable,str(P/'run_one_attempt.py'),'--binding',str(a.binding),'--out',str(a.out)]
with stdout.open('xb',buffering=0)as stream:
 child=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
stat=Path(f'/proc/{child.pid}/stat').read_text().rsplit(')',1)[1].split();d=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),owner_pid=child.pid,owner_start_ticks=int(stat[19]),owner_pgid=os.getpgid(child.pid),owner_sid=os.getsid(child.pid),command=cmd,stdout=str(stdout),output=str(a.out),supervisor_timeout_seconds=120,state='ONE_CURVE_ATTEMPT_OWNER_LAUNCHED_NOT_ACCEPTANCE')
assert d['owner_pgid']==d['owner_sid']==child.pid;receipt.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
