# Targeted qualification 03

Proposal 02 remains byte-for-byte unchanged: `33b498eb5dda6243046cff6debf629133d7ef7d5447814b8c0e0084fad2208c6`. No fix patch 03 is needed; this receipt qualifies only the named focused controls.

| Check | Result | Seconds |
|---|---|---|
| python3 tools/derive_horse_coats.py --check | PASS | 0.122 |
| node tools/test_horse_appearance.mjs | PASS | 0.592 |
| node tools/test_draft_horse_assets.mjs | PASS | 0.285 |
| node tools/test_driven_assembly.mjs | PASS | 1.449 |

Every command ran separately under SUP120 with the original resource guard, preRAM >=4GiB+512MiB, accepted before/after resources, zero remaining owned children and unchanged source/input hashes. No sole heavy lock was taken.

Final unchanged input population: 50 files, 12,881,402 bytes. Two legacy setup receipts are preserved: the sparse checkout initially lacked one re-export module, then one side-effect string import. Those unchanged dependencies were populated; all existing legacy assertions subsequently passed. No assertion, cap or runtime source was altered to pass.

The new guard executes the real stale-authored-recipe negative control and real Three source/material ownership checks. Its Node parser removes image links only for decoding, checking original payload SHAs separately. It does not compile GLSL, decode/render the original maps or prove scene contact/photographic quality.

Global writer inventory, step isolation, compiled liberties/source-use, full native gate and all-era desktop/phone image/cost qualification remain pending. See REGISTRATION-AND-REGEN-02.md for the required order and commands. ROOT and earlier clothing parcels remain untouched.
