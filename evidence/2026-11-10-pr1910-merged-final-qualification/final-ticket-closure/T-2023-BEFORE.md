---
id: T-2023
title: Seat the lodging remainder as lodging roofs rise: 7 West adults the book orders with no free bed, and 44 boarding-house and inn households waiting on roofs. T-1538's frozen top-up deals new roofs to them automatically
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-10-03
closed: null
pr: null
claimed_by: run 10/8/2026, 12:37:12 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/37817443904
claimed_at: 2026-10-08T17:37:12.195Z
decision: null
decision_answer: null
---

Seat the lodging remainder as lodging roofs rise: 7 West adults the book orders with no free bed, and 44 boarding-house and inn households waiting on roofs. T-1538's frozen top-up deals new roofs to them automatically.

## FILED OVER THE BUDGET, AND HERE IS THE REASON

The ticket budget refused this: the queue stands at 213 lines, at or over its ceiling of 140. It was filed anyway, on this reason:

> closing T-1538 strands the book's lodging rows (gate: closing this branch's tickets strands nobody); they need a live owner in the same PR

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

## Filed by T-1538 (PR #340, 2026-10-03)

**What is left, measured on the build that closed T-1538** (`1835_lodgers_seated.json` → `quota_basis.top_up.what_is_left`):

- **7 West adults ordered with no free bed**: male 20-29 ×2, 30-39 ×2, 40-49 ×1, 50+ ×1, and female 40-49 ×1, all `lodging/none`. They are already in the top-up's FROZEN room. A West lodging roof raised later is dealt to them automatically, last in the house order, so nobody already standing moves. This needs no new machinery, only the roof (T-1209) and a `seat_lodgers_1835.py --build`.
- **44 lodging households** (boarding_house + inn_tavern; the book orders 66 and the stage fills 22). These also wait on roofs.
- **29 ordinary-night beds with no order**: 13 North (Kelsey's 4, Chapin's H3 6, the Steamboat 3) and 16 South (the Dearborn and Market H3 houses). No adult `lodging/none` order is open in those divisions, so nobody is minted into them. Either the lodging model over-apportions beds in those divisions or the book under-orders them. Reconcile the two before minting.
- **The housing deal moves on every resident mint.** One more lodger took one place under the town-wide ceiling, so `hh_pennington_sack_f` (presence `ruled_in`, last in the line) now waits on a roof. The greedy least-crowded pass also re-shuffled about 367 boarded seats. An invented boarder outranking a named ruled-in household for a roof may be backwards (L252: documented people displace invented ones). It is worth a ruling.

## Carried here from T-1532 (2026-10-03): the staffing mint's DIVISION axis is still unpriced

T-1532 dealt the book's last `lodging/trade` order (four South youths, PR #343). It had
absorbed **T-1566** in the 2026-10-03 queue cleanup, and **T-1566's piece was NOT done
there**. `tools/staffing_mint_order_1835.py` still pays a hand from the first bucket by
key, whatever division its house stands in, so a north lodging slot can pay for a hand
in a south shop. It was not worth a run on its own: the mint pays **0** slots today, and
pricing the axis mints nobody. It rides with this ticket, because it becomes live the
moment the lodging roofs rise and the purse can pay again. T-1532's file keeps the
reading: 7 of 26 hands are derivable (5 `premises` and 2 `street_only` on
`south_water`), and 19 are not. Five of those 19 are out of town (Flag Creek and
Naper's Settlement), where "elsewhere" is the honest word rather than "unplaceable".

## RE-MEASURED 2026-10-08 (slice 5/5): nothing here can be seated yet, and the visible half is blocked on T-1953

Read on `dev` at 74d9f3949. `seat_lodgers_1835.py --check` is green, so the stage already
matches the roofs that stand: 27 built lodging places, 243 ordinary-night beds, 224 slept in.
From `1835_lodgers_seated.json` → `quota_basis.top_up.what_is_left`:

- **The 7 West adults are still ordered with no bed** (`ordered_with_no_bed`: south 0,
  north 0, west 7). Seating them needs a West lodging roof, and the only ticket that raises
  one is **T-1953** (the West's three H3 boarding houses), which is `blocked-tech` on
  T-1414: no platted West block's plan carries an H3, and the programme schedules the
  West's H3s only on ground beyond committed control. Nothing else in the queue puts a
  lodging roof in the West. When T-1953 lands, the top-up deals those roofs to these
  seven automatically and `seat_lodgers_1835.py --build` is the whole job.
- **The beds with no order are 24 now, not 29**: north 19 and south 5 (`beds_with_no_order`).
  Reconciling them is still owed before anybody is minted into them, and it is still
  invisible work. It rides with the West roof or with T-1957's South houses.
- **`hh_pennington_sack_f` HAS A ROOF.** `1835_housing_seats.json` boards it in
  `recon_1835_south_d6_012` (rung `boarder`, "boarding in the division's least crowded
  dwelling"), so the ruled-in household no longer waits behind invented boarders. That
  item is settled and needs no ruling.
- **The staffing mint's division axis has nothing to price.** `1835_staffing_mint_order.json`
  → `what_the_book_can_pay.slots_outstanding` is **0**: T-1532 dealt the last
  `lodging/trade` order, so the purse is empty and `mintable_today` is 0. Pricing the axis
  now changes no figure and nothing a visitor sees (AGENTS.md § THE VISIBLE-PROGRESS RULE,
  no exemption applies). It becomes live only when new lodging roofs reopen the purse.

**So it is blocked, not finished**: every remaining piece waits on a West roof (T-1953 →
T-1414) or on T-1957's South houses. Don't claim it to re-check; re-check when T-1953 merges.

## RE-POINTED 2026-10-10 (slice 7/7): T-1953 is withdrawn, and the West half is a stale figure, not a missing roof

T-1953 read the book on `dev` at b281f6d9b and withdrew: `structures/larger_boarding_houses/west`
is 6 of 6 (T-2148 raised `recon_1835_blk_washington_clinton_h3_02` and two H-family houses on
2026-10-06) and the roof programme leaves the West 0 roofs. **Nothing in the queue will raise a
West lodging roof, and nothing needs to**:

- The "7 West adults ordered with no bed" is the top-up's FROZEN room, carried from the build
  that recorded it. In the live book every one of those cells now reads `filled` =
  `to_reconstruct` (male 20-29 8/8, 30-39 5/5, 40-49 1/1, 50+ 1/1; female 40-49 1/1).
  `quota_basis.re_cut_since` already shows male 20-29 West cut from 12 to 8.
- So the West piece of this ticket is a reporting fix, not a roof: `top_up()` in
  `tools/seat_lodgers_1835.py` counts `what_is_left.ordered_with_no_bed` from the frozen
  `to_top_up` rows and never nets them against the live book. It should report what the
  live book still owes (0 West adults today), or say beside the 7 that the book has since
  re-cut them away. That is invisible work; it rides with the bed reconciliation below.
- Still owed here, measured on the same tree: `beds_with_no_order` south 16, north 20, west 0
  (36 in all); `houses_still_ordered_after_this_stage_s_counter` 34. The remaining West youth
  cells are `persons/female/under_10/west/lodging/none` (4 of 8) and
  `persons/male/10_19/west/lodging/none` (5 of 6).

Unblocked, since its only blocker is gone.
