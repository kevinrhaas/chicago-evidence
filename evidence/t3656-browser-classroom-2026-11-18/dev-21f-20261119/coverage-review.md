# Coverage scope for DEV 21f609244 (T-3635)

Read-only review completed 2026-11-19 by the accessibility lane, with an independent review of stages 13–15. No tests, browser, publisher, application edit, or ref change was performed. `origin/dev` was observed at c676; primary HEAD remained b1. The ongoing ddc source gate was left alone.

## Objects and comparison results

- Previous DEV: `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`.
- Incoming DEV: `21f609244a4a54135e0d3657bf0d1fff44ee30c7`.
- Primary: `b1f507400cb743a3985cb1d50de1ebd085bd4f63`.
- Follow-up: `ddc78606998ea8aee589941c6ab6cae76a80440a`, worktree `/workspace/chicago-followup-validation`.
- API receipt: `/tmp/t3656-dev-advance-21f609244a4a54135e0d3657bf0d1fff44ee30c7.json`.

The actual incoming diff has 25 paths. For every incoming path, both b1 and ddc currently have the same blob/absence as c676. Thus the upstream-input classification below applies to both candidates, subject to verifying the actual integrated trees; no candidate merge was constructed by this review.

The c676 and 21f renderer subtrees are identical (`4b8a335c70446c046163d282a29b9838d9a8af49`). Their smoke harness blob is unchanged (`9e0930c0531ca8508048eed407ebf5a771b9e391`). The current b1 and ddc harnesses also match each other, retaining the primary's later corrected budget assertion. The incoming change adds `changelog.d/T-3635.json`, but does not change `renderers/web/js/changelog.js`.

## Changed inputs that matter

- The 1904 draft house is replaced by `house_2027_prairie__as_mapped_1904.glb`. The web GLB grows from 36,648 to 1,999,080 bytes; its geometry and resource cost must not be treated as equivalent. The 1904 index/sidecar, front and back yards, doors, inside data and walk joins also change. The 1835 and 1812 structure indices are byte-identical.
- Global liberties grow from 1183 to 1184. `L-k01-2027-villa-3635` is new, and `L-draft-prairie-20-22-east-2352` changes its coverage/prose. This is not the previous review's single hidden paragraph-only change.
- The shared source index still has 709 identical source identities. Only `sanborn_1911_chicago_v3_sheet_35` changes: claims 917→922 and inferred claim count 741→746. Its `use` remains `other_scene`, so the default 1835 list excludes it, but the All registered sources list renders it at rank 7 before and after the change.
- That source's detail file replaces six old-phase edges with eleven new-phase edges, all for `house_2027_prairie`; its edge count changes 917→922. It is not just reordered unchanged text. The existing smoke paths do not open this Sanborn detail file.
- The compiled 1904 build-log jaunt changes only its opening text, from 103 developed buildings/53 omitted to 104/54. Its 50-stop route and the entire 1904 catalog are unchanged by this increment.
- `check_unique_ids.py` changes from blob `a39036c24a48b46e86eb80bfa68c7f25aa2a783a` to `a69d59142a4b185544c6662759010e97312eb7f2`. It adds two exact `(file, by_storey)` multiset exceptions, one for the 2027 structure and one for its compiled sidecar. No other validator logic changes.

## Required renderer refresh

After integration, run unchanged official **stages 13, 14 and 15 on desktop and mobile**, against each final runtime for which release evidence is claimed. The incoming delta has the same required stage set for primary and follow-up; that does not make their differing feature runtimes interchangeable.

| Stage | Exercised changed input and coverage |
| --- | --- |
| 13 | The Evidence hub renders/counts the whole liberty collection, searches it for `roof`, clears the search and checks the counts (`smoke_renderer.mjs:16613–16863`). The Sources All toggle renders the changed Sanborn index row, including its claim figures (`16706–16735`). Old b1/ddc-input results cannot stand for these new global UI inputs. The named source assertion checks Andreas, so passing this stage does not independently pin the exact new Sanborn counts. |
| 14 | Renders the global liberty list and checks count, prohibited internal identifiers, overflow and expanded-layout stress (`19008–19042`, `19612–19715`). It then boots 1904; the asserted placed set includes `house_2027_prairie` (`20965`). The replacement GLB and revised yard/door/inside inputs reach loader, error and draw-budget integration checks. |
| 15 | The real 1835→1904 Jump (`22173–22230`) loads the new destination inputs and checks arrival and carried Confidence settings. Its source-panel check loads the shared index, but opens Kinzie rather than the changed Sanborn detail (`22077–22088`). |

The pending changelog fragment alone does not invalidate current release-feed assertions. If folding changes `changelog.js`, run stage 13 on the actual folded publication as well; scheduling against the final feed avoids a redundant intermediate execution.

## What can retain its scoped evidence

The incremental DEV change does not require a blanket rerun of stages 1–12. Their 1835 geometry, materials, viewpoints, budgets, runtime code and assertions are unchanged. In particular:

- Stage 3 parses/renders the global list into its hidden mount, but its asserted Sauganash/Green Tree entries and popup behavior remain unchanged. Retain those assertions with the explicit limit that they do not validate the added villa entry or global count; fresh 13/14 supply that integration coverage.
- Stage 5's 1835 scene-detail ladder does not load the replaced 1904 model or revised 1904 yard/door inputs. It remains evidence for that unchanged ladder, not the new 1904 rendering cost.
- Stage 12's teacher-handout catalog is byte-identical, including its selected suggestions and printed content. Its About-this-destination path can populate the global liberty tile, whose displayed total now changes, but its assertions concern unchanged card labels/order, living/orderbook navigation, visibility and layout; they do not assert the new numeric count or open the new liberty prose. Fresh 13/14 cover the changed count/content instead. The lesson panel remains unopened and does not read the revised jaunt opening.
- Stage 4's building-specific Sources/Details paths use unchanged inspected 1835 sidecars, not the changed global Sanborn detail.

The follow-up's pure/DOM accessibility and curated hunt logic have no direct source change from this DEV increment. House 2027 is not one of the five curated photo owners, and the picture catalogue/owner sidecars for those rounds are unchanged. Preserve completed results only for their actual logic/input scope. An old full-town 1904 fixture must keep its old provenance; it cannot be relabelled a new merged-scene execution. The required official refresh above covers the changed world integration, not new native gesture implementation.

This analysis does not grant coverage to a stage or follow-up fixture that was missing, failed or incomplete before the DEV advance. Existing feature-specific obligations remain in force.

## Source validation and limitations

The current b1/ddc source receipts are checkpoints for their frozen inputs, not validation of 21f or a future merge. Complete the required source release gate on the actual integrated candidate. At minimum, affected checks include the changed unique-ID validator's `--check` and `--self-test` (called at `check.sh:2304–2307`), structure/scene/asset compilation and publication checks, 1904 yard/door/interior/walk-join joins, global liberties, source-use index/detail consistency, and the changed jaunt opening/compiler audits. The previous statement that all validator definitions were unchanged no longer applies. Refresh the changed tool's required step-isolation evidence according to the existing measurement workflow; an unchanged expected write footprint is not a new measurement receipt.

Fresh 13–15 results would establish their tested integration behavior, not photographic accuracy of the villa, every new doorway/collision path, the exact Sanborn detail contents, or the revised jaunt opening text. Those claims remain with their direct source/data gates and any separately required focused checks. No budget increase, assertion weakening, merge approval or future-tree certification is implied by this review.
