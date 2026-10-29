# Prepared native commands — NOT RUN; root releases the single heavy slot

Frozen staged TREE: `704c50077e647ab7813448f8cff6a564af949eb2`; APP: `6a1ce1edd4cc63199807dae01de558b24f160cc2`; public HEAD remains `9e14c138848ef854a535271fbd3feaae52dd4aa2`. The publisher may stamp that HEAD while building this explicitly bound staged source; do not mistake the stamp for a committed candidate. No source edits or owner writes are needed: SourceUse check is fresh. Root first renews the T2793 native claim normally after expiry. Do not force a claim or change the mirror during browser work.

After root GO, activate in the normal shell, select an owned empty short scratch directory, and verify fresh disk reserves. Publication needs measured mirror peak plus256MiB reserve; retain the512MiB native synthesis reserve if native synthesis were ever required. The current task requires no synthesis. Do not run another generator/publisher/browser concurrently.

```bash
source /workspace/.cloud-setup/transport-activate.sh
cd /tmp/chicago-wagon-20261029/chicago/4d
export TMPDIR=/tmp/w29
python3 /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/MEMORY-FOLLOWUP-PREP/check-staged-source-freeze.py
python3 /workspace/.cloud-setup/transport-supervise.py --prefix /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/rail-candidate-native-publish-01 --cwd /tmp/chicago-wagon-20261029/chicago/4d --timeout 300 -- bash tools/publish.sh
python3 /workspace/.cloud-setup/transport-supervise.py --prefix /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/rail-candidate-native-mirror-check-01 --cwd /tmp/chicago-wagon-20261029/chicago/4d --timeout 180 -- node tools/check_published.mjs
python3 /workspace/.cloud-setup/transport-supervise.py --prefix /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/rail-candidate-native-yearpacks-check-01 --cwd /tmp/chicago-wagon-20261029/chicago/4d --timeout 180 -- node tools/write_year_packs.mjs --check ../../site/4d
python3 /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/MEMORY-FOLLOWUP-PREP/check-staged-source-freeze.py
```

Read actual publisher result/cleanup, retain the complete native mirror file manifest and bind it to the above staged tuple before a browser. Use unique names if a prefix already exists; no overwritten receipts. Preserve source and full mirror hashes before/after every browser. A source-guard failure stops the run; do not truncate full Git/index output to pass it. Python source guard reads all2,132,488 index bytes, and later Node adapters that read Git must use explicit64MiB maxBuffer.

The baseline-identical native memory command below is exactly the original flags/viewport profiles, with a new output path. Native caps remain1300MiB desktop/400MiB phone; retain actual totals and compare desktop separately with historical1125MiB. No heap snapshots, altered renderer/stat methods or extra instrumentation. Native desktop starts Full; native phone starts Light. This run is separate from the later lifecycle page that intentionally switches Full/Balanced/Full.

```bash
python3 /workspace/.cloud-setup/transport-supervise.py --prefix /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/rail-candidate-native1904-memory-01 --cwd /tmp/chicago-wagon-20261029/chicago/4d --timeout 1200 -- node tools/measure_memory.mjs --gate --year 1904 --only both --no-snapshot --json /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/RAIL-CANDIDATE-NATIVE-1904-MEMORY-ACTUAL-01.json
```

For the reviewed lifecycle observer, root may lend its already-owned local static server for this exact mirror, or start an owned `python3 -m http.server 18794 --bind 127.0.0.1 --directory /tmp/chicago-wagon-20261029/site/4d` and stop only that owned server after the observations. Do not launch this preparation while H/P own the heavy slot. The adapter launches the same native Playwright Chromium default/executable selector as the unchanged memory meter. It adds no init scripts, mocks, routes, layer removals or renderer/stat overrides. Source-reviewed observer SHA remains `520790eed74fa3c6e76284634654e405ba0455d323f01b22dade29bc5701f629`.

```bash
python3 /workspace/.cloud-setup/transport-supervise.py --prefix /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/rail-candidate-lifecycle-desktop-01 --cwd /tmp/chicago-wagon-20261029/chicago/4d --timeout 5400 -- node /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/MEMORY-FOLLOWUP-PREP/run-native-railway-lifecycle.cjs http://127.0.0.1:18794/1904/ desktop /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/RAIL-LIFECYCLE-DESKTOP-01
python3 /workspace/.cloud-setup/transport-supervise.py --prefix /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/rail-candidate-lifecycle-mobile-01 --cwd /tmp/chicago-wagon-20261029/chicago/4d --timeout 5400 -- node /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/MEMORY-FOLLOWUP-PREP/run-native-railway-lifecycle.cjs http://127.0.0.1:18794/1904/ mobile /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/RAIL-LIFECYCLE-MOBILE-01
python3 /workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/MEMORY-FOLLOWUP-PREP/check-staged-source-freeze.py
```

These are bounded supervisor limits, not measured runtime promises or weakened native acceptance. Save every real failure/result/cleanup. Inspect actual frames and pick/UUID/state rows; source review and a returned observer do not certify photographic acceptance. Full required-reader preflight and all28 native mapped published smoke commands, including UI13, remain required before release. No commit/push/ready/merge or T3173 completion is authorized by this preparation.
