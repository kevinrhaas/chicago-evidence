Adds named human authoring studies for John Kinzie the elder in1812 and John Jacob Glessner in1904, using their existing evidence grades and date-qualified records. The1812 People directory gains Kinzie's sourced inferred household card. Both opt-in models use reconstructed age-specific bodies and original conjectural clothing, with explicit source-index footwear/body derivations and liberty L419.

The canonical CLI reuses the portable rig, four LODs, sockets, morphs, animation and existing export/normal/sole-contact gates. A fresh output directory keeps study exports separate. The manual workflow also self-tests when its own file changes, retains actual successes/failures, and performs source and published browser inspection. Existing1835 authoring and default fixture/export behavior are preserved.

Validation: independent frozen-source and installed-source reviews,25 source controls, both source-only CLIs, scene/liberty/source-use compilation. Full local preflight PASS:1,018 checks including377 self-tests; exact-commit changelog/ID and published-mirror checks PASS. Actual canonical CI remains pending. First preflight caught stale no-1812-people fixtures and six missing license rows; those were fixed with explicit production-data assertions and an isolated absent-layer negative control, then the complete gate passed. Blender has not run on the improve runner. Garment/body fit, mature skin, anatomical/period clothing detail, photographic quality, world placement and interaction remain open; these are review artifacts and do not close T-1789 or T-2804.

Depends on the transport foundation in PR #1041; this branch starts at its validated f2f607b0b commit. Target is dev.

Ticket: T-1789
Related: T-2804

Validated source commit:2726042ad9ea217687fab5525529bdee21656011.
