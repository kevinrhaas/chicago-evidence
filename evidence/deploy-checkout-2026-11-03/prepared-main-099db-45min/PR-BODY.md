The main Pages deploy exhausted four240-second checkout materializations in run41706449525 and never reached publication. A separate actual full-worktree checkout completed in15m58s, so rerunning the same four-minute cap is insufficient evidence of a repair.

Scope the existing clone inputs at only the Deploy checkout step to1200seconds and two attempts, with a45-minute total step timeout. The native script bounds fetch and checkout separately: without the step timeout, two attempts could nominally take80minutes. The total cap leaves room for one20-minute failed materialization and a retry at the observed16-minute duration after fast metadata fetches, while bounding this step's Pages-queue occupancy.

The shared clone script, its240-second/four-attempt defaults, other callers, complete main/dev history and current inputs, credentials/TLS, artifact assembly and all validation remain unchanged. This workflow-only change does not promote application work from dev to main.

Validation: private `git apply --check` passed; YAML parsed and its data differs only in those three checkout inputs; the existing native clone self-test passed in2.125seconds, including an injected timed-out first fetch and successful retry, exit0/all children reaped. No live20-minute checkout or deployment result is claimed; those require inspection of the actual authorized main Deploy run.

Prepared against main099db643c3691c90da8e02f45d86d254e7c6c263. This body is a proposed owner-visible workflow hotfix, not a submitted PR, merge approval or deployment authorization. Applicable committed-head PR checks remain required before normal merge.
