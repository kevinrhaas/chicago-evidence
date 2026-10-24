#!/usr/bin/env python3
import hashlib, json, re, subprocess
from pathlib import Path

root=Path('/workspace/chicago')
logs=Path('/workspace/.cloud-setup/logs/transport-recovery')
session=json.loads(Path('/workspace/.cloud-setup/queue-session.json').read_text())
binding=json.loads(Path(session['smoke_binding']).read_text())
assert binding['status']=='passed: all15parts/bothviewports, zero page errors'
assert len(binding['completed'])==24
for ref,key in [('HEAD','head'),('HEAD^{tree}','tree')]:
    assert subprocess.check_output(['git','rev-parse',ref],cwd=root).decode().strip()==binding[key]
subprocess.check_call(['git','diff','--quiet','HEAD'],cwd=root)
manifest_path=logs/'de91-integrated-published-files.json'
assert hashlib.sha256(manifest_path.read_bytes()).hexdigest()==binding['published']['manifest_sha256']
manifest=json.loads(manifest_path.read_text())
expected={x['path'] for x in manifest}
mirror=root/'site/4d'
actual={str(x.relative_to(mirror)) for x in mirror.rglob('*') if x.is_file()}
assert expected==actual, ('Published file set changed', len(expected),len(actual))
for row in manifest:
    path=mirror/row['path']
    assert path.stat().st_size==row['bytes'],row['path']
    with path.open('rb') as f: assert hashlib.file_digest(f,'sha256').hexdigest()==row['sha256'],row['path']
coverage={v:set() for v in ['mobile','desktop']}
for leg in binding['completed']:
    prefix=Path(leg['prefix'])
    result=json.loads(Path(str(prefix)+'.result.json').read_text())
    cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text())
    transcript=Path(str(prefix)+'.log').read_text(errors='replace')
    assert leg['verified_pass'] and leg['outer_returncode']==0 and result['returncode']==0 and not result['timed_out']
    assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
    assert 'SMOKE PASS' in transcript and 'zero page errors' in transcript
    staged=re.search(r'(\d+) staged-section check\(s\)',transcript)
    assert staged and int(staged[1])>0 and int(staged[1])==leg['staged_checks']
    bounds=[int(x) for x in leg['stage'].split('-')]
    coverage[leg['viewport']].update(range(bounds[0],bounds[-1]+1))
assert all(x==set(range(1,16)) for x in coverage.values())
out=logs/'de91-integrated-complete-smoke-verification.json'
assert not out.exists(), 'Keep original verification receipt'
record={'head':binding['head'],'tree':binding['tree'],'verified_legs':24,
        'coverage':{k:sorted(v) for k,v in coverage.items()},
        'published_file_count':len(manifest),'published_bytes':sum(x['bytes'] for x in manifest),
        'published_manifest_rehashed':True,'all_command_results_and_cleanup_verified':True,
        'source_unchanged':True,'all_legs_fit_600s':all(x['seconds']<=600 for x in binding['completed'])}
out.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
