from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess
import sys

WORK = Path(__file__).resolve().parent
def api(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint], text=True))
if '--offline-snapshot' in sys.argv:
    snapshot = json.loads((WORK / 'PR-SNAPSHOT.json').read_text())
    prs = {int(n): {**p, 'head': {'sha': p['head']}} for n, p in snapshot['pulls'].items()}
else:
    with ThreadPoolExecutor(max_workers=2) as pool:
        prs = dict(zip([1229, 1239], pool.map(api, [f'repos/kevinrhaas/chicago/pulls/{n}' for n in [1229, 1239]])))
    snapshot = {
        'at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Read-only publication snapshot, not new validation or ownership. Live CI may change.',
        'pulls': {str(n): {'number': n, 'state': p['state'], 'merged': p['merged'], 'draft': p['draft'], 'head': p['head']['sha'], 'merge_commit_sha': p['merge_commit_sha'], 'labels': [l['name'] for l in p['labels']], 'html_url': p['html_url']} for n, p in prs.items()},
        'no_original_picture_acceptance_claimed': True,
    }
    (WORK / 'PR-SNAPSHOT.json').write_text(json.dumps(snapshot, indent=2) + '\n')
rows = json.loads((WORK / 'ARCHIVES.json').read_text())
inventory = '\n'.join(f"- [{r['name']}](archives/{Path(r['archive']).name}) — {r['source_file_count']} selected files, archiveSHA256 `{r['sha256']}`, {r['readback']}. {r['scope_note']}" for r in rows)
text = f'''# Resumed picture-work recovery — 23 October 2026, 22:45 UTC

This is a new resumed-work checkpoint. Prior frozen evidence remains unchanged at [final27-archive checkpoint6d4df2f](https://github.com/kevinrhaas/chicago-evidence/blob/6d4df2f307067a664beb00f336138110d3ce5ed2/evidence/image-match-2026-10-22/final-parallel-recovery-20261023T1430/RECOVERY.md). The user renewed permission to continue after the cloud pause.

**No original T-2372 through T-2388 is certified as an image match by this checkpoint.** Actual comparisons and prepared/unrun work are labelled separately. Prototype exports are not canonical adoption.

## Current work and PR anchors

Read-only metadata snapshot: `{snapshot['at_utc']}`; raw summary is [PR-SNAPSHOT.json](PR-SNAPSHOT.json).

- [PR1229](https://github.com/kevinrhaas/chicago/pull/1229): merged={str(prs[1229]['merged']).lower()}, head `{prs[1229]['head']['sha']}`. This is Hogan's visible first increment; original T-2377 still requires image matching. Do not reconstruct that landed increment from old scratch files.
- [PR1239](https://github.com/kevinrhaas/chicago/pull/1239): state `{prs[1239]['state']}`, draft={str(prs[1239]['draft']).lower()}, head `{prs[1239]['head']['sha']}`. Initial resumed work respected its then-live owner. A later closed read-only packet records that owner completed at23:01:42 and actual hosted1060PASS for merge20455(sourcea219+dev5f15). Root owns further lock/dependency/merge decisions; this is not browser or other-target approval.
- School T-2372: resumed actual one-export/one-capture trial darkens the doorway with the existing blind-recess control. Master `de08343a76201c4e7199066b12c285efc28c855b0a84fbcf318796aadba3f8a2`, 496 triangles. Actual source/before/after inspected; verdict **differs**. Frontage, gable cladding, roof, logs/chinks, openings, stack/context and provisional camera remain unresolved. Canonical integration remains separate. The root's resumed recount finds82 current log-family masters including new Ouilmette1812; the older frozen81-family baseline is historical and must not omit the new master.
- School's next front-gable trial actually exported/captured once at the same camera, master `fe73a03a135811179b47ac603bf4169b35d1b0cc8b8d595d144885053189a8d8`,528triangles. Horizontal courses continue through the former plain triangle; all other raw polygons equal the actual blind-door baseline. Direct source/full/detail review remains **differs**, still **unadopted**. Exact680 noncache files plus originalmanifest include the4-file proposal, libertyCover, actual barePNG doorbaseline, raw/snapshot and real receipts. Historical81/51positional checks do not establish current82-family integration.
- Tremont T-2385: three actual native/GPU roof-only factors0.5/0.25/0.125 completed and were directly reviewed. All remain **differs**;0.25 is a preferred bounded next candidate, **unadopted**. Exact18 files plus author manifest are archived; shared328 native inputs remain in the prior frozen packet. The flag still differs and no historical pigment is asserted.
- A separate Tremont quarter-roof-stock producer proposal is **UNAPPLIED**:14closed files plus originalmanifest,4guarded existing-file candidates and16CPU/24rawphase parity/schema checks. Official23-family rebake, fullgates and native adoption were not run. It is not another actual capture or a historical pigment claim; recover from recorded792base plus guardedpatch.
- Tremont's subsequent single-flag pictorial pose has one successful actual native/GPU capture and reviewed **differs** result. The trial preserves global `WIND_FROM225`, holds the quarter-roof and all other controlled inputs, and applies only a per-flag pictorialTO105.6 override. It remains **unadopted**, with no historical wind claim. The initial signed-zero(-0/+0) harness failure, original runner/inputs, separate finite numeric-only normalization helper and expressly granted retry are preserved together.351closed files plus originalmanifest are archived. These controlled native-module/GPU diagnostics are not whole-town published-app validation.
- Wolf Point roof-relief experiment now has a closed actual comparison, **differs**, approximately40,000 triangles, **NOT RECOMMENDED / UNADOPTED**. Exact716 final files plus author manifest preserve the original405-file historical prepared set separately from306 actual-run files and final handoff. The integration baseline excludes this experimental roof. No additional trial was made after the granted run.
- T-3081's frozen log-family baseline12KW engineering plan is archived separately:154files plus manifest against dev5f15, five visible models and82 current masters, default/Hogan/source/Covers/provenance proof and authored patches. It is **UNBAKED**: the plan did no official family bake, browser, whole gate or canonical write. The root's separate live integration directory is intentionally not selected for archival until its owner closes it.
- A closed native-purefill lodging study preserves the Wolf-L risk and V2 dependency proof: olddev allocation churns13retired/12new/2movedpeople/5movedseats, while testedV2 inputs preserve22households/157people/52seats/counters.24canonicalinputs were double-hashed under write denial and orderbook6c5e9e stayed unchanged. The study launched no native writer, browser or new whole gate; its separate raw hostedCI transcript proves the dated1060PASS only for its explicitly bound merge candidate.
- Root T-3081 authored-only recovery is a separate closed20-file snapshot plus manifest, based on5f15:18authored files, patch and README. It was **UNCOMMITTED / UNBAKED** at capture, with native consumers and fullgates pending and PR1239V2 required before population writers. Changelog kind was validated. This is recovery material, not a code PR, official82 bake, readiness or image-match verdict; no live root tree was selected.
- A separate read-only applied82 audit checks all82 default-off raw/material/confidence outputs, the528triangle school candidate, Hogan/Ouilmette byte guards and the raw license prefix/append. Its native manifest check lists201steps/415files; it did not execute native consumers. This is a dated audit, **NO APPROVAL**, preceding the official bake below.
- The five-model published QA helper is **PREPARED, NOT BROWSER EXECUTED**:19closed files plus manifest contain syntax/dry-mode checks, authored records, existing provisional cameras, path-only portable copies and source images. It makes no new solve, accepted match or published-app verification claim.
- The guarded graft helper is **PREPARED, NOT CANONICALLY APPLIED**:25closed files plus manifest and45LIGHT checks cover actual disposable grafts and preimage/HEAD/index/no-partial-write guards. It binds the older18-file authored snapshot and intentionally refuses the root liveSTATUS wording change. It supplies no native/browser/fullgate result.
- A separate Tremont a219 follow-up plan is **LIGHT, UNAPPLIED / UNBAKED**:13closed files plus manifest bind the23-master inventory and earlier CPU parity to an authored integration/build plan and draft documents. Original T-2385 remains open/differs, the flag pose remains unadopted, and rights were not upgraded.
- Root T-3081 official82 master/web generation now has its own expressly closed650-file packet plus manifest. Generation exited0;76 masters are byteexact, five have intended visible changes, and one Kinzie stable master has a reviewed UV-only delta reproduced by both old/new official controls.77 web outputs are byteexact and only the five intended outputs change; all four Hogan guards remain exact. Generator/record bindings,18authored changes, native produced manifests, logs, original stamps and actual UV controls are included. **Native consumer execution, published browser QA and full gates remain pending.** This official bake is distinct from earlier unbaked plans and does not certify adoption or original picture matches.
- Two later PR1239 read-only checkpoints bind the96ca/e5 stack. The first preserves87 original guards, exact V2 tools and the rawLIBERTIES a219 prefix plus2849byte Glessner append, with checks still pending at that capture. The second preserves the actual hosted1060PASS transcript for job120710578230/run40040620666 and exact merge1266bb91e4fcbddb9b6ff90d4e212df0ec4ea4b5. Its snapshot still has moving-frames pending, a draft/open PR and live owner. Neither snapshot supplies final approval; the earlier20455 result remains historical.
- A separate reviewedLIBERTIES-exception helper is frozen **NOT APPLIED AT CAPTURE**:29closed files plus manifest require the exact incoming d872 hash, preserve the entire a219 prefix and2849byte Glessner append, and then append only the12owned records. The general helper remains unchanged. Later actual root graft/native execution belongs in its own closed receipt.
- Tremont utility T-3082 has a new19-file authored integration recovery plus manifest on96ca, **UNCOMMITTED / UNBAKED** at capture. It includes the authored patch, separate e5ed fold patch, ticket/entry, raw documentation guards,23recipe documentation, protected unrelated bytes and an old-cache move receipt. The258999416byte old cache is already committed at792 and is excluded. No native browser/fullgate/PR or original picture acceptance is claimed.
- Wolf's future data-only roof-finish/native-relief study is **LIGHT / UNRENDERED / UNADOPTED**:223closed files plus manifest bind current82 pure geometry/default/material guards and frozen prior actual-before inputs. It adds no T3081 scope, official bake, native/heavy run or canonical change. The earlier approximately40000triangle experimental roof remains rejected.
- Further producer/integration work is ongoing. Only expressly closed packets in the inventory qualify as archived output; no unlisted proposal is called an actual render or adoption.

## Exact archives

Every archive has an internal `ARCHIVE-MANIFEST.json`, an external manifest and a receipt. All selected source hashes are checked, source bytes are re-read during archive writing, and every tar member/hash/size is verified on full readback. Runtime symlinks, node_modules, private indexes, live tmp/logs and bytecode caches are excluded. Original author manifests remain verbatim even when the exact archival subset is smaller; explicit exclusion ledgers explain the difference.

{inventory}

## Resume

Extract only a needed bounded archive and verify its manifest. The school archive preserves the actual runner output, source/camera/master guards and the reviewed-differs/original-unreviewed records separately. Its original314-file author manifest is retained, while35 generated Python cache files are omitted by explicit [selection ledger](SCHOOL-SELECTION.json). All314 original hashes were verified;279 noncache payloads plus author manifest and selection ledger were archived.

Further canonical work belongs on code PRs into dev, with native shared-family rebuilds, full check/preflight and applicable published mobile/desktop verification. Do not promote a research camera or comparison to `matches` through archival storage. Bulk evidence stays in this private repository; chicago-tickets holds small text pointers only.
'''
(WORK / 'RECOVERY.md').write_text(text)
print('Resumed index written with exact archive inventory and read-only PR snapshot.')
