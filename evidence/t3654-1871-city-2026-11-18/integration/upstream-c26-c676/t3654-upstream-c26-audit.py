import datetime as dt
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path('/workspace/1871-upstream-75bf')
OURS = '871698ae94659100fcb8894f4967d4b15c62150f'
DEV = 'c26d33718ecb68cbed172d8b549cce720af71b56'
BASE = '169404c9f99d2defeca2b05f2364c868a4f4e745'

def git(*args, text=True):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=text)

def paths(a, b):
    return git('diff', '--name-only', a, b).splitlines()

def tree(ref):
    result = {}
    for line in git('ls-tree', '-r', ref).splitlines():
        spec, name = line.split('\t', 1)
        result[name] = spec.split()[2]
    return result

def obj(ref, p):
    return json.loads(git('show', f'{ref}:{p}'))

def change_keys(before, after):
    return sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))

merged = git('write-tree').strip()
trees = {ref: tree(ref) for ref in (BASE, OURS, DEV, merged)}
upstream_paths = paths(BASE, DEV)
changed = paths(OURS, merged)
assert changed == upstream_paths, (set(changed)-set(upstream_paths), set(upstream_paths)-set(changed))
outside = set(trees[OURS]) - set(upstream_paths)
assert all(trees[OURS][p] == trees[merged].get(p) for p in outside)
baseline_delta = set(paths(BASE, OURS))
unshared_baseline = sorted(baseline_delta-set(upstream_paths))
assert all(trees[OURS].get(p) == trees[merged].get(p) for p in unshared_baseline)
epoch_paths = sorted(p for p in trees[OURS] if '1871' in p or p.startswith('chicago/pre_fire_v1/')
                     or p.endswith(('/city-context.js', '/world.js', '/scene-loader.js')))
assert all(trees[OURS][p] == trees[merged].get(p) for p in epoch_paths)

master = 'chicago/4d/assets/manifest.json'
web = 'chicago/4d/assets/manifest.web.json'
target = 'fort_dearborn_massacre_monument_1893__on_18th_street_1893.glb'
ma, mm, md = [obj(ref, master)['assets'] for ref in (OURS, merged, DEV)]
wa, wm, wd = [obj(ref, web)['masters'] for ref in (OURS, merged, DEV)]
assert change_keys(ma, mm) == [target]
assert change_keys(wa, wm) == [target]
assert wm[target] == wd[target]
strip = lambda e: {k:v for k,v in e.items() if k != 'inputs_sha256'}
assert strip(mm[target]) == strip(md[target])

shared_sources = [p for p in upstream_paths if p.startswith('chicago/4d/data/sidecars/1835/sources/')
                  and trees[merged][p] != trees[DEV][p]]
assert len(shared_sources) == 4
source_receipts = []
canonical = lambda e: json.dumps(e, sort_keys=True, separators=(',', ':'))
for p in shared_sources:
    before, ours, dev, after = [obj(ref,p) for ref in (BASE,OURS,DEV,merged)]
    sets = [set(map(canonical,d['edges'])) for d in (before,ours,dev,after)]
    removed, added = sets[0]-sets[2], sets[2]-sets[0]
    assert sets[3] == (sets[1]-removed)|added
    context_before = [e for e in ours['edges'] if e.get('entity_type','').startswith('context')]
    assert all(e in after['edges'] for e in context_before)
    source_receipts.append({'path':p,'baseline_edges':len(sets[1]),'combined_edges':len(sets[3]),
                            'upstream_removed_edges':len(removed),'upstream_added_edges':len(added),
                            'context_edges_preserved':len(context_before)})

lib='chicago/4d/data/liberties.json'
def libs(ref): return {e['id']:e for e in obj(ref,lib)['liberties']}
lb,lo,ld,lm=[libs(ref) for ref in (BASE,OURS,DEV,merged)]
lib_changed=change_keys(lb,ld)
assert change_keys(lo,lm)==lib_changed
assert all(lm[k]==ld[k] for k in lib_changed)

binary={}
for p in upstream_paths:
    if p.endswith(('.glb','.jpg')):
        assert trees[DEV][p]==trees[merged][p]
        raw=git('show',f'{merged}:{p}',text=False)
        binary[p]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                   'git_blob':trees[merged][p],'matches_dev':True}
exact=[p for p in upstream_paths if trees[DEV].get(p)==trees[merged].get(p)]
exceptions=sorted(set(upstream_paths)-set(exact))
assert set(exceptions)=={master,web,lib,'chicago/4d/docs/LIBERTIES.md',*shared_sources}

out={
 'state':'coherent_merge_pending_root_full_checks',
 'generated_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'worktree':str(ROOT),'baseline':OURS,'upstream_dev':DEV,'merge_base':BASE,
 'merged_tree':merged,'changed_paths':changed,
 'changed_paths_exactly_upstream_set':True,
 'baseline_paths_outside_upstream_delta_preserved':len(outside),
 'baseline_feature_paths_preserved':len(unshared_baseline),
 '1871_and_prefire_paths_preserved':epoch_paths,
 'upstream_paths_preserved_exactly':exact,
 'shared_files_combining_both_parents':exceptions,
 'upstream_binary_outputs':binary,
 'master_registry':{'asset_count':len(mm),'changed_entries':[target],
                    'input_sha256':mm[target]['inputs_sha256'],
                    'method':'merge_asset_registry.py --resolve; pure emitter rebuilt byte-identical upstream GLB on merged tree'},
 'web_registry':'Only monument entry changed against baseline; its value equals upstream dev.',
 'source_use_merge':source_receipts,
 'liberties_changed_entries':lib_changed,
 'source_use_resolution':{
   'attempt':'node tools/rederive.mjs --resolve',
   'sparse_precondition':'Resolver stopped before publish because sparse checkout omits committed audio and most assets; no full publish attempted thereafter.',
   'owner_command':'python3 tools/compile_source_use.py',
   'result':'All four conflicting files regenerated from combined sources and complete GeoJSON inputs; no hand-merged output.'},
 'pushed':False,
 'limits':'No full source gate, full publish, global asset freshness or browser runs in sparse worktree. Root must run final checks after fast-forward.'
}
dest=pathlib.Path('/tmp/t3654-upstream-c26-integration.json')
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('merged_tree','changed_paths_exactly_upstream_set','baseline_paths_outside_upstream_delta_preserved','baseline_feature_paths_preserved')},indent=2))
print(f'{len(epoch_paths)} epoch/prefire paths unchanged; {len(exact)} upstream paths byte-identical; {len(binary)} binary assets/photos preserved')
