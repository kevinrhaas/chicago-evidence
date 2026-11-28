"""Carry a qualified feature through the documented ordinary Dev integration."""
import datetime,hashlib,json,os,stat,subprocess,tempfile,time
from pathlib import Path
from vegetation_core_dev072_native import qualify
from qualify_vegetation_roughness_channel_fix_calibration import qualify as qualify_cal
W=Path('/workspace/work');P='vegetation-roughness-channel-fix'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=read(W/(P+'-final-integration-proof.json'));r=Path(p['repo']);app=r/'chicago/4d'
def git(*a,**kw):return subprocess.check_output(['git',*a],cwd=r,**kw)
def tx(*a):return git(*a).decode().strip()
def raw(ref,path):return git('show',ref+':'+path)
def private(f):
 if f.is_file() and not f.is_symlink() and f.stat().st_nlink>1:
  t=f.with_name(f.name+'.correction-lap-private');assert not t.exists()
  t.write_bytes(f.read_bytes());t.chmod(stat.S_IMODE(f.stat().st_mode));t.replace(f)
n=qualify(P,'m2');c=qualify_cal('m2')
assert p['exact_native_tree_after_authorship'] and n['complete'] and c['complete']
assert p['final_tree']==n['candidate_tree']==c['candidate_tree']
assert tx('rev-parse','HEAD')==p['final_head'] and not tx('status','--porcelain')
for path,h in p['source_sha256'].items():assert sha(r/path)==h,path
for f in Path('/proc').glob('[0-9]*/cmdline'):
 try:a=f.read_bytes().split(b'\0')
 except OSError:continue
 assert not(a and b'/workspace/work/pw-browsers/' in a[0] and any(b'--type=gpu-process' in x for x in a))
 assert not(len(a)>1 and Path(os.fsdecode(a[0])).name=='bash' and a[1] in (b'tools/check.sh',b'./tools/check.sh'))
base=tx('ls-remote','origin','refs/heads/dev').split()[0]
assert base=='a54aeaf9ae1e0e564f05f9a83af723f40dbab83b','Inspect any newer functional upstream change before integration'
subprocess.run(['git','merge-base','--is-ancestor',p['actual_dev'],base],cwd=r,check=True)
saved=W/(P+'-authored-exact-source-proof.json');assert not saved.exists();saved.write_text(json.dumps(p,indent=2)+'\n')
derived={'chicago/4d/data/liberties.json','chicago/4d/docs/measurements/source_use_coverage.md'}
lib='chicago/4d/docs/LIBERTIES.md';note='chicago/4d/changelog.d/T-3747.json'
excluded=derived|{lib}
patch=git('diff','--binary',p['actual_dev'],p['final_head'],'--','.',*[':(exclude)'+x for x in sorted(excluded)])
patch_path=W/(P+'-preserved-feature-edits.patch');assert not patch_path.exists();patch_path.write_bytes(patch)
with tempfile.TemporaryDirectory(prefix=P+'-lap-index-',dir=W) as d:
 env={**os.environ,'GIT_INDEX_FILE':d+'/index'}
 subprocess.run(['git','read-tree',base],cwd=r,env=env,check=True)
 subprocess.run(['git','apply','--cached','--check'],input=patch,cwd=r,env=env,check=True)
 subprocess.run(['git','apply','--cached'],input=patch,cwd=r,env=env,check=True)
 before=git('write-tree',env=env).decode().strip()
 # Reversing the entire unchanged authored patch recovers every upstream byte.
 subprocess.run(['git','apply','--cached','--reverse'],input=patch,cwd=r,env=env,check=True)
 assert git('write-tree',env=env).strip()==git('rev-parse',base+'^{tree}').strip()
paths=set(tx('diff','--name-only',p['final_head'],before).splitlines())|{lib,note}
for step in read(app/'tools/derived_manifest.json')['steps']:
 if step.get('command') in (['python3','tools/compile_liberties.py'],['python3','tools/compile_source_use.py']):paths.update(step['resolves'])
for path in paths:private(r/path)
subprocess.run(['git','read-tree','--reset','-u',before],cwd=r,check=True)
old=raw(p['actual_dev'],lib);ours=raw(p['final_head'],lib);upstream=raw(base,lib)
assert ours.startswith(old) and ours[len(old):].startswith(b'\n### L-leaf-light-3747')
(r/lib).write_bytes(upstream+ours[len(old):])
original_note=read(r/note)
concise={'title':original_note['title'],'kind':original_note['kind'],'items':[
 'Trees have rounded foliage, warmer backlit leaves and finer close twigs in Full.',
 'Plants follow spring, summer, fall and winter across every scene, with evergreen colour and bare winter branches.',
 '1871’s remaining solid crowns become branching trees, keeping their recorded places, sizes and cards.'
]}
assert len(original_note['items'])==len(concise['items'])==3
(r/note).write_text(json.dumps(concise,ensure_ascii=False,indent=2)+'\n')
env={**os.environ,'PATH':str(W/'node22/bin')+':'+str(W/'vegetation-venv/bin')+':'+os.environ['PATH'],'NODE_PATH':str(W/'node22/lib/node_modules')};env.pop('CHICAGO_TICKETS_DIR',None)
checks=[]
for name,cmd in [('derive-liberties',['python3','tools/compile_liberties.py']),('derive-source-use',['python3','tools/compile_source_use.py']),('liberties-check',['python3','tools/compile_liberties.py','--check']),('source-use-check',['python3','tools/compile_source_use.py','--check']),('changelog-contract',['node','tools/check-changelog.mjs']),('pending-notes',['node','tools/changelog-entries.mjs','--check']),('historical-notes',['node','tools/changelog-history.mjs','--base',base])]:
 log=W/(P+'-standard-lap-'+name+'.log');assert not log.exists();start=time.monotonic()
 with log.open('w') as out:rc=subprocess.call(cmd,cwd=app,env=env,stdout=out,stderr=subprocess.STDOUT)
 checks.append({'name':name,'command':cmd,'exit_code':rc,'seconds':round(time.monotonic()-start,1),'log':str(log),'log_sha256':sha(log)})
 assert rc==0,str(log)
own=set(p['source_sha256']);code=set(p['feature_code_sha256'])
subprocess.run(['git','add','-u'],cwd=r,check=True);tree=tx('write-tree')
assert set(tx('diff','--name-only',base,tree).splitlines())==own
assert raw(tree,lib)==upstream+ours[len(old):]
# Every authored code change is exactly the independently applied original patch;
# files touched by both lanes also retain the newly landed upstream code.
for path in code:assert raw(tree,path)==raw(before,path),path
left=json.loads(raw(base,'chicago/4d/data/liberties.json'));right=read(app/'data/liberties.json')
assert isinstance(left,list) and isinstance(right,list)
byid={x['id']:x for x in right};assert all(byid[x['id']]==x for x in left)
assert set(byid)-{x['id'] for x in left}=={'L-leaf-light-3747','L-seasonal-flora-3748','L-1871-grown-context-3760'}
full_patch=git('diff','--binary',base,tree)
with tempfile.TemporaryDirectory(prefix=P+'-lap-reverse-',dir=W) as d:
 e={**os.environ,'GIT_INDEX_FILE':d+'/index'};subprocess.run(['git','read-tree',tree],cwd=r,env=e,check=True)
 subprocess.run(['git','apply','--cached','--reverse'],input=full_patch,cwd=r,env=e,check=True)
 assert git('write-tree',env=e).strip()==git('rev-parse',base+'^{tree}').strip()
head=tx('commit-tree',tree,'-p',p['final_head'],'-p',base,'-m','Integrate qualified Better Trees with current Dev and concise release notes')
subprocess.run(['git','reset','--soft',head],cwd=r,check=True)
assert not tx('status','--porcelain')
patch_name=P+'-integrated-feature.patch';(W/patch_name).write_bytes(full_patch)
out={**p,'final_head':head,'actual_dev':base,'final_tree':tree,'native_to_final_delta':tx('diff','--name-only',p['native_candidate_tree'],tree).splitlines(),
 'source_sha256':{path:sha(r/path) for path in sorted(own)},'feature_code_sha256':{path:sha(r/path) for path in sorted(code)},
 'pre_authorship_feature_code_sha256':p['feature_code_sha256'],'authored_feature_head':p['final_head'],'authored_feature_tree':p['final_tree'],
 'exact_native_tree_after_authorship':False,'authored_feature_tree_exactly_equals_native_tree':True,
 'feature_code_byte_identical_after_authorship':True,'standard_pr_lap_integration':True,'all_feature_edits_preserved_after_standard_lap':True,
 'independently_applied_feature_code_verified':True,'original_feature_patch':patch_path.name,'original_feature_patch_sha256':sha(patch_path),'source_before_metadata_owners':before,
 'upstream_liberties_values_preserved':True,'upstream_liberties_count':len(left),'combined_liberties_count':len(right),
 'pending_release_note_shortened_for_new_upstream_budget':True,'all_previous_release_literal_bytes_preserved':True,
 'integrated_patch':patch_name,'integrated_patch_sha256':hashlib.sha256(full_patch).hexdigest(),'checks':checks,
 'scope':'Corrected entire6b source passed full1441 Native and every eligible actual7763/4 calibration before seasonal feature authorship. Ordinary documented PR-lap integration carries the exact original feature edits over inspected upstream building, release-panel and process changes, preserves all upstream liberty values and canonical owner outputs, and shortens only the pending group note to the new60-word budget. No earlier execution is relabelled. Current integrated-head preflight, actual-merge Native and complete published smoke/frame/memory CI must pass before Dev merge.',
 'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(W/(P+'-final-integration-proof.json')).write_text(json.dumps(out,indent=2)+'\n')
cp=W/'better-trees-current-checkpoint.json';s=read(cp);s['m2'].update(head=head,base=base,standard_lap_integration=True,active_source_proof=P+'-final-integration-proof.json');cp.write_text(json.dumps(s,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','feature_code_sha256','pre_authorship_feature_code_sha256','checks')}),flush=True)
