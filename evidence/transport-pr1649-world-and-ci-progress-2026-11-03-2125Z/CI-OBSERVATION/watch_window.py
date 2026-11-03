"""Finite GET-only CI observer; no test/workflow mutations are implemented."""
from pathlib import Path
import datetime, hashlib, json, os, signal, subprocess, sys, time

ROOT = Path(__file__).resolve().parent
OBSERVER = ROOT / 'observe_pr1649_v3.py'
OBSERVER_SHA = '007111ef2ab4e80981880be2b037eb5f3a0bc6d7e35b97f102137340f326f240'
HEAD = '5439723317fbb6491e837911243f2f62fb35065b'
TREE = 'ef566b993dd2bfe76eea419c750aa01e7acec263'
OUT = ROOT / ('WINDOW-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
OUT.mkdir()

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(path, value):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)

assert hashlib.sha256(OBSERVER.read_bytes()).hexdigest() == OBSERVER_SHA
state = {'pid': os.getpid(), 'opened_utc': utc(), 'state': 'RUNNING',
         'original_budget_seconds': 1800, 'poll_seconds': 45, 'GET_only': True,
         'HEAD': HEAD, 'TREE': TREE, 'observer_sha256': OBSERVER_SHA, 'cycles': []}
save(OUT / 'LIVE-STATE.json', state)
save(ROOT / 'CURRENT-WINDOW.json', {'output': str(OUT), 'pid': os.getpid(), 'opened_utc': state['opened_utc']})
start = time.monotonic()
deadline = start + 1800
try:
    while time.monotonic() < deadline:
        cycle_start = time.monotonic()
        number = len(state['cycles']) + 1
        folder = OUT / f'{number:02d}'
        folder.mkdir()
        command = [sys.executable, str(OBSERVER), '--sha', HEAD, '--expected-tree', TREE,
                   '--logs', '--out', str(folder), '--log-cache', str(ROOT / 'native-logs')]
        assert hashlib.sha256(OBSERVER.read_bytes()).hexdigest() == OBSERVER_SHA
        with (folder / 'observer.stdout').open('w') as stdout, (folder / 'observer.stderr').open('w') as stderr:
            child = subprocess.Popen(command, stdout=stdout, stderr=stderr, start_new_session=True)
            timed_out = False
            try: code = child.wait(timeout=min(120, max(.1, deadline - time.monotonic())))
            except subprocess.TimeoutExpired:
                timed_out = True
                assert os.getpgid(child.pid) == child.pid
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
                code = child.returncode
        row = {'cycle': number, 'utc': utc(), 'returncode': code, 'GET_observer_timed_out': timed_out,
               'owned_GET_child_reaped': child.returncode is not None}
        try:
            summary = json.loads((folder / 'observer.stdout').read_text().splitlines()[-1])
            row.update(summary)
        except Exception as error: row['observer_result_unknown'] = str(error)
        state['cycles'].append(row)
        state['last_observation'] = row
        save(OUT / 'LIVE-STATE.json', state)
        print(json.dumps(row), flush=True)
        if row.get('metadata_state') == 'EXPECTED_15_SUCCESS_7_SKIP' and row.get('pinned_tree_matches'):
            state['state'] = 'CLOSED_METADATA_GREEN_REQUIRES_ROOT_NATIVE_SOURCE_FOOTER_AND_FRESHNESS_REVIEW'
            break
        if timed_out:
            state['state'] = 'CLOSED_GET_OBSERVER_TIMEOUT_NO_NATIVE_QUALITY_INFERENCE'
            break
        # A known terminal CI blocker is retained while other jobs finish;
        # only ROOT may decide whether to rerun its own failed workflow.
        next_poll = min(cycle_start + 45, deadline)
        while time.monotonic() < next_poll: time.sleep(min(1, next_poll - time.monotonic()))
    if state['state'] == 'RUNNING': state['state'] = 'CLOSED_ORIGINAL_1800_SECOND_GET_WINDOW'
except Exception as error:
    state.update(state='CLOSED_LOCAL_OBSERVER_ERROR_NO_NATIVE_QUALITY_INFERENCE', error=str(error))
finally:
    state.update(closed_utc=utc(), actual_seconds=time.monotonic() - start)
    save(OUT / 'CLOSED-WINDOW.json', state)
    save(OUT / 'LIVE-STATE.json', state)
