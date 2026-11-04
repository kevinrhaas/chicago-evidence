from pathlib import Path
import subprocess,json,base64,hashlib,datetime
P=Path(__file__).parent;R='repos/kevinrhaas/chicago-tickets/';F='T-3000-3249/T-3041-match-the-first-fort-dearborn-buildings-against-.md'
def api(p,d=None):
 c=['gh','api',R+p]
 if d is not None:c+=['--method','PUT','--input','-']
 r=subprocess.run(c,input=None if d is None else json.dumps(d).encode(),capture_output=True,timeout=45)
 assert r.returncode==0,r.stderr.decode();return json.loads(r.stdout)
h=api('git/ref/heads/main')['object']['sha'];d=api('contents/'+F+'?ref='+h);b=base64.b64decode(d['content']);front=b.decode().split('---',2)[1];f={l.split(':',1)[0]:l.split(':',1)[1].strip()for l in front.splitlines()if':'in l}
assert f['state'] in ('open','claimed')
assert f['claimed_run'] in ('null','https://github.com/kevinrhaas/polecat-platform/actions/runs/41782312201'), 'Other run owns original; do not write'
marker='### Root checkpoint-order clarification — 2026-11-04';assert marker.encode() not in b
s='\n\n'+marker+'\n\nThe earlier instruction to finish all four source-check parts before the FIRST source commit is superseded. After all genuinely affected native models have been built on the pinned runner, and actual MASTER/WEB bindings and affected owners are verified, promptly push an explicitly UNQUALIFIED source-branch/raw-log/hash checkpoint BEFORE long gates. The owner explicitly requested periodic GitHub checkpoints and visible incremental progress. Do not wait for every check to save valid work.\n\nAll four actual source-check parts and normal preflight remain required before opening the release PR under repository policy. Both published runtime viewports, actual controlled picture comparisons, and the current-head eight-part gate plus named aggregate remain required before ordinary dev merge. This changes checkpoint order only: no gate/assertion is waived, no model freshness is fabricated, and no partial fort match becomes complete. Preserve the current cupola and all243 outbuilding assets. Original T3041 remains partial. Actual native execution authorization remains the granted exact ROOTGO068f/run417823 described above.\n'
new=b+s.encode();P.joinpath('BEFORE.md').write_bytes(b)
r=api('contents/'+F,{'message':'T-3041: allow unqualified source checkpoint before long gates after genuine native build','branch':'main','sha':d['sha'],'content':base64.b64encode(new).decode()});commit=r['commit']['sha'];a=api('contents/'+F+'?ref='+commit);actual=base64.b64decode(a['content']);assert actual==new and actual.startswith(b) and actual.decode().split('---',2)[1]==front
P.joinpath('AFTER.md').write_bytes(actual);P.joinpath('RECEIPT.json').write_text(json.dumps({'commit':commit,'before_tip':h,'before_blob':d['sha'],'after_blob':a['sha'],'frontmatter_and_foreign_prefix_exact':True,'fields_preserved':f,'append_sha256':hashlib.sha256(s.encode()).hexdigest(),'no_claim_sourcewrite_newdispatch_or_gatewaiver':True,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n');print(commit)
