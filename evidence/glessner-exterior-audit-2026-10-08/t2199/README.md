# T-2199 reference recovery receipts

Bounded retrieval for the 1904-07-01 Glessner exterior/courtyard. All 17 original audit rows have explicit retrieval outcomes: ten recovered records (seven visual and three written), seven still without images. Counts are records, not unique photographs. A distinct IIT 1945 facade view is added as copyright/link-only. No copyrighted source-image bytes are committed.

The library report contains the exact unavailable list, remaining-view priorities, present-day measured-photo brief and five unsent inquiry drafts. Yale VRC 36, Box 34 is a seven-photograph lead with unspecified dates/views, not seven invented library records. Four Barford image endpoints returned 34-byte InternetShortcut placeholders; Nickel's image endpoints returned 403. Catalog metadata is not visual inspection.

- `library-validation.log`: eight evidence-review tests, schema, provenance and acquired-file checks passed.
- `source-integrity.json`: existing IDs and local-copy metadata preserved; one explicit rights downgrade (#165), no house geometry changes.
- `browser.log`: 18 details at both desktop and mobile widths, 172 Glessner cards, 17 report rows, seven priorities and five drafts; no page errors or horizontal overflow. Recovered Cornell, preliminary elevation and IIT holder images load.
- `comparison.log` and four Cornell screenshots: published before/after cards at 1280×800 and 390×780; previously unavailable Cornell image now displayed with its retrieval review.
- `report-overview.png`: unmodified report capture.
- `smoke-mobile.log`: selected published stage 12, 101 checks passed. Run on dev base f4172ede before the concurrent T-2195 integration; library implementation unchanged by that integration. This is not a claim to run all renderer stages.
- `smoke-mobile-missing-browser.log`: setup-only attempt before selecting installed Chromium; retained separately, no suite executed.

T-2200–T-2228 remain blocked-owner and commented in the queue. Source findings were appended to 14 relevant held tickets; no outreach or purchases were made.

Delivery [PR #556](https://github.com/kevinrhaas/chicago/pull/556) targets dev. Final combined base is `22685d12` (T-2195 and T-1273 integrated). `final-preflight.log` records all three preflight gates passing; `final-check.log` records all 794 repository steps passing. Since preflight ran before the commit, `committed-changelog-check.log` additionally verifies the actual committed diff. `library-final-validation.log` repeats the eight library tests and validator after integration.

`smoke-desktop.log`: published stage 12, 101 passed, zero failed and zero page errors, 18m39s under software rendering. This complete suite ran on base `6e5a9ec2`, before the final T-1273 household-data integration. The final combined tree is covered by the full gate above; no complete renderer smoke is claimed on that later tree.

Merged into dev as `1bf113e2b6265757339b6c7ce0e0f9c674fe1b52` through PR #556 at 2026-10-09 03:19:23 UTC. T-2199 is done. `held-tickets.json` verifies T-2200–T-2228 remain blocked-owner with commented queue entries. The merged library and changelog match validated feature head `91bfa37b` exactly.

Dev deployment [37878794334](https://github.com/kevinrhaas/chicago/actions/runs/37878794334) succeeded. The [live report](https://chicago.polecat.live/4d/dev/prairie-1904/docs/glessner-reference-recovery.html) and data identify dev `1bf113e2`; all 172 Glessner records match the merged source (`live-dev.json`). `live-browser-with-source-fallback.log` verifies all 18 details at both widths, report/priority/draft counts, 172 cards and zero page errors/overflow. Cornell, the preliminary elevation and IIT images all displayed on both widths in that completed pass.

The first live pass timed out on IIT (`live-browser-iit-timeout.log`). A separate browser and direct HEAD request observed its upstream HTTP 503; `diagnose-iit.log` confirms the existing source-link/copyright fallback rendered. The subsequent completed pass above loaded IIT successfully at both widths. This is an intermittent holder outage, not a claim that a link-only image is permanently available. No source bytes were mirrored to evade the rights restriction.

Final CI: PR gate [37878676314](https://github.com/kevinrhaas/chicago/actions/runs/37878676314), moving frames [37878676313](https://github.com/kevinrhaas/chicago/actions/runs/37878676313), post-merge dev gate [37878738786](https://github.com/kevinrhaas/chicago/actions/runs/37878738786), and dev deployment [37878794334](https://github.com/kevinrhaas/chicago/actions/runs/37878794334) all succeeded. Machine-readable results: `ci-status.json`.
