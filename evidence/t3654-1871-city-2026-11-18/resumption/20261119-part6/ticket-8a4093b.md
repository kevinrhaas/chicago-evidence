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

## Validation and recovery checkpoint — 2026-11-18

Implementation and research are pushed on `steward/t3654-1871-city-baseline`, checkpoint `6409dda1222e1284e111ab0efde1c471f3284d60`, draft PR #2198 into dev. `docs/measurements/t-3654-validation-checkpoint.json` revision 10 records completed checks and remaining verification. Integrated dev base: `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`.

Durable evidence: [chicago-evidence:evidence/t3654-1871-city-2026-11-18/](https://github.com/kevinrhaas/chicago-evidence/tree/fc296537a1a6ee2528bdf0bc8062de050b3c4de2/evidence/t3654-1871-city-2026-11-18), commit `fc296537a1a6ee2528bdf0bc8062de050b3c4de2`. The archive contains 649 files with all 648 SHA256 checks passing, including research audits, native browser proofs, source-gate failures and repairs, and resumption instructions.

The recorded `ae259` city snapshot passes both viewports/all three tiers, all 22 bridges in both directions, 597 quay approaches, streets/walks, collision and source/liberty checks with zero errors. Later focused native proof confirms confidence-aware shadows against exact `3f81` runtime bytes. Full `c0c235` publication passes mirror checks and rehydrates 1,119 named records across all scenes. Native 1871 starts with an empty named-structure pack and 33,580 context buildings; Edwards appears by default and actual cards plus all eleven new source details resolve without errors. Narrow probe scopes and software-rendering limits remain explicit.

Local source part 12 on `c0c235` found two issues: rounded bare sums in the harbor trace and seven new checks missing from the measured isolation census. Both are repaired on `871698`: precise summation leaves the trace byte-identical, and actual probes measure all seven checks passing without repository writes. Original failures remain preserved. The prior 871698 tree has successful dated evidence for all 1,379 source assertions, but its hosted run had seven passes and one timeout; no hosted full-gate pass is claimed. Current head 6409 incorporates dev monument/research and changelog changes, preserving all 201 audited 1871/pre-fire/runtime paths. Full current publication, published mirror and boot-packing checks pass; runtime input hash is `sha256:be6a6a9e5ee3c3e2`. New source gate [44421763389](https://github.com/kevinrhaas/chicago/actions/runs/44421763389) has its first verified pass, part 6/8 (175 checks in 393.937 seconds); the remaining parts and supporting workflows are pending. Fresh browser stages 1–15 on mobile and desktop remain undispatched until complete current source assertion coverage. Full hosted source and browser gates are required before merge; old-tree evidence supplies no current coverage.

The owner-requested modern-intersection cross-check remains in `t-3654-today-registration-audit.json`: nine City-centreline/OSM targets agree within 2.023 m RMS, and fourteen inherited targets match exactly. This is coordinate-frame consistency, not historical rendered accuracy. The generated State/Madison crossing retains its 22.57 m map-fit residual; older-year Today shifts are not copied into 1871. Overall map fitting improves from 37.73 m to 18.67 m RMS, with eight reserved checks at 15.62 m RMS.
