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

Implementation is pushed at `822f0a9ae94b52c893a00aaf7baf698a3cd1a6b9` on `steward/t3654-1871-city-baseline`, draft [PR #2198](https://github.com/kevinrhaas/chicago/pull/2198) into dev. It includes dev `69d9659ea09bcb8f87f9d9be9c475c657b6f5b8f`; runtime input hash is `sha256:f681e5412b836a8d`. The integration audits preserve all 899 audited 1871/pre-fire/renderer files and the incoming assets/photo proofs.

The earlier 933 source run found one real derived-data failure: both merge parents declared 1,184 liberties, while their combined document contains 1,185. The owning compiler corrected only the count; all 1,185 entries and 908 names remain unchanged. Its equality check and six canonical focused checks pass. The subsequent two-file release-note fold and postcommit entry check also pass. Full publication, published mirror and boot checks pass on clean 822.

Fresh source CI is [44447282208](https://github.com/kevinrhaas/chicago/actions/runs/44447282208), with supporting humans 44447282230 and moving/upload 44447282219. All eight source jobs are created and queued at this checkpoint; no pass is inferred from queueing. The previous source run is retained as failed dated evidence. After all eight old source parts were terminal, its obsolete queued aggregate alone held the new run; a guarded force-cancel of that superseded run returned HTTP202 and released the new jobs. This did not target current checks.

Six published browser groups were dispatched exactly once on 822: desktop13=44447647854, desktop1–8=44447665922, mobile1–12=44447683223, mobile13–15=44447702227, desktop9–12=44447717746 and desktop14–15=44447735937. Together they cover all 15 stages on both viewports. Desktop13 has started the native smoke; the other groups are queued, with zero fresh acceptance credit at this snapshot. Resume by monitoring these IDs, not dispatching duplicates. All six superseded 933 browser groups were ordinarily cancelled while queued; their coverage is zero.

[Evidence checkpoint 4a5ef91](https://github.com/kevinrhaas/chicago-evidence/tree/4a5ef9124200a3d1b726b68529a1e2cc1d2fe606/evidence/t3654-1871-city-2026-11-18) contains 1,229 files and 1,228 verified checksums. Its dated snapshot covers 933 publication/focused checks and dispatches, the separately pushed research follow-up, earlier source results, original failures and licensed research. New 933 failure/cancellation and 822 repair/publication/dispatch receipts are being added in the next bounded backup. No historical result supplies current-head acceptance.

The baseline contains 33,580 generic buildings, 3,627 trees, 22 road crossings, 597 quay bays and five rail corridors. Focused evidence covers both widths/all detail tiers, every rendered bridge both ways, quay approaches, walking/collision, confidence shadows, empty named-structure startup and source cards. It does not establish finished photographic detail, individual parcel accuracy or physical-device performance. Six additional report bridges remain withheld pending date or placement evidence. Mitchell-map registration improves 37.73→18.67m RMS; eight reserved checks improve 49.97→15.62m. Modern targets agree within 2.023m RMS, while actual historical State/Madison retains a 22.57m residual. Bank, parcel and elevation uncertainty remains separate.

The independent research website update is now MERGED into dev as [PR #2206](https://github.com/kevinrhaas/chicago/pull/2206), merge commit `8c605db0571e29ee9da6d8aba5181451d9d84db8`. Its two research commits were applied directly to dev on branch `steward/t3654-prefire-evidence-dev`, head `8c010cfac173a30773df097397d4d24916110e13`. Actual-dev validation passes 138 notebook and 57 dossier assertions, deterministic builds, mirror parity and image/provenance checks. All 47 changed paths are confined to pre-fire source/site; no 4D application input changes. The Carbutt photograph is included with its broad catalogue date and explicit limits. Live branch rules are empty and dev is unprotected; the 4D-only contract does not impose an unrelated full 4D gate on this independently validated website change.

The source and browser jobs for baseline #2198 continue on 822. The research-only dev advance does not retire those 4D results. The user requested session wrap-up before they finish: keep 2198 draft/resumable, resume existing run IDs, verify the complete gates and only then merge the expected head. Local pollers are stopped; GitHub workflows remain active. No background agent or automatic merge is promised. The complete frozen Chamber v2 candidate is backed up at [7fc913d8](https://github.com/kevinrhaas/chicago-evidence/tree/7fc913d8fe38e93202948ed4e9c53f796311175c/evidence/t3654-1871-city-2026-11-18); all three image comparisons remain differs, with camera limitations and unfinished geometry explicit.

Require all eight current source parts plus aggregate and all 30 browser stage/viewport pairs before baseline merge. File the native results on their matching runtime, archive them and update this ticket/PR. Once the current head is fully green, merge that verified baseline without a redundant metadata-only baseline commit; final STATUS/checkpoint/native smoke records can follow in the next checked bookkeeping update. The independent research PR has already merged. Release the owned PR lap, settle this ticket and verify the 1871 development preview. No production dispatch.
