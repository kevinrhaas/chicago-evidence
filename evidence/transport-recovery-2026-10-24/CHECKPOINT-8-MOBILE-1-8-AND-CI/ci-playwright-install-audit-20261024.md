Read-only CI install audit — 2026-10-24T10:35:23.882560+00:00

Confirmed facts

- Draft PR #1279 moving-frames run 40085901811 (pull_request, attempt 1, source HEAD 3290195d40cbacf5cbfd0c76f14119d6712aa30c) failed Install Playwright at 10:28:34–10:28:37 UTC on 2026-10-24. Checkout and setup-node succeeded. Publish and both renderer/performance steps were skipped. This is not an observed renderer assertion failure.
- Failure annotation: “Process completed with exit code 1.” It supplies no underlying install stderr.
- Exact notice annotation, including the quoted text: "The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026. For more information, see https://github.com/actions/runner-images/issues/14748"
- A separate warning says actions/checkout@v4 and actions/setup-node@v4 target deprecated Node.js 20 and are forced to run on Node.js 24. That same warning is present on successful runs, so it does not establish the install failure cause.

Normal moving-frames comparison (all pull_request, attempt 1)

| Run | Created UTC, 2026-10-24 | Install Playwright | Subsequent publish/render steps | Ubuntu 26 notice |
| --- | --- | --- | --- | --- |
| 40071829019 | 06:51:06 | failed in 3 s | skipped | present |
| 40074598743 | 07:33:20 | passed in 25 s | passed | absent |
| 40084563539 | 10:06:00 | passed in 25 s | passed | absent |
| 40085901811 | 10:26:11 | failed in 3 s | skipped | present |

Latest successful run 40084563539 used source HEAD 35f0c564cc25303d3f5641812d532dd9d2166b64. The recent 20-run sample contained 18 successes and two failures; both inspected failures stopped at the install step. Failure is not universal across this workflow.

Pinned-package source evidence

The workflow uses runs-on: ubuntu-latest and installs playwright@1.56.1 globally, then runs its CLI install --with-deps chromium. The installed Playwright 1.56.1 package has explicit Ubuntu dependency/browser mappings for 20.04, 22.04 and 24.04 (x64/arm64), and Debian 11/12/13. It has no Ubuntu 26.04 mapping.

hostPlatform.js maps Ubuntu major >=26 to the literal ubuntu<version>-<arch> and marks it unsupported. installDependenciesLinux warns and returns when no dependency mapping exists. Chromium DOWNLOAD_PATHS has no Ubuntu 26 entry or generic unknown fallback; _downloadExecutable throws an unsupported-platform error when no download path exists. If the failed runner actually used Ubuntu 26.04, the pinned package has a concrete incompatibility path. That is a supported hypothesis, not the observed underlying CI error.

Remaining evidence / minimal next step

The complete original failing job log is currently unavailable through its normal redirect because the managed proxy blocks the observed Azure result-storage hosts. The prepared draft adds the observed productionresultssa14/15.blob.core.windows.net hosts but is not applied yet. This audit neither followed an alternate URL/proxy route nor printed/stored signed URLs.

After the prepared runtime network change is applied, obtain the original failing log and latest successful log through the normal API route. Record the actual runner image/OS and first concrete install error. The migration notice alone does not prove the failed runner OS or exact failure. Do not patch CI, rerun/dispatch the workflow, change a browser baseline, or attribute this failure to the application based only on that notice. A supported runner pin or Playwright upgrade can be evaluated in a separately reviewed change after the log confirms the cause.

Public evidence references: https://github.com/kevinrhaas/chicago/actions/runs/40085901811 ; https://github.com/kevinrhaas/chicago/actions/runs/40084563539 ; https://github.com/kevinrhaas/chicago/actions/runs/40071829019 .

Only bounded API metadata/annotation reads and installed-source inspection were performed. No app/CI changes, workflow dispatches, reruns, browser launches or heavy tests.
