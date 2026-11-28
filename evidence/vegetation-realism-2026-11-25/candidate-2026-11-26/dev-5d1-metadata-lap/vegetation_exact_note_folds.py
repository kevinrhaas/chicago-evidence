"""Prove a tree changed only by exact official pending-entry folds."""
import base64, json, subprocess
from pathlib import Path

W = Path('/workspace/work')

def verify_folds(repo, before, after):
    def raw(*a):
        return subprocess.check_output(['git', *a], cwd=repo)
    changes = [line.split('\t') for line in raw('diff', '--no-renames',
               '--name-status', before, after).decode().splitlines()]
    if not changes:
        return {'complete': True, 'before': before, 'after': after,
                'paths': [], 'folds': []}
    changelog = 'chicago/4d/renderers/web/js/changelog.js'
    folds = [p for s, p in changes if s == 'D' and
             p.startswith('chicago/4d/changelog.d/') and p.endswith('.json')]
    assert folds and {tuple(x) for x in changes} == {
        ('M', changelog), *(('D', p) for p in folds)}, changes
    a, b = raw('show', before+':'+changelog), raw('show', after+':'+changelog)
    header = b'export const CHANGELOG = [ // newest first\n'
    assert a.startswith(header) and b.startswith(header)
    assert b.endswith(a[len(header):]), 'An existing release literal changed'
    parser = "import{readFileSync}from'node:fs';const d=JSON.parse(readFileSync(0,'utf8'));const a=await import('data:text/javascript;base64,'+d.before),b=await import('data:text/javascript;base64,'+d.after);console.log(JSON.stringify({old:a.CHANGELOG,new:b.CHANGELOG}));"
    decoded = json.loads(subprocess.check_output(
        [str(W/'node22/bin/node'), '--input-type=module', '-e', parser],
        input=json.dumps({'before': base64.b64encode(a).decode(),
                          'after': base64.b64encode(b).decode()}), text=True))
    assert len(decoded['new'])-len(decoded['old']) == len(folds)
    assert decoded['new'][len(folds):] == decoded['old']
    canon = lambda x: json.dumps({k: x[k] for k in ('title', 'kind', 'items')},
                                sort_keys=True)
    assert sorted(canon(e) for e in decoded['new'][:len(folds)]) == sorted(
        canon(json.loads(raw('show', before+':'+p))) for p in folds)
    return {'complete': True, 'before': before, 'after': after,
            'paths': sorted(p for s, p in changes), 'folds': folds,
            'all_previous_release_literal_bytes_preserved': True,
            'official_pending_entries_folded_exactly': True}
