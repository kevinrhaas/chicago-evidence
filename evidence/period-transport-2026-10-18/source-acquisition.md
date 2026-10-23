# T-2792 — source acquisition, 2026-10-18

This follow-up advances beyond the local image audit: Internet Archive search and
item metadata were retrieved successfully, three useful period technical sources
with explicit public-domain metadata were identified, and the Glessner House
Clarke article was read online. Full technical text/plates remain blocked at
Archive download redirects. No dimensions have been invented or attributed to an
unread book. This is not a completed modeling or photographic-match report.

## Sources actually accessible

All requests used inherited HTTPS proxy/CA configuration, with TLS verification
enabled. The statuses below describe GET responses unless explicitly called HEAD.

### 1. Fulton & Walker Company, 1893 commercial-wagon catalog

- Exact item: <https://archive.org/details/gri_33125017557972>.
- Retrieved metadata: <https://archive.org/metadata/gri_33125017557972> (HTTP200).
- Title: *Illustrated catalogue of the work of Fulton & Walker Company coach and
  wagon builders: “wagons for business”*.
- Creator: Fulton & Walker Company (Firm). Publisher: Philadelphia, Armstrong and
  Fears. Date:1893. Catalog description:86 pages. Contributor/sponsor: Getty
  Research Institute. Call number:`9922688920001551`; OCLC:`80461041`.
- Metadata rights field: `possible-copyright-status: NOT_IN_COPYRIGHT`.
- Relevance: first-party manufacturer catalog, eligible as period construction
  evidence for a1904 commercial wagon. This is substantially stronger for vehicle
  identity than an uncaptioned wagon outside a mansion. It does not establish any
  Fulton & Walker wagon in Chicago, and it is not eligible as an1835 design source.
- Dimensions: **not yet read**. No particular model number selected from unread
  plates. Do not call the catalog measured merely because technical data is likely.
- OCR file advertised by metadata: `gri_33125017557972_djvu.txt`, 34,716 bytes,
  SHA1 `4e9ad9e0c47429fd38d7d7f99c8f9a5267eb61cd`.
- Download URL:
  <https://archive.org/download/gri_33125017557972/gri_33125017557972_djvu.txt>.
  Returns302 to
  `https://dn720005.ca.archive.org/0/items/gri_33125017557972/gri_33125017557972_djvu.txt`;
  the redirected request fails `CONNECT tunnel failed:403 Forbidden`.
- Next useful operation: permit the observed Archive CDN destination through
  supported environment configuration, acquire OCR and page images, verify hashes,
  identify a specific illustrated wagon, and transcribe its printed specifications
  against the scanned page rather than OCR alone.

### 2. Isaac D. Ware, 1875 carriage-building handbook

- Exact item: <https://archive.org/details/gri_33125000005005>.
- Retrieved metadata: <https://archive.org/metadata/gri_33125000005005> (HTTP200).
- Title: *The coach-makers' illustrated hand-book: containing complete instructions
  in all the different branches of carriage building, adapted to the wants of every
  person directly or indirectly connected with the manufacture of carriages*.
- Creator: I. D. (Isaac Delaney) Ware,1839–1901. Publisher: Philadelphia, I. D. Ware.
  Date:1875. Getty Research Institute. Call number:`9921869560001551`;
  LCCN:`44024327`. Metadata image count456, not a claim of456 numbered text pages.
- Metadata rights:`NOT_IN_COPYRIGHT`.
- Relevance: period technical construction/manual source for later nineteenth
  century carriage mechanisms. Date precedes1904 but follows the1871 fire; do not
  use it as contemporary1835 or pre-fire evidence. Earlier designs must be dated
  individually if the book discusses them retrospectively.
- Dimensions/construction passages: **not yet read**; no exact spring, axle,
  wheelbase or carriage subtype is certified from this item.
- OCR: `gri_33125000005005_djvu.txt`,1,238,276 bytes,
  SHA1 `39eeaef758e554bf704a50e50081ab23dc16d450`.
- Download:
  <https://archive.org/download/gri_33125000005005/gri_33125000005005_djvu.txt>
  redirects302 to
  `https://ia800505.us.archive.org/3/items/gri_33125000005005/gri_33125000005005_djvu.txt`;
  redirected host blocked by proxy403.
- Next: acquire text/plates and select a dated four-wheel open passenger carriage
  with a published dimensional section. This is the preferred technical-source
  candidate for C01; the current generic C01 envelope remains reconstructed.

### 3. John Gustaf Holmström, Chicago,1904

- Item: <https://archive.org/details/modernblacksmith00holm>.
- Retrieved metadata: <https://archive.org/metadata/modernblacksmith00holm> (HTTP200).
- Title: *Modern blacksmithing: rational horse shoeing and wagon making, with
  rules, tables, recipes, etc.* Creator: John Gustaf Holmström.
- Publisher: Chicago, F. J. Drake & Co. Date:1904. Contributor: Webster Family
  Library of Veterinary Medicine; sponsor: Tufts University. Metadata says the
  copy is part of the John A. Seaverns Equine Collection. LCCN:`04011553`.
- Metadata rights:`NOT_IN_COPYRIGHT`.
- Relevance: particularly useful joint wagon/horse-gear technical source, published
  in the scene year and in Chicago. Publication locality is not proof that a
  depicted wagon belonged to a named Prairie Avenue household. Year1904 alone
  does not establish availability by target date1904-07-01; inspect front matter
  before making that stronger claim.
- Dimensions and technical statements: **not yet read**.
- OCR: `modernblacksmith00holm_djvu.txt`,274,024 bytes,
  SHA1 `8facf86663cacfc55a36e835f0c96b5a71993e2a`.
- Download:
  <https://archive.org/download/modernblacksmith00holm/modernblacksmith00holm_djvu.txt>
  redirects302 to
  `https://dn790000.ca.archive.org/0/items/modernblacksmith00holm/modernblacksmith00holm_djvu.txt`;
  redirected host blocked by proxy403.

### 4. G. W. Clark,1870 painting guide

- Item/metadata: <https://archive.org/details/carriagemakerspa00clar> /
  <https://archive.org/metadata/carriagemakerspa00clar> (metadata HTTP200).
- Title: *The carriage maker's and painter's “guide.”* Publisher: Buffalo, N.Y.,
  Haas & Kelley,1870. Contributor: Library of Congress. LCCN:`09002339`.
- Metadata rights: “The Library of Congress is unaware of any copyright
  restrictions for this item.”
- Potential use: period finish/material terminology, contemporary to1870 and prior
  to1904. It is not evidence of any specific vehicle's color or an1835 paint scheme.
- Contents not read; technical dimensional value unestablished. OCR download
  redirects to `ia800905.us.archive.org`, an additional observed destination.

### 5. Glessner House Clarke article, freshly read

- Exact URL:
  <https://glessnerhouse.blogspot.com/2014/08/house-moving-part-ii-clarke-house-1872.html>
  (HTTP200,107,693 HTML bytes at acquisition).
- Article: “House Moving Part II: Clarke House,1872,” August11,2014.
- The caption confirms “The house after its move to4526 S. Wabash Avenue with
  members of the Chrimes family in the foreground (Courtesy of Clarke House Museum).”
- Text places the house on its new foundation in June1872. This confirms the
  post-move context, not an exact carriage photograph date. No carriage manufacturer,
  model number, vehicle dimensions or explicit permission to derive assets was
  found in the article's relevant caption/text.
- Rights remain unresolved. Do not promote “courtesy” into a license. The article
  is a modern contextual source reproducing an older image, not a primary technical
  carriage record. The reported left-team count remains unresolved in the shared
  research record; no modeling decision here relies on it.

## Pullman / LoC request result

The exact catalog URL <https://www.loc.gov/pictures/item/2016801921/> returned200
to HEAD, but both its HTML GET and
<https://www.loc.gov/item/2016801921/?fo=json> returned403. A successful HEAD does
not establish readable catalog access. No high-resolution vehicle image or fresh
item-rights verification was acquired. The earlier local record's “no known
restrictions” statement remains the available rights evidence. Do not claim that
this follow-up identified Pullman's own carriage.

## Local source corpus checked for an immediately usable measured master

Searched the372 top-level `chicago/chicago/4d/data/sources/*.json` records for
vehicle/coach/wagon terms and inspected the relevant construction sources and
committed vehicle forms. Also checked the image streams and earlier audit paths.
No local source found in this pass supplies a cleared, measured passenger-carriage
master or makes the current farm wagon's invented dimensions attested.

- `data/yard/town_trade_goods.json`: W01's3.05×1.07×0.55m box dimensions explicitly
  reconstructed. Existing renderer wheel diameters/bed/tongue likewise remain
  reconstruction values. This is the ready portable-wagon compatibility target,
  not a newly discovered primary measured vehicle.
- `data/yard/town_water_cart.json` and
  `data/research/civic/claims/town_findings_andreas_v1.json#c013`: documented
  two-wheel/hogshead arrangement, lake filling by pail and Randolph Street locality.
  Andreas1884 is retrospective and supplies no measured chassis/body dimensions.
- `data/sources/trowbridge_green_tree_1902.json`: retrospective picture of1835,
  marked `check_required`; not an authorized source-derived geometry input.
- `data/sources/andreas_1884_green_tree_hotel_plate.json`: public-domain architectural
  plate; not a measured wagon drawing.
- `data/sources/dupage_history_david_brookins.json`: public-domain1882 county
  history, carriage-selling biographical lead; not a vehicle specification.
- `data/sources/resident_research_tribune_mitchell_1883.json`: wagon-factory
  biographical evidence, `check_required`; no cleared measured vehicle.
- Coach-house/porte-cochere architectural records locate/describe buildings and
  doors. They must not be converted into a household carriage inventory or a
  dimensional drawing of vehicles stored behind them.

## Selected reference and immediate next operations

**First buildable wagon reference remains W01's existing independently authored
reconstruction**, with the same data values and explicit liberties. It can become
an articulated glTF prototype without waiting for a catalog download or deriving
anything from a rights-pending photograph. Preserve the existing80 wagon placements
as specified in `vehicle-master-spec.md`.

**First primary reference selected for acquisition is the1893 Fulton & Walker
catalog**, with the1875 Ware handbook selected for passenger-carriage technical
construction. Their rights metadata is affirmative and their authorship/date are
known. A particular catalog model and dimensional table cannot honestly be selected
until readable pages arrive. Their1904-era use is a distinct branch from W01's1835
compatibility model; do not overwrite W01 with an1893 wagon design.

Remaining blocked operations are concrete:

1. Apply supported network access for observed Archive download hosts
   `dn720005.ca.archive.org`, `ia800505.us.archive.org`,
   `dn790000.ca.archive.org` (and `ia800905.us.archive.org` for paint guidance), or
   the Archive CDN family if the environment settings support that reviewed scope.
   No direct-network or alternate-proxy bypass was attempted.
2. Download OCR and verify against metadata hashes, then open actual page images.
   Transcribe each selected model's dimensions with printed page number, image
   leaf and exact quoted units. OCR alone cannot settle fractions or dimension arrows.
3. Add a source record/license provenance before using newly acquired public-domain
   plates in asset generation. Their metadata rights basis is recorded above;
   no new code/data source IDs have been fabricated here.
4. Recover the LoC original and resolve museum-image rights independently. Those
   unresolved images can remain research leads while independent prototype work
   continues. Do not claim photographic quality before an eligible reference is
   actually matched.

Temporary acquisition metadata/HTML are stored under `/tmp/vehicle-sources/` for
this working session; those scratch files are not durable published assets. The
exact identifiers, checksums and findings above are the durable handoff.
