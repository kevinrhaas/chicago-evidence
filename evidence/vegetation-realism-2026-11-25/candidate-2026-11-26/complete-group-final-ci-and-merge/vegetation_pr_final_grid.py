"""Verify retention of every successful stock report on this exact PR head."""
import hashlib,json,zipfile
from pathlib import Path
W=Path('/workspace/work')
def qualify(prefix):
    push=json.loads((W/(prefix+'-push-dispatch.json')).read_text())
    names={'still-frame-desktop','still-frame-mobile'}
    names|={f'memory-{year}-{profile}' for year in (1812,1835,1904) for profile in ('desktop','mobile','shared','chromebook')}
    names.add('memory-1835-self-test');assert len(names)==15
    missing=[];rows=[]
    for name in sorted(names):
        d=W/(prefix+'-final-ci')/'grid'/name
        files=['artifact.zip','artifact.json','job.json',name+'.json']
        if not all((d/f).is_file() for f in files):missing.append(name);continue
        artifact=json.loads((d/'artifact.json').read_text());job=json.loads((d/'job.json').read_text())
        assert artifact['name']==name and not artifact['expired']
        assert artifact['workflow_run']['id']==push['ci_runs']['standard_grid']
        assert artifact['workflow_run']['head_sha']==push['head']
        assert job['run_id']==push['ci_runs']['standard_grid'] and job['head_sha']==push['head']
        assert job['head_branch']==push['branch'] and job['status']=='completed' and job['conclusion']=='success'
        assert hashlib.sha256((d/'artifact.zip').read_bytes()).hexdigest()==artifact['digest'].split(':',1)[1]
        with zipfile.ZipFile(d/'artifact.zip') as z:
            assert z.namelist()==[name+'.json'] and z.read(name+'.json')==(d/(name+'.json')).read_bytes()
        json.loads((d/(name+'.json')).read_text())
        rows.append({'name':name,'job_id':job['id'],'files_sha256':{f:hashlib.sha256((d/f).read_bytes()).hexdigest() for f in files}})
    return {'complete':not missing,'head':push['head'],'run_id':push['ci_runs']['standard_grid'],'expected_reports':15,'missing_reports':missing,'reports':rows}
