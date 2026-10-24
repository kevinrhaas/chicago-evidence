Round the catalogue Brougham lamps, repair the planted horse’s eye UVs, and add a safe Western Hotel yard viewpoint.

- **T-3083:** V18 gives the lamps rounded upper housings and narrower lower bodies. Near/mid exports preserve the non-lamp geometry, materials, nodes, contacts, collision proxy and runtime policies. V17 history remains archived.
- **T-3086:** the separately versioned `d4544c28` derivative reproduces from canonical `b479`, changing the declared eye UVs, bounds and derivative notice. Geometry, rig, weights, animation, materials and all six embedded images are preserved.
- **T-3087:** adds the camera at E−124/N−292/yaw221.19. All 19 viewpoints are dry and outside roofs; the previous 18 and actor placement are unchanged. Shared licence, liberty, STATUS and ROADMAP records describe the group once.

The original ROADMAP bytes, historical V17 liberty decision and incoming Glessner records/assets are preserved. The V18 decision is appended. Broader photographic, native/world, gait, tack, team, occupant and riding acceptance stays with the existing remainder tickets; parents T-2794/T-2800 remain split.

Validated head: `be56fb269eee6aa7963b8a8d76d5a950f56f857c`, tree `a38d9b3efebb79ba4b3cb7a7c283360fe8139aa5`, including accepted DEV `de91c45b`.

- Local preflight passed **1,065 steps / 384 self-tests** in 657.702s. Cleanup reaped 721 owned descendants with none remaining. The committed tree equals the validated input; exact-HEAD changelog/ID questions pass.
- Ordered derivation passed 61 steps over two laps, with the final lap unchanged. Independent audits verify protected upstream content and show the two regenerated reports differed only in serialization; exact incoming bytes were restored before validation.
- Fresh normal PR gate and moving-frames checks passed. Report and the build-needed check passed; heavy baking was correctly skipped. The tested merge `0acb98a9` has the same tree as this head. The upstream Ubuntu24.04 runner fix is included through DEV.
- **Browser validation is still running.** Fresh published mobile part 14 passed 127 staged checks with zero page errors and complete cleanup in 560.999s. Desktop part 14 and the remaining local matrix are pending. The independent unfiltered full-smoke CI is also pending. Incoming core/harness changes require all 15 parts at both widths; older-tree results are not counted.

This PR stays draft until complete browser coverage and current CI are verified. DEV delivery has not occurred; production promotion is outside this change.

Evidence: [integrated source and full preflight](https://github.com/kevinrhaas/chicago-evidence/tree/8bd6b24676b988c95a44e6fa3c6371ed4dff07aa/evidence/transport-recovery-2026-10-24/CHECKPOINT-19-INTEGRATED-HEAD-PREFLIGHT-PASS) and [fresh mobile photo-stage pass](https://github.com/kevinrhaas/chicago-evidence/tree/aec47937cf348c35cdfcbfa02afc00e92b9bb6e0/evidence/transport-recovery-2026-10-24/CHECKPOINT-20-FRESH-MOBILE-PHOTO-STAGE-PASS).
