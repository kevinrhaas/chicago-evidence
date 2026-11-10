---
id: T-2484
title: 1812: build the Kinzie house, the former Point du Sable house on the north bank opposite the fort, with its piazza, fenced green, Lombardy poplars and two cottonwoods, matched to its pictures
state: open
epic: SOUTH_TIME
requested_by: owner
seen: true
effort: M
legacy_id: null
parent: null
opened: 2026-10-13
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

1812: build the Kinzie house, the former Point du Sable house on the north bank opposite the fort, with its piazza, fenced green, Lombardy poplars and two cottonwoods, matched to its pictures.

## The owner's ask (2026-10-13, project thread "1812 structures")

> For 1812 did I ask you to build the other buildings from that era the kinzie former dusable estate, ouillmettes house, there are certainly other structures in 1812, the Lee house etc. all known structures from history

Until now the 1812 scene has drawn only the first Fort Dearborn and its outer buildings (the 14 `first_fort_dearborn_*` and 7 `first_fort_outer_*` records, from Whistler's 1808 draught: T-2049, T-2062). No settler's house stands. The inventory this ticket comes from is the thread's reply; the settlement the histories put across and around the fort in 1803-1812 is the Kinzie house (the former Point du Sable house) and its establishment, Ouilmette's and Pettell's houses behind it, the Burns house up the north bank, the Lee family's house on the lake shore, and Lee's Place (Hardscrabble) on the South Branch.

## How it is built (applies to every 1812 settlement ticket)

- **Dated so it resolves in 1812 and not in 1835.** Each record's `documented_range` covers the 1812 scene date (1 August 1812 until T-2490 moves it to 14 August, owner 2026-10-13: cover both) and closes before 1835-07-01. `data/exclusions.json` already rules `kinzie_house` and `ouilmette_cabin` gone by 1835: keep those entries, and have the new records' closing dates agree with them. `tools/read_whistler_1808.py --check` and the scene-date checks must stay green.
- **Never invent a source** (AGENTS.md rule 1). Every `source_id` resolves in `data/sources/`. Sources this ticket needs that are not yet records get one first, with tier and `rights_status`: J. Seymour Currey, *The Story of Old Fort Dearborn* (1912, Project Gutenberg 52346); Joseph Kirkland, *The Chicago Massacre of 1812* (1893, Gutenberg 59624, catalogued at `chicago/reference/chicago-massacre-1812.yaml`); Benson J. Lossing, *Pictorial Field-Book of the War of 1812* (1869). Where a source cannot be reached from the run's container, say so in the ticket rather than citing it from memory.
- **The image gate** (AGENTS.md rule 11, `data/reference_views/README.md`): every picture of the building is read off the picture itself, its camera solved into `data/reference_views/<structure_id>/`, rendered with `node tools/photo_match.mjs`, and worked until it matches. Pictures are tier 5: form only, never a coordinate. Most are retrospective (1857-1912) or show a later year (1820, 1832); each is evidence of its own date, and the match record says which picture governs where they disagree.
- **What no source gives is a numbered liberty** in `docs/LIBERTIES.md` and `data/liberties.json` (check dev and open PRs for the next free number before merging), carried on the attribute as `reconstructed`.
- **No human figure is drawn** (standing constraint). Cards that name Native or Métis people carry `review_required` and `touches_removal` with their own sentence. The 1812 scene is already held for that review (T-0472) and stays unreleased.
- Gate (`tools/check.sh`), smoke by parts, desktop and 390x780 shots with no page errors, and a `changelog.d/<ticket>.json` entry.

## What to build

`kinzie_house_1812` (id at the builder's choice, but not `kinzie_house`, which is the 1835 exclusion's id): the log house Jean Baptiste Point du Sable built on the north bank of the river directly facing the fort, held after him by Le Mai, bought by John Kinzie in 1803 or 1804, and standing (not burned) in August 1812. The card names du Sable as its builder, the first non-Native settler at Chicago and a Black man, and dates Kinzie's ownership.

What the record says about it:
- "On the northern bank of the river, directly facing the fort, was the family mansion of my husband. It was a long, low building, with a piazza extending along its front, a range of four or five rooms. A broad green space was inclosed between it and the river, and shaded by a row of Lombardy poplars. Two immense cottonwood-trees stood in the rear of the building" (`kinzie_waubun_1856`, ch. XVII; describes 1831, so the 1812 house is inferred from it).
- "The house was of squared logs, after the fashion of the very best of the frontier mansions of that day" (`moses_kirkland_history_of_chicago_v1` p. 30, text lines 4953-4956); the 1803 view from its door across to the fort building (p. 36, lines 5610-5620).
- Currey 1912 ch. II: the house faced south with the river in front and the lake a short distance east; Kinzie "added a veranda, and planted four Lombardy poplars". Le Mai's and Kinzie's dates differ by source (Le Mai 1796 or 1797; Kinzie 1803 or 1804): record both.
- Du Sable's 1800 bill of sale to Jean La Lime gives the house as 22 by 40 feet (Quaife, "Property of Jean Baptiste Point Sable", *Mississippi Valley Historical Review* 15:1, June 1928, pp. 89-96). It is not in the corpus: add it as a source if a run can read it; otherwise the 22 x 40 ft footprint is cited to nothing and stays a liberty.
- Position: north bank opposite the fort, at the later foot of Pine Street (N. Michigan Avenue) at Kinzie Street, the site of Pioneer Court. The two cottonwoods are separately attested (exclusions `kinzie_house` detail); plant them as flora records scoped to 1812.

## Pictures (all of the house; read each one itself)

  picture: `chicago/reference/images/chicago/chicago_kinzie_house_fort_dearborn_1812.jpg` (Lossing 1869, house with poplars and fence, first fort across the river)
  picture: `chicago/reference/images/chicago/chicago_kinzie_house_1833.png` (Chicago Magazine 1857 / Andreas, "about 1833": piazza, picket-fenced green, four poplars)
  picture: `chicago/reference/images/chicago/chicago_kinzie_mansion_1832_and_1845_view.jpg` (Cram 1893 atlas plate, upper panel, "in 1832")
  picture: `chicago/reference/images/chicago/chicago_kinzie_house_1804.jpg` (Curt Teich postcard after a painting lent by John H. Kinzie)
  picture: `chicago/reference/images/chicago/chicago_settlement_1820_2.jpg` (Eastman after Schoolcraft, 1820: the Kinzie farmstead at right)
  picture: `chicago/reference/images/chicago/chicago_settlement_view_1820.jpg` (Gemmell lithograph of 1820; its colours are a later invention)
  not yet in the library: Currey 1912 "Residence of John Kinzie" (Sarony's lithograph of a sketch by Mrs. John H. Kinzie, the Wau-Bun plate) and Kirkland 1893 "Kinzie mansion in 1812" (p. 73). Bring them into the public image store with attribution if the run can reach them; if not, say so here and Kevin can upload them.

**Acceptance:** the house, its piazza, the fenced green to the river, the poplar row and the two cottonwoods stand in the 1812 scene and in no 1835 view; every reference view above has its camera, a side-by-side from the GLB in the tree and a match record at `matches` with nothing open; a camera anchor in `data/scenes/1812.json` looks at the house from the fort's side of the river; the card cites its sources and liberties. The PR carries the before/after side-by-sides.

## Image gate
- kinzie_house_1812

## Reopened (owner, 2026-10-28)

Owner, 2026-10-28: *"in looking at 1729 prairie, the pullman estate it seems like tickets are closed and the gate is exited, but it is still way off from a photographic match, the stepped front, the south face, the entire greenhouses and the stable are all way off, not to mention the greenhouse area south of 18th, am i wrong? did you consider it done? because its not and you need to reenter the photographic match on that one if not"*.

He chose, the same day, to reopen the other houses that had closed the same way ("Reopen them below Pullman").

This ticket closed without passing its image gate: `ticket.mjs split` closed it without asking the gate, and the pieces it minted carried no `## Image gate` section, so none of their `done`s asked it either (fixed by T-3235: a split parent's gate is now asked by its last piece). On 2026-10-28 its match records read:

- `kinzie_house_1812`: chicago_magazine_1857 differs, cram_1893 differs, eastman_1820 differs, gemmell_1820 differs, lossing_1869 differs, sarony_1912 differs, teich_postcard differs



It is reopened in place, not refiled. Read every picture itself, solve a camera for each one not yet solved, and work every view to `matches` under the T-3153 bar: an element missing or the wrong shape, a wrong count, a wrong material or colour, or a gap over about 0.3 m is `open`, never `within tolerance`. If it must be split again, its gate stays on it and the last piece closes it.
