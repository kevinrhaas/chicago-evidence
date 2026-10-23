import re

NORMAL={
 '.github/workflows/chicago-4d-check.yml':('gate',['Set up job','Run actions/checkout@v4','Run actions/setup-python@v5','Run actions/setup-node@v4','Install validator dependencies','How many cores this runner has','Run the gate','Does this change carry a changelog entry?','Complete job']),
 '.github/workflows/chicago-4d-moving-frames.yml':('moving-frames',['Set up job','Run actions/checkout@v4','Run actions/setup-node@v4','Install Playwright','Publish the mirror the gate serves (site/4d/ is generated)','Walk, turn, fly and ride; hold the flora frame to its ceilings','A phone keeps the town on the GPU, not twice','Complete job']),
 '.github/workflows/chicago-4d-pr-stuck.yml':('report',['Set up job','Check the secret before doing anything','Run actions/checkout@v4','Report every pull request nothing can move','Complete job']),
 '.github/workflows/chicago-4d-humans.yml':('humans',['Set up job','Run actions/checkout@v4','Run actions/setup-python@v5','Run actions/setup-node@v4','Run pip install --quiet jsonschema','Read the Blender pin','Cache Blender','Rebuild the fixture and require the committed bytes','Install Playwright','Open every human GLB in the browser, at both viewports','Drive the browser actor with the fixture, at both viewports','Complete job']),
}

def need(c,m):
 if not c:raise ValueError(m)

def audit_job(job,run,head,name,required):
 need(job['run_id']==run['id'] and job.get('run_attempt')==1 and job.get('head_sha')==head,'Job identity/attempt drift')
 need(job['name']==name and job['status']=='completed' and job['conclusion']=='success','Job did not succeed')
 steps=job.get('steps',[])
 for wanted in required:
  matches=[s for s in steps if s['name']==wanted]
  need(len(matches)==1 and matches[0]['status']=='completed' and matches[0]['conclusion']=='success','Required actual step did not succeed: '+wanted)
 need(all(s['conclusion']=='success' for s in steps),'Unexpected skipped/failed job step')
 return {'run_id':run['id'],'job_id':job['id'],'job_name':name,'required_steps':required,'PASS':True}

def checkout_sha(text,expected):
    clean=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text)
    lines=[re.sub(r'^\d{4}-\d\d-\d\dT\S+Z\s*','',x) for x in clean.splitlines()]
    values=[]
    for i,line in enumerate(lines):
        if re.fullmatch(r'\[command\].*[/ ]git log -1 --format=%H',line):
            need(i+1<len(lines) and re.fullmatch('[a-f0-9]{40}',lines[i+1]),'Missing exact checkout log SHA')
            values.append(lines[i+1])
    need(values==[expected],'Actual checkout SHA differs or is ambiguous: '+repr(values))
    return values[0]

def audit_human_jobs(jobs,run,head):
    names={j['name']:j for j in jobs}
    need(len(names)==len(jobs) and set(names)=={'humans','teamster-studies'},'Expected normal humans and explicit skipped dependent job')
    skipped=names['teamster-studies']
    need(skipped['run_id']==run['id'] and skipped.get('run_attempt')==1 and skipped.get('head_sha')==head and skipped['status']=='completed' and skipped['conclusion']=='skipped','Normal PR must not rebuild canonical teamster studies')
    name,steps=NORMAL['.github/workflows/chicago-4d-humans.yml']
    proof=audit_job(names[name],run,head,name,steps)
    proof['expected_skipped_dependent_job_id']=skipped['id']
    return names[name],proof
