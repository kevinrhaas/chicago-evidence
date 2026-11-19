# Next bounded classroom unit: Gossip evidence comparison

Read-only preparation, 18 November 2026. No repository/ticket edits, browser runs, gate runs, publishing or git mutations performed. This filename reserves no ticket ID; local T-3659 already belongs to the Otis rowhouse.

## Recommendation

After PRs #2197/#2199 finish their release work, add an optional, initially collapsed **“Make your case”** comparison to the existing *Gossip or Printed Notice?* completion card. Question: **“What can you responsibly carry back about the land sale and the proposed Chicago bank?”** Show the two newspaper readings, let the student select the evidence supporting their answer, write a claim and identify an uncertainty, compare against an authored reading guide, and explicitly save the result to the field notebook.

This is a useful first slice of #8, not the whole proposed mystery system. The existing four-stop route, choices and endings already supply the investigative walk. It needs no new world, service, narrative engine, record schema, additional tour or invented witnesses. Do not manufacture the suggested three people to question: existing evidence explicitly says no named person is met. Keep the ordinary optional reflection available; the specific comparison should not replace it or enlarge the compact completion card until opened.

## Exact historical footing

Canonical authored record: `data/jaunts/gossip-or-notice.json`; the four `gossip-or-notice-{grades-3-5,grades-9-10,grades-11-12,adults}.json` tellings have `version_of: gossip-or-notice` and the same evidence IDs. Their compiled equivalents are in `data/sidecars/1835/jaunts/`.

| Evidence | Source and issue | What the pilot may say |
| --- | --- | --- |
| `land-sale`, canonical line 394 | `chicago_democrat_1833_1835`; extracted `chicago_democrat_1835_07_01#c020`; 1 July 1835, Vol. II No. 11, p. 3 col. 2, transcription lines 2566–2592 | The paper could not ascertain the receipts and was only “led to believe.” Preserve `between Fi[v]e and […]red Thousand Dollars` and the statement that the second figure is lost. It does not establish an exact total. |
| `bank-branch`, line 422 | `chicago_american_1835`; extracted `chicago_american_1835_06_27#c001`; 27 June 1835, Vol. I No. 4, p. 1 col. 5, transcription line 108 | It reprints the Sangamon Journal: directors decided on a Chicago branch; its officers were not made known. This is evidence of what the paper reported, not proof an operating Chicago bank existed. |
| `bank-springfield`, line 431 | Same American item | The brick building is **read as Springfield’s**. This is `inferred`, with the record’s reasoning, not an attested Chicago address. |
| `gossip`, line 477 | No source; `L-jaunt-gossip-or-notice` | The million-dollar and imminent-bank rumors, asker, errand and responses are liberties. No historical person is assigned the rumors. |

Authority for the corrected reading: `docs/JAUNTS-INITIAL-LIBRARY.md:570`, `docs/LIBERTIES.md:21227`, T-2031 (PR #355), and T-2040 (PR #362). **Do not pull the extraction’s normalized land-sale amount into the UI:** it still supplies `[Six Hund]red` and `amount_normalized: between five and six hundred thousand dollars`, expressly rejected by T-2031. Do not turn the American’s supplied `squa[re, near]` into an unqualified quotation.

Both source records in `data/sources/` are `public_domain`, **`asset_use: text_only`**, and have empty public URLs. Their text rights do not authorize page images. The bounded pilot should display the existing jaunt evidence text verbatim as **“Our reading of the newspaper transcription”**, with date/page/column and transcription uncertainty; do not label these summaries full documents, page scans, or invented source links. The primary Democrat text exists at `chicago/reference/newspapers/Transcriptions/Chicago_Democrat_1833-11_to_1835-08/Chicago_Democrat_1835-07-01_Vol2_No11_Transcription.txt`; the American text is `data/research/newspapers/text/chicago_american_1835_06_27.txt`. `corpus.json` resolves those artifact roles. Nothing needs to fetch either full corpus into the browser.

## Existing APIs are enough

- `renderers/web/js/jaunt-understanding.js:24` already models eligibility, committed visited stops, evidence IDs and resolved citations; `checkBand` supplies prompt banding. The new comparison model can use `(jaunt.version_of || jaunt.id) === 'gossip-or-notice'`, require `the-democrat` and `the-american` committed, and resolve exactly the three evidence IDs above from the **current compiled telling**. Do not repurpose the generic three-question sampler; it does not select these particular claims reliably.
- `renderers/web/js/jaunt-preview.js:135–190` owns session-scoped drafts and mounts optional work on completion. Add one separate draft/model/view beside the existing check, dropped on dismissal/replay/new session and retained through same-session menu repaint.
- `renderers/web/js/field-notebook.js:15–27,58–73` already accepts `kind: 'note'`, title, year, place, text, excerpt and sources. Save the student’s claim/selected evidence/uncertainty in `text`; preserve the cited reading, source IDs, locators and inference reasoning in `excerpt`; use existing citation text for source titles. Existing limits are 6,000 note characters, 12,000 excerpt characters and 500 characters per source title. Bound inputs before save, so provenance is never silently truncated.
- `renderers/web/js/field-notebook-view.js:18,95–120` already renders and exports text, evidence and citations, including citations without links. No notebook schema migration or new entry kind is necessary.

Likely authored files: new `renderers/web/js/jaunt-investigation.js` (pure model/draft/notebook adapter), `jaunt-investigation-view.js`, `strings/investigation.js`, a small `css/jaunt-investigation.css`, and the preview hook. Add focused `tools/test_jaunt_investigation.mjs`/view checks, hook the existing source gate, and update `docs/CLASSROOM-FEATURES.md`, `docs/STATUS.md`, and one ticket-owned changelog entry. Existing historical JSON/sidecars can remain untouched.

## Acceptance for that PR

1. Only eligible completed Gossip tellings expose the collapsed comparison. Interrupted, incomplete, unrelated and uncited sessions do not. All five tellings resolve the intended three claims; prompts suit the selected band.
2. The lost amount stays lost, Springfield stays inferred, rumors remain liberties, and sources retain page/column and transcription context. “Documented” means the paper reports it; no scoring claims that documentation makes an assertion true. Review is explanatory, retryable and ungraded.
3. Draft edits survive same-session remount. Replay/dismiss/new session starts clean. Nothing persists before explicit Save. Save success, full/damaged/unavailable storage and repeated-save handling are visible; failed writes retain the draft and earlier notebook entries.
4. Actual keyboard traversal at 390×780 and 1280×800 reaches summary, evidence selectors, fields, review, revise and save with visible focus and labelled controls; status changes are announced. Browser magnification/200% text remains readable, scrollable and free of horizontal clipping. Optional work never traps the user or forces movement.
5. A saved claim is readable in Notebook, downloaded HTML and browser print/PDF: selected evidence, both source identities, locators, uncertainty and inference reasoning survive; student HTML is escaped; no broken/fabricated source links or extra live-world frame.
6. Run focused model/view/export checks, existing reflection/notebook regressions, then the repository’s required source/preflight and published phone+desktop renderer checks once the renderer owner releases CPU. No validation is claimed by this preparation.

## Separate accessibility lead, not yet browser-reproduced

Static inspection of `/workspace/chicago-hunt/chicago/4d` found keyboard ownership worth a focused reproduction: `renderers/web/js/main.js:5198–5207` captures Arrow keys and requests pointer lock even from Navigator rail buttons; its guard excludes typing, the jaunt panel and picture viewer, but not Navigator. `controls/pointerlock.js:87–112` ignores neither `defaultPrevented` nor focused button ownership and intercepts Space for inspect/fly. Its `holding` callback at `main.js:5163` only recognizes the popup. `nav-rail.js:351–362` handles arrows later in bubbling, after the capture request. This can interfere with keyboard menus and native Space activation; code inspection alone is not a browser result. If reproduced by the current accessibility owner, it fits a small #10 continuation. It does not require widening the evidence-comparison feature.
