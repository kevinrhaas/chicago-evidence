"""Compare stock Light timing on immutable E21/B4 runtime snapshots; no waiver."""
import datetime, hashlib, json, os, shutil, signal, stat, subprocess, time
from pathlib import Path
w=Path('/workspace/work');repo=w/'better-trees-integration';app=repo/'chicago/4d'
pre=json.loads((w/'vegetation-m1-memoryfix-preflight-receipt.json').read_text())
base=pre['base'];head=pre['head'];assert head=='b4cd05e12b3c2c113583682b9ba0eda27c37bfb8'
done=json.loads((w/'vegetation-m2-driver-core-baseline-1904-material-review.json').read_text());assert done['exit_code']==0
frozen=json.loads((w/'vegetation-m2-driver-paired-before-publication-frozen.json').read_text());archive=Path(frozen['root'])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
def verify_archive():
    for p,h in frozen['sha256'].items():assert sha(archive/p)==h,p
verify_archive()
for p in Path('/proc').glob('[0-9]*/cmdline'):
    try:a=p.read_bytes().split(b'\0')
    except (FileNotFoundError,PermissionError):continue
    assert not (a and b'/workspace/work/pw-browsers/' in a[0] and b'--type=gpu-process' in a),'GPU still owned'
    assert not (len(a)>1 and Path(os.fsdecode(a[0])).name=='bash' and a[1] in [b'tools/check.sh',b'./tools/check.sh']),'Native still owned'
delta=git('diff','--name-only',base,head,'--','chicago/4d/renderers/web/js').decode().splitlines()
assert delta and all(p.endswith('.js') for p in delta)
root=w/'vegetation-m1-e21-b4-light-cost-diagnostic';assert not root.exists();root.mkdir()
receipt={'base':base,'head':head,'runtime_delta_paths':delta,'jobs':[],
         'purpose':'Diagnostic paired stock Light timing only. No calibrated EPYC failure is waived. No app source, stock helper, frame count, geometry, population, radius, raster setting or ceiling is edited. Both sides use identical current assets/data and the stock measurement helper. Only the complete authored M1 runtime delta is restored to actual E21 on BEFORE. Other served runtime is byte-identical B4.',
         'timing_helper_sha256':sha(app/'tools/measure_still_frame.mjs'),
         'local_cpu_is_not_the_failed_epyc_runner':True}
env={**os.environ,'PATH':str(w/'node22/bin')+':'+os.environ['PATH'],
     'NODE_PATH':str(w/'node22/lib/node_modules'),
     'PW_EXECUTABLE':str(w/'pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell')}
for label,ref in [('before-e21',base),('after-b4',head)]:
    at=root/label;site=at/'site/4d';site.parent.mkdir(parents=True)
    # Matches are linked only to an independently immutable archive, never active publication.
    shutil.copytree(archive,site,copy_function=os.link,symlinks=True)
    runtime_hashes={}
    for p in delta:
        rel=Path(p).relative_to('chicago/4d/renderers/web');target=site/'walk'/rel
        candidate=git('show',head+':'+p);assert target.read_bytes()==candidate,p
        exists=subprocess.run(['git','cat-file','-e',ref+':'+p],cwd=repo,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
        if not exists:
            target.unlink();runtime_hashes[str(rel)]=None;continue
        raw=git('show',ref+':'+p)
        if target.read_bytes()!=raw:
            temp=target.with_name(target.name+'.diagnostic-private');assert not temp.exists()
            temp.write_bytes(raw);temp.chmod(stat.S_IMODE(target.stat().st_mode));temp.replace(target)
        runtime_hashes[str(rel)]=sha(target)
    tools=at/'chicago/4d/tools';tools.mkdir(parents=True)
    for name in ['measure_still_frame.mjs','still_frame_ceilings.json']:shutil.copy2(app/'tools'/name,tools/name)
    assert sha(tools/'measure_still_frame.mjs')==receipt['timing_helper_sha256']
    log=w/f'vegetation-m1-light-cost-{label}.log';result=w/f'vegetation-m1-light-cost-{label}.json'
    assert not log.exists() and not result.exists()
    # Reporting mode selects the identical stock gate stand and Light workload.
    # This is deliberately not represented as passing the complete calibrated gate.
    args=['node','tools/measure_still_frame.mjs','--year','1835','--only','desktop',
          '--tiers','light','--stands','town_backyard','--json',str(result)]
    start=time.monotonic();print('Starting',label,flush=True)
    with log.open('w') as stream:
        child=subprocess.Popen(args,cwd=tools.parent,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
        try:code=child.wait(timeout=590)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGTERM)
            try:child.wait(timeout=10)
            except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
            code=124
    row={'label':label,'runtime_ref':ref,'runtime_sha256':runtime_hashes,'command':args,'exit_code':code,
         'seconds':round(time.monotonic()-start,1),'log':str(log),'log_sha256':sha(log),
         'result':str(result),'result_sha256':sha(result) if result.exists() else None}
    receipt['jobs'].append(row);receipt['time_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt['complete']=len(receipt['jobs'])==2 and all(r['exit_code']==0 for r in receipt['jobs'])
    (w/'vegetation-m1-light-cost-paired-diagnostic.json').write_text(json.dumps(receipt,indent=2)+'\n')
    verify_archive();print(json.dumps(row),flush=True)
    if code:raise SystemExit(code)
print('Both diagnostic reports complete. Original calibrated failure still blocks merging.',flush=True)
