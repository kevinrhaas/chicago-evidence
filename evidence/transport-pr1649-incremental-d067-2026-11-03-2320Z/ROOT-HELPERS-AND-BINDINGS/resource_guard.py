"""Fresh restored-runtime epoch; never requalifies historical resource10 receipts."""
from pathlib import Path
import datetime, hashlib, json, os, sys

ROOT = Path('/sys/fs/cgroup')
BASELINE = Path(__file__).with_name('RESTORED-RUNTIME-BASELINE.json')
RAM_FLOOR = 4 * 1024**3
WORKSPACE_FLOOR = 512 * 1024**2
TMP_FLOOR = 1024**3

def snapshot():
    memory = dict(line.split() for line in (ROOT/'memory.stat').read_text().splitlines())
    events = {k: int(v) for k, v in (line.split() for line in (ROOT/'memory.events').read_text().splitlines())}
    limit = int((ROOT/'memory.max').read_text().strip())
    current = int((ROOT/'memory.current').read_text().strip())
    inactive = int(memory['inactive_file'])
    dirty, writeback = int(memory['file_dirty']), int(memory['file_writeback'])
    def free(path):
        s = os.statvfs(path)
        return s.f_bavail * s.f_frsize
    return dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                cgroup_inode=ROOT.stat().st_ino, memory_max_bytes=limit,
                memory_current_bytes=current, inactive_file_bytes=inactive,
                file_dirty_bytes=dirty, file_writeback_bytes=writeback,
                available_memory_bytes=max(0, limit-current)+max(0, inactive-dirty-writeback),
                workspace_free_bytes=free('/workspace'), tmp_free_bytes=free('/tmp'),
                memory_events=events, pids_current=int((ROOT/'pids.current').read_text()),
                cpu_quota_period=(ROOT/'cpu.max').read_text().strip())

def baseline():
    return json.loads(BASELINE.read_text())['snapshot']

def check(s):
    b = baseline()
    values = [s[k] for k in ['cgroup_inode','memory_max_bytes','memory_current_bytes',
              'inactive_file_bytes','file_dirty_bytes','file_writeback_bytes',
              'available_memory_bytes','workspace_free_bytes','tmp_free_bytes','pids_current']]
    events, initial = s['memory_events'], b['memory_events']
    available = max(0, s['memory_max_bytes']-s['memory_current_bytes']) + max(0,
        s['inactive_file_bytes']-s['file_dirty_bytes']-s['file_writeback_bytes'])
    checks = dict(exact_nonnegative_integers=all(type(v) is int and v >= 0 for v in values+list(events.values())),
                  same_restored_epoch=s['cgroup_inode']==b['cgroup_inode'] and s['memory_max_bytes']==b['memory_max_bytes'],
                  complete_event_keyset=set(events)==set(initial) and 'max' in events,
                  all_nonmax_zero=all(v==0 for k,v in events.items() if k!='max'),
                  max_not_below_new_epoch_baseline=events.get('max',-1)>=initial['max'],
                  available_components_agree=s['available_memory_bytes']==available,
                  ram_floor=available>=RAM_FLOOR,
                  workspace_floor=s['workspace_free_bytes']>=WORKSPACE_FLOOR,
                  tmp_floor=s['tmp_free_bytes']>=TMP_FLOOR)
    return dict(accepted=all(checks.values()),checks=checks,
                baseline_sha256=hashlib.sha256(BASELINE.read_bytes()).hexdigest())

def pair(before, after):
    a,b=check(before),check(after)
    transition=set(before['memory_events'])==set(after['memory_events']) and after['memory_events']['max']>=before['memory_events']['max']
    return dict(accepted=a['accepted'] and b['accepted'] and transition,
                before=a,after=b,max_monotone_between_snapshots=transition)

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='init':
        assert not BASELINE.exists(), 'Never reset a running epoch baseline'
        s=snapshot()
        assert 'max' in s['memory_events'] and all(v==0 for k,v in s['memory_events'].items() if k!='max')
        BASELINE.write_text(json.dumps(dict(schema='restored-runtime-resource-epoch-v1',
            reason='Managed environment restored; fresh process/cgroup counters. Old resource10 receipts remain immutable and are not reinterpreted.',
            observed_cloud_spec='4',snapshot=s),indent=2)+'\n')
        verdict=check(s)
    elif mode=='capture':
        s=snapshot();Path(sys.argv[2]).write_text(json.dumps(s,indent=2)+'\n');verdict=check(s)
    elif mode=='pair':
        verdict=pair(json.loads(Path(sys.argv[2]).read_text()),json.loads(Path(sys.argv[3]).read_text()))
        Path(sys.argv[4]).write_text(json.dumps(verdict,indent=2)+'\n')
    else:
        raise SystemExit('usage: resource_guard.py init | capture FILE | pair BEFORE AFTER RESULT')
    print(json.dumps(verdict))
    raise SystemExit(0 if verdict['accepted'] else 1)
