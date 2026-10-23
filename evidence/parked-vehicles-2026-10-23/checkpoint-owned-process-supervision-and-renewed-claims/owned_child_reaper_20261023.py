"""Reap only newly adopted children of THIS supervisor; never touch init.

The main Popen child is excluded from orphan waitpid calls so its real exit
status remains authoritative. This cannot reap or affect existing PID1 children.
"""
import ctypes, os, pathlib, subprocess, time, signal

def enable():
    assert ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) == 0

def children():
    p = pathlib.Path('/proc') / str(os.getpid()) / 'task' / str(os.getpid()) / 'children'
    try:
        return [int(x) for x in p.read_text().split()]
    except FileNotFoundError:
        return []

def reap_orphans(exclude=None):
    reaped = []
    for pid in children():
        if pid == exclude:
            continue
        try:
            got, status = os.waitpid(pid, os.WNOHANG)
            if got:
                reaped.append({'pid': got, 'wait_status': status})
        except ChildProcessError:
            pass
    return reaped

def run(command, cwd, env, log, timeout=3600):
    started = time.monotonic()
    adopted = []
    with pathlib.Path(log).open('wb') as f:
        child = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                 stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            while True:
                rc = child.poll()
                adopted.extend(reap_orphans(child.pid))
                if rc is not None:
                    return {'returncode': rc, 'seconds': time.monotonic()-started,
                            'main_child_pid': child.pid, 'new_owned_orphans_reaped': adopted}
                if time.monotonic()-started > timeout:
                    raise TimeoutError('Owned child exceeded its explicit deadline')
                time.sleep(.01)
        finally:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
            adopted.extend(reap_orphans(child.pid))

def finish():
    # Only direct children adopted by this subreaper remain after its main child
    # has ended. No live process from another run can become our child.
    reaped = reap_orphans()
    signaled = []
    for pid in children():
        try:
            fields = (pathlib.Path('/proc') / str(pid) / 'stat').read_text().rsplit(')', 1)[1].split()
            if int(fields[1]) != os.getpid():
                continue
            start = fields[19]
            current = (pathlib.Path('/proc') / str(pid) / 'stat').read_text().rsplit(')', 1)[1].split()
            if current[19] == start and int(current[1]) == os.getpid():
                os.kill(pid, signal.SIGTERM)
                signaled.append(pid)
        except (FileNotFoundError, ProcessLookupError):
            pass
    deadline = time.monotonic()+3
    while children() and time.monotonic() < deadline:
        reaped.extend(reap_orphans())
        time.sleep(.01)
    return {'owned_adopted_children_reaped': reaped,
            'owned_adopted_children_SIGTERM': signaled, 'remaining_owned_children': children()}
