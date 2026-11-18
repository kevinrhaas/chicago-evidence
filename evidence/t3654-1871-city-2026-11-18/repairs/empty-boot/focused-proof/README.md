# T-3654 empty scene boot packing repair

Base:7e99cd8c363baced005d691b3eb1eec086a90202. Candidate changes only tools/pack_boot_sidecars.mjs. This is focused source/CLI proof, not complete source-gate, full-publisher, browser or CI acceptance.

The exact old CLI reproduces the missing boot descriptor on the committed1871 empty structure index. The repaired CLI packs that scene with an empty shared table and no parts, and rehydrates all765 actual1835 records exactly. Summary records SHA256 for767 selected source inputs, each verified against its committed Git blob before copying into the temporary fixture. No geometry or broad assets are needed.

The integrated self-test exercises zero/nonzero records, the50-row part boundary, deterministic repeat publication, preserved positions around missing records and cleanup when a previously nonempty scene becomes empty. Nine negative cases cover a partially missing record, all records missing, missing/wrong boot descriptor, missing/malformed shared table, an unreferenced part, missing required part and corrupted packed record. Reinstating the old writer skip or old checker missing-record skip independently makes this self-test fail. The malformed table refusal matches scene-loader.js's existing Array.isArray requirement.

The large generated fixture directory is deliberately excluded from this handoff. To reproduce in a checkout containing the base commit and matching selected source files, use Node22:

    python3 reproduce.py /path/to/chicago candidate-packer.mjs /path/to/node22 /tmp/empty-boot-reproduction

Create that output directory first. The reproducer records actual exit statuses and checks every expected success/failure. It makes no edits to the supplied checkout. Its temporary generated fixture can be discarded after inspection.
