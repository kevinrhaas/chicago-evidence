Round the catalogue Brougham lamps, repair the planted horse's eye UVs, add a safe Western Hotel yard viewpoint, and keep release-note text inside the Navigator.

- **T-3083:** V18 rounds the upper lamp housings and narrows the lower bodies. Near/mid exports preserve non-lamp geometry, materials, nodes, contacts, collision proxy and runtime policies. V17 history remains archived.
- **T-3086:** separately versioned `d4544c28` reproduces from canonical `b479`, changing the declared eye UVs, bounds and derivative notice. Geometry, rig, weights, animation, materials and all six embedded images are preserved.
- **T-3087:** adds the yard camera at E-124/N-292/yaw221.19. All 19 viewpoints are dry and outside roofs; the previous 18 and actor placement remain unchanged.
- **T-3125:** three existing news grids now use a zero-minimum flexible column and allow long text to wrap. The retained before-change mobile view showed a 349.859px grid inside a 292px host, visibly clipping text. No font reduction or clipping mask is added. One short visitor item joins the existing T-3083 changelog anchor.

The original three feature commits remain intact; the fourth change also integrates accepted DEV `abb1dd4`. Independent review preserves 52 feature-specific files byte-for-byte and the original anchor's title/kind/three items plus exactly one UI item. Shared licence, liberty, STATUS and ROADMAP records describe the group. Original ROADMAP bytes, historical V17 liberty decision and accepted incoming records/assets are retained. Broader photographic, native/world, gait, tack, team, occupant and riding acceptance remains with the existing remainder tickets; parents T-2794/T-2800 stay split.

Current pushed head: `c4b8ccb3a20234fdebf43e9ea48f00d9855b9aba`, tree `4b2a7066a039936ddcc65d8c1c891fcf25dd7e5f`.

- Fresh combined full preflight passed **1,066 steps / 384 self-tests** in 640.241s. Cleanup reaped 721 owned descendants with none remaining. The committed tree equals the validated input. Canonical liberties check matches all 751 entries.
- Fresh current-head publication and normal CI are in progress. Shared CSS requires all 15 browser parts at both widths; a completely fresh source-bound matrix is required, plus all-row release-note layout checks at normal/140% text size on both widths.
- Earlier be56 mobile1-14 passes remain historical and are not counted on this head. The paused old mobile15 wrapper was retired before browser launch and reaped; it cannot run against changed source. The old desktop14 timeout and old unfiltered 150-minute CI cancellation remain NONPASS. No browser PASS is inferred from partial logs or source inspection.

This PR remains draft until current browser coverage and CI are verified. No DEV delivery or production promotion is claimed.

Evidence: https://github.com/kevinrhaas/chicago-evidence/tree/main/evidence/transport-recovery-2026-10-24/CHECKPOINT-27-CURRENT-DEV-GATE-AND-SAVED-WRAPPING-FIX
