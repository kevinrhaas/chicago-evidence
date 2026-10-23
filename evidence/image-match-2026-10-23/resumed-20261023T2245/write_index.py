from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess

WORK = Path(__file__).resolve().parent
def api(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint], text=True))
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
- [PR1239](https://github.com/kevinrhaas/chicago/pull/1239): state `{prs[1239]['state']}`, draft={str(prs[1239]['draft']).lower()}, head `{prs[1239]['head']['sha']}`. The root identified a live automation owner and is respecting its lock. This metadata is not a claim that its latest gate/browser coverage passed.
- School T-2372: resumed actual one-export/one-capture trial darkens the doorway with the existing blind-recess control. Master `de08343a76201c4e7199066b12c285efc28c855b0a84fbcf318796aadba3f8a2`, 496 triangles. Actual source/before/after inspected; verdict **differs**. Frontage, gable cladding, roof, logs/chinks, openings, stack/context and provisional camera remain unresolved. Canonical integration remains separate. The root's resumed recount finds82 current log-family masters including new Ouilmette1812; the older frozen81-family baseline is historical and must not omit the new master.
- Tremont T-2385: three actual native/GPU roof-only factors0.5/0.25/0.125 completed and were directly reviewed. All remain **differs**;0.25 is a preferred bounded next candidate, **unadopted**. Exact18 files plus author manifest are archived; shared328 native inputs remain in the prior frozen packet. The flag still differs and no historical pigment is asserted.
- Wolf Point resumed work and the next school-gable/Tremont producer proposals are ongoing. Only expressly closed packets in the inventory qualify as archived output; no unlisted proposal is called an actual render or adoption.

## Exact archives

Every archive has an internal `ARCHIVE-MANIFEST.json`, an external manifest and a receipt. All selected source hashes are checked, source bytes are re-read during archive writing, and every tar member/hash/size is verified on full readback. Runtime symlinks, node_modules, private indexes, live tmp/logs and bytecode caches are excluded. Original author manifests remain verbatim even when the exact archival subset is smaller; explicit exclusion ledgers explain the difference.

{inventory}

## Resume

Extract only a needed bounded archive and verify its manifest. The school archive preserves the actual runner output, source/camera/master guards and the reviewed-differs/original-unreviewed records separately. Its original314-file author manifest is retained, while35 generated Python cache files are omitted by explicit [selection ledger](SCHOOL-SELECTION.json). All314 original hashes were verified;279 noncache payloads plus author manifest and selection ledger were archived.

Further canonical work belongs on code PRs into dev, with native shared-family rebuilds, full check/preflight and applicable published mobile/desktop verification. Do not promote a research camera or comparison to `matches` through archival storage. Bulk evidence stays in this private repository; chicago-tickets holds small text pointers only.
'''
(WORK / 'RECOVERY.md').write_text(text)
print('Resumed index written with exact archive inventory and read-only PR snapshot.')
