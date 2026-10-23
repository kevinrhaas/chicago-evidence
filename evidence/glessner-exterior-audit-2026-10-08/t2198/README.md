# T-2198 implementation receipts

[Delivery PR #549](https://github.com/kevinrhaas/chicago/pull/549), targeting **dev**.
The source-review findings are committed with the library at
`chicago/prairie_1904_v1/docs/glessner-source-review.md`.

- `source-integrity.json`: all 168 original IDs, rights, local-copy metadata and source URLs preserved; previous changed fields match baseline exactly; four Florian filenames checked against the corrected subjects.
- `browser.log`: nine representative image-detail records, each at 1280×800 and 390×780. Correct captions, history, exclusions, family navigation, unavailable-image status and link-only rights; no page errors or horizontal overflow.
- `grid.log`: all 171 Glessner records displayed at both widths; no horizontal overflow; disputed-attribution search returns exactly one record.
- `desktop-quarantine.png`, `mobile-quarantine.png`: the source-use restriction in the published library. Screenshots are unmodified.
- `smoke-mobile.log`: published app stage 12, 101 checks passed. This is the part selected by `smoke_budget.mjs --for-diff` for the changelog; it is not a claim to have rerun all 14 renderer stages.
- `smoke-desktop.log`: idle rerun of published stage 12; 101 checks passed, zero page errors.
- `smoke-desktop-startup-timeout.log`: first desktop stage-12 attempt, retained as failed. It ran during concurrent checks and timed out before the scene became ready; zero page errors. The later idle rerun is recorded separately.

Local repository gate: 792 steps passed. `tools/preflight.sh` passed all three gates.
Library: `python3 tools/validate.py` passed, including the six tests in
`tools/test_evidence_review.py`. Desktop and mobile stage 12 each passed 101 checks. CI results are on the delivery PR.

No house geometry or source-image bytes were added or changed. Three new records link to
museum-hosted Florian photographs with copyright/link-only rights. The 17 inaccessible
records remain catalog-only; the other 30 programme tickets remain on manual hold.

Integrated dev `7aed0a2a` after its concurrent people-data change. `combined-preflight.log` records the combined tree passing all three gates (792 repository steps). `merged-changelog.log` verifies the published renderer shim preserves both entries, Glessner v1553 followed by Mark Noble v1552. The complete stage-12 transcripts predate that integration; the library validator and published changelog import were checked again afterward.

Final integration includes dev `a7010885` (the separately landed T-2231 roof correction). `final-preflight.log` records the combined working tree passing all three gates, including 792 repository steps; `final-changelog.log` verifies audit v1555 and roof correction v1554. Existing materialized GLBs were refreshed from the committed dev archive and verified before this gate. Full stage-12 transcripts above predate these dev integrations.

Merged into dev as `f4172ede4f7f3789b503dc0099d08e34ebe948ed` through PR #549 on 2026-10-09 at 02:01:03 UTC (`merge-result.json`). T-2198 is done; `held-tickets.json` verifies T-2199–T-2228 remain blocked-owner with commented queue entries.

Live preview verified at https://chicago.polecat.live/4d/dev/prairie-1904/viewer/#images?b=pa-1800-22 after deployment [37872602397](https://github.com/kevinrhaas/chicago/actions/runs/37872602397) succeeded. `live-dev.json` checks the served 171 records and review UI; `live-browser.log` checks nine representative details on both desktop and mobile, including history, exclusions, family navigation and zero page errors/overflow. `live-desktop-quarantine.png` and `live-mobile-quarantine.png` show the deployed result.

CI at delivery: PR gate [37872508268](https://github.com/kevinrhaas/chicago/actions/runs/37872508268) and moving frames [37872508281](https://github.com/kevinrhaas/chicago/actions/runs/37872508281) both passed on final feature head `c5cc1f6c`. Deployment passed and the live dev build identifies `f4172ede`. The separate post-merge dev gate [37872546129](https://github.com/kevinrhaas/chicago/actions/runs/37872546129) also passed.
