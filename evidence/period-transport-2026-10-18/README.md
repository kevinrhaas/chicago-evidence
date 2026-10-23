# Period transport — research and first work, 2026-10-18

Owner request: photographic-quality period carriages/wagons and horses/gear, first modeled from evidence, then animated as distant traffic and riders/drivers, then boardable/ridable. Two bands sit immediately below portable humans by explicit owner instruction. Research and first specifications were produced by parallel agents; no production model or riding behavior is claimed complete.

## Queue

- **T-2791, period carriages and wagons:** grouping epic; T-2792–T-2797 implement evidence/specification, one wagon master, one carriage master, articulated running gear/hitches, distant traffic, and boarding/riding.
- **T-2798, period horses and gear:** grouping epic; T-2799–T-2805 implement evidence/specification, one horse master, draft harness, riding tack, rig/gaits, portable-human rider/driver fitting, and mounting/riding.
- Both use the existing `RENDERING` category and normal parent links. The two grouping records are split, not independently claimable giant tickets. Each model/animation ticket states its bake capability requirement.
- T-2792 and T-2799 are the parallel first work. Initial evidence and specifications are saved; archive retrieval, dated object/construction sources, rights clearance and production validation remain open. No completed ticket is claimed on the basis of a written proposal.

## Evidence and artifacts

| File | What was done |
|---|---|
| [carriages.md](carriages.md) | Existing static wagon audit and inspected photographic vehicle leads, with dates/rights/identity limits. |
| [horses.md](horses.md) | Actual horse/harness image observations and implementation audit: camera travel is not a rendered horse; actor/route reuse points. |
| [viewer-survey.md](viewer-survey.md) | All 24 pre-fire media screened; all 944 Prairie source records searched; 83 targeted Prairie images screened, six priority candidates examined full-size, exact IDs logged. Not a complete visual review of all Prairie records. |
| [vehicle-master-spec.md](vehicle-master-spec.md) | First bounded wagon and provisional open-carriage engineering studies, dimension/material tiers, portable sockets, preservation plan and measurable production gates. |
| [horse-master-spec.md](horse-master-spec.md) | First generic light-harness horse study, proposed anatomy/material targets, separate equine skeleton/clip contract and shared tack/hitch/rider sockets. |

The 80 existing trade wagons (25 farm-box, 17 covered, 38 carts) are static merged renderer geometry, with a separate water-cart layer. Their reconstructed dimensions and colors must retain that tier. Preserve placements while adding portable articulated masters. The existing human exporter validates humanoids; sharing export conventions does not make its humanoid skeleton contract suitable for horses.

## Prioritized source leads and disagreements

1. **J. P. Smith & Co. ICE wagon:** business lettering identifies a concrete commercial subject in the c.1890 McBirney photo. It does not identify the manufacturer, measured chassis, original paint colors, or prove the same livery existed in 1904. Resolve original holder/rights before deriving assets.
2. **Harvey-frontage enclosed carriage:** strong side view; collection calls it a brougham. Type, date and maker still need technical corroboration; frontage does not prove ownership. Prioritize measured builder/museum plans over inventing hidden machinery.
3. **Carriage beside Pullman residence:** LoC item 2016801921, LC-DIG-det-4a08065. Local record says no known publication restrictions. It is a Pullman-location carriage, not an established Pullman-owned one. Recover the high-resolution scan before identifying construction details.
4. **Clarke/Chrimes open carriages:** clear body/wheel/harness views. Right turnout is single; left team count is disputed between audit readings and remains unresolved pending annotated original inspection. Exact date, maker and rights remain open.
5. **Horses at attributed Glessner stable:** useful anatomy/harness pixels; existing T-2198 disputes building attribution. Do not promote location/ownership to fact.

The pre-fire viewer yields no dependable contemporary photographic model plate in this screening. Later drawings depict horse vehicles, but are retrospective evidence, not direct photographs of earlier Chicago. Earlier scenes require dated analogies or bounded reconstructions. No horse breed, individual animal identity or original color has been established.

## Access and validation limits

Both live viewer HTML endpoints returned HTTP 200 through the supported proxy. Image analysis used local source files and pixels, not interactive Chrome browsing; no Chrome connector was available. Requests to Library of Congress, Internet Archive and Glessner external sources returned proxy 403. Required domain additions were saved to the environment draft; saving does not establish current access. Do not bypass the proxy or mark those unvisited sources verified.

Environment installation/start instructions were tested and saved separately in the environment draft. Mobile stage-1 4D smoke passed 95 checks; complete release smoke and production asset/render validation are different work. The initial full repository check had a concurrent generated-mirror publication failure; clean serial publication and its mirror check subsequently passed. Queue validation also found inherited T-2686's `PROVENANCE` category unsupported by this selected main checkout's tool; do not rewrite that unrelated ticket to hide a tooling-version mismatch.

The initial research/setup phase changed no tracked application source. Subsequent owner-authorized model work is now recorded in [CHECKPOINT.md](CHECKPOINT.md), with the exact code commit, validation and recovery instructions. No dependency declaration or lockfile was modified.
