# PR 1649 memory repairs, 3 November 2026

This is a small incremental recovery packet for **uncommitted** TREE `c6d84d690f862e7a90650e2fc4bd584783937169`, based on public app parents `ae762df51dad3bd48e7d5307e0bda3cd0ce05e31` and `073a337e4ed89b362469246c1c5aa927c70975cd`. It records exactly five changed paths since the preceding recovery packet: two planar-occluder paths, tree construction scratch release, and two railway cache paths. No app commit, DEV merge or ticket completion is claimed.

## Required public dependency

Keep `evidence/transport-pr1649-recovery-2026-11-03-1935Z` beside this folder, from chicago-evidence commit `0b7d232b7c232cee0927ecb6a40dcc30d2cc6fe7`. Its manifest SHA256 is `c72e77d39ee4b99b04b19d037334a053a4248815038c76b38b9a646fbe3ec0f1`. This packet intentionally does not duplicate its 16 novel blobs or its Mayer model. Only five additional novel blobs are included. `RECOVERY-RECIPE/recover_tree.py` verifies and uses that public dependency, then reconstructs the exact new Git tree without changing a checkout or index. Its actual isolated roundtrip result is preserved.

## Actual results and their limits

The original 1812 mobile gate failed at 240930717 bytes after the planar change. A subsequent ungated 40-second retainer profile found the tree flood-search scratch arrays. Releasing construction-only scratch produced an actual native 1812 mobile **PASS at 233354145 bytes**, against 235929600, on intermediate TREE `f71556275c06a165c14e46c49415cab35ebc9edb`. That pass is not retargeted to the later railway source in this packet.

The preserved 1904 retainer profile describes earlier TREE `4cbd54078ab4a6dda0c19bbe15ba0a4d90aa7a40`; it completed as an ungated diagnostic and remained above the phone ceiling. It is not a passing gate or a measurement of this final source.

The original combined railway CPU control timed out at its 5-second cap. Its raw negative result remains included. Two explicit control phases subsequently passed their separate original 5-second caps; the complete native default gate still needs to run. No new 1904 measurement or full four-part gate result for this packet's source is claimed. The driver fixture was running and is excluded.

Original commands, source guards, caps, resource and cleanup receipts, exact external patches and ROOT adoption records remain unmodified. The runtime metadata erratum corrects the descriptive cloud revision from 4 to observed revision 9; the baseline bytes and counters were not reset.
