"""Ordinary current-Dev integration, retaining all qualified feature edits."""
import datetime,hashlib,json,os,stat,subprocess,tempfile,time
from pathlib import Path
from vegetation_core_dev072_native import qualify as qualify_native
from qualify_vegetation_roughness_channel_fix_calibration import qualify as qualify_cal
W=Path('/workspace/work');P='vegetation-dev-445';OLD='vegetation-roughness-channel-fix'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
local=read(W/'vegetation-dev-d2b-final-integration-proof.json');previous=read(W/(OLD+'-final-integration-proof.json'));original=read(W/(OLD+'-authored-exact-source-proof.json'));r=Path(previous['repo']);app=r/'chicago/4d'
def git(*a,**kw):return subprocess.check_output(['git',*a],cwd=r,**kw)
def tx(*a):return git(*a).decode().strip()
def raw(ref,path):return git('show',ref+':'+path)
def private(f):
 if f.is_file() and not f.is_symlink() and f.stat().st_nlink>1:
  t=f.with_name(f.name+'.devd2b-private');assert not t.exists();t.write_bytes(f.read_bytes());t.chmod(stat.S_IMODE(f.stat().st_mode));t.replace(f)
n=qualify_native(OLD,'m2');c=qualify_cal('m2');assert n['complete'] and c['complete'] and n['candidate_tree']==c['candidate_tree']==original['final_tree']
assert tx('rev-parse','HEAD')==local['final_head'] and not tx('status','--porcelain')
for path,h in local['source_sha256'].items():assert sha(r/path)==h,path
base='445b43c924dbe4594a88244bb23633829aa3a6e3';assert tx('ls-remote','origin','refs/heads/dev').split()[0]==base,'Inspect any newer upstream first'
subprocess.run(['git','merge-base','--is-ancestor',previous['actual_dev'],base],cwd=r,check=True)
source_patch=W/original.get('original_feature_patch',OLD+'-preserved-feature-edits.patch');patch=source_patch.read_bytes()
with tempfile.TemporaryDirectory(prefix=P+'-index-',dir=W) as d:
 env={**os.environ,'GIT_INDEX_FILE':d+'/index'};subprocess.run(['git','read-tree',base],cwd=r,env=env,check=True)
 subprocess.run(['git','apply','--cached','--check'],input=patch,cwd=r,env=env,check=True);subprocess.run(['git','apply','--cached'],input=patch,cwd=r,env=env,check=True)
 before=git('write-tree',env=env).decode().strip()
 subprocess.run(['git','apply','--cached','--reverse'],input=patch,cwd=r,env=env,check=True);assert git('write-tree',env=env).strip()==git('rev-parse',base+'^{tree}').strip()
lib='chicago/4d/docs/LIBERTIES.md';note='chicago/4d/changelog.d/T-3747.json';check='chicago/4d/tools/check.sh'
paths=set(tx('diff','--name-only',previous['final_head'],before).splitlines())|{lib,note,check}
for step in read(app/'tools/derived_manifest.json')['steps']:
 if step.get('command') in (['python3','tools/compile_liberties.py'],['python3','tools/compile_source_use.py']):paths.update(step['resolves'])
for path in paths:private(r/path)
subprocess.run(['git','read-tree','--reset','-u',before],cwd=r,check=True)
oldlib=raw(original['actual_dev'],lib);ourlib=raw(original['final_tree'],lib);assert ourlib.startswith(oldlib)
(r/lib).write_bytes(raw(base,lib)+ourlib[len(oldlib):]);(r/note).write_bytes(raw(previous['final_head'],note))
# Carry upstream's exact --list repair; its strict audit and ordinary stale gate remain.
resolved=before
env={**os.environ,'PATH':str(W/'node22/bin')+':'+str(W/'vegetation-venv/bin')+':'+os.environ['PATH'],'NODE_PATH':str(W/'node22/lib/node_modules')}
env.pop('CHICAGO_TICKETS_DIR',None);env.pop('GH_TOKEN',None);env.pop('GITHUB_TOKEN',None)
checks=[]
commands=[('restamp-readonly',['python3','tools/restamp_stale.py','--list']),('audit-gate',['python3','tools/audit_check_gates.py','--gate','--quiet']),('audit-self-test',['python3','tools/audit_check_gates.py','--self-test']),('derive-liberties',['python3','tools/compile_liberties.py']),('derive-source-use',['python3','tools/compile_source_use.py']),('liberties-check',['python3','tools/compile_liberties.py','--check']),('source-use-check',['python3','tools/compile_source_use.py','--check']),('changelog-contract',['node','tools/check-changelog.mjs']),('pending-notes',['node','tools/changelog-entries.mjs','--check']),('historical-notes',['node','tools/changelog-history.mjs','--base',base])]
for name,cmd in commands:
 log=W/(P+'-integration-'+name+'.log');assert not log.exists();start=time.monotonic()
 with log.open('w') as out:rc=subprocess.call(cmd,cwd=app,env=env,stdout=out,stderr=subprocess.STDOUT)
 checks.append({'name':name,'command':cmd,'exit_code':rc,'seconds':round(time.monotonic()-start,1),'log':str(log),'log_sha256':sha(log)});assert rc==0,str(log)
own=set(previous['source_sha256']);code=set(previous['feature_code_sha256'])
subprocess.run(['git','add','-u'],cwd=r,check=True);tree=tx('write-tree');assert set(tx('diff','--name-only',base,tree).splitlines())==own
for path in code:assert raw(tree,path)==raw(resolved,path),path
assert raw(tree,lib)==raw(base,lib)+ourlib[len(oldlib):]
left=json.loads(raw(base,'chicago/4d/data/liberties.json'));right=json.loads(raw(tree,'chicago/4d/data/liberties.json'));byid={x['id']:x for x in right['liberties']}
assert all(byid[x['id']]==x for x in left['liberties']) and all(x in right['names'] for x in left['names'])
assert set(byid)-{x['id'] for x in left['liberties']}=={'L-leaf-light-3747','L-seasonal-flora-3748','L-1871-grown-context-3760'} and right['count']==left['count']+3
full_patch=git('diff','--binary',base,tree)
with tempfile.TemporaryDirectory(prefix=P+'-reverse-',dir=W) as d:
 e={**os.environ,'GIT_INDEX_FILE':d+'/index'};subprocess.run(['git','read-tree',tree],cwd=r,env=e,check=True);subprocess.run(['git','apply','--cached','--reverse'],input=full_patch,cwd=r,env=e,check=True);assert git('write-tree',env=e).strip()==git('rev-parse',base+'^{tree}').strip()
head=tx('commit-tree',tree,'-p',previous['final_head'],'-p',base,'-m','Integrate current Dev and its maintenance audit fix with Better Trees')
subprocess.run(['git','reset','--soft',head],cwd=r,check=True);assert not tx('status','--porcelain')
patch_name=P+'-integrated-feature.patch';(W/patch_name).write_bytes(full_patch)
out={**previous,'final_head':head,'actual_dev':base,'final_tree':tree,'native_to_final_delta':tx('diff','--name-only',n['candidate_tree'],tree).splitlines(),'source_sha256':{x:sha(r/x) for x in sorted(own)},'feature_code_sha256':{x:sha(r/x) for x in sorted(code)},'previous_review_head':previous['final_head'],'source_before_metadata_owners':resolved,'source_before_integration_resolution':before,'checks':checks,'integration_resolution_patches':[],'integrated_patch':patch_name,'integrated_patch_sha256':hashlib.sha256(full_patch).hexdigest(),'upstream_liberties_count':left['count'],'combined_liberties_count':right['count'],'scope':'Unchanged qualified tree feature commits, full1441 Native and actual7763/4 readings retain their original6b source. Ordinary PR-lap integration preserves their exact edits over the newly merged cloud-save/classroom/launch UI. The fully retained inherited audit failure is resolved by carrying the exact upstream445 --list repair; Native still validates stale meshes and no audit assertion, baseline exception or performance cap changes. Canonical metadata, upstream values and every feature edit are verified. Fresh combined-head preflight and final CI are required.','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(W/(P+'-final-integration-proof.json')).write_text(json.dumps(out,indent=2)+'\n');cp=W/'better-trees-current-checkpoint.json';s=read(cp);s['m2'].update(head=head,base=base,active_source_proof=P+'-final-integration-proof.json',final_integration_proof=P+'-final-integration-proof.json',active_final_prefix=P);cp.write_text(json.dumps(s,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','feature_code_sha256','pre_authorship_feature_code_sha256','checks','native_to_final_delta')}),flush=True)
