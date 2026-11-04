# T-3041 parade fix: genuine isolation repair in progress

The original seven authored postimages remain exactly those preserved in evidence commit 8db78f8de6488bf692e330d2cda6aa58db65c7f5. They are on branch `steward/t3041-parade-presence-20261104`, based on merged roof commit 22d624f3e5061dfaf54af0e3429e6278be60abe3. No new code commit or PR has been made yet.

Actual source parts 1–3 passed on staged tree 44ce86cca566c052627bf4d42f3753266245b6d8. Original part 4 failed exactly one step: the new production-loader regression had no measured isolation row. The complete original failure and proper failed reapers are retained here. This is not an all-four pass.

The native targeted instrument, `node tools/measure_step_isolation.mjs --tool tools/test_parade_presence.mjs`, genuinely measured the new declared command. Its row records no in-tree writes. An additional run of that exact regression under the same native probe captured actual child exit 0 and the raw `wrote: []` trace, because the inventory writer itself suppresses child status/output. The native isolation audit now passes. All existing inventory row values are unchanged; only the new measured row, native sorting and measurement date changed.

The generated eighth path is `tools/step_isolation.json`. All seven authored postimages are unchanged. New staged tree fa94320657e0e4dc3a2ae87acaf93acb672d61fa is now undergoing a protected WHOLE part-4 rerun. A qualified checkpoint will bind actual parts 1–3 to the unchanged authored code and repaired part 4 to the measured-inventory delta; it will not pretend every part ran on the new whole-tree hash. No source commit is allowed before that rerun succeeds.

The automatic roof changelog fold is authenticated and must be adopted normally from current dev after this source gate closes. Its old roof entry and all prior stamped history must remain exact, and the fix-only T-3041 file becomes a fresh pending entry. Shared immutable object caches avoid duplicate downloads; no Git GC, force or direct dev/main push is allowed.

The coordinator narrowed actual runtime qualification for this accounting fix to two real 1812 cards plus native parade-ground GPU-hit checks (desktop/mobile), and the existing 1835 native Stage 3 checks at both viewports. The prepared helper still requires the mounted owner, visible trodden-earth geometry, finite GPU hit at the native interior, delegated direct roll, no missing flag, no fabricated building box, zero errors and exact source/Git/published/helper bindings. These four runtime legs are UNRUN. Roof body acceptance is explicitly deferred; original T-3041 and T-2387 image acceptance remains open.

Existing T-3041 is normally claimed by this continuation. The old owned PR1685 lap was normally released; the merged source branch was not pushed again. Latest ticket claim proof and fold-history proof are preserved in prior evidence commit f641103b94f07c7ae281f69b50af9e651a7fcd27. Root owns CPU/GPU and writer leases.
