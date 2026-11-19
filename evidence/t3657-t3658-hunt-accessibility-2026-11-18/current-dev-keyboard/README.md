# Combined validation candidate

- Commit: `ddc78606998ea8aee589941c6ab6cae76a80440a`
- Tree: `fa70a0164ccbef670529470937b170677c5a99b0`
- Parent: `b1f507400cb743a3985cb1d50de1ebd085bd4f63`
- Current DEV: `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`
- Keyboard checkpoint: `597a7c392f7300eeafd069b2afe245c44c1bb7cf`

The exact eight-file keyboard delta from pushed follow-up `6ee1a6890` was applied
through a temporary index onto proven combined tree `d8df5af9`. The resulting
single commit was unreferenced at preparation; root subsequently pushed and verified it
on qa/t3657-t3658-current-dev-keyboard. This child did not push or change any ref.

`combined.patch` is the complete 27-file delta from parent `b1f5074`.
`keyboard-input.patch` preserves the exact authored keyboard contribution.
`provenance.json` records blob/tree matches, SHA-256 values, parent policy pins,
and the check that all four real worktree indexes and refs stayed unchanged.

Current DEV assets, data, generators and stamped changelog remain byte-identical.
The parent's corrected smoke assertions, Full policy, 900-second CI completion
allowance, budget receipt and pending T-3656 entry remain intact. Keyboard runtime,
focused regression, gate hook, isolation registry and T-3657 entry match `597a7c392`.
STATUS retains the newer parent validation prose as well as the authored keyboard receipt.

No source gate, browser, publisher or renderer was run for this object combination.
Earlier focused/native evidence retains its original commit attribution; complete
combined release gates remain pending. The commit message states those limits.

After the actual parent squash and fold, preserve the folded DEV changelog and the
removal of T-3656.json. This 27-file normalized patch touches neither path, nor any
upstream asset/data/generator path. Apply the normalized contribution to the verified
new parent, compare actual runtime and data trees, and classify additional DEV/fold
changes before reusing validation. Do not merge the older QA history through the
custom changelog driver, which can unstamp an already-published entry.

Stage-5 reuse is scoped in `stage5-reuse.json`: identical 1835 geometry, policy and
API-driven stand checks, with original b501 evidence attribution. It is not a new
measurement on this candidate or validation of the keyboard changes. The actual parent
fold should change only its release entry and stamped changelog if DEV does not advance;
compare actual resulting objects and any re-derived data rather than assuming that.
