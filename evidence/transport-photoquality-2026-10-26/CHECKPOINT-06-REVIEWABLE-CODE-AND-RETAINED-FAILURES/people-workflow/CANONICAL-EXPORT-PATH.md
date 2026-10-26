# T1789: checked source, remaining canonical export path

Status: proposal only. No workflow was edited or dispatched. Application HEAD is `1cbb1817508593562f99ed378b6932368b5699b9`, clean, checked and normally pushed; draft PR1346 is the source-review surface. The source garment preview is a draft. No female canonical master, portable derivative, photographic approval or ticket completion is asserted.

## Existing supported dispatch cannot target this source

Observed accepted dev was `e871d5c3b06c08dbe2ae21048f5a3989712877d9`. Its T3169/PR1339 fix (`ad283c0419d66153c84dd86b500e1ace2783f96e`) pins the human study worker to Ubuntu24.04, compatible with the existing Playwright1.56.1 installation. The old floating runner and Playwright-install failure are consistent; inaccessible old job logs do not establish the exact old exception.

`chicago-4d-humans.yml` has only `build_teamsters` and `build_seated_driver_study` inputs. Its checkout has no ref override. Dispatching dev uses dev source; dispatching the checked feature uses its old workflow definition. The three generation, hierarchy and validation loops still select only Bardwell, Dufresne and Martin Flynn with `worker_1835.json`. Artifact patterns `*_1835.lod*.glb` exclude `flynn_mary_1835_dress_study`, and the master path includes only `teamsters/`, not `dress/`. The era workflow supports only1812/1904. Thus there is no current normal dispatch that combines the fixed dev definition, exact1cbb source, and this female study.

## Smallest proposed explicit route

Correction to the first proposal: a new workflow generally must exist on the default branch before GitHub will register it for dispatch. Accepting a new dress workflow only on dev would therefore not establish a dispatchable route. A main-branch promotion is outside this scope. Do not use the earlier proposed new filename/command.

After a reviewed workflow change is authorized, extend the already registered `.github/workflows/chicago-4d-humans.yml` with one opt-in `build_dress_study` boolean input (default false), one `source_ref` string (default empty), and one separately gated `dress-study` job. Keep existing three-male generation/packaging loops, their recipe, the default fixture path, both existing opt-in defaults and the era workflow unchanged. This would use existing checked native CLI tools; no builder/exporter change is currently justified by static review. This is one existing workflow file, not a new workflow registration or main-push proposal.

For a dress dispatch require `source_ref` to be an immutable lowercase40-hex SHA and, initially, exactly the reviewed `1cbb1817508593562f99ed378b6932368b5699b9` allowlisted in the workflow change. A future different source requires its own review/binding and allowlist update. Disallow combining the dress option with either existing male/seated option; reject a nonempty source_ref when dress is false. Run this request validation as a small inline step in `humans` before checkout, using environment variables rather than interpolating input into shell source. Ordinary pull_request/push/default dispatch behavior retains its original checkout, dependencies and fixture/actor checks.

Only for that validated dress dispatch, make the existing `humans` checkout select source_ref. Its existing native byte-verification/browser/actor checks then actually qualify the same source used by `dress-study`. The new job must `needs: humans`, be gated only by `workflow_dispatch && build_dress_study`, check out the same same-repository SHA, independently verify `git rev-parse HEAD` equals the validated input and run the source-specific reproduction checks below. It must not substitute successful fixture verification on dev for fixture verification on1cbb. Both jobs should record the workflow-definition SHA/ref and actual checked-out source SHA; name dress artifacts by the latter. The existing male job checkout and conditions need no changes.

Retain read-only contents permissions, Ubuntu24.04, Python3.11 and Node22. Use `persist-credentials: false` for explicit study-source checkouts, no environment secrets, no write token and no arbitrary repository, command or recipe/path inputs. The fixed reviewed SHA avoids treating arbitrary user-selected source as approved executable code. A separate source SHA does not change the pinned worker definition or expand cache keys from unchecked input. Preserve existing cache semantics; source-controlled code is restricted to the reviewed allowlist. Preserve failures and never use `pull_request_target` to execute this source. The existing workflow concurrency group can cancel another run on the same ref; schedule any later authorized dispatch after checking that ref has no run that should be preserved. No dispatch occurs during this proposal.

Use normal YAML/workflow validation, the existing runner-image checker, repository CI and the complete required native source preflight for the eventual workflow change. Static workflow checks must cover default/PR/push behavior, each existing male/seated option, valid exact-source dress, malformed/nonallowlisted SHA, a source_ref without dress, and mixed study options. Inspect the resulting job graph and confirm all new actual-asset validators select the fixed female ID. Neither a static matrix nor a passing fixture is actual new-master execution.

Future request, only after that route is accepted on dev:

```
gh workflow run chicago-4d-humans.yml --ref dev \
  -f build_dress_study=true \
  -f source_ref=1cbb1817508593562f99ed378b6932368b5699b9
```

The existing workflow file is already registered; the proposed new input/job still must be accepted on the selected dev revision before this command is valid. This is not a claim that the unmodified current workflow accepts these inputs. No main promotion is requested. If reviewed source changes later become necessary, qualify their new SHA instead of relabeling1cbb.

The new disposable dress job should install the existing pinned dependencies and depend on the existing same-source fixture job, then:

```
python tools/compile_scene.py --scene 1835
python tools/test_human_dress_components.py
python tools/human_base_prepare.py --source-manifest SOURCE-female.json \
  --height-m 1.65 \
  --target-recipe assets/authored/humans/makehuman_hm08/adult_female_25.recipe.json \
  --output /tmp/dress-study/prepared_adult_female_25.json
cmp assets/authored/humans/makehuman_hm08/prepared_adult_female_25.json \
  /tmp/dress-study/prepared_adult_female_25.json
```

Create `/tmp/dress-study` before the command block. The prerequisite `humans` job must have run `bash tools/human_export.sh --verify` using the native4.5.3 cache on this exact source. Restore its existing pinned cache in the new job. Invoke its pinned Blender binary with `--factory-startup --python-exit-code 1 --python tools/human_teamster_blend.py --`, fixed recipe `data/humans/recipes/adult_dress_1835.json`, variant `flynn_mary_1835_dress_study`, umbrella Liberty `L418`, and master `assets/authored/humans/dress/flynn_mary_1835_dress_study/canonical.blend`. Preserve the separate dress Liberty already carried by the component metadata. The existing explicit `--experimental-normal-probes --normal-probe-receipts /tmp/dress-study/normal-probes` diagnostic opt-in can match the accepted male study path; retain the existing actual1e-3 readback gate. No seated/driver options apply. Export with the unchanged `human_export.sh --master` path.

Build a same-new-master parented control using existing `human_hierarchy_control.py --test-only-parented-control`, export it with existing `human_export.py`, and run the same `human_skin_canonicalize.py` diagnostic path. Supply that control/root pair to `validate_hierarchy_controls.mjs`; do not infer hierarchy qualification from the old male artifacts.

Run animation-time audits on all eight actual new raw/web LODs, existing hair source/runtime checks and the ID-selectable `check_human_hair.py`, and Khronos validation on all eight files. Require fresh `human_fixture.mjs --write` success; this command intentionally measures every GLB present and has no asset-ID selector. Run the normal publisher, inspection self-test and ID-selectable `human_teamster.mjs` source and published inspections with `--sole-contact`, four LODs, both viewports and explicit raw/canonical/hierarchy frame pairs with21 samples per clip. Preserve all return codes and actual-image diagnostics. Mechanical success leaves photographic and clothing fit review open.

Always retain logs, fresh reports, source/definition SHA bindings, normal/frame/hierarchy diagnostics, the new dress master and all eight raw/web GLBs, measurements and actual rendered frames under a study artifact. Use exact female paths, not the existing male-only glob. A failure upload may contain partial outputs; its mere existence is not qualification. Never substitute an old carried measure file for a command that did not run.

## Dependencies and space

Use `generators/blender.pin` unchanged: Blender4.5.3 CLI, verified SHA256 `975c58fcb244273838534bba771e64ad87739216b0f9b39a888531a49a72d845`. Existing Blender4.3.2 and the documented BPy-wheel fallback are not this supported CLI path. Reuse existing glTF-transform4.5.0 pins, Playwright1.56.1 with Chromium/dependencies on Ubuntu24.04, gltf-validator2.0.0-dev.3.10, and existing Python dependency list. No policy bypass, alternate artifact route or repeated blocked download is proposed.

The earlier three-male partial artifact12629696462/run40273347532 is473,179,002 compressed bytes, not a measured bound for the proposed female run. A complete future artifact and its unpacked footprint are unknown. Obtain actual archive size and entry census, then reserve compressed plus unpacked plus native working-copy demand before ingest. Current official artifact-host policy remains unapplied; generation on a hosted runner would not by itself make local download/qualification possible.

## Static findings and remaining real gates

The two obsolete unconditional male-only waist/hem reads were removed before the checked commit. The actual-source AST regression guard rejects that original failure and a missing ordinary dress key, while accepting the male path. No further definite unconditional male-key, material-name, per-corner-UV or native per-LOD shoe-selection blocker was found. Static checks do not execute BPy.

Actual Blender4.5.3 body-normal readback, modifier/decimation/morph behavior, all56 bones/three sockets, actual clip time/contact, portable export, quantization parity, hierarchy and all LOD skin/eye/hair fits remain unrun for the new female source. The source preview lowered arms about54.4degrees; the canonical idle uses78degrees, so sleeve/torso fit needs the real pose. Pelvis-bound skirt/apron are standing source construction and are unqualified for walking/seated cloth, even though the portable contract produces a mechanical walk. The provisional male-named skin atlas and short04 hair remain female appearance/period risks. Bodice finish, seams/closures, headwear, hair and face/skin realism need actual close views and garment work before photographic acceptance. Keep `production_eligible:false`, walking/seated/photo flags false, reconstructed identity/wardrobe scope and T1789 OPEN.

Normal owner-generated asset intake, newly bound source checks and complete native preflight follow any accepted canonical output or source change; browser/frame evidence must bind the actual downloaded bytes. PR1346 currently qualifies checked source code only. No completion percentage or runtime estimate is supported by these remaining unexecuted gates.
