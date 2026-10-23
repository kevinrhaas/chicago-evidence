# NEXT-HEAD CI — HELD, SHA:null, no POST

Root must supply an exact newly committed/pushed SHA and full preflight PASS before activation. Old2aeb and0a037 heads cannot be executed by this dispatcher. Original18 request receipts/failures are preserved as history, never reused as current qualification. No app/index/mirror/source gate/browser action is present here.

Manual identity: chicago-4d-smoke.yml, SHA25600ae307ad6cbeb556ddd5028668ee53a839393c619cc52ae5d0e8f39eb84ec52, dispatch inputsviewport/stage, actual published command node tools/smoke_renderer.mjs --published; each job150min cap. Nightly matrix source chicago-4d-bake.yml must still have exact ranges1-2,3-4,5,6-7,8,9-12,13,14,15. Both desktop/mobile tile1..15 with no gaps/overlaps:18 requests. Original priority order retained (desktop13 first). PREPARED-WORKFLOW-PINS.json includes all five mandatory workflow identities. A changed workflow demands inspection/repreparation.

Expected automatic workflows: pull_request gate, pull_request moving-frames, push stuck-report. The final independent price command checks *all* current source workflow push/PR filters using the final exact commit, its actual previous pushed0a037 and local origin/dev merge base. Unknown glob syntax or changed expected workflows stops activation. A source prediction is not actual CI evidence. Root should reconcile fresh remote base/diff if dev moves. The native smoke_budget command reports measured local recipe cost and limitations; neither tool launches smoke.

After commit/push (commands below use FINAL40HEX as a literal placeholder):

```sh
python3 /workspace/shared/parked-covered-2981-NEXT-HEAD-CI-HELD/price-final-diff.py --sha FINAL40HEX > /workspace/shared/parked-covered-2981-FINAL40HEX-pricing.json
```

```sh
node /workspace/chicago/chicago/4d/tools/smoke_budget.mjs --for-diff origin/dev > /workspace/shared/parked-covered-2981-FINAL40HEX-native-smoke-price.txt
```

Run native price only while live HEAD is FINAL40HEX; it prices HEAD by its interface. The Python pricing uses immutable Git blobs regardless of live staging. It reports18 manual jobs/2700 runner-minute worst-case job-cap sum, not a runtime or billing prediction. The OLD-HEAD-* files are parser/dry-plan controls only, clearly historical0a and not activation pricing.

Copy ROOT-ACTIVATION-HELD.json OUTSIDE this package to /workspace/shared/ROOT-RELEASE-parked-covered-2981-ci-nexthead.json. Root sets statusROOT_RELEASED_EXACT_HEAD, allow_dispatchtrue, actualsha, committed_pushedtrue, full_preflight_PASStrue, and exact final pricing path/SHA. Repository/branch/PR/sourceSHA must match. Workflow pins and finaltree/pricing are checked locally, then fresh GET branch/commit/tree/PR source repo/base=dev checks run before any POST and branch is checked before each POST. The dispatcher refuses any existing selected-workflow run at this new head, creates a fresh new-head POST lock, checkpoints post_attempted before request, never retries a POST, and stops ambiguity. No rerun/cancel, unfiltered duplicate, bake, canonical human or production dispatch.

```sh
python3 /workspace/shared/parked-covered-2981-NEXT-HEAD-CI-HELD/dispatch-once.py --sha FINAL40HEX --pr 1174 --activation /workspace/shared/ROOT-RELEASE-parked-covered-2981-ci-nexthead.json --execute --output /workspace/shared/parked-covered-2981-FINAL40HEX-dispatch-once
```

If all18 POSTs succeeded but discovery lagged, GET-only reconciliation uses the SAME new dispatcher source and old receipt; it never sends more POSTs:

```sh
python3 /workspace/shared/parked-covered-2981-NEXT-HEAD-CI-HELD/dispatch-once.py --reconcile /workspace/shared/parked-covered-2981-FINAL40HEX-dispatch-once/receipt.json --output /workspace/shared/parked-covered-2981-FINAL40HEX-reconcile-GET-only
```

Do not reconcile/redispatch an ambiguous or partial POST set automatically. Preserve receipt/locks and let root inspect. Root may assign one GET observer after a complete18-accepted/18-discovered receipt:

```sh
python3 /workspace/shared/parked-covered-2981-NEXT-HEAD-CI-HELD/observe-GET-only.py --receipt /workspace/shared/parked-covered-2981-FINAL40HEX-dispatch-once/receipt.json --output /workspace/shared/parked-covered-2981-FINAL40HEX-CI-GET-owner1 --minutes 180 --interval 60
```

The GET observer owns a fresh disjoint exact-head lock and output. Poll at mostonce/min. Retry only transient HTTP502/503/504 or EOF/reset reads, at most2 retries after2/4seconds; no auth/semantic/failure retries. Strict audit_job and smoke_cell helpers are unchanged from recovered4 (hash proofs in pins). Qualification requires18 unique successful actual workflow/job/log cell bindings plus3 normal actual jobs/steps, currentSHA/branch/repo/base=dev, attempt1, no unexpected/duplicate workflow, full listing, exact steps success, single SMOKE PASS and matching env+runtime filters. An old run/receipt/head cannot count. A failure, drift, missing cell or unexpected workflow stops with evidence. Default/fresh preparation is not a network action.

Qualification is handed to root for final fresh required checks/branch protection/route/lap/mergeability review. This observer does not ready, change PR body, merge or bypass protection. Old diagnosis/rebudget decisions are not replaced by prior green runs.
