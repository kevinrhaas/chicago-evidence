Use an isolated checkout of kevinrhaas/chicago at parent revision `fc5a52b6cab3eed78e2db5864aa811dff5df2795`. Apply SOURCE06.patch to recover the exact nine reviewed files. This is a source recovery step, not an APP commit, actor opt-in or asset installation.

Obtain only the four near parent GLBs at the exact recipe paths and verify their SHA256, size and Git blob pins. The recipe also records four far baselines; this generator does not produce or install them. The actual study used already cached parent objects, zero network body bytes. Dependency versions are in DEPENDENCIES.json. Keep all outputs in fresh directories outside the application.

The original guarded executions used a120s supervisor and unchanged4GiB available-RAM/512MiB workspace/1GiB temporary-storage floors, with one worker at a time. Use the equivalent resource controls before any reproduction. These commands are provided for reviewed measurement, not automatic production execution.

```sh
cd chicago/4d
node tools/test_human_charles_coat.mjs
node tools/human_charles_coat.mjs \
  data/humans/materials/charles-coat-woven-v1.json \
  "$INPUTS" "$MASTER_CHILDREN" "$PINNED_NODE_MODULES"
for lod in 0 1; do
  name="nelson_charles_1904_coachman.lod${lod}.glb"
  python3 tools/verify_human_charles_coat.py \
    data/humans/materials/charles-coat-woven-v1.json \
    "$INPUTS/assets/humans/$name" "$MASTER_CHILDREN/$name" --lod "$lod"
done
node tools/human_charles_coat_semantics.mjs --master-only \
  data/humans/materials/charles-coat-woven-v1.json \
  "$INPUTS" "$MASTER_CHILDREN" "$PINNED_NODE_MODULES"
node tools/test_human_charles_coat_defaults.mjs \
  "$PINNED_NODE_MODULES" "$MASTER_CHILDREN/nelson_charles_1904_coachman.lod0.glb"
bash tools/human_charles_coat_web.sh \
  data/humans/materials/charles-coat-woven-v1.json \
  "$INPUTS" "$MASTER_CHILDREN" "$WEB_CHILDREN" "$PINNED_NODE_MODULES"
```

Then use official gltf-validator2.0.0-dev.3.10 `validateBytes(new Uint8Array(bytes), {uri: logicalName})` on the two MASTER and two WEB children, requiring zero errors/warnings and no truncation, with no ignored issues or severity overrides. Reject external resources. The actual four results and their hashes are summarized in NATIVE-VALIDATOR-SUMMARY.json.

The byte hashes bind the actual measured outputs, not a promise of byte-identical JPEG/codec output across other platform/dependency builds. Raw canonical WEB remains distinct from any later selected publisher/externalized fixture. Full APP checks, native actor/published renderer, fit, phone budgets and photographic acceptance remain separate.
