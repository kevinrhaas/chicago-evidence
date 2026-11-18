# T-3657 / T-3658 — photo hunt and accessibility checkpoint

Recovery evidence for browser-only follow-up work after classroom tools PR 2197.
**This is focused logic, browser-fixture, and photo-audit evidence. Full source,
native-town, and published renderer release gates have not passed for this work.**
No production promotion, new server, account service, or paid API is involved.

- Combined code commit: `f1f2229f0879c4f1771b07fd9409f994cfc6a986`.
- Branch: `steward/t3657-t3658-hunt-accessibility`.
- Base: `03ecd9678e15988abe44c50e27c2bd9fec569530` from the classroom branch.
- No follow-up PR or merge at this checkpoint. After PR 2197 merges, rebase only
  the commits after that base onto the actual dev head, retaining subsequent
  classroom test repairs. Do not replay the classroom implementation commits.
- `combined/manifest.json` identifies the base, combined commit, scope, and exact
  file hashes. Every listed hash was independently checked against that immutable
  Git commit while creating this archive.

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

The hunt fixture substitutes tiny image bytes and does not load a town. It does
not establish that the solved photo camera coordinates or visit locations work
in the live 1904 world. The separate photo audit below reads the real images.

`combined/accessibility/report.json` and its browser log cover both widths:
picture-modal keyboard cycling, background isolation, focus return, image cleanup,
and zero page errors. The phone fixture additionally exercises native browser
pinch/pan, orientation, and independent two-thumb controls while magnified. Its
recorded scale reaches approximately 1.968, with the canvas retained at 390×780.
It uses the actual Navigator markup/CSS and touch/modal modules and the production
resize function body, with a small WebGL canvas. It is not full-town, physical
device, or complete WCAG conformance validation.

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

## Integrity and remaining work

`artifact-manifest.json` records original paths/timestamps, scope, file size, and
SHA-256 for every copied artifact. This checkpoint adds no source changes and
runs no new browser. Required remaining work includes rebasing after the classroom
merge, current-head source checks, native/published integration verification, and
the appropriate renderer release gate. Existing classroom mobile passes are
for its unchanged runtime and do not automatically cover this follow-up runtime.
