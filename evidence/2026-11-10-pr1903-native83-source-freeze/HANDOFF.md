# Final T-2374/T-2376/T-2380 native before-binding

Frozen clean source HEAD `5484f145fb02e51a4f43a773c4bf818ab9e46b8f`; registry base `c5382c727ae06e0ba1cd6816cc072cbfba4d963d`. Original `/tmp/nov10-group-native` packet is preserved. No repository edits, Blender, installs, browser, dispatch, GitHub writes or model exports were performed by this capture.

`RECAPTURE-PROOF.json` proves all 83 resolved mesh input documents and hashes and all MASTER/WEB/LOD baselines and registry snapshots exactly equal the earlier 42db packet. The only changed bound source bytes are exactly one documented Cobweb note edit: `Exterior lower-wall fields` becomes `The exterior lower-wall fields`. Committed Jail picture review outputs change no mesh inputs. All bound sources, registries, HEAD and clean status were guarded again after validators.

## Dispatch authority

- `only.txt`: exact CSV, 83 distinct IDs / 83 default phase bindings / zero variants.
- 82 log_dwelling family bindings plus Green Tree's one frame_tavern binding. Cobweb and Green Tree are the 2 intended geometry targets; 81 others are controls. Jail's enclosure has no native model target.
- `BEFORE-BINDING.json`: actual resolved docs/hashes, old rows, MASTER/WEB bytes/hashes, Blender pin and producer recipes.
- `BEFORE-manifest*.json`: all 3 raw registries, byte-identical to dev c538.
- `BEFORE-foreign-defaults.json` / `BEFORE-foreign-versions.json`: 961 foreign defaults plus all 6 variants, rows/receipts and actual MASTER/WEB/LOD readback hashes.

## Literal validation

- `python3 tools/validate.py --params`: exit 0; PASS 0 errors / 323 warnings (22.789 seconds).
- `python3 tools/validate.py --params --stale`: exit 1; exactly 83 selected default stale errors / 323 warnings (25.495 seconds). No unexpected error or variant. Expected before-build red; no full gate or native acceptance claimed.
- Full logs and return codes: `params.log`, `stale.log`, `VALIDATORS.json`, `VALIDATION-SCOPE.json`.

## Post-native audit

`audit-retained.py RETAINED_SHA --run-id RUN_ID` now requires this final HEAD as the retained native commit's single raw parent. It is syntax-checked only and has not been run against missing outputs. Read `AUDIT-USAGE.md`; it verifies fresh 83 rows, 81 complete control semantics and strict WEB identity, target costs/bounds/semantic deltas, and exact foreign 961+6 preservation using immutable Git objects. Failures return 1 and retain literal FAIL JSON. Parent remains sole dispatcher/publisher.
