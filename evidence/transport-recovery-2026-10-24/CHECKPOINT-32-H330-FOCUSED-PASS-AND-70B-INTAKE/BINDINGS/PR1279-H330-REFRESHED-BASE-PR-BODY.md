Round the Brougham lamps, repair the planted horse’s eye UVs, add a safe Western Hotel yard viewpoint, and keep release-note text inside the Navigator.

- T-3083: V18 rounds the upper lamp housings and narrows the lower bodies, preserving non-lamp geometry, materials, nodes, contacts, collision proxy and runtime policies. V17 remains archived.
- T-3086: separately versioned d4544c28 reproduces from canonical b479 with the declared eye UV correction. Geometry, rig, weights, animation, materials and all six embedded images are preserved.
- T-3087: adds E−124/N−292/yaw221.19. All 19 viewpoints are dry and outside roofs; the previous 18 and actor placement are unchanged.
- T-3125: three news grids gain a zero-minimum flexible column and long-text wrapping. No font reduction or clipping mask. Exactly one visitor item joins the existing T-3083 changelog anchor.

The original feature commits remain intact. The latest merge incorporates accepted DEV 6ab39e9, including its Glessner and First Presbyterian changes, while preserving the transport files and original ROADMAP bytes. Shared licence, liberties, STATUS and ROADMAP records describe the group. Broader photographic, native/world, gait, tack, team, occupant and riding acceptance remains open with the existing remainder tickets; T-2794/T-2800 stay split.

Current head: 330eadaa68df9ec9b8e09601a1b88c8d5ca52915; tree 757e30973d8e8b13d167e86fe95aeb5f58c6a41d; app subtree 77cd7218e00cf750ad1cb423fc05ddb0376ba560.

Validation:

- Full preflight passed 1,066 steps / 384 self-tests in 659.859s against the refreshed origin/dev 6ab39e9. Actual return code 0; 721 descendants reaped, none remaining. The committed tree exactly equals the validated tree. Canonical liberties/source-use checks also passed.
- Current-head publication, fresh focused news checks at both widths and normal/140% text size, all 15 browser parts at both widths, and fresh ordinary CI must complete before DEV delivery.
- Earlier C4B8 focused checks passed 92 assertions. Its seven complete mobile legs covered parts 1–13, but that run was deliberately retired with outer code 130 and complete cleanup before the changed app was merged. Those results remain historical and are not counted on this head. Interrupted attempts, timeouts and the older 150-minute CI cancellation remain nonpasses.

Draft while current browser qualification and CI complete. No DEV delivery or production promotion is claimed.

Saved evidence: https://github.com/kevinrhaas/chicago-evidence/tree/fef7e68/evidence/transport-recovery-2026-10-24/CHECKPOINT-30-FOCUSED-WRAPPING-PASS-AND-FRESH-MOBILE-PROGRESS
