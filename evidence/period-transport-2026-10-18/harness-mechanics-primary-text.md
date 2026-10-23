# Shaft tugs, breeching and traction: primary text continuation

2026-10-18, T-2799 / T-2801 research. Read `CHECKPOINT.md` before this pass. Its reported 45 mm shaft-loop gap and unqualified historical fit remain outstanding. This report supplies newly read construction/mechanical text, not a passed fit gate. Only this new report was authored; no generator, GLB, code, queue or earlier report changed. No denied host was retried unchanged. Official Internet Archive stream HTML was fetched through inherited proxy/TLS and its full-text `<pre>` OCR read. No illustration or plate was seen in this pass.

## The historical component graph needs separate forward and restraining paths

**Francis Dwyer, *Seats and saddles, bits and bitting, draught and harness, and the prevention and cure of restiveness in horses***. IA `seatssaddlesbits00dwyerich`. Metadata actually read: creator Francis Dwyer, publisher London: W. B. Whittingham, date **[1886]** (brackets preserved), no explicit rights field. Text: https://archive.org/stream/seatssaddlesbits00dwyerich/seatssaddlesbits00dwyerich_djvu.txt . It is a contemporary author advocating particular arrangements, not a universal engineering standard or evidence of a named Chicago turnout. Historical text is US public domain by age; no image-derived asset made here.

Printed **pp.260–261**, section *Training for Draught*, discussion of four-wheeled carriages with shafts:

> “whether it should be what is called a short or a long breeching, that is to say, whether it is to act directly on the shafts, or to be carried forward so as to act on the tugs, when it is called a long breeching.”

The following paragraph, p.261, explains that low front wheels and a relatively tall horse can incline the shafts, making short breeching act “downwards, not horizontally as it should”; the author states this makes the carriage less effectively held back.

**Use in this project:** choose and declare either a short/direct-to-shaft or long/to-tug breeching graph. A rear strap ending at a decorative unconnected ring does not implement either. Trace ends and breeching ends are different connection roles; joining them all to one generic vehicle point hides an actual historical distinction. The shaft-loop position and clearance matter, not just global root distance. Source text does not specify this project's desired numeric clearance, its current 45 mm gap tolerance, or one universal breeching height. Those remain fitted reconstruction/engineering choices to verify against the selected vehicle and actual anatomy.

Dwyer **pp.224–225**, *The Angle of Traction, Etc.*, discusses tilted shafts and short versus long traces changing the direction of pull and potentially moving the collar upward. The author refers to Fig.17; that figure remains **unseen**, and no geometry is extracted from it. **Use:** coupled tests should vary horse height, vehicle front/shaft height and trace length together. Testing a single default root transform and wheel size is insufficient to qualify adjustable parameters. Do not present the author's health/comfort opinions as veterinary advice.

## Shaft tugs are physical folded leather loops, not merely sockets

**Paul N. Hasluck, editor, *Harness Making***, Philadelphia: D. McKay, **1904**, IA `harnessmaking01hasl`, LoC contributor. Text actually read: https://archive.org/stream/harnessmaking01hasl/harnessmaking01hasl_djvu.txt . Existing metadata has no explicit rights declaration. Reasoned US public-domain basis is US publication 1904; this is our assessment, not a LoC grant. Workshop context is British; no Chicago-specific adoption is established.

Printed **p.151**, section *Van and Cab Harness*; text itself points to **Fig.191, p.147**:

> “The shaft tugs … are made by cutting a … length of leather to the same width as the buckles and back-band … Overlap this piece … the overlap then being bent together and knocked flat in the centre. Through both leathers cut a hole for a buckle in the bend …”

The text continues with thinning/creasing/stitching, a brass or nickel loop, and buckle adjustment. OCR fractional lengths/widths are corrupted (`1 ft. 71 in.`, `1| in.`, `4^ in.`); **all are withheld**, not silently normalized. The seven-per-inch stitching phrase is readable but is still OCR, not a page-verified measurement.

Printed **p.153** (adjacent preceding/following page headers establish this location), same section:

> “The big loops for a shaft and the hame tugs, etc., must always be made of firm loop leather, which will grow hard in finishing and retain its firmness and shape in spite of rain and weather.”

**Use:** original loop geometry should have finite cross-sectional thickness, a returned/overlapped strap path and independently modeled buckle/metal loop when the chosen recipe includes them. A thin open arc located 45 mm away from a shaft is a fixture marker, not demonstrated shaft support. Loop firmness is text-supported; a perfect rigid torus, exact loop dimensions and resulting collision clearance are not. The primary text is van/cab construction, so it supports topology/material construction as a comparator; do not relabel it the exact Moore No.1 light buggy fitting.

## Breeching assembly has bearer, hip-strap and shaft-strap structure

Hasluck **pp.148–150**, text around Fig.189 (figure unseen), describes making the breeching body, rings/dees, bearers and hip-strap. It says to place the two bearers at openings left near the ends and to fit leather into the hollow square in the breeching dees. The matching hip-strap is slit at its ends to suit bearer buckles.

Printed **p.149**, continuing to p.150:

> “The breeching straps to go round the shafts …”

It then describes turned ends, buckle preparation, strong loops, including one in reverse position to turn under the strap. Fractional widths are OCR-damaged and not adopted.

**Use:** trace, breeching/body strap, hip support/bearer, and wrap-around shaft strap are separate named geometry/constraint roles. A practical next fit should show shaft encirclement/retention and support points on both sides, not only a rear belt around the rump. The loop/buckle detail can be reconstructed from text at declared dimensions, but should remain open for actual figure review. Source construction lengths are cut-stock dimensions and would not automatically be the final assembled world-space path even if the OCR were perfect.

Hasluck **p.156**, Fig.197 caption/key (figure unseen), separately identifies `I trace`, `J saddle`, `K shaft tug`, `N tug strap`, `O bearer`, `P breeching`, and `R shaft strap`. This supplies explicit distinct roles for a semantic attachment schema. It does not establish their visible arrangement from a picture or justify importing hansom dimensions into the first light harness. Text states hansom/four-wheeler harness is heavier than gig harness except at the saddle.

## Breastcollar remains an attested option, but position must be bounded honestly

**John Moore, *Fine harness, saddlery & horse clothing***, New York, **1891**, IA `fineharnesssaddl1891john`. Text reread: https://archive.org/stream/fineharnesssaddl1891john/fineharnesssaddl1891john_djvu.txt . Printed **p.1**, *Buggy Harness*, No.1, explicitly lists folded/stitched **breast collar, breeching and girth**, straight stitched **1-inch traces**, flat reins and a bridle with round check rein. Printed **p.4**, *Track or Single Leather Harness*, No.5, separately lists breast collar, breeching, belly band and traces of heavy single leather. This demonstrates availability of breastcollar configurations in a US commercial catalog; it does not prove exact shape/height or specific Chicago ownership.

Printed **p.8** Village Cart No.52 identifies Tilbury tugs; following cart passage says regular cart or Tilbury **shaft tugs**. That is a different configuration in the catalog. Do not attach Tilbury hardware to Moore No.1 and mark it text-attested to that item: such a choice is at most a stated reconstruction/comparator until more direct evidence is obtained.

Dwyer **pp.217–218**, *Draught and Harness*, criticizes breast harness and trace attachment near the movable shoulder joint. This **disagrees in attitude** with simply treating the commercially sold breastcollar as an ideal general solution. Preserve the distinction: Moore attests a product; Dwyer argues about mechanical effectiveness. Neither refutes the other's existence claim. Do not erase the breastcollar from a historical library merely because an author dislikes it, and do not use a catalog listing to certify anatomical pressure or suitability. A fit study should locate actual moving shoulder anatomy and inspect forelimb sweep versus strap clearance; the text provides no numeric safe zone and this project has no veterinary fit certification.

## Gait and anatomy evidence relevant to moving harness

**J. D. B. Stillman, *The Horse in Motion***, Boston, **1882**, IA `horseinmotionass00stil`; existing acquisition report gives full imprint/rights rationale. Text reread at https://archive.org/stream/horseinmotionass00stil/horseinmotionass00stil_djvu.txt . Chapter VI begins printed **p.105** and covers trot/walk distinctions; contents identifies **Plate X at p.48** as showing automatic action of hock/stifle, **Plate LIV Horse Hauling** and **LV Irregular Hauling** at p.114, and gait plates LVII–CV. These are exact retrieval leads, not images viewed.

A muscle discussion describes a trotting wheel horse's torso and alternating diagonal legs; source page OCR at the immediate header is damaged, so do not cite a fabricated precise page number for that passage. Printed pp.52–53 discusses load-related fetlock/pastern response. **Use:** harness contact points tied to torso/head/neck must be sampled over the actual movement cycle, not a neutral standing pose only. Traces, shaft tugs, shoulder/breast region, rein endpoints and breeching supports require independent motion/clearance observations; a passing sole-drift check does not validate them. No source-derived stride frequency, torso amplitude or tension curve was measured by this pass.

## Concrete next fit checks informed by this reading

1. Declare short-to-shaft or long-to-tug breeching graph in metadata; test actual named endpoints and retention geometry separately from pull traces.
2. Inspect the 45 mm loop/shaft gap with transformed mesh vertices and a chosen reconstructed clearance target; demonstrate shaft passage/retention and both sides over the gait, not coincident socket points only.
3. Separate tug loop, tug strap, bearer/hip strap, shaft strap, trace and breeching mesh/attachment roles. Keep mechanism-specific local frames explicit.
4. Parameter sweep horse height, shaft height/angle and trace length. Report when an assembly no longer fits instead of scaling or translating the whole horse silently.
5. Render close shoulder sweep, loop cross-section/buckle, rump breeching and head/rein views; retain collision/pressure/tension as unpassed until measured. Production visual matching still awaits source images.

No ticket is closed by this report. No numeric OCR-corrupted fitting dimension, unseen figure shape, animal-health claim or named-horse attribution has been promoted to fact.
