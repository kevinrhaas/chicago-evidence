"""Launch the already bounded diagnostic owner in one recorded private session."""
from pathlib import Path
import argparse, datetime, json, os, subprocess, sys

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--binding', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--mode', choices=['diagnostic', 'master-candidate'], default='diagnostic')
    a = p.parse_args(); here = Path(__file__).resolve().parent
    binding = json.loads(a.binding.read_text())
    go_flag = 'ROOT_EXPLICIT_GARMENT_DIAGNOSTIC_GO' if a.mode == 'diagnostic' else 'ROOT_EXPLICIT_MASTER_GARMENT_PROTOTYPE_GO'
    assert binding['template_only'] is False and binding[go_flag] is True
    repo = Path(binding['repo']).resolve(); app = Path(binding['app']).resolve(); out = a.out.resolve()
    assert app == repo/'chicago/4d'
    assert out != repo and repo not in out.parents, 'Reject output within the repository before any sidecar write.'
    a.out = out
    receipt = a.out.with_name(a.out.name+'-LAUNCH.json')
    stdout = a.out.with_name(a.out.name+'-OWNER.stdout')
    assert a.binding.is_file() and not a.out.exists() and not receipt.exists() and not stdout.exists()
    runner = 'run_bounded_diagnostic.py' if a.mode == 'diagnostic' else 'run_bounded_master_candidate.py'
    command = [sys.executable, str(here/runner), '--binding', str(a.binding.resolve()), '--out', str(a.out.resolve())]
    with stdout.open('xb', buffering=0) as f:
        child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT,
            start_new_session=True, close_fds=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    stat = Path(f'/proc/{child.pid}/stat').read_text().rsplit(')', 1)[1].split()
    row = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), owner_pid=child.pid,
        owner_start_ticks=int(stat[19]), owner_pgid=os.getpgid(child.pid), owner_sid=os.getsid(child.pid),
        command=command, stdout=str(stdout), output=str(a.out), native_timeout_seconds=120,
        status='OWNER_LAUNCHED_NOT_DIAGNOSTIC_COMPLETION_OR_QUALITY_PASS')
    assert row['owner_pgid'] == row['owner_sid'] == child.pid
    receipt.write_text(json.dumps(row, indent=2)+'\n'); print(json.dumps(row))

if __name__ == '__main__':
    main()
