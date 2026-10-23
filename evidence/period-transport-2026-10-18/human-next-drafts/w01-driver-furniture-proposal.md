# W01 removable driver furniture — engineering proposal

Not implemented. Not an attested Chicago1835 wagon accessory. No source photograph
has been identified in the reviewed collection that proves this particular bench.
T2793 permits bounded reconstruction, but its construction-reference/photographic
acceptance remains open. This proposal makes the physical support explicit instead
of treating `vehicle_seat_driver` as a real seat.

Actual current W01 generator:

- Body3.05m long×1.07m wide, BED.95m, sides.55m.
- Floor planks centerY.915/thickness.07 => floorTOP.95m.
- Top rails centerY1.51/thickness.04 => railTOP1.53m.
- Empty driver socket(0,1.15,1.10) is inside the box; no supporting bench exists.
  It is unsuitable as a physical seated-driver acceptance target.

Proposed detachable cross-plank bench mounted across the existing upper rails,
near the front but with space ahead for the feet:

|Part|Proposed glTF dimensions/position|Tier and mechanical reason|
|---|---|---|
|Seat plank|1.18m wide×.05m thick×.30m fore/aft, center(0,1.555,.65), top1.58|Reconstructed independent joinery study. Spans the1.07m box and bears on both rails; not floating over the box.|
|Underside retaining cleats|Two .045m square timber cleats at the two side-rail bearings; actual fit derived from rail positions, no wheel/steer intrusion|Reconstructed means of limiting lateral/fore-aft movement. Do not claim historically documented hardware.|
|Retention|Two visible removable iron clamps or through-bolt fastenings to reinforced bearing blocks, chosen after construction review|Reconstructed safety/mechanical detail; avoid modern spring-seat brackets or hidden unsupported strength claim.|
|Footrest platform|.85m wide×.04m thick×.30m fore/aft, center(0,1.10,1.27), top1.12|Reconstructed. Its z1.12..1.42 stays inside front wallz1.525 and width inside box; seat/footrest height difference.46m.|
|Footrest supports|Timber blocks/brackets down to floorTOP.95, no attachment to rotating front gear|Reconstructed explicit load path. Shape must be designed/checked; no thin plane floating in air.|
|Driver socket|Move to physical seatTOP(0,1.58,.65) for selected bench-equipped variant only|Engineering attachment datum, not anatomy or attested seating position. Pelvis registration depends on actual body/seat contact.|

Furniture is an opt-in variant; do not change all80 parked static wagons or imply
every farm wagon carried this bench. Preserve non-driver wagons and the baseline
empty-socket semantics until this variant exists. A removable plank/cleat treatment
is a **proposed period-compatible reconstruction**, not a reference-backed finding.

Evidence bounds: existing wagon body/rail dimensions constrain span/placement;
mechanical fit constrains bearings and load paths; generic adult thigh/shin lengths
constrain seat/footrest difference. None supplies a historical bench dimension.
The1893 manufacturer catalog and1875/1904 manuals read so far do not establish
1835 bench details. Rights-pending retrospective wagon illustrations may be discussed
but must not be traced/derived into this furniture. Seek a cleared earlier wagon
construction source/depiction and retain this reconstruction grade in the meantime.

Before acceptance: actualmesh seat/cleat/rail contacts; thigh/foot fit on actualbody;
skin/clothing penetration at seat and knees; foot soles fully supported; leg/board
clearance inside front box; hands/reins reachable; unchanged front-gear sweep and
boarding clearance; near/side renders. Driver clothing must be1835eligible. C01
numeric instrument stays1904engineering-only; a1835worker is not a1904coachman.

The current C01 solver remains a numeric instrument only. Do not deploy it as an
1835 seated driver until actual W01 furniture and a matching profile are authored.
