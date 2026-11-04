"""API-only bounded native-fort observer; status55s, source discovery every5samples."""
from pathlib import Path
import json,subprocess,time,datetime,argparse
P=Path(__file__).resolve().parent
TASKS=json.loads((P/'TASKS.json').read_text())
HEAD='aa9d7d2322d3abbc78d72526146c018a241c643e'
ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=72);ap.add_argument('--interval',type=int,default=55);args=ap.parse_args()
assert json.loads(Path('/tmp/fort-ne-native-handoff-20261103/MONITOR-CLOSED.json').read_text())['latest']['our_exact_claim']
assert json.loads(Path('/tmp/second-fort-native-handoff-20261103/MONITOR-CLOSED.json').read_text())['latest']['our_exact_claim']
def api(path):return json.loads(subprocess.check_output(['gh','api',path],timeout=30))
def dump(name,obj):
 f=P/name;t=P/(name+'.tmp');t.write_text(json.dumps(obj,indent=2)+'\n');t.replace(f)
last_health={};last_source={};snapshots=[];events=json.loads((P/'PRIOR-EVENTS.json').read_text())if(P/'PRIOR-EVENTS.json').exists()else[];final=None
for event in events:
 row=event['data']
 if event['type']=='HEALTH_TRANSITION':last_health[row['ticket']]=(row.get('status'),row.get('conclusion'),row.get('active_step'),tuple(row.get('failed_steps',[])),row.get('read_error'))
 if event['type']=='SOURCE_DISCOVERY':last_source[row['ticket']]=json.dumps({k:row[k]for k in ['PRs','topic_refs','artifacts']},sort_keys=True)
for i in range(args.samples):
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat();health=[];source=[];force_discovery=False;TASKS=json.loads((P/'TASKS.json').read_text())
 for task in TASKS:assert json.loads(Path(task['claim_closed_receipt']).read_text())['latest']['our_exact_claim']
 for task in TASKS:
  try:
   j=api('repos/kevinrhaas/polecat-platform/actions/jobs/'+str(task['job']));assert j['run_id']==task['run']and j['head_sha']==HEAD and'ubuntu-26.04'in j['labels'];step=next((x['name']for x in j['steps']if x['status']=='in_progress'),None)
   row={**task,'utc':utc,'head':j['head_sha'],'status':j['status'],'conclusion':j['conclusion'],'active_step':step,'failed_steps':[x['name']for x in j['steps']if x['conclusion']=='failure'],'completed_steps':[x['name']for x in j['steps']if x['status']=='completed'],'labels':j['labels']}
  except Exception as exc:row={**task,'utc':utc,'read_error':repr(exc)}
  health.append(row);sig=(row.get('status'),row.get('conclusion'),row.get('active_step'),tuple(row.get('failed_steps',[])),row.get('read_error'))
  if sig!=last_health.get(task['ticket']):
   event={'type':'HEALTH_TRANSITION','data':row};events.append(event);print(json.dumps(event),flush=True);last_health[task['ticket']]=sig
   if row.get('failed_steps')or row.get('status')=='completed':force_discovery=True
 if i%5==0 or force_discovery:
  try:prs=api('repos/kevinrhaas/chicago/pulls?state=all&sort=updated&direction=desc&per_page=100')
  except Exception as exc:prs=[];events.append({'type':'SOURCE_READ_ERROR','utc':utc,'error':repr(exc)})
  for task in TASKS:
   try:
    matches=[{'number':x['number'],'url':x['html_url'],'title':x['title'],'state':x['state'],'draft':x['draft'],'head':x['head']['sha'],'branch':x['head']['ref'],'base':x['base']['ref'],'updated':x['updated_at'],'merged_at':x['merged_at']}for x in prs if(task['ticket'].lower()in(x['title']+' '+x['head']['ref']).lower()or task['prefix']in x['head']['ref'].lower())and(x['state']=='open'or datetime.datetime.fromisoformat(x['updated_at'].replace('Z','+00:00'))>=datetime.datetime.fromisoformat(task['source_after_utc']))]
    refs=api('repos/kevinrhaas/chicago/git/matching-refs/heads/steward/'+task['prefix']);art=api('repos/kevinrhaas/polecat-platform/actions/runs/'+str(task['run'])+'/artifacts')['artifacts']
    row={**task,'utc':utc,'PRs':matches,'topic_refs':[{'ref':x['ref'],'sha':x['object']['sha']}for x in refs if task.get('known_finished_refs',{}).get(x['ref'])!=x['object']['sha']],'artifacts':[{'id':x['id'],'name':x['name'],'bytes':x['size_in_bytes'],'expired':x['expired'],'created':x['created_at']}for x in art]}
    sig=json.dumps({k:row[k]for k in ['PRs','topic_refs','artifacts']},sort_keys=True)
    if sig!=last_source.get(task['ticket']):
     event={'type':'SOURCE_DISCOVERY','data':row};events.append(event);print(json.dumps(event),flush=True);last_source[task['ticket']]=sig
   except Exception as exc:row={**task,'utc':utc,'source_read_error':repr(exc)}
   source.append(row)
 snap={'sample':i+1,'utc':utc,'health':health,'source_discovery':source};snapshots.append(snap);dump('LATEST.json',snap);dump('SNAPSHOTS.json',snapshots);dump('EVENTS.json',events)
 if len(health)==len(TASKS)and all(x.get('status')=='completed'for x in health):final='ALL_MONITORED_NATIVE_JOBS_COMPLETED';break
 if i+1<args.samples:time.sleep(args.interval)
dump('CLOSED.json',{'reason':final or'BOUNDED_OBSERVATION_WINDOW_COMPLETE','samples':len(snapshots),'latest':snapshots[-1],'API_only':True,'repository_ticket_run_mutations':False,'actual_geometry_or_gate_completion_claimed':False})
