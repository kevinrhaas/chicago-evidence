# Pushed pre-fire research recovery branch, no PR yet

The reviewed candidate is now a concrete recovery commit: `bf6e3e14059f5876fdd9a0de3c63774e50e20990`, on `steward/t3654-prefire-research-followup`, parent `933e1f9e00f378436bb2c9396b634696dc6f3138`, tree `56c2d45eeacfb39c0aee71af709c5faa65864bce`. The remote branch was verified read-only at archive time. It has not been merged into the frozen baseline and has no PR at this capture.

Exactly the 13 released public validation/handoff files are preserved here, totaling 477,827 bytes, plus archive-authored manifest, Git binding and this README. Source and mirror payloads are not duplicated: all 22 committed source-file hashes equal the reviewed candidate already archived under `../prefire-site-candidate/`; all 16 corresponding committed mirror files match those source bytes. `committed-binding.json` records the full 38-path comparison with Git blob IDs and hashes.

The supplied rerun logs record 138 notebook and 51 dossier checks passing, plus target captures and preservation of existing records. The handoff records deterministic builders/publish parity and a clean committed worktree. The four captures come from that worktree mirror, with original capture evidence retained. These are research-site checks; no full 4D gate, 4D model integration or baseline acceptance is inferred.

After baseline PR #2198 merges, create the actual follow-up from then-current dev, cherry-pick this single research commit, and verify conflicts and regenerated mirror parity. The current workflow path filters do not automatically trigger the required 4D source gate for a pre-fire-only PR, so that eventual PR needs an explicit canonical check. The included PR-body text is a draft, not evidence that a PR was created.
