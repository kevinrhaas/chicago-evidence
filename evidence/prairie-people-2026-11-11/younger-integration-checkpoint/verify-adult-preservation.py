import json, subprocess
from pathlib import Path
root=Path('/workspace/chicago/chicago/4d')
def baseline(p):
    return json.loads(subprocess.check_output(['git','show','c7de594a7:chicago/4d/'+p],cwd=root,text=True))
def current(p):
    return json.loads((root/p).read_text())
old=baseline('data/humans/inside_1904.json')['people']
new={p['person']:p for p in current('data/humans/inside_1904.json')['people']}
assert len(old)==362
for p in old:
    assert new[p['person']]==p, 'Adult routine changed: '+p['person']
    path='data/humans/variation/looks/'+p['person']+'.json'
    assert current(path)==baseline(path), 'Adult appearance changed: '+p['person']
print('PASS: all 362 adult routine and appearance records are unchanged from c7de594a7')
