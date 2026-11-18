# T-3657/T-3658: final follow-up rebase plan

Read-only preparation, 2026-11-18. No real branch, index, worktree, ticket, or PR was changed.

## Proven objects

- DEV: `169404c9f99d2defeca2b05f2364c868a4f4e745`.
- Primary PR 2197: `5034a724d993abe0876a4db7bbfff02d2bb4da0a`.
- Follow-up PR 2199: `6ee1a689077839dd9923edbc80269dd2cbaccfb6`.
- Shared classroom boundary: `03ecd9678e15988abe44c50e27c2bd9fec569530`.
- QA: `b501bfcbc9a9ecb38c7bed76efe35a48165b061b` = follow-up plus exact parent assertion repair.
- Predicted primary merge tree: `34572243b84a594fa3783fe82b228664fc16d8ee`.
- GitHub merge commit `400ac5f8e803958e4ec577ea3317d9003b6f7efa` has exactly that tree and parents DEV + primary above (verified from raw Git database JSON).
- Predicted complete follow-up tree: `76bc63254d7474081d8a49122dc93856efa60458`.

The primary tree is a clean ordinary Git merge of DEV and primary. The complete tree is
a clean three-way merge with explicit base03ecd of that primary tree and QA b501.
The only difference from QA b501 is STATUS.md retaining34 added and8 replaced lines
of newer primary validation prose. Renderers, assets, data and generators are byte-identical
by Git subtree IDs. The normalized parent→follow-up delta is24 files, with no changes to
assets/data/generators, changelog.js, T-3656.json, budget pins, CI workflow, or parent tests.

A temporary index applied the exact normalized patch and wrote the predicted complete
tree. Artifacts:
- /tmp/t3657-t3658-rebase-provenance.json
- /tmp/t3657-t3658-normalized-followup.patch
- /tmp/t3657-t3658-rebase-prediction.index

## Minimal sequence after the authorized primary squash and fold

Use one normalized follow-up cherry-pick; replaying16 historical checkpoints is unnecessary
and invites intermediate conflicts from parent fixes already landed.

1. Fetch the actual PR2197 squash S and wait for its normal changelog fold D. Require S's tree
   to equal34572243 above and S to be an ancestor of D. If DEV acquired unrelated changes,
   recompute the prediction and classify them before using this plan.
2. Construct one local aggregate commit with tree76bc6325 and parent S. This is exactly the
   24-file feature delta already tested in QA, with newer parent validation prose retained.
   Do not use a raw diff from03ecd: that includes DEV roofs and duplicate parent repairs.
3. From a clean detached D checkout, cherry-pick that one aggregate commit. Detaching keeps
   the existing follow-up branch at its pushed6ee checkpoint until the result is validated.
4. Verify the resulting runtime (excluding the now-folded changelog.js), assets, data and
   generators against QA b501. Preserve D's changelog.js verbatim. T-3656.json must stay absent;
   T-3657.json must remain pending and byte-identical to6ee. If fold re-derived data differs,
   inspect the actual files rather than assuming equivalence.
5. Run the required final base-sensitive/preflight checks and changed runtime coverage.
   Publish the rebased follow-up to its existing PR branch once, with an explicit lease on
   the previously observed remote head6ee. Do not push intermediate historical replays.

Concrete local commands for steps1–3, after recording the real full S and D SHAs:

```sh
# Set task-specific variables only after fetching and verifying the actual squash/fold.
test "$(git rev-parse "$parent_squash^{tree}")" = 34572243b84a594fa3783fe82b228664fc16d8ee
git merge-base --is-ancestor "$parent_squash" "$folded_dev"
# The message file must describe final T-3657/T-3658 behavior and actual validation.
followup_delta=$(git -c commit.gpgSign=false commit-tree \
  76bc63254d7474081d8a49122dc93856efa60458 -p "$parent_squash" \
  -F /tmp/t3657-t3658-final-message.txt)
# In a clean follow-up checkout; retain its current branch as the checkpoint.
git -c core.hooksPath=/dev/null switch --detach "$folded_dev"
git -c core.hooksPath=/dev/null cherry-pick "$followup_delta"
```

These commands are a plan, not executed here. The normalization makes no source edits or
new behavioral choices. The final aggregate commit and its cherry-pick receive normal
honest validation before the PR update.

## Duplicate parent contributions

- `308e45207` duplicates primary `ae4e0bdd7` (same stable patch ID): Full budget.
- `4a2ee67dc` duplicates primary `7019f986b` (identical patch): CI completion allowance.
- QA `b501bfcbc` duplicates primary `5034a724` (identical patch): exact restored budget pins.
- `e579424f0` caption/draft code and tests are fully subsumed by primary `45b35a2c7`.
- `07977f549` has six code/test files already covered by `bb59311bf` + `45b35a2c7`.
  Its STATUS additions also contain follow-up receipts; do not blindly discard its whole
  documentation contribution. The normalized tree retains the merged documentation.
- `e23ea1f45` is the DEV merge; `75bf82b7a` and `169404c9f` are already in the new base.
  They must not be replayed as new follow-up work.
- A raw6ee merge at boundary03ecd has one add/add conflict in the Full-budget measurement
  note because it lacks5034's receipt. Using the proven QA tree avoids that conflict.

## Changelog

The normal workflow folds T-3656.json into changelog.js, stamps it, deletes the entry and
re-derives counts. Do not recreate T-3656.json, restamp shipped entries, or copy QA's older
changelog.js over D. Only T-3657.json belongs to the follow-up; its T-3658 rail/modal/zoom
wording is already included. The24-file normalized delta touches none of the parent's fold
paths, so its cherry-pick preserves them naturally.

## Primary merged-candidate coverage

Primary5034's renderer proof is not proof of the newly combined1904 assets. QA b501 is
also not a substitute for a primary-only candidate: it adds hunt/accessibility behavior.
Use immutable primary merge commit400ac5f8/tree34572243 for the targeted integration proof.

| Difference from primary5034 | Published coverage on both390×780 and1280×800 |
| --- | --- |
| Two1904 GLBs, manifests, doors1904 cache/input hashes | Stage14: /1904/ boot, exact placed set, loader errors and spawn budget. |
| Those same assets reached through real navigation | Stage15: actual1835→1904 Jump, destination arrival and Confidence restoration. |
| DEV's already-folded T-3562 changelog entry | Stage13: What's new import, entries/date/unread marker and returning visitor behavior. |
| Generator/measurement/photo-match evidence files | Source/asset validation; generator code does not execute in browser. |

Exact smoke locations: stage14 door20676; houses20835/20870; set21143; loader/budget21836–21840.
Stage15 real transfer22173–22230. Stage13 What's new18864–18968. Every selected invocation
must finish its final page-error/vendor checks. Stage14 alone does not cover stage15's
changed destination load and state transfer.

1808 and1815 are Prairie addresses. Keith's phase begins1886; Sears–Meeker's begins1904.
The1812/1835 sidecar indexes exclude both, while1904 includes both changed model paths.
The1904 door changes are input/cache hashes, not coordinates. Stage5's1835 geometry is
unchanged. Stage13 opens/aborts Jump without loading1904; its new dependency is changelog.
Source CI on400ac5f8 may establish source gates on the merged tree, but does not replace
these published renderer checks. Actual later fold content still needs its own changelog
verification; predictions do not pre-certify future objects.

