# T-2792 — primary coachbuilding text read, 2026-10-18

This supersedes the **unread OCR** status in `source-acquisition.md` for the three
books below. It does not supersede their plate/image limitations. Actual primary
text is now accessible through Internet Archive's ordinary full-text reader route,
without disabling TLS, changing proxy configuration, or contacting a denied
storage server. No new model or photographic comparison is claimed here.

## Acquisition and rights

The exact OCR filenames came from each item's successfully retrieved metadata.
These public reader URLs returned HTTP200 HTML containing a `<pre>` full-text OCR
block, which was extracted and read:

| Source | Verified reader URL | HTML bytes / extracted text characters |
|---|---|---|
| Fulton & Walker,1893 | <https://archive.org/stream/gri_33125017557972/gri_33125017557972_djvu.txt> |178,805 /33,855 |
| I.D. Ware,1875 | <https://archive.org/stream/gri_33125000005005/gri_33125000005005_djvu.txt> |1,382,641 /1,237,207 |
| J.G. Holmström,1904 | <https://archive.org/stream/modernblacksmith00holm/modernblacksmith00holm_djvu.txt> |417,724 /273,873 |

These are reader HTML responses, **not byte-identical downloads of the advertised
plain-text files**. Do not claim that their SHA1 matches the download-file checksums
in the earlier report. Each metadata record states `NOT_IN_COPYRIGHT`; exact item
identities, publishers and institutional contributors are in `source-acquisition.md`.
The Getty records contain catalog call numbers and Archive ARKs, but no external
Getty object-record URL was supplied in the retrieved metadata. No guessed Getty
record URL is claimed as accessed.

Only the relevant passages described below were read, not every page of every
book. Printed page numbers are those visible in OCR text; fractional numerals and
figure geometry need image verification before numeric promotion into asset data.

## Ware1875: passenger-carriage construction, not a generic box seat

Source: Isaac D. Ware, *The coach-makers' illustrated hand-book*, Philadelphia,1875,
Getty Research Institute copy `gri_33125000005005`.

### English phaeton, printed p70

Heading: **“ENGLISH PHAETON. THREE-QUARTER-INCH SCALE.”**

The actual text describes three views: Fig1 side elevation in the completed body's
natural position; Fig2 top view established by projected dotted lines; Fig3 back
view recording seat-corner curvature. It identifies bottom sideA, front pillarB,
top arm railC, seat frameDDD and five strainers. Short exact excerpts:

> “The seat frame is grooved at the bottom to receive the panel”

> “select wide panels, which must be cut quartering to allow them to bend around the corners”

> “the joints made on two of the strainers, a recess being left to receive a key panel, which forms keyed joints.”

The arm rail is also grooved for panels; the front pillar is framed into the bottom
side, and the arm rail into the front pillar. The stated visual aim is a massive
appearance through deep panels while retaining lightness. Well-seasoned,
well-painted wood is intended to hide the joints.

**Model implication:** a period-study seat should have a real frame/pillar/rail and
curved panel construction, rather than a rectangular upholstered block. The text
supports this construction **for Ware's English phaeton**. Applying it to an
independently reconstructed C01 is an explicitly reasoned choice; it does not
identify the Chrimes vehicles as English phaetons or turn C01 into a replica.

### French cabriolet Americanized, printed pp70–72

The following section describes body/boot drafting, turn-under, standing pillar and
projected plan lines. One unambiguous integer statement is:

> “the width of the boot, which is 31 inches.”

31in converts exactly to0.7874m. This is a **text-reading candidate dimension for
that illustrated cabriolet's boot**, not a whole-body width, passenger-seat width,
wheel track or C01 dimension. Plate verification remains required before it is
entered as a checked model constraint. Adjacent fractions (body width, turn-under,
rail allowance and half-width) are corrupted in OCR and are deliberately not
transcribed as certified numerical values.

### Victoria phaeton No1, printed p73

The section explicitly discusses a **light Victoria phaeton**, centerline drafting,
lengthening the front pillar to allow for turn-under and obtaining bevels for the
bottom sides, rockers and crossbars. It states a six-inch contraction, but the
preceding half-width has an ambiguous fractional glyph in OCR. Do not transfer
this contraction into a generic carriage without seeing the working draft and
understanding the lines involved. The next section, Victoria phaeton No2, explains
that a crooked arm rail and double-sweep front pillar need a lengthened working
pattern; copying the side outline directly changes the intended sweep.

**Useful next source target:** English phaeton p70 or Victoria phaeton No1 p73,
actual working-draft images. This is now a named technical reference family with
construction read, rather than a bibliography-only lead. Choosing which to model
still requires the plate and a deliberate type selection.

## Holmström1904: wagon axle, wheel and tire construction

Source: John Gustaf Holmström, *Modern blacksmithing: rational horse shoeing and
wagon making*, Chicago, F.J. Drake & Co.,1904, Webster Family Library/Tufts copy
`modernblacksmith00holm`.

### Wooden axle, printed pp187–189

The author specifies **well-seasoned hickory or maple**, removal of the old axle,
and warming the skeins for removal. The replacement axle's length follows the
broken axle. Text says half an inch is removed from the back side and half an inch
from the bottom side at the end, running out at the skein's inner end/collar, in
order to establish pitch and gather. Figure14 is referenced but not visually read.

The functional explanation is important: gather brings the front of the wheel
inward so loading bears toward the collar/wider part of the tapered skein, instead
of the retaining nut. The author warns against copying an old sprung axle's shape.
He recommends no gap between skein collar and axle because water entering it rots
the timber; new versus repaired axles receive different advice about painting the
portion inside the skein.

**Model implication:** represent a timber axle and distinct metal skein/collar
where this construction is chosen; do not depict a wheel simply pierced by a
featureless round stick. Hickory/maple is attested as this manual's recommended
material choice; which species a specific Chicago wagon used remains unknown.
The half-inch hewing instruction is not a measured wheel-camber or toe angle and
must not be converted into one without the skein length and diagram.

### Spokes, printed pp190–191

The author calls for a dry hub mortise and glue, removal/replacement of relevant
hub rivets for buggy-wheel repairs, and the spoke tenon reaching through the rim/
felloe without protruding above its outside. Otherwise a wet felloe can soften,
allow the spoke shoulder to settle and loosen the tire. Hub flange rivets are
restored **before the tire is set**.

**Model implication:** distinguish hub, spokes, wooden felloes and outer tire.
The tenon construction can inform a close-detail model; hidden joinery can remain
declared simplified geometry. The manual does not supply an exact W01 spoke count,
wheel diameter, track or wagon wheelbase in these read passages.

## Fulton & Walker1893: first-party commercial-wagon materials

Source: *Illustrated catalogue … “wagons for business”*, Philadelphia,1893,
Getty copy `gri_33125017557972`. Relevant opening section is headed “HISTORICAL”
in the OCR, followed by company/workmanship discussion. Printed page number not
securely recovered; use the heading and excerpts until actual page images are read.

The company says it makes most springs itself using **“the finest spring steel,
oil-tempered”**, buys **“Patent wheels”**, and buys green timber to date/store it
for seasoning. It specifically lists **oak, ash and hickory**. The text describes
paint as a substantial part of the finished product and says painted wheels of
different wood grades can look alike despite different toughness.

These are attributable manufacturer claims about its own practice, not independent
verification of every catalog wagon. They justify period material vocabulary and
an oil-tempered steel spring option in a later commercial-wagon reconstruction.
They do not prove a specific wagon's wood species or pigment and do not justify
backdating a firm's1893 construction to1835. No vehicle dimension was recovered
from the read catalog text; the cited52×163 storehouse dimensions describe a
building and are explicitly **not** vehicle dimensions.

## Resulting decisions and remaining work

1. W01 may continue as a portable version of the existing1835 reconstruction.
   New technical vocabulary can guide a declared study, but no1835 historical
   attribute is promoted solely from1875/1893/1904 manuals.
2. C01 remains an independent prototype. It now has a specific cleared textual
   construction lead: Ware's English phaeton p70, with frame, curved grooved panel
   seat and keyed joints. Selecting that design as the eventual model is conditional
   on seeing its plate, not inferred from a museum photograph with pending rights.
3. The late-period wagon study can use Holmström's skein/collar/felloe distinctions
   as manual-attested construction, with applicability and any simplification stated.
4. Next acquisition is actual working-draft/figure images and readable dimension
   labels. Do not set an alleged historical wheelbase, track or shaft length from
   this OCR alone. Numeric fractions require image checking; full photographic
   fidelity still needs a suitable vehicle photograph and camera comparison.

Temporary reader HTML and extracted `.ocr` files are at `/tmp/vehicle-sources/`.
Those files are scratch evidence, not new licensed repository assets. The verified
URLs, attributed readings and limitations above are the durable research result.
