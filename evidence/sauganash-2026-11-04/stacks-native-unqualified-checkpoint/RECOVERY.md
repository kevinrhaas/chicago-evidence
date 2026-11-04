# T-2383 — Sauganash ridge-end stacks: UNQUALIFIED native checkpoint

**This is durable work-in-progress evidence, not a claim that any gate passed.**
No source qualification, image acceptance or runtime verdict is claimed here. The
long checks (`tools/check.sh --part k/4`, the published both-viewport smoke, the
hosted whole-source `gate`) had NOT been run when this checkpoint was written.

- Repo: `kevinrhaas/chicago`
- Branch: `steward/t2383-sauganash-ridge-end-stacks-20261104`
- Head at checkpoint: `7819ad07cae4dc7ceed1de3db61fd26721ea7e24`
- Base: `dev` at `59ec08a37e269eba6f4fc22a7697453e6f453fe5`
- Lane: `sauganash-stacks-native-20261104`, slice 1/1
- Worker: GitHub Actions, Ubuntu 26.04.1 LTS, official pinned Blender 4.5.3 LTS
  (`generators/blender.pin`, archive sha256 verified `OK` against
  `975c58fcb244273838534bba771e64ad87739216b0f9b39a888531a49a72d845`).
  No cloud-host Blender, no GPU, no hand-authored or hand-edited GLB.

## Authorization actually verified before any write

- `ROOT-GO.json` fetched from `chicago-evidence/main`:
  `authorized: true`, reviewer `root`, feature `7b427d130a2cca6ed82c183c74605b965aee1d4e`
  (this worker's own feature ref), patch digest
  `33d16a51d37e10a2eea2bdcc62a10ca73c906fae7c1c1b90a2a45a5d2741a408`.
- The approved patch was fetched from its immutable raw URL and its sha256
  recomputed locally: `33d16a51d37e10a2eea2bdcc62a10ca73c906fae7c1c1b90a2a45a5d2741a408` — matches.
- Ownership re-read fresh at start: T-2383 `state: open`, `claimed_by: null`,
  `pr: null`; no open PR on `kevinrhaas/chicago` carried T-2383; `ticket.mjs inflight`
  named no T-2383 branch. Claimed normally with `node tools/ticket.mjs claim T-2383`.
  No force, no takeover, no stale-branch deletion.

## Scope actually measured, not asserted

`tools/validate.py --stale` on the clean checkout, before the patch:
**1035 assets match their inputs, 0 stale** (`staleness-before-patch.log`).
(One clone-local FAIL preceded it — three Glessner v4 packaged GLBs were not
materialized in a fresh clone — resolved with the official
`tools/recover_glessner_v4.py --materialize`; those outputs are untracked.)

After applying the approved data patch: **1034 match, 1 stale** —
`sauganash_hotel__frame_1831.glb`, inputs `8ea9c88aeb16` → `53c9902f43ee`
(`staleness-after-patch.log`). Exactly one affected default, as approved. No
other frame_tavern default and neither Tremont variant moved, which is what it
means that no producer, archetype or kit code was touched.

## Native stages actually run (bounded, foreground, regular-file logs)

1. `blender -b -noaudio --factory-startup --python generators/build.py -- --only
   sauganash_hotel --wrote <file>` → exit 0, `1 asset(s) built; manifest updated`.
   The actual wrote list is exactly one line: `sauganash_hotel__frame_1831.glb`
   (`native-stage1-blender-build.log`).
2. `tools/web_derivatives.sh --only sauganash_hotel__frame_1831.glb` → exit 0,
   223592 → 38536 bytes, `recorded 1 master hash(es)`
   (`native-stage2-web-derivatives.log`).
3. `tools/compile_scene.py --all`, then `tools/validate.py --stale` → PASS,
   **1035 match, 0 stale**, and `tools/measure_web_derivatives.py` → exit 0,
   `master lineage (K39): 1035 of 1035` (`staleness-after-bake.log`,
   `web-derivative-measure.log`).

The monolithic `tools/bake.sh` wrapper was deliberately NOT scheduled: it ends
with an unpartitioned `check.sh` and has no skip flag, so it cannot fit the
600 s foreground ceiling.

## Actual output hashes

| file | before | after |
|---|---|---|
| `assets/gltf/sauganash_hotel__frame_1831.glb` | `08b77238df24e848…` | `16335b77d3549966…` |
| `assets/web/sauganash_hotel__frame_1831.glb` | `d595f39254980d91…` | `4afa7cfb8bbffdb5…` |
| manifest `inputs_sha256` | `8ea9c88aeb160651…` | `53c9902f43ee811b…` |

`assets/manifest.web.json` keeps 1035 master rows before and after. One foreign
row, `log_jail_keeper_house__frame_1835.glb`, was re-sorted into alphabetical
position by the official writer; its key and value are unchanged and no foreign
row was dropped or rewritten. The Green Tree's recipe and MASTER binding are
untouched — nothing selected or rebuilt them.

## Image work at the checkpoint

All four Hotel-dependent controlled views were rendered from their own unchanged
cameras BEFORE the change (archived here as `hotel-andreas-1884-BEFORE.jpg`, and
to `/tmp` for the three shop views so no committed record was disturbed) and
again AFTER. `roof-band-before-over-after.png` is the same crop of the hotel's
render, before over after.

Verdicts were set only after directly viewing each refreshed pair beside its
picture. The hotel's own Andreas comparison stays **differs**; the stack station
is recorded `fixed` and the shafts' proportions and heads `open`. The three
Carpenter-shop comparisons retain **matches**, with the shop anchor
`f3e26f650627…` byte-identical before and after.

## Remaining work at the moment of this checkpoint

- `tools/check.sh --part k/4` for k = 1..4 — not yet run.
- `node tools/smoke_budget.mjs --for-diff` and its named legs at 1280×800 and
  390×780 against the published mirror — not yet run.
- The hosted whole-source `gate` check on the final head — not yet requested.
- PR into `dev`; ordinary merge only on green. T-2383 is then released
  **open/partial**, never done, with no photo follow-up ticket filed.
