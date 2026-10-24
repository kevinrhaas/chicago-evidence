T-3121: restrict automatic full-smoke measurements to dev

Merging DEV's workflow edit into a PR branch currently starts another full unfiltered smoke run on that head. These measurements reach their150minute timeout and leave an otherwise green PR pending or red. Restrict the existing automatic workflow-file self-test to pushes on `dev`; keep its path filter and explicit dispatch.

Both viewport defaults, all15parts, published-mirror generation, smoke assertions, runner, timeout, and every job step remain unchanged. No merge policy or required check is bypassed. An edited workflow still self-tests after landing on DEV. Explicit branch measurements retain GitHub's existing requirement that the workflow be registered on the default branch.

Validation so far: full YAML parsing, exact semantic comparison permitting only `on.push.branches: [dev]`, five branch/path trigger fixtures, and `git diff --check` passed. Full preflight and normal exact-head/merge CI remain pending. No new renderer or photo result is claimed.

T-3121's final acceptance also requires PR1277 and PR1278 to merge through their ordinary green gate. This WIP neither merges them nor claims that outcome has occurred. Already-running/old-head measurements are not removed by this source change; a later ordinary fresh-head validation is still necessary.

Updated preparation base: accepted DEV33a99a557bd53aa637cc7173589d610f8a15f14b (HoganT3118 + normalchangelogfold). App/reference files equal that base; thisPR changes only theworkflow.

Automatic measurements on main and tagpushes are also excluded. GitHub skips pathfilters for tagpushes, so this is an explicit narrowing of automatic tagmeasurements. Dispatch/nightly publishedsmoke and allassertions stay unchanged. Seven static branch/path/tag cases pass; no new actual workflowevent or renderergate has run. Explicit smoke mapping treats this unmappedworkflowpath as ALLparts; noNO PARTwaiver is asserted.
