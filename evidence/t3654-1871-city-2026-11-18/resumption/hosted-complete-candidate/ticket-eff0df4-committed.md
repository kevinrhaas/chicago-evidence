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

Implementation and research are pushed on `steward/t3654-1871-city-baseline`, commit `6409dda1222e1284e111ab0efde1c471f3284d60`, draft [PR #2198](https://github.com/kevinrhaas/chicago/pull/2198) into dev. Integrated dev base: `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`. Runtime input hash: `sha256:be6a6a9e5ee3c3e2`. The committed checkpoint revision 10 is an earlier dated snapshot; this ticket and the versioned evidence carry the later verification state.

Durable evidence: [chicago-evidence checkpoint `9a103dc1`](https://github.com/kevinrhaas/chicago-evidence/tree/9a103dc1080917fd35c278c911564a4863558c42/evidence/t3654-1871-city-2026-11-18), with 955 files and all 954 SHA256 checks passing. It preserves the complete exact-tree source assertion proof, root review, all twelve browser dispatch IDs, screenshots/reproductions, prior failures and licensed research packets. Its first-dispatch snapshot accurately records the then-pending hosted jobs; the later full hosted success is recorded below and will join the next archive.

All 1,379 source declarations have verified successful execution on the exact current tree. All eight hosted source parts and the aggregate also pass in [run 44421763389](https://github.com/kevinrhaas/chicago/actions/runs/44421763389); the full workflow is successful. Portable-human and moving-frame/upload workflows are fully green. Full publication, mirror and boot packing pass; freshness verifies all 1,126 assets against their inputs.

All twelve published browser groups were dispatched exactly once on `6409dda`, covering stages 1–15 on mobile and desktop. The immutable `t3654-6409-first-batch-result.json` records every run ID and tested commit. Queued/running jobs have no pass credit. Resume by checking those existing runs, not by dispatching duplicates. Full hosted source success and all current browser results are required before merge.

Focused evidence covers the complete generic-city snapshot at both widths/all three detail levels, all 22 bridges in both directions, 597 quay approaches, walking/collision, context cards and confidence; later focused proofs cover shadows, empty named-structure startup and actual source cards. Exact inputs, software-rendering limits and earlier failures remain in the archive. The baseline does not claim finished photographic detail, individually identified parcels or a complete population. Six other municipal-report bridges remain withheld pending date or placement evidence.

The modern-intersection audit remains in `t-3654-today-registration-audit.json`: nine City-centreline/OSM targets agree within 2.023 m RMS, and fourteen inherited targets match exactly. This checks the coordinate frame. The generated State/Madison crossing retains its 22.57 m historical map-fit residual; older-year display shifts are not copied into 1871. Overall map fitting improves from 37.73 m to 18.67 m RMS, with eight reserved checks at 15.62 m RMS.

Finish by recording actual browser results through the existing recorder at a clean boundary, updating the checkpoint/STATUS and evidence link, committing/pushing final records, and requiring the final-head gate. Then merge into dev, release the owned PR lap, settle this ticket and verify the 1871 development preview. Production promotion remains owner-dispatched. Subsequent detail should land in smaller coherent PRs; the original Chamber of Commerce exterior and sourced street-life candidates have bounded research handoffs, not completed models.
