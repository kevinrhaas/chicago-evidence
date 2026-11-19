# Derived liberty-count repair and preserved failure

The genuine 933 source-part failure exposed an incorrect derived count: `data/liberties.json` declared 1,184 liberties but contained 1,185. Both merge parents had independently increased the earlier count to 1,184; their entries combined correctly while the matching count field stayed unchanged. The defect entered at 7c1c1dda and was still present in 933. It was not a strict-warning issue or a metadata-only failure.

The owning compiler regenerated the file. The only JSON change is `/count: 1184 → 1185`; all 1,185 liberty entries, all 908 names, the source Markdown and the compiler itself remain unchanged. Original before/after hashes, the exact diff, lineage, build log, explicit compiler `--check` receipt and six focused-check receipts are preserved. The owner check exited 0, and all six focused canonical checks passed.

Those checks ran on staged tree `fecca6cc033f66a07c5327e885d04c6ff9e936cc`, which exactly matches repair commit `5f947ddc8613761f8a30b248a2c69b520a9c19ec`. The later checkpoint `822f0a9ae94b52c893a00aaf7baf698a3cd1a6b9` adds only two release-note fold paths. `committed-binding.json` independently verifies that lineage and the count-only JSON difference using committed Git objects. The original staged receipts remain unmodified, including their then-uncommitted state.

This is a narrow data repair, not a complete source/browser gate. The original native failure and exact checkout-tree proof are under `../../ci/superseded-933-source/`; the six old browser cancellations are separate from that assertion failure. New publication and dispatch records bind the successor head and runtime fingerprint without inheriting old acceptance.
