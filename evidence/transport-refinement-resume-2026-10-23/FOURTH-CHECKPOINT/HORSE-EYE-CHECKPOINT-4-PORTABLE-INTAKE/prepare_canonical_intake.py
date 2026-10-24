from pathlib import Path
import copy,hashlib,json,shutil,textwrap
P=Path(__file__).resolve().parent
A=Path('/workspace/chicago-waistcoat/chicago/4d')
Q=P/'CANONICAL-INTAKE-PROPOSAL';assert not Q.exists();N=Q/'new/chicago/4d';N.mkdir(parents=True)
AUTH='assets/authored/transport/horse_standing/'
DATA='data/transport/parked/standing-horse-planted/'
OLD='horse-sevket-v16-planted-standing-v1.glb'
NEW='horse-sevket-v16-planted-standing-eye-uv-v1.glb'
BASE='b479442cb03ac46eb13c19da15a79cdfaf28dbdf356b116f78de7ce7ecdc60be'
TARGET='d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914'
sha=lambda x:hashlib.sha256(x).hexdigest()
def put(path,content):
 f=N/path;f.parent.mkdir(parents=True,exist_ok=True)
 f.write_bytes(content if isinstance(content,bytes) else content.encode())
def putj(path,obj):put(path,json.dumps(obj,indent=2)+'\n')
def readj(path):return json.loads((A/path).read_text())
candidate=P/'V4-CINF-LINEAR-RESERVE-UV/ACTUAL-ONE-UV-ONLY-CANDIDATE/horse-sevket-v16-planted-standing-ocular-uv-CANDIDATE.glb'
assert sha(candidate.read_bytes())==TARGET
put(AUTH+NEW,candidate.read_bytes());put('renderers/web/transport/standing-horse/'+NEW,candidate.read_bytes())

# Portable stdlib generator: embed only the frozen source decoder, not its report loop.
gen=(P/'V4-CINF-LINEAR-RESERVE-UV/generate_eye_uv_candidate.py').read_text()
decoder=Path('/workspace/shared/HORSE-B479-EYE-UV-APERTURE-SOURCE-INSPECTION-20261023/ACTUAL-CORRECTED-READER.py').read_text()
fragment=decoder[decoder.index('fmt='):decoder.index('eye=[p for p in prims')]
decoderfn='def decode_rest(g,B):\n'+textwrap.indent(fragment,'    ')+'    return locals()\n\n'
gen=gen.replace(gen[:gen.index('from pathlib import Path')],'''"""Reproduce the separately versioned, UV-only planted horse eye derivative.

Python stdlib only. Never overwrites a source or existing output directory.
The original b479 source, 4/256 centroid bound, non-fold/crack constraints,
and every non-eye-UV GLB byte/semantic field remain protected. This is an
explicit reconstructed eye appearance correction, not a photographic claim.
"""\n''',1)
start=gen.index("BASE=Path(");end=gen.index("IMAGE_SHA=",start)
gen=gen[:start]+"BASE=D/'"+OLD+"'\nBASE_SHA='"+BASE+"'\nRAYS=D/'eye-uv-v1-source-aperture-rays.json'\nRAYS_SHA='d44a04364da6e3a8dcc23f3e67ea5dc00d14cda9c4c2801d7036e44a1da7a6fa'\n"+gen[end:]
gen=gen.replace('# Frozen proposed trial values. A different trial needs separate ROOT review.','# Versioned accepted source recipe; changing values creates a different derivative.')
idx=gen.index('def main():');gen=gen[:idx]+decoderfn+gen[idx:]
start=gen.index("    parser.add_argument('--root-release'");end=gen.index("    receipt=",start)
gen=gen[:start]+'''    parser.add_argument('--baseline',type=Path,default=BASE)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    baseline=args.baseline.resolve();OUT=args.output_dir.resolve()
    need(not OUT.exists(),'Output must be fresh; no overwrite or automatic retry')
    OUT.mkdir(parents=True)
'''+gen[end:]
gen=gen.replace("str(BASE)","str(baseline)").replace('raw=BASE.read_bytes()','raw=baseline.read_bytes()').replace('sha(BASE.read_bytes())','sha(baseline.read_bytes())')
start=gen.index('        saved=DECODER.read_bytes()');end=gen.index("        prims=env['prims']",start)
gen=gen[:start]+'''        raybytes=RAYS.read_bytes();need(sha(raybytes)==RAYS_SHA,'Pinned exposed-aperture evidence')
        env=decode_rest(g,B)
'''+gen[end:]
gen=gen.replace("file=OUT/'horse-sevket-v16-planted-standing-ocular-uv-CANDIDATE.glb'","need(sha(candidate)=='"+TARGET+"','Versioned derivative digest mismatch')\n        file=OUT/'"+NEW+"'")
gen=gen.replace("        for name in ['ATTRIBUTION.md','LICENSE-CC-BY-4.0.txt','PROPOSAL.md']:(OUT/name).write_bytes((D/name).read_bytes())\n",'')
put(AUTH+'generate_eye_uv_v1.py',gen)
rays=Path('/workspace/shared/HORSE-B479-OCULAR-FIRST-EXTERIOR-20RAY-SOURCE-20261023/RESULT.json').read_bytes()
assert sha(rays)=='d44a04364da6e3a8dcc23f3e67ea5dc00d14cda9c4c2801d7036e44a1da7a6fa'
put(AUTH+'eye-uv-v1-source-aperture-rays.json',rays)

# Independent source boundary checker and meaningful in-memory negative controls.
test=(P/'verify_uv_derivative_boundary.py').read_text()
start=test.index('D=Path(');end=test.index('\ndef decode',start)
test=test[:start]+"D=Path(__file__).resolve().parent.parent;BASE=D/'"+AUTH+OLD+"';CAND=D/'renderers/web/transport/standing-horse/"+NEW+"'\n"+test[end:]
test=test.replace("baseraw=BASE.read_bytes();candraw=CAND.read_bytes();bj,bb=decode(baseraw);cj,cb=decode(candraw)","baseraw=BASE.read_bytes();candraw=CAND.read_bytes();assert hashlib.sha256(baseraw).hexdigest()=='"+BASE+"';assert hashlib.sha256(candraw).hexdigest()=='"+TARGET+"';bj,bb=decode(baseraw);cj,cb=decode(candraw)")
test=test.replace("(D/'ACTUAL-INDEPENDENT-UV-BOUNDARY.json').write_text(json.dumps(report,indent=2)+'\\n');",'')
put('tools/test_standing_horse_eye_uv_boundary.py',test)
boundary=json.loads((P/'ACTUAL-INDEPENDENT-UV-BOUNDARY.json').read_text())
boundary['scope']='Exact source-data equivalence and five rejected controls only; fresh d454 Mixer129 qualification is recorded separately. Historical b479 loaded129 remains historical.'
putj(AUTH+'eye-uv-v1-boundary-receipt.json',boundary)

actual=P/'D454-FRESH-CLONE129/ACTUAL'
readback=json.loads((actual/'READBACK.json').read_text());terminal=json.loads((actual/'TERMINAL.json').read_text())
assert readback['selected_asset_sha256']==TARGET and terminal['exit_code']==0 and len(readback['poses'])==129
put(DATA+'eye-uv-v1-loaded129-result.json',(actual/'READBACK.json').read_bytes())
put(DATA+'eye-uv-v1-loaded129-terminal.json',(actual/'TERMINAL.json').read_bytes())
qualification={k:v for k,v in readback.items() if k not in ['poses','image_shims']}
qualification.update(schema='standing_horse_eye_uv_v1_loaded129_summary',raw_result_file='eye-uv-v1-loaded129-result.json',raw_result_sha256=sha((actual/'READBACK.json').read_bytes()),terminal_file='eye-uv-v1-loaded129-terminal.json',terminal_sha256=sha((actual/'TERMINAL.json').read_bytes()),fresh_input_asset_bytes=candidate.stat().st_size,maximum_rss_bytes=256*1024*1024,original_physical_limits_unchanged=True,old_proof_sha256=sha((P/'D454-FRESH-CLONE129/EXACT-BRIDGE.diff').read_bytes()),historical_b479_summary_file='loaded129-summary.json',historical_b479_summary_sha256=sha((A/DATA/'loaded129-summary.json').read_bytes()),historical_b479_asset_sha256=BASE)
putj(DATA+'eye-uv-v1-loaded129-summary.json',qualification)
qsha=sha((N/DATA/'eye-uv-v1-loaded129-summary.json').read_bytes())

# Stable canonical derivation receipt points at portable source and original baseline.
receipt=json.loads((P/'V4-CINF-LINEAR-RESERVE-UV/ACTUAL-ONE-UV-ONLY-CANDIDATE/ACTUAL-RECEIPT.json').read_text())
receipt.update(baseline=OLD,candidate_file=NEW,portable_generator='generate_eye_uv_v1.py',portable_generator_sha256=sha(gen.encode()),original_trial_generator_sha256=receipt.pop('source_sha256'),source_aperture_file='eye-uv-v1-source-aperture-rays.json',source_aperture_sha256=sha(rays),independent_boundary_file='eye-uv-v1-boundary-receipt.json',independent_boundary_sha256=sha((N/AUTH/'eye-uv-v1-boundary-receipt.json').read_bytes()),original_export_receipt='planted-standing-export-receipt.json',original_export_applies_to_sha256=BASE,loaded_qualification_file='../../../../data/transport/parked/standing-horse-planted/eye-uv-v1-loaded129-summary.json',loaded_qualification_sha256=qsha,qualification_scope='Fresh current-SHA production loader/clone/Mixer129 CPU only. Source-only trial receipt and historical b479 qualification do not imply native/GPU/world/photo acceptance.',native_browser_acceptance=False,photographic_acceptance=False)
putj(AUTH+'eye-uv-v1-derivation-receipt.json',receipt)
rsha=sha((N/AUTH/'eye-uv-v1-derivation-receipt.json').read_bytes())
putj(DATA+'eye-uv-v1-derivation-receipt.json',receipt)

# Runtime exact identity changes only. All physical/channel/lifecycle/budget guards retained.
idle=(A/'renderers/web/js/standing-horse-planted-idle.js').read_text();assert idle.count(BASE)==1
put('renderers/web/js/standing-horse-planted-idle.js',idle.replace(BASE,TARGET).replace('3783600','3784176'))
contract=(A/'tools/test_planted_standing_horse_contract.mjs').read_text();assert contract.count(OLD)==1
put('tools/test_planted_standing_horse_contract.mjs',contract.replace(OLD,NEW))

spec=readj('data/transport/parked/horse-sevket-sidecar.json')
historical={k:copy.deepcopy(spec['idle'][k]) for k in ['loaded_qualification_status','loaded_qualification_file','loaded_qualification_sha256','loaded_raw_result_sha256']}
historical.update(asset_sha256=BASE,bytes=3783600,scope='Historical original b479 qualification only; not inherited by d454.')
def runtime_update(r):
 r.update(file='transport/standing-horse/'+NEW,sha256=TARGET,bytes=candidate.stat().st_size,standing_export_receipt_applies_to_sha256=BASE,eye_uv_derivation_receipt_file='transport/parked/standing-horse-planted/eye-uv-v1-derivation-receipt.json',eye_uv_derivation_receipt_sha256=rsha)
runtime_update(spec['runtime_asset'])
spec['status']='Development planted-standing horse with bounded reconstructed dark-eye UV improvement. Fresh d454 production loader/clone/Mixer129 CPU passed; native app/yard/mobile/GPU/photographic qualification remains pending.'
spec['material_variants']['organic_dielectric_v1']['change_notice']='Declared runtime material adaptation: metalness=0 on all three cloned materials. The selected eye-UV-v1 derivative changes only eye TEXCOORD_0 and its bounds plus derivative notice, affecting both existing eye base-color and metallic-roughness UV maps as runtime uses them. All six embedded image payloads, material records, roughnessFactor0.6, opacity, double-sided policy, geometry, body/hair UVs, rig and clip are exact b479 bytes/semantics. Opaque hair and baked coat highlights remain; no native or photographic acceptance.'
spec['known_quality_limits'].append('Eye UV v1 reconstructs coherent dark brown iris/pupil placement on the unchanged near-closed source globes; gaze and approximately horizontal pupil are authored choices, not measured equine anatomy or historical identity. Same-camera CPU diagnostic was reviewed; actual browser PBR, close eye detail and mobile inspection remain unqualified.')
spec['idle'].update(actual_loaded_mixer_accepted=True,activation_note='Current d454 was freshly loaded and production-cloned for actual Mixer129 CPU checking with unchanged physical guards in an external 1904 diagnostic fixture. This is not 1904 scene activation or app/yard/native/GPU/photo acceptance.',loaded_qualification_status=readback['status'],loaded_qualification_file='transport/parked/standing-horse-planted/eye-uv-v1-loaded129-summary.json',loaded_qualification_sha256=qsha,loaded_raw_result_sha256=qualification['raw_result_sha256'],historical_b479_qualification=historical)
putj('data/transport/parked/horse-sevket-sidecar.json',spec)
manifest=readj('data/transport/parked/standing-horses.json');manifest['models']['sevket_horse_standing_development_01']['file']='transport/standing-horse/'+NEW
manifest['status']='Same1835 development horse placement with versioned eye-UV-v1 appearance correction and fresh current-SHA production clone/Mixer129 CPU pass. App/yard/mobile/native/GPU/photo qualification remains pending.'
putj('data/transport/parked/standing-horses.json',manifest)

source=readj(AUTH+'SOURCE.json');runtime_update(source['runtime_derivative'])
r=source['runtime_derivative'];r.update(adaptation='Original rest surface baked to canonical metres; reconstructed26 rig/V16 skin and one planted-standing clip. Eye-UV-v1 changes only eye UV10, its bounds and explicit derivative notice from protected b479; all image payloads, materials, geometry, body/hair UVs, indices, rig and animation are exact. Original15 rig/clips and original b479 qualification remain separate historical stages. No walking/head-tail composition.',loaded_qualification_summary='../../../../data/transport/parked/standing-horse-planted/eye-uv-v1-loaded129-summary.json',loaded_raw_result_sha256=qualification['raw_result_sha256'],loaded_qualification_status=readback['status'],historical_b479_qualification=historical)
source['authored_exception']='Licensed third-party derivative with exact source/rights/credit/change notice. Portable stdlib eye-UV-v1 generator reproduces the separately versioned derivative from the protected existing b479 baseline; no original-source generator master is asserted.'
source['runtime_adaptations'].append('Reconstructed horizontal dark pupil/gaze from existing source eye texture through UV10 only; original six texture payloads and original b479 baseline remain unchanged. Same-camera CPU software diagnostic informed this limited improvement; photographic completion is not asserted.')
putj(AUTH+'SOURCE.json',source)
adapt='''# Canonical26 planted-standing eye-UV-v1 development derivative

“Horse” by sevketkabatas, CC BY4.0, https://sketchfab.com/3d-models/horse-53a6eb7ccf054aa2a378dd7ec08f88fe, retrieved through Objaverse. The acquired original41acd9bee7bf05fbcdd813fad965027b01b8801d6a21ca1c22eb2178c8842988 remains unchanged. The previous canonical26 planted-standing b479442cb03ac46eb13c19da15a79cdfaf28dbdf356b116f78de7ce7ecdc60be (3,783,600bytes) remains preserved under its original filename and original export/loaded129 receipts.

The selected separately versioned derivative is `horse-sevket-v16-planted-standing-eye-uv-v1.glb`, SHA256 d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914,3,784,176bytes. Its only appearance edit is existing eye TEXCOORD_0 accessor10 (BIN332984..364727,31,744bytes), accessor bounds and a new explicit GLB derivative notice. The reconstructed gaze/pupil maps the existing dark brown iris/pupil into the small exposed source globes. Approximately2:1 horizontal pupil placement and gaze are bounded authored choices, not anatomical measurements or identification of a historical animal. Existing index-connected charts, positive UV orientation, no new intra-chart cracks and maximum4/256UV centroid interpolation error are protected by the generator. No texture pixels were changed.

Geometry/indices/normals, source rest surface, all six embedded image payloads, all material records, body/hair UVs, reconstructed26 hierarchy/joints/inverse binds/weights and one12s13channel65LINEARkey planted body-shift clip are exact protected b479 data. Eye UV10 drives both unchanged eye base-color and metallic-roughness maps as in the runtime. Runtime organic_dielectric_v1 still clones metalness0; opaque hair, baked coat glints and coarse/near-closed eyelids remain. Unit canonical metres/Yup/Zforward/Xleft, zero runtime origin,1mm support/10um penetration constraints and all resource/lifecycle guards remain unchanged.

The earlier canonical stage baked the original rest surface into metres and replaced the original15rig with reconstructed26 controls/V16 skin. Rigged Mid-Poly Horse by antemeossa, CC BY4.0, https://sketchfab.com/3d-models/rigged-mid-poly-horse-fea999c1d8d64eb4a9c2bb1fac1e7d83 supplied hierarchy analogy only, with no donor mesh or animation keys. Original source six clips and earlier head/tail derivative are not composed or played here.

`generate_eye_uv_v1.py` plus pinned `eye-uv-v1-source-aperture-rays.json` reproducibly generate the exact new GLB from the existing old baseline using Python stdlib only. `eye-uv-v1-derivation-receipt.json` distinguishes original export, source protection, and fresh current-SHA loaded qualification. The independent boundary test rejects protected geometry/material/animation mutations, false UV bounds and NaNs. A fresh actual standardGLTFLoader/production SkeletonUtils clone/AnimationMixer129 run passed65keys+64midpoints and the unchanged physical/contact/segment/loop/meaningful negative controls for d454. The original b479 loaded129 summary remains historical and is not relabelled as a new run.

Root reviewed same-camera baseline/candidate CPU texture projections and approved this limited eye appearance improvement. Those are perspective-correct software diagnostics with sampled original image pixels, approximate lighting/PBR and no browser; they do not qualify native Three/WebGL, world clearance, device performance or photographic quality. Native capture attempts failed before any new browser image. Current-SHA native app/yard/desktop/mobile inspection remains pending. No walking, trot, route, tack, teams, horse riding or carriage driving is enabled by this change.

The individual, date, breed, owner, coat, grooming, dimensions, pupil/gaze and precise placement remain reconstructed. Modern model rights/publication do not attest an1835 Chicago horse; existing yard sources supply horsekeeping context only. Existing legal/dataset/acquisition credit notices remain unchanged.
'''
put(AUTH+'ADAPTATION.md',adapt)
attr=(A/AUTH/'ATTRIBUTION.md').read_text();attr+='\n## Eye-UV-v1 change notice (2026-10-23)\n\nThe separately versioned selected derivative d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914 changes only the existing eye UV10 field/bounds and adds an explicit derivative notice to the protected b479 planted-standing model. Its original texture pixels, geometry, rig and planted clip are unchanged from that stage. Pupil/gaze are reconstructed; this is a limited development appearance improvement with no photographic or native-browser acceptance. The source author/license/Objaverse credit above remains applicable to both derivative stages. Portable generation and exact protection receipts are listed in SOURCE.json and ADAPTATION.md.\n'
put(AUTH+'ATTRIBUTION.md',attr)
src=readj('data/sources/sevketkabatas_2021_horse_model.json');src['note']+=' Eye-UV-v1 d4544c28 separately supersedes the selected b479 appearance with reconstructed dark pupil/gaze through existing UV10 only; all six source image payloads remain exact. Fresh d454 production clone/Mixer129 CPU passed without inheriting b479 historical qualification. Native browser, mobile, world, tack, routes and photographic completion remain open.'
putj('data/sources/sevketkabatas_2021_horse_model.json',src)

# Preserve the historical liberty text verbatim; append an amendment within its entry.
lib=(A/'docs/LIBERTIES.md').read_text();start=lib.index('### L-standing-horse-development-2800');end=lib.find('\n### ',start+5);assert end>start
amend='''

**2026-10-23 eye-UV-v1 amendment (T-2800).** The selected planted-standing development horse now has a separately versioned dark-eye UV correction (d4544c28) from preserved b479. Gaze and an approximately horizontal2:1 pupil are reconstructed on the unchanged source eye globes using the existing brown iris/pupil texture. The bounded recipe preserves existing charts/tessellation, rejects folds/cracks and retains the original4/256UV centroid error limit. Only eye UV10/accessor bounds and explicit GLB derivative notice change; original six image payloads, material records, body/hair UVs, geometry, canonical26 rig/weights and planted clip remain exact. Modern horse-model rights do not attest this eye, breed or historical individual. Root reviewed equal-camera software texture projections and approved a limited appearance improvement; current-SHA native app/yard/mobile/PBR/photographic acceptance remains pending. Fresh d454 production loader/clone/Mixer129 CPU passed unchanged physical guards; historical b479 loaded129 remains historical. Opaque mane/tail, baked coat glints and near-closed/coarse eyelids remain quality limits. No route, harness, team, rider or player interaction is certified. **How to resolve:** anatomy/reference-led modelling and actual matched native/browser/device review; no software diagnostic is relabelled photographic proof.
'''
put('docs/LIBERTIES.md',lib[:end]+amend+lib[end:])
status='\n\nT-2800 bounded eye-UV-v1 development refinement (2026-10-23): selected separately versioned d4544c28 corrects cloudy exposed eyes using the original brown iris/pupil pixels through UV10 only. All geometry/rig/clip/material/image payload and budget guards remain exact. Actual independent source-boundary checks and fresh production GLTFLoader/SkeletonUtils clone/Mixer129 CPU65keys+64midpoints passed; old b479 qualifications remain historical. Equal-camera software texture diagnostics were reviewed for this limited improvement. Native app/yard/desktop/mobile/PBR and photographic acceptance remain unverified; native capture attempts produced no new browser image. This does not close T-2800/T-2803 or enable walking, teams, routes, tack, rider or player interaction. Full current-tree integration gates remain required.\n'
put('docs/STATUS.md',(A/'docs/STATUS.md').read_bytes()+status.encode())
put('docs/ROADMAP.md',(A/'docs/ROADMAP.md').read_bytes()+b'\n\nT-2800 eye-UV-v1 checkpoint (2026-10-23): limited dark-eye correction prepared with exact source protection and fresh current-SHA production clone/Mixer129 CPU pass. Native app/yard/mobile inspection, photographic completion, locomotion, tack, teams and interaction remain open; preserve ticket ownership and continue the existing people/horse/carriage bands.\n')
lic=(A/'assets/LICENSES.md').read_text();lic+='\n## Eye-UV-v1 planted-standing derivative amendment (T-2800)\n\nThe historical b479 entry above describes the preserved previous stage. The current separately versioned selection is d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914,3,784,176bytes, `horse-sevket-v16-planted-standing-eye-uv-v1.glb`. Its eye UV10/bounds and derivative notice change; source texture pixels, other UVs, material records, geometry, rig and planted animation are exact b479 data. Reconstructed gaze/pupil is an adaptation under the same sevketkabatas Horse CC BY4.0 source credit and Objaverse database notice, not attested Chicago anatomy or photographic completion. The preceding unchanged-UV statements apply to the historical b479 stage only. Fresh d454 loaded129 CPU qualification is distinct from historical b479 results; neither certifies native/mobile/GPU/world/photographic quality.\n\n|Path relative to assets/|License and provenance|\n|---|---|\n'
newassets=[NEW,'generate_eye_uv_v1.py','eye-uv-v1-source-aperture-rays.json','eye-uv-v1-boundary-receipt.json','eye-uv-v1-derivation-receipt.json']
for f in newassets:
 desc='CC-BY-4.0 derivative of Horse by sevketkabatas; exact changes in ADAPTATION.md.' if f.endswith('.glb') else 'Project-authored UV recipe/source-aperture evidence/protection receipt; source mesh/image rights and author credit remain CC-BY-4.0.'
 lic+='|`authored/transport/horse_standing/'+f+'`|'+desc+'|\n'
lic+='\nByte-identical current runtime copy: `renderers/web/transport/standing-horse/'+NEW+'`. Protected b479 authored/runtime files and original receipts remain unchanged.\n'
put('assets/LICENSES.md',lic)
putj('changelog.d/T-2800.json',{'title':'Clearer eyes on the development horse','kind':'improvement','items':['The standing horse in the Western Hotel yard has a more coherent dark iris and pupil, using its original texture pixels.','Its planted weight shift is retained; photographic detail, walking, tack and riding are still in progress.']})

inventory=[]
for f in sorted(N.rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(N);old=A/rel
 inventory.append({'path':'chicago/4d/'+str(rel),'operation':'modify'if old.exists()else'add','preimage_sha256':sha(old.read_bytes())if old.exists()else None,'preimage_bytes':old.stat().st_size if old.exists()else None,'proposed_sha256':sha(f.read_bytes()),'proposed_bytes':f.stat().st_size})
(Q/'CHANGED-FILES.json').write_text(json.dumps(inventory,indent=2)+'\n')
instructions='''This is an unapplied canonical intake proposal, not app/Git work. Root must compare CHANGED-FILES preimage hashes before applying; concurrent 1904 carriage/horse intake must be merged structurally, never overwritten. In particular standing-horses.json and the sidecar may have advanced. No original b479 GLB is duplicated here. The existing old authored baseline must remain in the app, and both historical original export/loaded129 receipts stay byte-identical.

Generator reproduction (Python stdlib; a new output directory is mandatory):
python3 assets/authored/transport/horse_standing/generate_eye_uv_v1.py --baseline assets/authored/transport/horse_standing/horse-sevket-v16-planted-standing-v1.glb --output-dir /tmp/horse-eye-uv-v1-UNIQUE
Expected GLB SHA256 d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914,3784176bytes.

Targeted source/runtime checks after root integration:
python3 tools/test_standing_horse_eye_uv_boundary.py
node --v8-pool-size=1 tools/test_planted_standing_horse_contract.mjs
node tools/changelog-entries.mjs --check
python3 tools/compile_liberties.py
python3 tools/compile_scene.py --all
python3 tools/compile_source_use.py
Then root-owned ./tools/preflight.sh and required source/published renderer desktop+mobile gates, respecting current environment/browser ownership and actual blockers. Do not weaken or mark skipped gates green.

The proposed tools/test_planted_standing_horse_contract.mjs changes only the versioned selected filename. Runtime idle module changes only exact selected SHA and exact byte count; every previous semantic/physical/channel/lifecycle/budget guard remains. The new independent boundary check additionally rejects non-UV binary/JSON mutations and five meaningful negative controls.

Fresh actual d454 runtime evidence is D454-FRESH-CLONE129/ACTUAL; raw READBACK, terminal and compact summary are copied with exact binding. That CPU loader/clone/Mixer129 pass uses a held external1904 support fixture and does not activate canonical1904. Current canonical proposal retains only existing1835 placement. Root owns any additional1904 intake.

No browser/native screenshot, GPU, world, phone performance or photographic PASS exists. Software images are diagnostic and remain in CHECKPOINT-3. Root approved only bounded dark-eye UV improvement, not photographic completion. Native capture failures remain nonpasses. T-2800/T-2803 stay open. No locomotion/tack/team/rider/player interaction is enabled.

Portable generator must be executed once to a fresh owned output and compared to d454 before this proposal is treated as ready. Source-only original V4 receipt state is retained; new runtime CPU acceptance is separate. Compiler-derived data/liberties.json/source_use/scene outputs are intentionally not hand-edited; canonical root must regenerate them. Existing same-ticket changelog file must be merged if it appears concurrently.
'''
(Q/'ROOT-INTEGRATION.md').write_text(instructions)
print(json.dumps({'proposal':str(Q),'changed_files':len(inventory),'portable_generator_sha256':sha(gen.encode()),'new_sha256':TARGET,'summary_sha256':qsha},indent=2))
