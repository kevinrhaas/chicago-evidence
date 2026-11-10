from pathlib import Path
import json,hashlib,shutil,datetime
b=Path('/tmp/nov10-kinzie-ui');out=b/'public-packet';out.mkdir(exist_ok=True)
for name in ['desktop-c7f-yearapp','desktop-resource-recovery-c7f','phone-c7f-yearapp','phone-row-supplement-c7f','desktop-c7f','desktop-c7f-world']:
 shutil.copytree(b/name,out/name,dirs_exist_ok=True)
for name in ['expected-c7f.json','prepare-expected.mjs','review.mjs','resource-only.mjs','phone-row-supplement.mjs','ACTUAL-DESKTOP-c7f-YEARAPP.log','ACTUAL-DESKTOP-RESOURCE-RECOVERY.log','ACTUAL-PHONE-c7f-YEARAPP.log','ACTUAL-PHONE-ROW-SUPPLEMENT.log','INITIAL-PORTAL-URL-FIXTURE.json','INITIAL-ROOT-URL-FIXTURE.json','PREPARE-INITIAL-IGNORED-PICTURES-FIXTURE.log','PREPARE-ACTUAL-PUBLISHED-PIN-RETRY.log','ALL1050-NATIVE-INPUTS-FRESH-DOC-FINAL.json','ALL1050-NATIVE-INPUTS-FRESH-DOC-FINAL.log','all-native-inputs-doc-final.py','ROOT-COMBINED-PUBLISH.log','ROOT-COMBINED-NATIVE-FRESHNESS.log','ROOT-COMBINED-CLOSING-CHECK.log','ROOT-FULL-CHECKOUT-BEFORE-ADOPTION.json','ROOT-FINAL-APP-AND-NATIVE-EQUIVALENCE.json','PLANTING-CLEARANCE-PREFLIGHT.json','GREEN-COMMON-GRADE-TERRAIN-CHECK.json']:
 shutil.copy2(b/name,out/name)
native=Path('/tmp/nov10-kinzie-native-qualification')
for name in ['ORIGINAL-JOB.log','ATTEMPT2-JOB.log']:
 d=out/'native-desktop13-timeout';d.mkdir(exist_ok=True);shutil.copy2(native/'desktop13-recovery'/name,d/name)
shutil.copy2('/tmp/nov10-kinzie-source/publish-exact-commit-api.py',out/'publish-exact-commit-api.py')
reviews=[]
notes=[
 'Pale squared-log house and bounded picket green visible with four separate Lombardy poplars and two rear cottonwoods in desktop context. Authored row stations and heights remain R.',
 'Same house/green/tree context in ByGrade. Tree surfaces show inherited inferred ecology; this does not propagate R planting coordinates into materials.',
 'Elevated overview separates the four-poplar row and both rear cottonwoods and shows the narrowed green in its river-bank setting.',
 'Overview ByGrade reviewed; scope and grade caveat remain as in view2.',
 'West end door visibly raised beneath retained wall plate, pale finish preserves log relief, end/front opening arrangement remains.',
 'West end normal/grade geometry consistent; no claim that reconstructed finish or height becomes an attested dimension.',
 'Sources tab labels end-door height2.5 and whitewash RECONSTRUCTED; source links and adjacent inferred window dimensions remain visible.',
 'Images tab lists eight credited source records with publication dates/creators/collections and PUBLIC DOMAIN credit. All seven canonical witnesses remain available; late postcard remains cross-check.',
 'Standing Liberty visible and expandable; text explains whitewash continuity, source date disagreement and reconstructed opening/green/planting decisions.'
]
for folder in ['desktop-c7f-yearapp','phone-c7f-yearapp']:
 r=json.loads((b/folder/'receipt.json').read_text())
 assert len(r['screenshots'])==9
 assert all(not r[k] for k in ['pageErrors','consoleErrors','failedRequests','badResponses'])
 for i,name in enumerate(r['screenshots']):
  note=notes[i]
  if folder.startswith('phone')and i<4:note='Default phone context directly reviewed: house/green/grade view is present; narrow viewport, distance, foliage overlap and default tree detail do not visually separate every crown. All six actual planted-stem/species/height records and terrain stations independently match source. No four-separate-phone-crown claim. '+('Normal mode.' if i%2==0 else 'ByGrade mode.')
  reviews.append({'file':folder+'/'+name,'directly_viewed':True,'verdict':'ACCEPT_WITH_STATED_SCOPE','finding':note})
r=json.loads((b/'phone-row-supplement-c7f/receipt.json').read_text())
for name in r['screenshots']:
 reviews.append({'file':'phone-row-supplement-c7f/'+name,'directly_viewed':True,'verdict':'ACCEPT_WITH_STATED_SCOPE','finding':'Closer default-phone context shows pale house and bounded green in Normal/ByGrade; the row still overlaps to one dominant crown from this pose. This is not proof of four visually separable phone crowns. Actual six-stem source/runtime/terrain records match. No additional geometry, detail or shader override.'})
summary={'kind':'DIRECT_PUBLISHED_T2484_REVIEW_WITH_EXPLICIT_QUALIFICATIONS','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'published_source':'c7f15e3db13660d7e6d2599effcee6c6d3304d86','final_source':'2beb73357a68a2678e8663b6acc4ce4120943dea','native_source':'6b11594bbd1d1a4e9fdd864878359ccf1c54edfc','native_retained':'d6076c038f5d7e103c922110b568c3188436ec25','all20_directly_viewed':True,'desktop_qualification':'Original desktop runner completed all9 screenshots and all source/asset/six-stem/UI assertions with zero errors, then failed because its final helper incorrectly imposed coarse-phone source-release on desktop. Original FAIL receipt preserved. Independent resource-only actual default-desktop recovery proves both target sources retained, exact pins/six stems, zero hard problems and zero errors. No original FAIL was rewritten.','phone_qualification':'Nine actual default-phone views and two bounded supplements pass target runtime/UI and release/collapse assertions. Row overlap/viewport limits remain explicit; no claim of six visually separable phone crowns.','canonical_scope':'Seven unchanged canonical house+native-green cameras only; procedural trees qualified separately by this full-context published review.','confidence':'Finish/end-height/green metric placement/tree stations/heights R, existing tree ecology I. No per-stem R shader propagation claim.','native_wide_limitation':'Authenticated native bake and strict83/81control/961foreign+6variant audit PASS. Broad native smoke17/18 legs passed; desktop13 timed out at40min in both original and single recovery, with no assertion failure. No third retry. Old6b Part4 stale derived owners corrected officially on final source; current protected source checks remain final merge prerequisite.','reviews':reviews}
(out/'DIRECT-20-SCREENSHOT-REVIEW.json').write_text(json.dumps(summary,indent=2)+'\n')
(out/'README.md').write_text('''# T-2484: actual published 1812 Kinzie house completion review

The pale squared-log house, 2.50m clear west end door,17m reconstructed green and four-poplar row are implemented in PR[1919](https://github.com/kevinrhaas/chicago/pull/1919). Two cottonwoods remain unchanged. Seven house+native-green source comparisons are Matches with source/date/camera disagreements explicitly adjudicated; procedural trees are qualified separately here.

Actual full publication uses c7f15e3db13660d7e6d2599effcee6c6d3304d86, build c7f15e3db1, official publisher/freshness/closing checks PASS. Final source2beb73357a68a2678e8663b6acc4ce4120943dea has exactly the same entire chicago/4d tree; its only delta is an external research README. All tracked native assets/registries/packages match independently audited d6076c038f5d7e103c922110b568c3188436ec25. All1050 native input recipes are fresh.

[Direct review](DIRECT-20-SCREENSHOT-REVIEW.json) covers9 desktop +9 default-phone views +2 closer phone supplements. All six actual planted-stem IDs, species, heights and terrain stations match source; page/console/request/response errors are zero. Desktop separates the four poplars and both cottonwoods. Phone perspective/detail overlaps row crowns; these views do not establish four separately visible phone crowns. Existing tree surface colour inherits inferred ecology, while authored planting coordinates/heights remain reconstructed in Source/Lib. No per-stem R shader proof is claimed.

Original desktop9 runner completed its images/UI checks but then imposed phone-only source-release on desktop. Its literal FAIL is retained. The independent resource-only desktop recovery proves the actual policy: desktop retains source geometry; coarse default phone releases and collapses it. Phone full9 and supplement runners PASS. Two earlier wrong-URL fixtures captured no world; original receipts are preserved. Ignored generated pictures-pin fixture failure is preserved, followed by official compiler/exact published-output binding.

Native bake run42818215260 is authenticated Ubuntu26.04/Blender4.5.3. Its strict audit proves83 defaults, exactly2 changed targets, all81 control MASTER/WEB/LOD byte-exact, and961 foreign defaults+6 variants unchanged. Door leaf head2.52m with .02m sill is measured from actual leaf triangles. [Committed native/seven-picture dossier](https://github.com/kevinrhaas/chicago/tree/2beb73357a68a2678e8663b6acc4ce4120943dea/chicago/4d/docs/RESEARCH/kinzie-completion-T-2484).

Broad native runtime coverage is17/18 passed legs; desktop13 hit the40-minute cap twice without assertion failure. Both actual logs are retained. It is an old1835 UI leg and does not test these1812 targets. No full18-green claim is made. The frozen6b Part4 stale worn-ground/land-owner outputs were officially regenerated; final protected source checks and ordinary dev merge remain required. This packet is runtime/source evidence, not a bypass of GitHub checks.
''')
files=[]
for p in sorted(out.rglob('*')):
 if p.is_file() and p.name!='MANIFEST.json': files.append({'path':p.relative_to(out).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(out/'MANIFEST.json').write_text(json.dumps({'files':files,'count':len(files),'bytes':sum(x['bytes']for x in files)},indent=2)+'\n')
print(json.dumps({'packet':str(out),'files':len(files)+1,'bytes':sum(x['bytes']for x in files)}))
