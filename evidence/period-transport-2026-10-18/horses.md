# Horses and gear: implementation and visual evidence audit

Audit date: 2026-10-18. Read-only examination of application and local research collections; this report is the only file authored by this audit. This is an initial evidence-backed assessment, not completion of the requested deep archival research. Local copies and their existing catalog metadata were inspected; the live public viewers and external catalog pages were not visited by this agent.

## Existing implementation

- `chicago/chicago/4d/renderers/web/js/travel.js`, especially lines 17–25: horse/wagon travel is camera movement. The header explicitly says that riding does not draw a horse. Defaults and gait labels are interface choices, not period evidence. They cannot be used as measured animal animation speeds.
- `renderers/web/js/route.js`, including line 841: road routing already distinguishes horse/wagon from pedestrian modes. Reuse the street routing semantics, but inspect road widths and collision envelopes before adding a physical horse, shafts, team or vehicle.
- `renderers/web/js/humans.js`: an existing engine loads rigged glTF actors, clones skeletons safely, animates, picks, switches LOD, and disposes assets. Human LOD bands are 8/20/45 m; face animation stops beyond 20 m, shadows beyond 30 m, mixers beyond 70 m, rendering beyond 140 m. These are reusable patterns, not an already implemented horse actor or suitable horse budgets without measurement.
- Human scene mounting is distinct from the actor engine and enforces L1. `docs/HUMAN-ASSET-CONTRACT.md` is the existing human integration contract. A seated state exists; a rider/driver pose, reins/hand targets and synchronized mount movement still need specific work.
- `docs/RESEARCH/1835_tavern_horse_keeping.md` documents licensed houses charging to feed and keep horses, citing Andreas volume 1 scan p. 249 (`andreas_1884_v1`). It distinguishes evidence of service from evidence of any particular stable structure.
- `data/sources/fergus_historical_series_26_29.json` records the mail sequence including a four-horse stage semiweekly in 1834 and triweekly in 1835. This establishes service/team count as recorded there, not a photographic vehicle design.
- `data/sources/trowbridge_sauganash_hotel.json` already identifies a saddled horse at a roadside post in a retrospective drawing. No horse mesh/rig, tack assembly, equine clip set or horse actor module was found by targeted filename/content search. This is a search result, not an exhaustive binary asset inventory.

## Actual images viewed

Paths below are relative to `/workspace`. Metadata is from `chicago/chicago/prairie_1904_v1/data/images.json`, except where stated. The visible observations below are this audit's reading of the actual pixels.

### Clarke/Chrimes carriages: strongest close harness reference found

- File: `chicago-images/prairie-1904/files/a19-gh-clarke-wabash-chrimes.jpg` (1500 × 1008).
- Catalog: https://glessnerhouse.blogspot.com/2014/08/house-moving-part-ii-clarke-house-1872.html
- Title: house after its move to 4526 S. Wabash with members of the Chrimes family; courtesy Clarke House Museum.
- Date: undated after June 1872; registry suggests 1880s–1900s and records broad bounds 1872–1910. This is NOT pre-fire evidence and is not securely dated to 1904.
- Photographer unknown. Museum blog reproduction; rights **unknown — link only**. Do not derive assets until rights/holding institution terms are resolved.
- Visible: two occupied open carriages in side/three-quarter profile, fine spoked wheels, narrow shafts, reins running to seated occupants, bridles and body harness; near horse at right has a visible light facial marking. Considerable overlapping anatomy occurs at left. One audit initially read a paired left team; another read two single-horse turnouts. **Team count remains disputed and must be resolved from a higher-resolution original before being modeled as an attested pair.** Neither breed, exact carriage subtype, maker, owner of each turnout, nor original coat color is established by this sepia image.
- Valuable first task: independently annotate horse silhouettes, shaft positions, leg counts, harness traces, seat/hand positions and wheel geometry, recording which details remain occluded.

### J. P. Smith & Co. ice delivery wagon

- File: `chicago-images/prairie-1904/files/a16-ghm-blog-1736-mcbirney-c1890.jpg` (900 × 611).
- Catalog: https://glessnerhouse.blogspot.com/2020/07/the-early-history-of-prairie-avenue.html
- Date: circa 1890; registry bounds 1885–1895. Creator unknown; original holder not named.
- Rights **unknown — link only**; resolve before asset derivation.
- Visible: covered delivery wagon at kerb, legible `J. P. SMITH & CO. ICE` branding, two horses facing toward the camera in a front-three-quarter view, wheels and team connection partially occluded. This is an identifiable business/vehicle depiction and a stronger named starting point than an unverified assertion of Pullman's personal carriage. Exact harness component geometry, manufacturer, horse breeds and coat colors are not established.
- Valuable first task: seek original negative/print and dated trade advertisements/catalogs to identify vehicle construction and lettering independently.

### Enclosed carriage on the 2100 block

- File: `chicago-images/prairie-1904/files/a20-glessner-2100-block-east-side-1890s.jpg` (604 × 675).
- Catalog: https://glessnerhouse.blogspot.com/2015/08/marriott-marquis-breaks-ground.html
- Date: 1890s per museum blog caption. Original photographer/holder unknown.
- Rights **unknown — link only**.
- Visible: enclosed carriage and horse in the roadway, largely side-on with a slightly oblique front, slender wheels and raised roof/cabin. Useful silhouette and street-scale evidence; too small/dark for close tack construction, exact horse anatomy or confident subtype attribution.

### Near-1904 distant movement context

- File: `chicago-images/prairie-1904/files/a19-chm-ichi66015-west-side-north-from-allerton.jpg` (750 × 565).
- Catalog: https://collections.carli.illinois.edu/digital/collection/chm_pp/id/1296
- Charles R. Clark; Chicago History Museum via CARLI; circa 1905 (registry bounds 1903–1907).
- Rights `no known restrictions`, but registry explicitly retains link-only because CHM asks reproduction licensing via its image service. Preserve that caveat.
- Visible: small horse-drawn traffic at distant right side of avenue. Useful composition, density, street scale and distance-quality target. Insufficient resolution for harness or horse identity. Catalog location wording conflicts with apparent block; registry records that disagreement.

### Early Chicago: retrospective saddled horse

- File: `chicago/chicago/reference/images/chicago/sauganash-hotel/sauganash2.jpg`.
- Source record: `chicago/chicago/4d/data/sources/trowbridge_sauganash_hotel.json`.
- Catalog reproduction: https://chicagology.com/chicagostreets/lakestreet/
- Visible: saddled horse at right edge, standing at roadside post; partial animal cropped at image boundary. Small-scale drawn tack silhouette only.
- W. E. S. Trowbridge; plate undated. Related Green Tree drawing is signed 1902, but that does NOT date this plate. Describes Sauganash's 1831–1851 life retrospectively, not an eyewitness view of 1 July 1835. Registry tier 5; `rights_status: check_required`; `asset_use: cross_check`. No derived asset permitted under current source status.
- Also viewed `sauganash.jpg` (Braunhold/Andreas engraving), which does not supply the same clear horse, and `chicago_sauganash_hotel_1831_petford.jpg`, which shows posts but no horse. Do not count these as independent horse witnesses.
- Pre-fire viewer registry at `chicago/chicago/pre_fire_v1/data/media.csv` distinguishes 1884 Andreas retrospective lithograph from depicted 1831–1833 and separately catalogs the 1893 Kurz & Allison sheet. Publication date must remain separate from depicted date.

## Research conclusions and remaining work

The collection already supports identifiable turnouts and a named ice delivery wagon, but not a verified Pullman-owned personal carriage. A coach-house photograph is not evidence identifying a specific carriage. Existing sources do not justify assigning horse breeds or recovering exact colors from monochrome images. Match visible silhouette, proportions, markings and tack while labeling unseen geometry and color as bounded reconstruction.

Separate the 1835 scene from the broader pre-fire period and the 1904 scene. An 1860s vehicle can be pre-fire yet wrong for 1835; a post-1872 Clarke photo cannot seed an attested 1835 turnout. Seek dated, rights-cleared museum vehicle records, maker catalogs, harness catalogs and contemporary equine references for each target date; do not register external sources as verified until actually read. Acquire primary originals for the named local cases first. Later horse locomotion photography can inform anatomy/gait mechanics with its temporal role stated, not prove an 1835 Chicago turnout or tack set.

## Phased horse/gear tickets and acceptance

1. **Reference and provenance dossier.** Independently resolve the Clarke team-count disagreement; identify original holders/rights and exact source dates where possible; annotate visible harness, horse shape/markings and seated human geometry. Keep source date, depicted date, scene applicability and confidence separate. Deliver image contact sheets with exact locators and an uncertainty table; no invented breed or ownership.
2. **Portable equine asset contract.** Define engine-neutral glTF, metre scale, coordinate/facing convention, skeleton hierarchy, clip names, feet/contact markers, body dimensions, rider-seat/hand/foot targets, bridle/rein/harness/shaft anchors, collision envelopes, LOD/material/texture budgets and license/provenance manifest. Reuse existing human loader/LOD patterns without coupling horses to person identity.
3. **First static horse and interchangeable gear.** One rights-cleared, reference-matched body with skin, mane/tail, eyes, hooves and documented coat reconstruction; separate riding tack and single/team draft harness. Review neutral close-up lighting plus matched source views. Occluded backs/sides and color remain declared reconstructions. No modern generic saddle silently substituted for period tack.
4. **Equine rig and locomotion.** Idle, walk, trot, stop/start/turn first; add faster gaits only when needed. Validate footfall order, limb articulation, hoof contact, speed/stride relationship, turns and transitions without sliding. Reins and traces follow tension/contact constraints; shafts/team spacing remain stable. Camera travel speed labels do not supply animation truth.
5. **Distant horse-drawn traffic.** Reuse road graph semantics; include horse/team/vehicle swept bounds, turning radii, clearance, deterministic spawning and stopping, wheel rotation from travel distance, and distinct simulation/animation/visibility LOD. Measure mobile and desktop tiers; distinguish nearby interaction actors from distant low-cost traffic. Source-matched distance screenshots must still read as horse-drawn traffic.
6. **Rider/driver integration.** Portable-human rider poses, seat anchors, stirrup/foot and rein/hand targets, gait-synchronized body motion and combined collision; first exercise in an isolated nonpublished fixture. Existing L1 scene policy remains distinct from engine capability; do not silently enable public human figures.
7. **Mount/ride/dismount.** Approach eligibility, boarding/mount point, occupied state, camera transition, steering/stop, safe dismount/exit, collision and interaction recovery. Save source IDs and reconstruction notes on visitor evidence cards. Wagon passenger boarding, coachman driving and direct horse riding are separate capabilities, even when they share input/controller code.

No production scene depiction, external publication or source-rights change was performed by this audit.
