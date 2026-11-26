# Better Trees — T-3747, T-3748 and T-3760

Owner request: improve all trees and flora in Chicago 4D's 1812, 1835, 1871 and 1904 worlds, with adaptive detail and all four seasons. Integration target is `dev`.

## T-3747 methods

Base: `kevinrhaas/chicago` commit `9ce06bacd5a91ce96984114b961837b70b67371f`. Input hashes identify the runtime candidate, including changes made before the final validation snapshot. The app images use the complete generated published tree, its compressed derivatives and the real scene data. Before images substitute only the original renderer modules from that base; data, assets, camera and viewport are held fixed. The gallery is an isolated diagnostic of the actual tree model, batching, materials and existing leaf/bark atlases; it is not a historical scene.

Full adds a close mesh within 14 m: three smaller sprays at different depths and angles, with fine round attachment twigs. The original near level remains beyond that ring. Balanced and Light keep their geometry counts. Rounded normals and shadowed thin-leaf light apply through the shared woody renderer. Capable devices reuse the existing leaf sheet for bump relief. No new external asset, licence or engine is introduced. Artistic approximations are declared in `L-leaf-light-3747`.

The original 1904 desktop comparison was captured before the final woodland fade adjustment. At the fixed Prairie Avenue stand, Full reads 5,398,983 -> 5,807,865 triangles and 1,037 -> 1,038 draw calls, with the same 3,694 street trees and zero page/shader errors. That stand fits the existing district allowance of 6.67 million triangles, not the closer-view allowance. The final candidate adds the existing dissolve to Full woodland close transitions; street and front-yard trees already requested it. `T-3747-inputs-pre-fade.json` preserves the earlier input hashes. Final captures and gate receipts are identified separately.

## Limits and seasonal findings

Chromium here uses SwiftShader. Frame times are observations from software rendering under varying contention, not evidence of low-power or high-end hardware FPS, and they do not establish a performance improvement. Kept geometry byte counts in QA are diagnostic CPU arrays; the project's resident-memory meter separately counts JS heap, ArrayBuffer backing storage, measured GPU buffers and textures.

Tree gallery spring/summer/fall/winter images show deciduous leaf-cover changes and the same winter limbs. The winter image review exposed an inherited evergreen tint-cutoff bug: the cutoff assumes five atlas rows, while the atlas now has six. T-3748 includes that correction and enables 1871 free-roam seasons, while preserving the Great Fire's historical dated stops and the visitor's restored season/time. The earlier gallery's grey winter conifer is retained as the diagnostic finding, not as an accepted final evergreen result.

Local gate and mapped published smoke receipts, final candidate hashes, memory readings and PR/CI links are added below as each item completes. Interrupted attempts are not qualified as passes.

## Qualified readings so far

- `logs/vegetation-leaf-test.log`: actual shader and tree-template/range/fade checks pass.
- `logs/vegetation-smoke-mobile-5.log`: published mobile scene-detail ladder passes, 30 passed / 0 failed, zero page errors, 8 m 46 s on this runner. Worst Full 3,281,273 / 3,630,000 triangles; Balanced 2,337,783 / 2,750,000; Light 994,996 / 1,305,000.
- `logs/vegetation-gate-9of16.log` and `logs/vegetation-gate-2of8-final.log`: partial native gate coverage only. Remaining partitions, desktop and other mapped smoke parts are pending; these files do not claim a complete gate.
- `T-3747-runtime-candidate.patch`: the frozen runtime candidate, applicable to the stated base. Its reverse application was checked against the working tree without modifying it. Final input hashes are in `T-3747-inputs.json`.
- `T-3760-initial-audit.json`: initial 1871 diagnosis, with source hashes and explicit limits. The 3,538 portable context crowns remain a separate path; one is at the pumping works beside the Water Tower. The two named grounds GLBs contain kerbs/railings, with stone and iron materials, rather than baked foliage. The street/context trunk-centre check found no pair closer than 2 m; crown/building intersections and actual published cleanup remain to be checked.

The local native gate initially failed because the session's tickets directory was a symlink that `git check-ignore` cannot traverse. It is now a regular linked Git checkout, and the unchanged isolation-reader self-test passes. The failed partition was rerun and passes. Earlier time-limited attempts and a resident-memory attempt under contention have no qualifying verdict and are not counted.


Native gate update: all eight fresh Node 22 partitions passed with required raster readers, on the frozen runtime candidate. `T-3747-native-gate.json` records the base, rebased candidate, timings and unchanged runtime hashes; `logs/gate-node22-*.log` are the complete receipts. `T-3747-final.patch` is the rebased reviewable change. Rebased preflight, exact-head CI, remaining published scene/smoke and memory checks are still pending; this update does not declare merge acceptance.


## 26 November: rebuild ownership, memory and seasonal probes

The static-release candidate follows the earlier patch: forests own their templates and instance records, repeated choices join their pending rebuild, and old trees remain mounted until replacements are ready. The M1 follow-up patch contains tracked-file changes; its new native regression is under `code/`. The runtime freeze identifies the actual uncommitted candidate.

Published Full desktop memory passes: 1812 **843.7 MiB / 875**, 1835 **1347.0 MiB / 1475**, with zero page errors. These are local readings, not the final full viewport grid. Three close sprays now share a supporting shoot. The static woodland and thicket CPU triangle copies are released through the established path; the moving horizon keeps its arrays. The gallery settles the close LOD before capture; its `geometryBytes` is only retained CPU geometry, not GPU or total resident memory.

The 1871 pumping-works probe under `m2-atomic-pumping/` checks actual visible wood/leaf instance pairs in fall and winter, not just placement counts. Earlier prototype matrices could capture an empty pending forest and are superseded as final image acceptance. The native held-checkpoint regression reproduces that gap and verifies the replacement and repeated request. `T-3760-named-footprint-audit.json` finds no trunk-centre hits against 19 named solid footprint parts, in addition to the previously confirmed two context-shop intrusions. No crown-clearance claim follows from those scans.

The new leaf fixture verifies winter removes legacy deciduous leaf colour and both directional/point shadows while retaining wood. It also retains the vine mask, shadow/night checks, and seven grown habits. Flora CPU/fetched wind-normal pixels remain equal at the sampled times.

Complete native partitions, preflight, exact-head CI and the mapped published smoke remain pending for the final merge. Earlier `T-3747-final.patch` and eight-part gate receipts describe the earlier candidate, before these corrections; they do not cover this runtime. All software frame samples remain diagnostic, with no hardware FPS claim.


## Completed static-renderer comparisons

`m1-final-comparison-receipt.json` binds the frozen M1 renderer, the original renderer overrides and the QA helper to 24 completed cases under `m1-final-scenes/`: 1871 and 1904, phone and desktop, before and after, all three tiers. Every case reports zero page/shader errors at DPR 1. All eight Full cases also pass night-light and Confidence checks. The 1904 desktop jobs were partitioned by tier after two aggregate attempts reached their outer 590-second limit; those interrupted logs are retained and are not passes. Individual completed desktop jobs took 435–512 seconds. Wind and people animation were not locked for the scene captures; frame samples under native-check contention remain diagnostic.

`m2-evergreen-winter/` shows the actual cedar and pine templates retaining green colour under the corrected complete six-row atlas exemption. These are material fixtures, not historical scene photographs. The M2 relief regression first fails on Full → Light retaining the extra sampler, then passes after the reused street/front-yard material drops it and restores the same atlas on Full.

`t3748-t3760-prototype.patch` and `vegetation-m2-complete-runtime.json` preserve the uncommitted seasonal layer over its staged M1 baseline. This is a reviewable prototype, not the final integrated PR head. Its complete seasonal scene sweep, integrated native gate, required CI, published smoke and memory/frame grid remain pending. The M1 native gate is also still completing; these scene receipts do not declare either change merge-ready.
