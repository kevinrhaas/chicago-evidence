#!/usr/bin/env python3
"""Offline receipt/byte review after exact-ID collection and fetching claimed bot SHA.

No extraction, execution of archive code, source/index changes or network calls.
This binds the actual native evidence; it does not substitute for native gates.
"""
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile

repo, out = map(Path, sys.argv[1:])
def git(*args):
    return subprocess.check_output(['git', *args], cwd=repo)
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while chunk:=stream.read(1024*1024):h.update(chunk)
    return h.hexdigest()
run=json.loads((out/'run.json').read_text())
source=run['head_sha']; run_id=str(run['id']); attempt=str(run['run_attempt'])
assert run['status']=='completed' and run['conclusion']=='success' and run['event']=='workflow_dispatch'
archives={}
for label in ('bundle','closure'):
    meta=json.loads((out/f'{label}-artifact.json').read_text())
    assert not meta['expired'] and re.fullmatch('sha256:[0-9a-f]{64}',meta['digest'])
    assert sha(out/f'{label}.zip')==meta['digest'].split(':')[1]
    w=meta['workflow_run']
    assert str(w['id'])==run_id and w['head_sha']==source and w['head_branch']=='steward/t1789-people-photoquality-20261026'
    assert w['repository_id']==w['head_repository_id']==run['repository']['id']
    archives[label]=zipfile.ZipFile(out/f'{label}.zip')
bundle=archives['bundle']; closure=archives['closure']
def unique(name):
    rows=[n for n in closure.namelist()if PurePosixPath(n).name==name and not n.endswith('/')]
    assert len(rows)==1,(name,rows)
    return closure.read(rows[0])
manifest_bytes=bundle.read('delivery-manifest.json')
manifest=json.loads(manifest_bytes); family=manifest['family']
assert family in ('dress','teamsters')
assert manifest['source_sha']==manifest['definition_sha']==source
assert manifest['repository']=='kevinrhaas/chicago' and manifest['branch']=='steward/t1789-people-photoquality-20261026'
assert manifest['run_id']==run_id and manifest['run_attempt']==attempt
assert manifest['photographic_accepted'] is False and manifest['production_eligibility_changed'] is False
assert manifest['format']=='canonical_human_delivery_v1'
assert manifest['source_tree']==git('rev-parse',source+'^{tree}').decode().strip()
assert json.loads(unique('installed-manifest.json'))==manifest
seal=json.loads(unique('GATED-TREE.json')); push=json.loads(unique('ACTUAL-PUSH.json'))
artifact=json.loads(unique('artifact.json'))
assert artifact['id']==json.loads((out/'bundle-artifact.json').read_text())['id']
assert artifact['digest']==json.loads((out/'bundle-artifact.json').read_text())['digest']
assert seal['source']==push['source']==source and seal['family']==family
assert str(seal['artifact_id'])==str(artifact['id']) and seal['manifest_sha256']==hashlib.sha256(manifest_bytes).hexdigest()
assert seal['run_id']==run_id and seal['attempt']==attempt
assert seal['returncode']==0 and seal['required_readers']is True and seal['required_base']is True
assert seal['preflight_log_sha256']==hashlib.sha256(unique('native-preflight.log')).hexdigest()
assert b'PREFLIGHT PASS' in unique('native-preflight.log') and b'CHECK PASS' in unique('preflight-check.log')
assert push['TREE']==seal['tree'] and push['auto_ready']is False and push['auto_merge']is False and push['photographic_accepted']is False
bot=push['HEAD']
assert git('rev-parse',bot+'^').decode().strip()==source
assert git('rev-parse',bot+'^{tree}').decode().strip()==seal['tree']
spec=importlib.util.spec_from_file_location('reviewed_delivery',repo/'chicago/4d/tools/human_delivery.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
assert set(git('diff','--name-only',source,bot).decode().splitlines()) <= helper.allowed({'family':family})
expected={target for _,target in helper.spec(family)}
assert len(expected)==(20 if family=='dress'else 60)
members=[n for n in bundle.namelist()if not n.endswith('/')]
assert len(members)==len(set(members)) and set(members)==expected|{'delivery-manifest.json'}
assert len(manifest['files'])==len(expected) and {x['path']for x in manifest['files']}==expected
for row in manifest['files']:
    name=row['path'];p=PurePosixPath(name)
    assert not p.is_absolute() and '..'not in p.parts and p.as_posix()==name
    assert bundle.getinfo(name).file_size==row['bytes']
    h=hashlib.sha256(); blob=hashlib.sha1(f"blob {row['bytes']}\0".encode())
    with bundle.open(name)as stream:
        while chunk:=stream.read(1024*1024):h.update(chunk);blob.update(chunk)
    assert h.hexdigest()==row['sha256'],name
    tree_row=git('ls-tree',bot,'--','chicago/4d/'+name).decode().split()
    assert tree_row[:2]==['100644','blob'] and tree_row[2]==blob.hexdigest(),name
assert set(manifest['source_files'])=={(repo/'chicago/4d'/p).resolve().relative_to(repo).as_posix()for p in helper.SOURCE_FILES}
for name,digest in manifest['source_files'].items():
    assert hashlib.sha256(git('show',source+':'+name)).hexdigest()==digest
    assert git('show',source+':'+name)==git('show',bot+':'+name)
receipt=json.loads(git('show',bot+':chicago/4d/data/humans/canonical-deliveries/'+family+'.json'))
assert all(receipt[k]==v for k,v in manifest.items())
assert receipt['artifact_id']==artifact['id'] and receipt['delivery_manifest_sha256']==seal['manifest_sha256']
assert receipt['artifact_zip_sha256']==artifact['digest'].split(':')[1]
measure=json.loads(git('show',bot+':chicago/4d/data/humans/fixture.measure.json'))
previous=json.loads(git('show',source+':chicago/4d/data/humans/fixture.measure.json'))
expected_hash={x['file']:x['sha256']for x in previous['files']}
expected_hash.update({x['path']:x['sha256']for x in manifest['files']if x['path'].startswith('assets/humans/')})
assert len(measure['files'])==len(expected_hash)==(24 if family=='dress'else 40)
assert {x['file']:x['sha256']for x in measure['files']}==expected_hash
for row in measure['files']:
    verdicts=row['verdicts'];assert isinstance(verdicts,list)and verdicts
    assert all(isinstance(v,dict)and v.get('ok')is True and v.get('check')and'got'in v for v in verdicts)
summary=dict(result='PASS exact native delivery receipt/byte/tree review',family=family,source=source,run_id=run_id,attempt=attempt,artifact_id=artifact['id'],manifest_sha256=seal['manifest_sha256'],bot_HEAD=bot,TREE=seal['tree'],all_asset_measurements=len(measure['files']),bundle_members=len(expected),native_gate_seconds=seal['seconds'],ordinary_PR_CI='UNKNOWN: bot push does not trigger ordinary checks; same-tree normal-auth followup required',photographic_accepted=False)
(out/'REVIEW.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
