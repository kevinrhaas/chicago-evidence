import base64, datetime, json, subprocess, time
from pathlib import Path
p=Path('/tmp/jail-native-run-monitor-20261103'); p.mkdir(exist_ok=True)
expected='https://github.com/kevinrhaas/polecat-platform/actions/runs/41734994705'
def api(path):
 r=subprocess.run(['gh','api',path],capture_output=True,check=True,timeout=25)
 return json.loads(r.stdout)
previous=None; discovery_previous=None
for i in range(90):
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  j=api('repos/kevinrhaas/polecat-platform/actions/jobs/126261776333')
  t=api('repos/kevinrhaas/chicago-tickets/contents/T-2250-2499/T-2380-match-the-log-jail-to-its-pictures.md?ref=main')
  b=base64.b64decode(t['content']).decode(); h=b.split('\n---\n',1)[0]
  state={'status':j['status'],'conclusion':j['conclusion'],'active_or_failed':[x for x in j['steps'] if x['status']=='in_progress' or x['conclusion'] not in [None,'success','skipped']],'ticket_blob':t['sha'],'ticket_header':h}
  snapshot={'observed':now,'job_id':j['id'],**state}
  (p/'LATEST-POLL.json').write_text(json.dumps(snapshot,indent=2)+'\n'); (p/'T2380-LATEST.md').write_text(b)
  with (p/'POLL-HISTORY.jsonl').open('a') as f:f.write(json.dumps(snapshot)+'\n')
  if state!=previous:
   print(json.dumps({'transition':snapshot}),flush=True);previous=state
  if j['labels']!=['ubuntu-26.04'] or ('state: claimed\n' in h and f'claimed_run: {expected}\n' not in h):
   print(json.dumps({'ALERT':'Unexpected worker label or other run owns claimed ticket','snapshot':snapshot}),flush=True);break
  if i%7==0 or j['status']=='completed':
   prs=api('search/issues?q=repo:kevinrhaas/chicago+is:pr+is:open+%22T-2380%22')
   refs=api('repos/kevinrhaas/chicago/git/matching-refs/heads/steward/t2380')
   artifacts=api('repos/kevinrhaas/polecat-platform/actions/runs/41734994705/artifacts')
   discovery={'prs':[{'number':x['number'],'title':x['title'],'url':x['html_url'],'updated_at':x['updated_at']} for x in prs['items']],'refs':refs,'artifacts':artifacts}
   (p/'LATEST-DISCOVERY.json').write_text(json.dumps({'observed':now,**discovery},indent=2)+'\n')
   if discovery!=discovery_previous:print(json.dumps({'discovery':{'observed':now,**discovery}}),flush=True);discovery_previous=discovery
  if j['status']=='completed':break
 except Exception as error:print(json.dumps({'poll_error':str(error),'observed':now}),flush=True)
 if i<89:time.sleep(45)
