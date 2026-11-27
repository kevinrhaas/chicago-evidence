"""Check the observed facade on the pre-M1 E21 runtime, without editing sources."""
import datetime,hashlib,json,os,signal,subprocess,time
from pathlib import Path
w=Path('/workspace/work');repo=w/'better-trees-seasons-current';app=repo/'chicago/4d'
pair=json.loads((w/'vegetation-m1-light-cost-paired-diagnostic.json').read_text())
assert pair['complete'] and len(pair['jobs'])==2 and all(r['exit_code']==0 for r in pair['jobs'])
before=pair['jobs'][0];assert before['label']=='before-e21'
site=w/'vegetation-m1-e21-b4-light-cost-diagnostic/before-e21/site/4d'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in before['runtime_sha256'].items():
    f=site/'walk'/p
    if h is None:assert not f.exists()
    else:assert sha(f)==h,p
for p in Path('/proc').glob('[0-9]*/cmdline'):
    try:a=p.read_bytes().split(b'\0')
    except (FileNotFoundError,PermissionError):continue
    assert not (a and b'/workspace/work/pw-browsers/' in a[0] and b'--type=gpu-process' in a),'GPU still owned'
    assert not (len(a)>1 and Path(os.fsdecode(a[0])).name=='bash' and a[1] in [b'tools/check.sh',b'./tools/check.sh']),'Native still owned'
prep=json.loads((w/'vegetation-m2-driver-current-integration-proof.json').read_text())
for p,h in prep['source_sha256'].items():assert sha(repo/p)==h,p
out=w/'vegetation-evidence/e21-1904-spring-material-review';assert not out.exists()
log=w/'vegetation-e21-1904-spring-material-review.log';assert not log.exists()
env={**os.environ,'PATH':str(w/'node22/bin')+':'+os.environ['PATH'],
     'NODE_PATH':str(w/'node22/lib/node_modules'),
     'PW_EXECUTABLE':str(w/'pw-browsers/chromium-1194/chrome-linux/chrome'),
     'QA_SITE':str(site),'QA_OUT':str(out),'QA_TAG':'dev-e21','QA_YEAR':'1904',
     'QA_VIEWPORT':'desktop','QA_STAND':'back_yard','QA_TIERS':'balanced',
     'QA_SEASONS':'spring','QA_PAIRS':'balanced:spring','QA_MODES':'0','QA_FRAMES':'3'}
env.pop('QA_BEFORE',None)
start=time.monotonic()
with log.open('w') as stream:
    child=subprocess.Popen(['node','tools/qa_vegetation_t3747.mjs'],cwd=app,env=env,
                           stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
    try:code=child.wait(timeout=590)
    except subprocess.TimeoutExpired:
        os.killpg(child.pid,signal.SIGTERM)
        try:child.wait(timeout=10)
        except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
        code=124
index=out/'dev-e21-1904-desktop.json';cases=json.loads(index.read_text()) if index.exists() else []
receipt={'runtime_base':pair['base'],'site':str(site),'restored_runtime_sha256':before['runtime_sha256'],
         'paired_runtime_proof_sha256':sha(w/'vegetation-m1-light-cost-paired-diagnostic.json'),
         'exit_code':code,'seconds':round(time.monotonic()-start,1),'cases':cases,
         'log':str(log),'log_sha256':sha(log),'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'note':'Pre-M1 E21 runtime restored from actual Git blobs, identical current assets/data to B4, unchanged stock QA helper, same spring date/camera. Diagnostic of whether dark building faces predate both tree batches; no cause assumed and no source/publication edit.'}
for p,h in prep['source_sha256'].items():assert sha(repo/p)==h,p
assert code==0 and len(cases)==1 and all(not c.get('errors') and not c.get('problems') for c in cases),cases
receipt['captures']={c['image']:sha(out/c['image']) for c in cases}
(w/'vegetation-e21-1904-spring-material-review.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='cases'}),flush=True)
