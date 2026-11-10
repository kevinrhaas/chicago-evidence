### L45 — The garrison garden: a fence read from a drawing convention, and a planting not drawn
**Decision:** `fort_dearborn_garrison_garden` is built as a worm rail fence round a square of
about 77 m. The fence's **height, its courses, its panel length and its zigzag** are invented,
and the **planting inside it is documented and not built at all**.
**Why:** the 1830 Harrison plan draws this plot and labels it "Garden for the Garrison", and it
draws two of its sides as a continuous zigzag. A zigzag boundary on a period American survey is
the convention for a worm — snake — rail fence, so that is what is built; but the convention is
the reading and the sheet never says "fence", which is why `wall_kind` is `inferred` and every
dimension of the fence is `conjectural`. The planting is the opposite case and the sharper one:
Juliette Kinzie says the company gardens were *"well filled with currant-bushes and young
fruit-trees"*, which is `documented`, and **nothing of it is modelled**, because currant bushes
and fruit trees are flora and `data/flora/` has no cultivated zone and no garden species. So the
record carries a documented chip over an empty rectangle of ground.
**A guard belongs here too.** The garden usually quoted in accounts of this fort — *"The ground
on the south side was enclosed and cultivated as a garden"* — is from a passage that ends *"Such
was the old Fort previous to 1812"*. It is the FIRST fort's garden and this record does not rest
on it.
**Consequence:** the reservation reads as fenced, empty ground. The single most evocative
detail anyone recorded about this place — fruit trees in a garrison garden on the Chicago
prairie — is in the data and invisible in the model.
**How to resolve:** a cultivated-ground zone in `data/flora/`, which is a flora parcel rather
than a structure one; the species are already named by the source.
**Covers:** `fort_dearborn_garrison_garden.fence_1816.form.fence_height_m`, `fort_dearborn_garrison_garden.fence_1816.form.rail_courses`, `fort_dearborn_garrison_garden.fence_1816.form.panel_length_m`, `fort_dearborn_garrison_garden.fence_1816.form.panel_offset_m`, `fort_dearborn_garrison_garden.fence_1816.form.planting`.
**Recorded:** 2026-08-11.

