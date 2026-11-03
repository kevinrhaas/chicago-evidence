from pathlib import Path
import json,hashlib,gzip,shutil,datetime
R=Path('/workspace/.cloud-setup/transport-current-20261103');D=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence/transport-pr1649-dev08-startup-repairs-2026-11-03-2200Z');C=R/'ci-head543-watch';V=Path('/workspace/.cloud-setup/transport-driver-motion-20261103');orig=[]
def cp(p,rel):
 b=p.read_bytes();compressed=len(b)>512*1024;q=D/(rel+'.gz' if compressed else rel);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(gzip.compress(b,mtime=0) if compressed else b);orig.append(dict(path=str(q.relative_to(D)),original=str(p),original_bytes=len(b),original_sha256=hashlib.sha256(b).hexdigest(),lossless_gzip=compressed,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
for n in ['DEV08-SOURCE-UNION-BEFORE-CUSTOM-FIXES.json','DEV08-STARTUP-AND-SPARSE-FIXES-APPLIED.json','DEV08-REVIEWABLE-COMMIT-MESSAGE.txt','integrate_reviewed_dev08.py','run_dev08_targeted_and_owners.py','actual-dev08-startup-targeted-and-owners-01-LAUNCH.json','actual-dev08-startup-targeted-and-owners-01-OWNER.stdout','actual-dev08-startup-fourpart-preflight-01-LAUNCH.json','actual-dev08-startup-fourpart-preflight-01-ROOT-STOP-REASON.json','actual-dev08-startup-fourpart-preflight-01-OWNER.stdout','CURRENT.md','PR1649-CURRENT-BODY.md','PR1649-BODY-UPDATE-RECEIPT.json','HEAD543-NATIVE-NUL-TREE-SIZES-V2.json','HEAD543-NATIVE-TREE-SIZES.json','RESTORED-RUNTIME-BASELINE.json','RUNTIME-EPOCH-METADATA-ERRATUM.json','resource_guard.py']:
 cp(R/n,'ROOT-STATE-AND-HELPERS/'+n)
for n in ['actual-dev08-normal-integration-01','actual-dev08-startup-targeted-and-owners-01','actual-dev08-startup-fourpart-preflight-01','actual-head543-world-1835-mobile-C-01','actual-head543-world-1904-mobile-C-03-stored-balanced']:
 for p in sorted((R/n).rglob('*')):
  if p.is_file() and 'native-tmp' not in p.relative_to(R/n).parts:cp(p,'ACTUAL-RESULTS/'+n+'/'+str(p.relative_to(R/n)))
for n in ['CURRENT-SCOPED-PUBLISHED-DIAGNOSTIC-V2','CURRENT-SCOPED-PUBLISHED-STORED-TIER-V3','ELIGIBLE-MODULE-PREWARM-COMBINED-UNADOPTED']:
 for p in sorted((R/'world-prep'/n).rglob('*')):
  if p.is_file() and 'proposed' not in p.relative_to(R/'world-prep'/n).parts:cp(p,'WORLD-HELPERS-AND-APPLIED-STARTUP-PROPOSAL/'+n+'/'+str(p.relative_to(R/'world-prep'/n)))
for p in sorted((C/'warranted-sparse-proposal-01').iterdir()):
 if p.is_file():cp(p,'APPLIED-WARRANTED-SPARSE-PROPOSAL/'+p.name)
# This directory's sandbox uses hardlinks and was not frozen after closure.
# Archive ONLY finalized top-level receipts; never read later sandbox GLBs.
for p in sorted((C/'PHYSICAL-CONSERVATIVE-FRESHNESS-01').iterdir()):
 if p.is_file():cp(p,'PHYSICAL-FRESHNESS-FINALIZED-RECEIPTS-ONLY/'+p.name)
for n in ['WARRANTED-ORIGINAL-5M-CHECKOUT-TIMEOUT-NONPASS.json','WARRANTED-SECOND-ORIGINAL-5M-CHECKOUT-TIMEOUT-NONPASS.json','WARRANTED-ATTEMPT2-ANNOTATIONS.json','UPLOAD-RELEASE-ORIGINAL-TIMEOUT-NONPASS.json','UPLOAD-RELEASE-ANNOTATIONS.json','V3-COMPLETED-CHECKOUT-PARSER-ERRATUM.json']:
 cp(C/n,'OLD-PUBLIC543-CI/'+n)
ss=sorted(C.glob('**/5439723317fbb6491e837911243f2f62fb35065b/2026*.json'),key=lambda p:p.name,reverse=True)
for p in ss:
 try:j=json.loads(p.read_text())
 except json.JSONDecodeError:continue
 if j.get('closed_utc'):latest=p;break
cp(latest,'OLD-PUBLIC543-CI/LATEST-FINALIZED-SNAPSHOT.json')
for p in sorted((C/'native-logs').glob('*.log')):cp(p,'OLD-PUBLIC543-CI/RAW-COMPLETED-LOGS/'+p.name)
for p in C.glob('WINDOW-*/CLOSED-WINDOW.json'):cp(p,'OLD-PUBLIC543-CI/'+p.parent.name+'-CLOSED-WINDOW.json')
p=V/'NEXT-INCREMENT-INTEGRATION-PREPARED-DEV08-V2.json';prepared=json.loads(p.read_text());cp(p,'UNADOPTED-NEXT-DRIVER-DEV08-V2/'+p.name)
for name,sha in prepared['files'].items():
 p=V/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==sha;cp(p,'UNADOPTED-NEXT-DRIVER-DEV08-V2/'+name)
for folder,name in [('periodic-evidence-checked-push','40AE'),('periodic-evidence-world-ci','8CBE'),('periodic-evidence-final-prep','478')]:cp(R/folder/'PUBLICATION-CLOSED.json','PRIOR-PUBLIC-PROOF-REFERENCES/'+name+'-PUBLICATION-CLOSED.json')
for n in ['capture_immutable.py','collect_packet.py']:cp(R/'periodic-evidence-dev08'/n,'RECOVERY-RECIPE/'+n)
(D/'COPY-ORIGINS.json').write_text(json.dumps(orig,indent=2)+'\n');print('copied',len(orig),'records; sandbox contents never read')
