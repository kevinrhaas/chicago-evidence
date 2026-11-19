#!/usr/bin/env python3
"""Dispatch the six explicitly authorized groups; preserve each ID before the next."""
import datetime,hashlib,json,re,subprocess,sys,time
from pathlib import Path
ROOT=Path('/workspace/chicago')
REPO='kevinrhaas/chicago'
BRANCH='steward/t3654-1871-city-baseline'
LEDGER=Path('/tmp/t3654-legacy-coverage-ledger.json')
GROUPS=[('desktop','13'),('desktop','1-8'),('mobile','1-12'),('mobile','13-15'),('desktop','9-12'),('desktop','14-15')]
def run(args,cwd=ROOT):return subprocess.check_output(args,cwd=cwd,text=True).strip()
def gh(*args):return run(['/usr/bin/gh',*args])
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(doc):
 p=LEDGER.with_suffix('.next.json');p.write_text(json.dumps(doc,indent=2)+'\n');p.replace(LEDGER)
def rows():
 return json.loads(gh('run','list','--repo',REPO,'--workflow','chicago-4d-smoke.yml','--branch',BRANCH,'--event','workflow_dispatch','--limit','30','--json','databaseId,headSha,status,conclusion,createdAt,url'))
def identity(a):
 if run(['git','rev-parse','HEAD'])!=a['head'] or run(['git','rev-parse','HEAD^{tree}'])!=a['tree']:raise SystemExit('Local identity changed; stop.')
 if run(['git','status','--porcelain','--untracked-files=no']):raise SystemExit('Tracked checkout is dirty; stop.')
 if gh('api',f'repos/{REPO}/git/ref/heads/{BRANCH}','--jq','.object.sha')!=a['head']:raise SystemExit('Remote task head changed; stop.')
 if gh('api',f'repos/{REPO}/git/ref/heads/dev','--jq','.object.sha')!=a['base']:raise SystemExit('Live dev advanced; stop.')
def main():
 if len(sys.argv)!=2:raise SystemExit('Pass the immutable exact-head root authorization JSON.')
 ap=Path(sys.argv[1]);a=json.loads(ap.read_text())
 if (a.get('schema')!='t3654-six-browser-authorization-v1' or a.get('authorized') is not True or a.get('repository')!=REPO or a.get('branch')!=BRANCH or a.get('pull_request')!=2198 or a.get('hosted_source_required_before_merge') is not True):raise SystemExit('Exact-head root authorization is missing.')
 for key in ('head','tree','base'):
  if not re.fullmatch('[0-9a-f]{40}',a.get(key,'')):raise SystemExit('Invalid bound Git identity.')
 if a.get('helper_sha256')!=hashlib.sha256(Path(__file__).read_bytes()).hexdigest():raise SystemExit('Helper differs from authorized bytes.')
 for item in a['focused_and_publication_artifacts']:
  if hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()!=item['sha256']:raise SystemExit('Authorized artifact changed.')
 focused=json.loads(Path(a['focused_receipt']).read_text());published=json.loads(Path(a['publication_receipt']).read_text())
 if focused.get('complete') is not True or len(focused['checks'])!=6 or any(c['exit_code']!=0 for c in focused['checks']):raise SystemExit('Focused checks incomplete.')
 if published.get('complete') is not True or published.get('head')!=a['head'] or published.get('tree')!=a['tree'] or published.get('base')!=a['base'] or any(c['exit_code']!=0 for c in published['checks']):raise SystemExit('Exact-head publication incomplete.')
 identity(a)
 measured=run(['node','tools/dev-smoke-state.mjs','hash'],ROOT/'chicago/4d')
 if a['runtime_input_hash'] not in re.findall(r'sha256:[0-9a-f]+',measured):raise SystemExit('Runtime input hash changed.')
 doc=json.loads(LEDGER.read_text())
 if doc.get('source_task_commit')!=a['head'] or doc.get('included_dev_base')!=a['base'] or doc.get('runtime_input_hash')!=a['runtime_input_hash'] or doc.get('dispatch_hold'):raise SystemExit('Ledger identity differs or remains held.')
 if [(g['viewport'],g['stage']) for g in doc['ci_plan']]!=GROUPS:raise SystemExit('Unexpected stage grouping.')
 cells=[(g['viewport'],p) for g in doc['ci_plan'] for p in g['parts']]
 if len(cells)!=30 or set(cells)!={(v,p) for v in ['mobile','desktop'] for p in range(1,16)}:raise SystemExit('Coverage is not exactly30 unique cells.')
 doc['dispatch_authorization']={'path':str(ap),'sha256':hashlib.sha256(ap.read_bytes()).hexdigest(),'checked_at':stamp(),'hosted_source_required_before_merge':True};save(doc)
 for group in doc['ci_plan']:
  if group.get('run_id'):
   if group.get('head_sha')!=a['head']:raise SystemExit('Existing ID belongs to another head.')
   continue
  if group['status']!='pending_dispatch':raise SystemExit('Unassigned row requires reconciliation; do not blindly retry.')
  identity(a)
  before={r['databaseId'] for r in rows()};group.update(status='dispatching',dispatch_started_at=stamp(),dispatch_prior_ids=sorted(before));save(doc)
  gh('workflow','run','chicago-4d-smoke.yml','--repo',REPO,'--ref',BRANCH,'-f',f"viewport={group['viewport']}",'-f',f"stage={group['stage']}")
  deadline=time.monotonic()+40
  while True:
   fresh=[r for r in rows() if r['databaseId'] not in before]
   if len(fresh)>1:raise SystemExit('Multiple new IDs: reconcile before any further dispatch.')
   if fresh:
    r=fresh[0]
    if r['headSha']!=a['head']:raise SystemExit('New workflow head differs; stop.')
    group.update(run_id=r['databaseId'],head_sha=r['headSha'],status=r['status'],conclusion=r['conclusion'],created_at=r['createdAt'],url=r['url']);save(doc)
    print(f"{group['viewport']} {group['stage']}: {r['databaseId']} {r['status']}",flush=True);break
   if time.monotonic()>=deadline:raise SystemExit('New ID not yet visible: reconcile saved prior IDs, never blindly retry.')
   time.sleep(2)
if __name__=='__main__':main()
