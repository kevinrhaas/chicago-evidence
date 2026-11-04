from pathlib import Path
import json,hashlib,gzip,datetime,subprocess,os
P=Path('/workspace/.cloud-setup/transport-current-20261103');R=Path('/workspace/chicago-transport-current-20261103');E=Path('/tmp/transport-evidence-recovery-20261103/repo');T='transport-pr1649-nav-checkpoint-7d757-2026-11-04-0000Z';D=E/'evidence'/T
H='7d75789f9c2d5dc91aab4227d20e20f0677c6cf9';TREE='9c4550f9f49dd33a9b4d5262b92cf25a234f5ed2';APP='92a63744fe38744fe1df5c7a501ad754ed2c5fc7';assert not D.exists();D.mkdir(parents=True);orig=[]
def sh(b):return hashlib.sha256(b).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'),timeout=35)
def cp(f,rel):
 b=f.read_bytes();assert f.suffix!='.glb'and len(b)<20*1024**2,(f,len(b));compressed=len(b)>512*1024;q=D/(rel+'.gz'if compressed else rel);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(gzip.compress(b,mtime=0)if compressed else b);orig.append(dict(path=str(q.relative_to(D)),original=str(f),original_bytes=len(b),original_sha256=sh(b),lossless_gzip=compressed,sha256=sh(q.read_bytes())))
def folder(source,target):
 for f in sorted(source.rglob('*')):
  if f.is_file()and '__pycache__'not in f.parts:cp(f,target+'/'+str(f.relative_to(source)))
assert git('rev-parse',H+'^{tree}').decode().strip()==TREE and git('rev-parse',H+':chicago/4d').decode().strip()==APP
rec=json.loads((P/'actual-dev42-nav-incremental-checkpoint-01/RECONCILED-CLOSED.json').read_text());assert rec['normal_push_verified']and rec['source']['HEAD']==H and rec['source']['TREE']==TREE and rec['source']['APP']==APP and rec['full_native_preflight_pending']and rec['current_source_world_interaction_status']=='PENDING'and not rec['DEV_merged']
for n in ['actual-dev42-nav-incremental-checkpoint-01','actual-dev42-rail-targeted-and-reports-01','actual-staged-dev42-rail-publication-01','actual-staged-dev42-v8-world-1904-mobile-C-01','actual-dev42-native-report-tail-01','actual-own-claim-renewal-2350','independent-dev42-merge-review-01']:
 folder(P/n,'ACTUAL-RESULTS/'+n)
for n in ['ROOT-RAIL-PRELOAD-ADOPTION.json','DEV42-ALL-THIRTEEN-RAIL-FIXES.json','DEV42-NAV-INCREMENTAL-COMMIT-MESSAGE.txt','DEV42-NAV-INCREMENTAL-CHECKPOINT-BINDING.json','DEV42-NAV-INCREMENTAL-CHECKPOINT-PREP.json','DEV42-NAV-INCREMENTAL-CHECKPOINT-PREP-V2-PRESERVED.json','DEV42-NAV-INCREMENTAL-CHECKPOINT-V2-PREP.json','DEV42-NAV-CHECKPOINT-PREPARATION-RACE-ERRATUM.json','checkpoint_dev42_nav_incremental_pr1649_PREP.py','checkpoint_dev42_nav_incremental_pr1649_PREP_v2.py','run_dev42_rail_targeted_and_reports.py','resource_guard.py','RESTORED-RUNTIME-BASELINE.json','PR1649-7D-REVIEWABLE-BODY.md','PR1649-7D-BODY-UPDATED.json']:
 if(P/n).is_file():cp(P/n,'HELPERS-BINDINGS-AND-RACE-ERRATUM/'+n)
for n in ['NATIVE-GZIP-METADATA-TRANSITION.json','WORKFLOW-RESOLUTION.json','INTERRUPTED-RECOVERY-CLOSED.json','OPENED.json']:
 cp(P/'actual-dev42-normal-integration-01'/n,'DEV42-NORMAL-INTEGRATION/'+n)
for n in ['PREPARED-MANIFEST.json','PREPARED-PRELOAD-5-PATH.patch','BASE-PINS.json','P14-ACTUAL-DIAGNOSIS.json']:
 cp(P/'rail-code-preload-dev42-01'/n,'REVIEWED-NAV-PRELOAD-PATCH/'+n)
folder(P/'rail-code-preload-dev42-01/actual-navigator-fixture-02','REVIEWED-NAV-PRELOAD-PATCH/OUTSIDE-ROOT-FIXTURE-PASS')
folder(P/'world-prep/CURRENT-STAGED-DIAGNOSTIC-V8','PRIOR-SOURCE-V8-DIAGNOSTIC-HELPERS')
# Bound GET snapshots only; no live writer or application state is adopted.
ci=P/'ci-head543-watch/HEAD-7D757-AFTER-CHECKPOINT-01'
for f in sorted(ci.iterdir()):
 if f.is_file()and f.name!='watch.py':cp(f,'EXACT-7D-CI-GET-SNAPSHOTS/'+f.name)
for name in ['FRAME-DISPATCH-ONCE']:
 if(ci/name).is_dir():folder(ci/name,'EXACT-7D-CI-GET-SNAPSHOTS/'+name)
obs=sorted(f for f in ci.glob('observe-*')if f.is_dir())
if obs:folder(obs[-1],'EXACT-7D-CI-GET-SNAPSHOTS/LATEST-BOUNDED-OBSERVATION')
# Preserve the optional outside-app mane negative without duplicating GLBs.
mane=Path('/workspace/.cloud-setup/transport-horse-mane-proposal-20261103/actual-generation-01/CLOSED.json')
if mane.exists():cp(mane,'OPTIONAL-OUTSIDE-APP-MANE-NEGATIVE/CLOSED.json')
fixes=json.loads((P/'DEV42-ALL-THIRTEEN-RAIL-FIXES.json').read_text())['files'];rows=[];assert len(fixes)==13
for name,h in fixes.items():
 b=git('show',H+':'+name);assert sh(b)==h;q=D/'IMMUTABLE-7D-THIRTEEN-FIXES'/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);rows.append(dict(path=name,sha256=h,git_blob=git('rev-parse',H+':'+name).decode().strip(),bytes=len(b)))
source=dict(HEAD=H,TREE=TREE,APP=APP,parents=git('show','-s','--format=%P',H).decode().split(),semantic_index_sha256=rec['source']['semantic_index_sha256'],extraction='Immutable Git objects only; ROOT source/index untouched',files=rows);save(D/'IMMUTABLE-7D-THIRTEEN-FIXES/SOURCE.json',source)
(D/'IMMUTABLE-7D-THIRTEEN-FIXES/COMMIT.txt').write_bytes(git('show','--format=fuller','--stat','--no-renames',H))
assert sh((D/'HELPERS-BINDINGS-AND-RACE-ERRATUM/checkpoint_dev42_nav_incremental_pr1649_PREP.py').read_bytes())=='3bb0a1cbbc706b83b1ff26cae649ddddd600d4331242716fac747edb01cee1c4'
assert sh((D/'HELPERS-BINDINGS-AND-RACE-ERRATUM/checkpoint_dev42_nav_incremental_pr1649_PREP_v2.py').read_bytes())=='3ec6c9c2b2dddddb7f08962b48db8f01bba71580e2ab9aca14fffa9f55998275'
cp(Path(__file__),'RECOVERY-RECIPE/collect_packet_7d.py');save(D/'COPY-ORIGINS.json',orig)
(D/'README.md').write_text('''# PR 1649: actual 7d757 nav-loading checkpoint, 4 November 2026 UTC\n\nApplication commit `7d75789f9c2d5dc91aab4227d20e20f0677c6cf9` is normally pushed to the existing PR1649 feature branch. Tree9c4550f9 and APP92a63744 are bound in SOURCE.json. Its parents are prior checkpointd067 and reviewed DEV42. The thirteen repaired source files here come only from immutable Git objects; no GLB or texture is duplicated.\n\nThe new five-path patch prepares registered Navigator/Inspector code alongside eligible driver metadata and reuses it at interaction. Preparation creates no panel or seen marker. Existing import deduplication, later-choice ownership and failed-load retry remain. The actual ROOT nine-command fixture/native-report closure and native staged publication/check pass on exact9c/92. These are incremental feature proofs: complete native preflight, new-source published interaction and current-head CI remain pending before DEV merge. Broad photographic, gait, rider and boarding work is not complete.\n\nThe original checkpoint CLOSED remains NONPASS for its immediate post-push API readback assertion. Actual normal commit, all five native HEAD QA commands, whitespace and push completed with cleanup/resources; independent Git and fresh PR API reconciliation verifies the exact public7d HEAD. No push was retried. A preparation race is retained honestly: the agent later added a QA-output field to the already-written helper. ROOT had executed the original3bb version. Its exact bytes were restored after verification, the later3ec version saved separately, and the original CLOSED left unchanged. Read the race erratum and execution pins; the later PREP metadata is not another executed proof.\n\nThe previous1904 phone ScopeC remains NONPASS on source1bc/APPf770. Its per-poll P14 trace and failure report are preserved, not promoted to a passing timing result or transferred to patched APP92. The native affected-owner tail also remains a600-second timeout, with its original result, cleanup, transcript and independent gzip byte proof. The research-ledger gzip changed only the platform byte at offset9; deflate and decodedJSON remain exact. No owner fixed-point PASS is asserted.\n\nThe independent authored merge/parent-union review and original invalid-UTF8 ROADMAP inventory are dated source-specific reviews, not a fullgate. Fresh native claim/lap renewal receipts are retained. Any optional mane receipt is an outside-app negative, not a shipped anatomical improvement.\n\nExact7d CI snapshots show PR-event gate, moving/release and humans flows starting once conflicts cleared. The synthetic merge8d715502 has exactTREE9c and parentsDEV42+7d. Content build completes SUCCESS with bake skipped because the branch changes the bake workflow only inside its warranted gate; this is not a measured1034-asset freshness verdict. One newly authorized native frame/memory dispatch is recorded after fresh exact-head absence and public ref readback; defaults, matrices, caps and self-test are unchanged, and no secondPOST or retry was performed. Read the dated snapshots for actual check states; no full CI green or DEV merge is claimed.\n''')
records=[]
for f in sorted(D.rglob('*')):
 if f.is_file():
  b=f.read_bytes();records.append(dict(path=str(f.relative_to(D)),bytes=len(b),sha256=sh(b)))
assert sum(x['bytes']for x in records)<12*1024**2
manifest=dict(schema='pr1649-7d757-nav-feature-checkpoint-with-original-negatives-and-exact-ci-v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),topic='evidence/'+T,source=source,normal_application_push_verified=True,original_immediate_readback_negative_preserved=True,preparation_race_erratum_and_exact_executed_helper_preserved=True,staged_source_targeted_and_report_checks_PASS=True,staged_source_publication_PASS=True,full_native_preflight_pending=True,current_source_world_interaction_status='PENDING',old_source_scopeC='NONPASS_APP_f770_NOT_TRANSFERRED',native_affected_tail='TIMEOUT600_NOT_FIXEDPOINT_PASS',full_current_head_CI_green=False,DEV_merged=False,broad_transport_tickets_done=False,records=records,packet_bytes_without_manifest=sum(x['bytes']for x in records))
save(D/'MANIFEST.json',manifest)
for x in records:assert sh((D/x['path']).read_bytes())==x['sha256']
summary=dict(status='SMALL_IMMUTABLE_PACKET_COLLECTED_NOT_YET_PUBLIC',topic=T,records=len(records),bytes=manifest['packet_bytes_without_manifest'],manifest_sha256=sh((D/'MANIFEST.json').read_bytes()),source=source)
save(P/'periodic-evidence-7d/PACKET-CLOSED.json',summary);print(json.dumps({k:v for k,v in summary.items()if k!='source'}))
