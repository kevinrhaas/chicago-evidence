---
id: T-2023
title: Seat the lodging remainder as lodging roofs rise: 7 West adults the book orders with no free bed, and 44 boarding-house and inn households waiting on roofs. T-1538's frozen top-up deals new roofs to them automatically
state: done
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-10-03
closed: 2026-11-10
pr: 1920
claimed_by: Chicago lodging reconciliation 2026-11-10 11/10/2026, 5:21:24 AM CT
blocked_on: null
needs_bake: false
closed_at: 2026-11-10T14:54:40Z
claimed_run: null
claimed_at: 2026-11-10T11:21:26.821Z
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


## Progress checkpoint 2026-11-10 — current debt and division-safe payments

PR [chicago#1920](https://github.com/kevinrhaas/chicago/pull/1920), source `195c2f761a`, separates the carried adult allocation from the live order. Its seven unspent West slots are historical residue; the current book orders zero West adults. Staffing payment now requires the same committed civil division as the premises and refuses a missing/conflicting division. Official lodger/staff checks and self-tests, unchanged housing derivation, and actual write-isolation checks pass. This checkpoint adds no people and moves no resident or housing assignment.

A separate candidate for three already-ordered South youths is deliberately held outside the public delivery: the old greedy housing pass would move 1,028 existing assignments and strand a ruled-in resident. Current lodger-only bed accounting omits occupants placed by the housing overlay, so apparent empty beds are not accepted as whole-roof capacity. The completion work preserves all existing assignments, audits already-standing residential quarters, and reconciles actual household membership units instead of treating each container card as one household.

The live work still belongs here: 13 people and 34 lodging-household units remain before the candidate is safely applied. No new historical people, roofs, follow-up tickets, lifecycle override or completion is claimed by this checkpoint.


## Public checkpoint 2026-11-10 — actual person and household debt reaches zero

Source commit `dd8e0f59f3` is pushed to [chicago#1920](https://github.com/kevinrhaas/chicago/pull/1920). The derivation seats all thirteen already-ordered reconstructed residents and two existing North adults, and reconciles the missing thirty-four household-unit receipts through explicit disjoint shared economies. The live person and household debts are both zero. All 157 original person JSON records, 52 earlier layer seats and 1,807 accepted housing/roof pairs remain exact. The actual 56 reconstructed plus 20 known units have 368 disjoint sleeping member IDs; the global 165 known-house crosswalk reserves each household once and excludes T-2193/T-1174 household members.

Six already-standing vacant upper residences correct dwelling stock from 415 to 421 with the census ratio unchanged at 8.204; final housing is 3,452 people, under the 3,453 ceiling. One explicitly exceptional West youth night stays within the unchanged full capacity. Nine secondary boarding uses, supplementary anonymous kin, source-size bounds and two single-person official known-house receipts are expressly reconstructed, without new historical attestation. Seven pre-existing whole-roof capacity excesses remain disclosed and receive no new admissions. Source checks and substantive negative guards pass; protected full CI and published walkthrough review remain. The ticket stays claimed until those finish and the PR actually merges.


## Integrated public source checkpoint 2026-11-10

PR1920 now points at `2ea44eff141ed62a88286ea5d331ca648ac587be`, normally merged with actual dev after Brick PR1918 (`0d64b936`). All source work and generated owner refreshes are pushed. The independent verification receipt is committed at `chicago/4d/docs/measurements/t2023_lodging_completion.json`: original157 person records,52 prior seats and1,807 accepted housing roofs exact; thirteen ordered R people and two existing-person seats appended; live person and household debt both zero;56 R economies plus20 known receipts,368 disjoint members and165 exclusive global known-house receipts.

Current lodging, housing, population profile,658-door entrance derivation, public sidecars, source backlinks, staffing/re-family/employment checks and closure liveness pass. The final published mirror and closing-convergence report are being produced in the full integration checkout, followed by actual desktop/phone review and protected full CI. The source worktree is clean; the ticket remains in flight until the actual reviewed merge. Historical partition counts are labeled as snapshots, and the seven older lodging-roof capacity excesses remain explicitly unchanged.

**Completed 2026-11-10:** [PR #1920](https://github.com/kevinrhaas/chicago/pull/1920) merged to dev at 2026-11-10T14:54:40Z, squash `115f62fa85227236eb90fb5a4196cd861148819b`, from qualified source `997203a6ad5a2392520f043aeebbd815fe18a449`. The live lodging remainder is resolved: person debt 0 and household-unit debt 0. Thirteen reconstructed people and two existing adults are seated; 56 reconstructed and 20 known unit receipts account for 368 disjoint members and 165 exclusive known receipts. Original 157 person records, 52 seats and 1,807 housing assignments remain exact. The seven disclosed older crowding excesses remain outside this resolved remainder.

[Durable qualification and exact public readback](https://github.com/kevinrhaas/chicago-evidence/tree/a95257b2a9e43ca621ee96569ebe7772d9a6176c/2026-11-10/T-2023-lodging-completion-999209fffb) preserves actual desktop and 390-pixel phone cards, six paid cells, corrected reconstructed identity labels for all thirteen new people, the original data invariants and native freshness proof. Final source parts 1–8, aggregate and report passed. The final documentation-only child restores canonical reference links without changing the accepted app tree. Official normal done/settle records the actual merge instant, without an override.
