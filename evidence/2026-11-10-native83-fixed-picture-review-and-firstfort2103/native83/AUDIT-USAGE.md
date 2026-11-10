# Retained native audit

Executed successfully against retained native commit 47f5ecbbe3a15cd0011eb6d87a619e4bd0144c4f after correcting the documented glTF Y-up auditor axis bug and narrowly reading the three package-backed Glessner assets. Original failures are preserved; see AUDITOR-CORRECTION-EXPLANATION.json.

Run after the retained native commit is locally readable:

```sh
source /tmp/chicago-resume-env-20261109.sh
python3 /tmp/nov10-group-native-final/audit-retained.py RETAINED_SHA --run-id WORKFLOW_RUN_ID
```

Optional `--repo PATH` chooses the Git object database; `--output-dir PATH` chooses an external receipt directory. `--run-id` is optional context, not authenticated workflow provenance. Git lazy fetching is explicitly disabled, and the audit never checks out a commit.

It requires the retained commit's single raw parent to be 5484f145fb02e51a4f43a773c4bf818ab9e46b8f and binds the frozen BEFORE-BINDING SHA. It checks all 83 fresh default rows, all bound source/recipe bytes, 81 controls' complete non-UV accessor bytes/materials/nodes/topology and actual strict WEB bytes, and exact registry/MASTER/WEB/LOD preservation of 961 foreign defaults and 6 foreign variants. MASTER UV-only differences are accepted only when every other byte/semantic condition from the West audit holds and the actual byte-identical WEB has no UV/textures/images.

Targets receive decoded exported costs, local mesh bounds, vertex semantic/position multiset deltas, oriented triangle semantic deltas and aligned-position diagnostics. Green Tree requires stable costs/glTF X-Z ground-plane projection and exact overall bounds/materials/nodes. Cobweb requires exactly 1002 added triangles (501 clapboard quads), preserving every old oriented non-UV triangle including material/normal/confidence; exact bounds/materials/nodes remain required. These checks derive from the frozen pre-export receipts; unexpected differences fail honestly.

Success writes POST-NATIVE-AUDIT.json, POST-NATIVE-CONTROLS.json and POST-NATIVE-TARGETS.json; failure writes POST-NATIVE-AUDIT-FAIL.json with the literal exception and returns 1. No GPU/image-gate or scene acceptance is claimed.

This final packet preserves all 83 mesh input documents/hashes and all asset/registry baselines from the original 42db packet. The final source commits contain the documented non-geometry Cobweb prose fix and Jail picture review outputs. The earlier packet remains untouched.
