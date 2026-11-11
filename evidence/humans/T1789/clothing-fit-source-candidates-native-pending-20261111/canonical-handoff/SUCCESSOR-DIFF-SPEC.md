# Owner-visible DEV support proposal: canonical clothing capture v2

SOURCE-ONLY DIFF SPECIFICATION, not executable support, not dispatch admission. ROOT has now authorized preparation of necessary DEV-only workflow support; no MAIN/production operation follows. This supersedes PLAN.md's initial policy constraint on preparing a workflow change, but all concrete current-route limitations remain true. Existing 59914 files and all frozen clothing packets stay unchanged.

The artifact-capture part is a straightforward versioned driver around existing canonical primitives. The complete active-v2 owner is NOT yet a safely fillable patch: its eight actual parents, output hashes, artifact identity and independent fit/codec proofs do not exist. This spec names that boundary and provides finite files, states, command sequence and controls for review. No placeholder is accepted as an admitted value.

## First support PR: capture only, no active owner/asset change

Add exactly these versioned support files, together with a normal DEV changelog/STATUS entry and source-only tests, after the combined clothing source is reviewed. Do not modify v1 producer/export implementation, recipe, admission, derivation or active assets in this support PR. The one additive existing-workflow input/job change is explicit below.

1. Extend the ALREADY REGISTERED `.github/workflows/chicago-4d-humans.yml` additively, manual dispatch only for this new mode. Add `build_clothing_capture_v2` boolean defaultfalse, `clothing_source_ref` full40 string defaultempty, and `clothing_manifest_sha256` full64 string defaultempty. No new workflow file, push/schedule trigger or MAIN merge is proposed. Preserve every existing default/PR/push/dress/teamster/stills input and behavior. Before checkout the current opt-in validation gains a separate mutually exclusive clothing branch; reject any clothing field without its flag or in combination with dress/teamsters/seated/stills; retain the existing dress SHA restriction and ordinary source_ref rejection unchanged. New clothing inputs pass only through env, never inline shell interpolation. Bind fixture verification and the new capture job to the same actual reviewed clothing source; expose a separate clothing_source_sha output rather than overloading dress_source_sha. Add a separately named `clothing-capture-v2` job conditional on explicit dispatch/flag, dependent on the existing fixture job, using contents:read and no push/PR/release/Pages/deploy action. Checkout the exact source with persist-credentials:false, verify the requested manifest hash BEFORE executing the builder, record actual workflow definition SHA/ref and source checkout SHA. Existing workflow concurrency remains unchanged; coordinate one explicit feature ref rather than alter cancellation semantics. The new job uses the existing human-study30-minute envelope; no existing cap changes. Reuse existing Python3.11/Node22 setup, unchanged Blender archive pin and package versions. All Blender execution occurs on this hosted canonical bake runner; none here.

   **Registration/input question remains OPEN:** the workflow ID is already registered from MAIN, but it is not yet demonstrated here that GitHub dispatch against a DEV support ref accepts new inputs declared only in that ref's YAML. Do not assert this without a bounded actual API admission. First confirm the registered workflow ID/path via read-only GET; review the proposed target-ref YAML/schema and exact source pins; ROOT must separately admit the first dispatch. If GitHub refuses branch-only inputs, retain that refusal and STOP—no automatic MAIN change, fallback dispatch with ignored fields, or new workflow registration. Default input values false/empty must make the support change inert on every existing event.

2. `data/humans/studies/clothing-capture-v2.json` — a *capture request*, explicitly `status:source_only`, `assets_installable:false`, `native_fit_accepted:false`, `material_admission:null`. It declares a finite exact `(recipe_path, variant_id, component_assembly, liberty)` set; every recipe/variant must agree with its actual source JSON. No arbitrary recipe or runtime role substitutions. It records exact source input paths/SHA256 (producer, raw exporter, canonicalizer, texture labeling, pin/codec owner, all changed/shared helpers, recipes, body/source/skin/license records, and contract). Do not embed a future source commit in the same manifest and create a circular self-hash; source SHA and manifest SHA are independently pinned by dispatch. ROOT must freeze the final variant set after combined source validation; transitive staleness may add more variants without inventing byte invariance. This manifest contains NO expected new GLB or v2 material hashes.

3. `tools/human_clothing_capture_v2.py` — strict orchestration/inventory owner. Validate source+manifest and finite entries before creating output. Refuse output under APP/repository and refuse pre-existing output; all outputs stay below a fresh RUNNER_TEMP directory. Resolve every source input and verify declared size/hash before builder launch. Snapshot actual Git-tracked APP/source/active asset hashes before and after. Build masters by invoking unchanged `human_teamster_blend.py` with exact recipe/variant/liberty and external master output; invoke unchanged `human_export.py` with an external raw directory and `HUMAN_EXPORT_EVIDENCE_DIR` external. Then call the existing canonicalizer and exact existing codec commands below. Do not call `human_export.sh` pretending its v1 Charles terminal accepted; this successor is explicitly artifact-only and cannot install. All mesh authoring/export settings remain in the existing Python owners. The only newly owned behavior is quarantined orchestration, manifest checks and durable artifact inventory.

For each family:

```text
existing pinned Blender -> human_teamster_blend.py -> external canonical.blend
same pinned Blender -> human_export.py -> external four post-frame-repair raw GLBs
  retain pre-frame-repair raw GLBs + existing frame receipts separately
for LOD0..3:
  human_skin_canonicalize.py RAW -> external parents/assets/humans/NAME
  human_web_texture_inputs.py MASTER -> external temporary labeled GLB
  pinned GT resize (2048/1024/512/256 by LOD)
  pinned GT jpeg formats=* quality92 pattern=c4d_web_opaque_* slots={baseColorTexture,emissiveTexture}
  pinned GT meshopt level=medium quantization-volume=scene quantize-normal=16
    -> external parents/assets/humans/web/NAME
human_contract.py --glb exact eight outputs
strict closed inventory; source/active asset before/after actual-hash equality
```

The GT pins are read from unchanged `web_derivatives.sh` just as `human_export.sh` does. No new mesh generator, exporter setting, skin repair, UV generator, compression algorithm or material fallback is introduced. Exact command-closure drift between this artifact-only versioned driver and the existing owner must be refused by a source control; changing a canonical owner requires this successor's explicit versioned source pin update/review, never v1 admission retargeting.

Capture receipts record: schema/version, definition/source commit, manifest digest, source/pin hashes, actual variant/recipe/body/source identity, actual rig/clip/provenance summaries, all master/raw/frame/canonical-parent files with full SHA256/bytes/Git-blob digest, contract results, complete inventory, source/active actual before/after equality, and explicit `status:CANONICAL_PARENT_CAPTURE_ONLY`, `install:false`, `material_applied:false`, `production_eligible:false`, `native_fit_accepted:false`, `photo_accepted:false`. A completed canonical capture is allowed to be a successful *capture job*, never a release/fit PASS. Distinguish build errors, contract failures and missing/incomplete artifacts; no failure is converted into capture success.

4. `tools/test_human_clothing_capture_v2.py` — tiny pure metadata/fake-runner controls, not Blender tests: reject unknown variant/assembly/recipe/hash/source/output paths before writes; reject incomplete8/duplicate/extra members, source mutation, bad GLB summary/contract return; preserve failure logs; closed inventory and no active writes; exact command args/LOD caps/codec and artifact-only fixed status. Mocked orchestration cannot certify native geometry. Real workflow dispatch remains separately admitted after ROOT review and normal source checks.

The workflow uploads complete external parent output+master+diagnostics with `if:always()` and `if-no-files-found:error`, named from actual source SHA/run ID, without merging or publishing. Failed/incomplete captures are retained with a failure manifest and cannot be input to the next stage. The artifact action gives the actual archive digest/artifact identity; later intake binds those actual values, not a guessed run URL.

## Second support stage: actual immutable v2 parent intake, then material qualification

Do not prepare a seemingly valid `.admission.json` with nulls or guessed expected hashes. After a reviewed actual capture, add `charles-coat-woven-v2.parents.json` with a typed canonical-bake-artifact source binding: actual source+definition commit, exact run/job/artifact ID, archive digest and the eight full member SHA/bytes/Git-blob digests. This is not `parent_revision`; no source-tree membership is claimed for generated files. An intake owner must verify the immutable archive, refuse traversal/links/duplicate/extra members, verify all hashes and recipe/provenance/rig/clip summaries, and write only fresh external output. If the project elects an actual archived raw-parent Git tree instead, map logical8 paths explicitly to that tree and prove real membership. Choose ONE typed binding; no fallback between ambiguous sources.

New files `tools/human_charles_coat_v2.py` and `.mjs` own this new binding and data paths. Reuse unchanged v1 pure `derive`, pixel/map and pinned dependency helpers plus the recipe-agnostic independent MASTER/WEB verification owners; reproduce the existing actual-node world-area/UV-area calibration into a versioned callable location without editing frozen v1 code. Admit only the Charles exact coat material, complete eight immutable parents, exact known version, unchanged palette/map scale/common-macro behavior. Unknown version/recipe/body/hash/metadata is fatal before output. Protect all new parent BIN and nonvolatile JSON and retain precisely the existing one absolute authoring-path exception. New geometry exists in the parents, not as an ignored difference during material derivation.

The new material producer creates two near MASTER and two near WEB children externally with `UNQUALIFIED` receipts. Independently prove all noncoat geometry/materials/images, source component corner streams, rig/binds/clips/morph/provenance, original normal+ORM macro chain and exact pinned codec semantics; official Mikk corners and map ownership remain strict. New FAR files are the new capture's FARs. Separate full-cycle native fit/variation/LOD and photo review still determine clothing acceptance. Record output SHA/bytes from these real children, then perform independent full reproduction before sealing v2 admission. If reproduction differs, STOP; expected output hashes are not repair knobs.

## Third support stage: explicit active-owner migration, never a blanket exemption

Only after the new parent/child proofs exist, add an explicit active version selector and v2 registration/check/reproduction/transaction owner. Existing v1 files/admission/outputs/history remain byte-exact. The active selector must support exactly reviewed v1 or reviewed v2; absence/unknown/ambiguous/mixed family fails. V1 continues to use its unchanged historical owner on its exact v1 family; v2 uses a check at least as strict, not a skip of Charles's gate. Retain independent historical v1 reproduction coverage against its immutable recorded bytes separately from active-v2 checks; never claim old active hashes match new geometry. Existing v1 tests must retain their original corruption expectations.

The v2 transaction may recognize a migration source ONLY as the full exact currently admitted v1 eight-family (all actual hashes), an already complete admitted v2 family, or an entirely fresh external target. Partial or foreign/improved active families fail before writes. Fresh export compatibility is compared to the new admitted8 parents. Once every input/body/proof/expected child has verified, write ALL eight replacements as one rollback-capable operation: new2nearMASTER+new2nearWEB and new4FAR. Preserve all original files on any write/receipt failure; validate inventory/source isolation afterward. No restoring old FARs, no swallowing an unknown body, no silent texture-map deletion. Real refusal/repair/inventory controls and canonical fixture writer/unchanged-asset checks precede candidate APP adoption.

This third stage necessarily changes how the active gate dispatches; that is more than adding data. The exact patch cannot be frozen before the actual v2 parent/admission schemas and proofs are reviewed. The proposed first capture support PR does not make this switch and cannot release new assets.

## Finite delivery order

1. Finish1928 normally; review combined clothing sources and pure pose controls on current DEV.
2. Review this finite T1789-only capture owner/additive existing-workflow support spec. Implement its small isolated source patch, normal source gates, owner-visible DEV PR; no MAIN/production change and no asset adoption.
3. Admit ONE canonical capture on exact reviewed source+manifest, retain actual artifacts and failures. Check actual all-family geometry/identity; do not dispatch loops.
4. Review actual immutable parent intake + versioned material-v2 prototype, then independent reproduction/semantic/fit/native budget evidence. Only real proofs can fill the admission.
5. Review explicit active selector/atomic8 migration with meaningful refusal/rollback controls. Integrate qualified bundle+canonical fixture receipts, current complete source/renderer/PR gates, then normal future combined DEV PR. T1789 remains open.


## Guarded future dispatch request (NOT authorized or executed)

After the exact support source has been reviewed, committed and pushed by ROOT with normal checks, the request is to the *existing registered* portable-human workflow. All values below are unresolved REVIEW placeholders; no shell script or auto-dispatch helper is supplied. Use structured request data, not user-input interpolation:

```json
{
  "endpoint": "POST /repos/kevinrhaas/chicago/actions/workflows/chicago-4d-humans.yml/dispatches",
  "admission": "ROOT_REVIEW_REQUIRED_NOT_GRANTED_BY_THIS_DOCUMENT",
  "ref": "REVIEWED_T1789_SUPPORT_FEATURE_BRANCH",
  "inputs": {
    "build_clothing_capture_v2": "true",
    "clothing_source_ref": "ACTUAL_REVIEWED_FULL40_SOURCE_SHA",
    "clothing_manifest_sha256": "ACTUAL_REVIEWED_FULL64_MANIFEST_SHA256",
    "build_teamsters": "false",
    "build_seated_driver_study": "false",
    "build_dress_study": "false",
    "render_library_stills": "false",
    "source_ref": "",
    "library_source_run": ""
  }
}
```

Required pre-dispatch questions: registered workflow path/ID exists; target feature ref remains the reviewed exact commit; GitHub supports target-ref-only input declarations; source+manifest/producer pins match; all combined pure source controls and normal support source gates passed; no conflicting same-ref run; planned external artifact size/run bound reviewed. A 204 only means request accepted; fetch the resulting run and verify actual source/definition SHA, event, requested flag and exact job before treating it as the intended capture. Failure/unknown input/missing job/mismatched source is NONPASS, not a reason to repeat an unchanged expensive bake. Current phone/render jobs and1928 remain separate.

Add metadata controls for mode isolation: all legacy fixtures/defaults/dress restrictions unchanged; newflag absent makes no newjob; every mixedflag/partialnewfield rejects before checkout; unknown schema/recipe/variant/assembly/hash rejects before output; definition/source/manifest mismatch rejects before Blender; malicious paths/duplicate members/missing family/source mutation reject; all four LOD caps/codec args exact; no active APP write/push/deploy; missing artifact/failure status cannot yield release eligibility. This is one finite T1789 capture task, not a general export framework.
