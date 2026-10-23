# Generic adults and transport integration audit

Date:2026-10-18. Read-only application/queue audit. User now authorizes generic adult
teamsters/drivers/riders, standing by vehicles/horses and walking streets, with
clothing appropriate to each year and photographic-quality acceptance. A named
Mark Beaubien likeness is not a prerequisite under that instruction. This report
does not depict people, create residents, change queue claims or assert completed
human models. Native depiction and speculative cultural content are outside this
audit's scope.

## What exists and what does not

The portable pipeline is real: T-1786(contract), T-1787(Blender→GLB export), and
T-1788(browser actor) are marked done. Files include:

- `chicago/chicago/4d/docs/HUMAN-ASSET-CONTRACT.md`;
  `data/humans/contract.json`; `data/humans/human_instance.schema.json`.
- `tools/human_fixture_blend.py`, `human_export.py`, `human_export.sh`,
  `human_contract.py`, `human_fixture.mjs`, `human_actor.mjs`.
- `renderers/web/js/humans.js`, plus human actor/fixture inspection HTML tools.
- Four source GLBs under `assets/humans/c4d_fixture.lod0..3.glb` and their four
  exported web counterparts under `assets/humans/web/`.

The eight GLBs are **one fixture at four LODs plus corresponding web derivatives**,
not eight distinct people. `human_fixture_blend.py` explicitly describes “NOBODY,”
a primitive fixture: tapered cylinders, head/eye spheres, foot boxes and light-LOD
mitten hands. Its idle and walk clips are procedural proof motions. They establish
pipeline mechanics, not a photographic adult body, face, hands or period wardrobe.

`data/humans/fixture.measure.json` records measurements dated2026-10-10: LOD0 nearest
full-tier3668 triangles, balanced nearest2012, light nearest468; full-tier all-LOD
web bytes360,408. Timings are SwiftShader software-renderer measurements. They are
fixture evidence, not photoreal human budgets or actual hardware performance.

No dedicated dated clothing/wardrobe/fashion dossier was found in the inspected
`docs/research`, `docs`, source-record names and targeted source-text search.
T-1789 lists intended garment categories but remains open. A source statement
that teamsters used the Western Hotel supports occupation/context; it does not
establish the cut, fabric, color or fit of an individual's clothes.

## Authorization and stale enforcement

Authoritative queue band8C lists T-2672 first. It remains open and unclaimed in the
inspected ticket file. The ticket quotes the owner's2026-10-16 permission to draw
humans once the portable pipeline renders them, and expressly requires obsolete
L1/release restrictions to be updated before figures land in scenes.

The inspected application still contradicts that ruling:

- `AGENTS.md` standing section says no human figures, with repeated L1 language.
- `HUMAN-ASSET-CONTRACT.md` says L1 stands and describes `l1.in_force:true`.
- `renderers/web/js/humans.js` scene loader refuses `shown` while L1 is true and
  separately refuses a review flag with no review record.

User authorization is already present; this is an implementation reconciliation
task, not a reason to ask permission again. T-2672 owns that reconciliation. Preserve
scene-date/provenance honesty and the reasons carried by review metadata while
following its actual current owner ruling. Do not silently weaken unrelated checks.

## Generic adults need an explicit identity path

Current schema requires `person_id`, and defines it as an existing person in
`data/sidecars/<scene>/people.json`. `humans.js` looks up that person before checking
display/L1 and refuses an absent ID. Duplicate checks are keyed by person identity.
An anonymous driver therefore cannot simply be assigned `person_id:generic_driver`
without a deliberate contract/runtime extension.

Implement a distinction between a canonical historical person's instance and a
reconstructed anonymous role instance. The latter needs a stable instance ID,
adult-only assembly, scene/date bounds, source/wardrobe provenance, declared liberty,
role and placement, without minting an invented resident or biography. Selection
can explain “reconstructed teamster/driver,” without opening a fabricated personal
card. Keep canonical named person/card lookup for the existing historical path.
Version the contract and validate both paths; do not bypass the current validator
or use an unrelated person record merely to make a generic actor render.

## Dependency-safe next work

These are recommendations for root coordination, not new ticket IDs or claims.

| Existing ticket / proposed parcel | Current state | Safe next action |
|---|---|---|
| T-2672 depiction-ruling reconciliation | Open; first8C; no bake needed | Claim first after root's code freeze ends. Reconcile prose, machine flags, relevant validator/runtime/release behavior and meaningful checks. |
| T-1789 modular1835 adult library | Open; `needs_bake:true` | Claim on the authorized Blender/bake-capable path. Its acceptance already requires at least3 deliberately different anonymous test residents. Use generic adults as requested; do not wait for Mark. |
| Anonymous role-instance contract | No dedicated owning ticket found | Root should attach to/split an existing relevant human integration task or mint a bounded parcel before implementation; identity is a real blocker independent of model quality. |
| T-1790 reusable clips | Open, blockedT-1789; bake | Proceed after compatible library. Idle/walk/stand form first shared motion set; driver/rider specialized motion belongs withT-2804. |
| T-2673/74/75 Mark likeness/browser/measurement | Open named path | Retain as optional named-person work. Do not substitute generic assets and close likeness acceptance. Explicitly remove their role as mandatory generic-path prerequisite where the new ruling conflicts. |
| T-1792 population/LOD budgets | Open; explicit body says wait untilT-2675 merged | Root must revise the named-first dependency under the current generic-example instruction, or create a separate generic specimen measurement parcel. Do not claim unchangedT-1792 as if its written dependency disappeared. |
| T-2804 portable-human riders/drivers | Open; bake | Already owns anonymous rider+driver fit; avoid duplicate tickets. Written dependencies includeT-2672/1789/1790/1792/2801/2802/2803. Isolated technical fixture fitting may be split/assigned explicitly before production dependencies, but cannot close the whole ticket. |

Useful parallel parcels after root coordination: dated wardrobe evidence sheets;
adult body/head/hand topology and skin/material work; generic-role schema/runtime;
and rigged driver/rider pose studies on the shared skeleton. Keep artifact ownership
separate so the library/contract/exporter are not edited concurrently without review.

## Roles and proof examples

1. One generic adult standing beside a horse/vehicle tests shared scale, feet,
   shadows, clothing drape and hand detail before mounted motion complicates it.
2. One walking adult tests terrain contact, stride speed, foot slide, garment
   deformation and LOD continuity. Existing fixture walk is a starting mechanical
   proof, not finished gait animation.
3. One wagon/carriage driver tests seat/pelvis/feet, rein grips, steering gaze and
   torso response without seat penetration. Reins are actual geometry/attachments,
   not implied by arms held forward.
4. One mounted adult tests saddle/seat, thighs, stirrups, foot support, hands/reins,
   transitions and horse gait synchronization. It must reuse portable-human rig
   and licensed period wardrobe; no isolated new human engine.

All four examples are anonymous reconstructed adults. They demonstrate a role,
not a particular ethnicity, social biography, named worker or specific household's
employee. Keep placement plausible and explicitly reconstructed; generic anonymity
does not make every street/year or costume historically interchangeable.

## Scene/date eligibility

| Scene/date | Wardrobe and source treatment | Release/integration implication |
|---|---|---|
|1812|Requires its own dated adult clothing/footwear/headwear evidence. Later carriage photos cannot attest1812 dress. |Share skeleton/base anatomy where suitable; separate wardrobe/material eligibility. No speculative cultural/camp scenario. |
|1835-07-01|T-1789 explicitly targets1835. Shirt, waistcoat, trousers, work/outer coat and hat are category candidates; actual cut/fabric/fastening needs evidence. |First generic library can serve the existing wagon reconstruction, with liberties. Do not stage August1835 events. |
|Pre-fire through1871|A range, not one costume era. Choose an explicit demonstration year and source bounds. |Do not mark one1835 wardrobe as automatically suitable for1860/1871. Gate each assembled actor's garments by dates. |
|1904-07-01|Late nineteenth-century local photographs are useful appearance leads, but exact fashion/occupation/date and rights must be checked. |A generic teamster's workwear and a carriage driver's formal dress may differ; do not derive either from a rights-pending image or imply a named household's employment. |

Age is adult for these specimens; source files and UI should not imply exact birth
dates or historical biographies. No minors or cultural representation are required
to satisfy the current examples.

## Source, rights and photographic-quality gaps

The reviewed Clarke/Chrimes vehicle image has occupants and useful clothing/pose
context but unresolved rights and exact date. It cannot supply traced human meshes,
copied texture/material atlases or a claimed1835 outfit. Pullman-location photographs
do not identify a carriage's owner, driver or attire inventory. Coachbuilding manuals
support vehicle construction, not a complete human wardrobe/body likeness.

For each selected garment obtain dated pattern/construction or museum-object
evidence and usable rights. Record original textile/color evidence separately from
monochrome reconstruction. Original project-authored bodies/materials may proceed
with declared proportions and anatomy references; asset licenses must allow GLB,
texture and canonical-source redistribution. No copied generator asset may enter
without that check. Missing precise measurements allow bounded reconstruction,
but do not make a primitive figure photographic quality.

Acceptance must include inspected neutral-light front/profile/three-quarter renders
of adult body, face, hands and full clothing, then the actual browser specimen near,
conversation and street distances at desktop/mobile. Compare eligible dated clothing
sources, inspect seams/silhouette, skin/hair/eyes, hands and footwear, test walk and
seated deformation, and record remaining discrepancies. Measure shipped bytes,
materials/draw calls, skinning/animation cost, texture memory and LOD transitions.
Fixture success, an exporter passing, or a distant silhouette is insufficient for
the requested photographic-quality claim.

## Handoff

First actionable queue claim: **T-2672**, then **T-1789** on the proper authoring
runner. Coordinate the generic-instance extension and named-first dependency update
with root. Continue clothing research and isolated pose studies in parallel; route
rider/driver production proof through existingT-2804. No queue, application or claim
changes were made by this audit.
