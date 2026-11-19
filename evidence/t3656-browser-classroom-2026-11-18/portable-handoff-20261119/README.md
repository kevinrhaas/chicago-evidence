# Portable continuation checkpoint

**Latest incremental update:** [coordinator handoff after mobile5](mobile5-update/HANDOFF.md).
[Normal stage5](../renderer/347-mobile5-complete/README.md) now passed30/0
with exit0 and all final guards in354.664seconds. Stage6 is active and excluded.
The earlier handoff below remains an immutable dated snapshot.

Read [the coordinator handoff](HANDOFF.md) first. It records the requested
continuation and delegated release ownership. All status is dated: PR2197 at
`af466d1638fda72a468ecd3ac22456844b870c1b` and PR2205 at
`fc51c9efcd56f863a3493d67101ae2e1ec60e75e` are draft/open; no DEV merge is
claimed. User authorization remains merge to DEV when the required gates are
green. Release_checks accepted the remaining PR2197 gate/expected-head merge
work; the local mobile supervisor continues and must not be duplicated.

Durable recovery map:

- [Normal completed347 mobile2–4](../renderer/347-mobile2-4-complete/README.md):267/0 with ordinary exit0 receipts. The saved partial manifest/events show5 running; no active5 log copied.
- [Separately recovered347 mobile1](../renderer/347-mobile1-recovered/README.md):95/0 with accepted exact kernel exit0. Original supervisor SIGKILL and unavailable normal end receipt remain explicit.
- [Frozen347 and folded af provenance](../combined-347-c23-20261119/README.md): only the upstream entry removal/changelog fold differs. Local publication remains347.
- [Desktop1–12 scope proof](../../t3657-t3658-hunt-accessibility-2026-11-18/desktop-early-stage-scope-347/README.md): retains original DDC1–4/6–12 and bounded b501 stage5 attribution; fresh13–15 still required.
- [b501 stage5 reuse receipt](../../t3657-t3658-hunt-accessibility-2026-11-18/current-dev-keyboard/stage5-reuse.json).
- [Space repair, preserved first failure and successful focused probes](../../t3657-t3658-hunt-accessibility-2026-11-18/stage14-space-focus-b327/README.md).
- [T3663 source checkpoint and unrun browser preparation](../../t3663-gossip-investigation-2026-11-19/README.md), now [draft PR2205](https://github.com/kevinrhaas/chicago/pull/2205).

`ci-status-20261119-0304.json` is a dated snapshot, not an evergreen queue
claim. `live-recovery-snapshot.json` retains historical fields; the handoff and
named current fields take precedence. Completed local phone2–4 and this handoff
are now archived even though the original coordinator text describes this
archive as upcoming. The source worktrees, live publication, running supervisor,
application refs and tickets were not changed during this checkpoint.

Primary tickets clone: `/workspace/chicago/chicago/4d/tickets`, branch`work`.
T3656/T3657/T3658 remain review in groupT3656,T3657,T3658 with PR2197; use the
supported ticket workflow and preserve remote external commits. The isolated
follow-up validation tickets clone is separate and must not be used for these
updates. No final PR validation text or merge action was authored by this archive.
