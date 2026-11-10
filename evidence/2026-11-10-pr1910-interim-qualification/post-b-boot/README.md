# Queued official post-B boot — preparation only

Do not execute until Root's final merged-source republish, the Fort/Cobweb GPU
legs and Sauganash stage1 are complete and Root explicitly grants this queued
exclusive slot. No browser or GPU has been launched by preparing this command.

```bash
source /tmp/chicago-resume-env-20261109.sh
GPU_SLOT_GRANTED=post-b-boot python3 /tmp/nov10-post-b-boot/run-official.py \
  --expected-source FINAL_FULL_SOURCE_SHA \
  --expected-build FINAL_BUILD_VERSION \
  --expected-build-sha256 FINAL_BUILD_JSON_SHA256
```

The unchanged official tool serves the final mirror using gzip and a fresh
1280×800 context, waits for real ready plus the official three-second settle,
records every request and applies the actual documented boot budget with
`--check`. No blocked routes, forced tiers, tool edits or source/cache substitution
are used. Raw stdout/stderr, all entries, exact source/build/tool/native bindings
and actual result are preserved. The initial attempt cannot be overwritten or
automatically retried. This certifies actual boot bytes only, not frame/Light/FITS.

Native B desktop stage5 passes the real worst-stand Full/Balanced/Light budget
assertions, but its success log omits numeric maxima. The actual post-B priced
Balanced maximum therefore still needs the unchanged official six-stand tool.
After the boot command, in the same exclusive slot but a separate foreground
call:

```bash
source /tmp/chicago-resume-env-20261109.sh
GPU_SLOT_GRANTED=post-b-boot python3 /tmp/nov10-post-b-boot/run-balanced.py
```

It binds the same exact source/build as the completed boot receipt and preserves
the actual JSON/readout/command. Exit zero alone does not assert whole FITS.
