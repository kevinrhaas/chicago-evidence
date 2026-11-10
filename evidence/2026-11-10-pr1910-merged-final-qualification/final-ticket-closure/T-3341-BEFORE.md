---
id: T-3341
title: Give every 1812 and 1835 brick wall and chimney real brick: the 1835 library's local clay brick, lime mortar sheet, shuffled per brick
state: open
epic: TOWN
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-11-02
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: null
decision: null
decision_answer: null
---

Give every 1812 and 1835 brick wall and chimney real brick: the 1835 library's local clay brick, lime mortar sheet, shuffled per brick.

Owner, 2026-11-03 (thread "Add bird's-eye fort view to sources", decision card): yes, one ticket for 1812 and 1835 brick. His words on the fort: "I saw a red structure that has a face that does not look like a real surface ... we make some nice bricks in 1904 that maybe the technique could be used for those chimneys if they are brick"; then: "if you have evidence of clay chimneys or that is more historic likely of course keep them as clay chimneys and make the texture surface appear correct for those".

**What is wrong now.** Every 1812/1835 GLB material named `brick`, `chimney`, `draft_brick` or `k13_brick` is a flat colour (0.45/0.23/0.17) with no texture and no relief, while log walls and shingle roofs bind real maps (wall-relief.js, roof-relief.js). The first fort's magazine (brick, attested: Quaife 1913, "a small structure made of brick") and the ranges' ridge stacks read as painted boxes.

**What each stack is made of — follow docs/RESEARCH/chimneys.md, don't re-decide it.** It already rules: a stack that rises INSIDE the wall / through the ridge of a timber roof is masonry, brick (inferred, §2); a stack built OUTSIDE a log cabin's gable is stick-and-clay (reconstructed, §3). The first fort's ranges carry ridge stacks (Whistler 1808's folded elevations; the Currey 1912 bird's-eye draws them on the ridges), so they are interior masonry → brick, unless a source found during this ticket says otherwise (the magazine proves brick was at the post by 1812). Log-cabin gable stacks keep stick-and-clay and get the clay daub surface. Record any change of a stack's material in its record with its source, or as a liberty.

**The surfaces exist already:** assets/textures/chicago_1835_pbr/masonry/chicago_clay_brick_lime_mortar (handmade local clay brick, lime mortar — the period's brick, not 1904 pressed) and masonry/cat_and_clay_chimney. Neither is shipped (tools/web_textures.py SHIPPED). Bind them by material name in the renderer, with the per-brick shuffle and shade from renderers/web/js/brick-bond.js (T-3295) so a wall or stack never tiles, without a rebake if the material names suffice.

**Acceptance:** the first fort's magazine and every brick wall and chimney in 1812 and 1835 shows a real brick surface (mortar joints, per-brick variation, relief) and every stick-and-clay stack a clay daub surface; no 1904 material changes; boot payload and phone memory (1812, 1835 mobile) stay under their ceilings; desktop and 390x780 before/after shots of the magazine, a range's ridge stack and an 1835 brick building and cabin stack in the PR; no page errors.
