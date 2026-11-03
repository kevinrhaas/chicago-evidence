from pathlib import Path
import json,hashlib,datetime,shutil,gzip,ast
R=Path('/workspace/.cloud-setup/transport-current-20261103');D=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence/transport-pr1649-world-and-ci-progress-2026-11-03-2125Z');D.mkdir(parents=True,exist_ok=False);orig=[]
def read(p):return json.loads(p.read_text())
def cp(p,rel):
 b=p.read_bytes();q=D/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);orig.append(dict(path=rel,original=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
W=R/'actual-head543-world-1904-mobile-C-02';world=read(W/'CLOSED.json');assert world['status']=='ACTUAL_CURRENT_PUBLISHED_WORLD_SCOPE_NONPASS' and world['source_before']==world['source_after'];assert world['source_before']['HEAD']=='5439723317fbb6491e837911243f2f62fb35065b';assert world['result']['returncode']==1 and not world['result']['timed_out'] and world['result']['requested_timeout_seconds']==world['result']['effective_timeout_seconds']==600;assert world['cleanup']['cleanup_complete'] and not world['cleanup']['remaining_owned_children'] and world['resources']['accepted']
for p in sorted(W.rglob('*')):
 if p.is_file():cp(p,'WORLD1904-C02-ACTUAL-NONPASS/'+str(p.relative_to(W)))
for n in ['actual-head543-world-1904-mobile-C-02-LAUNCH.json','actual-head543-world-1904-mobile-C-02-OWNER.stdout','launch_detached_world.py','world-HEAD543-GO.json','PR1649-CURRENT-BODY.md','PR1649-BODY-UPDATE-RECEIPT.json','CURRENT.md','ACTUAL-HEAD543-PUBLICATION-SOURCE-BINDING.json']:
 cp(R/n,'ROOT-STATE-AND-LAUNCH/'+n)
cp(R/'actual-head543-world-1835-mobile-C-01-LAUNCH.json','ACTIVE-1835-LAUNCH-ONLY/OWNER-LAUNCHED-NOT-PASS.json')
for n in ['CURRENT-SCOPED-PUBLISHED-DIAGNOSTIC-V2','CURRENT-SCOPED-PUBLISHED']:
 for p in sorted((R/'world-prep'/n).iterdir()):
  if p.is_file():cp(p,'EXACT-WORLD-HELPERS/'+n+'/'+p.name)
for n in ['READONLY-CURRENT-WORLD-DIAGNOSTIC-REVIEW.json','AWAIT-CHAIN-READONLY-543.json','STATIC-ROUTE-CHUNK-COUNTS-543.json','NATIVE-PREFLIGHT-COUNT-CONTRACT-543.json']:
 p=R/'world-prep'/n
 if p.exists():cp(p,'EXACT-WORLD-HELPERS/'+n)
for p in sorted((R/'actual-head543-warranted-rerun-01').rglob('*')):
 if p.is_file():cp(p,'WARRANTED-ORIGINAL-AND-ONE-RETRY/'+str(p.relative_to(R/'actual-head543-warranted-rerun-01')))
C=R/'ci-head543-watch'
for n in ['WARRANTED-ORIGINAL-5M-CHECKOUT-TIMEOUT-NONPASS.json','WARRANTED-CHECK-RUN.json','WARRANTED-ANNOTATIONS.json','V2-OBSERVER-CACHE-LOCATION-ONLY.json','V3-COMPLETED-CHECKOUT-PARSER-ERRATUM.json','observe_pr1649_v3.py','observe_pr1649_v2.py','watch_window.py']:
 cp(C/n,'CI-OBSERVATION/'+n)
ss=sorted(C.glob('**/5439723317fbb6491e837911243f2f62fb35065b/2026*.json'),key=lambda p:p.name,reverse=True)
for p in ss:
 try:snapshot=read(p)
 except json.JSONDecodeError:continue
 if snapshot.get('closed_utc'):latest=p;break
else:raise AssertionError('No finalized CI snapshot')
assert snapshot['expected_public_commit']==world['source_before']['HEAD'] and snapshot['GET_only']
cp(latest,'CI-OBSERVATION/LATEST-FINALIZED-SNAPSHOT.json')
for p in sorted((C/'native-logs').glob('*.log')):cp(p,'CI-OBSERVATION/RAW-COMPLETED-NATIVE-LOGS/'+p.name)
r=read(R/'actual-head543-warranted-rerun-01/GET-RECONCILED.json');p=Path(r['snapshot']);assert hashlib.sha256(p.read_bytes()).hexdigest()==r['snapshot_sha256'];cp(p,'WARRANTED-ORIGINAL-AND-ONE-RETRY/EXACT-ATTEMPT2-RECONCILIATION-SNAPSHOT.json')
for folder,name in [('periodic-evidence-checked-push','40AE'),('periodic-evidence-final-prep','478')]:cp(R/folder/'PUBLICATION-CLOSED.json','PRIOR-PUBLIC-PROOF-REFERENCES/'+name+'-PUBLICATION-CLOSED.json')
summary=dict(status='PUBLIC543_WORLD1904_C02_NATIVE_NONPASS_AND_CI_PENDING_CHECKPOINT',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=world['source_before'],world1904=dict(status=world['status'],actual_seconds=world['result']['seconds'],native_returncode=1,outer_native_timeout=False,original_cap_seconds=600,source_unchanged=True,resources_PASS=True,complete_owned_cleanup=True,all_cases_or_photo_PASS=False),world1835=dict(status='OWNER_LAUNCHED_NOT_PASS_LAUNCH_ONLY_ARCHIVED',active_results_not_copied=True),CI=dict(snapshot_original=str(latest),snapshot_closed_utc=snapshot['closed_utc'],check_counts=snapshot['check_counts'],missing_or_not_success=snapshot['missing_or_not_success'],full_green=False,one_warranted_retry_attempt=2,no_additional_dispatch_by_evidence_agent=True),DEV_merge=False,broad_tickets_done=False,no_source_or_GLB_payload_duplication=True)
(D/'CUTOFF-SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');(D/'COPY-ORIGINS.json').write_text(json.dumps(orig,indent=2)+'\n')
(D/'README.md').write_text('''# PR 1649 world and CI progress, 3 November 2026\n\nThe application remains public commit `5439723317fbb6491e837911243f2f62fb35065b`, TREE `ef566b993dd2bfe76eea419c750aa01e7acec263`. This append-only checkpoint preserves completed diagnostics and pending CI evidence. It does not duplicate source blobs, old asset packs or driver GLBs. Prior evidence commits40ae0706cdac6eb0b08d972ebdbfb6b42ec4ad8e and478b51b01fd23774f6ed0c20dcdfd1d53532d8a6 are referenced by their actual publication receipts.\n\nThe second native 1904 phone Scope C run **failed** after467.372seconds, within its unchanged600-second outer cap. Its source was unchanged, resource checks passed, and all owned children were cleaned up. Full native telemetry, configuration, exact V2 helpers and diagnostic diffs, owner launch and final closure are included. A diagnostic observation is not a passing world, interaction or photographic acceptance result.\n\nThe 1835 run was still active at this cutoff. Only its immutable launch record is archived and explicitly labeled NOT PASS; no mutable result or completion is inferred.\n\nCI remains pending. The latest finalized GET-only snapshot and available completed native logs are included. The original warranted job exceeded its5-minute checkout limit; its original negative is retained alongside ROOT's single retry intent, POST result and exact GET reconciliation to attempt2. No additional retry or dispatch was made for this evidence save. Observer cache-location and checkout-parser errata are kept with their actual helper versions. None of those observations imply full CI green or a DEV merge.\n\nThe current PR body, update receipt and CURRENT.md are snapshots of their recorded times. They may describe earlier observations than a later CI snapshot; the raw timestamped evidence remains authoritative.\n''')
p=D/'ARCHIVE-RECIPE/build_packet.py';p.parent.mkdir();shutil.copy2(Path(__file__),p);ast.parse(p.read_text())
rows=[]
for p in sorted(D.rglob('*')):
 if p.is_file() and p!=D/'MANIFEST.json':
  b=p.read_bytes();assert len(b)<50*1024**2 and p.suffix!='.glb';rows.append(dict(path=str(p.relative_to(D)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
M=dict(schema='pr1649-finalized-world-negative-and-pending-ci-evidence-v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),topic='evidence/transport-pr1649-world-and-ci-progress-2026-11-03-2125Z',source=world['source_before'],world1904_native_status=world['status'],world1904_source_resource_cleanup_valid=True,world1835='ACTIVE_LAUNCH_ONLY_NOT_PASS',full_CI_green=False,DEV_merge=False,broad_tickets_done=False,no_source_or_GLB_duplicates=True,records=rows,packet_bytes_without_manifest=sum(r['bytes'] for r in rows))
(D/'MANIFEST.json').write_text(json.dumps(M,indent=2)+'\n');assert len(rows)==len([p for p in D.rglob('*') if p.is_file()])-1
for row in rows:
 b=(D/row['path']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
print(json.dumps(dict(records=len(rows),bytes=M['packet_bytes_without_manifest'],manifest_sha256=hashlib.sha256((D/'MANIFEST.json').read_bytes()).hexdigest(),latest_CI_snapshot=str(latest)),indent=2))
