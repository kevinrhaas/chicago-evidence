---
id: T-3532
title: Recorded spatial audio pilot and music cue library
state: review
epic: META
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-11-09
closed: null
pr: 1912
claimed_by: run 11/9/2026, 10:15:10 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
claimed_at: 2026-11-10T04:15:12.433Z
decision: null
decision_answer: null
---

Recorded spatial audio pilot and music cue library.

**Acceptance:**
- Replace synthetic destination atmosphere with recorded water and wind, selected by the live terrain and season; opt-in sound remains silent and fetch-free by default.
- Integrate the seven owner-supplied music cues: Frontier=1812, Border=1835, Waltzes=1904. Stream only the selected era and support independent music volume. Owner confirmed usage/distribution rights in chat on 2026-11-10; generated-music provenance is explicit.
- Catalog source/license/derivative metadata; retain originals outside the published payload and show credits in the app.
- Verify lifecycle, mute, hidden-tab, scene changes, browser decoding and payload size. Report unverified listening quality and deferred moving-source/voice work honestly.
- No production promotion.

**Released 2026-11-09** (claim of run 11/9/2026, 9:14:52 PM CT): Audio/R2 implementation is retained uncommitted on audio/recorded-soundscape in /workspace/chicago. All 40 hosted objects verified; real published arrival playback and mute pass at 390px and 1280px; generated app is 431.363 MiB within 432 MiB. Source gate part 1 failed Node24 geometry checks and the audio liberty format; Node22 and compiled liberties now pass targeted checks, but all four parts must still run. Published mobile smoke stage 13 stops before audio on the Hogan card expecting building navigation where the current UI offers disabled Find this person (52 pass, 2 fail, zero page errors). Do not weaken assertions or claim release; see docs/STATUS.md and docs/AUDIO-HOSTING.md. No PR, merge or production deployment.
