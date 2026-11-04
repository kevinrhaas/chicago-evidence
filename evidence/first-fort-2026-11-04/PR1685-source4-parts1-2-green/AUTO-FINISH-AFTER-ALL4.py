from pathlib import Path
import os,subprocess,json,time,hashlib
P=Path(__file__).parent;Q=P/'source4-final-corrected';R=Path('/workspace/chicago-bridge-increment-20261102');A=R/'chicago/4d';F=P/'qualified-push';F.mkdir(exist_ok=True);H='c8562a164f1df66a42f33457ac4ff65e1ed6111b';D='96d0612d940e3652af24875674a2e17feeb38184';BR='steward/t3041-ne-house-pyramid-roof';E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1',C4D_GATE_REQUIRE_READERS='1',C4D_GATE_REQUIRE_BASE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES','CHICAGO_TICKETS_DIR']:E.pop(k,None)
def git(*x):return subprocess.check_output(['/usr/local/bin/git','-C',str(R),*x],env=E)
def dump(name,d):(F/name).write_text(json.dumps(d,indent=2)+'\n')
def native(tag,cmd,cwd=A):
 with(F/(tag+'.log')).open('xb')as log:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(F/(tag+'-REAPER.json')),'--','timeout','--signal=TERM','--kill-after=15s','600s','nice','-n','19','taskset','-c','2',*cmd],cwd=cwd,env=E,stdout=log,stderr=subprocess.STDOUT)
 proof=json.loads((F/(tag+'-REAPER.json')).read_bytes());assert r.returncode==proof['command_exit']==0 and proof['all_children_reaped']and not proof['leftover_cleanup'],tag
 print(tag+' PASS',flush=True)
# Wait only for this exact active controller; never fabricate, override or rerun a verdict.
while not(Q/'SOURCE4-PASS.json').exists():
 rr=json.loads((Q/'SOURCE4-OUTER-REAPER.json').read_bytes())
 assert rr['command_exit']is None,'Final source4 stopped without all4PASS; inspect receipts'
 time.sleep(5)
full=json.loads((Q/'SOURCE4-PASS.json').read_bytes());assert full['all4_green']and len(full['parts'])==4
assert all(x['exit']==0 and x['source_exact']and x['reaper']['all_children_reaped']and not x['reaper']['leftover_cleanup']for x in full['parts'])
assert git('rev-parse','HEAD').decode().strip()==H and git('rev-parse','MERGE_HEAD').decode().strip()==D and git('write-tree').decode().strip()==full['source']['index_tree']
assert not git('diff','--name-only')and not git('diff','--name-only','--diff-filter=U')
pr=json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/pulls/1685'],env=E));assert pr['head']['sha']==H and pr['head']['ref']==BR and pr['base']['ref']=='dev'and pr['state']=='open';dump('REMOTE-PR-BEFORE.json',{'head':pr['head']['sha'],'base':pr['base']['sha'],'branch':pr['head']['ref']})
message="""Merge dev into T-3041 NE small-house pyramid increment

Preserve current lowered Dearborn bridge, Pruyne/1835 plan changes and
Sauganash metadata alongside the genuine pinned native 243-outbuilding bake.
Resolve only entrywise manifest/source indexes and both liberty appends.
Re-render the two affected jail reviews and the current 14-member first-fort
view; retain their existing DIFFERS verdicts and all open discrepancies.

Correct the native worker's attribution: 179 default MASTERs have only unused
UVs repacked; positions, normals, colours, material bindings, indices and
mesh/node topology are exact. All 243 current recipes and MASTER/WEB blobs
match the native build; only the intended NE roof WEB changed.

All four complete source parts passed on the exact staged tree before this
commit. Hosted gate and actual final app review follow; T-3041 remains partial
and T-2387 remains split. This is not original-ticket completion.
""";(F/'COMMIT-MESSAGE.txt').write_text(message)
native('commit',['/usr/local/bin/git','commit','--file',str(F/'COMMIT-MESSAGE.txt')],R)
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();assert tree==full['source']['index_tree'];assert not git('status','--porcelain','--untracked-files=normal');parents=git('show','-s','--format=%P','HEAD').decode().split();assert parents==[H,D];dump('QUALIFIED-COMMIT.json',{'head':head,'tree':tree,'parents':parents,'all4_source_green':True,'source_guard':full['source'],'runtime_pending':True,'original_ticket_partial':True})
native('changelog-entry',['node','tools/check-changelog-entry.mjs',D,head]);native('id-collisions',['node','tools/resolve_id_collisions.mjs','--base',D,'--check'])
native('push',['/usr/local/bin/git','push','origin','HEAD:refs/heads/'+BR],R)
remote=json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/git/ref/heads/'+BR],env=E))['object']['sha'];assert remote==head;dump('PUSHED.json',{'head':head,'tree':tree,'branch':BR,'normal_fast_forward':True,'readback_exact':True,'PR':1685})
native('gate-dispatch',['gh','workflow','run','chicago-4d-check.yml','--repo','kevinrhaas/chicago','--ref',BR],R)
for attempt in range(12):
 runs=json.loads(subprocess.check_output(['gh','api','repos/kevinrhaas/chicago/actions/workflows/chicago-4d-check.yml/runs?event=workflow_dispatch&head_sha='+head+'&per_page=10'],env=E))['workflow_runs'];runs=[x for x in runs if x['head_sha']==head and x['head_branch']==BR]
 if runs:break
 time.sleep(3)
assert runs,'Dispatch succeeded but run not yet observed; inspect before redispatch'
dump('NAMED-GATE-RUN.json',{'run':runs[0]['id'],'head':head,'url':runs[0]['html_url'],'status':runs[0]['status'],'name':runs[0]['name'],'must_require_actual_gate_success':True});print('GATE '+runs[0]['html_url'],flush=True)
native('publish',['bash','tools/publish.sh']);native('published-contract',['node','tools/check_published.mjs'])
assert not git('status','--porcelain','--untracked-files=normal');build=json.loads((R/'site/4d/build.json').read_bytes());assert head.startswith(build['version']);dump('READY-FOR-RUNTIME.json',{'head':head,'tree':tree,'publication':str(R/'site/4d'),'published_version':build['version'],'PR':1685,'gate_run':runs[0]['id'],'source4_green':True,'PR_only_preflight_green':True,'normal_FF_pushed':True,'runtime_pending':True,'ordinary_merge_not_authorized_until_actual_runtime_and_root_review':True});print('READY-FOR-RUNTIME '+head+' '+tree,flush=True)
