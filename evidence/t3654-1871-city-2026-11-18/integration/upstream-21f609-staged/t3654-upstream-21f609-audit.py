"""Audit the staged, uncommitted 2027 integration without changing repository files."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path('/workspace/chicago')
BEFORE = json.loads(Path('/tmp/t3654-upstream-21f609-before.json').read_text())
BASE, OURS, DEV = (BEFORE[k] for k in ('merge_base', 'baseline', 'upstream_fold'))

def git(*a, raw=False):
    return subprocess.check_output(['git', *a], cwd=ROOT, text=not raw)

def tree(ref):
    result = {}
    for line in git('ls-tree', '-r', ref).splitlines():
        spec, name = line.split('\t', 1)
        result[name] = spec.split()[2]
    return result

def obj(ref, p):
    return json.loads(git('show', f'{ref}:{p}'))

def changes(a,b):
    return sorted(k for k in set(a)|set(b) if a.get(k)!=b.get(k))

assert git('rev-parse','HEAD').strip()==OURS
assert git('rev-parse','MERGE_HEAD').strip()==DEV
assert git('diff','--name-only','--diff-filter=U').strip()==''
assert git('diff','--name-only').strip()==''
merged=git('write-tree').strip()
current,upstream=tree(merged),tree(DEV)
incoming=set(git('diff','--name-only',BASE,DEV).splitlines())
changed=set(git('diff','--name-only',OURS,merged).splitlines())
assert changed==incoming,(changed-incoming,incoming-changed)
outside=set(BEFORE['all_baseline_blobs'])-incoming
assert all(current.get(p)==BEFORE['all_baseline_blobs'][p] for p in outside)
assert all(current.get(p)==blob for p,blob in BEFORE['protected_1871_prefire_runtime_blobs'].items())

old='house_2027_prairie__draft_1904.glb'
new='house_2027_prairie__as_mapped_1904.glb'
man='chicago/4d/assets/manifest.json'
web='chicago/4d/assets/manifest.web.json'
before_master=obj(OURS,man)['assets'];after_master=obj(merged,man)['assets']
before_web=obj(OURS,web)['masters'];after_web=obj(merged,web)['masters']
assert changes(before_master,after_master)==sorted([old,new])
assert changes(before_web,after_web)==sorted([old,new])
assert after_web[new]==obj(DEV,web)['masters'][new]
strip=lambda row:{k:v for k,v in row.items() if k!='inputs_sha256'}
assert strip(after_master[new])==strip(obj(DEV,man)['assets'][new])
binaries={}
for kind in ('gltf','web'):
    p=f'chicago/4d/assets/{kind}/{new}'
    assert current[p]==upstream[p]
    assert f'chicago/4d/assets/{kind}/{old}' not in current
    raw=git('show',f'{merged}:{p}',raw=True)
    assert (ROOT/p).read_bytes()==raw
    binaries[p]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':current[p],'matches_upstream':True}

source='chicago/4d/data/sidecars/1835/sources/sanborn_1911_chicago_v3_sheet_35.json'
canonical=lambda e:json.dumps(e,sort_keys=True,separators=(',',':'))
sb,so,sd,sm=[obj(ref,source) for ref in (BASE,OURS,DEV,merged)]
eb,eo,ed,em=[set(map(canonical,s['edges'])) for s in (sb,so,sd,sm)]
removed,added=eb-ed,ed-eb
assert em==(eo-removed)|added
context_before=[e for e in so['edges'] if e.get('entity_type','').startswith('context')]
assert all(e in sm['edges'] for e in context_before)

lib='chicago/4d/data/liberties.json'
def liberties(ref):return {e['id']:e for e in obj(ref,lib)['liberties']}
lb,lo,ld,lm=[liberties(ref) for ref in (BASE,OURS,DEV,merged)]
assert changes(lo,lm)==changes(lb,ld)
assert all(lm.get(k)==ld.get(k) for k in changes(lb,ld))

def diff(a,b,path=''):
    if type(a)!=type(b):return [path]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:out.append(path+'/'+k)
            else:out+=diff(a[k],b[k],path+'/'+k)
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [path+'/length']
        return [q for i,(x,y) in enumerate(zip(a,b)) for q in diff(x,y,path+'/'+str(i))]
    return [] if a==b else [path]

doors='chicago/4d/data/humans/doors_1904.json'
do,du,dm=[obj(ref,doors) for ref in (OURS,DEV,merged)]
def by_id(d):return {x['structure']:x for x in d['structures']}
dos,dus,dms=map(by_id,[do,du,dm])
assert changes(dos,dms)==['house_2027_prairie']
new_door_deltas=diff(dus['house_2027_prairie'],dms['house_2027_prairie'])
assert set(new_door_deltas)<={'/model_inputs_sha256','/barrier/key','/floor/key'},new_door_deltas
assert dms['house_2027_prairie']['model_inputs_sha256']==after_master[new]['inputs_sha256']
assert {k:v for k,v in dm.items() if k not in ('structures','barriers')}=={k:v for k,v in du.items() if k not in ('structures','barriers')}
bo,bu,bm=[{x['structure']:x for x in d['barriers']} for d in (do,du,dm)]
assert changes(bo,bm)==['prairie_2027:back_door:stoop']
assert bm['prairie_2027:back_door:stoop']==bu['prairie_2027:back_door:stoop']
assert current['chicago/4d/data/humans/doors_1835.json']==BEFORE['all_baseline_blobs']['chicago/4d/data/humans/doors_1835.json']

exact=sorted(p for p in incoming if current.get(p)==upstream.get(p))
shared=sorted(incoming-set(exact))
receipt={
 'state':'resolved_staged_merge_pending_root_checks_and_commit',
 'recorded_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'baseline':OURS,'merge_base':BASE,'included_upstream':BEFORE['upstream'],'included_fold':DEV,
 'staged_tree':merged,'head_unchanged':True,'committed':False,'pushed':False,
 'changed_paths':sorted(changed),'changed_paths_exactly_upstream_delta':True,
 'all_baseline_paths_outside_upstream_delta_preserved':len(outside),
 'protected_1871_prefire_runtime_paths_preserved':len(BEFORE['protected_1871_prefire_runtime_blobs']),
 'upstream_paths_exact_including_intentional_deletions':exact,
 'shared_files_with_combined_parent_data':shared,
 'incoming_binary_outputs':binaries,
 'registries':{'master_count':len(after_master),'changed_keys':sorted([old,new]),
   'only_new_input_hash_generated_by':'generators/k01_emit.py --only house_2027_prairie',
   'new_input_sha256':after_master[new]['inputs_sha256'],
   'retirement_receipt':'/tmp/t3654-upstream-21f609-registry-retirement.json'},
 'doors':{'1835_unchanged':True,'1904_changed_structure_ids':changes(dos,dms),
   'new_house_differences_from_upstream':new_door_deltas,
   '1904_changed_barrier_ids':changes(bo,bm),'new_back_stoop_exactly_upstream':True,
   'owner_command':'python3 chicago/4d/tools/derive_doors_scene.py'},
 'source_use':{'owner_command':'python3 chicago/4d/tools/compile_source_use.py',
   'baseline_edges':len(eo),'combined_edges':len(em),'upstream_removed':len(removed),'upstream_added':len(added),
   'context_edges_preserved':len(context_before),'set_equals_baseline_plus_upstream_delta':True},
 'liberties_changed_ids':changes(lo,lm),
 'resource_recovery':'/tmp/t3654-upstream-21f609-merge-resource-recovery.json',
 'limits':'No full gate, publication, CI dispatch, commit or push; root owns freshness/derived/source/changelog/publication checks and checkpoint metadata.'}
Path('/tmp/t3654-upstream-21f609-integration.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('staged_tree','changed_paths_exactly_upstream_delta','all_baseline_paths_outside_upstream_delta_preserved','protected_1871_prefire_runtime_paths_preserved','shared_files_with_combined_parent_data')},indent=2))
print(f'Exact upstream paths, including intended deletions: {len(exact)}; protected paths: {len(BEFORE["protected_1871_prefire_runtime_blobs"])}')
