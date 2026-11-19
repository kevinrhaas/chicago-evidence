import datetime
import hashlib
import json
from pathlib import Path
import subprocess

root = Path('/workspace/chicago-af-prefire-validation')
out = Path('/tmp/t3656-af-prefire-validation')
candidate = '539f09beb735e7555745566667140de72c44b796'
dev = '8c605db0571e29ee9da6d8aba5181451d9d84db8'
def git(*args, at=root):
    return subprocess.check_output(['git','-C',str(at),*args],text=True).strip()
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda:stream.read(1048576),b''): h.update(data)
    return h.hexdigest()
def inventory(path):
    return [{'path':p.relative_to(path).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
            for p in sorted(path.rglob('*')) if p.is_file()]
assert git('rev-parse','HEAD') == candidate
assert git('status','--porcelain') == ''
proof=json.loads(Path('/tmp/t3656-dev8c-dependency-proof.json').read_text())
changed=proof['byteproof']['changed']
rows=[]
for entry in changed:
    rel=entry['path']
    source=root/'chicago/pre_fire_v1'/rel
    production=root/'site/pre-fire'/rel
    preview=root/'site/4d/pre-fire'/rel
    assert git('hash-object',str(source)) == entry['sha']
    assert git('hash-object',str(production)) == entry['sha']
    if rel.startswith('media/'):
        assert not preview.exists(), str(preview)
    else:
        assert git('hash-object',str(preview)) == entry['sha']
    rows.append({'path':rel,'git_blob':entry['sha'],'bytes':entry['size'],
                 'sha256':digest(source),'source_site_equal':True,
                 'preview_equal':True if rel.startswith('viewer/') else None,
                 'root_served_pruned':rel.startswith('media/')})
prefire=inventory(root/'site/4d/pre-fire')
(out/'published-prefire-inventory.json').write_text(json.dumps(prefire,indent=2)+'\n')
totals={}
for name in ['site/4d','site/pre-fire','site']:
    files=[p for p in (root/name).rglob('*') if p.is_file()]
    totals[name]={'files':len(files),'bytes':sum(p.stat().st_size for p in files)}
primary=Path('/workspace/chicago')
previous=json.loads(Path('/tmp/t3658-347-mobile-2-12/mirror-inventory.json').read_text())
current_paths={p.relative_to(primary/'site/4d').as_posix() for p in (primary/'site/4d').rglob('*') if p.is_file()}
assert current_paths == {r['path'] for r in previous}
differences=[]
for row in previous:
    p=primary/'site/4d'/row['path']
    if p.stat().st_size != row['size'] or digest(p) != row['sha256']:
        differences.append(row['path'])
assert not differences, differences
assert git('rev-parse','HEAD',at=primary) == '3472ec872d00e33761490b0138b23da1c63daee2'
assert git('rev-parse','origin/dev',at=primary) == 'c676aa2f4ad6ee8cff0521da6ba8add70d55949c'
assert git('status','--porcelain',at=primary) == ''
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'candidate_commit':candidate,'candidate_tree':git('rev-parse','HEAD^{tree}'),
        'dev_base':dev,'tickets_head':git('rev-parse','HEAD',at=root/'chicago/4d/tickets'),
        'candidate_tracked_status':git('status','--porcelain'),
        'new_prefire_blobs':rows,'publication_totals':totals,
        'root_served_js':(root/'site/4d/pre-fire/viewer/root-served.js').read_text(),
        'primary_preservation':{'full_content_rechecked':True,'file_count':len(previous),
             'bytes':sum(r['size'] for r in previous),'differences':differences,
             'equal_to_inventory':'/tmp/t3658-347-mobile-2-12/mirror-inventory.json',
             'reference_inventory_sha256':'89d0794baf108252fb5c21f2fe2d48bdca878af2b0a338482b2fc1a4faa3cfb0',
             'head':'3472ec872d00e33761490b0138b23da1c63daee2',
             'origin_dev':'c676aa2f4ad6ee8cff0521da6ba8add70d55949c','tracked_status':''}}
(out/'publication-proof.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'publication_totals':totals,'verified_changed_paths':len(rows),
                  'primary_preservation':result['primary_preservation']},indent=2))
