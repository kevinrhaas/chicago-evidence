# T-3551 — owner-held recovery handover

Owner explicitly requested on 2026-11-11: commit and stop work, leave handover materials, and hold PRs so another process does not pick this up. This supersedes earlier automatic DEV merge authorization. **Do not resume, remove hold, rebuild, or merge until the owner explicitly releases the hold.** Do not close the implementation ticket as completed.

## Durable code and scope

- Code PR: https://github.com/kevinrhaas/chicago/pull/1934 — open DRAFT, `hold` label, DEV target. No merge occurred.
- Branch: `steward/1812-seasonal-audio`.
- Latest pushed commit: `c5de44a61e8cd0c254e4d213f5ecd1046cbe4000`.
- Implementation commit: `3df73785f8ba9093ade9d1fed98503cc45ad76dc`.
- Application working tree clean at shutdown; no uncommitted application changes.
- Associated ticket: T-3551 in kevinrhaas/chicago-tickets.
- Existing evidence checkpoint: https://github.com/kevinrhaas/chicago-evidence/tree/0b1687837bc34c4b6664dbdafd03bc695264eaa7/evidence/1812-audio-2026-11-11
- This directory's additional recovery archive and two phone images supplement that checkpoint. They are not release approval.

1812 now implements seasonal/habitat/time-selected robin, redwing, cicada, cricket, katydid and rare distant coyote recordings; moving-horse gait-linked dirt hoofbeats with renderer-snow damping; and visible militia repair/packing with hammer impacts at actual tool contact. Work uses existing actor hi_town_chicago_militia_unnamed_4_1812, Apr 7–Aug 13 repair and Aug 14 packing. No fall/winter work activity was invented. Snow is a processed dirt-recording proxy, not a dedicated snow recording. Existing 1835 placements and 1904 activation remain unchanged. No new R2 upload or purchase is needed.

## Validation at hold

- 52 focused tests PASS; actual R2 nature/hoof and hosted-library browser fixtures PASS.
- Local gate part 1 PASS 328, part 2 PASS 329, **part 3 PASS 327**. Part 4/preflight NOT RUN. Part 3 finished before shutdown; no local gate/browser remains running.
- Current-head hosted gate 43111188820, moving frames 43111188589, portable humans 43111188845 and mobile stage 13 43111230458 SUCCESS.
- Desktop stage 13 run **43111248377** still in progress at 23:29 UTC. Existing hosted validation may finish independently; HOLD blocks merge even if green. It was not restarted or canceled. Re-read its final status only after owner resumes.
- All 16 non-stage-13 renderer runs on 3df passed. Only one PART13 expected-help-text assertion differs in c5; smoke-scope-reuse.json proves all app bytes and other test sections unchanged. Honest matrix reuse retains actual tested SHAs. Last known matrix 17/18 green; do not claim 18/18.
- Published native data/audio checks passed at 390 Light and 1280 Full across four seasonal views, both tasks, dirt/snow and lifecycle. Drawing held during data/UI preparation and restored for screenshots. This is not physical listening approval or continuously unheld animation proof.
- Both phone close views visually accepted by root and reviewer: hands/hammer/support visible, no gross detachment. Fine finger detail too small to assess. Desktop close visual views are STILL MISSING.
- Prior desktop capture expired after only 20 rendered frames/250 seconds, all outside active primary work; no application errors. Preserve failure logs. Do not infer an app defect or weaken assertions.
- Earlier moving benchmark failure was one flora interval above threshold; cause undetermined. Current-head repeat passed unchanged app and original thresholds. Earlier mobile13 failed only stale Effects text, now corrected.

## Resume sequence — only after explicit owner release

1. Read ticket and PR hold reason first. Fetch current code DEV and branch refs. CLI GitHub credential expired in this session; connected GitHub APIs work. Do not expose/request secrets unnecessarily. Use expected-head/lease protection for remote writes.
2. Preserve code c5 and immutable evidence. No 1904 activation until 1812 release is complete. Current DEV last seen 8a643db9e089a007668b33edcb3852cb2f85e7a9; do not assume it remains current. Integrate concurrent DEV safely and revalidate affected code if changed.
3. Finish TWO missing desktop Full close views only: packing and repair. Keep already accepted phone images. Prepared helper `review/capture-close-work-desktop.mjs` is syntax checked, NOT RUN. It holds draws during native setup/wait for ordinary work, then calls original renderer and captures real canvas pixels plus pose atomically. No forced actor/time/phase. Root must inspect resulting images. Any corridor warning needs actual image review.
4. Run local part 4/preflight sequentially, with no heavy local browser in parallel. `PATH=/workspace/audio-tooling/node_modules/.bin:$PATH CHECK_JOBS=4 CHECK_PART=4/4 ./tools/preflight.sh` from app. Save stdout and `/tmp/preflight-check.log`; inspect final aggregate, not intentional self-test FAIL lines.
5. Read final desktop13 and current required CI. Regenerate `release-smoke-coverage.json` from actual run statuses using `release-smoke-status.py` plus source comparison helper. If code changes, reassess reuse; do not label prior runs as current-head runs.
6. Commit final evidence to chicago-evidence, update PR with actual final results, remove hold ONLY under owner release, mark ready, merge DEV only when all required checks/visual review pass. Do not promote MAIN.
7. Wait for DEV deployment including squash merge/fold SHA, then run `verify-live-delivery.mjs` against exact deployed version. It checks both layouts, icon/help, native sound gesture, arrival music silence and town music, delivery hashes and work controller. Do not require lazy work prop loaded at entrance. Do not claim physical listening.

## Local recovery locations and commands

- App: `/workspace/chicago/chicago/4d` (Node 22 via `/workspace/audio-tooling/node_modules/.bin`). Playwright in `/workspace/audio-tooling/node_modules`, Chromium `/usr/bin/chromium`.
- Master recovery directory `/workspace/audio-1812`; full chronological `STATE.txt` preserved in archive.
- Immutable current publication `/workspace/audio-1812/published-props`: build 3df73785f, reviewed source tree f22922b9f32b90f800c018045603cc05b752ad68. Never mutate it. If environment is lost, republish an isolated checkout of 3df and verify hashes; record the new publication identity honestly.
- Older original publication `/workspace/audio-1812/published`, reviewed tree f7a4e1d433f3c824912c09da23944a295f20f115. `prop-path-equivalence.json` records subsequent asset path correction; runtime/prop bytes unchanged.
- Desktop command: `C4D_PUBLISHED_ROOT=/workspace/audio-1812/published-props EXPECTED_BUILD_SHA=3df73785f REVIEWED_SOURCE_TREE=f22922b9f32b90f800c018045603cc05b752ad68 CLOSE_WORK_REPORT_DIR=/workspace/audio-1812/review/desktop-resumed-results /workspace/audio-tooling/node_modules/.bin/node /workspace/audio-1812/review/capture-close-work-desktop.mjs` (redirect a new log; do not overwrite failures).
- Phone PNGs in `review/close-work-observed-ui-results`; partial manual receipt `review/close-work-visual-review.json`.
- Live command after deploy: `EXPECTED_DEV_VERSION=<exact deployed revision> /workspace/audio-tooling/node_modules/.bin/node /workspace/audio-1812/verify-live-delivery.mjs`.
- Helpers contain absolute workspace paths; restore the archive under `/workspace/audio-1812`, and source-scope helper under `/workspace/audio-next/verify_smoke_scope_reuse.py`, or deliberately update paths and record changes.
- Evidence is stored remotely via GitHub connector blob/tree/commit/expected-ref APIs because CLI auth expired. Local evidence clone HEAD is stale; NEVER push it over remote main. Fetch fresh remote parent/tree and normal-fast-forward with expected_sha.

## Subsequent 1904 work (read-only preparation)

`1904-next-options.txt` and `1904-recording-shortlist.txt` preserve recommendations and six verified recording/license pages. Priority: appropriate asphalt/macadam brougham hoof recording; sparse urban ecology around actual elms/lawns; visible Annie Allman entrance sweeping before broom sounds. Do not reuse dirt audio under a hard-paving label or copy prairie/coyote ecology blindly. Source recordings are not auditioned/downloaded/activated; full source decodes exceed current memory limits, so prepare bounded excerpts later. No 1904 ticket or PR was opened for these notes.
