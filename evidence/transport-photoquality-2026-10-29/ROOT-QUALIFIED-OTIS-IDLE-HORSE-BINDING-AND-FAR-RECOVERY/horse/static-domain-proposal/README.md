# Natural-idle binding repair: fixed source domain proposal

This is LIGHT source preparation only after the real 8ea seventeen-track trial
failed unchanged physical limits. No new weights, model, numerical pose, solver,
browser, GPU, application file or Git index is written by this proposal. The
frozen54-file H candidate and old14 implementation remain unchanged.

## Concrete failure and its source cause

The genuine native trial evaluated all65keys+64midpoints. Hoof drift8.6498um,
seam0 and leg lengths/links remained within their original limits. BODY skin
edges ranged0.0967-4.5543, areas0.0141-5.0613 and13 triangles flipped. HAIR skin
also exceeded edge/area limits. The strict physical failure correctly stopped
before any socket raw capture; no new posed/socket or scene acceptance exists.

The first failed BODY triangle1610 is on the LOWER JAW, not a walking limb:

|Vertex|Position y/z, metres|Accepted standing field|Original26 bind field|
|---|---|---|---|
|1300|1.1142/1.5016|100% BODY1|51.34% BODY1,48.66% HEAD3|
|1316|1.1174/1.4991|48.80% BODY1,51.20% HEAD3|48.80% BODY1,51.20% HEAD3|
|1233|1.1085/1.4909|100% BODY1|54.58% BODY1,45.42% HEAD3|

Read-only inspection of the actual saved PhaseA source explains the discontinuity.
Its old co-motion reduction explicitly maps joints2-5 into BODY1 for the standing/
gait solve, then freezes rows aboveY1.14 or with dominant neck/head/tail ownership.
The two lower-jaw rows below that plane and below50% head ownership collapsed into
BODY1; their51.2%-head neighbor was frozen. This was numerically harmless under
the original clip, where head/tail co-move with the body, and fails when they move
independently. It does not justify smaller head movement or a tolerance waiver.

All three vertices project to neck-to-head axis parameter1.59-1.61: well beyond
the skull pivot. The jaw, muzzle and skull must follow one rigid head controller
for a head look. They cannot retain an arbitrary height/dominance cut through the
jaw. No open-jaw/chewing or independent ears are proposed.

## References actually inspected

The source candidate's actual saved RAW profile was viewed, together with the
complete Ellenberger/Baum/Dittrich Tafel6 head plate and Joselodos' saved1920x1280
living-horse rendition. The plate shows the continuous skull/lower-jaw relation
and cervical transition; the living image shows a head turn and continuous neck,
not a calibrated motion range. Existing source records are
`ellenberger_baum_dittrich_equine_plates` (public-domain, represented edition
uncertain and disclosed) and `joselodos_2025_horse_anatomy` (CC0). Their existing
rights, source URLs, image hashes and use limits are preserved. No pixels are
copied, no exact dimension/movement is measured from them, and no historical
Chicago animal, coat, breed, owner or individual identity is invented.

## Fixed row domain before any binding export

`STATIC-DOMAIN-PROPOSAL-01.json` enumerates every eligible row, with source hash,
coordinates, existing palettes, component counts and full hoof-patch exclusion.
The masks are based on the unchanged source geometry and named landmarks, not on
an optimization over failed poses or accepted edge ratios:

- BODY head/neck:2913rows, y>1.04m and z>0.28m. This covers the whole skull/lower
  jaw and the fore-neck transition. Changes taper smoothly to exactly zero at
  the declared boundary. The surrounding rest torso/limbs stay exact outside it.
- HAIR forelock/mane:2306rows, the entire first source welded component, under
  the same source head/neck support. No mesh edit or new hair strands.
- BODY tail dock:78rows, abs(x)<0.22m,z<-0.78m,y>1.08m, with zero boundary delta.
- HAIR tail:969rows, exactly the isolated second source welded component already
  named in the original protection fixture. This permits its explicit new bind
  field rather than claiming the old static tail weights are moving-tail proof.

BODY is one connected5595row surface. The first jaw triangle cannot be repaired
as three arbitrary independent weights. EYE's3968rows remain100% HEAD3 and are
fully excluded. Every whole source-derived hoof patch179/179/30/24rows is excluded.
All2604 BODY rows outside the two BODY masks, every unlisted skin slot, all geometry,
normals, UVs/topology, images/materials, node rests, pivots, IBMs and old clips stay
byte-identical. Tiny influences outside the domain are never pruned. Inside the
head domain12rows have other limb-joint components: their positive components must
remain exact and the four-slot bound must be met without dropping any influence.

## Proposed anatomical field, not yet evaluated/exported

Redistribute only the existing mass on BODY1/NECK2/HEAD3 inside the head domain.
Use the existing reconstructed neck pivot[0,1.3,0.55] and head pivot[0,1.48,1.03]
as a centreline. The explicit skull core beyond neck-to-head parameter0.9 follows
HEAD3 rigidly; all three lower-jaw witnesses and the eye/socket region lie well
inside it. A smooth partition between adjacent body/neck then neck/head controls
provides the cervical transition. A C1 support taper, exactly zero on the fixed
mask boundary, blends into the untouched original torso field. This is anatomical
region authoring, not unconstrained/global weight smoothing or a numerical solver.
Any source seam/UV duplicates use one explicit shared canonical class value.

On the tail domain, redistribute only BODY1/TAILBASE4/TAILTIP5 mass along the actual
dock[0,1.28,-0.85] to tip[0,0.6,-1.1] centreline, with a body-to-dock root transition
and an adjacent dock-to-tip blend. The lateral flick and its4/8deg amplitudes stay
unchanged. The field must attach to these actual pivots, rather than inherit an
unproved old tail palette. C1 BODY support tapers preserve the rear torso outside
the declared dock. No new joint, pivot, IBM, geometry or hidden tail deletion.

The row lists are an upper bound, not permission to change every slot. The export
must record every actual changed tuple and reject unlisted changes. Preserve all
other positive joint components, exact source row correspondence, four influences,
finite nonnegative mass and loader normalization. A pure static audit must report
palettes/normalization and class consistency before a native motion run.

Use in-place replacement of ONLY reviewed JOINTS/WEIGHTS row bytes. Appending full
new skin streams would add roughly213kB and exceed the unchanged4MiB master cap;
it is unnecessary. All other BIN bytes remain exact. Version the recipe, change
notice, parent/candidate and companion-reference hashes explicitly. Do not overwrite
the original8ea/bd443/e49/925 assets or their old certificates/modes.

## New paired925 reference and qualification

The new candidate and a SEPARATELY VERSIONED companion derived from original925
receive the exact same reviewed binding tuples on the same semantic row IDs.
The companion retains original925 geometry, normals, UVs, images/materials, old
clip and provenance; it is explicitly a newly bound925 geometry reference, never
mislabelled unchanged original925. Derive the tuple overlay once from the reviewed
canonical source/row recipe and verify exact equality in both exports. No unlisted
source or geometry change, and no new geometry exemption.

The existing old925 source remains immutable input for ancestry, original face
maps and source topology. The production static/socket geometry predicates stay
unchanged. During capture the new companion follows the candidate's actual new
PRS, with identical rig/IBMs/bone matrices. This tests the same old versus new
eye-interface geometries under LIKE binding/motion. A static ancestor resting
head or the old known-bad weight field is not the dynamic reference for a corrected
skin. Keep original14/7mm bounds,178scan faces,20source interface faces, unchanged
source geometry provenance and zero-new-crossing rules.

The old5605 protected semantic-vector statement applies to the OLD field only.
New admission must explicitly version the reviewed changed-row domain; enforce
every original vector outside it, full foot/torso protection and exact paired
reference tuples. Do not rewrite old source constants, weaken old rejection tests,
retarget an old certificate or pretend the old field is still bit-identical.

Before new17 motion qualification, independently play the untouched original13
clip on OLD8ea and NEWskin through the genuine loader/Mixer at all65keys+64midpoints.
Require every position and shader-normal to remain within the existing1e-5m/0.01deg
native equivalence limits and original complete physical bounds. The original
clip's joints1-5 share a co-moving affine field, which makes this a defensible
invariant; it still needs actual native proof, not an assumed certificate.

Then run actual selected17 physical129 against independently composed expected
matrices, retaining the entire original9176B metric loop and every fixed edge,
area, normal, foot, link, seam, ground and loop limit. New-domain corruption controls
must reject changed feet/torso/outside rows, dropped tiny influences, bad palettes,
material/geometry changes and mismatched companion tuples. Only after that passes
capture genuine paired925 Float64 poses and apply unchanged production socket129.

Root review of this domain and proof plan precedes source intake, field export
or any new numerical run. Fresh canonical implementation pins and bounded resource
GO precede native execution. Real published1835 desktop/phone visible motion,
image/video review, owners/full gates and ordinary CI/DEV acceptance follow later.
No photographic, walking, rider/driver or interaction completion is claimed.
