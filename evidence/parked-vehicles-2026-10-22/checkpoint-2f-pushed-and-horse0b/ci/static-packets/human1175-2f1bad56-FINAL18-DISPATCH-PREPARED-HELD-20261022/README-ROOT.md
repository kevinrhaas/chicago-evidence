# HELD exact2f fresh18 once-only dispatch

Bound head2f1bad56ffa14abf2644f8d12f118096944eeec5, tree00cb2e2fd5c49d3d2716fb33b5f74b94c5fc4833, DEVbase4591932010d13063b753c39fcc72607d58086bc6, PRmerge642064a4d359440b22b3176573a7b571d54ae958. Actual source pins are regenerated from that commit, including Calumet-updated smoke_renderer9ec8961e. Unchanged canonical96c4/run39736567239 baselinec670 and all four actual webGLB bytes are checked by the existing dry planner. DRYPLAN.json is source-only; no network or dispatch was run.

The existing18-cell nightly grid and both widths are unchanged. Existing onePOST/cell, fresh source lock, no retry,180s operation, source-clean/index-clean, pinned workflows, exactPR/base/merge and before/after remote-ref guards remain. The small patch replaces the unreliable head_sha listing with a COMPLETE branch listing, filtered by exact head and smoke workflow path. All other branch runs are retained in raw evidence and excluded only by explicit path/head selection. Incomplete pagination refuses before dispatch/discovery acceptance.

FINAL-PRICING.json binds the current47-path diff against459 and root's actual smoke_budget --for-diff ALL log. Historical779 smoke successes do not qualify2f. Normal actualIDs supplied by root: gate39806171573, humans39806171507, moving39806171475(PR), report39806159734 and guardedbake39806159720(push). No manual moving request is planned, and no normal result is asserted here. Local focused flags stayfalse; prior779visual/mobile are historical support and all3supplementary desktop stress failures stay recorded. Root independently reviews requiredCI; no private focused protocol is introduced.

After root reviews the patch/pricing and confirms the exact pushed source, write ONE immutable release:

```bash
python3 -B - <<'PYROOT'
from pathlib import Path
import hashlib,json
p=Path('/workspace/shared/human1175-2f1bad56-FINAL18-DISPATCH-PREPARED-HELD-20261022')
r=json.loads((p/'ROOT-FINAL18-DISPATCH-HELD.json').read_bytes())
assert r['released'] is False and r['allow_dispatch'] is False
assert hashlib.sha256((p/'dispatch-once.py').read_bytes()).hexdigest()==r['dispatcher_sha256']
r.update(released=True,allow_dispatch=True,status='ROOT_RELEASED_HUMAN1175_EXACT_HEAD_SMOKE_DISPATCH')
out=Path('/workspace/shared/ROOT-1175-2f1bad56f-FINAL18-DISPATCH-RELEASE.json')
with out.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(out,hashlib.sha256(out.read_bytes()).hexdigest())
PYROOT
```

Root's ONE dispatcher, with network escalation required by this environment:

```bash
python3 -B /workspace/shared/human1175-2f1bad56-FINAL18-DISPATCH-PREPARED-HELD-20261022/dispatch-once.py --sha 2f1bad56ffa14abf2644f8d12f118096944eeec5 --pr 1175 --activation /workspace/shared/ROOT-1175-2f1bad56f-FINAL18-DISPATCH-RELEASE.json --execute --output /workspace/shared/ROOT-1175-2f1bad56f-FINAL18-DISPATCH-ONCE
```

If any POST/result is ambiguous, stop and preserve the receipt. Do not repeat this command or rerunCI. Existing --reconcile is GET-only and may be separately authorized only after18acceptedPOSTs; no automatic dispatch recovery is authorized.
