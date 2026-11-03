# T2380: practical native family qualification next step

Candidate checkpoint d73cd2f3d8f7b207069ac479846a21ddc4d24f3d is complete. No native build, benchmark, workflow dispatch, registry write or new implementation was performed in this execution-plan review.

## Available standard command

Once the candidate source branch is available under the normal commit/PR policy, the existing workflow accepts a COMMA LIST through `only`, even though its input description says single id. `generators/build.py --only` parses that list, refuses unknown ids and builds all reached phases in one Blender startup. `FRAME-STRUCTURE-IDS.csv` is the actual current unique frame-family roster plus the new keeper. Use the command from the shared environment:

```bash
JAIL_FRAME_ONLY=$(cat /tmp/jail-family-native-execution-plan-20261103/FRAME-STRUCTURE-IDS.csv)
gh workflow run chicago-4d-bake.yml --repo kevinrhaas/chicago --ref OWN_SOURCE_BRANCH -f only="$JAIL_FRAME_ONLY"
```

The workflow's build job uses pinned Ubuntu26.04, Blender4.5.3 from the SHA-verified pin and a50minute job cap. It builds the dispatch source ref and PRs the generated result back to THAT SAME ref, not dev/main. The selected batch covers271existing family assets plus the keeper; it avoids a whole-town foreign-family rebuild. Source/job policies and exact resulting check status still apply; this command is not permission to commit an unchecked tree or bypass the four-part source gate. No workflow changes are required or proposed here.

## Reuse and cost

The selected keeper pair is genuinely reusable when its FULL normalized input document remains cbc124... exactly equal to the original native build. No keeper rebake is necessary for a private native parity controller that retains that pair; the standard selected workflow will rebuild selected ids, including keeper, because its build loop has no fresh-asset skip.

All271unchanged-default meshes still need ACTUAL native MASTER qualification under the optional keeper producer. Predicted recipe hashes and resolved-param identity do not prove geometry parity. After byte-exact actual MASTER parity is established, the existing exact WEB bytes and real master bindings can be retained without claiming a new encode. Entrywise native registry provenance must accompany the actual builds.

The standard `tools/bake.sh --only` path ALWAYS calls official WEB derivation for every master the selected build wrote, even if those bytes stayed identical. The unselected/full-bake path uses `tools/stale_derivatives.py` and derives only moved/unrecorded masters. Thus existing workflow dispatch has no flag for selected-default native MASTER builds plus unchanged-WEB reuse. A full unselected bake would save those WEB encodes but needlessly regenerate all other families; do not choose it merely to avoid the selected path's derivative loop.

Prior ACTUAL one-asset controls quoted in the retained native controller README: Carpenter MASTER0.837s and WEB2.895s; School MASTER0.744s. Straight-line271xCarpenter arithmetic is about227s MASTER+785s WEB, roughly17minutes before check/publish/smoke and without startup amortization. This is only historical pricing, NOT a new benchmark or a completion promise. Current selected workflow amortizes the Blender startup but its WEB tool still runs the selected loop. The workflow's source check and later phone/desktop smoke add separate time.

A native controller with retained keeper and unchanged-WEB reuse could price its first8defaults at around6–7s of historical MASTER work plus startup, then use actual measured time. The old `/workspace/T2380-native-batch-controller-20261030/controller.py` is not directly runnable against current source: it points at old keeper layout/expected recipe4217..., old source pins and private root-grant variables. Do not execute it blindly or treat its UNRUN34batch plan as passed proof. No new controller is prepared here. The immediately AVAILABLE no-new-code route is the bounded selected workflow above, with actual before/after default MASTER/WEB identity review and foreign-registry guards.
