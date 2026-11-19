# Prepared final-candidate mobile 1–12 runner

Preparation only. No new renderer, publisher, stage, or publication hashing has been launched. Wait for root's explicit go and the final corrected candidate/publication pins. The existing edc mirror is not the intended input.

Files:

- `/tmp/t3658-final-mobile-runner.py`
- `/tmp/t3658-final-mobile-config.template.json` (deliberately invalid placeholders)

After root supplies the final head/tree, smoke-harness SHA256, source/published main SHA256, published build version/time and smoke-tree descriptor, copy/fill the template as `/tmp/t3658-final-mobile-config.json`. `frozen_refs` may pin any additional explicitly frozen Git ref; HEAD and its tree are always checked regardless. Do not freeze a remote tracking ref that root needs to update for unrelated monitoring.

Run under a durable supervisor in its own OS session, with a NEW output directory and NEW supervisor log. Plain nohup leaves the supervisor in the tool command's process group and was SIGKILLed after tool return during the first real stage; it is not sufficient in this environment. The supervisor waits synchronously for every bounded foreground smoke invocation, one world at a time:

```sh
python3 - <<'PY'
import subprocess, sys
with open('/tmp/t3658-final-mobile-APPROVED_HEAD-supervisor.log', 'xb', buffering=0) as log:
    child = subprocess.Popen([
        sys.executable, '-u', '/tmp/t3658-final-mobile-runner.py',
        '--execute', '--config', '/tmp/t3658-final-mobile-config.json',
        '--out', '/tmp/t3658-final-mobile-APPROVED_HEAD',
    ], stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
       start_new_session=True, close_fds=True)
    print(child.pid)
PY
```

Every child uses the absolute Node22 path and Chromium, a clean set of `SMOKE_*` variables, `SMOKE_VIEWPORT=mobile`, one `SMOKE_STAGE`, `SMOKE_TIMING=1`, the pinned mirror and `--published`. Exact command/env and process IDs are saved. The immutable command cap is `timeout --signal=TERM --kill-after=5s 1200s`; no stage automatically retries or raises its allowance.

Evidence is written durably to the cohort directory:

- `manifest.json`: atomic/fsynced live state and per-stage start/end/exit/provenance.
- `events.ndjson`: append+fsync before spawn and immediately after exit, plus validation results.
- `mobile-N.log`: untouched official output, flushed/fsynced at child exit.
- `mobile-N-receipt.json`: complete final receipt, log SHA256, exact four guard lines, counts, runtime and exit code.
- `mirror-inventory.json`: initial SHA256 of every published file plus file metadata; full content rehashed at final completion, complete file-set/stat inventory rechecked before and after each stage.
- `config.json`: frozen expected pins; runner/config hashes recorded in manifest.

`--resume` accepts the same directory/config/script only when every existing stage has a durable zero exit, complete terminal PASS with all guards, and its unchanged log hash. A missing exit receipt is incomplete even if the log ends in PASS. A failed, capped, interrupted or provenance-drift attempt is never rerun automatically; preserve it and obtain a new coordinated attempt/cohort if needed. A live supervisor holds an exclusive lock. Any existing live Chromium or official smoke process blocks a new stage; the runner never kills unrelated processes.

The strict parser requires exactly one mobile single-stage header, one published mirror header, one ordered summary/count/time/PASS footer ending the log, observed timed-check counts equal to the totals, positive selected-body checks and 13 always-on checks, plus exactly one passing suite-completion, zero-page-errors and each vendor guard. Grouped/concatenated logs, partial footers, wrong stage/viewport, changed counts, nonzero/missing exits, and later log mutation cannot become coverage. Stage results from older cohorts are not imported.

Preparation validation: `python3 ... --self-test` passed using a real historical mobile2 log solely as a parser fixture, with 21 negative text cases, five nonzero/missing exit cases, and wrong-stage/mirror/viewport rejection. Untimed or malformed check-looking lines are rejected too. Python syntax compilation passed. A separate tiny-process lifecycle test verified durable JSON/event writes, the stop-signal guard, and owned-process-group cleanup: TERM reaped the parent and bounded escalation killed its TERM-ignoring descendant (6.357 seconds, zero live owned processes remaining). Exceptions clean up the owned group before attempting further receipt writes; no unrelated process is killed. No browser launched. These tests do not replace the first authorized live smoke run. The operator-supplied smoke-tree descriptor is labeled as such; independent source Git tree and file SHA256 checks are recorded separately.

## First live-run recovery

The 347 stage1 official invocation completed 95/0 with all final guards and SMOKE PASS, but the original nohup supervisor was SIGKILLed before persisting its end receipt. Original cohort `/tmp/t3658-347-mobile-1-12` is preserved unchanged, apart from adding a separately labeled recovered-kernel-exit receipt. That receipt contains the raw zombie process stat and exit0 of the exact recorded timeout PID, a 0.028966-second start-identity cross-check, and a full unchanged mirror rehash; it does not invent a normal supervisor exit or exact process end timestamp. Root explicitly authorized this recovery. Stage1 was not rerun.

The verified `start_new_session=True` launcher is recorded in `/tmp/t3658-347-mobile-2-12-launch.json`. The new supervisor is PID/PGID/session235873. `/tmp/t3658-final-mobile-runner-v2.py` adds only an explicit validated contiguous stage subset in configuration; the new `/tmp/t3658-347-mobile-2-12-config.json` selects2–12. Its separate output directory is `/tmp/t3658-347-mobile-2-12`; no older result is silently imported into this cohort.
