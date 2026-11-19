# Exact af + DEV8c targeted publication checks complete

Candidate 539f09beb735e7555745566667140de72c44b796, tree 6b2c34dfa605a475fc9695abcfb2d0c0b019bb76,
published and passed all targeted dependency checks in the isolated worktree.
The nine command receipts (including setup and proof recording) each have
exit 0. They cover the normal publisher, published-source parity, validate--site,
pre-fire mirror parity and two changed JavaScript syntax checks. Four quiet
logs are empty with explicit exit 0 receipts; silence alone is not counted.

Publication parity accounts for 1,625 source-identical files and 6,042 transformed
files under 21 declared rules, zero unmapped. Site validation reports **0 errors,
340 warnings**; no strict-mode pass is claimed. The existing 740 MiB budget and 64 KiB
duplicate threshold are unchanged. Actual 4D output is 7,667 files / 515,614,141 bytes;
the whole isolated working site is 7,942 files / 689,592,349 bytes. This is not an
uploaded deployment artifact or live-site measurement.

All seven changed viewer files match exact 8c source blobs in root and 4D copies.
All 13 added media/provenance files match source/root and are pruned from the 4D
duplicate. ROOT_SERVED points at /pre-fire/ for maps/images/ and media/, with no
exceptions. Exact twenty blob IDs, sizes and SHA256 values were independently
checked during archive creation.

The review owner fully rehashed the original primary 347 fixture against the
saved phone inventory: 7,667 files / 515,543,560 bytes, zero differences. Primary
source/ref/status remained unchanged. Original pending preparation receipts
remain in ../dev8c-publication-preparation/; this completion supersedes only
their pending execution status. The candidate remains local/detached/unpushed
at the recorded completion, and no source/assertion/budget was changed.

This closes the narrow new-DEV publication dependency. Source and renderer
receipts retain their actual original heads/runs. The full eight-part source
gate, moving retry and remote 13–15 are separate; no overall release pass or
DEV merge is claimed. completion.json binds all detailed logs and receipts.
