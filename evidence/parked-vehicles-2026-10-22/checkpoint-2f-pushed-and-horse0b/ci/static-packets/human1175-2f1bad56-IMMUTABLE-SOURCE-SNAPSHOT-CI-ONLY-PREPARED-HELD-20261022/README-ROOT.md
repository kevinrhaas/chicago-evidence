# HELD historical immutable source-snapshot CI_ONLY

This observer collects existing2f source-test evidence. It is not current-target qualification. Live DEV can advance while source2f stays frozen. The source tree, original run base459, PR checkout merge642,23 existing runIDs, complete branch inventory, source/workflow bytes, attempt1, per-run PR base/head metadata, required jobs/steps, actual checkout/log/cell/population/guarded-bake/check-run/status guards remain unchanged. No actual immutable run metadata guard was relaxed speculatively.

Only live PR target eligibility is separated: openPR1175/repository/sourcebranch/head/devroute and remote human ref must still match; fresh current PR base/merge/dirty/mergeable and DEV ref are recorded as live_target/target_advanced. They do not overwrite the immutable test base or checkout and never qualify a merge. If immutable runPR metadata actually changes, the original strict guard stops with the saved API evidence. Qualification/readiness/live-target-eligibility remain false forever. Success is labelled CI_ONLY_SOURCE_SNAPSHOT_23_VERIFIED.

The prior stopped observer's exact terminalad80b4cb and deadline2026-10-22T18:19:13.496129+00:00 are pinned. Its actual terminal ended15:51:33.275812UTC; the error was live PR source/base/merge binding, not an actual CI failure. Original output and owner lock stay untouched. A new SOURCE-SNAPSHOT owner lock is used only after the existing no-live-collector scan. All audited proofs start empty; no restoration framework. The original150min deadline is retained, never restarted.

No sourcehead movement, workflow dispatch, CI rerun, browser, app/Git/index write, collector or network call occurred in preparation. All original source-only current-input receipts and historical779visual/mobile support/3stress failures remain unchanged. Root will separately integrate/validate the actual changed target after the existing23 terminal results.

After root reviews the small patch, write one immutable source-only release:

```bash
python3 -B - <<'PYROOT'
from pathlib import Path
import hashlib,json
p=Path('/workspace/shared/human1175-2f1bad56-IMMUTABLE-SOURCE-SNAPSHOT-CI-ONLY-PREPARED-HELD-20261022')
r=json.loads((p/'ROOT-SOURCE-SNAPSHOT-CI-ONLY-HELD.json').read_bytes())
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert r['released'] is False and r['allow_GET_collection'] is False and r['collection_mode']=='CI_ONLY' and r['source_snapshot_only'] is True
assert H(p/'collect-GET-only.py')==r['collector_sha256']
assert H(Path(r['prior_observer_terminal_path']))==r['prior_observer_terminal_sha256']
r.update(released=True,allow_GET_collection=True,status='ROOT_RELEASED_HUMAN1175_CI_ONLY_GET_COLLECTION')
out=Path('/workspace/shared/ROOT-1175-2f1bad56f-SOURCE-SNAPSHOT-CI-ONLY-GET-RELEASE.json')
with out.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(out,H(out))
PYROOT
```

Root's sole GET owner, fresh output, environment network escalation:

```bash
python3 -B /workspace/shared/human1175-2f1bad56-IMMUTABLE-SOURCE-SNAPSHOT-CI-ONLY-PREPARED-HELD-20261022/collect-GET-only.py --release /workspace/shared/ROOT-1175-2f1bad56f-SOURCE-SNAPSHOT-CI-ONLY-GET-RELEASE.json --output /workspace/shared/ROOT-1175-2f1bad56f-SOURCE-SNAPSHOT-CI-ONLY-ACTUAL
```
