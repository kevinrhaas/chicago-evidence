import json,os,subprocess,time
from pathlib import Path
ROOT=Path('/workspace/chicago-smoke-infra-t3121');LOG=Path('/workspace/.cloud-setup/logs/transport-recovery');H='84272d6e0c7e9da3a72dde76b080de71783fd212';B='abb1dd407a96cf64b9b04735cca432129342beb2';Q='2158db01731a6b3c7c12f53c7bd7b3a7ed0703b3';TREE='4a2c75629c545d8be63dcd0ab8f328603539994b';env=os.environ.copy();env.pop('GH_REST_MERGE_BLIND',None)
def cmd(args):return subprocess.check_output(args,cwd=ROOT,env=env,text=True)
def api(path,method=None,body=None):
 args=['gh','api','repos/kevinrhaas/chicago/'+path]
 if method:args+=['--method',method]
 if body is not None:
  f=LOG/'t3121-normal-merge-api-input.json';f.write_text(json.dumps(body)+'\n');args+=['--input',str(f)]
 return json.loads(cmd(args))
def guard(ready=False):
 refs={l.split()[1]:l.split()[0]for l in cmd(['git','ls-remote','origin','refs/heads/dev','refs/pull/1284/head','refs/pull/1284/merge','refs/heads/lap/pr-1284']).splitlines()}
 assert refs['refs/heads/dev']==B and refs['refs/pull/1284/head']==H and refs['refs/pull/1284/merge']==Q
 assert 'codex-transport-recovery'in cmd(['git','show','-s','--format=%B',refs['refs/heads/lap/pr-1284']])
 p=api('pulls/1284');assert p['state']=='open'and p['head']['sha']==H and p['base']['sha']==B and p['merge_commit_sha']==Q and p['mergeable']and p['mergeable_state']=='clean'and not any(x['name']=='hold'for x in p['labels'])
 if ready:assert not p['draft']
 for ref in [Q,H]:assert cmd(['git','rev-parse',ref+'^{tree}']).strip()==TREE
 c=api('commits/'+H+'/check-runs?per_page=100');assert c['total_count']==len(c['check_runs'])and c['total_count']>0
 assert all(x['status']=='completed'and x['conclusion']in ['success','skipped','neutral']for x in c['check_runs'])and any(x['name']=='gate'and x['conclusion']=='success'for x in c['check_runs'])
 r=api('actions/runs/40121257436');assert r['head_sha']==H and r['conclusion']=='success'
 return {'native_refs':refs,'checks':[{'name':x['name'],'status':x['status'],'conclusion':x['conclusion'],'id':x['id']}for x in c['check_runs']],'run':r['id'],'head':H,'merge':Q,'tree':TREE,'base':B,'blind_override_unset':True,'guarded_at_unix':time.time()}
pre=guard();(LOG/'t3121-normal-merge-pre-ready-guard.json').write_text(json.dumps(pre,indent=2)+'\n')
body=(LOG/'T3121-CURRENT-BASE-PR-BODY.md').read_text().replace('Fresh normal hosted CI is pending;','Fresh normal hosted gate40121257436, report and content checks passed. The original gate log confirms checkoutQ2158db01731a6b3c7c12f53c7bd7b3a7ed0703b3, tree4a2c7562, 1,065 steps /384self-tests and the workflow-only changelog exemption. No feature-head full smoke was started;').replace('Draft while the fresh hosted checks complete.','Fresh hosted verification complete; ordinary SHA-pinned DEV merge next.')
api('pulls/1284','PATCH',{'body':body});(LOG/'T3121-MERGE-READY-PR-BODY.md').write_text(body)
ready=cmd(['gh','pr','ready','1284','--repo','kevinrhaas/chicago']);(LOG/'t3121-normal-ready-receipt.log').write_text(ready)
pre=guard(True);(LOG/'t3121-normal-merge-final-guard.json').write_text(json.dumps(pre,indent=2)+'\n')
r=api('pulls/1284/merge','PUT',{'sha':H,'merge_method':'squash'});(LOG/'t3121-ordinary-sha-pinned-merge-result.json').write_text(json.dumps(r,indent=2)+'\n');assert r.get('merged')is True,r;print(json.dumps(r))
