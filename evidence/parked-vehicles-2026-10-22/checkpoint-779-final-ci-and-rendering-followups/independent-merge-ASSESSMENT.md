# PR1175 initial visible-person DEV assessment

I do not find a demonstrated asset/pose/source correctness regression in the inspected evidence that independently blocks an INITIAL DEV integration. I do find genuine unresolved local loader/readiness and extreme rendering-latency failures. They remain FAIL and cannot be labelled noise, fixed, hardware-safe or a passing focused-functional contract. The cause and contribution of the newly enabled human workload are unproven.

The current779978bce Full desktop visual receipt is PASS/CLOSED/source-unchanged with four captures and zero page/HTTP/request failures. Original Light mobile full is also PASS/CLOSED/source-unchanged, including all four actual production LOD loaders, ordinary AUTO farLOD3, contact/GL/budget assertions and four captures. Independently verified all eight PNG byte/hash records and identical39-path inputPins across both passes and all three failures. Main/humans/sharpness runtime code is unchanged from DEV142f, although new assets and an enabled actor can still affect cost.

The supplemental failures are real and distinct:

- Combined Full: four loaders finished by507.230s, far started515.458s, global540s killed the run. This is not a90s far-condition result.
- Separate Full warm far: actual requestedLOD3 remains pending at its90s deadline; no successful far snapshot.
- Balanced warm far: body/LOD3/pending=false is first observed305445.7ms, AFTER304932ms deadline, about514ms late. Late readiness cannot become an in-bound PASS.

All have zero recorded page/HTTP/request errors and unchanged source. Accepted visual-run normal-loop diagnostics are themselves roughly4.7s p95 Full and1.05s Light. This establishes an extremely slow local browser workload consistent with renderer/loader stress; it does not isolate a software/backend cause, establish no regression, or certify real-device performance. Treat the unresolved90s responsiveness as a documented follow-up, not a solved defect.

AGENTS requires check.sh/preflight, both published smoke viewports with zero page errors before merging, no weakened assertion, correct provenance and honest unfinished-quality status. DEV is expressly staging, not production. The visible-progress rule supports landing a visible person/card increment; photographic production acceptance and broader people tickets remain open. These supplemental outside-app focused callers are distinct from the named repository smoke gate; their unmet private focused flags are NOT qualified by this assessment.

My recommendation is conditional: root may accept the narrowly documented initial-person DEV scope once every required exact-head published smoke/normal CI/merge guard is actually green, while preserving all three failures and the performance/quality follow-up. Until actual collection is complete, no all-green or merge-ready claim is justified. The inspected CI owner still stated qualification_pass:false and CI-only scope; its final result and actual PR/base eligibility belong to root. No merge permission or action is supplied here.

Evidence/pins: EVIDENCE.json beside this file. Read-only receipt/source review only; no new tests/framework/browser/network/app/Git mutation.
