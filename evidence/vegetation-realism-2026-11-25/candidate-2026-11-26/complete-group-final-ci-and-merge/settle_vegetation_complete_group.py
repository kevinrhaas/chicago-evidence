"""Settle all three tickets only after the verified actual group squash."""
import datetime,hashlib,json,os,stat,subprocess
from pathlib import Path
W=Path('/workspace/work');R=W/'better-trees-seasons-current';A=R/'chicago/4d'
T=W/'better-trees-seasons-integration/chicago/4d/tickets'
def read(p):return json.loads(Path(p).read_text())
def git(*a,at=R):return subprocess.check_output(['git',*a],cwd=at,text=True).strip()
m=read(W/'vegetation-complete-group-merge-receipt.json')
p=read(W/m['qualified_integration_proof'])
pr=read(W/'vegetation-complete-group-merged-pr.json')
assert m['merged'] and m['pr']==2414 and m['head']==p['final_head']
assert pr['merged'] and pr['number']==2414 and pr['base']=='dev'
assert pr['head_sha']==m['head'] and pr['merge_commit_sha']==m['merge_sha']
def verify():
 assert git('rev-parse','HEAD')==p['final_head'] and not git('status','--porcelain')
 for path,h in p['source_sha256'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h,path
verify();refs={k:git('rev-parse',k) for k in ['HEAD','origin/dev']}
cp=W/'better-trees-current-checkpoint.json';state=read(cp)
env={**os.environ,'PATH':str(W/'node22/bin')+':'+os.environ['PATH'],'NODE_PATH':str(W/'node22/lib/node_modules'),'CHICAGO_TICKETS_DIR':str(T)}
env.pop('GH_TOKEN',None);env.pop('GITHUB_TOKEN',None)
assert not git('status','--porcelain',at=T)
subprocess.run(['git','fetch','origin','main','--quiet'],cwd=T,check=True)
subprocess.run(['git','merge','--ff-only','origin/main'],cwd=T,check=True)
mirror=R/'site/4d/tickets.json'
if mirror.is_file() and mirror.stat().st_nlink>1:
 t=mirror.with_name(mirror.name+'.complete-group-settle-private');assert not t.exists()
 t.write_bytes(mirror.read_bytes());t.chmod(stat.S_IMODE(mirror.stat().st_mode));t.replace(mirror)
lap=git('ls-remote','origin','refs/heads/lap/pr-2414');released=False
if lap:
 assert lap.split()[0]==state['process']['m2_lap_sha']
 s=subprocess.run(['node','tools/ticket.mjs','lap','2414','--status'],cwd=A,env=env,capture_output=True,text=True)
 assert s.returncode in (0,3) and 'Better Trees season pass ' in s.stdout
 with (W/'vegetation-complete-group-lap-release.log').open('w') as out:
  out.write(s.stdout);out.flush();subprocess.run(['node','tools/ticket.mjs','lap','2414','--release'],cwd=A,env=env,stdout=out,stderr=subprocess.STDOUT,check=True,timeout=120)
 assert not git('ls-remote','origin','refs/heads/lap/pr-2414');released=True
with (W/'vegetation-complete-group-settle.log').open('w') as out:
 subprocess.run(['node','tools/ticket.mjs','settle'],cwd=A,env=env,stdout=out,stderr=subprocess.STDOUT,check=True,timeout=180)
for n in ['T-3747','T-3748','T-3760']:
 f=list(T.rglob(n+'-*.md'));assert len(f)==1
 raw=f[0].read_text();assert '\nstate: done\n' in raw and '\npr: 2414\n' in raw,n
assert not git('status','--porcelain',at=T);verify()
assert refs=={k:git('rev-parse',k) for k in refs}
out={'complete':True,'pr':2414,'head':m['head'],'merge_sha':m['merge_sha'],'tickets_done':['T-3747','T-3748','T-3760'],'own_lap_released':released,'tickets_head':git('rev-parse','HEAD',at=T),'all_feature_source_and_app_refs_unchanged':True,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(W/'vegetation-complete-group-settle-receipt.json').write_text(json.dumps(out,indent=2)+'\n')
state=read(cp);state['process'].update(m2_lap_sha=None,group_lap_released=True,all_three_tickets_settled=True)
state['complete_group']={'merged':True,'pr':2414,'head':m['head'],'merge_sha':m['merge_sha'],'tickets_done':out['tickets_done']}
state['m1'].update(landed_via_pr=2414,ticket_done=True,original_pr_2358_closed_unmerged=True)
state['m2'].update(merged=True,merge_sha=m['merge_sha'],all_three_tickets_done=True)
cp.write_text(json.dumps(state,indent=2)+'\n')
live=W/'better-trees-live-state.json';s=read(live);s.update(app_merged=True,merged_via_pr=2414,merge_sha=m['merge_sha'],time_utc=out['time_utc']);s['complete_group'].update(merged=True,merge_sha=m['merge_sha'],tickets_done=out['tickets_done'],status='Actual expected-head group squash merged to Dev; all three canonical tickets done and owned lap released. Verify served Dev build and retain final CI/merge evidence.');live.write_text(json.dumps(s,indent=2)+'\n')
print(json.dumps(out))
