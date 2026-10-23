---
id: T-2792
title: Carriages and wagons: evidence register and first master specification
state: done
epic: RENDERING
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: T-2791
opened: 2026-10-18
closed: 2026-10-21
pr: 1174
claimed_by: vehicle evidence completion agent 10/21/2026, 9:57:49 PM CT
blocked_on: null
needs_bake: false
closed_at: 2026-10-22T04:16:26Z
claimed_run: null
claimed_at: 2026-10-22T02:57:51.192Z
decision: null
decision_answer: null
group: T-2792,T-2799
---

## Scope and acceptance

Deliver the first vehicle evidence register and an executable modeling specification, not a new research bureaucracy.

- Inventory existing wagon geometry, data, sources, counts, dimensions, license provenance and placements; distinguish supported mechanics from static appearance. Identify what can be reused without redoing T-0084/T-0087/T-2121.
- Record every actually inspected relevant viewer image with stable ID, date interval, provenance URL, visible features, rights and candidate class. Include the pre-fire coverage result and remaining Prairie coverage. Start from identified J. P. Smith & Co. wagon and Harvey-frontage carriage leads; investigate the LoC Pullman-location high-resolution scan, recording access denial rather than inventing ownership/type.
- Select a first static wagon and passenger-carriage specimen; state evidence tiers and bounded dimensions/materials. Preserve rights-pending photographs as text citations only. Select a cleared construction basis before derived assets begin.
- Write `vehicle-master-spec.md`: components, pivots, axle/steering/shaft/pole/seats, scale/axes, portable JSON interfaces, matched-view acceptance and LOD/performance receipt expected of the next two tickets. Record unresolved source/rights work precisely.
- Provide research findings and a concrete first modeling handoff. A proxy-denied archive is an outstanding prerequisite for that source, not a completed deep-dive.

## Work started

Two independent visual audits and an implementation audit are already saved in the evidence directory. The carriage and horse agents have saved initial master specifications in parallel; source/rights clearance and production validation remain outstanding. External LoC/archive/Glessner access was denied by proxy on the current instance; domain additions are saved in the environment draft for review.

## Shared requirements

Owner request, 2026-10-18: two epics below portable humans; inspect both research viewers and existing wagons; build photographic-quality period models first, then distant movement, riders/drivers, and eventually boarding/riding. Explicitly authorized parallel work. Implementation target is `kevinrhaas/chicago` **dev**; use the existing isolated checkout, no worktree unless requested.

- Keep 1812/1835, pre-fire (through 1871), and Prairie Avenue 1904 eligibility separate. Later images may support a labeled period analogy, never establish earlier Chicago presence. Do not call the Pullman-location carriage Pullman-owned without evidence.
- Resolve every implementation source ID in `data/sources/`; distinguish attested, inferred with reasoning, and bounded reconstruction. Unknown dimensions/color/breed do not block a defensible reconstruction; record bounds and liberties. Never promote a guess to attested.
- Text citation of rights-pending sources is permitted; assets must not be derived from them. Every shipped asset/input carries license provenance. Prefer project-authored or institutionally cleared references and no paid acquisition without owner authorization.
- Photographic quality is an acceptance target, not a status label. Compare actual renders against dated source views at matched cameras, record discrepancies and what is hidden/inferred. Do not close on a placeholder silhouette or unseen screenshot. Keep black-and-white sources distinct from reconstructed color.
- Canonical deliverables follow the existing portable export pipeline: authored masters where supported, glTF/GLB + engine-neutral JSON, metres and explicitly tested axes, licensed materials and near/mid/far LODs. No Blender installation on the improve runner; mark `needs_bake` honestly.
- Preserve existing placed static wagons; route/actor integration is additive. Existing camera horse/wagon paces do not count as a rendered animal/vehicle or a working riding interaction.
- Measure GLB/texture bytes, triangles, draw calls, texture memory and frame cost for the selected desktop/mobile specimen. Reuse materials and population budgets; do not regress the phone memory work above this band.
- Rider/driver work reuses portable humans and follows the owner's current depiction rulings (T-2672); isolated test fixtures can validate attachments before scene release. No invented named likenesses, dialogue or ceremonies.

## Evidence

Read `evidence/period-transport-2026-10-18/carriages.md`, `horses.md`, and `viewer-survey.md`. They distinguish pixel inspection from metadata, record coverage and rights, and explain external archive access blockers. The Prairie visual pass was targeted, not all 944 source records were visually reviewed. Read the master specifications as they are added; they are a first-pass design, not proof of finished models.


## Owner steering and source update —2026-10-21

Primary-source manufacturer/type register now acquired and backed in evidence/parked-vehicles-2026-10-21/HISTORICAL-VEHICLE-REGISTER.md. Specifics: Fort1812 baggagewagons (maker unknown); Dearborn passengerwagon in Kinzie1831 pp297/302 with pairteam; Briggs&Humphrey actualRandolphStreet carriage/sleighshop1835; Studebaker1893 Chicago branch and Brougham/FarmNo4/FancyParcelNo382 plates. Market availability is not localownership or rankedpopularity. Exact source images/rights and modelling limits retained. CurrentW01/C02 not retrospectively branded.

**Released 2026-10-21** (claim of root parallel people vehicles and horses completion 2026-10-22 10/21/2026, 9:56:46 PM CT): Claims audit: reopen stale inactive work; reference and carriage work immediately reassigned individually for independent parallel completion

## Active parallel completion — 2026-10-22 03:04 UTC

Assigned to vehicle evidence completion agent; finish the exact research/specification acceptance with existing inspected-image, rights and manufacturer evidence. Implementation and photographic masters are separate follow-on acceptance. See `WORKPLAN-PEOPLE-TRANSPORT.md` for current owners and dependency order.

## Completed research acceptance — 2026-10-22

All five research/specification clauses have reviewed deliverables in evidence/period-transport-2026-10-18: current geometry/counts/license/placement inventory, fourteen actually inspected relevant image records with precise coverage and rights, bounded W01/1893 Studebaker Brougham first selections, executable vehicle-master specification and concrete model handoff. The original LoC master access failures remain recorded; catalog access succeeds and does not establish ownership. Kinzie Dearborn evidence is explicitly the1831 journey, chaptersXXIII/XXIV pp297/302. Existing W01/C02 remain unbranded. The actual twelve-view V10 carriage comparison now passes, with photographic/world acceptance still open in T2794.

App source records are integrated in staged treec0b314187a80cbcf8cc115ffeec8f400386b827e for PR1174. First fullgate caught the stale derived Kinzie resident export; ordinary regeneration and package check passed, and the second fullgate is running. Mark review only after a successful gate and actual app push. Independent source/asset review found no blocking findings. Current research scope does not close photographic model, motion or occupied interaction tickets.
