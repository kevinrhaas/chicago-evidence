Supported-runner patch review — 2026-10-24T13:20:16.929117+00:00

Confirmed cause: the official per-job log for moving-frames job 120848672967, run 40085901811, reports Ubuntu 26.04.1 LTS / image ubuntu-26.04 / image version 20261012.163.1. npm successfully added the two pinned Playwright packages. Browser installation then reports:

    Cannot install dependencies for ubuntu26.04-x64 with Playwright 1.56.1!
    Error: ERROR: Playwright does not support chromium on ubuntu26.04-x64

Thus the failure is the actual unsupported runner OS/browser-platform combination, not merely a migration notice. Publish and renderer checks were skipped in this run.

Reviewable minimal fix: change only moving-frames job runs-on from ubuntu-latest to ubuntu-24.04. The pinned Playwright 1.56.1 package explicitly includes Ubuntu 24.04 x64 dependency mappings (21 Chromium libraries plus its tools/fonts) and a Chromium download-path mapping. Its platform classifier marks Ubuntu version 24.04 officially supported; Ubuntu 26.04 has neither required dependency nor Chromium mapping. The patch preserves all workflow triggers, step commands, assertions, Node/PW versions, browser install verification and timeouts.

No application/workflow files were edited. `git apply --check` passes against the current checkout; this validates patch applicability, not a new CI run. Root should apply after its frozen browser batch is complete, commit through the normal reviewed PR path, then require fresh normal CI on the resulting head. No dispatch or rerun was performed by this audit.

Evidence: moving-job120848672967-sanitized.log and moving-job-log-source-binding.json in this directory. Raw job log remains private and must not be published; no signed URL or credential is included here.
