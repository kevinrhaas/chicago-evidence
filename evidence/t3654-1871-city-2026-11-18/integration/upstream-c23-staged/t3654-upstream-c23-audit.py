"""Audit the staged c23 integration without changing the application or index."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path('/workspace/chicago')
BEFORE=json.loads(Path('/tmp/t3654-upstream-c23-before.json').read_text())
BASE,OURS,DEV=(BEFORE[k] for k in ('merge_base','baseline','upstream'))

def git(*a,raw=False):return subprocess.check_output(['git',*a],cwd=ROOT,text=not raw)
def obj(ref,p):return json.loads(git('show',f'{ref}:{p}'))
def changes(a,b):return sorted(k for k in set(a)|set(b) if a.get(k)!=b.get(k))
def tree(ref):
    result={}
    for line in git('ls-tree','-r',ref).splitlines():
        spec,name=line.split('\t',1);result[name]=spec.split()[2]
    return result

assert git('rev-parse','HEAD').strip()==OURS
assert git('rev-parse','MERGE_HEAD').strip()==DEV
assert git('diff','--name-only','--diff-filter=U').strip()==''
assert git('diff','--name-only').strip()==''
merged=git('write-tree').strip();current,upstream=tree(merged),tree(DEV)
incoming=set(git('diff','--name-only',BASE,DEV).splitlines())
changed=set(git('diff','--name-only',OURS,merged).splitlines())
assert changed==incoming,(changed-incoming,incoming-changed)
outside=set(BEFORE['all_baseline_blobs'])-incoming
assert all(current.get(p)==BEFORE['all_baseline_blobs'][p] for p in outside)
assert all(current.get(p)==blob for p,blob in BEFORE['protected_1871_prefire_runtime_blobs'].items())

target='sears_meeker_house_1815_prairie__as_mapped_1904.glb'
master='chicago/4d/assets/manifest.json';web='chicago/4d/assets/manifest.web.json'
mo,md,mm=[obj(ref,master)['assets'] for ref in (OURS,DEV,merged)]
wo,wd,wm=[obj(ref,web)['masters'] for ref in (OURS,DEV,merged)]
assert changes(mo,mm)==[target]
assert changes(wo,wm)==[target]
assert wm[target]==wd[target]
strip=lambda row:{k:v for k,v in row.items() if k!='inputs_sha256'}
assert strip(mm[target])==strip(md[target])
binary={}
for p in sorted(incoming):
    if p.endswith(('.glb','.jpg')):
        assert current[p]==upstream[p]
        raw=git('show',f'{merged}:{p}',raw=True)
        assert (ROOT/p).read_bytes()==raw
        binary[p]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':current[p],'matches_upstream':True}

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
do,dd,dm=[obj(ref,doors) for ref in (OURS,DEV,merged)]
so,sd,sm=[{s['structure']:s for s in d['structures']} for d in (do,dd,dm)]
structure='sears_meeker_house_1815_prairie'
assert changes(so,sm)==[structure]
door_deltas=diff(so[structure],sm[structure]);dev_deltas=diff(sd[structure],sm[structure])
assert set(door_deltas)=={'/model_inputs_sha256','/barrier/key','/floor/key'},door_deltas
assert set(dev_deltas)=={'/model_inputs_sha256','/barrier/key','/floor/key'},dev_deltas
assert sm[structure]['model_inputs_sha256']==mm[target]['inputs_sha256']
assert {k:v for k,v in do.items() if k!='structures'}=={k:v for k,v in dm.items() if k!='structures'}
assert current['chicago/4d/data/humans/doors_1835.json']==BEFORE['all_baseline_blobs']['chicago/4d/data/humans/doors_1835.json']

smoke='chicago/4d/tools/smoke_renderer.mjs'
def line_edits(a,b):
    lines=git('diff','--unified=0',a,b,'--',smoke).splitlines()
    return {'added':[s for s in lines if s.startswith('+') and not s.startswith('+++')],
            'removed':[s for s in lines if s.startswith('-') and not s.startswith('---')]}
edits=line_edits(OURS,merged)
assert edits==line_edits(BASE,DEV)
assert len(edits['added'])==15 and not edits['removed']

exact=sorted(p for p in incoming if current.get(p)==upstream.get(p))
shared=sorted(incoming-set(exact))
assert set(shared)=={master,web,doors,smoke}
receipt={
 'state':'resolved_staged_merge_pending_root_checks_and_commit',
 'recorded_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'baseline':OURS,'merge_base':BASE,'upstream':DEV,'staged_tree':merged,
 'head_unchanged':True,'committed':False,'pushed':False,
 'changed_paths':sorted(changed),'changed_paths_exactly_upstream_delta':True,
 'baseline_paths_outside_upstream_delta_preserved':len(outside),
 'protected_1871_prefire_renderer_paths_preserved':len(BEFORE['protected_1871_prefire_runtime_blobs']),
 'upstream_paths_byte_identical':exact,'shared_files_combining_parent_changes':shared,
 'incoming_binary_outputs':binary,
 'registry':{'changed_entries':[target],'combined_input_sha256':mm[target]['inputs_sha256'],
   'method':'Unmodified merge_asset_registry.py --resolve re-emitted through K01 and required every GLB byte-identical'},
 'doors':{'1835_unchanged':True,'1904_changed_structure_ids':[structure],
   'changed_fields_against_baseline':door_deltas,'changed_fields_against_upstream':dev_deltas,
   'all_2027_house_and_stoop_rows_preserved':True,'all_other_top_level_data_unchanged':True},
 'smoke_harness':{'upstream_additions_preserved_exactly':15,'baseline_lines_removed':0,
   'old_1871_additions_preserved':True,'change':'Wait for picture work before part15 nav=jump reload; page-error assertion unchanged'},
 'source_use':'No incoming changes; every source-use file preserved byte-for-byte; no regeneration needed',
 'focused_check_suggestions':[
   'python3 tools/validate.py --stale',
   'python3 generators/k01_emit.py --only house_2027_prairie,sears_meeker_house_1815_prairie --check',
   'python3 tools/derive_doors_scene.py --check',
   'python3 tools/compile_source_use.py --check',
   'python3 tools/compile_liberties.py --check',
   'python3 tools/jaunt_built_so_far.py --check',
   'python3 tools/compile_jaunts.py --check',
   'node tools/rederive.mjs --check',
   'node tools/check-changelog.mjs',
   'node tools/changelog-entries.mjs --check',
   'node --check tools/smoke_renderer.mjs',
   'python3 tools/measure_web_derivatives.py --gate --quiet'],
 'limits':'No full gate, publication, browser, CI dispatch, commit or push. Root owns validation and final checkpoint. New smoke harness bytes require a newly bound browser run.'}
receipt['logs']={}
for name in ('merge','registry','doors-build'):
    p=Path('/tmp/t3654-upstream-c23-'+name+'.log');raw=p.read_bytes()
    receipt['logs'][name]={'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
Path('/tmp/t3654-upstream-c23-integration.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('staged_tree','changed_paths_exactly_upstream_delta','baseline_paths_outside_upstream_delta_preserved','protected_1871_prefire_renderer_paths_preserved','shared_files_combining_parent_changes')},indent=2))
print(f'{len(exact)} upstream paths byte-identical; {len(binary)} incoming assets/photo proofs preserved.')
