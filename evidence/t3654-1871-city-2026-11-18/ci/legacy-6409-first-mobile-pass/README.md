# Fixed browser snapshot: first four mobile stages passed

The snapshot captured at 01:43:29 UTC on 19 November 2026 includes completed run 44435608683, job 135263559336, on exact source `6409dda1222e1284e111ab0efde1c471f3284d60`. The original decoded log and actual GitHub metadata confirm mobile stages 1–4 passed 323 checks: 310 staged checks plus 13 always-on checks, zero failures and zero page errors. The harness reported 9 minutes 38 seconds. These four stage/viewport cells are verified; 26 of the required 30 remain unverified.

The fixed ledger/status has mobile stages 5–8 in progress and the ten other groups queued, with no credit for those pending runs. No later result was awaited or imported. The original first-dispatch snapshot remains under `../legacy-6409-first-batch/`, accurately recording that all groups were queued then. This update changes no earlier snapshot and launches no additional run.

All eight hosted source parts plus aggregate have now passed separately. Full browser coverage and the remaining release requirements still prevent a merge-readiness claim. ROOT application receipts were not updated by this archival task or by the CI snapshot producer; reconcile the actual evidence and existing run IDs before recording or retrying.

The complete source/browser artifact manifest and dependency map are under `../current-6409/full-hosted-source/`. They bind these exact log, metadata, status and ledger bytes; original local paths are execution provenance.
