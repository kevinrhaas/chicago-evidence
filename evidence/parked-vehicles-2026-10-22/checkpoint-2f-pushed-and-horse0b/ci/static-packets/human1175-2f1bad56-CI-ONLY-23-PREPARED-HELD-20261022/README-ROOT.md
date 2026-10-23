# HELD fresh2f CI_ONLY23 observer

Fresh2f head/tree/base459/merge642 and normal5 IDs are pinned in ROOT-CI-ONLY-OBSERVE-HELD.json. Actual18dispatch receipt is COMPLETE with18acceptedPOSTs/18discovered runs and SHAeedbca56…; dispatcherdb013f3e is copied byte-exact for identity verification. All source/workflow/job/attempt1/log/checkout/population/guarded-bake/checkrun/status checks,61s polling and150min cap remain unchanged. The only collector delta is COMPLETE branch inventory then exact per-run head filtering, including duplicate/existence/extra-run refusals. There is no prior22 restoration: all23 jobs must be freshly audited.

CANONICAL-EXPECTED-INPUTS-2f1bad56.json is a NEW current-head path (007c29f7…), with actual current head/tree/index and38 rehashed source/published/asset input files. CURRENT39-INPUTS.json adds the canonical JSON hash to form the39-pin set. Actual source/public mirror pairs, committed source input bytes, current published build and all8 unchanged canonical96c4/run39736567239GLBs were verified. The old b06f absolute JSON supporting779images was read and confirmed unchanged; it was not overwritten or repinned. These are source-only pin receipts, not a current browser PASS.

Historical779desktopFullvisual/mobilePASS and3desktopstressFAILs remain explicitly historical support/failures. Current-local focused flags remainfalse; they are not a private CI_ONLY prerequisite. qualification_pass and ready_for_root_fresh_merge_review remainfalse forever, including after remoteCI_ONLY success. Root independently reviews the repository-required actual green checks and merge criteria.

After root source review/freshPR/ref confirmation, write one immutable GET release:

```bash
python3 -B - <<'PYROOT'
from pathlib import Path
import hashlib,json
p=Path('/workspace/shared/human1175-2f1bad56-CI-ONLY-23-PREPARED-HELD-20261022')
r=json.loads((p/'ROOT-CI-ONLY-OBSERVE-HELD.json').read_bytes())
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert r['released'] is False and r['allow_GET_collection'] is False and r['collection_mode']=='CI_ONLY'
assert H(p/'collect-GET-only.py')==r['collector_sha256']
for a,b in [('dispatch_receipt','dispatch_receipt_sha256'),('final_diff_pricing','final_diff_pricing_sha256'),('canonical_inputs_path','canonical_inputs_sha256'),('current_input_pins_path','current_input_pins_sha256')]:assert H(Path(r[a]))==r[b]
r.update(released=True,allow_GET_collection=True,status='ROOT_RELEASED_HUMAN1175_CI_ONLY_GET_COLLECTION')
out=Path('/workspace/shared/ROOT-1175-2f1bad56f-CI-ONLY-23-GET-RELEASE.json')
with out.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(out,H(out))
PYROOT
```

Root's ONE fresh GET observer, with network escalation required by this environment:

```bash
python3 -B /workspace/shared/human1175-2f1bad56-CI-ONLY-23-PREPARED-HELD-20261022/collect-GET-only.py --release /workspace/shared/ROOT-1175-2f1bad56f-CI-ONLY-23-GET-RELEASE.json --output /workspace/shared/ROOT-1175-2f1bad56f-CI-ONLY-23-GET-ACTUAL
```

No observer, browser, network call, POST, rerun, cancel, app/Git/index write or new framework was performed in preparation. No historical smoke stage transfers into current-head PASS. Preparation only ran the existing source-only dry planner and AST/source checks.
