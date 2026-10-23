# Glessner House — exterior and courtyard completion programme

Owner-authorized filing, 2026-10-09 UTC. **31 tickets, all manually held; no automated execution.**

> Ok go ahead and file and create tickets for all of this and put them in a group below the people and comment the group out so we can take these tickets manually one at a time

## What was filed

The reviewed 26 audit items are preserved. Four large items (GA-05 roof tiles, GA-09 granite, GA-11 windows and GA-13 inscription/carving) each became two bounded implementation passes, giving 30 completion tickets. One additional ticket covers retrieval of the 17 unavailable source records and the missing-view brief. That makes **31**. Each ticket is `blocked-owner`, carries a clear scheduling reason and appears as a commented `# BLOCKED-OWNER` row in one group immediately below the portable humans (after T-1792). This is the owner's explicit hold, not a request for another permission round.

**Released 2026-10-11:** the owner released the whole group to the loop ("Move all the Glessner house refine tickets below 2352 and un comment them for the loop to pick them up put them above 2341"). The open tickets run one at a time in audit order from band 7, below T-2352 and above T-2341: T-2201 is open, and T-2207 through T-2228 are chained as blocked-tech on their predecessor, so settle opens each in turn. The manual procedure below is history.

## Take one manually

1. Select a specific ticket with the owner and read its dependencies and existing-ticket cross-references. Do not release the rest of the group.
2. Change only that selected ticket from `blocked-owner` to `open`, clear `blocked_on`, and replace only its `# BLOCKED-OWNER` queue row with the normal `T-NNNN — exact title` row in the same group. Record the owner's selection in its body.
3. Regenerate the board, validate and sync the ticket repository, then claim the selected ticket using the normal claim command. All other rows/states stay held.
4. Complete its acceptance and close it through the normal PR workflow. Completing one ticket does not activate its successor.

The stock `unblock` command appends to the queue bottom; if used, restore only the selected row to its place in this group before sync. Never run a bulk unblock.

## Scope and historical limits

Target 1904-07-01. Exterior, courtyard, stable, boundary, ground interfaces and exterior-visible glazing; no furnished interiors. Existing neighborhood work remains in T-1882/T-1883/T-1935/T-2159; T-1843 owns the shared metric/browser contract. The group supplies Glessner-specific completion criteria and must not duplicate those programmes. T-2183 was already recovered in [PR #540](https://github.com/kevinrhaas/chicago/pull/540); preserve its courtyard/eave/copper changes and dark-glass default.

## Ticket map

| Audit item | Filed ticket | Priority |
|---|---|---|
| GA-01 | [T-2198: Glessner: repair source identity, captions and evidence families](../../T-2000-2249/T-2198-glessner-repair-source-identity-captions-and-evidence-famili.md) | P0 |
| GA-R1 | [T-2199: Recover unavailable Glessner references and resolve missing exterior views](../../T-2000-2249/T-2199-recover-unavailable-glessner-references-and-resolve-missing.md) | P1 |
| GA-02 | [T-2200: Glessner: establish a dated, camera-matched exterior acceptance baseline](../../T-2000-2249/T-2200-glessner-establish-a-dated-camera-matched-exterior-acceptanc.md) | P0 |
| GA-03 | [T-2201: Glessner: close the south courtyard boundary and resolve its junctions](../../T-2000-2249/T-2201-glessner-close-the-south-courtyard-boundary-and-resolve-its.md) | P1 |
| GA-04 | [T-2202: Glessner: restore Prairie frontage curbs, thresholds and ground contact](../../T-2000-2249/T-2202-glessner-restore-prairie-frontage-curbs-thresholds-and-groun.md) | P1 |
| GA-05A | [T-2203: Correct Glessner roof tile scale and coverage on every roof plane](../../T-2000-2249/T-2203-correct-glessner-roof-tile-scale-and-coverage-on-every-roof.md) | P1 |
| GA-05B | [T-2204: Remove Glessner roof banding and stabilize tile detail in motion](../../T-2000-2249/T-2204-remove-glessner-roof-banding-and-stabilize-tile-detail-in-mo.md) | P1 |
| GA-06 | [T-2205: Glessner: refine ridge caps, cresting, finials, eaves and flashing](../../T-2000-2249/T-2205-glessner-refine-ridge-caps-cresting-finials-eaves-and-flashi.md) | P1 |
| GA-07 | [T-2206: Glessner: validate roof, dormer and courtyard-bay proportions before further reshaping](../../T-2000-2249/T-2206-glessner-validate-roof-dormer-and-courtyard-bay-proportions.md) | P1 |
| GA-08 | [T-2207: Glessner: finish stable cupola and north loft fittings](../../T-2000-2249/T-2207-glessner-finish-stable-cupola-and-north-loft-fittings.md) | P1 |
| GA-09A | [T-2208: Refine Glessner street masonry courses, relief and opening returns](../../T-2000-2249/T-2208-refine-glessner-street-masonry-courses-relief-and-opening-re.md) | P1 |
| GA-09B | [T-2209: Calibrate Glessner granite texture, roughness and shadow readability](../../T-2000-2249/T-2209-calibrate-glessner-granite-texture-roughness-and-shadow-read.md) | P1 |
| GA-10 | [T-2210: Glessner: calibrate courtyard brick and limestone as distinct materials](../../T-2000-2249/T-2210-glessner-calibrate-courtyard-brick-and-limestone-as-distinct.md) | P1 |
| GA-11A | [T-2211: Finish Glessner street and stable window profiles and stone supports](../../T-2000-2249/T-2211-finish-glessner-street-and-stable-window-profiles-and-stone.md) | P1 |
| GA-11B | [T-2212: Finish Glessner courtyard, bow, turret and dormer window profiles](../../T-2000-2249/T-2212-finish-glessner-courtyard-bow-turret-and-dormer-window-profi.md) | P1 |
| GA-12 | [T-2213: Glessner: give dark glazing believable exterior-visible depth and variation](../../T-2000-2249/T-2213-glessner-give-dark-glazing-believable-exterior-visible-depth.md) | P1 |
| GA-13A | [T-2214: Correct the mirrored Glessner 1886 inscription and monogram](../../T-2000-2249/T-2214-correct-the-mirrored-glessner-1886-inscription-and-monogram.md) | P1 |
| GA-13B | [T-2215: Finish Glessner entry tympanum, ornamental band and varied capitals](../../T-2000-2249/T-2215-finish-glessner-entry-tympanum-ornamental-band-and-varied-ca.md) | P1 |
| GA-14 | [T-2216: Glessner: complete the main entry oak door and iron grille](../../T-2000-2249/T-2216-glessner-complete-the-main-entry-oak-door-and-iron-grille.md) | P1 |
| GA-15 | [T-2217: Glessner: finish both porte-cochere leaves, hardware and passage](../../T-2000-2249/T-2217-glessner-finish-both-porte-cochere-leaves-hardware-and-passa.md) | P2 |
| GA-16 | [T-2218: Glessner: reconstruct the curved courtyard hall steps and cheek wall](../../T-2000-2249/T-2218-glessner-reconstruct-the-curved-courtyard-hall-steps-and-che.md) | P1 |
| GA-17 | [T-2219: Glessner: audit basement grilles, light wells and service openings](../../T-2000-2249/T-2219-glessner-audit-basement-grilles-light-wells-and-service-open.md) | P2 |
| GA-18 | [T-2220: Glessner: refine copper roof panels, seams and weathering](../../T-2000-2249/T-2220-glessner-refine-copper-roof-panels-seams-and-weathering.md) | P2 |
| GA-19 | [T-2221: Glessner: complete gutters, rainwater heads, downpipes and attachments](../../T-2000-2249/T-2221-glessner-complete-gutters-rainwater-heads-downpipes-and-atta.md) | P2 |
| GA-20 | [T-2222: Glessner: resolve chimney phase and finish stack/cap detail](../../T-2000-2249/T-2222-glessner-resolve-chimney-phase-and-finish-stack-cap-detail.md) | P1 |
| GA-21 | [T-2223: Glessner: date and finish courtyard service stairs, rails and rear gate](../../T-2000-2249/T-2223-glessner-date-and-finish-courtyard-service-stairs-rails-and.md) | P2 |
| GA-22 | [T-2224: Glessner: finish courtyard paths, edging, lawn and drainage](../../T-2000-2249/T-2224-glessner-finish-courtyard-paths-edging-lawn-and-drainage.md) | P1 |
| GA-23 | [T-2225: Glessner: add restrained, dated courtyard vines and exterior planting](../../T-2000-2249/T-2225-glessner-add-restrained-dated-courtyard-vines-and-exterior-p.md) | P1 |
| GA-24 | [T-2226: Glessner: balance lighting, contact shadows and restrained surface aging](../../T-2000-2249/T-2226-glessner-balance-lighting-contact-shadows-and-restrained-sur.md) | P1 |
| GA-25 | [T-2227: Glessner: validate full/light browser quality and controlled performance](../../T-2000-2249/T-2227-glessner-validate-full-light-browser-quality-and-controlled.md) | P1 |
| GA-26 | [T-2228: Glessner: run final photographic comparison and evidence sign-off](../../T-2000-2249/T-2228-glessner-run-final-photographic-comparison-and-evidence-sign.md) | P1 |

## Evidence archive

- [Original reviewed audit PDF](glessner-exterior-audit.pdf): retained unchanged as the pre-filing review artifact. Its “not queued” wording describes the review date, not the present ticket state. This index and ticket front matter govern current state.
- [Original 26 proposals](proposed-tickets.json) / [CSV](proposed-tickets.csv), and [filed ticket crosswalk](filed-ticket-map.json).
- [168-record source coverage ledger](coverage-ledger.csv) / [full provenance and hashes](coverage-ledger.json). 102 visual records inspected, 2 written documents read, 44 interior-detail records excluded, 17 catalog-only records and 3 text metadata records. The 17 are not all distinct photographs.
- [12 model captures and browser observations](model/) and [4 close-ups](details/). These are full-detail desktop stills, not mobile/FPS tests.

Snapshot: code checkout ca405da1ae52f2cd15a5b64084ea259f12973e0d; recovered dev build b307fa8e9ebc1f77ab4ac59d9474b8af63369edb. Captures use the locally served published app copy. Source files in the ledger may name the original audit workspace; canonical catalog URLs and file hashes are durable. Restricted source image downloads are not redistributed in this archive. The PDF embeds HABS public-domain references and project model captures.

Additional inspected museum gallery views: GX112.50 (entry/curb), GX112.1–3 (front/northeast), GX112.25 (courtyard bow/chimney), all July 1948, from [the museum Florian gallery](https://glessnerhouse.blogspot.com/2023/07/glessner-house-july-1948.html). These improve detail evidence but do not independently establish the 1904 phase.

## Source corrections and execution caution

Correct Florian associations: #024 is porte-cochere doors, #136 roof/dormers/turret, #137 courtyard toward the stable, #138 industrial interior. Quarantine disputed Lowe #112 as a geometry source until reconciled. Sheet #089 is marked “Not Correct”; preliminary central-gable designs and watercolor conservatory/fountain are not as-built evidence. Correct the confirmed mirrored north 1886 inscription; retain the stable pigeon openings that already exist.

HABS identifies street Wellesley granite, courtyard light pink common brick/Joliet limestone and original unglazed red roof tiles. Later tar treatment, institutional paving, replaced doors/stairs and dense mid-century ivy must be phase-checked. Exact color/patina/hidden construction remain explicitly inferred or reconstructed when not attested.

## Filing validation

Validation must establish that all 31 ticket IDs exist once, are blocked-owner with a stated reason, appear once as commented entries directly after the portable people, and are absent from active queue selection. Existing active row order must remain unchanged. No model, source metadata or deployment changes are included.

Filing checks: all 31 held states, commented rows, dependency/evidence links and absent active queue ranks verified; existing active order unchanged. The strict ticket checker reports the same **9 pre-existing issues before and after**, with **0 introduced**. See [filing validation](filing-validation.json), [baseline](ticket-check-before.log) and [after](ticket-check-after.log). No unrelated ticket was edited to hide a baseline fault.
