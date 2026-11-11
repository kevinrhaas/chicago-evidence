import json, os, subprocess, time
from pathlib import Path
repo='kevinrhaas/chicago'
branch='steward/t3546-t3547-t3548-prairie-portraits'
sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/'+branch],text=True).split()[0]
assert sha==remote, (sha,remote)
assert not subprocess.check_output(['git','status','--porcelain'],text=True).strip(), 'dirty worktree'
out=Path('/workspace/prairie-younger/integrated-smoke-runs.json')
assert not out.exists(), 'existing dispatch inventory; inspect it before running again'
def runs():
    return json.loads(subprocess.check_output(['gh','run','list','--repo',repo,'--workflow','chicago-4d-smoke.yml','--branch',branch,'--event','workflow_dispatch','--limit','40','--json','databaseId,headSha,createdAt,status,url'],text=True))
seen={r['databaseId'] for r in runs()}
records=[]
plan=[('desktop','13'),('mobile','13')]+[(v,s) for v in ['desktop','mobile'] for s in ['1-4','5-8','9-12','14-15']]
for viewport,stage in plan:
    subprocess.check_call(['gh','workflow','run','chicago-4d-smoke.yml','--repo',repo,'--ref',branch,'-f','viewport='+viewport,'-f','stage='+stage])
    for attempt in range(15):
        candidates=[r for r in runs() if r['headSha']==sha and r['databaseId'] not in seen]
        if candidates: break
        time.sleep(2)
    assert len(candidates)==1, candidates
    record=candidates[0] | {'viewport':viewport,'stage':stage}
    records.append(record)
    seen.add(record['databaseId'])
    out.write_text(json.dumps({'head':sha,'branch':branch,'runs':records},indent=2)+'\n')
    print(json.dumps(record),flush=True)
