# PR1175: finite merge-qualification recommendation

The smallest defensible route on the currently observed broad integration is one fixed GitHub test-merge snapshot, the ordinary current PR checks, and the existing published smoke coverage on that same snapshot. Do not restart the source branch for every metadata-only DEV append. Do not rename historical source-head results as current test-merge results.

## Existing policy and tools

AGENTS.md lines 774–780 requires both check.sh and the published renderer gate before merge, with both 390×780 and 1280×800, zero page errors, and no weakened assertions. docs/SMOKE-BUDGET.md permits selecting affected parts but explicitly says a staged pass is not the whole gate. The existing smoke budget map returns ALL parts for data/scenes, data/structures and unrecognized runtime modules. I ran only its inexpensive source planner for the current building-feet/buildings/scene/terrain/Green Tree paths: it returned parts 1–15. No browser was run.

The present merge changes actual terrain, eight building footprint projections and enclosure/frontage/yard geometry. buildings.js now uses native wall feet to choose placement. Relative to b092, guide/Inspect/Navigator/tour and street-tree modules also differ. This is more than the earlier four affected 1904 parts. Old results are useful evidence but cannot fill current town-grounding, traversal, batching, flora, source UI or arrival coverage by assertion alone.

The existing dev-smoke-state.mjs treeHash uses index blob identities for renderers/data/assets/smoke plus published markup with only its build stamp normalized. Changelog is hashed separately for part 13. It is not a per-part dependency proof and does not authorize ignoring altered terrain, scene or runtime files. Its own standing record is explicitly a record, not a bar. A matching exact rendering-input projection could support reuse across different commit metadata, but the current broad integration does not have that identity with 779 or b092.

## Exact test-merge branch is a valid verification carrier

The unchanged chicago-4d-smoke.yml is dispatchable on a branch; actions/checkout@v4 checks out that dispatched ref, publish.sh builds its mirror, and the next step runs smoke_renderer.mjs --published. Creating an isolated stewardship ref at the exact existing refs/pull/1175/merge commit requires no authored source or workflow edit. Its labels must say verification of that test merge, not a new feature build. Record the source workflow, synthetic merge SHA/tree, both parents, dispatched branch and actual executed checkout. This tests the combined tree including the DEV T3032 correction; it does not mistakenly repeat the known older source without that fix.

Use the existing stage ranges to tile all 1–15 once per viewport, not a new collector or a single expensive unstaged process. This is one immutable verification batch. The normal PR gate uses default checkout and therefore checks the event's GitHub merge commit; bind its actual checkout too. The source-head and synthetic merge SHA differ legitimately: qualification is by the exact actual combined tree and parent bindings, not by pretending their commit IDs are equal.

A SHA-pinned ordinary PR merge pins the PR head, not DEV. Immediately before merge, GET the live PR head/base and synthetic test-merge tree. Require the same reviewed head and tested resulting rendering tree; inspect any advance before treating old evidence as applicable. Do not claim this API creates an atomic base pin. An advance that changes real render inputs needs affected coverage; an unrelated prose/ticket/build-stamp-only advance need not restart all 18 runs if exact relevant input equality is established and required checks remain green. If GitHub requires an updated branch, that requirement still applies.

## What person evidence can be retained

Read-only git comparisons found no differences from 779 in assets/humans, data/humans, the specified human runtime files, or the compiled 1835 people file. The prior actual canonical/loader/garment/identity readbacks and desktop/mobile person appearance records remain valid evidence for those unchanged assets and behaviors. Their original heads, dates, limits and failures remain attached. They do not become fresh screenshots of the changed town.

No new canonical generation, loader matrix or exhaustive matched-view grid is justified merely by unrelated DEV append. The fresh published smoke already checks ordinary human bootstrap and the current town budgets; current source tests check exact installed assets/eligibility. A new same-camera person support/appearance check is required only if the final integration changes its actual ground at E −94, N −36.5, its placement/consumer/asset, or the matched view's framing/occluder dependencies. The packet does not prove those local dependencies unchanged against future T3032 data, so verify that finite comparison rather than assuming it. Keep all Full/combined/Balanced timeout failures as failures with their original contexts; no new gait, photo or focused-flag acceptance follows.

## Decision

Recommend the proposed exact GitHub test-merge verification ref and one published all-part batch for this broad integration. It is compatible with existing tools and honest about the normal gate's source. A four-part-only substitution is not supported by the current dependency delta or existing map. After this fixed snapshot passes, do not lap/re-run indefinitely for commit metadata alone: compare the actual last target advance, preserve valid input-bound evidence, and merge ordinarily while the reviewed head and required current checks are green.

This is a read-only engineering recommendation. I did not fetch or independently verify the latest d1cea object, dispatch CI, mutate refs, edit app/tickets/workflows, launch a browser, or decide the final merge.


## Existing lap is the sanctioned convergence path

`.github/steward/pr-lap.sh` lines 825–860 explicitly omit a pre-push full check.sh because that repeated gate prevented queue convergence. The existing `chicago-4d-pr-lap.yml` supports `only=1175`, installs the declared dependencies and runs the supported resolver/lap. Thus a ready, non-held PR with its own lease released can be lapped, regenerated and pushed once, then qualified by actual CI. This does not require another local full gate before that supported lap push. The comment's old assertion about all-branch push triggers is historical; current PR synchronization is the actual workflow trigger that must be observed, not assumed.

Reacquire the lease after the actual successful push: the lap checks it again immediately before push and deliberately refuses if another owner acquires it during regeneration. The lease protects the repository lap and merge-ready actors; GitHub-native auto-merge does not consult that lease. Keep native auto-merge unarmed before exposing the PR as ready, otherwise a green normal gate could merge it before the supplemental published verification finishes. Do not call a lease by itself an atomic merge prohibition. Preserve the existing lap refusal on unresolved authored conflicts, and compare the resulting actual head's human/source pins before accepting its push.

A finite local terrain comparison additionally found the exact bilinear field metadata and all 16 grid vertices covering the 4 m square centered on Bardwell's actual E −94, N −36.5 unchanged from b092 to coherent 4459. See `BARDWELL-LOCAL-GROUND-IDENTITY.json`. This supports retaining the source-bound shoe/support evidence; it does not transfer the town background, global performance, or future DEV changes. It does not require repeating the expensive canonical person grid just to prove that unchanged local sole field again.
