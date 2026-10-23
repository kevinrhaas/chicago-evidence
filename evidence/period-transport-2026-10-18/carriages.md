# Period carriages and wagons: initial evidence and implementation audit

Date: 2026-10-18. Scope: the selected `main` checkouts of `kevinrhaas/chicago`,
`chicago-images`, and `chicago-tickets`. This is an initial local-source audit, not
a completed survey of every photograph in either research browser. The images
listed below were opened and visually inspected. Repository notes are distinguished
from observations made during this audit.

## Findings that can guide the first work

The collection already contains a particularly useful photograph of two open
carriages (right drawn by one horse; left team count unresolved) outside the Clarke House during the Chrimes family's tenure.
It shows more carriage and harness detail than the Pullman-house photographs reviewed
here. Its date and rights need further resolution before it can support a named,
precisely dated replica or an asset derived from its pixels.

A Library of Congress photograph of the Pullman residence contains a carriage at
the 18th Street kerb. This is a good named-location lead with a usable recorded
rights basis. It does **not** establish that the vehicle belonged to George Pullman.
The available derivative is too small to settle its body type or construction.
Recovering the highest-resolution institutional scan is the next concrete research
action. No Pullman-owned vehicle has been identified by this audit.

The current 1835 scene already has a substantial static wagon layer. It should be
assessed and reused selectively, rather than treated as an absent feature or as a
finished articulated transport system. Its dimensions, placements and colors are
mostly declared reconstructions; photographic detail must not silently promote
those values to attested measurements.

## Photographs and drawings actually inspected

Paths below are relative to `/workspace`.

| Image | Direct observation | Dating and identity limits | Rights and next action |
|---|---|---|---|
| `chicago-images/prairie-1904/files/a19-gh-clarke-wabash-chrimes.jpg` | Two open four-wheel vehicles with occupants: right drawn by one horse; overlapping anatomy leaves the left team count unresolved pending higher-resolution review. Useful lateral/oblique views of hitch arrangements, fine spokes, body/seating, reins and harness. | Caption identifies members of the Chrimes family, not the vehicle makers or carriage types. House is at 4526 S. Wabash after its 1872 move. Exact exposure date unknown. | Record says `unknown — link only`; a credited reference copy is present. Do not texture, trace, or derive an asset while its rights remain unresolved. Seek the Clarke House Museum original and item-level terms. |
| `chicago-images/prairie-1904/files/a16-pullman-det-4a08065.jpg` | Small enclosed-looking carriage seen principally from behind at the 18th Street kerb beside the Pullman residence. Body/type identification remains tentative at this resolution. | House/location is identified; owner, manufacturer, model and exact vehicle date are not. Do not name it “Pullman's carriage.” | Record says `no known restrictions`. Obtain the institutional high-resolution scan, then inspect body, roof, rear wheels, suspension, lamps and horse arrangement before selecting a class. |
| `chicago-images/prairie-1904/files/a16-pullman-det-4a08066.jpg` | Companion view along the Pullman property's 18th Street side; no similarly useful vehicle detail found. | Useful architectural/location context, not proof of an absent or owned vehicle. | LoC record says `no known restrictions`; not a principal vehicle modeling reference. |
| `chicago-images/prairie-1904/files/a16-aic-taylor-pullman-from-nw.jpg` | Pullman house and detached service/coach-house context; no useful carriage detail found in this inspected view. | A coach house establishes building context, not a particular carriage inventory. | Consult its complete record before reuse; no rights decision is made here. |
| `chicago-images/prairie-1904/files/st-flinn-1892-looking-south-prairie-from-18th.jpg` | Street, walks, trees and residential frontages; no sufficiently detailed vehicle found. | An engraved streetscape is not a measured vehicle drawing. | Useful setting context only in this audit. |
| `chicago/chicago/pre_fire_v1/media/images/buildings/green_tree_tavern_1859.jpg` | Reproduced line image of the building and street edge; no carriage/wagon detail found. | Viewer metadata calls it a historical photograph, but the file visibly presents a line reproduction. Resolve medium/original before calling this photographic evidence. | Viewer says public domain with a note to recheck item-level terms for external republication. |

### Exact records for the strongest references

**Clarke House / Chrimes family**

- Record: `a19-gh-clarke-wabash-chrimes` in
  `chicago/chicago/prairie_1904_v1/research/images/stream-1900.json`.
- Title: “The house after its move to 4526 S. Wabash Avenue with members of the
  Chrimes family in the foreground (Courtesy of Clarke House Museum).”
- Catalog/context: <https://glessnerhouse.blogspot.com/2014/08/house-moving-part-ii-clarke-house-1872.html>.
- Record date: “undated (after June 1872; carriages and dress suggest c. 1880s–1900s).”
  Machine bounds are 1872–1910. These bounds are not proof of an exposure in 1904.
- Creator unknown; museum blog reproduction; rights not stated. Original copied
  image dimensions recorded as 1500 × 1008.
- Family identification is contextual attribution from the record, not an
  independently established identification of each occupant by this audit.

**Pullman residence / carriage at kerb**

- Record: `a16-pullman-det-4a08065` in
  `chicago/chicago/prairie_1904_v1/research/images/stream-1600-1700.json`.
- Institutional catalog: <https://www.loc.gov/pictures/item/2016801921/>.
- Title: “The Pullman residence, Chicago”; Detroit Publishing Co.; Library of
  Congress Prints & Photographs Division, Detroit Publishing Company collection.
- Call numbers: `LC-D4-12551 [P&P]`; `LC-DIG-det-4a08065`.
- Existing image URL:
  <https://tile.loc.gov/storage-services/service/pnp/det/4a00000/4a08000/4a08000/4a08065v.jpg>.
- Catalog date text held locally: “[between 1890 and 1901].” Repository earliest
  bound is 1893 because the monument erected that year is visible; latest 1901.
- Local derivative: 1024 × 804. It supplies a silhouette/location lead, not enough
  evidence for a photoreal carriage replica.
- Rights held locally: “No known restrictions on publication.” Preserve the
  institutional statement and credit with any permitted source/asset record.
- Companion: <https://www.loc.gov/pictures/item/2016794585/>, `LC-D4-12552 [P&P]`,
  `LC-DIG-det-4a08066`, c.1900, locally bounded 1899–1901.

### Additional carriage/wagon candidates visually verified after cross-agent review

- `chicago-images/prairie-1904/files/a16-ghm-blog-1736-mcbirney-c1890.jpg`: covered commercial wagon with a pair of draft horses, front-three-quarter view. Visible lettering reads `J. P. SMITH & CO.` and `ICE`. This is a stronger named commercial-vehicle lead than an unproven Pullman ownership attribution; the lettering identifies the depicted business, not the wagon manufacturer. Local record dates it c.1890 and has unknown/link-only rights.
- `chicago-images/prairie-1904/files/a20-glessner-2100-block-east-side-1890s.jpg`: side/oblique street view of one horse drawing an enclosed carriage, with running gear and body silhouette visible. Local dating is 1890s; rights unknown/link-only. Body subtype remains unconfirmed.

Both were suggested by the horse research agent and then independently opened in this audit. They should enter the reference/rights register before any geometry is traced or materials derived. Neither demonstrates an 1835 vehicle.

## Existing wagon implementation

The following are code/data observations, not a live-renderer measurement:

| Component | Current state |
|---|---|
| `chicago/chicago/4d/data/yard/town_trade_goods.json` | Counts 80 wagons: 25 `farm_box`, 17 `covered`, 38 `cart`. Counts also report 71 street-verge and 6 yard placements; these categories should not be assumed to exhaust every held/manual stand. |
| `chicago/chicago/4d/tools/generate_yard_goods.py` | Derives the yard goods and wagon placement record. Retain deterministic placement and refusal reasons when replacing geometry. |
| `chicago/chicago/4d/renderers/web/js/yard.js` | Builds static merged geometry at runtime, rather than loading one articulated glTF vehicle per wagon. `buildWagon` begins around line 1483 in this checkout. |
| Wagon form | Planked box, axles, wheels, bolsters, reach, hounds, kingbolt, tongue; optional canvas tilt; deterministic paint variation. |
| Cart form | Two-wheel cart with shafts; also supports the separately recorded hogshead water cart. |
| Unhitched state | Tongues and shafts are inclined down to ground. Existing comments explicitly describe no draft animals. Ox yokes are props beside selected wagons. |
| Animation interfaces | Current merged static geometry is not evidence of steerable front-gear nodes, rotating wheels, suspension rig, boarding seats or a horse coupling contract. These require explicit new interfaces. |

Some source comments still mention 68 wagons. The current committed data count is
80. This report does not claim that 80 are visible in any particular live camera.

Important existing tickets to consult before filing overlapping work:

- T-0040: first goods/wagon layer.
- T-0064: additional frontier-town wagons.
- T-0084: tongue form corrected from an oversized plank.
- T-0087: bolsters, reach, hounds and kingbolt, closing the floating-box defect.
- T-0688: wagon-variety gate measures placement slew rather than street headings.
- T-0759: hogshead water cart, cited in `yard.js`.
- T-0836: standing orientation variation, discussed by T-0688.
- T-2121: planked bodies and paint/wood variation, cited in `yard.js`.

### What existing dimensions mean

`town_trade_goods.json` explicitly labels the wagon body of 3.05 × 1.07 × 0.55 m
as invented/reconstructed: approximately 10 ft × 3 ft 6 in × 22 in. Rear/front wheel
diameters of 1.37/1.07 m and bed height of 0.95 m are the existing form values,
not measured dimensions of a specific Chicago wagon. Cart dimensions are likewise
reconstructed. Keep that grade if these proportions seed a new master.

The separately recorded water-cart trade has stronger documentary description:
`data/yard/town_water_cart.json` cites `andreas_1884_v1` through
`data/research/civic/claims/town_findings_andreas_v1.json#c013`: two-wheel vehicles
carried hogsheads, filled by pails after being driven into the lake, generally at
the foot of Randolph Street. Its particular cart, exact appearance, owner, count
and presence on 1835-07-01 remain reconstructed. The testimony is retrospective
(1884), not an 1835 vehicle photograph.

## Chronological eligibility

- **1835 scene, target 1835-07-01:** the current farm box, covered wagon, cart and
  hogshead-cart research can bound declared reconstructions. A late nineteenth
  century carriage photograph cannot simply be backdated into this scene.
- **Other pre-fire years through 1871:** use a vehicle's actual manufacture/use
  bounds, not the broad “pre-fire” label. The pre-fire viewer's maps and later
  retrospective prints may supply street context without supplying carriage detail.
- **Prairie 1904, target 1904-07-01:** 1893–1901 photographs establish earlier
  appearance of a vehicle class at a place; they do not establish that the same
  individual vehicle survived or stood there in 1904. A class-based reconstruction
  can be appropriate if its temporal case and liberty are stated.
- **Named ownership:** requires an explicit caption, inventory, invoice, museum
  object provenance or equivalent connection. A vehicle parked outside a mansion
  is not sufficient evidence of its owner.
- **People and riding:** research may document seating, mounting and driver pose.
  Shipping a visible rider/driver remains subject to the portable-human work and
  applicable human-depiction constraints. A vehicle-only master can proceed first.

The local pre-fire browser dataset is
`chicago/chicago/pre_fire_v1/viewer/data.json`, with 24 media entries. No entry
contains horse/carriage/wagon metadata terms in this audit's search. That is a
metadata result, not a finding that all 24 images lack vehicles. The subsequent
24-record visual screening is recorded in `viewer-survey.md`; archive-resolution
street-detail review remains outstanding.

The owner's 2026-08-18 brief and identification ledger also contain useful early
wagon research leads: `data/sources/assets/owner_brief_2026_08_18/README.md` identifies
the Trowbridge Green Tree image as showing farm wagons and a covered wagon in a shed;
it links `trowbridge_green_tree_1902`. Its depicted 1835 scene is retrospective,
signed 1902, and marked `check_required`. This audit read that ledger but did not
open the Trowbridge plate, so it is a lead rather than a newly reviewed image.

## Recommended first modeling parcel

Start with one **photograph-bounded static vehicle**, then animate that same master.
First recover the high-resolution LoC Pullman-location scan. If it resolves enough
construction, select its carriage class and name the asset by type and date range,
not unproven ownership. Otherwise use the clear Clarke/Chrimes reference only after
rights are resolved, or acquire a documented public-domain measured vehicle source.
Do not claim the current references support an exact Pullman carriage replica.

The first master should deliver:

1. Source register, cropped-reference locators, rights record, date eligibility,
   identity uncertainty and an attribute table separating attested, inferred and
   reconstructed dimensions, colors and materials.
2. Engine-neutral generated/authored glTF under the project's existing provenance
   rules, with wheel centers, wheel radii, track, wheelbase and steering kingpin
   recorded in data rather than hidden in one renderer.
3. Separate root/body, front steering gear and wheel nodes; declared shafts or
   pole attachment; hitch and seat/boarding sockets; axes, units and pivots.
4. Period-specific body, suspension, wheels, ironwork, lamps, upholstery and paint
   only to the extent the selected evidence permits. Monochrome photographs do
   not attest paint color. Hidden surfaces must be declared reconstructions.
5. Near, mid and distant comparisons against the actual reference at solved or
   explicitly approximate cameras; no completion claim based only on a successful
   export. A silhouette/distant pass alone is not photographic-quality acceptance.
6. Measured LOD/draw-call/triangle cost, collision envelope and a static placement
   that preserves existing wagon stands where appropriate.

Next parcels should separate mechanically coupled motion (wheel rotation from
distance, steering geometry and turn envelope), horse/harness coupling, distant
traffic route behavior, then boarding/riding controls. New animation must not move
the body while leaving an unhitched tongue on the ground or let a horse walk without
matching wheel travel and shaft/pole motion.

## External research status and remaining work

The environment's supported HTTP policy snapshot was inspected. During this audit,
an HTTPS HEAD request through the inherited proxy to the exact LoC catalog URL
failed with `CONNECT tunnel failed, response 403`. TLS/proxy verification was not
disabled and no alternate route was used. Consequently the institutional records
above are reported from committed local metadata; this audit does not claim a
fresh online catalog verification or an external deep-dive completion.

To finish the broader research request: enable the needed institutional research
destinations through supported environment settings; retrieve LoC originals;
inspect every candidate image from both browser collections; check Clarke House
rights/provenance; seek dated manufacturer catalogs and museum carriage records for
dimensions and hidden running gear; and seek explicit Pullman inventories or object
provenance before making any ownership attribution. Additional domains should be
requested from observed destination needs rather than guessed as an unrestricted
research entitlement.


## Completion update —22 October 2026, T-2792

The 18 October narrative above is retained as a dated audit, not a current assertion that all archive access is blocked or no cleared construction source exists. The concrete handoff is now [vehicle-master-spec.md](vehicle-master-spec.md), with exact current data/GLB inventory in [existing-vehicle-inventory.json](existing-vehicle-inventory.json) and all 14 relevant full-size inspected viewer references normalized in [inspected-image-register.json](inspected-image-register.json). No rights-pending photograph is included in this new parcel or used as a geometry/texture input.

**First choices:** W01 remains the first 1835 static compatibility wagon, an original unbranded reconstruction. The first specifically documented passenger-carriage target is the 1893 Studebaker Brougham, from the actually inspected, cleared first-party catalog plate leaf 0095. Farm Wagon No4(leaf 0103) is the first numbered1904 wagon target; Fancy Parcel No382(0107) supplies another distinct future design. Their1893 colors/components may guide new1904 type reconstructions; they do not identify any1835 wagon or a1904 household owner. Current W01/C01/C02 do not acquire Studebaker branding. Public-domain catalog scans and exact page/text/hash evidence are retained in [the 21 October register](../parked-vehicles-2026-10-21/HISTORICAL-VEHICLE-REGISTER.md) and its `HISTORICAL-VEHICLE-MODEL-REGISTER-AND-DEARBORN-2026-10-21.tar.gz` packet. Root integration includes the actual source record permitting this bounded construction use, not merely an unresolved proposed ID.

J.P.Smith &Co ICE and Harvey-frontage images were re-opened22 October. Smith shows a paired team, high-sided commercial wagon, legible business lettering and a partly obscured chassis; neither maker nor full construction is established. Harvey shows a single horse, shafts, raised coachman's seat, two men, side lamp and enclosed body with clipped rear wheel/body. Both remain unknown-rights/text-citation-only for derived assets. The 1893 catalog supplies a separate cleared construction basis; similarity is not evidence that either photographed vehicle was made by Studebaker.

Kinzie's actual 1856 p297 was re-opened: the Dearborn wagon was brought from Detroit by Kercheval and purchased by John Harris Kinzie for his mother/nephew on the 1831 journey; p302 names a pair of travelling horses. A light passenger wagon, a pair-team interface and that historical purchase are supported; maker/roof/curtains/metres and precise1835 survival/placement are not. This is not1812 evidence. Local Briggs&Humphrey carriage/sleigh manufacture in 1835 is documentary business evidence, not an illustrated model. Market availability is not independently established popularity. The expanded first-edition locator is included in the existing `kinzie_waubun_1856` source proposal without rewriting its earlier chapterXVII claims.

**Fresh LoC investigation:** item2016801921 JSON and resource det.4a08065 JSON both returned200 on22 October. The institution confirms `[between 1890and1901]`, negative glass8×10 in, DetroitPublishingCo no012551, LC-D4-12551 and “No known restrictions on publication.” Local1893 lower bound rests on the visible monument, not a different catalog date. The catalog lists20,855,150-byte`4a08065u.tif` and166,586,278-byte`4a08065a.tif` masters. The smaller official CDN master request returnedHTTP520; the alternative official tile URL did not complete within198seconds and was stopped with no pixels saved. The 166.6 MB master was not requested. The higher-resolution prerequisite remains open; no new type, owner or hidden construction was inferred. The old proxy403 is preserved as historical evidence, but it is no longer a current catalog-access blocker. Exact metadata, requests and outcomes accompany this completion parcel.

**Current inventory and reuse:**80 trade wagons(25 farm_box/17 covered/38 cart) plus one separate hogshead cart. Three farm-box and two varied covered stands are selected for portable1835 replacements; one generic C02 is a reconstructed1904 stop. Preserve the individual stable IDs, coordinates, bearings, coat/age families and laid-by yokes. Inventory includes GLB hashes/bytes, source primitives/triangles, image hashes/dimensions/memory estimates and real socket hierarchy. T-0084/0087/2121 running gear, tongue and varied planking are retained. Actual picked/rendered behavior, whole-frame cost, runtime visibility and exact-source regeneration are separate implementation checks; the 22 October source-reproduction CI failure/repair remains separate from this research deliverable.

**Bounded research result:** first evidence register and executable first-master specification are supplied for review. The image source packet, source rights/tier limits, selected constructions, per-component/pivot/seat/hitch interfaces and actual-match/LOD/performance receipt are concrete. All remaining source work is named: higher-resolution Pullman scan; Smith/Harvey/Clarke original-holder rights and further views; pre1835 Dearborn construction comparator;1812 military-wagon comparator; dated1904 ownership/presence and independent manufacturer popularity evidence. No completed photographic geometry, invisible image acceptance or exhaustive Prairie audit is claimed.
