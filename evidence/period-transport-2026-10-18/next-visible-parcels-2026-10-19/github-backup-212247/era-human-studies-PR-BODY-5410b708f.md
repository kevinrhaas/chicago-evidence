Adds named human authoring studies for John Kinzie the elder in1812 and John Jacob Glessner in1904. Kinzie gains a sourced inferred household card in the1812 People directory; Glessner keeps his existing attested identity. Appearance, body dimensions and conjectural civilian clothing remain explicitly reconstructed under L419.

The opt-in canonical builder reuses the portable rig, four LODs, sockets, morphs, animation and existing export, custom-normal and sole-contact gates. Its workflow validates fixture bytes and exact source-body reproduction, builds separate study artifacts, then checks actual source and published renders. Existing1835 authoring and default exports are preserved.

The first actual canonical run failed during master authoring/export after fixture and source checks passed. This revision reports the caught Python exception through a bounded CI annotation and fresh failure receipt, then rethrows it. No normal threshold or export assertion is relaxed. The diagnostic revision includes the validated transport/dev merge from PR #1041.

Validation at `5410b708fc177eb794249af0b157a36edb1e34b3`:

- Complete local preflight: 1,020 checks, including 377 deliberate refusal self-tests, PASS. Exact-commit changelog/ID and published-mirror checks PASS.
- 25 source controls, both source-only CLIs and independent installed-source/complete-index preservation audits PASS.
- [Current canonical build](https://github.com/kevinrhaas/chicago/actions/runs/39325858203) is pending. Actual model, garment/body fit, age-appropriate skin, photographic quality and world placement remain unaccepted. These studies do not close T-1789 or T-2804.

Depends on the transport foundation in PR #1041, currently at25b92c950. Target is dev. No Blender ran on the improve runner; new figures, drivers and riders are not enabled in the town.

Ticket: T-1789
Related: T-2804
