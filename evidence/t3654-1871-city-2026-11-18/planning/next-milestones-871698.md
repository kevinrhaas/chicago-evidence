# Three bounded follow-on PRs after the 1871 baseline

Read-only handoff from checkpoint `871698ae94659100fcb8894f4967d4b15c62150f`. These are proposed milestones, not filed tickets or completed research/modeling. No application files were changed. Land PR #2198 first; do not add these to its validation cycle.

The existing scene is intentionally only `terrain`, `water`, and `context`, with `structure_ids: []` (`chicago/4d/data/scenes/1871.json`). It has no 1871 actor population or identified-property model. The current queue contains T-3654 for this baseline; existing transport and human tickets own reusable machinery, not researched 1871 placements.

## 1. One named building: the 1865 Chamber of Commerce

**One PR:** replace generic context on this one parcel with the identified building's exterior, entrances, collision and evidence/image card. Keep surrounding blocks as context; omit interiors and exchange crowds. This creates the reusable first-property integration path without trying to rebuild Court House Square at once.

**Existing evidence:**

- `chicago/pre_fire_v1/data/buildings.csv`, `CHI-B1860-022`: southeast Washington/LaSalle corner, 1865 completion, 1871 destruction, 93 × 180 feet, Athens-marble fronts and brick south wall.
- `chicago/pre_fire_v1/data/building_sources.csv` and `sources.csv`: `ANDREAS2_COMMERCE`, Andreas volume II, printed pp. 352–369. Re-read the cited pages before deriving metric geometry; this handoff inspected the dataset, not that original scan.
- `chicago/pre_fire_v1/data/field_notebook_1871.json`: `building-chamber`, directory p. 54.
- `chicago/pre_fire_v1/data/research_1871.json`: `structure-1871-chamber-commerce`, identified 1866–67 Jevne & Almini view `ichi-63073`, linked at <https://greatchicagofire.org/landmarks/chamber-of-commerce/>.

**Prerequisites/acceptance:** acquire and inspect the actual image, resolve asset-use rights, register the 4D source and solve its camera under `data/reference_views/`. The current research card's museum-caption summary is not a completed image gate or an acquired reusable image. Reconcile the footprint against the period map; keep alignment uncertainty separate from building dimensions. Add an explicit context-replacement footprint so the named model does not overlap generic buildings, and admit only this ID to the scene. `generators/city_1871_emit.py` currently excludes generic buildings using plan polygons; preserve unrelated instance identities when adding the replacement mechanism. Complete the existing photo/image gate, card, confidence and walking checks at both widths in this PR.

**Why this candidate:** its identity, phase and recorded dimensions are relatively clear. Palmer House still has a State/Quincy versus State/Monroe image/identity dispute; the enlarged Court House adds a larger phase-and-grounds problem. No CHM image reuse rights are assumed here.

## 2. One utility corner: Chicago Avenue and Pine Street

**One PR:** a researched hydrant and a small, walkable street-furniture patch at the historic corner, with readable evidence cards. A nearby lamp-mounted street-name label can be a declared reconstruction; do not present a citywide practice as an attested fixture at this exact corner. Keep the Water Tower, engine houses, citywide utility placement and fire response outside this PR.

**Existing evidence:** `field_notebook_1871.json` packet `chicago-pine`; records `hydrant-chicago-pine` (new hydrant at the northeast corner, report pp. 79/84, year ending April 1, 1871), `building-water` (directory p. 54) and `lamp-streetnames` (report p. 116). The preserved scans and page metadata are in the same pre-fire package. `chicago/4d/data/sources/chicago_public_works_1871.json` already registers the municipal report with public-domain original-publication rights.

**Prerequisites/acceptance:** use historical Pine/Chicago alignments, not today's widened Michigan Avenue geometry. The report does not give a hydrant casting, paint, setback, lamp lettering or operating state: obtain a period visual reference where possible and label remaining choices reconstructed. Reuse scene-specific instancing, picking, confidence and detail tiers from `renderers/web/js/street-furniture.js`, but do not copy its 1904 lamp/hydrant shapes or gas-mantle assumptions back to 1871. Author dated geometry/parameters and 1871 placements, verify supported ground and clear pedestrian passage, and prove other years unchanged. This is bounded to a corner rather than a utility-network rebuild.

## 3. One person: a directory-backed worker and short exterior routine

**One PR:** the first 1871 person record, evidence card and short walking/standing routine. Candidate: William Alexander the drayman, explicitly distinguished from the waiter with the same name. Presence, appearance, position and action must remain separately graded reconstruction where the source is silent. No vehicle, indoor layout, employer delivery relationship or elaborate daily schedule belongs in this first pilot.

**Existing evidence:** `field_notebook_1871.json` record `worker-alexander-drayman` (Edwards p. 72, scan n63): H. A. Kohn & Bros., residence 212 Fourth Avenue. The separate `worker-alexander-waiter` entry gives Palmer House and 55 Fourth Avenue. Neither supplies race, appearance, a shift, a route or presence on October 8.

**Prerequisites/acceptance:** resolve the historical address and select a clear exterior route; qualify an 1871 wardrobe rather than reusing an older-year person's appearance. Publish scene-specific people and actor data. Reuse portable humans, identity binding and daily motion (`humans.js`, `human-identity.js`, `human-days.js`; completed T-3516/T-3554), but make 1871 admission explicit in `main.js` around the daily-routine allowlist.

**Critical integration dependency:** `main.js` currently builds day-routing obstacles from named-structure footprints; those are empty for 1871. The context layer already exposes `containsBuilding` and `footprintsNear` in `city-context.js` around lines 252–253. Connect actor clearance to that index and the actual walk surfaces before enabling the first routine; test foot contact, collision, selection and confidence at both viewports. Simply adding 1871 to the year allowlist would not prove that actors avoid 33,580 context buildings.

Keep transport as a later milestone: `state-randolph` records nominal horsecar routes but leaves Sunday frequency, track/stop/turn geometry and vehicle appearance unresolved. `transport-scenes.js` currently enables only 1812/1835/1904; its existing 1893-pattern Brougham does not substantiate an 1871 vehicle. Respect existing transport epics T-2791/T-2798 rather than duplicating their machinery work.

## Shared handoff rules

- Each PR has one visible acceptance demonstration, source/date/rights declarations, fresh compiled source-use, appropriate published mobile/desktop verification, then a green dev merge.
- Preserve the exact 8 October 1871 16:00 local-mean-solar-time baseline. Proposed actions are not witnessed events; March bridge counts and nominal timetables are not Sunday traffic observations.
- The 1869 harbor trace still lacks absolute registration; the outer-breakwater chronology separately documents 29 cribs/1,450 feet by spring 1871. Do not spend those unresolved placements in one of these small PRs.
- The existing `rendering_year_audit.md` remains useful for reusable systems, but its historical counts and pre-foundation statements about the missing 1871 scene/epoch are a dated audit, not current runtime state. Use current `data/scenes/1871.json` and T-3654 measurements for the delivered baseline.
