from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess
P=Path('/workspace/.cloud-setup/transport-current-20261103')
E=Path('/tmp/transport-evidence-recovery-20261103/repo')
T='transport-pr1649-merged-dev-9881-final-ci-and-original-world-negatives-2026-11-04'
D=E/'evidence'/T
L=P/'periodic-evidence-final-merge'
assert not D.exists();D.mkdir(parents=True);L.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
orig=[]
def cp(f,rel):
 b=f.read_bytes();assert f.suffix not in['.glb','.zip']and len(b)<10*1024**2
 compressed=len(b)>128*1024;q=D/(rel+'.gz'if compressed else rel);q.parent.mkdir(parents=True,exist_ok=True)
 q.write_bytes(gzip.compress(b,mtime=0)if compressed else b);assert sha(f.read_bytes())==sha(b)
 orig.append(dict(path=str(q.relative_to(D)),original=str(f),original_bytes=len(b),original_sha256=sha(b),lossless_gzip=compressed))
def folder(q,target):
 for f in sorted(q.rglob('*')):
  if f.is_file()and'__pycache__'not in f.parts and f.suffix not in['.glb','.zip']:cp(f,target+'/'+str(f.relative_to(q)))
merge=json.loads((P/'actual-pr1649-ordinary-dev-merge-01/CLOSED.json').read_text())
assert merge['merge_commit']=='9881d782370d612c3ca521df383d67b1bb48487f'and merge['tree_identical_to_current_qualified_HEAD']and merge['ordinary_merge_no_force_admin_or_production']
CI=P/'ci-head543-watch/HEAD-A620-NATIVE-EIGHT-PART-WINDOW-01'
ci=json.loads((CI/'CI-ALL-CURRENT-CHECKS-PASS-CLOSED.json').read_text());assert ci['checks_success']==23 and ci['expected_skips']==7 and ci['negative_checks']==ci['unfinished_checks']==0
assert ci['HEAD']==merge['head']and ci['TREE']==merge['TREE']
folder(P/'actual-pr1649-ordinary-dev-merge-01','ACTUAL-ORDINARY-DEV-MERGE')
for n in ['CI-ALL-CURRENT-CHECKS-PASS-CLOSED.json','CI-FRAME-MEMORY-QUALIFIED-CLOSED.json','CI-NATIVE-GATE-QUALIFIED-CLOSED.json','NATIVE-CHECK.sh','NATIVE-GATE-WORKFLOW.yml','NATIVE-HARNESS.sh','NATIVE-MATRIX-WORKFLOW.yml','SOURCE-AND-WINDOW-AUTHORITY.json']:
 cp(CI/n,'CURRENT-A620-QUALIFIED-CI/'+n)
for n in ['terminal-native-parts','FRAME-DISPATCH-ONCE','final-moving-watch']:
 folder(CI/n,'CURRENT-A620-QUALIFIED-CI/'+n)
for n in ['CLOSED.json','TERMINAL-ARTIFACT-SUMMARIES.json','TERMINAL-NATIVE-SUMMARIES.json']:
 cp(CI/'resumed-window'/n,'CURRENT-A620-QUALIFIED-CI/resumed-window/'+n)
for n in ['terminal-logs','terminal-artifacts']:
 folder(CI/'resumed-window'/n,'CURRENT-A620-QUALIFIED-CI/resumed-window/'+n)
for n in ['actual-headA620-v15-world-1904-mobile-C-01','actual-headA620-v15-world-1835-desktop-A-01']:
 r=json.loads((P/n/'CLOSED.json').read_text());assert 'NONPASS'in r['status']and r['source_after']['HEAD']==merge['head']
 folder(P/n,'ORIGINAL-A620-WORLD-NONPASS/'+n)
for n in ['A620-V15-DESKTOP-A-REVIEW.json','A620-V15-POSTDEADLINE-FIND-REVIEW.json']:
 cp(P/'interaction-trace-reviews'/n,'PASSIVE-REVIEWS-NOT-LATE-PASS/'+n)
driver=Path('/workspace/.cloud-setup/transport-driver-motion-20261103')
for n in ['NEXT-INCREMENT-INTEGRATION-PREPARED-A620-V5.json','A620-COMPATIBLE-NEXT-V5-18-PATH.patch','A620-COMPATIBLE-NEXT-V5-PREVIEW.json','A620-COMPATIBLE-NEXT-V5-PROFILE.json','A620-COMPATIBLE-NEXT-V5-README.md','A620-COMPATIBLE-NEXT-V5-ROOT-READONLY.json','A620-V5-INITIAL-TEXT-PREP-NONPASS.json']:
 cp(driver/n,'NEXT-DRIVER-V5-PREPARED-NOT-ADOPTED/'+n)
gait=Path('/workspace/.cloud-setup/transport-next-gait-readonly-a620-20261104')
for n in ['README.md','READONLY-ASSESSMENT.json']:cp(gait/n,'NEXT-GAIT-READONLY-NOT-IMPLEMENTED/'+n)
cp(Path(__file__),'RECOVERY-RECIPE/collect_packet_final_merge.py')
save(D/'COPY-ORIGINS.json',orig)
(D/'README.md').write_text('''# PR1649 merged into DEV with complete current CI\n\nPR1649 merged by the ordinary protected DEV merge at 2026-11-04 01:29:50 UTC. Actual merge `9881d782370d612c3ca521df383d67b1bb48487f` has parents DEV96d and featurea620. Its tree `0472b3e7d758fe265e93b2d6f508cf91564286f6` is byte-identical to the qualified feature tree and CI synthetic merge tree. This packet contains the actual remote PR, DEV and merge readbacks. No force, admin override or production promotion was used. DEV deployment and public build/asset readback were still pending at this merge receipt; this packet does not assert deployment.\n\nAll 30 current project checks are terminal: 23 success, seven expected skips, zero negatives or unfinished checks. The native gate's eight actual parts and required aggregate gate pass. Its exact union is 1155 distinct native steps and 401 self-tests, with 1176 executions including 21 repeated prerequisites. Original 600-second per-part caps, required reader/base flags and actual four-worker pools are verified; maximum actual native part-step wall time was367 seconds. These are actual current-source CI receipts, separate from earlier proposal estimates or old7d failure. No local four-part execution is invented.\n\nAll nine native frame/memory jobs pass, and exact-a620 artifacts are retained as extracted JSON without duplicate zip copies. Ordinary mobile memory was1812 222.74MiB,1835 496.56MiB and1904 399.01MiB with zero errors; the separate memory self-test remains an intentional negative-control job. Moving frames passed their original ceiling, and upload release passed all32 native checks. Original native footers/raw logs, source-bound union proofs, artifact metadata and one-dispatch reconciliation are retained. No additional dispatch or rerun is asserted.\n\nThe supplemental current-a620 local world runs remain NONPASS: phone1904 ScopeC closed at459.577 seconds and desktop1835 ScopeA at508.295 seconds. The original configured bounds and all unmet predicates remain authoritative. Passive post-deadline Find observations are evidence of later behavior, never a timely PASS; the reviews do not rewrite original verdicts. Local1904 desktop ScopeB was still running when this packet was collected, so no active outputs or results are copied. The CI/merge facts do not qualify these supplemental interactions or photographic acceptance.\n\nBroader T1790/T2804/T3088 remain claimed with no completion PR, not DONE. Next-driver V5 is prepared only; its patch/profile/read-only preview are not an adopted, tested or shipped increment. The next-gait assessment is read-only research, not implemented motion. The goal of natural riders, articulated gait, boarding and photographic quality remains open.\n\nThe earlier a620 checkpoint packet remains separately published at evidence0524faba. Each copied original has SHA-256 and original length in COPY-ORIGINS.json; larger logs/results use lossless gzip. MANIFEST.json hashes all packet files except itself.\n''')
records=[]
for f in sorted(D.rglob('*')):
 if f.is_file():records.append(dict(path=str(f.relative_to(D)),bytes=f.stat().st_size,sha256=sha(f.read_bytes())))
total=sum(r['bytes']for r in records);assert total<8*1024**2,total
manifest=dict(schema='pr1649-ordinary-dev-merge-complete-current-ci-original-world-negatives-v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),feature_HEAD=merge['head'],DEV_merge=merge['merge_commit'],TREE=merge['TREE'],normal_DEV_merge_verified=True,CI_success=23,CI_expected_skip=7,CI_negative=0,native_distinct_steps=1155,native_selftests=401,all9_frame_memory_jobs_PASS=True,DEV_deployment_public_readback='PENDING_AT_MERGE_RECEIPT',supplemental_local_A_C='NONPASS_ORIGINALS_RETAINED',supplemental_B='ACTIVE_NOT_COPIED',broad_transport_tickets_DONE=False,next_driver='PREPARED_NOT_ADOPTED',next_gait='READONLY_NOT_IMPLEMENTED',records=records,packet_bytes_without_manifest=total)
save(D/'MANIFEST.json',manifest)
for r in records:assert sha((D/r['path']).read_bytes())==r['sha256']
save(L/'PACKET-CLOSED.json',dict(status='SMALL_FINAL_MERGE_PACKET_COLLECTED_NOT_PUBLIC',topic='evidence/'+T,records=len(records),packet_bytes=total,manifest_sha256=sha((D/'MANIFEST.json').read_bytes())))
print(json.dumps(dict(topic=T,records=len(records),bytes=total,manifest_sha256=sha((D/'MANIFEST.json').read_bytes()))))
