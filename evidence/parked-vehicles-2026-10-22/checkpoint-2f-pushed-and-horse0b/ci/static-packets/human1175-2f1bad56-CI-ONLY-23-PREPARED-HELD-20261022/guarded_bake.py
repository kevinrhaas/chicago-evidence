"""Narrow ownership-skip audit for pinned cf7e706a workflow; no actual build allowed."""
import re
BAKE='.github/workflows/chicago-4d-bake.yml'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def audit_guarded_bake_jobs(jobs,run,head):
 names={j['name']:j for j in jobs};need(len(names)==len(jobs)==6 and set(names)=={'warranted','bake','smoke','open-pr','publish-bundle','fresh-consumer'},'Expected exact ownership-guard and five skipped dependent jobs')
 for job in jobs:need(job['run_id']==run['id'] and job.get('run_attempt')==1 and job.get('head_sha')==head and job['status']=='completed','Guard job identity/attempt/completion drift')
 skipped=[names[k] for k in ['bake','smoke','open-pr','publish-bundle','fresh-consumer']]
 need(all(j['conclusion']=='skipped' and not j.get('steps') for j in skipped),'Actual bake/downstream execution is NOT the expected source-owned=false guard')
 job=names['warranted'];need(job['conclusion']=='success','Ownership guard did not succeed')
 expected={1:('Set up job','success'),2:('Run actions/checkout@v4','success'),3:('Run actions/setup-python@v5','success'),4:('Run set -uo pipefail','success'),5:('Run set -uo pipefail','skipped'),9:('Post Run actions/setup-python@v5','success'),10:('Post Run actions/checkout@v4','success'),11:('Complete job','success')}
 steps={s['number']:s for s in job.get('steps',[])};need(len(steps)==len(job.get('steps',[])) and set(steps)==set(expected),'Exact q/live guard step inventory differs')
 for number,(name,conclusion) in expected.items():need(steps[number]['name']==name and steps[number]['status']=='completed' and steps[number]['conclusion']==conclusion,'Guard q/live/post step differs at '+str(number))
 return job,{'run_id':run['id'],'job_id':job['id'],'job_name':'warranted','PASS':True,'source_owned':False,'expected_skipped_dependent_job_ids':[j['id'] for j in skipped],'q_success_step_number':4,'live_skipped_step_number':5}
def audit_guarded_bake_log(text):
 clean=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text);lines=[re.sub(r'^\d{4}-\d\d-\d\dT\S+Z\s*','',line) for line in clean.splitlines()]
 notices=['##[notice]SKIPPING — nothing this branch owns under generators/, tools/bake.sh','##[notice]or this workflow differs from dev. Any generators change here came',"##[notice]in with the PR lap's merge, and dev's own bake covers it."]
 need(all(lines.count(line)==1 for line in notices),'Actual source-ownership skip notice missing/ambiguous; other skip reasons do not qualify')
 for name,value in [('BASE','dev'),('EV','push'),('REF','steward/1835-workwear-repair-20261021')]:need(len(re.findall(r'^\s*'+name+': '+re.escape(value)+r'\s*$','\n'.join(lines),re.M))==1,'Ownership guard event/ref/base differs')
 return {'actual_source_ownership_skip_notice':True,'source_owned':False,'bake_not_executed':True}
