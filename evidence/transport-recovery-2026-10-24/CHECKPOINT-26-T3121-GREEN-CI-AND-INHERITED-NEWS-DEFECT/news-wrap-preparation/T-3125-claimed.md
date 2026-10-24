---
id: T-3125
title: Keep long release notes inside the Navigator at every text size
state: claimed
epic: RENDERING
requested_by: steward
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-10-24
closed: null
pr: null
claimed_by: Codex interactive news wrapping repair; isolated clone; real screenshot and all-row bounds preserved 10/24/2026, 12:11:37 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: 2026-10-24T17:11:38.087Z
decision: null
decision_answer: null
---

Keep long release notes inside the Navigator at every text size.

## FILED ABOVE BAND 9, BECAUSE IT BLOCKS

A follow-up goes to the foot of band 9 unless dev's gate is red on it or the build in hand cannot finish without it (owner, 2026-09-27). This one was placed above band 9 on this reason:

> Current published notes validation for T-3121 exposed visible clipping on mobile; its new layout check cannot honestly pass while the inherited news grid is wider than its panel.

**Observed failure:** a real published 33a99a notes view at 390 x 780 has a 292 px host but a 349.859 px implicit grid track. Entry text extends to x 424.859 while its Settings screen ends at x 381; the screen clips the visible title and prose. All 2,250 release rows rendered, with no page/HTTP errors. Long URLs in older entries are a plausible intrinsic-width trigger; the new release is not assumed to cause the inherited defect.

**Scope:** a CSS-only correction limited to the existing What's-new grids. Keep the feed content, typography, unread state, navigation, scene, and all other components intact. Never hide overflowing text, shrink the font, mask the failure or weaken its assertion to pass.

**Acceptance:**
- On the real published page at 390 x 780 and 1280 x 800, the complete news feed fits the visible Settings/news screen at 100% and 140% text size. Inspect every rendered row for horizontal overflow/clipping; retain the original layout predicates and screenshots. Long older URLs wrap while their complete text remains available.
- Preserve the six existing news-flow assertions: first-visit unread indicators, populated releases/items, title/date, clearing seen state, no first-visit new flags, and exact returning-visitor flags. Verify current newest content and the Settings/About entry route, with zero page/console/network errors and complete owned cleanup. Readiness waits use canonical semantics; a helper timeout is not misreported as a canonical assertion failure.
- Complete the normal full preflight and relevant published browser validation before source delivery; ordinary exact-head CI must pass. Keep any unchanged-source baseline reuse explicit. A focused news proof is not a fresh whole-part13/full-renderer result.

**Evidence:** external diagnostic2 packet at `/workspace/.cloud-setup/logs/transport-recovery/t3121-focused-current-notes-diagnostic2-attempt1-output/`, especially `mobile390x780-normal-news-layout-DIAGNOSTIC.json` and `mobile390x780-normal-news-layout-FAILURE.png`; durable checkpoint link will be added by the owning root run. No new render, CSS acceptance, source commit or PR exists yet.
