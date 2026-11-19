---
id: T-3654
title: Build the 1871 citywide context baseline with varied buildings, streets and bridges
state: review
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-11-18
closed: null
pr: 2198
claimed_by: continuing the same 1871 integration 11/18/2026, 11:06:18 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: 2026-11-18T17:06:19.857Z
decision: null
decision_answer: null
---

Build the 1871 citywide context baseline with varied buildings, streets and bridges.

## Owner request

2026-11-18: “Go ahead and lay the foundations to start working through 1871 and then built it out entirely perfectly photographic cinematic quality.” Scope clarified: “build the entire city as a context city to start with general buildings with basic textures that look ok but all the buildings in the city have variation and are correct in form and style for the business or residential area of the city, built the entire city map with a baseline city.” Also: “And of course the streets and walks etc, bridges other structure.”

## Acceptance

A visitor can enter an explicit pre-fire 1871 scene and see a citywide baseline across the documented/reconstructed municipal extent, with varied period commercial, residential and industrial building forms, streets, walks, river/lake edges, bridges and supporting infrastructure. Ordinary building placement and unmeasured fabric are visibly identified as reconstructed context; no later-year terrain, named houses or people silently leak into the scene. Context geometry is generated reproducibly as glTF plus JSON from a sourced plan, with district variation and detail levels that support street-level and citywide cameras. Source/date/rights limitations are exposed on the scene or context card. Cinematic camera views show the actual rendered city. Validate both desktop and mobile, full project checks, published mirror, and rendering/performance checks appropriate to the change.

This acceptance is the explicitly requested citywide context baseline, not a claim that every historical parcel or facade has been identified, or that the finished photographic-quality city is complete. The baseline is the foundation into which researched named structures and higher-detail materials can be substituted.

## Scope

1871 scene/epoch selection, context generation, plan/source records, portable building and infrastructure assets, city exploration/cinematic views, and a link from the pre-fire research viewer if needed. Preserve existing 1812, 1835 and 1904 behavior. No production dispatch.


## Delivery instructions

The owner requests checkpoint commits and pushes, periodic PR merges into `dev`, and explicitly authorizes “Merge to dev when green.” This integrated baseline is PR #2198. Subsequent 1871 detail work should use smaller coherent milestones so verified progress lands regularly. Production promotion remains owner-dispatched.

## Validation and recovery checkpoint — 2026-11-19

Implementation is pushed at `933e1f9e00f378436bb2c9396b634696dc6f3138` on `steward/t3654-1871-city-baseline`, draft [PR #2198](https://github.com/kevinrhaas/chicago/pull/2198) into dev. It includes dev `c23d8a9e85bf37de9c2eb2dce9118cb709edf0da`; runtime input hash is `sha256:a4155e8aed968b10`. Both integration audits preserve all 899 audited 1871/pre-fire/renderer files and incoming assets/photo proofs. Committed checkpoint revision 11 and STATUS record the pre-publication snapshot; the dated results below are newer.

Canonical focused freshness, derived-record, source-use, unique-ID and changelog checks pass: 1,126 assets match inputs, zero stale assets or validator errors, with 338 existing warnings. Full publication, published-mirror and boot checks now also pass on clean 933. Fresh source CI is [44444393454](https://github.com/kevinrhaas/chicago/actions/runs/44444393454), with supporting humans44444393304 and moving/upload44444393308. These were queued at this checkpoint; no success is inferred from queueing.

Six published browser groups were dispatched exactly once on 933, covering all 15 stages on both viewports: desktop13=44444724593, desktop1–8=44444739587, mobile1–12=44444759609, mobile13–15=44444773514, desktop9–12=44444794793, desktop14–15=44444815188. All were queued at dispatch, with zero fresh acceptance credit. Resume by monitoring these IDs, not dispatching duplicates. Full hosted source 8/8 plus aggregate and all 30 current browser cells must pass before merge.

[Evidence checkpoint 0d1f5e5](https://github.com/kevinrhaas/chicago-evidence/tree/0d1f5e53589613a86907a1f0082ce3aa6f5bf45d/evidence/t3654-1871-city-2026-11-18) contains 1,146 files and 1,145 verified checksums. It preserves the earlier 6409 full source/supporting passes, mobile1–12's468 checks, nine unfinished-run cancellations after upstream runtime changes, research, screenshots, original failures, and the first Chamber prototype (both image comparisons still `differs`). Those dated results supply no 933 gate credit. New 933 receipts/dispatch records are being archived separately.

The baseline contains 33,580 generic buildings, 3,627 trees, 22 road crossings, 597 quay bays and five rail corridors. Focused evidence covers both widths/all detail tiers, every rendered bridge both ways, quay approaches, walking/collision, confidence shadows, empty named-structure startup and source cards. It does not establish finished photographic detail, individual parcel accuracy or physical-device performance. Six additional report bridges remain withheld pending date or placement evidence.

Mitchell-map registration improves 37.73→18.67m RMS; eight reserved checks improve 49.97→15.62m. Modern Today/Google Maps and OSM controls agree within 2.023m RMS, while actual historical State/Madison retains a 22.57m residual. These are distinct measurements; older-year display shifts are not copied into 1871, and bank/parcel/elevation uncertainty remains separate.

Finish the existing runs, record actual results on the matching runtime, update validation records and evidence, and require final-head source success. Then merge to dev, release the owned PR lap, settle this ticket and verify the 1871 development preview. The next reviewed research-site expansion is being prepared as a separate commit/PR; Chamber refinement remains a later city milestone. No production dispatch.
