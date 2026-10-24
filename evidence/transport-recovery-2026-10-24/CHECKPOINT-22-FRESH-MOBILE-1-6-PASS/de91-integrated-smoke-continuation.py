#!/usr/bin/env python3
import hashlib, json, os, re, subprocess, time
from pathlib import Path

ROOT = Path('/workspace/chicago')
APP = ROOT/'chicago/4d'
LOG = Path('/workspace/.cloud-setup/logs/transport-recovery')
OUT = LOG/'de91-integrated-smoke-continuation-binding.json'
HEAD = 'be56fb269eee6aa7963b8a8d76d5a950f56f857c'
TREE = 'a38d9b3efebb79ba4b3cb7a7c283360fe8139aa5'
assert not OUT.exists(), 'Preserve previous receipts; inspect before resuming'
state = {'head':HEAD, 'tree':TREE, 'incoming_dev':'de91c45b314a705a6cc2fb9430becb666dfbded6',
         'status':'running', 'started_unix':time.time(), 'completed':[],
         'note':'Continue unchanged be56/a38 after explicit1800sdesktop14timeout. Retain only independently verified mobile14pass on identical published bytes. Preserve timeout/browser-closed failure; retry desktop14 last with3600s operationalcap. No assertion or budget weakened.'}
def save():
    tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2)+'\n');tmp.replace(OUT)
def verify():
    for ref,expected in [('HEAD',HEAD),('HEAD^{tree}',TREE)]:
        assert subprocess.check_output(['git','rev-parse',ref],cwd=ROOT).decode().strip()==expected
    subprocess.check_call(['git','diff','--quiet','HEAD'],cwd=ROOT)
    assert json.loads((ROOT/'site/4d/build.json').read_text())['version']==HEAD[:9]
def digest_published():
    rows=[]
    for p in sorted((ROOT/'site/4d').rglob('*')):
        if p.is_file(): rows.append({'path':str(p.relative_to(ROOT/'site/4d')),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()})
    p=LOG/'de91-integrated-published-files.json';assert p.exists();assert json.loads(p.read_text())==rows
    return {'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
verify()
pub=json.loads((LOG/'de91-integrated-head-publish.result.json').read_text())
clean=json.loads((LOG/'de91-integrated-head-publish.cleanup.json').read_text())
assert pub['returncode']==0 and clean['cleanup_complete'] and not clean['remaining_owned_children']
state['published']=digest_published()
prior_path=LOG/'de91-integrated-smoke-binding.json'
prior=json.loads(prior_path.read_text())
assert prior['head']==HEAD and prior['tree']==TREE and prior['status'].startswith('stopped')
retained=[x for x in prior['completed'] if x['verified_pass']]
assert len(retained)==1 and retained[0]['viewport']=='mobile' and retained[0]['stage']=='14'
old=retained[0];prefix=Path(old['prefix'])
result=json.loads(Path(str(prefix)+'.result.json').read_text())
cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text())
text=Path(str(prefix)+'.log').read_text(errors='replace')
count=re.search(r'(\d+) staged-section check\(s\)',text)
assert old['outer_returncode']==0 and result['returncode']==0 and not result['timed_out']
assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
assert count and int(count[1])==old['staged_checks'] and 'SMOKE PASS' in text and 'zero page errors' in text
state['completed']=retained
state['prior_binding']={'path':str(prior_path),'sha256':hashlib.sha256(prior_path.read_bytes()).hexdigest()}
state['prior_incomplete_attempts']=[x for x in prior['completed'] if not x['verified_pass']]
assert len(state['prior_incomplete_attempts'])==1
state['deferred']=[{'viewport':'desktop','stage':'14','reason':'Previous attempt hit1800s operationalcap; induced browser-close suite-completion failure preserved; fresh3600s attempt scheduled after other parts.'}]
save()
legs=[]
legs += [('mobile',s) for s in ['1-2','3-4','5-6','7-8','9-10','11-12','13','15']]
legs += [('desktop',str(s)) for s in range(1,16) if s!=14]
legs += [('desktop','14')]
try:
    for viewport,stage in legs:
        verify()
        prefix=LOG/(f'de91-integrated-smoke-{viewport}-{stage}'+('-after-operational-timeout' if (viewport,stage)==('desktop','14') else ''))
        timeout=3600 if stage in ['13','14'] else 1800
        state['active']={'viewport':viewport,'stage':stage,'prefix':str(prefix),'timeout_seconds':timeout}
        save();print(f'Starting {viewport} {stage}',flush=True)
        outer=subprocess.call(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(APP),'--timeout',str(timeout),'--','env',f'SMOKE_VIEWPORT={viewport}',f'SMOKE_STAGE={stage}','node','tools/smoke_renderer.mjs','--published'])
        result=json.loads(Path(str(prefix)+'.result.json').read_text())
        cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text())
        transcript=Path(str(prefix)+'.log').read_text(errors='replace')
        count=re.search(r'(\d+) staged-section check\(s\)',transcript)
        passed=outer==0 and result['returncode']==0 and not result['timed_out'] and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and count and int(count[1])>0 and 'SMOKE PASS' in transcript and 'zero page errors' in transcript
        record={'viewport':viewport,'stage':stage,'prefix':str(prefix),'outer_returncode':outer,'command_returncode':result['returncode'],'seconds':result['seconds'],'staged_checks':int(count[1]) if count else None,'cleanup_complete':cleanup['cleanup_complete'],'remaining_owned_children':len(cleanup['remaining_owned_children']),'verified_pass':bool(passed),'foreground_budget_seconds':600,'fits_foreground_budget':result['seconds']<=600}
        state['completed'].append(record);state.pop('active',None)
        if (viewport,stage)==('desktop','14') and passed:state.pop('deferred',None)
        save()
        assert passed, f'Actual command/transcript/cleanup failed: {viewport} {stage}'
    verify();assert len(state['completed'])==24
    for viewport in ['mobile','desktop']:
        covered=set()
        for x in state['completed']:
            if x['viewport']!=viewport:continue
            bounds=[int(s) for s in x['stage'].split('-')];covered.update(range(bounds[0],bounds[-1]+1))
        assert covered==set(range(1,16))
    assert not state.get('deferred')
    state['status']='passed: all15parts/bothviewports, zero page errors'
    state['finished_unix']=time.time();save()
except BaseException as error:
    state['status']='stopped; inspect actual failure before resuming';state['error']=str(error);save();raise
