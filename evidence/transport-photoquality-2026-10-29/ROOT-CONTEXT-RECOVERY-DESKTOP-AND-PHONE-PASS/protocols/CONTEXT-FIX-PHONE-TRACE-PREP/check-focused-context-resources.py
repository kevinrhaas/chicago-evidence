"""Read-only launch guard. No process is stopped or modified."""
from pathlib import Path
import datetime, json, shutil

GiB = 1024**3
max_memory = int(Path('/sys/fs/cgroup/memory.max').read_text())
memory = int(Path('/sys/fs/cgroup/memory.current').read_text())
free = {p: shutil.disk_usage(p).free for p in ('/workspace', '/tmp')}
active = []
for process in Path('/proc').iterdir():
    if not process.name.isdigit():
        continue
    try:
        stat = (process / 'stat').read_text().rsplit(')', 1)[1].split()
        if stat[0] == 'Z':
            continue
        argv = (process / 'cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace')
    except (OSError, ValueError, IndexError):
        continue
    tokens = argv.split()
    # Inspect executable/script names rather than shell prose or this file's
    # source text. The scheduler's explicit root GO is required independently.
    is_browser = tokens and Path(tokens[0]).name in ('chromium', 'chrome', 'chrome-headless-shell')
    is_heavy_owner = any(Path(t).name in ('rederive.mjs', 'preflight.sh', 'check.sh', 'publish.sh', 'smoke_renderer.mjs') for t in tokens[:5])
    if is_browser or is_heavy_owner:
        active.append(dict(pid=int(process.name), command=' '.join(tokens[:6])))
receipt = dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               cpu_quota=Path('/sys/fs/cgroup/cpu.max').read_text().strip(),
               memory_current_bytes=memory, memory_max_bytes=max_memory,
               memory_headroom_bytes=max_memory-memory, free_disk_bytes=free,
               active_browser_or_heavy_owners=active,
               minimum_memory_headroom_bytes=4*GiB,
               minimum_workspace_free_bytes=512*1024**2,
               minimum_tmp_free_bytes=GiB)
print(json.dumps(receipt, indent=2), flush=True)
assert max_memory-memory >= 4*GiB, 'Insufficient cgroup RAM headroom; do not start GPU work'
assert free['/workspace'] >= 512*1024**2, 'Preserve 512 MiB workspace headroom'
assert free['/tmp'] >= GiB, 'Preserve 1 GiB temporary browser headroom'
assert not active, 'Root must release other browser/native-owner slots first'
