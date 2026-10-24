resume: corrected-source ordinary CI and published mobile/desktop renderer qualification are pending; keep draft during primary integration · waits on: nothing

T-3107 adds the Kimball house’s south-side HABS photograph, a provisional camera and two tall stacks in pale stone where one small brick stack stood. This is piece 1 of the T-3003 split. The front stack stays at 18.0 m under the earlier Taylor view’s phase ruling; the rear reaches about 20.1 m. Their detailed heads remain unfinished.

The photograph is a credited 1800 px derivative of HABS IL-1077 photograph 1, Harold Allen, June 1965. The source record, camera and match records retain their provenance and disagreement. The current comparison is **DIFFERS: 1 fixed, 12 open, 3 not shown**; the southwest cornice/camera residual is about 85 px. **T-1890’s full-building Image gate remains OPEN**, as do T-3108 (corner/camera), T-3109 (roof, openings and details) and T-3110 (east/rear). This PR does not establish a complete photographic match.

The recovery preserves accepted DEV `305dc4e0663faf16870c11dab2ed49beb1df3b15` and its workflow-only base advance. Native canonical owners restore all 751 accepted liberties exactly, add only `L-kimball-1801-south-stacks-3107` for a total of 752, and refresh the source-use coverage row from 746 to 752. The existing remote merge `024b8f9d` and liberties correction `732deddf` are preserved; the final correction changes only the coverage report. ROADMAP/FC, authored evidence, geometry and baked master/web bytes are unchanged by this recovery.

Validation on full source tree `c1ab86a710e378acb7ff891987b7e12617110708` (APP `754da58e88c034c0bb061ed0db7bb836ab32cda3`):

- Normal full preflight **PASS**: 1,065 steps, including 384 self-tests, plus changelog and ticket-ID questions; 657.099 seconds, return 0, no timeout, cleanup complete with 0 children remaining. All 16,976 tracked source entries match before and after. Reader dependencies were required with `C4D_GATE_REQUIRE_READERS=1`.
- Native `compile_liberties.py --check` and `compile_source_use.py --check` pass after their documented canonical regeneration. The intermediate source-use staleness failure is preserved. Changelog and ID questions pass again against the preserved `732deddf` ancestry.
- An earlier full202 attempt **FAILED** at step 24 while fetching a pinned IIIF map through the normal proxy. It changed no tracked source and never reached the liberties owner. This remains a failed attempt; the supported standalone stale-output repair and normal preflight are separate results.
- Fresh ordinary hosted CI on corrected head `a729a4e0dc39ec2b6c9236ac310387799433c0bc`: **PENDING**. The old `732deddf` hosted gate remains a historical failure, with no claim that its denied raw log proved a particular failing command.
- Published renderer qualification on this corrected source, at 390×780 and 1280×800 with zero page errors: **PENDING**. Earlier partial or other-source renderer results are not transferred to this head.

PR remains **DRAFT** until current-source CI, renderer qualification and base coordination are complete. No full-building completion, full202 pass, production promotion or merge readiness is claimed.
