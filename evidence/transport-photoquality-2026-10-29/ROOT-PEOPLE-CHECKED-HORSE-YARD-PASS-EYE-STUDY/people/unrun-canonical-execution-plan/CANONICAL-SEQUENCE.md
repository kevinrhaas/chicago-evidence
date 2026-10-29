# T-1789 canonical generation and ingestion — prepared 29 October 2026

Status: **UNRUN**. The GitHub API remains proxy-denied in this session. Current PR number, ordinary CI, workflow run IDs, attempts, artifact IDs/digests, producer manifest hashes, canonical delivery commits and still images are unknown. No command in this packet has been dispatched. The user already authorized this generation and safe feature writer; execution resumes when the configured API/artifact network policy permits it.

The exact checked source is `a3971c9a638e03216945fc52ce57d7453596187e`, TREE `e873ea8531ab1a8f8bb74434976ace6234c3d6e6`, APP `8906d01e088f79614fb8020a119ec20e6aa6cf49`, normally pushed on `steward/t1789-people-photoquality-20261026` in `kevinrhaas/chicago`. Required-reader preflight passed 1105 steps/395 self-tests in 918.203s (600s target missed), actual four new-HEAD checks passed, and fresh checked-HEAD publication/mirror/year packs passed. The closed ignored mirror was hash-verified and reclaimed; source and Git objects remain intact.

Read the scripts before execution. They are command templates, syntax-checked only. They add no application tools, gate exceptions or alternative writer. Generation/ingestion uses the existing reviewed Actions workflow and helper, with its native assertions unchanged. The scripts use normal configured credentials, with no auth installation, proxy workaround, force push, production publish or automatic merge.

## Fixed sources and outputs

- Workflow: `.github/workflows/chicago-4d-humans.yml` at the owned feature branch. Delivery requires actual definition SHA = actual source SHA, canonical repository, `workflow_dispatch`, one family, no seated study, and unchanged remote source at each writer boundary.
- Actual inputs: `build_dress_study`, `build_teamsters`, `build_seated_driver_study`, `deliver_generated_assets`, `source_ref`. Defaults remain artifact-only. Female uses `source_ref=a3971c9a638e03216945fc52ce57d7453596187e`; male **must use empty `source_ref`** because the first study-request guard rejects nonempty values for a non-dress request. Male still binds actual definition/source through `GITHUB_SHA`.
- Blender is pinned to **4.5.3**, archive SHA256 `975c58fcb244273838534bba771e64ad87739216b0f9b39a888531a49a72d845`, on Ubuntu24.04 GitHub runners. No Blender installation or generation on this local runner.
- Female: one `assets/authored/humans/dress/flynn_mary_1835_dress_study/canonical.blend`, four raw + four web GLBs, two native inspection reports, eight validator reports and actual source binding. Native fixed bundle has **20 files + delivery-manifest.json**.
- Male: three masters under `assets/authored/humans/teamsters/{bardwell_otis_1835,dufresne_joseph_1835,flynn_martin_1835}/canonical.blend`, 12 raw + 12 web GLBs, two inspection reports, 24 validator reports and seven Blender-still files. Native fixed bundle has **60 files + delivery-manifest.json**.
- Completed library: **four canonical masters and 32 canonical raw/web LOD GLBs**. Current checkout has16 human GLBs (eight fixture + eight old Otis). Combined native all-asset census should become **24 after female, 40 after male**; rebuilt Otis replaces its eight existing files. There are eight fixture files in addition to the32 library files.
- Exactly three real native Blender PNGs: `bardwell_otis_1835-assembly-threequarter.png`, `dufresne_joseph_1835-assembly-threequarter.png`, `flynn_martin_1835-assembly-threequarter.png`. Cycles CPU,640×640,24samples,two threads; source masters/geometry/UVs/rig/poses are hashed before/after. These assembly proofs establish no photographic acceptance.

## 1. Establish the actual PR and the exact initial source

After the configured policy is fixed, query once; do not retry the present unchanged403 denial. Ordinary Git alone cannot dispatch Actions. Preserve raw API results outside the app.

```bash
source /workspace/.cloud-setup/transport-activate.sh
export PEOPLE_REPO=/tmp/chicago-transport-resume-20261029
export PEOPLE_PLAN=/workspace/.cloud-setup/logs/transport-recovery/T1789-CANONICAL-EXECUTION-PLAN-20261029
gh pr list --repo kevinrhaas/chicago --state open --base dev \
  --head steward/t1789-people-photoquality-20261026 \
  --json number,url,isDraft,headRefOid,statusCheckRollup > "$PEOPLE_PLAN/ACTUAL-PRS.json"
```

Use the real returned PR. If none exists, root can create the already-authorized owner-visible draft with the prepared truthful body, then record its actual number and CI:

```bash
gh pr create --repo kevinrhaas/chicago --draft --base dev \
  --head steward/t1789-people-photoquality-20261026 \
  --title 'T-1789: modular resident wardrobe and guarded canonical delivery' \
  --body-file "$PEOPLE_PLAN/PR-BODY.md"
```

Do not merge, synchronize DEV, edit recipes/helpers/workflow or let another writer advance this feature branch during the female→male sequence. Unrelated H/W branches may continue independently. The native male guard compares **all** paths since the female source, not just its17 explicitly hashed authoring files; any non-female-delivery change fails. Real full history is enabled for optional male mode. A normal empty same-tree followup is compatible with this guard.

## 2. Female generation and optional ingestion from the checked source

```bash
export PEOPLE_EVIDENCE=/workspace/.cloud-setup/logs/transport-recovery/T1789-ACTUAL-FEMALE-DISPATCH-20261029
bash "$PEOPLE_PLAN/dispatch-family.sh" dress a3971c9a638e03216945fc52ce57d7453596187e
```

The script verifies clean exact source/owned branch/remote, native source binding and absent prior female delivery before dispatching. It records the request timestamp and actual run candidates. Identify the actual run by workflow, event, exact head SHA and creation time at/after that timestamp. A missing or ambiguous immediate listing is not permission to dispatch again. Read that run directly once known. Record **actual** RUN_ID and RUN_ATTEMPT; no placeholders become receipts.

The workflow runs `humans` prerequisite, `dress-study` producer, then `deliver-canonical-family`. Native stages include pinned-fixture reproduction, cleared-body/default preparation, real female master/export, same-new-master hierarchy control, animation/hair/container gates, both source and published LOD/browser/contact inspections, exact-ID bundle download, fresh **all-asset** measurements, rights/provenance, complete required-reader preflight, staged-tree seal and normal feature-only bot push. Other family is skipped intentionally. The helper refuses incomplete/partial artifacts, unsafe paths/links/GLB URIs, stale metadata, a changed branch or inadequate scratch capacity. Retain all failure artifacts; do not promote a partial run.

After that actual run completes successfully:

```bash
# Set FEMALE_RUN_ID from the actual API response, not this document.
: "${FEMALE_RUN_ID:?actual female run id required}"
bash "$PEOPLE_PLAN/collect-run.sh" dress a3971c9a638e03216945fc52ce57d7453596187e \
  "$FEMALE_RUN_ID" /workspace/.cloud-setup/logs/transport-recovery/T1789-ACTUAL-FEMALE-COLLECT-20261029
```

Collection requires completed success for the exact source/definition workflow and native jobs. It resolves unique unexpired artifact IDs from the actual run/attempt, then downloads each archive **by that ID**, retaining official metadata and raw logs. Names are `human-delivery-dress-RUN-ATTEMPT`, `human-delivery-closure-RUN-ATTEMPT` and `resident-dress-study-SOURCE`. The manifestSHA is obtained from the actual producer manifest and cross-checked against `GATED-TREE.json`'s trusted job-output binding; it is never supplied by guessing.

Read the closure archive's unique `ACTUAL-PUSH.json` to obtain the real bot HEAD (archive subdirectory names are not assumed). Fetch **that exact SHA** with normal Git, leaving checkout/index unchanged, then run the offline reviewer:

```bash
export FEMALE_COLLECT=/workspace/.cloud-setup/logs/transport-recovery/T1789-ACTUAL-FEMALE-COLLECT-20261029
FEMALE_BOT_SHA=$(python3 - "$FEMALE_COLLECT/closure.zip" <<'PY'
import json,sys,zipfile
from pathlib import PurePosixPath
with zipfile.ZipFile(sys.argv[1]) as z:
 rows=[n for n in z.namelist() if PurePosixPath(n).name=='ACTUAL-PUSH.json']
 assert len(rows)==1
 print(json.loads(z.read(rows[0]))['HEAD'])
PY
)
git -C "$PEOPLE_REPO" fetch --no-tags origin "$FEMALE_BOT_SHA"
PYTHONDONTWRITEBYTECODE=1 python3 "$PEOPLE_PLAN/review-archives.py" "$PEOPLE_REPO" "$FEMALE_COLLECT"
```

The reviewer checks official ZIP SHA256, exact run/attempt/artifact identity, manifest binding/full members/bytes, native gate-log SHA and PASS footers, exact bot parent and gated tree, fixed allowed paths, unchanged authoring files, all delivered bytes against Git blob identities, appended canonical receipt and native all-asset24-file measurement verdicts. It executes/extracts no archived code and writes only `REVIEW.json` outside the app. Root must also read actual failures/warnings and inspect the actual female source/published images; a successful mechanical report does not approve the provisional skin/hair, period outfit or likeness.

## 3. Ordinary-auth same-tree female followup and actual CI

`GITHUB_TOKEN` bot pushes do **not** trigger ordinary PR checks. Do not label CI green from the delivery gate. After reviewing the actual closure and native output, fast-forward the clean owned checkout to the real bot HEAD, then make only an empty normal-auth followup:

```bash
git -C "$PEOPLE_REPO" merge --ff-only "$FEMALE_BOT_SHA"
bash "$PEOPLE_PLAN/same-tree-followup.sh" "$FEMALE_COLLECT"
```

That script requires exact reviewed bot HEAD/TREE, clean checkout and unchanged remote; uses `git commit --allow-empty`; proves identical parent content/TREE; runs actual changelog-entry, ID-collision, folded-format and explicit shipped-history checks against checkedW9e14; then performs normal non-force push and verifies exact remote/clean status. Capture the actual ordinary PR CI on the resulting `SAME-TREE-FOLLOWUP-SHA.txt`. Ensure the real PR `headRefOid` equals it, required jobs pass and no relevant check is missing. Existing native same-tree gate evidence carries forward; no authored content has changed. Do not edit to fix unrelated DEV changes between families.

## 4. Male generation, three real stills and ingestion

Only after complete female delivery, root review, same-tree followup and actual CI observation:

```bash
MALE_SOURCE_SHA=$(cat "$FEMALE_COLLECT/SAME-TREE-FOLLOWUP-SHA.txt")
export PEOPLE_EVIDENCE=/workspace/.cloud-setup/logs/transport-recovery/T1789-ACTUAL-MALE-DISPATCH-20261029
bash "$PEOPLE_PLAN/dispatch-family.sh" teamsters "$MALE_SOURCE_SHA"
```

This locally calls the existing read-only `require_female_delivery` guard before dispatch. Actions repeats it using actual context and real full ancestry: female source hashes match current source, only its fixed delivery paths differ, prior female delivery is complete and all member bytes still match. Male has `source_ref=''`, `build_teamsters=true`, dress/seated false and delivery true. Native three masters/24GLBs, validators, all-LOD/source+published/browser/contact/hierarchy inspections and **all three real Blender renders** must finish before bundle creation. The seven still members are manifest + three PNGs + three source-protection receipts. No source/intermediate preview image substitutes for them.

After the actual male run succeeds, collect using its real ID:

```bash
: "${MALE_RUN_ID:?actual male run id required}"
export MALE_COLLECT=/workspace/.cloud-setup/logs/transport-recovery/T1789-ACTUAL-MALE-COLLECT-20261029
bash "$PEOPLE_PLAN/collect-run.sh" teamsters "$MALE_SOURCE_SHA" "$MALE_RUN_ID" "$MALE_COLLECT"
```

Male names: `human-delivery-teamsters-RUN-ATTEMPT`, `human-delivery-closure-RUN-ATTEMPT`, `resident-teamster-studies-SOURCE`, `resident-teamster-blender-stills-SOURCE`. Obtain actual male bot SHA from the unique closure `ACTUAL-PUSH.json`, fetch it, run the same offline reviewer, fast-forward the owned checkout and run `same-tree-followup.sh "$MALE_COLLECT"`. Then require actual ordinary PR CI on its new exact head. The combined all-asset census is now40, with no lost female/fixture asset.

## Acceptance and truthful limits

Accept the canonical mechanical delivery only when the actual artifact IDs and official ZIP digests, producer manifest SHA, source/definition/tree/run/attempt, native GATED-TREE/PREFLIGHT and ACTUAL-PUSH, bot commit parent/tree and remote SHA all agree for each family. Preserve original failures and actual elapsed time/600s status; artifact `always()` uploads can contain partial output and are not acceptance. Current full preflight's1105/395 is source evidence, never a substitute for the post-generation native full gate.

For each family, source and published inspection reports must cover every raw/web LOD at both desktop1280×800 and mobile390×780: female8 runs per mode, male24 per mode; hash binding, every native check true, zero page errors/failed requests and no validator errors/truncation. Combined `fixture.measure.json` must enumerate every current human GLB exactly once, each hash fresh and nonempty native verdict list entirely true. Keep the existing export/skin/animation/sole/contact/hair/hierarchy assertions; warnings retain their authentic native meanings rather than being suppressed.

View all three actual640×640 Blender PNGs. Require manifest status `actual_three_native_Blender_stills_completed`, exact three fixed asset IDs, pinned4.5.3 version, actual run/source/definition and `source_protection_verified=true` on each receipt; same canonical master SHA before/after and identical source body/rig/geometry state. A failed render, hidden/truncated garment, unreadable bonnet/hat or visible body/garment defect is a real review finding. Do not claim photo quality from CPU render completion or a mechanical PASS.

Preserve cleared MakeHuman commit `a8bc2d54ff0ac92e78ff71431b1023eda42bf482`, graphical CC0-1.0 notices, cleared skin/hair/source manifests and original geometry provenance; generator code remains GPL-3.0-or-later. Dimensions, finishing, hats, generic atlas and identities remain reconstructed and evidence bounded. Never import rights=`check_required` geometry/texture, invent a likeness, clear provenance flags or label this historical photographic fidelity. Native metadata appends actual per-asset license/hash/bytes and limits rather than replacing prior notices.

The writer retains the existing standing Otis selection/identity/idle placement, adds no world placements for the other three, updates actual cost/provenance and leaves photographic/production eligibility false. Native asset delivery does **not** close published scene performance, continuous animated fit, seated driver/rider/harness interfaces, period photographic/material acceptance or the wider people tickets. Final PR ready/DEV merge requires ordinary exact-head green checks, fresh published/native scene acceptance relevant to the real assets, root review and current competing-change checks. This packet performs none of those operations.

On any failure or concurrent source advance: keep actual logs/artifacts, stop the sequence and report the exact gate. Do not force push, fabricate a local Actions context, ingest artifact-name matches from another run, weaken an assertion or silently change authoring sources between the female and male generation.
