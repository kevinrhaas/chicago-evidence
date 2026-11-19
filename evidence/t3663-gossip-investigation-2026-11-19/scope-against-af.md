# T3663: bounded validation recommendation against af466d163

Recommendation after PR #2197 lands and T3663 is integrated on its actual DEV result:
run official published **stage 15 at both widths**, plus the **actual completed Gossip
case flow at both widths** and the prepared **native DOM/export fixture**. In the same
Gossip boot, exercise the existing daybook → back-to-Jaunts path and Go-to text ownership.
Reuse complete passing earlier stage receipts only after confirming the final integrated
inputs and unaffected assertions equal their accepted baseline. This is a proposed
coverage scope, not granted release coverage or a reason to accept incomplete groups.

## What existing stages actually cover

- **Stage 15**, `tools/smoke_renderer.mjs:22094–22209`: imports the lazy Jaunts path,
  starts `new-in-chicago`, opens linked cards/sources, changes mode, moves between stops,
  pauses into the Continue card, resumes, ends early, starts `taverns-of-chicago`, and
  clears a paused outing with Explore Myself. This directly exercises preview/list/Continue
  integration. It does **not** finish a jaunt or inspect an eligible outcome card.
- **Stage 13**, lines 18423 and 18587–18621: selects Jaunts during Field Check, then opens
  the Navigator License daybook and returns to the list. This exercises the shared
  preview shell/daybook. The Field Check completion is not a completed Gossip session.
- **Stage 14**, lines 20552–20566 and 21827–21850: opens Jaunts' Go-to host and checks
  input ownership. It does not open a completed outcome.
- **No existing official stage** selects Gossip or asserts its completed-outcome comparison.
  Repeating all fifteen stages would still leave that new behavior untested.

## Why this can be bounded

Only five runtime files are owned by this feature: jaunt-preview.js and four new
investigation model/view/strings/CSS files. The preview adds an isolated stylesheet,
one session-scoped draft and an outcome-only mount. The model returns null for unrelated,
interrupted, in-progress, unvisited or uncited sessions. New CSS selectors are confined
to the investigation's classes; new strings use only the new investigation namespace.
No existing controls, world tick, geometry, source/jaunt data, routing, storage schema,
Notebook implementation or renderer assertion is changed.

`/tmp/t3663-scope-against-af.json` preserves Git-object equality for data, assets,
generators, main, jaunts/menu/journal, notebook model/view, controls, shared string registry
and the full smoke harness. The stage 13 daybook and stage 14 Go-to owner functions are
unchanged; checking those paths in the dedicated Gossip boot covers shared-preview
loading without replaying all of either long stage. Add a fresh whole stage 13 if the final
integration changes the served changelog or any of its other inputs beyond the accepted
baseline; do not assume that future DEV is still af.

The branch is intentionally still based on347. af adds only the T3562 changelog fold:
removal of its pending entry and a changed changelog.js. These inherited differences must
be preserved when root integrates the feature; do not carry the older feed onto DEV.
The new T3663 pending entry is source-gated and is not served before the normal fold.

## The automatic budget fallback

`node tools/smoke_budget.mjs --for-diff af466d163` was read, not ignored. Its saved output
is `/tmp/t3663-smoke-budget-against-af.log`. It maps jaunt-preview to15, but the two new
modules are unknown, scoped CSS matches the generic chrome rule, and new strings match
the generic all-strings rule; therefore it mechanically recommends1–15. Its module comment
also predates the stage13 daybook checks. No map or assertion was changed. A reviewed,
precise coverage entry could document this case; generic all-CSS/all-strings rules should
not be narrowed for other features.

## Dedicated new behavior that must run

Complete the real four-stop Gossip route using its actual start/choice/next/finish controls
and normal committed visits (official travel.simulate may finish travel). Do not inject a
fabricated completion state into the published-world proof. At both390×780 and1280×800,
verify the initially collapsed case, native keyboard/Space ownership, both source readings,
missing figure, Inferred Springfield/shared locator, chosen support and claim/uncertainty,
ungraded review/revise, explicit Save and readable Notebook entry. Check daybook/back and
Go-to ownership in that same live document; release it before booting the other viewport.

The separate no-world fixture covers native summary/checkbox/textarea/save traversal,
visible focus, status announcements, storage refusal, repaint/replay/dismiss behavior,
200% text, escaped HTML and actual PDF output. The pure suite covers all five tellings and
real bounded-store/export negative cases. Full source/preflight remains required on the
final integrated branch. Neither this recommendation nor the prepared fixture is a pass.

## Import and first-open effects that must not be overlooked

`main.js:6047` keeps jaunt-preview behind `ensureJaunts()` dynamic import. Its callers
are explicit jaunt start/daybook actions and `openJauntList()` (main6324), not a new boot
hook. The main and caller functions are byte-identical to af. Once that boundary loads,
preview now statically imports the new model/view; those import the new string namespace.
`createJauntPreview` also appends the new stylesheet once even when no eligible case is
present. Thus a non-Gossip Jaunts opening gains module/CSS requests and parse work:
returning null from `gossipInvestigation` does not make those load effects disappear.

The view's `field-notebook.js` dependency is already on main's static `people.js` import
path (main154, people44); the new path reuses the module singleton. Its construction
allocates a bounded listener set but reads/writes no storage until called. The case model
and strings perform no fetch, DOM mutation or storage access at module evaluation; the
new namespace does not replace any existing namespace. CSS is wholly scoped to the new
component and is linked only once per document. Draft allocation happens only for an
outcome and replaces the one previous session's draft; no world/render loop is created.

Fresh stage15 is therefore required to exercise the changed lazy-loading boundary even
though its outings never make the case eligible. Its existing response/console/pageerror
listeners, completion and vendor checks must remain intact. The dedicated published
flow should record new module/CSS requests and confirm they load successfully before
opening an eligible case; this is also why a DOM-only fixture cannot replace it.
If postmerge DEV changes the import boundary, boot/precache manifests, shared styles,
controls or source data, revisit the proposed reuse scope rather than assuming this
analysis still holds. No coverage-map change was made.
