"""One ordinary SHA-guarded merge only after the actual current named eight-part gate."""
from pathlib import Path
import json,subprocess,hashlib,datetime
P=Path(__file__).parent/'integration-ce094';repo='repos/kevinrhaas/chicago/';head='e8977b52d387a5a42dd9cf7d399f4b060aa064a4';base='ce094fbe74b44f6be134c355d88c41ea3aae7a54';tree='6687b64da5533cdaf450dd956cdb833e894dcdc6';runid=41808419254

def api(p,b=None,m=None):
 c=['gh','api',repo+p]
 if m:c+=['--method',m]
 if b is not None:c+=['--input','-']
 return json.loads(subprocess.check_output(c,input=None if b is None else json.dumps(b).encode()))
def save(n,v):(P/n).write_text(json.dumps(v,indent=2)+'\n')
assert not (P/'MERGE-REQUEST-SENT.json').exists(),'Never repeat uncertain merge request'
pr=api('pulls/1703');save('PREMERGE-PR.json',pr);assert pr['state']=='open' and not pr['draft'] and pr['head']['sha']==head
h=api('git/commits/'+head);assert h['tree']['sha']==tree
live=api('git/ref/heads/dev')['object']['sha'];assert live==base,('Base advanced; scoped latest-dev integration required before merge',live)
assert pr['mergeable'] is True and pr['mergeable_state']=='clean',pr['mergeable_state']
r=api('actions/runs/'+str(runid));js=api('actions/runs/'+str(runid)+'/jobs?per_page=100');save('FINAL-CURRENT8-RUN.json',r);save('FINAL-CURRENT8-JOBS.json',js)
assert r['head_sha']==head and r['status']=='completed' and r['conclusion']=='success'
names={j['name']:j for j in js['jobs']};expected={f'gate part {i}/8'for i in range(1,9)}|{'gate'};assert expected<=names.keys(),names.keys()
for name in expected:assert names[name]['status']=='completed' and names[name]['conclusion']=='success',(name,names[name])
checks=api('commits/'+head+'/check-runs?per_page=100');save('FINAL-CURRENT-CHECKS.json',checks);assert any(c['name']=='gate' and c['status']=='completed' and c['conclusion']=='success' for c in checks['check_runs'])
# The API branch commit is exactly six authored/official files over the accepted base.
compare=api('compare/'+base+'...'+head);save('PREMERGE-SCOPE-COMPARE.json',compare);want=set('chicago/4d/'+x for x in json.loads((P/'SOURCE-FILE-BINDINGS.json').read_text()));assert {f['filename']for f in compare['files']}==want
save('MERGE-REQUEST-SENT.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':head,'base':base,'tree':tree,'run':runid,'ordinary_squash':True,'uncertain_response_must_readback_not_repeat':True})
result=api('pulls/1703/merge',{'sha':head,'merge_method':'squash','commit_title':'T-2379: clarify the Lake House editorial proposal (#1703)'},'PUT');save('MERGE-RESPONSE.json',result);assert result.get('merged') is True,result
merged=api('pulls/1703');commit=api('git/commits/'+result['sha']);save('MERGED-PR.json',merged);save('MERGED-COMMIT.json',commit);assert merged['merged'] and merged['merge_commit_sha']==result['sha'];assert commit['tree']['sha']==tree;assert [p['sha']for p in commit['parents']]==[base];print('MERGED',result['sha'],'exacttree',tree)
