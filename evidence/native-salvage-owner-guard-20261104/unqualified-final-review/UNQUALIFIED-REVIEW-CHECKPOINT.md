# UNQUALIFIED review checkpoint — platform targeted salvage owner guard

Existing PR219, base b37fdeca6b74d8e3c70945a75687140c0718f549. No feature push, workflow dispatch, main merge or activation.

Parent-approved core candidate adds archive-only salvage for owner-targeted Chicago contexts, immutable run-ID/full-SHA UNQUALIFIED refs, alternate-index dirty snapshots, exact remote verification, and success-only journal parsing. Final bounded delta preserves actual private HEAD if rev-list/count fails, while retaining generic prior behavior.

All 11 actual ci.yml commands pass. Salvage has 50 real-Git checks, including the new failed-count shim. Original CPU2/nice19 GHREST run's 84pass/2fail one-second last-poll timing failure remains in CI-03.log; one approved CPU3 normal-priority retry passed all86 unchanged assertions in19.4s. Other commands passed on CPU2/nice19.

Official unmodified smoke passed all15 checks at1280x800 and390x780 in18.34s. Native WebKit is unavailable and reported by the existing smoke runner. Every one of337 tracked source members matches FROZEN-CANDIDATE before/after all commands; no edits occurred after freeze.

This is a public recovery/review packet only. Root final delta/receipt review, existing-feature normal-FF push and both hosted CI results remain before activation.
