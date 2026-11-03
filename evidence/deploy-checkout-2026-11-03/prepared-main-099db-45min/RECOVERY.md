# Prepared main Deploy checkout remedy — not activated

Actual main preimage: `099db643c3691c90da8e02f45d86d254e7c6c263`.
This packet contains an outside-source patch and full proposed workflow body.
No checkout, Git ref, source file, claim, PR, workflow dispatch or deployment was
changed. No main merge or production promotion is authorized by this preparation.

The sole proposed source change is `.github/workflows/deploy.yml`, at the Deploy
job's existing checkout step:

- `CLONE_BOUND_SECS: '1200'` — allow20 minutes for each native fetch/checkout operation.
- `CLONE_ATTEMPTS: '2'` — retain a retry while avoiding four long attempts.
- `timeout-minutes: 45` — cap the entire checkout step and its Pages-queue occupancy.

The shared clone script remains byte-exact with its default240-second bound and
four attempts. Other callers, promotion/steward limits, credentials, TLS, complete
main/dev inputs, all history, blob filtering and every validation step are unchanged.

## Actual diagnosis and budget

Production main Deploy run41706449525/job126162944784 fetched main/dev metadata
in about24 seconds, then exhausted four240-second checkout operations. The
complete failed checkout step ran19:47:14–20:03:57 UTC, 16m43s. Its attempts
reported264/242/249/248 seconds. No downstream publication or Pages upload ran.
The later dev preview remained at485ca273 when the parent investigated; a merged
source PR and a published preview are therefore different observed states.

A distinct actual full-current-worktree checkout in native bake41705636341,
job126161893192, completed in15m58s. This supports allowing20 minutes for one
materialization. It does not guarantee that Deploy's next checkout will finish.

**The clone script bounds fetch and checkout separately.** Its historical header
says end-to-end, but implementation invokes `bounded "$bound"` twice per attempt.
Consequently1200seconds×2 operations×2 attempts has a nominal80-minute worstcase
before termination overhead; four attempts would allow160minutes. The proposed
45-minute checkout-step timeout is what imposes the true overall step cap.
With actual fast metadata fetches, a first20-minute bad checkout plus a retry
completing at the observed15m58s costs about37minutes including fetches. Both
native retry behavior and a finite queue budget are retained. GitHub runner
cancellation/cleanup overhead may extend wall time slightly past the step cap.

The Deploy job intentionally has no explicit job timeout. Its other steps and
the later Pages deployment still have their existing behavior. This patch limits
only checkout, not the entire deployment duration or all queue waiting time.

## Validation actually performed

- Fetched both exact main workflow/script preimages through existing authenticated
  GitHub API and retained their blob identities and bytes.
- `git apply --check` passed against the private preimage directory without applying.
- Existing YAML parser accepted the proposed workflow. Parsed-tree comparison
  found exactly the three checkout inputs above changed, all other workflow data exact.
- The unchanged native clone `--self-test` passed in2.125seconds onCPU2/nice19,
  under600-second foreground/reaper limits. The injected2-second bad fetch was
  abandoned and the next attempt succeeded; exit0, three children reaped, none left.
- Native global default240/four and fixture2/three controls remain exact.

The self-test proves the existing retry mechanism. It does not prove a real
1200-second remote checkout, live publishing, current app runtime, four source
parts or hosted PR checks. None of those outcomes is claimed by this packet.

## Review and activation boundary

Pages runs its actual deployment on main; dev pushes only dispatch that main
workflow. A dev-only workflow PR cannot repair the active main checkout. The
concrete next step is a separately reviewed, owner-visible workflow hotfix into
main containing only this workflow delta, with the applicable actual PR gates.
Do not promote application changes or merge dev into main merely to carry it.
Recheck the main preimage before applying; the packet is not approval to push
main or activate deployment. After authorized normal merge, inspect the actual
main Deploy result and separately verify the delivered dev build/source ancestry.

Files: `deploy-checkout-bound.patch`, `postimages/.github/workflows/deploy.yml`,
exact preimages, `ACTUAL-MAIN-CHECKOUT-FAIL.log`, `QUALIFICATION.json`, native
self-test log/reaper, proposed `PR-TITLE.txt`/`PR-BODY.md`, and closed manifest.
