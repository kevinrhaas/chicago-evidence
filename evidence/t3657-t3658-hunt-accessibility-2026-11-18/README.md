# T-3657 / T-3658 — photo hunt and accessibility checkpoint

Recovery evidence for [draft PR 2199](https://github.com/kevinrhaas/chicago/pull/2199),
targeting dev and dependent on classroom tools PR 2197.
**Focused native-town checks now pass at both sizes, alongside the earlier logic,
fixture, and photo-audit evidence. Full source and published renderer release
gates remain separate and are not declared green here.**
No production promotion, new server, account service, or paid API is involved.

- Latest combined checkpoint: `6ee1a689077839dd9923edbc80269dd2cbaccfb6`.
- Latest completed focused native runtime: `5674d33df9f39048e5c3ced87c33e3855afdf3ee`.
- Current dev: `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`; old-dev evidence retains its 169404 provenance.
- Original combined fixture commit: `f1f2229f0879c4f1771b07fd9409f994cfc6a986`.
- Branch: `steward/t3657-t3658-hunt-accessibility`.
- Base: `03ecd9678e15988abe44c50e27c2bd9fec569530` from the classroom branch.
- Draft PR 2199 depends on PR 2197; neither is merged. After PR 2197 merges, use
  the normalized follow-up plan plus the keyboard repair below against the actual dev squash/fold.
  The original base is an audit boundary, not permission to merge raw old history.
  Preserve upstream changelog verbatim and omit duplicate parent repairs.
- `combined/manifest.json` identifies the base, combined commit, scope, and exact
  file hashes. Every listed hash was independently checked against that immutable
  Git commit while creating this archive. `repair-checkpoint.json` identifies
  the subsequent repair commits and exact changed-file hashes at e579424f0.
  `integration-checkpoint.json` records current branch/dev heads, verified base
  ancestry, and completed focused combined native-town work without extending
  earlier fixture results to another runtime.

## New keyboard ownership checkpoint and pushed normalized QA

`keyboard-ownership/` preserves the before-repair reproduction, actual native
browser harness, two screenshots, complete report, isolation measurement and
self-test. **20 checks passed: 10 at 390×780 and 10 at 1280×800**, with zero page
errors, HTTP errors or blocked external requests. The test used actual Navigator,
desktop capture, PointerLockControls and movement code, without a world or WebGL.
It covers native rail/app-button keys, standalone controls, native dialog
ownership, Popup E versus text entry, hand/automatic Inspect, world focus,
releasing held movement on Tab, and already-prevented keys. Pointer-lock requests
were counted at the canvas method; mouse capture was not granted. This is not
full-town, physical-device, screen-reader or complete accessibility certification.

The report tested **3131c798648f4ea244009c4bc66162826565b2e9**, with only an
uncommitted four-line isolation metadata row. The pushed backup is
**597a7c392f7300eeafd069b2afe245c44c1bb7cf**, branch
`backup/t3658-keyboard-ownership`. All seven reported runtime hashes match both
commits and the new normalized QA below. The exact harness hash is verified.
`verification.json` records the committed zero-write measurement row and tool
SHA `d8f2163a1b9f38ebcaf83f68ff1660cf6485bd731b89f7e2e58707c9b853b21d`.
The saved measurement and self-test passed. The coordinator reported the full
audit PASS, but no nonempty saved full-audit receipt was available; the unrelated
empty rail audit file is excluded and no audit was rerun by the archivist.

Normalized QA **ddc78606998ea8aee589941c6ab6cae76a80440a** is now independently
verified pushed to `qa/t3657-t3658-current-dev-keyboard`. Its tree is
**fa70a0164ccbef670529470937b170677c5a99b0**, parent **b1f5074**, current dev
**c676aa2f**. `current-dev-keyboard/` preserves the original Git-object preparation
receipt and patches; `recovery.json` separately verifies the later push, exact
parent/tree, all 46 upstream changed blobs, source hashes and retained policy
and harness blobs. No full renderer had been dispatched for this candidate at
the coordinator checkpoint. Full combined gates remain pending; PR 2199's real
head is still 6ee and neither PR is merged. The eventual first-PR squash/fold
must be checked again and shipped dev changelog preserved.
The review-authored `current-dev-keyboard/stage5-reuse.json` permits only the
original b501 stage-5 measured 1835 geometry/policy evidence to carry forward;
its API-driven checks and unchanged indexed assets do not exercise keyboard
ownership or establish a fresh ddc runtime pass.

Historical **b501 QA desktop 13 passed 157/0 in 27m47s**, including completed
suite, zero page errors and vendor checks; its raw log is
`parent-pin-validation/desktop13-pass.log`. This is old-dev, pre-keyboard evidence,
not validation of ddc's keyboard or c676's changed changelog/source inputs.
The frozen primary 5034/ae4 desktop 13 retry also completed 157/0, separately in
the classroom folder. Primary b1 is now published and local mobile work is in
progress; remote mobile 44422910837 was cancelled wholly queued. No active local
mobile logs were copied. Primary source, moving/upload and changed desktop
13–15 checks remain required. The following sections retain earlier checkpoint
context and source attribution.

## Earlier dev provenance and remaining validation

Actual remote primary **b1f507400cb743a3985cb1d50de1ebd085bd4f63** combines 5034
with current dev c676, with tree **858aa04a6f34329f71efbbe0c472ad5902fea23b**.
The normalized follow-up prediction is tree
**d8df5af979b82a6206f71d68bf52fa67f3dca99f**. `integration-c676/` preserves the
Git-object proof and byte-identical normalized 24-file follow-up patch; the
superseded old-dev plan/proof is under its `historical-old-dev/` subfolder.
Every one of the 46 upstream changed blobs was independently checked as exact
in actual primary and predicted follow-up. The configured direct changelog merge
driver produces an unsafe tree that unstamps an already shipped entry; do not
use that tree or replay raw old history. Verify the actual future dev squash/fold
again and preserve upstream changelog bytes.

`integration-c676/t3657-t3658-rebase-c676-plan.md` is the final readable plan and
behavioral dependency review. It supports retained desktop 1–12 and mobile 1:
none opens the 24 changed source-detail edge files; stage 3's changed hidden
monument paragraph does not affect its asserted 1835 subsets/counts/layout; all
96 rows have the identical complete projection consumed by stage 12's handout.
Those tests do not validate the changed paragraph or revised 50-stop route. Fresh
merged-input 13–15 and all eight source parts remain required. The listed run
IDs record dispatch, not successful results.

PR 2199's real head remains 6ee and still depends on PR 2197; neither is merged.
The completed local primary retry remains scoped to 5034/ae4, separate from
b1's required source 44422645793, moving/upload 44422645797 and desktop 13–15
run 44422884843. Remote mobile 44422910837 was cancelled wholly queued; local
b1 mobile validation is in progress. No latest aggregate gate pass is inferred from
the historical receipts. Ticket checkpoint 85ea6b1 predates this integration.

The b501 QA desktop 5 job now passed **30 checks in 13m32s**, including all three
budget tiers, suite completion, zero errors and vendor checks. Its unmodified
log is `parent-pin-validation/desktop5-pass.log`; the stage applies to its
recorded 1835 geometry, while changelog/source-sensitive stage 13 requires the
latest merged input checks. The old 400ac QA candidates were cancelled wholly
queued and have no test coverage.

## Current preflight and recovery scope

`preflight-part1of16/` preserves the completed bounded preflight at 4a2ee67d,
exit 0: source **partition 1 of 16 passed 89 checks**, including 26 self-tests,
plus changelog and ticket-ID metadata checks. Its manifest records clean source,
dev/base head 169404c9f, exact command, and independently verified log hashes.
This is only one partition; the other 15 remain required. The standard wrapper
success banner is broader than the explicitly partitioned command. No browser
or renderer check ran in this preflight.

The earlier preflight checkpoint used primary 5034a724d; follow-up remains 6ee1a6890. The primary-only stage 13
smoke pin correction has no application change and is not yet incorporated here.
Full required gates are still running, and the primary local
desktop stage 5 budget retry was incomplete at 595 seconds, with no complete
stand/tier sweep or final PASS. The classroom evidence records that log separately.
Primary source 44412406486 and moving/upload 44412406478 remain required.
Its newly completed remote desktop stages, corrected mobile 13 pass, and corrected
desktop 13 timeout are recorded in the classroom folder. The next desktop retry
has no archived result.
Consult both PRs for current checks before merging; keep the existing rebase
boundary and discard duplicate first-PR repairs only after they are upstream.

## Pushed parent-pin QA backup

`parent-pin-validation/provenance.json` preserves the clean local validation
combination at **b501bfcbc9a9ecb38c7bed76efe35a48165b061b**: follow-up 6ee1a6890
plus the primary 5034 stage-13 pin repair. Its root/app tree hashes, unchanged
renderer/assets/data/generator subtrees, and byte-identical repair patch were
independently verified. The original record correctly says no push, browser,
publisher, full source gate or CI had run when that local validation was made;
that historical record is unchanged.

The later backup branch **qa/t3657-t3658-parent-pin** is now pushed and its remote
head was independently checked. `parent-pin-validation/recovery.json` records
that later state and the queued conditional desktop 5/13 runs **44415899803** and
**44415925432**. This backup is not the eventual rebased/folded dev tree and does
not change PR 2199's real head 6ee1a6890. Its nine focused policy tests and syntax
checks do not establish a complete release pass.

On real follow-up 6ee, source partitions 6 and 7 passed, while the wholly queued
moving/upload run was paused until rebase. Primary remains 5034; its source and
moving checks remain required. Primary remaining mobile stages 2–12,14–15 are
queued in 44418522036. Neither PR is merged. Preserve the existing rebase boundary
and use the actual dev head after PR 2197 merges.

## Navigator rail keyboard repair

`rail-keyboard/` preserves the report, four screenshots, reproduction harness,
fixture HTML/script, source verification, and review. All **36 checks passed**:
390×780 and 1280×800, each with normal and reduced motion. The fixture uses the
real Navigator/Rail code and Navigator markup/CSS, with small app bodies replacing
world-dependent contents. Native Tab, Shift+Tab, arrows, Home/End, Enter, Escape
and N exercise Home → Move and year chip → Jump, a surviving visible rail Tab
stop, truthful selection state, manual activation, close/reopen, disappearing
conditional tabs and unregistering an app. There are zero page/HTTP errors,
forbidden requests or world canvases.

The report's tested commit is **15ebfe4ce2ba26ec30ee4cef850ba655301675fe**.
The repair is integrated into PR 2199 at **6ee1a689077839dd9923edbc80269dd2cbaccfb6**;
all four recorded source hashes were independently matched to both immutable
commits in `rail-keyboard/integration-provenance.json`. This establishes the
fixture's exact tested code, not whole-branch identity or new native-town coverage.
The earlier missing bundled-browser launch failed before a page opened; its
separate failure JSON/log remain preserved. The passing run used installed
Chromium. No physical-device, assistive-technology or whole-app accessibility
certification is claimed.

## Combined checks

`logs/t3657-t3658-new-pure-tests.log` records the photo-hunt and viewport logic
tests passing. `logs/t3657-t3658-combined-focused.log` records the accompanying
focused regression/string/changelog checks. These are not a complete source gate.

`combined/hunt/report.json` and its browser log cover both 390×780 and 1280×800:

- Real Home/hunt modules and compiled catalogue; lazy loading of one image.
- No reveal or travel before a guess; live position, distance score, guarded visit,
  and the real source date descriptions.
- Preserved round order/score after reload, five-photo completion, image cleanup,
  failure/retry, clipboard fallback, and no horizontal overflow.
- Visible corrupt/blocked-storage handling with in-memory play still possible.

The hunt fixture substitutes tiny image bytes and does not load a town. That fixture alone does
not establish native-world camera safety or travel. The newer native checks below
exercise the live world; the separate photo audit reads the real images.

`combined/accessibility/report.json` and its browser log cover both widths:
picture-modal keyboard cycling, background isolation, focus return, image cleanup,
and zero page errors. The phone fixture additionally exercises native browser
pinch/pan, orientation, and independent two-thumb controls while magnified. Its
recorded scale reaches approximately 1.968, with the canvas retained at 390×780.
It uses the actual Navigator markup/CSS and touch/modal modules and the production
resize function body, with a small WebGL canvas. It is not full-town, physical
device, or complete WCAG conformance validation.

## Completed native-town checks on 5674d33

`native-final/` contains the final publisher and runtime manifests, reproduction
harness, visual review, complete reports/logs, captured metadata and screenshots.
The official publisher exited 0 on the clean combined revision
`5674d33df9f39048e5c3ced87c33e3855afdf3ee`. Its missing `bc` affected only the
printed MB footer; actual output byte counts were measured separately.
All **27 listed JS/CSS hashes** were independently matched against that immutable
Git commit. The other four runtime hashes identify generated entry/data files;
they are not claimed to be authored Git blobs.

The final actual 1904-town runs passed **11 phone checks at 390×780 and 10 desktop
checks at 1280×800**. They fetched the five real hosted photographs, compared
image hashes with the photo audit, completed all guesses and source/date reveals,
checked all five live camera safety decisions, made one permitted visit through
the production `Instantly` travel mode, used the native Inspect photo modal,
and preserved the challenge day, answer, score and order after shared-link reload.
The phone also exercised native pinch and pan without reducing the drawing buffer.
All five revealed photographs announced “Photograph loaded.” at both sizes.

Both runs captured a real normal frame with the production shutter, retained
all **27 canonical citations** in capture metadata, and saved the bounded local
photo and note in the notebook. The notebook uses its existing bounded source-row
format. Its photo strings were 32,451 and 56,027 characters. The 9,307-character
source caption required 17 phone and 18 desktop text measurements, taking about
7.3ms in the delegated `measureText` calls; the complete captures took 3.34s and
7.62s including the actual frame and PNG encoding. These are functional receipts,
not sustained-rendering or hardware performance benchmarks.

Both reports record zero page errors, HTTP errors, non-cancelled request failures,
and horizontal overflow. They separately retain 42 phone and 45 desktop
`ERR_ABORTED` cancellations from the live app, navigation and teardown. This is
not a claim that every request completed. The hunt owned at most one image at a
time; an explicit visit also opens the existing Inspect gallery, which owns its
own images. Each run used one page/world and two sequential boots, with continuous
software-GPU drawing paused between interactions. This does not certify every
walking route, physical-device performance, or whole-app accessibility compliance.

### Preserved stale-status defect

`native-before-status-fix/` preserves the e23ea1f manifests, original harness,
reports/logs and representative round-4 screenshots. Its automated flow assertions
passed, but they did not yet check completion status: the loaded and revealed
photograph still displayed “Loading this photograph…”. The archived desktop
screenshot visibly demonstrates that defect. Those original passing labels are
not final visual acceptance. Commit 5674 repairs the status and the new native
harness asserts it for every round and restored answer.

`status-fixture/` retains the smaller actual Home/catalogue view fixture and
immutable test source. At both sizes it covers guessed, skipped, retried and
reloaded answered images, polite loaded status, and no second guess. It uses
substituted fixture image bytes without a town. The native reruns above provide
separate evidence with real images. The old preservation manifest lists the full
local snapshot; only representative old images are copied here to avoid storing
all superseded screenshots twice.

## Original isolated fixtures

`original-fixtures/` preserves the original reports and provenance manifests:

- Hunt: commit `45f822b6e9baaa95cf4fc5823be4149cb87fe797`.
- Accessibility: commit `8c291d0d8174f09278bcdf2dbf0c03d4128b10c6`, based on
  `cbf3408e032eb6341df9d52bfbb289810035f412`.

Their corresponding final browser transcripts are in `logs/`. Original hunt and
accessibility screenshots were byte-for-byte identical to the combined fixture
screenshots, so images are retained only once under `combined/`. Original and
combined reports retain their distinct provenance; none is called a full-town run.

## Five real photo audit

`photo-audit/` contains five fetched JPEG thumbnails, HTTP/MIME/byte/hash receipts,
canonical catalogue records, existing rights records, app display records, and
the recorded visual review. All five thumbnail requests returned HTTP 200 with
`image/jpeg`; the archived bytes match their recorded SHA-256 values.

The selected photographs cover Glessner's street frontage and stable end, Kimball,
Wheeler, and Pullman. The visual review found all five visibly photographic and
no blocking subject/view mismatch. Dates and attribution come from the canonical
records, not guesses from appearance. Existing rights metadata is preserved;
this archive does not make a new legal determination or authenticate originals.

The review retains two catalogue differences: Wheeler's structured range starts
in 1884 while its description says circa 1885–1900; Pullman's structured range
starts in 1893 while its description says between 1890 and 1901. Both canonical
forms remain visible rather than silently choosing one. The photographs predate
the 1904 world and do not prove unchanged appearance in 1904. Thumbnail review
does not validate solved cameras against the native town.

## Resource regression evidence and repairs

The earlier repair checkpoint adds the docked-Home repair at `2f42e3c605c7e55f778c837bbcdcf9e9f03e19bb`
and caption/draft repairs at `e579424f02287d38639f643b102688ef0846f000`.
Primary commit45b now includes caption/draft/person/lazy-CSS repairs, and both
new focused actual-town photo/notebook/link runs pass at that exact primary
revision (see the classroom evidence folder). Combined e23ea1f includes those
repairs and the behavioral tour test, all hunt/accessibility fixes, and current
dev. Revision 5674 adds the revealed-image loaded-status repair and completed
new focused native checks. The current combined head includes the authorized Full policy in 308e45207 and
the CI completion allowance in 4a2ee67d. Those came after the native-tested 5674
revision; its recorded evidence stays tied to that runtime. No earlier
fixture or base-runtime gate is automatically a result for changed application files.

`repairs/caption-fit/` preserves the actual Canvas2D measurement harness, original
`moment.js`, and before/after timing report. The input uses a real 9,307-character
Glessner citation line and a 390×780 source canvas. Across three samples, the old
implementation made **9,241 `measureText` calls** and spent **2.0–5.6 seconds**
synchronously copying/fitting the caption; the repaired implementation made
**17 calls** and spent **3.6–4.9 milliseconds**. Source metadata stayed intact,
and every output PNG was 22,567 bytes. The archived original hash matches the
report, and its repaired hash matches the immutable e579424f0 `moment.js`.
This is headless Chromium's real Canvas2D, with no town or WebGL. The synchronous
measurement excludes PNG encoding; concurrent source checks can affect wall
times. It is not a phone, town, or sustained hardware-performance benchmark.

`repairs/t3658-notebook-drafts-before.log` records the stale-draft regression:
restoring a removed entry's ID revived its old unsaved draft instead of the
fresh persisted text. The corresponding `after.log` passes the real People/
notebook component test, including source/identity/save/deduplication/denied
storage, preservation of live drafts on storage changes, and removed-ID pruning
over 120 IDs. These are focused component assertions, not full-town testing.

`repairs/t3657-docked-home-before.log` records the image-resource regression:
quietly selecting Home while the Navigator was docked restored an image. The
`after.log` and `repairs/docked-home-after/` report/screenshots/manifest show the
real nav-rail, Home, hunt modules, and catalogue fixture passing at both widths:
the image stays released while docked and exactly one is restored on reopening.
The fixture uses tiny image bytes and no town. The manifest hashes were checked
against its exact 2f42e3c60 commit, which precedes e579424f0.

## Integrity and remaining work

`artifact-manifest.json` records original paths/timestamps, scope, file size, and
SHA-256 for every copied artifact. This checkpoint adds no source changes and
runs no new browser. Required remaining work includes rebasing after the classroom
merge, accounting for classroom repairs absorbed into that merge, current-head
source checks, native/published integration verification, and
the appropriate renderer release gate. Existing classroom mobile passes are
for its unchanged runtime and do not automatically cover this follow-up runtime.
