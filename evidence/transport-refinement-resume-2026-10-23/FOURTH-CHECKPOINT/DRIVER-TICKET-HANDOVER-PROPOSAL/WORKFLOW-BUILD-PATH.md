# Existing canonical seated-driver build path

Inspected `.github/workflows/chicago-4d-humans.yml` in the current app checkout, without edits or dispatch. Its SHA256 is `62048edeed40b6d5fe8c42feec1a031b7b2581a39ec7215ce0a20b170769c847`. The existing workflow supports this build; no workflow change is needed.

## Source and authentication boundary

New T-2804 work remains outside the app. First review and install the four-file canonical source proposal from CHECKPOINT-2 on an owner-visible authoring PR, run required local checks, and push the reviewed branch. The files are Bardwell's pose, resident-driver-bindings.json, human_teamster_blend.py and new human_seated_contact_lod.py. Check exact preimage hashes in CANONICAL-CONTACT-FLOOR-BINDINGS.json. Dispatching current DEV or another ref without these files builds the old driver.

Actual GitHub authorization currently returns HTTP 401; the observed evidence push also could not authenticate. Restore the environment's GitHub authorization through its supported mechanism before pushes or dispatch. No credential probing, identity substitution, retries or dispatch were performed by this inspection. The command below is a template for the root's authorized canonical build after the reviewed source is actually available on GitHub:

```sh
gh workflow run chicago-4d-humans.yml --repo kevinrhaas/chicago --ref 'PUSHED_REVIEWED_AUTHORING_BRANCH' -f build_teamsters=false -f build_seated_driver_study=true
```

Replace the quoted ref with the actual pushed authoring branch and bind the run to its full commit SHA. `build_teamsters=false` is sufficient: the study job condition is `(inputs.build_teamsters || inputs.build_seated_driver_study)`. Both inputs default false. A normal PR or DEV push runs fixture verification only; it does not produce the new seated study. The workflow has `contents: read`, no branch write or production promotion, and per-ref concurrency that cancels an older workflow run on the same ref.

## What the existing workflow actually executes

1. `humans` job (20-minute bound) checks out the chosen source, sets Python 3.11/Node 22, restores the Blender cache, runs `tools/human_export.sh --verify`, and exercises fixture GLBs and HumanActor at desktop/mobile.
2. `teamster-studies` (30-minute bound, `needs: humans`) verifies original prepared bodies byte-for-byte, generates the physical W01 bench variant, and runs the original seated-source and supported-wagon refusal tests. The reviewed profile must retain valid Dufresne/Flynn pose files already present in the app.
3. It builds **all three** named masters: bardwell_otis_1835, dufresne_joseph_1835 and flynn_martin_1835. There is no single-resident selector. For each variant the exact existing builder command is:

```sh
source generators/blender.pin
"$BLENDER_CACHE/$BLENDER_DIR/blender" -b -noaudio --factory-startup --python-exit-code 1 --python tools/human_teamster_blend.py -- --recipe data/humans/recipes/worker_1835.json --variant "$variant" --liberty L418 --output "assets/authored/humans/teamsters/$variant/canonical.blend" --experimental-normal-probes --normal-probe-receipts /tmp/teamster-studies/normal-probes --sit-drive-study data/humans/poses/w01/resident-driver-bindings.json --sit-drive-vehicle renderers/web/transport/wagon-driver/wagon-w01.json
bash tools/human_export.sh --master "assets/authored/humans/teamsters/$variant/canonical.blend"
```

These are copied workflow commands, not commands executed here. `BLENDER_CACHE=/opt/blender-dl`; the actual pin is Blender **4.5.3**, directory blender-4.5.3-linux-x64, tarball SHA256 **975c58fcb244273838534bba771e64ad87739216b0f9b39a888531a49a72d845**. The pinned exporter creates four source LODs and four normal web derivatives with the existing texture caps, JPEG and Meshopt settings. Preserve that path rather than importing the engineering amendments as a newly generated master.

4. The workflow builds same-master parented hierarchy controls, audits animation times/hair, runs Khronos validation, measures exported GLBs, publishes the mirror, captures source and web workwear views, and invokes `human_seated_driver.cjs` plus source/published W01 smoke. The seated observer uses actual web LOD0, three views, two viewports and all three residents, and checks wrong-era/baseline-wagon refusals.

**Its own seated observer explicitly excludes garment/contact/photographic acceptance.** It proves actual clips, supported vehicle binding, actor loading, framing, GL errors and captures. It does not run this lane's all-LOD cloth/bench and full-shoe measurements. After download, bind and rerun those physical measurements on the actual new source/web hashes; do not transfer the engineering results to fresh canonical output. Inspect the actual pictures and measure unchanged GPU/world budgets before town activation.

## Artifact identity and contents

The final `actions/upload-artifact@v4` step runs with `if: always()`, retention **30 days**, and artifact name:

```text
resident-teamster-studies-FULL_GITHUB_SHA
```

Expected contents: canonical .blend files under assets/authored/humans/teamsters/; named source and web *_1835.lod*.glb files; fixture.measure.json; the physical wagon-driver directory; and /tmp/teamster-studies/ with build/export logs, normal probes, raw export/frame evidence, hierarchy controls, animation-time/hair/Khronos reports, source/web captures, and seated-driver/seated-driver.json plus images. Body-preparation logs and prepared JSON are also uploaded. Multiple upload roots mean archive nesting must be inspected rather than assumed flat.

An artifact may exist after a failed job because upload is `always()`. Verify actual event, requested inputs, checkout SHA, both job conclusions and expected files; preserve failed or partial artifacts honestly. Download by the exact successful run and full-SHA artifact name, for example:

```sh
gh run download RUN_ID --repo kevinrhaas/chicago --name 'resident-teamster-studies-FULL_GITHUB_SHA' --dir /workspace/shared/T2804-reviewed-canonical-artifact
```

Intake only reviewed assets after canonical/readback/visual/budget checks; unrelated Dufresne/Flynn outputs are not automatically installed. Ordinary app CI and DEV merge still follow the repository rules. T-2804 remains unfinished for reins/grips, natural seated motion, transitions, vehicle/horse synchronization, mounted rider, and actual scene interaction.
