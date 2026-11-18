# T-3657/T-3658 integration update — DEV c676aa2f

Updated 2026-11-18 23:45 UTC. Git-object preparation only; no branch, real index, worktree,
ticket, test, publisher, browser or workflow changed by this review.

## Exact objects and preserved changes

- New DEV: `c676aa2f4ad6ee8cff0521da6ba8add70d55949c`.
- Original primary: `5034a724d993abe0876a4db7bbfff02d2bb4da0a`.
- Actual integrated primary: `b1f507400cb743a3985cb1d50de1ebd085bd4f63`,
  parents 5034+c676, tree `858aa04a6f34329f71efbbe0c472ad5902fea23b`.
  A separate conflict-free Git merge-tree calculation produced exactly that tree.
- Pushed follow-up checkpoint: `6ee1a689077839dd9923edbc80269dd2cbaccfb6`.
- QA checkpoint: `b501bfcbc9a9ecb38c7bed76efe35a48165b061b`.
- Updated normalized follow-up tree:
  `d8df5af979b82a6206f71d68bf52fa67f3dca99f`.

The existing 24-file patch /tmp/t3657-t3658-normalized-followup.patch applied cleanly
through a separate temporary index onto858aa04a and produced d8df5af9. Its bytes are
unchanged. Every one of the 46 paths changed by new DEV versus169404 has the exact new DEV
blob in BOTH candidate trees. Historical → new primary and historical→new follow-up
diffs byte-match169404→c676. No upstream change was discarded or rewritten.

Application code, CSS and markup outside changelog.js remains equal to QA b501. Assets, data and
generators are now intentionally newer; QA is not blanket evidence for these inputs.

Artifacts:
- /tmp/t3657-t3658-rebase-c676-provenance.json (machine-readable assertions)
- /tmp/t3657-t3658-rebase-c676-prediction.index (separate temporary index)
- /tmp/t3657-t3658-normalized-followup.patch (unchanged 24-file delta)
- /tmp/t3657-t3658-rebase-plan.md and -provenance.json remain HISTORICAL169404 proof.

## Exact runtime impact

c676 adds the T-3594 monument model, its asset manifest hashes, picture-match evidence,
generator changes, revised monument liberty prose, a regenerated1904 build-log jaunt and
catalog,24 source-detail backlink files, and the folded release entry.

- Monument model: the 1893–1931 phase is listed under excluded_by_date in1812 and1835.
  Only1904's drawn structures list names its changed GLB. Together with earlier T-3562,
  the integrated primary has three changed1904 model masters/derivatives relative to5034.
  No1812/1835 geometry changed.
- Build-log jaunt: same 50 destinations; the monument moves from 43rd to3rd. Versions,
  links, timing and evidence indices regenerate. Only prairie-built-so-far changes in
  the 1904 catalog's96 rows; no jaunt is added or removed.
- Sources: all 24 changed1835/sources detail files change only 66 edges[].claim strings.
  Every changed edge belongs to entity prairie-built-so-far. All other fields, list
  lengths and source identities match. These files serve source detail across scenes;
  the 1835 path does not mean1835 geometry changed.
- Liberties: only fields[2].text of existing L-fort-dearborn-monument-3567 changes.
  The global count, title, subjects and all 1835 building-specific records are identical.

## Behavioral reach and retained evidence

| Stage/surface | Actual changed dependency and interpretation |
| --- | --- |
| Desktop1–12 source details | None opens these 24 source-detail files. sources.js96–99 lists unchanged sources/index.json and uses.json; individual edges load only at openDetail159. Stage 3 citations9072–9157 use unchanged Sauganash sidecar citations. Stage 4 Sources pane10640 uses unchanged Hogan/Inspect joins. Stage 12 opens living then orderbook at 15082/15108, not source details. |
| Stage 3 liberties | loadLiberties at 9262 renders the whole array into a hidden mount via main 4114/liberties 230, so changed bytes are parsed. Assertions inspect only unchanged Sauganash and GreenTree subsets. The hidden monument paragraph does not change asserted text, counts or layout. Retain those assertions; do not claim they validate the new monument paragraph. |
| Stage 12 teacher handout | Guide fetches all three catalogs at guide-view125/main 7006. All961904 rows have identical complete consumed projection: id,title,availability,audience,version_of,featured,stop_count,premise. teacher-handout29–53 selects/sorts/projects only those values. The same three suggestions, order and printed text result; it does not open the revised 50-stop document. |
| Stage 13 | Changed folded changelog: import/title/date/unread/returning-visitor checks at 18864–18968 need new merged-input proof. Existing budget restoration evidence on5034 remains scoped to that runtime. |
| Stage 14 | New1904 model bytes and global liberty UI: /1904/ boot20676, exact placed set21143 including monument21139, review annotations21825–21834, loader errors and spawn budget21835–21840. |
| Stage 15 | Real1835→1904 transfer22173–22230 loads the new models and tests arrival/Confidence restoration. It does not walk the revised build-log route. |
| Shared boot/manifest/vendor checks | Each new selected invocation repeats its own boot and final errors/vendor tail. No new geometry is introduced into the default1835 scene. |

Root chose behavioral equivalence for prior desktop 1–12 and mobile 1, with the explicit
limits above, rather than repeating stages only because unused fields or hidden prose
were fetched. Fresh merged-input 13–15 remain necessary on both viewports. Root dispatched
b1 desktop 13–15 run 44422884843 and mobile 2–15 run 44422910837; this document records dispatch,
not successful results. Existing moving/upload success on400ac5f8 belongs to old DEV;
it is not relabelled as b1 evidence.

## Source validation

The complete tools subtree and CI workflow blob are identical between5034 and b1.
Step definitions and partition assignment therefore do not change, but data/model inputs do.
All eight source parts remain required on the actual merged candidate; earlier400ac source
passes must not be relabelled as b1 passes.

Direct checks include image_gate.py --check, monument_emit.py --check, validate.py --all,
compile_liberties.py --check, compile_scene.py --all --check, jaunt_built_so_far.py --check,
compile_jaunts.py --check, jaunt_reading_level.py --check, audit_jaunts.py,
audit_jaunt_refusals.py, check_jaunt_demolitions.py, compile_source_use.py --check,
the shared published-GLB checks and published-asset checks. They cover current metadata,
re-derived route/order/backlink joins, assets and provenance. Stages 14/15 are integration
coverage, not photographic face-match proof or a traversal of all 50 changed route stops.
The existing image records/source gates remain the evidence for those respective claims.

## Final follow-up after primary squash/fold

Keep the original one normalized cherry-pick plan; substitute current objects:

1. Record actual primary squash S and folded DEV D. Require S tree 858aa04a and S ancestor D.
   If unrelated new DEV commits arrive, refresh this object proof before proceeding.
2. Make an aggregate local commit with tree d8df5af9 and parent S. It contains exactly the
   unchanged 24-file follow-up delta, already derived from pushed follow-up+parent repairs.
3. Cherry-pick it onto a clean detached D, preserving the pushed6ee branch as checkpoint.
4. Preserve D's changelog.js verbatim and T-3656.json removal; T-3657.json remains pending.
   Verify all upstream data/assets/generators unchanged from D. Compare final feature
   code to d8df5af9 and classify actual fold/DEV differences before reusing QA evidence.
5. Complete required base-sensitive checks and the changed-input renderer/source proof,
   then update the existing follow-up PR once with an explicit remote-head lease.

DO NOT merge the old QA history directly using boundary 03ecd on latestDEV: the configured
changelog driver treats the new published T-3594 entry as “ours” and unstamps it. The
discarded exploratory tree a3e43c56eff6f86d24ee8cc2e3a022f7c157e840 demonstrates that hazard.
The24-file normalized delta never touches changelog.js or any upstream asset/data path.

No claim here pre-certifies future squash/fold objects, new DEV changes, or unfinished runs.

