# V3 reviewed fixture-only source bridge

V1 and V2 executables and negative receipts remain immutable. V3 keeps the actual
positive native parts1/2 at their original staged TREE `bf9edb2d…`; it does not
relabel those rows as current-source runs. It requires fresh original parts3/4
at current TREE `e00cce44…`, with the original 600-second caps and native
reader/base/pool flags.

The only source difference is `tools/test_working_driver_1904.mjs`. Its original
three clips remain required at every master/web LOD. Its exact clip-list assertion
now additionally requires `sit_drive_look_v2` only at active LOD0/3. Every byte
outside that replacement is identical, including imports and all seat, palm,
footplate, rig and LOD assertions. Runtime, data, provenance and all assets are
byte-identical between the two trees. The changed native command is declaration
167, assigned to part3, which runs fresh. ROOT also actually reran the original
fixture, syntax and generic gate audit checks successfully at current source.

`INDEPENDENT-FIXTURE-SOURCE-BRIDGE.json` seals the independent one-file review.
Its later generic ordinal labels need the explicit correction in
`GENERIC-ORDINAL-ERRATUM.json`: the ordinary measurement reader omits three
`every_part` prerequisites. `NATIVE-FULL-1156-COMMAND-CATALOG.json` retains all
1,156 declarations, including those prerequisites. The changed fixture167/part3
was before them and remains correct. The global fixture-body scanner is native831
in fresh part3. Reused generic isolation/parser checks read unchanged check.sh,
isolation metadata or controlled fixtures; reader availability and JSON inputs
also remain unchanged. The frozen original audit was not silently rewritten.

The native environment removes `GIT_NO_LAZY_FETCH`, while only metadata Git calls
set it to1. This preserves the earlier repaired sparse-clone fixture's normal
environment without changing assertions or commands.

The positive closure, if actually earned, has status
`FULL_NATIVE_COVERAGE_PASS_WITH_REVIEWED_FIXTURE_ONLY_SOURCE_BRIDGE` and explicitly
records `all_four_same_TREE: false`. Its four ledger rows preserve original
source profiles: oldbf9 for parts1/2, currente00 for fresh parts3/4. The complete
native union must cover 1,156 distinct steps and 401 self-tests. A current PR's
complete CI must still run the exact current committed tree. The preparation
manifest and CLI-help receipt are not a whole-gate PASS.
