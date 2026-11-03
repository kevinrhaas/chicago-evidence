from pathlib import Path
import json,hashlib,gzip,datetime,subprocess,ast
P=Path('/workspace/.cloud-setup/transport-current-20261103');R=Path('/workspace/chicago-transport-current-20261103');E=Path('/tmp/transport-evidence-recovery-20261103/repo');topic='transport-pr1649-incremental-d067-2026-11-03-2320Z';D=E/'evidence'/topic
assert not D.exists();D.mkdir(parents=True)
HEAD='d0671d821ba861a171fbd3394b22e4ed496dceda';TREE='603f2f88b53ee4a2a2b08d13047383db4ecab221';APP='c8f78fbe675db8d3ca1d6907b79aef13e46dd6e9';orig=[]
def sh(b):return hashlib.sha256(b).hexdigest()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def cp(p,rel):
 b=p.read_bytes();compressed=len(b)>512*1024;q=D/(rel+'.gz'if compressed else rel);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(gzip.compress(b,mtime=0)if compressed else b);orig.append(dict(path=str(q.relative_to(D)),original=str(p),original_bytes=len(b),original_sha256=sh(b),lossless_gzip=compressed,sha256=sh(q.read_bytes())))
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],timeout=30)
assert git('rev-parse',HEAD+'^{tree}').decode().strip()==TREE and git('rev-parse',HEAD+':chicago/4d').decode().strip()==APP
rec=json.loads((P/'actual-dev08-incremental-checkpoint-01/RECONCILED-CLOSED.json').read_text());assert rec['source']['HEAD']==HEAD and rec['normal_push_verified']and rec['full_native_preflight_pending']and not rec['world_interaction_scope_passed']and not rec['DEV_merged']
for name in ['actual-dev08-incremental-checkpoint-01','actual-dev08-startup-targeted-and-owners-03','actual-staged-dev08-v5-publication-01','actual-staged-dev08-v5-world-1904-mobile-C-03','actual-staged-dev08-v6-world-1904-mobile-C-04']:
 for p in sorted((P/name).rglob('*')):
  if p.is_file():cp(p,'ACTUAL-RESULTS/'+name+'/'+str(p.relative_to(P/name)))
for n in ['DEV08-ALL-ELEVEN-FINAL-FIXES.json','INCREMENTAL-PR1649-BINDING-v2.json','INCREMENTAL-PR1649-COMMIT-MESSAGE.txt','checkpoint_pr1649_v2.py','run_dev08_targeted_and_owners_v3.py','resource_guard.py','RESTORED-RUNTIME-BASELINE.json','actual-dev08-incremental-checkpoint-01-LAUNCH.json','actual-dev08-incremental-checkpoint-01-OWNER.stdout']:
 cp(P/n,'ROOT-HELPERS-AND-BINDINGS/'+n)
for v in ['CURRENT-STAGED-DIAGNOSTIC-V5','CURRENT-STAGED-DIAGNOSTIC-V6']:
 for p in sorted((P/'world-prep'/v).rglob('*')):
  if p.is_file():cp(p,'WORLD-HELPERS/'+v+'/'+str(p.relative_to(P/'world-prep'/v)))
ci=P/'ci-head543-watch/HEAD-D067-RECONCILE-20261103T232109Z'
for p in sorted(ci.iterdir()):
 if p.is_file():cp(p,'SOURCE-D067-READONLY-CI/'+p.name)
fixes=json.loads((P/'DEV08-ALL-ELEVEN-FINAL-FIXES.json').read_text())['files'];rows=[]
for name,sha in fixes.items():
 b=git('show',HEAD+':'+name);assert sh(b)==sha;q=D/'IMMUTABLE-D067-ELEVEN-FIXES'/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);rows.append(dict(path=name,sha256=sha,git_blob=git('rev-parse',HEAD+':'+name).decode().strip(),bytes=len(b)))
source=dict(HEAD=HEAD,TREE=TREE,APP=APP,parents=git('show','-s','--format=%P',HEAD).decode().split(),semantic_index_sha256=rec['source']['semantic_index_sha256'],extraction='git show immutable commit object, never mutable working source/index',files=rows)
save(D/'IMMUTABLE-D067-ELEVEN-FIXES/SOURCE.json',source)
(D/'IMMUTABLE-D067-ELEVEN-FIXES/COMMIT.patch').write_bytes(git('show','--format=fuller','--stat','--no-renames',HEAD))
save(D/'COPY-ORIGINS.json',orig)
owner=json.loads((D/'ACTUAL-RESULTS/actual-dev08-startup-targeted-and-owners-03/CLOSED.json').read_text());pub=json.loads((D/'ACTUAL-RESULTS/actual-staged-dev08-v5-publication-01/CLOSED.json').read_text());assert owner['status']=='TARGETED_FIXTURES_AND_NATIVE_OWNERS_PASS_NOT_FULL_PREFLIGHT'and pub['status']=='ACTUAL_STAGED_NATIVE_PUBLICATION_PASS'
for n in ['actual-staged-dev08-v5-world-1904-mobile-C-03','actual-staged-dev08-v6-world-1904-mobile-C-04']:
 w=json.loads((D/'ACTUAL-RESULTS'/n/'CLOSED.json').read_text());assert w['status']=='ACTUAL_STAGED_PUBLISHED_SCOPE_NONPASS'and w['source_before']['TREE']==w['source_after']['TREE']==TREE and w['cleanup']['cleanup_complete']and w['resources']['accepted']
(D/'README.md').write_text('''# PR 1649 incremental application checkpoint, 3 November 2026\n\nThe actual application commit `d0671d821ba861a171fbd3394b22e4ed496dceda` is normally pushed to the existing PR 1649 feature branch. Its complete tree is `603f2f88b53ee4a2a2b08d13047383db4ecab221`, app tree `c8f78fbe675db8d3ca1d6907b79aef13e46dd6e9`, with parents `5439723317fbb6491e837911243f2f62fb35065b` and `08d3f3d7c85545013eaca18a9d256fe63a8e17e0`. Full source already exists in the application repository; this small packet adds the eleven final repair files read from immutable Git objects, their hashes, native receipts, and honest negatives. No GLB is duplicated.\n\nThe owner explicitly requested periodic incremental commits. This reversible feature-branch checkpoint preserves the working occupied-traffic loading, driver-card preparation, People-tab dependency fix and checkout-input changes while the complete local preflight and interaction qualification remain pending. It does not merge DEV or certify broad photo quality.\n\nThe checkpoint helper's original CLOSED receipt is NONPASS because its immediate post-push readback assertion failed. Every actual native commit, five HEAD QA commands, whitespace check and normal push command passed, with complete owned cleanup and accepted resources. A separate RECONCILED-CLOSED receipt preserves that original negative and verifies the exact new HEAD using both a fresh Git remote read and PR API read. It never re-runs the push or rewrites the negative.\n\nThe actual source603 targeted/native-owner receipt passes nine commands, and the actual staged-source publication/check receipt passes. Their source remains explicitly staged (HEAD543 plus MERGE_HEAD08); equal TREE603 and APPc8 bridge those checks to the immutable committed checkpoint, without claiming a freshly committed-head published build.\n\nBoth actual1904 mobile Scope C runs are retained as NONPASS. V5 used the original RAF wait; V6 changed only that wait to100ms polling without changing its predicate or30-second cap. Occupied traffic mounted and Hans's card/census appeared in each failure snapshot, but the actual visible-Inspector wait timed out. Find, the remaining Light tail and a complete interaction pass are not established. No visible-card snapshot is promoted to a passing gate. Cleanup, resources, source bindings, original600-second outer limit and all raw reports remain preserved.\n\nThe source-specific d067 CI GET snapshot records automatic frame/content/report workflows, while the conflicting PR had no PR gate/moving/humans run at that cutoff. Warranted's actual checkout completed in5seconds and the native job succeeded, but its real decision was `bake=1` because the workflow itself changed outside the warranted job; this is not a1034-asset freshness/skip verdict. Desktop frame checkout completed in3seconds and its complete physical input materialization in91seconds; the actual frame check was still pending at that snapshot. These observations do not claim full CI green.\n\nDEV subsequently advanced to42b9c601; ROOT is separately integrating that newer source. The packet captures only d067 and does not reinterpret any later mutable checkout, generated result or CI run. Broad transport tickets remain unfinished and no DEV merge is claimed.\n''')
cp(P/'periodic-evidence-d067/collect_packet.py','RECOVERY-RECIPE/collect_packet.py');ast.parse((D/'RECOVERY-RECIPE/collect_packet.py').read_text())
records=[]
for q in sorted(D.rglob('*')):
 if q.is_file():
  b=q.read_bytes();assert len(b)<20*1024**2 and q.suffix!='.glb';records.append(dict(path=str(q.relative_to(D)),bytes=len(b),sha256=sh(b)))
manifest=dict(schema='pr1649-owner-incremental-d067-normal-push-and-honest-pending-qualification-v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),topic='evidence/'+topic,source=source,normal_application_push_verified=True,original_checkpoint_readback_negative_preserved=True,staged_source_targeted_and_owners_PASS=True,staged_source_publication_PASS=True,full_local_preflight_pending=True,scope_1904_mobile_C='V5_NONPASS_AND_V6_NONPASS',full_CI_green=False,DEV_merged=False,broad_tickets_done=False,records=records,packet_bytes_without_manifest=sum(x['bytes']for x in records))
save(D/'MANIFEST.json',manifest)
for x in records:
 b=(D/x['path']).read_bytes();assert len(b)==x['bytes']and sh(b)==x['sha256']
summary=dict(records=len(records),bytes=manifest['packet_bytes_without_manifest'],topic=topic,manifest_sha256=sh((D/'MANIFEST.json').read_bytes()),source=source)
save(P/'periodic-evidence-d067/PACKET-CLOSED.json',summary);print(json.dumps(summary,indent=2))
