from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess
P=Path('/workspace/.cloud-setup/transport-current-20261103')
R=Path('/workspace/chicago-transport-current-20261103')
E=Path('/tmp/transport-evidence-recovery-20261103/repo')
T='transport-pr1649-a620-checkpoint-and-native-fixtures-2026-11-04-0110Z'
D=E/'evidence'/T
L=P/'periodic-evidence-a620'
assert not D.exists()
D.mkdir(parents=True);L.mkdir(exist_ok=True)
H='a6207b493f7ce06052e9e211245631a1e07f8df1'
def digest(b):return hashlib.sha256(b).hexdigest()
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'),timeout=35)
orig=[]
def cp(f,rel):
 b=f.read_bytes();assert f.suffix!='.glb'and len(b)<20*1024**2
 compressed=len(b)>400*1024
 q=D/(rel+'.gz'if compressed else rel)
 q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(gzip.compress(b,mtime=0)if compressed else b)
 assert digest(f.read_bytes())==digest(b),f
 orig.append(dict(path=str(q.relative_to(D)),original=str(f),original_bytes=len(b),original_sha256=digest(b),lossless_gzip=compressed))
def folder(n,target):
 p=P/n
 for f in sorted(p.rglob('*')):
  if f.is_file()and'__pycache__'not in f.parts:cp(f,target+'/'+str(f.relative_to(p)))
rec=json.loads((P/'actual-dev96d-reviewed-checkpoint-01/CLOSED.json').read_text())
source=rec['source'];assert source['HEAD']==H and rec['normal_push_verified']and rec['source_guard_verified']and rec['error']is None and not rec['DEV_merged']
assert git('rev-parse',H+'^{tree}').decode().strip()==source['TREE']
assert git('rev-parse',H+':chicago/4d').decode().strip()==source['APP']
for n in ['actual-dev75cd-reviewed-checkpoint-01','actual-ci-and-empty-fix-delivery-01','actual-dev96d-reviewed-checkpoint-01','actual-dev96d-targeted-and-owners-01','actual-devfc5d-targeted-and-owners-01','independent-devfc5d-review-01','independent-dev96d-review-01','actual-head7d-v10-world-1904-mobile-C-01','actual-head7d-v10-world-1835-desktop-A-01','empty-scene-fixture-fix-01']:
 assert(P/n/'CLOSED.json').exists()or n.startswith(('independent-','empty-scene-')),n
 folder(n,'ACTUAL-RESULTS/'+n)
for n in ['OWNED17-CI-FIXES-D802.json','V14-PRE-BROWSER-NO-EXECUTION-ERRATUM.json','ACTUAL-A620-V14-WORLD-GO.json','actual-headA620-v14-world-1904-mobile-C-01-LAUNCH.json','actual-headA620-v14-world-1904-mobile-C-01-OWNER.stdout','actual-head7d-v10-world-1835-desktop-A-01-ROOT-STOP-REASON.json','PR1649-A620-REVIEWABLE-BODY.md','PR1649-A620-BODY-UPDATED.json']:
 if(P/n).is_file():cp(P/n,'SOURCE-SCOPES-AND-ERRATA/'+n)
folder('world-prep/CURRENT-COMMITTED-DIAGNOSTIC-V14','FROZEN-NO-EXECUTION-V14')
folder('world-prep/CURRENT-COMMITTED-DIAGNOSTIC-V15/actual-cli-help-01','SEPARATE-V15-CLI-HELP-PROOF-NOT-WORLD')
for n in ['PREPARED-CI-EIGHT-PART-AND-GUARD-v3.patch','PROPOSAL-v3-CLOSED.json','WORKFLOW-GUARD-PYTHON-v3.py','OLD7D-GATE-TERMINAL-SUMMARY.json','OLD7D-GATE-FINAL.log','OLD7D-GATE-JOB-FINAL-GET.json','EXACT-NATIVE-DECLARATION-PARTITION-8.json','PRICING-AND-VALIDATION-PLAN-v2.json']:
 cp(P/'ci-head543-watch/GATE-PARTITION-FEASIBILITY-01'/n,'CI-PARTITION-PROPOSAL-AND-OLD7D-ACTUAL-FAILURE/'+n)
fixes=json.loads((P/'OWNED17-CI-FIXES-D802.json').read_text())['files'];assert len(fixes)==17
rows=[]
for name,h in fixes.items():
 b=git('show',H+':'+name);assert digest(b)==h
 q=D/'IMMUTABLE-A620-OWNED17'/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 rows.append(dict(path=name,sha256=h,bytes=len(b),git_blob=git('rev-parse',H+':'+name).decode().strip()))
save(D/'IMMUTABLE-A620-OWNED17/SOURCE.json',dict(**source,parents=rec['parents'],files=rows,extraction='Immutable Git objects; no app worktree/index mutation'))
(D/'IMMUTABLE-A620-OWNED17/COMMIT.txt').write_bytes(git('show','--format=fuller','--stat','--no-renames',H))
cp(Path(__file__),'RECOVERY-RECIPE/collect_packet_a620.py')
save(D/'COPY-ORIGINS.json',orig)
(D/'README.md').write_text('''# PR 1649: a620 incremental checkpoint and actual fixture repair\n\nThe normally pushed application head is `a6207b493f7ce06052e9e211245631a1e07f8df1`, tree `0472b3e7d758fe265e93b2d6f508cf91564286f6`, app `d4eb444a2cdf7186a4a0c4f7a5ee83512d00d716`. Its normal parents are D802 and reviewed DEV96d. PR1649 remains open: no DEV merge, full current-source native CI success, current-source world interaction pass, or broad photographic/gait/rider/boarding completion is asserted by this packet.\n\nThe actual 81bbb checkpoint, D802 CI/fixture delivery, and a620 reviewed integration each retain their own source identifiers, normal commit/push/readback, five HEAD QA commands, publication, validators, cleanup and resource receipts. The current 13-command targeted/native-owner run is precommit D802+MERGE96d at the exact a620 tree/app/index. Its native liberties/source-use writers and checkers, transport/driver/Navigator fixtures, empty-scene fixture, full existing native harness, syntax, bake-warranted self-test, all-assets validator and structure-clearance checks pass. They are not the full native gate.\n\nThe previous complete 7d native CI gate failed one of 1154 steps: the extracted empty-scene fixture lacked the new draws/preparation bindings. The raw original failure is retained. D802 fixes that isolated fixture using actual scene layer bindings, preserving the original assertions and adding empty/Light preparation controls. Actual ROOT execution passes the repaired fixture and full existing native harness (50 passed, zero failed), including 14 workflow refusal controls. The CI workflow now runs the same native gate in eight parallel parts with its 600-second per-part cap and required aggregate gate demanding all parts succeed. No assertion, reader/base flag, frame/memory budget or asset quality is lowered. Partition proposal estimates and old7d source declaration counts are historical planning, not current-source CI execution or speed evidence.\n\nThe 17 owned files are extracted from immutable a620 Git objects and individually hashed. All match the D802 owned-file pins. Reviewed incoming DEV content remains in a620, including 1919 rear stone dressings and earlier yard/bridge changes. The independent spatial reviews are analytic source checks, not browser screenshots.\n\nThe actual 7d phone1904 ScopeC result remains NONPASS. Person-card P14 passed under its original 30-second cap, but Find touch acknowledgement exceeded the next original 30-second cap. P15/P16/Light acceptance was not completed. The old7d desktop1835 ScopeA run was explicitly stopped with owned cleanup when incoming DEV changed real world geometry; it has no control verdict. Neither result transfers to a620.\n\nV14 is a pre-browser no-execution negative: its wrapper defined main but omitted the CLI entrypoint. The launcher existed, stdout stayed empty and the requested output directory was absent; there was no browser launch or world receipt. Its original wrapper and erratum are frozen here. The separate V15 supervised --help receipt proves CLI invocation only, not a browser or world predicate. In-flight V15 world output is deliberately absent from this immutable packet.\n\nLarge logs, when present with .gz suffix, are lossless gzip with original SHA-256 and byte count in COPY-ORIGINS.json. Every packet file except the self-referential manifest is hashed in MANIFEST.json. The existing public 7d packet at evidence commit41997711 remains the earlier source-specific record.\n''')
records=[]
for f in sorted(D.rglob('*')):
 if f.is_file():records.append(dict(path=str(f.relative_to(D)),bytes=f.stat().st_size,sha256=digest(f.read_bytes())))
total=sum(x['bytes']for x in records);assert total<12*1024**2,total
manifest=dict(schema='pr1649-a620-checkpoint-native-fixtures-original-negatives-v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=source,parents=rec['parents'],normal_application_push_verified=True,full_current_source_native_gate_PASS_claimed=False,current_source_world_PASS_claimed=False,DEV_merged=False,broad_transport_tickets_done=False,V14='PRE_BROWSER_NO_EXECUTION',V15='CLI_HELP_PROOF_ONLY',records=records,packet_bytes_without_manifest=total)
save(D/'MANIFEST.json',manifest)
for r in records:assert digest((D/r['path']).read_bytes())==r['sha256']
save(L/'PACKET-CLOSED.json',dict(status='IMMUTABLE_SMALL_PACKET_COLLECTED_NOT_PUBLIC',topic='evidence/'+T,source=source,records=len(records),packet_bytes=total,manifest_sha256=digest((D/'MANIFEST.json').read_bytes())))
print(json.dumps(dict(topic=T,records=len(records),bytes=total,manifest_sha256=digest((D/'MANIFEST.json').read_bytes()))))
