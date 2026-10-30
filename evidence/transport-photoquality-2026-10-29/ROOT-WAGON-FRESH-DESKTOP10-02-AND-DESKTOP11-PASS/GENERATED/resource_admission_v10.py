"""External resource accounting proposal; native application gates are unchanged."""

import datetime
import hashlib
import json
import shutil
from pathlib import Path

BASELINE_PATH = Path('/workspace/.cloud-setup/logs/transport-recovery/ROOT-READONLY-MEMORY-EVENT-BASELINE-20261030-0235.json')
BASELINE_SHA256 = 'fc9b837d38e9c235ae8c2fa88001a31ac05bdb858e051193df36dbdbd1be4205'
MEMORY_FLOOR = 4 * 1024**3
WORKSPACE_FLOOR = 512 * 1024**2
TMP_FLOOR = 1024**3
POLICY = 'resource10: nonmax counters zero; max informational and monotonic; healthy resources at both ends'


def trusted_baseline():
    raw = BASELINE_PATH.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BASELINE_SHA256, 'Trusted baseline bytes changed'
    data = json.loads(raw)
    events = data['events_baseline']
    assert data['before']['events'] == data['after']['events'] == events
    assert data['original_available_RAM_floor_bytes'] == MEMORY_FLOOR
    assert events['max'] == 1269 and all(v == 0 for k, v in events.items() if k != 'max')
    assert data['before']['memory_max_bytes'] == data['after']['memory_max_bytes']
    return data


def check_events(before, after=None):
    baseline = trusted_baseline()['events_baseline']
    keys = set(baseline)

    def valid(events):
        return (isinstance(events, dict) and set(events) == keys
                and all(type(v) is int and v >= 0 for v in events.values())
                and all(events[k] == 0 for k in keys if k != 'max')
                and events['max'] >= baseline['max'])

    before_valid = valid(before)
    after_valid = after is None or valid(after)
    monotonic = after is None or (before_valid and after_valid and after['max'] >= before['max'])
    return {
        'accepted': bool(before_valid and after_valid and monotonic),
        'trusted_initial_baseline_sha256': BASELINE_SHA256,
        'trusted_keyset': sorted(keys),
        'before_valid': before_valid,
        'after_valid': after_valid,
        'max_monotonic': bool(monotonic),
        'max_initial_floor': baseline['max'],
        'max_before': before.get('max') if isinstance(before, dict) else None,
        'max_after': after.get('max') if isinstance(after, dict) else None,
        'max_delta_informational': (after['max'] - before['max'])
        if after is not None and before_valid and after_valid else None,
        'policy': POLICY,
    }


def snapshot():
    baseline = trusted_baseline()
    cg = Path('/sys/fs/cgroup')
    maximum = int((cg / 'memory.max').read_text())
    current = int((cg / 'memory.current').read_text())
    stat = {k: int(v) for k, v in (line.split() for line in (cg / 'memory.stat').read_text().splitlines())}
    events = {k: int(v) for k, v in (line.split() for line in (cg / 'memory.events').read_text().splitlines())}
    raw = max(0, maximum - current)
    clean_inactive = max(0, stat['inactive_file'] - stat['file_dirty'] - stat['file_writeback'])
    return {
        'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'policy': POLICY,
        'trusted_initial_baseline_path': str(BASELINE_PATH),
        'trusted_initial_baseline_sha256': BASELINE_SHA256,
        'trusted_initial_events': baseline['events_baseline'],
        'memory_max_bytes': maximum,
        'memory_current_bytes': current,
        'memory_peak_bytes_informational': int((cg / 'memory.peak').read_text()) if (cg / 'memory.peak').exists() else None,
        'raw_headroom_bytes': raw,
        'clean_inactive_file_bytes': clean_inactive,
        'memory_available_bytes': raw + clean_inactive,
        'memory_stat': stat,
        'memory_events': events,
        'workspace_free_bytes': shutil.disk_usage('/workspace').free,
        'tmp_free_bytes': shutil.disk_usage('/tmp').free,
        'memory_floor_bytes': MEMORY_FLOOR,
        'workspace_floor_bytes': WORKSPACE_FLOOR,
        'tmp_floor_bytes': TMP_FLOOR,
        'available_calculation': 'max(0,memory.max-memory.current)+max(0,inactive_file-file_dirty-file_writeback); excludes shmem, active_file and slab',
    }


def check_snapshot(state):
    baseline = trusted_baseline()
    stat = state['memory_stat']
    calculated = max(0, state['memory_max_bytes'] - state['memory_current_bytes']) + max(0, stat['inactive_file'] - stat['file_dirty'] - stat['file_writeback'])
    events = check_events(state['memory_events'])
    checks = {
        'memory_limit_unchanged': state['memory_max_bytes'] == baseline['before']['memory_max_bytes'],
        'raw_headroom_component_agrees': state['raw_headroom_bytes'] == max(0, state['memory_max_bytes'] - state['memory_current_bytes']),
        'clean_inactive_component_agrees': state['clean_inactive_file_bytes'] == max(0, stat['inactive_file'] - stat['file_dirty'] - stat['file_writeback']),
        'available_components_agree': state['memory_available_bytes'] == calculated,
        'available_memory_floor': state['memory_available_bytes'] >= MEMORY_FLOOR,
        'workspace_floor': state['workspace_free_bytes'] >= WORKSPACE_FLOOR,
        'tmp_floor': state['tmp_free_bytes'] >= TMP_FLOOR,
        'nonmax_zero_and_max_above_initial': events['accepted'],
    }
    return {'accepted': all(checks.values()), 'checks': checks, 'events': events, 'policy': POLICY}


def check_pair(before, after):
    first = check_snapshot(before)
    last = check_snapshot(after)
    events = check_events(before['memory_events'], after['memory_events'])
    return {
        'accepted': first['accepted'] and last['accepted'] and events['accepted'],
        'before': first,
        'after': last,
        'events': events,
        'policy': POLICY,
    }
