from pathlib import Path
import base64,hashlib,json,subprocess
P=Path(__file__).parent;R=Path('/workspace/chicago-bridge-increment-20261102');base='0a14eb07bc6630ace4ce8bec12b87e9fa1a4b0d4';branch='steward/t2379-editorial-proposal-20261104';repo='repos/kevinrhaas/chicago/'
def api(p,b=None,m=None):
 c=['gh','api',repo+p]
 if m:c+=['--method',m]
 if b is not None:c+=['--input','-']
 return json.loads(subprocess.check_output(c,input=None if b is None else json.dumps(b).encode()))
def save(n,v):(P/n).write_text(json.dumps(v,indent=2)+'\n')
status=json.loads((P/'SCOPED-VALIDATION-MATERIALS-REAPER.json').read_text());assert status['command_exit']==0 and status['all_children_reaped'] and not status['leftover_cleanup']
assert not (P/'SOURCE-BRANCH-CREATED.json').exists()
files=list(json.loads((P/'SOURCE-SCOPE-AUDIT.json').read_text())['changes'])+['docs/STATUS.md','docs/ROADMAP.md','changelog.d/T-2379.json'];tree=[];hashes={}
for rel in files:
 b=(R/'chicago/4d'/rel).read_bytes();expect=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();row=api('git/blobs',{'encoding':'base64','content':base64.b64encode(b).decode()});assert row['sha']==expect;tree.append({'path':'chicago/4d/'+rel,'mode':'100644','type':'blob','sha':expect});hashes[rel]={'git_blob':expect,'sha256':hashlib.sha256(b).hexdigest()}
old=api('git/commits/'+base);row=api('git/trees',{'base_tree':old['tree']['sha'],'tree':tree});save('SOURCE-TREE.json',row)
commit=api('git/commits',{'message':'T-2379: distinguish the Lake House editorial proposal from measured scale','tree':row['sha'],'parents':[base]});save('SOURCE-COMMIT.json',commit)
ref=api('git/refs',{'ref':'refs/heads/'+branch,'sha':commit['sha']});save('SOURCE-BRANCH-CREATED.json',ref);save('SOURCE-FILE-BINDINGS.json',hashes)
# Import only the authenticated commit header, whose tree/blobs already exist locally.
d={'__file__':'/workspace/cobweb-resume-recovery-20261103/adopt_latest.py'};exec(Path(d['__file__']).read_text().split('comparison =')[0],d);d['P']=P;d['O']=P/'objects';d['commit'](commit['sha'])
# Local index is synchronized from exactly those six files, without changing sparse boundaries.
subprocess.run(['git','add','--']+['chicago/4d/'+r for r in files],cwd=R,check=True)
localtree=subprocess.check_output(['git','write-tree'],cwd=R,text=True).strip();assert localtree==row['sha'],(localtree,row['sha'])
subprocess.run(['git','update-ref','refs/heads/'+branch,commit['sha'],base],cwd=R,check=True)
subprocess.run(['node','tools/check-changelog-entry.mjs',base,commit['sha']],cwd=R/'chicago/4d',check=True)
body='''The Lake House Record treated an editor's June 10, 1835 proposal for a hotel “about double” its size as measured scale, an existing-building ranking and proof that the proposed site was vacant. It now identifies the comparison as a proposal and states those evidence limits. The admitted c001 interpretation is corrected on the same terms; “unfinished building” avoids an unsupported timber implication.

Only the two approved notes, the official compiler's Lake House sidecar, append-only STATUS/ROADMAP entries and one What's-New entry change. The exact quotation, normalized transcription, locator, reading type, other claims and PR1694 Fergus address ruling are preserved. Current actual resolved parameters/properties/confidence are identical; all geometry, native MASTER/WEB files, recipes and renderer code are byte-identical to the base. This is an interpretation correction, not a new source reading or facsimile inspection.

Validation: official scene1835/material/sourceUse writers and their checks, dataset/schema/params validation (0 errors;299 existing warnings), changelog shape, ticket-ID collision and PR changelog question. The complete current hosted eight-part source gate and aggregate must pass before ordinary SHA-guarded merge. The sparse local checkout does not claim a full published gate; two excluded-material-JSON fixture failures are retained separately from the corrected control run.

No native generation or new browser execution is claimed for this prose-only change. Prior Lake body/cards remain historical evidence, not a fresh run. T-2379 stays OPEN/partial: the July1835 shell is reconstructed and its whole image match remains incomplete; a later completed-hotel picture does not establish its construction stage.'''
(P/'PR-BODY.md').write_text(body+'\n')
pr=api('pulls',{'title':'T-2379: clarify the Lake House editorial proposal','head':branch,'base':'dev','body':body,'draft':False});save('PR-CREATED.json',pr);print(json.dumps({'pr':pr['html_url'],'head':commit['sha'],'tree':row['sha']}))
