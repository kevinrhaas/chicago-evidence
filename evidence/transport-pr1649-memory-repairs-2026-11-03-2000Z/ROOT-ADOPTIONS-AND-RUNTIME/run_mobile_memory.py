from pathlib import Path
import fcntl, hashlib, importlib.util, json, os, subprocess, sys

R=Path('/workspace/chicago-transport-current-20261103');A=R/'chicago/4d'
year=sys.argv[1];assert year in ['1812','1904'];D=Path(sys.argv[2]);D.mkdir(exist_ok=False)
def save(name,obj): (D/name).write_text(json.dumps(obj,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),timeout=20)
def source():
    assert not git('ls-files','-u').strip() and not git('diff','--name-only').strip()
    tree=git('write-tree').decode().strip()
    return dict(HEAD=git('rev-parse','HEAD').decode().strip(),MERGE_HEAD=git('rev-parse','MERGE_HEAD').decode().strip(),TREE=tree,APP=git('rev-parse',tree+':chicago/4d').decode().strip(),semantic_index_sha256=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest())
lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
spec=importlib.util.spec_from_file_location('guard',Path(__file__).parent/'resource_guard.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
original=source();save('SOURCE-BEFORE.json',original)
browser='/workspace/.cloud-setup/transport-browser141-20261103/chromium_headless_shell-1194/chrome-linux/headless_shell'
version=subprocess.check_output([browser,'--version'],timeout=5).decode().strip();assert version=='Chromium 141.0.7390.37'
env=dict(os.environ,PW_EXECUTABLE=browser,PLAYWRIGHT_BROWSERS_PATH='/workspace/.cloud-setup/transport-browser141-20261103',PYTHONDONTWRITEBYTECODE='1');env.pop('CHICAGO_TICKETS_DIR',None)
meter=A/'tools/measure_memory.mjs';ceilings=A/'tools/memory_ceilings.json'
meter_hash=hashlib.sha256(meter.read_bytes()).hexdigest();ceiling_hash=hashlib.sha256(ceilings.read_bytes()).hexdigest()
assert meter_hash=='bff9aea2fd77ee4f7d18399642829d296e2d5a0e217b8fb82223ecba6e5935d3'
assert ceiling_hash=='c400e0fa99011046ca889b30643697c650b9d3f375f0673728505ac4de2a292b'
ledger=[];status='RUNNING_ORIGINAL_NATIVE_MOBILE_MEMORY'
save('STATE.json',dict(status=status,source=original,year=year,browser_version=version))
try:
    commands=[('publish',['bash','tools/publish.sh'],180),('published-check',['node','tools/check_published.mjs'],120),('memory',['node','tools/measure_memory.mjs','--gate','--year',year,'--only','mobile','--json',str(D/'memory.json')],600)]
    for label,command,cap in commands:
        assert source()==original
        before=g.snapshot();assert g.check(before)['accepted'];prefix=D/label
        save('STATE.json',dict(status=status,active_label=label,source=original,year=year))
        q=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(A),'--timeout',str(cap),'--',*command],env=env,stdout=Path(str(prefix)+'.stdout').open('xb'),stderr=subprocess.STDOUT)
        result=json.loads(Path(str(prefix)+'.result.json').read_text());cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text());resources=g.pair(before,g.snapshot())
        row=dict(label=label,command=command,result=result,cleanup=cleanup,resources=resources,source_after=source());ledger.append(row);save('LEDGER.json',ledger)
        assert not result['timed_out'] and result['effective_timeout_seconds']==cap and result['timeout_override_reason']is None and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted'] and source()==original
        if q.returncode!=0 or result['returncode']!=0:
            status='ACTUAL_NATIVE_'+year+'_MOBILE_MEMORY_NONPASS' if label=='memory' else 'PUBLICATION_NONPASS'
            break
    else:status='ACTUAL_NATIVE_'+year+'_MOBILE_MEMORY_PASS'
except BaseException as error:
    save('CLOSED-NONPASS.json',dict(status='RUNNER_STOPPED_NONPASS',error=repr(error),source_before=original,ledger=ledger));raise
receipt=dict(status=status,source_before=original,source_after=source(),year=year,browser_version=version,meter_sha256=meter_hash,ceilings_sha256=ceiling_hash,ledger=ledger)
if (D/'memory.json').exists():receipt['native_memory_report']=json.loads((D/'memory.json').read_text())
save('CLOSED.json',receipt);print(json.dumps({'status':status,'receipt':str(D/'CLOSED.json')}));raise SystemExit(0 if status.endswith('_PASS') else 1)
