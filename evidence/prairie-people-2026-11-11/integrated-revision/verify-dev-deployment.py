#!/usr/bin/env python3
"""Verify the deployed dev revision and exact published Prairie runtime inputs."""
import hashlib,json,subprocess,sys,time,urllib.request
from pathlib import Path

expected=sys.argv[1]
assert len(expected)==40 and all(c in '0123456789abcdef' for c in expected)
repo='/workspace/chicago'
subprocess.run(['git','fetch','origin','dev'],cwd=repo,check=True)
dev=subprocess.check_output(['git','rev-parse','origin/dev'],cwd=repo,text=True).strip()
subprocess.run(['git','merge-base','--is-ancestor',expected,dev],cwd=repo,check=True)
base='https://chicago.polecat.live/4d/dev/'
def fetch(path):
    request=urllib.request.Request(base+path+'?verify='+dev+'&nonce='+str(time.time_ns()), headers={'Cache-Control':'no-cache'})
    with urllib.request.urlopen(request,timeout=40) as r:
        assert r.status==200
        return r.read()
build=json.loads(fetch('build.json'))
assert build['tier']=='dev' and build['ref']=='refs/heads/dev',build
assert 7 <= len(build['sha']) <= 40 and all(c in '0123456789abcdef' for c in build['sha']),build
# The automatic changelog fold may land while deployment is in flight. The live
# revision must include this merge and belong to current dev; exact runtime hashes
# below verify the requested application even if a later changelog is still queued.
live=subprocess.check_output(['git','rev-parse','--verify',build['sha']+'^{commit}'],cwd=repo,text=True).strip()
subprocess.run(['git','merge-base','--is-ancestor',expected,live],cwd=repo,check=True)
subprocess.run(['git','merge-base','--is-ancestor',live,dev],cwd=repo,check=True)
manifest=json.loads(Path('/workspace/prairie-younger/integrated-runtime-manifest.json').read_text())
paths={'walk/js/main.js','walk/js/human-days.js','walk/js/human-variation.js',
       'data/humans/inside_1904.json','data/humans/web/hm08_variation_kit.json',
       'data/humans/web/hm08_variation_persons.json'}
verified=[]
for row in manifest['published']:
    if row['path'] not in paths:continue
    data=fetch(row['path'])
    assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
    verified.append(row)
    if row['path']=='data/humans/inside_1904.json':
        people=json.loads(data)
        assert len(people['people'])==397 and len(people['care'])==5
assert len(verified)==6
assert b'1904' in fetch('1904/')
receipt={'verified_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'expected_ancestor':expected,'deployed_dev':live,'latest_dev':dev,'build':build,
         'runtime_inputs':verified,'additional_people':397,'household_care':5,
         'entry_page':'1904/ HTTP 200','result':'PASS'}
out=Path('/workspace/prairie-younger/dev-deployment-verification.json')
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
