import hashlib,json,subprocess,sys,datetime,shutil
from pathlib import Path
APP=Path('/tmp/chicago-transport-resume-20261029/chicago/4d');REPO=APP.parent.parent;OUT=Path(__file__).parent
phase=sys.argv[1]
commands={'lib144':[['python','tools/compile_liberties.py'],['python','tools/compile_liberties.py','--check']], 'prerequisite-publish':[['bash','tools/publish.sh'],['node','tools/check_published.mjs'],['node','tools/write_year_packs.mjs','--check','../../site/4d']], 'sourceuse152-tail':[['node','tools/rederive.mjs','--tail','tools/compile_source_use.py']], 'affected-readers':[['python','tools/compile_source_use.py','--check'],['python','tools/report_research_signoff.py','--check'],['python','tools/audit_check_gates.py','--gate','--quiet'],['python','tools/human_contract.py','--check'],['node','tools/human_fixture.mjs','--check'],['python','tools/human_natural_idle.py','--check']], 'final-publish':[['bash','tools/publish.sh'],['node','tools/check_published.mjs'],['node','tools/write_year_packs.mjs','--check','../../site/4d']]}[phase]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((APP/'tools/derived_manifest.json').read_text());steps=manifest['steps'];first=next(i for i,s in enumerate(steps) if s['command'][1]=='tools/compile_source_use.py')
allowed=set(steps[143]['resolves'])|{p for s in steps[first:] for p in s['resolves']}|{'chicago/4d/tools/derived_manifest.json'}
paths=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=REPO,text=True).splitlines();protected=sorted(set(p for p in paths if p not in allowed)|{'chicago/4d/tools/compile_liberties.py','chicago/4d/tools/compile_source_use.py','chicago/4d/tools/rederive.mjs','chicago/4d/tools/publish.sh'})
before={p:sha(REPO/p) for p in protected};index_before=subprocess.check_output(['git','ls-files','-s','-z'],cwd=REPO)
resource={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'headroom_bytes':int(Path('/sys/fs/cgroup/memory.max').read_text())-int(Path('/sys/fs/cgroup/memory.current').read_text()),'workspace_free_bytes':shutil.disk_usage('/workspace').free,'tmp_free_bytes':shutil.disk_usage('/tmp').free}
(OUT/(phase+'-RESOURCE.json')).write_text(json.dumps(resource,indent=2)+'\n')
assert resource['headroom_bytes']>=2*1024**3 and resource['workspace_free_bytes']>=512*1024**2 and resource['tmp_free_bytes']>=1024**3,'resource guard failed'
rc=1
try:
 for cmd in commands:
  print('NATIVE-COMMAND '+repr(cmd),flush=True);subprocess.run(cmd,cwd=APP,check=True)
 rc=0
finally:
 after={p:sha(REPO/p) for p in protected};index_after=subprocess.check_output(['git','ls-files','-s','-z'],cwd=REPO)
 changed=set(subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).splitlines());unexpected=sorted(changed-set(paths)-allowed)
 guard={'phase':phase,'actual_commands':commands,'returncode':rc,'protected_source_pins_before':before,'protected_source_pins_after':after,'all_protected_exact':before==after,'semantic_index_exact':index_before==index_after,'unexpected_changed_paths':unexpected,'allowed_native_output_count':len(allowed),'scope':'Native owner regeneration/publication only, not browser/world/fullgate acceptance.'}
 (OUT/(phase+'-GUARDS.json')).write_text(json.dumps(guard,indent=2)+'\n')
 assert before==after and index_before==index_after and not unexpected,'source/index/output ownership guard failed'
