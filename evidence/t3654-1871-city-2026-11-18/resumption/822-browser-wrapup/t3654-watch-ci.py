import json,time,subprocess,datetime
from pathlib import Path
ledger=Path('/tmp/t3654-legacy-coverage-ledger.json')
prior={}
while True:
    d=json.loads(ledger.read_text()); targets=d['ci_plan']+d['supporting_ci']
    r=subprocess.run(['gh','run','list','--repo','kevinrhaas/chicago','--branch','steward/t3654-1871-city-baseline','--limit','60','--json','databaseId,name,status,conclusion,headSha,createdAt,updatedAt,url'],text=True,capture_output=True,timeout=50)
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    if r.returncode:
        print(now,'POLL_ERROR',r.stderr[:300],flush=True)
    else:
        rows=json.loads(r.stdout); Path('/tmp/t3654-ci-all-status.json').write_text(json.dumps(rows,indent=2)+'\n'); byid={x['databaseId']:x for x in rows}
        done=True
        for row in targets:
            rid=row['run_id']; actual=byid.get(rid)
            if not actual: done=False;continue
            assert actual['headSha']==row['head_sha'],(rid,actual['headSha'],row['head_sha'])
            state=(actual['status'],actual['conclusion'])
            if prior.get(rid)!=state:
                print(now,row.get('viewport',row.get('name')),row.get('stage',''),rid,*state,flush=True);prior[rid]=state
            if actual['status']!='completed': done=False
        if done: break
    time.sleep(60)
