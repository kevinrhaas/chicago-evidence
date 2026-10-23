Hogan's store used the generic cabin front despite Cameron's depiction of one sash, an off-centre doorway and a small gable opening. This first geometry increment rebuilds those features and moves the visible stack through the ridge, using existing parameters. Both master and compressed visitor assets are rebuilt with the pinned toolchain.

The source preserves Cameron/Chicago Historical Society credit and the inventory's date/rights limits. A pictured ruling derives the structure grade while numeric opening/stack choices remain reconstructed and covered by a liberty. The documented footprint, placement and scene-date caveats stay intact; derived signage, goods and the entrance apron follow the revised doorway.

**T-2377 remains open.** The research camera is provisional and its reviewed comparison says `differs`; doorway, gable treatment, proportions, chimney detail and material work remain. This PR closes no image-match acceptance.

[Before/after and remaining differences](https://github.com/kevinrhaas/chicago/blob/steward/t2377-hogan-picture-match/chicago/4d/docs/RESEARCH/hogan-picture-match-T-2377/README.md) · [Recovery checkpoint, screenshots and receipts](https://github.com/kevinrhaas/chicago-tickets/tree/main/evidence/image-match-2026-10-22/hogan-first-rebuild)

Validation:
- Pinned Blender 4.5.3 build and glTF-Transform4.5.0 derivative; current asset/camera/source hashes reviewed.
- Full local preflight passes: 1,049 steps, strict raster readers enabled. Committed-diff changelog and ID checks pass.
- Published 390×780 and 1280×800 app/card checks pass: exact review flags, no unexpected loader/network/page errors, credited picture link and expanded Cameron/Chicago Historical Society citation.
- All 15 renderer-smoke parts at both viewports are running on this head before merge, partitioned as 1–12, 13, 14–15 so the long part has its own runner. CI and those six runs must pass.

| Viewport | Parts 1–12 | Part 13 | Parts 14–15 |
|---|---|---|---|
| mobile | [run](https://github.com/kevinrhaas/chicago/actions/runs/39903318380) | [run](https://github.com/kevinrhaas/chicago/actions/runs/39903329759) | [run](https://github.com/kevinrhaas/chicago/actions/runs/39903339626) |
| desktop | [run](https://github.com/kevinrhaas/chicago/actions/runs/39903350301) | [run](https://github.com/kevinrhaas/chicago/actions/runs/39903360096) | [run](https://github.com/kevinrhaas/chicago/actions/runs/39903370456) |
