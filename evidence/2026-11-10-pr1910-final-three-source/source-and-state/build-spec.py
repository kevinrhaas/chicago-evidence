from pathlib import Path
import json,hashlib,subprocess
O=Path('/tmp/nov10-pr1910-source-checkpoint');R=Path('/tmp/chicago-west-wicket-20261109');N=Path('/tmp/nov10-final-three-native');B=Path('/tmp/nov10-secondfort-before-actual');F=Path('/tmp/nov10-complete-second-fort');BASE='2dcdf91df70ae52c5d121162939cfe2aa4617152';HEAD='b9c767997c452740c6b690cf2d280d7f75c8c9d5'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*args,repo=R):return subprocess.run(['git','-C',str(repo),*args],check=True,capture_output=True).stdout
scope=json.loads((N/'SCOPE-REPORT.json').read_text());assert scope['pinned_HEAD']==HEAD and scope['counts']['actual_stale_defaults']==27 and scope['counts']['actual_stale_variants']==2
assert sha(N/'BEFORE-BINDING.json')=='27e6ea7f369349e2769dd42eb81e0fe0402892d2f6208a090ef467b2c8d29553'
run=json.loads((N/'NATIVE-RUN.json').read_text());assert run['databaseId']==42758213227 and run['headSha']==HEAD
changed=git('diff','--name-only',BASE,HEAD).decode().splitlines();assert not any(p.endswith(('.glb','.gltf','.blend')) for p in changed)
(O/'SOURCE-base2dc-to-b9-FULL-BINARY.patch').write_bytes(git('diff','--binary',BASE,HEAD));(O/'SOURCE-COMMITS.txt').write_bytes(git('log','--reverse','--format=fuller',BASE+'..'+HEAD));(O/'SOURCE-CHANGED-PATHS.txt').write_text('\n'.join(changed)+'\n')
for c in ['c39028a8a3','780c4252ca']:(O/f'POST-NATIVE-ONLY-{c}.patch').write_bytes(git('format-patch','--no-signature','--stdout','-1',c,repo=F))
summary=json.loads((B/'SUMMARY.json').read_text());assert len(summary['views'])==9 and all(v['verdict']=='unreviewed' and v['exit_code']==0 for v in summary['views']);assert summary['views'][-1]['camera_sha256']=='cafea15f52de57a3268c7db88c9bbd42d84e1e0300e67979fc85b7c1d46a0dd8'
for v in summary['views']:assert json.loads(next(Path(v['receipt']).parent.glob('*.match.json')).read_text())['verdict']=='unreviewed'
lib=Path('/tmp/nov10-b3-liberty-resolution');lr=json.loads((lib/'VERBATIM-MOVE-AND-SUCCESSOR-RECEIPT.json').read_text());assert lr['all_unrelated_old_bytes_exact'] and len(lr['mapping'])==3 and all(v['verbatim_exact'] for v in lr['mapping']);assert sum(map(len,lr['standing_successor_Covers'].values()))==10
cost=json.loads((N/'TARGET-CPU-COST-BOUNDS.json').read_text());assert cost['sum_positive_triangle_increments_no_reduction_credit']==1678
pricing=json.loads(Path('/tmp/nov10-a5-pre-b-budget/MEASUREMENT-AND-PRICING.json').read_text());assert pricing['boot']['bytes']==45932852 and pricing['pricing_basis']['chosen_conservative_baseline_triangles']==2657398
cl=json.loads((N/'SOURCE-PREFLIGHT-CLASSIFICATION.json').read_text());assert cl['literal_stale_errors']==29 and cl['other_validator_errors']==0 and cl['no_native_or_image_acceptance_claim']
prior=json.loads(Path('/tmp/nov10-delivery-checkpoint/staged/ORIGINAL-TICKET-PROGRESS-FINAL.json').read_text());public=json.loads(Path('/tmp/nov10-ticket-reconciliation/21-final-public-states.json').read_text());states={t['ticket']:t['recorded_state'] for t in prior['tickets']};states.update({t['id']:t['state'] for t in public['tickets'] if t['id'] in states});assert len(states)==17 and sum(v=='done' for v in states.values())==14
(O/'ORIGINAL-17-CURRENT-STATUS.json').write_text(json.dumps({'counts':{'originals':17,'done':14,'remaining':3},'states':states,'public_latest_commit':public['commit'],'basis':'Prior exact 10 DONE snapshot plus four exact public DONE readbacks; renewed T-2376/T-3041/T-2388 group. Foreign claim retained. No B acceptance or new ticket.'},indent=2)+'\n')
first=[];sd=O/'first-fort-b9-metadata';sd.mkdir(exist_ok=True)
for p in git('ls-tree','-r','--name-only',HEAD,'chicago/4d/data/reference_views').decode().splitlines():
 if '/first_fort' not in p or not p.endswith('.match.json'):continue
 data=git('show',HEAD+':'+p);d=json.loads(data);assert d['verdict']=='matches' and not any(x.get('status')=='open' for x in d.get('differences',[]));dest=sd/(p.split('/reference_views/')[1].replace('/','--'));dest.write_bytes(data)
 cam=p.replace('.match.json','.json');(sd/(cam.split('/reference_views/')[1].replace('/','--'))).write_bytes(git('show',HEAD+':'+cam));first.append({'source_path':p,'metadata_sha256':hashlib.sha256(data).hexdigest(),'verdict':'matches','glb_sha256':d.get('glb_sha256'),'camera_sha256':d.get('camera_sha256'),'group_sha256':d.get('group_sha256')})
assert len(first)==4
(O/'FIRST-FORT-FOUR-CURRENT-SOURCE-READBACK.json').write_text(json.dumps({'source_pin':HEAD,'views':first,'scope':'Four existing actual first-fort source views accepted. T-3041 remains claimed; no new B native/image/UI acceptance.'},indent=2)+'\n')
files={}
def add(d,p):
 p=Path(p);assert p.is_file(),str(p);assert d not in files;assert p.suffix.lower() not in ['.glb','.gltf','.blend','.pyc'];files[d]=str(p)
for p in N.iterdir():
 if p.is_file() and p.name not in ['MONITOR-RUN-LATEST.json','MONITOR-JOBS-LATEST.json','CURRENT-RUNS.json','PROGRESS.json','ACTIVE-RUNS-READONLY.json']:add('native-preparation/'+p.name,p)
for p in Path('/tmp/nov10-a5-pre-b-budget').iterdir():
 if p.is_file():add('actual-pre-B-baseline/'+p.name,p)
add('actual-pre-B-baseline/RETAINED-A5-HIGHER-FULL-SMOKE-RED.log','/tmp/nov10-completion-native/native-smoke-reds/129601520087.log')
for p in lib.iterdir():
 if p.is_file():add('liberties-verbatim-resolution/'+p.name,p)
for p in Path('/tmp/nov10-ticket-reconciliation').iterdir():
 if p.is_file():add('ticket-reconciliation/'+p.name,p)
add('prior-checkpoints/ORIGINAL-TICKET-PROGRESS-BEFORE-PR1907.json','/tmp/nov10-delivery-checkpoint/staged/ORIGINAL-TICKET-PROGRESS-FINAL.json');add('prior-checkpoints/PR1907-FINAL-QUALIFICATION-RECEIPT.json','/tmp/nov10-pr1907-final-qualification/GITHUB-CHECKPOINT-RECEIPT.json')
for name in ['SUMMARY.json','MANIFEST.json','BASELINE_OBSERVATIONS.md']:add('second-fort-BEFORE/'+name,B/name)
for dirname,target in [('captures','captures'),('captures-history-1855-c390-cropped','HISTORY-ONLY-SUPERSEDED-1855-CROPPED'),('captures-extra-1855-context21','HISTORY-ONLY-SUPERSEDED-1855-CONTEXT21'),('chicago/4d/data/reference_views','camera-and-match-snapshots')]:
 for p in (B/dirname).rglob('*'):
  if p.is_file() and p.suffix.lower() not in ['.glb','.gltf','.blend','.pyc']:add('second-fort-BEFORE/'+target+'/'+p.relative_to(B/dirname).as_posix(),p)
for p in sd.iterdir():add('first-fort-b9-metadata/'+p.name,p)
for p in O.iterdir():
 if p.is_file() and p.name not in ['SPEC.json','INVENTORY.json','SPEC-VALIDATION.json','README.md','AFTER-NATIVE-ADOPTION-ORDER.md']:add('source-and-state/'+p.name,p)
readme=f'''# PR1910 source / BEFORE / pricing checkpoint

Public source PR1910 is pinned to `{HEAD}` from base `{BASE}`.
The full binary patch and exact commit list are preserved, with no additional
MASTER, WEB or other model-binary copies. A later working checkout HEAD is not
silently equated with this immutable source pin. Native run42758213227 has the
exact b9 pin and is queued on the parent-qualified26.04runner. Waiting in the
runner queue is not a native failure or reason for a second dispatch. No B
native output, actual AFTER image match, final published UI or budget acceptance
is claimed in this package.

The frozen union contains29outputs through27IDs:27defaults plus2Tremont variants;
1017default and4variant foreign records remain bound. BEFORE-BINDING hash is
27e6ea7f369349e2769dd42eb81e0fe0402892d2f6208a090ef467b2c8d29553.
Strict audit binds raw pinned parent, resolved source/input documents, all
foreign registry/MASTER/WEB/LOD bytes, topology/material/confidence, consumed UVs
and selected control WEB/LOD bytes. The narrow unconsumed-UV exception has three
real rejection controls; no blanket foreign/material/confidence waiver exists.
The actual preflight reports exactly29expected stale outputs and no other
validator errors. Source checks include28frame tests,114gate checks,8budget
checks and9actual policy negative controls. Native-before postern52/58blocked
triangles and the mistaken Brougham command-path RED are explicitly retained and
classified; neither is silently called a native or whole-renderer pass.

Historical L45/L47/L225 moved verbatim, with unrelated bytes exact. Standing
successors keep all10continuing reconstructed metric admissions. Only those
specific historical omissions/refusals are source-resolved; this does not settle
new native/image acceptance or erase live metric reconstruction.

Actual pre-B boot was45,932,852bytes. The fresh six-stand sweep was lower than
retained actual full-smoke worst; the conservative baseline is2,657,398triangles.
CPU source/native-old-equal counts bound positive resident geometry growth by
1678triangles, or3356under at most two passes. This is NOT whole-frame, shadow,
instancing, calls, payload/wire, Light or FITS acceptance. New actual native and
published measurements remain required; the lower old sweep is not substituted
for the higher observed cost.

Nine second-fort actual BEFORE comparisons preserve full picture/render pairs,
raw PNGs, camera/photo/group bindings and command receipts. ALL remain unreviewed.
Eight cameras use exact b9 canonical bytes. The securely named1855pair uses the
explicitly proposed post-native metadata camera
cafea15f52de57a3268c7db88c9bbd42d84e1e0300e67979fc85b7c1d46a0dd8.
Both the old cropped1855and superseded21-member1855trial are labelled HISTORY
ONLY, not canonical extra views. Exact individual patches c39028a8a3 and780c4252ca
are saved separately: Root must apply them AFTER native adoption, in that order,
then compile and inspect actual AFTER views. They are not in b9.

Four current first-fort source views are already accepted, with zero open
items; their exact b9 cameras/match metadata are preserved here. This does not
close T3041 or the three remaining originals. Public reconciliation commit
3f80aa2233d51601b87a786590c52df6acb45ef9 records four new DONE originals and the
renewed T2376/T3041/T2388 claim group, while preserving a foreign claim. Together
with the earlier10DONE originals,14of17are DONE. Green Tree and the two forts
remain active. Root alone publishes checkpoints, adopts native, updates tickets
and completes PR lifecycle. No GitHub/ticket write or production promotion was
performed by this specification worker.
'''
for a,b in {'run427':'run 427','qualified26.04runner':'qualified 26.04 runner','contains29outputs through27IDs:27defaults plus2Tremont':'contains 29 outputs through 27 IDs: 27 defaults plus 2 Tremont','1017default and4variant':'1017 default and 4 variant','exactly29expected':'exactly 29 expected','include28frame tests,114gate checks,8budget':'include 28 frame tests, 114 gate checks, 8 budget','and9actual':'and 9 actual','postern52/58blocked':'postern 52/58 blocked','all10continuing':'all 10 continuing','was45,932,852bytes':'was 45,932,852 bytes','is2,657,398triangles':'is 2,657,398 triangles','1678triangles, or3356under':'1678 triangles, or 3356 under','named1855pair':'named 1855 pair','cropped1855and':'cropped 1855 and','superseded21-member1855trial':'superseded 21-member 1855 trial','and780c':'and 780c','earlier10DONE originals,14of17are DONE':'earlier 10 DONE originals, 14 of 17 are DONE'}.items():readme=readme.replace(a,b)
(O/'README.md').write_text(readme);add('README.md',O/'README.md')
(O/'AFTER-NATIVE-ADOPTION-ORDER.md').write_text('''# Required order

1. Root audits and adopts only the authenticated native output pinned to b9
   against BEFORE-BINDING. Queue wait is not a build failure or retry trigger.
2. Only AFTER adoption, apply exact c39028a8a3, then780c4252ca. These narrow the
   dated1855view to named A+B and refine its focal/principal framing. The
   cafea15f…pair is the qualified BEFORE reference, not either superseded trial.
3. Compile scene/pictures/source-use as needed, render actual AFTER and compare
   all eligible architecture at the finite visitor-visible stopping bar.
4. Check actual published desktop/phone and real frame/wire/Light/payload
   pricing. CPU bounds and source isolation do not claim whole FITS.
5. Root alone updates the original tickets and PR after the actual results
   warrant it. No B native/image/UI acceptance is supplied by this package.
''');add('AFTER-NATIVE-ADOPTION-ORDER.md',O/'AFTER-NATIVE-ADOPTION-ORDER.md')
inv={'prefix':'evidence/2026-11-10-pr1910-final-three-source/','source_head':HEAD,'native_run':42758213227,'native_status_snapshot':run['status'],'files':{d:{'source':p,'bytes':Path(p).stat().st_size,'sha256':sha(p)} for d,p in files.items()},'no_model_binaries':True,'no_B_native_or_image_acceptance':True};(O/'INVENTORY.json').write_text(json.dumps(inv,indent=2)+'\n');add('INVENTORY.json',O/'INVENTORY.json')
spec={'prefix':'evidence/2026-11-10-pr1910-final-three-source/','message':'Checkpoint PR1910 b9 source and exact 29-output native request, nine unreviewed actual BEFORE views, strict audits, bounded pricing and deferred camera patches; queued native and three originals remain','receipt':str(O/'GITHUB-CHECKPOINT-RECEIPT.json'),'files':files};(O/'SPEC.json').write_text(json.dumps(spec,indent=2)+'\n')
val={'status':'PASS_SPEC_READY_SOURCE_BEFORE_PRICING_ONLY','source_head':HEAD,'source_base':BASE,'native_run':42758213227,'native_status_snapshot':run['status'],'file_count':len(files),'total_bytes':sum(Path(p).stat().st_size for p in files.values()),'qualified_before_views':9,'all_qualified_before_verdicts':'unreviewed','refined_1855_camera_sha256':summary['views'][-1]['camera_sha256'],'no_additional_model_binaries':True,'all_paths_exist':True,'spec_sha256':sha(O/'SPEC.json'),'inventory_sha256':sha(O/'INVENTORY.json')};(O/'SPEC-VALIDATION.json').write_text(json.dumps(val,indent=2)+'\n');print(json.dumps(val,indent=2))
