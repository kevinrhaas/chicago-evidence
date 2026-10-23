from pathlib import Path
import datetime,gzip,hashlib,io,json,tarfile
H=Path(__file__).resolve().parent;stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');OUT=H/('closed-image-progress-'+stamp);OUT.mkdir();sha=lambda b:hashlib.sha256(b).hexdigest();packets=[]
def capture(name,mapping,status,manifest_proofs=None):
 frozen=[]
 for member,p in sorted(mapping.items()):
  p=Path(p);assert p.is_file() and not p.is_symlink(),str(p);assert not Path(member).is_absolute() and '..' not in Path(member).parts
  raw=p.read_bytes();frozen.append((member,p,raw,sha(raw)))
 meta={'status':status,'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_proofs':manifest_proofs or [],'files':[{'path':n,'source_path':str(p),'bytes':len(b),'sha256':s} for n,p,b,s in frozen]}
 archive=OUT/(name+'.tar.gz')
 with archive.open('wb') as target:
  with gzip.GzipFile(fileobj=target,mode='wb',compresslevel=1,mtime=0) as gz:
   with tarfile.open(fileobj=gz,mode='w') as tar:
    for n,p,b,s in frozen:
     info=tarfile.TarInfo(n);info.size=len(b);info.mode=0o644;info.mtime=0;tar.addfile(info,io.BytesIO(b))
    b=(json.dumps(meta,indent=2)+'\n').encode();info=tarfile.TarInfo('CAPTURE.json');info.size=len(b);info.mode=0o644;tar.addfile(info,io.BytesIO(b))
 # Source stability and archive byte readback are separate checks.
 for n,p,b,s in frozen:assert sha(p.read_bytes())==s,('source changed',p)
 with tarfile.open(archive,'r:gz') as tar:
  assert set(tar.getnames())=={n for n,_,_,_ in frozen}|{'CAPTURE.json'}
  for n,p,b,s in frozen:assert sha(tar.extractfile(n).read())==s,('archive readback',n)
 row={'archive':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'source_files':len(frozen),'status':status,'source_manifest_proofs':manifest_proofs or []};packets.append(row);(OUT/(name+'.capture.json')).write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(row),flush=True)
# Hogan exact closed author manifest,37listed+manifest=38.
P=Path('/tmp/hogan-pr1229-integration/.hogan-recovery/closed-5eae-local-pass-newhead-20261023T1305');manifest=P/'MANIFEST.json';assert sha(manifest.read_bytes())=='0ff5251c3cbdedeabb93350f7bc87c61fc7d29ca07e9235db63242293167d00e';j=json.loads(manifest.read_text());assert len(j['files'])==37
mapping={r['path']:P/r['path'] for r in j['files']}
for r in j['files']:assert sha((P/r['path']).read_bytes())==r['sha256']
mapping['MANIFEST.json']=manifest
capture('Hogan-5eae-closed-local-PASS1053-remote-outcomes-PENDING',mapping,'CLOSED_LOCAL_PREFLIGHT_PASS1053_HEAD5eae_REMOTE_OUTCOMES_UNQUALIFIED_ORIGINAL_MATCH_OPEN',[{'path':str(manifest),'sha256':sha(manifest.read_bytes())}])
# Dispatch initialization is closed; no monitor file or fresh remote inference included.
paths=[Path('/tmp/hogan-5eae-final-head-smokes.json'),Path('/tmp/hogan-5eae-smoke-initialize.log'),Path('/tmp/hogan-5eae-smoke-dispatch.log')];j=json.loads(paths[0].read_text());assert len(j['runs'])==10 and j['dispatch_complete'];assert {r['head'] for r in j['runs']}=={'5eaeac194eb12843e511e1ab5d7deff70daa57e3'}
capture('Hogan-5eae-ten-confirmed-dispatches-NOT-tenPASS',{p.name:p for p in paths},'CLOSED_DISPATCH_RECEIPTS_TEN_REAL_RUN_IDS_RESULTS_NOT_CERTIFIED')
# Closed actual lighthouse geometry/image evidence, exact explicit rows plus closed inputs.
P=Path('/tmp/chicago-next-model/T-2373-shaft-stone-next/runs/20261023-130205-554211');review=json.loads((P/'actual-review.json').read_text());assert review['verdict']=='differs';mapping={r['path']:P/r['path'] for r in review['artifacts']}
for r in review['artifacts']:assert sha((P/r['path']).read_bytes())==r['sha256']
for n in ['ACTUAL-REVIEW.md','actual-review.json','baseline-export.log','baseline-review.log','baseline-wrote.txt','proposed-export.log','proposed-review.log','proposed-wrote.txt','scope.json']:mapping[n]=P/n
for kind in ['baseline','proposed']:
 for n in ['generators/archetypes/fort_structure.py','generators/archetypes/fort_structure_params.py','data/structures/chicago_lighthouse_1832.json','assets/manifest.json','data/sources/castelnau_1842_chicago_harbor.json','FIXTURE-ONLY.txt']:
  mapping[kind+'/'+n]=P/kind/n
capture('lighthouse-actual4926-stone-apertures-DIFFERS',mapping,'CLOSED_ACTUAL_TWO_EXPORTS_TWO_COMPARISONS4926_CONTRACT_PASS_VISUAL_DIFFERS_NO_CANONICAL_ADOPTION')
# Wolf exact owner-closed169-file manifest plus its author manifest.
P=Path('/tmp/chicago-next-model/T-2386-surface-pole-next/runs/20261023-130354-476531');manifest=P/'ARTIFACTS.json';assert sha(manifest.read_bytes())=='b95f6d528ea70cbcbed798b849b51cd75a3ff04e44dc4d1563d9e933cc41a4b1';j=json.loads(manifest.read_text());assert len(j['files'])==169;mapping={r['path']:P/r['path'] for r in j['files']}
for r in j['files']:assert sha((P/r['path']).read_bytes())==r['sha256']
assert sha((P/'visual-review.json').read_bytes())=='1af5d69f7baa6287e2f8d40764fac97f76f93eb228a284b8edbec199982fe8fb';mapping['ARTIFACTS.json']=manifest
capture('Wolf-actual1079-surface-pole-DIFFERS',mapping,'CLOSED_ACTUAL_ONE_EXPORT_ONE_COMPARISON1079_CONTRACT_PASS_VISUAL_DIFFERS',[{'path':str(manifest),'sha256':sha(manifest.read_bytes())}])
# First-fort closed16-export/zero-browser data set; do not reach live runner folders.
P=Path('/tmp/chicago-next-model/T-3041-build-resume-20261023');manifest=P/'closed-build-evidence-sha256.json';j=json.loads(manifest.read_text());assert len(j)==243;mapping={'closed-build-evidence/'+n:P/'closed-build-evidence'/n for n in j}
for n,s in j.items():assert sha((P/'closed-build-evidence'/n).read_bytes())==s
receipt=json.loads((P/'closed-build-evidence/actual-build-receipt.json').read_text());assert receipt['actual_fresh_exports']==16 and receipt['actual_browser_runs']==0
mapping['closed-build-evidence-sha256.json']=manifest;mapping['README.md']=P/'README.md'
capture('first-fort16-actual-exports30-context-NO-BROWSER',mapping,'CLOSED_BUILD_PASS16_REAL_EXPORTS30_CONTEXT_NO_BROWSER_NO_MATCH_ACCEPTANCE',[{'path':str(manifest),'sha256':sha(manifest.read_bytes())}])
# Closed native first sequence ONLY, all files are immutable named receipt members.
P=Path('/tmp/frame-integration/M-capacity-freeze-actual');receipt=P/'actual-native-sequence.json';j=json.loads(receipt.read_text());assert j['business_group_check_exit']==1 and j['business_full_check_exit']==0 and not j['final_preflight_or_smoke_acceptance'];mapping={'actual-native-sequence.json':receipt,'diff-check.log':P/'diff-check.log'}
for n,r in j['artifacts'].items():assert sha((P/n).read_bytes())==r['sha256'];mapping[n]=P/n
capture('M-first-native-sequence-not-finalgate32-semantics-pending',mapping,'CLOSED_NATIVE_SEQUENCE_GROUP_CHECK_FAIL_RETAINED_FULL_CHECK_PASS_TAIL_STABLE_NOT_FINAL_GATE_32SLOT_SEMANTICS_PENDING')
# Optional exact frozen lighthouse23-file character proposal; no fixture/runtime.
P=Path('/tmp/chicago-next-model/T-2373-irregular-stone-next');manifest=P/'RECOVERY-SHA256.json';assert sha(manifest.read_bytes())=='ac8cc536f187209820326c4a1886ad37b7a98ee9bc133f502e93ebcf527339a0';j=json.loads(manifest.read_text());assert len(j['files'])==23;assert not(P/'runs').exists() and not(P/'latest-run.txt').exists();mapping={r['path']:P/r['path'] for r in j['files']}
for r in j['files']:assert sha((P/r['path']).read_bytes())==r['sha256']
mapping['RECOVERY-SHA256.json']=manifest
capture('lighthouse-irregular-stone23-UNAPPLIED-UNRUN-one-export-plan',mapping,'FROZEN_UNAPPLIED_UNRUN_ONE_CANDIDATE_EXPORT_PLAN_AGAINST_HELD4926_BASELINE',[{'path':str(manifest),'sha256':sha(manifest.read_bytes())}])
index={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CLOSED_PROGRESS_RECOVERY_ONLY_NOT_FULL_IMAGE_ACCEPTANCE','packets':packets,'excluded':['live gate/monitor/integration folders','node_modules symlinks, caches and unmanifested files','capacity V1/V2 proposal histories owned separately','adjacent evolving Wolf/firstfort/lighthouse packages','separate lighting diagnostic'],'Hogan_dispatches':[{'viewport':r['viewport'],'stage':r['stage'],'id':r['id'],'url':r['url'],'head':r['head']} for r in json.loads(Path('/tmp/hogan-5eae-final-head-smokes.json').read_text())['runs']]}
(OUT/'RECOVERY.json').write_text(json.dumps(index,indent=2)+'\n');(OUT/'SHA256SUMS.txt').write_text(''.join(r['sha256']+'  '+r['archive']+'\n' for r in packets));(H/'latest-capture.txt').write_text(str(OUT)+'\n');print('CAPTURED',OUT,flush=True)
