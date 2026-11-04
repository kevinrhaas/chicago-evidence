# Cold Find V2 — prepared, not applied or executed

V1 stays immutable. This packet contains a two-file runtime candidate, native
unit append, optional actual-adapter motion-composition append and complete
combined motionV2+cold patches. No application edits, parser/syntax checks,
Node tests, native jobs, browser work, gate changes or asset work were run.

The author confirmed a minimal V2 correction: reject a new approach request
for a row already in the terminal failed set. The original fatal handler clears
the intent that failed; without this rejection, a later Find could create a new
intent that ready skips indefinitely. Recoverable deferred spawn rows remain
eligible, and original cold anchor lookup remains unchanged.

Root selected a small transactional refinement inside the same request API:
validate first, successfully stop any live actor, then clear older unresolved
intent and install the new token. Main no longer clears old intent before this
request can return null. A failed new target therefore preserves the prior
valid pending rendezvous and native Travel ride. A replaced ride's old onStop
closure cannot cancel the newer token. No new options or API knobs are added.

Static review found the existing stop-after-generation-check/before-publication
placement correct. Token identity protects newer requests from stale callbacks;
fulfilled intent is deleted; cancellation never resumes a driver. Light carries
an active unresolved intent to the current generation; a retired parse cannot
consume it. Saved fulfilled stops restore stopped. Disposal isolates layer maps.
Fatal source/loader errors retain their original owner and automatic-retry rules.

Both runtime preimages match motionV2 exactly. The two parcels' actual changed
line ranges are disjoint. PREPARED.json records the ranges and hashes; the
combined runtime patch was built by statically combining those nonoverlapping
edits against their common preimages. No git application or execution occurred.

## Patch choices

- Cold-only: CANDIDATE-NOT-APPLIED.patch plus UNIT-COLD-NOT-APPLIED.patch.
- Composed next increment: COMBINED-MOTION-V2-COLD-FIND-NOT-APPLIED.patch plus
  UNIT-COMBINED-MOTION-V2-COLD-FIND-NOT-APPLIED.patch.

Choose one path. Do not apply combined and constituent patches together. Runtime
files must still match the pinned preimages after the current merge/checkpoint;
otherwise adapt and review against the new source. The existing declared
test_driven_assembly step receives the cold tests. No new gate step is added.
All original test lines/assertions remain intact. The combined unit patch also
contains the existing motionV2 test_transport_loop tests and actual-adapter tests.

## Meaningful unit coverage

The cold append uses actual createTownTransport/createTransportLoop, actual
extracted main.goToTarget, actual Travel and shared Interact engine. Its deferred
assembly adapters isolate lifecycle ownership; they do not claim to validate
historical assets or visible bodies. Both configured years are tested separately.
A namespaced synthetic second metadata row tests map-key isolation only.

It covers the first ten original acceptance cases: lazy metadata/no model load;
unchanged route/seat side stand; stop before actor publication/replay; two-second
stopped hold; cancellation false/throw/idempotency; real Travel manual input,
Move Stop, unreachable/replacement and instant arrival; stale/cross-person token
isolation; clearance-checked shared Continue/Stop and no later re-stop; Light
restoration and retired-generation race; disposed-layer isolation; identity/date/
eligibility/Light refusals; typed recoverable spawn deferral and terminal factory/
ground failures. Two actual Travel regressions specifically cover valid old
Find followed by a known-failed target, and same-person Find replacement through
the older ride's native onStop callback. The optional composition block uses real createDrivenAssembly
with existing source vehicle hierarchy to test cold stop, motionV2 synthetic
visual admission, independent stopped looking and first Continue frame zero.

Original acceptance cases 11/12 remain future actual published Find/walk-up and
trusted keyboard/touch/browser acceptance. No unit callback or actor.stop call
stands in for those. Original latency negatives, physical/gait/assets, source
ownership, deadlines, budgets and full-native/real-frame CI requirements remain.

Future unit execution requires Root's separate authorization and a source-pinned
candidate projection or actual approved application. This packet claims only
static review/composition/preparation, not a passing candidate.
