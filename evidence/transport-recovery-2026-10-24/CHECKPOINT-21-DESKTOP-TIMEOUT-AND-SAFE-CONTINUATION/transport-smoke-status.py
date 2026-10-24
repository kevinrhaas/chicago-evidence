import json
from pathlib import Path
r = Path('/workspace/.cloud-setup/logs/transport-recovery')
session = json.loads(Path('/workspace/.cloud-setup/queue-session.json').read_text())
binding = Path(session.get('smoke_binding', str(r/'latest-dev-smoke-deferred-images-binding.json')))
d = json.loads(binding.read_text())
out = {'status': d['status'], 'completed_legs': len(d['completed']), 'total_legs': 24}
out['deferred'] = [{'viewport': x['viewport'], 'stage': x['stage']} for x in d.get('deferred', [])]
active = d.get('active')
if active:
    out['active'] = active
    key = f"{active['viewport']}:{active['stage']}"
    override = session.get('smoke_active_prefix_overrides', {}).get(key)
    p = Path(active['prefix']+'.log') if active.get('prefix') else (Path(override+'.log') if override else r/f"latest-dev-smoke-{active['viewport']}-{active['stage']}.log")
    if p.exists():
        lines = p.read_text(errors='replace').splitlines()
        passes = [x.strip() for x in lines if x.lstrip().startswith('pass  ')]
        fails = [x.strip() for x in lines if x.lstrip().startswith('FAIL  ')]
        out.update(active_pass_lines=len(passes), active_fail_lines=len(fails), latest_pass=passes[-1].split(' — ')[0][:240] if passes else None)
print(json.dumps(out))
