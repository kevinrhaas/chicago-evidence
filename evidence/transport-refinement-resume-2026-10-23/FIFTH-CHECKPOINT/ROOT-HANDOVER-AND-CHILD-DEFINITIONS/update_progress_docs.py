from pathlib import Path
import hashlib, json

root = Path('/workspace/chicago-waistcoat/chicago/4d')
status = '''## T-2794 / T-2800 — rounded carriage lamps and horse viewpoint (2026-10-23)

The reconstructed 1904 Studebaker-catalogue Brougham now has rounded coach-lamp
heads and narrower lower bodies. Current V18 assets contain 33,374 near and
11,706 mid triangles. Independent binary review preserves all 450 near and
284 mid non-lamp occurrences, materials, anchors, contacts and the original
near collision proxy. Current receipts bind the new assets; the archived V17
appearance acceptance is historical and is not transferred to V18.

The installed near/mid and actual Three-loader card/LOD checks pass. A matched
CPU software projection of the actual V17/V18 meshes was visually reviewed
against the untouched 1893 catalogue plate and supports the limited lamp-form
improvement. It does not qualify Three PBR materials, native desktop/mobile
appearance, photographic matching, world clearance or published world budgets.
Both browser attempts failed before any app frame because Chromium could not
create threads. A separate isolated-container attempt failed at OCI process
startup; none of those attempts produced native acceptance.

The 1835 viewpoint list gains “Western Hotel yard and horse”, aimed at the
existing planted-standing horse. The corrected arrival point passes the actual
anchor ground/roof check. This is a camera-only discoverability change; its
first candidate was inside the stable and that failed measurement is retained.

The existing planted horse was merged through normal green PR #1244 into DEV
as fa115d72534e234fe5ac7b94fd2f1a3eb38065c8, and public asset hashes were verified.
That exact prior commit's CI does not qualify this new refinement. Fresh final
source preflight and normal required PR checks remain necessary before merging.
Photographic anatomy/materials, native published inspection, walking, tack,
teams, occupants, riding and boarding remain open under the existing tickets.

'''
roadmap = '''### Rounded Brougham lamp form and horse access — T-2794/T-2800, 2026-10-23

V18 changes the reconstructed catalogue Brougham's lamps to rounded upper
housings and narrower lower bodies, at 33,374 near / 11,706 mid triangles.
Actual non-lamp geometry, materials, contacts, anchors and the original near
collision proxy remain protected. Matched software mesh projections reviewed
against the original 1893 plate support only this limited form improvement;
native rendering, photographic matching, world clearance and published budgets
remain unqualified. Historical V17 visual acceptance is retained separately.
The existing 1835 yard horse gains a viewpoint whose arrival passes the ground
and roof check. These increments do not close photographic, gait, gear,
occupied-team, driving, riding or boarding acceptance. The queue remains the
operational work order; no acceptance box or queue rank changes here.

'''
receipt = {}
for relative, prefix in [('docs/STATUS.md', status), ('docs/ROADMAP.md', roadmap)]:
    path = root / relative
    original = path.read_bytes()
    encoded = prefix.encode('utf-8')
    assert not original.startswith(encoded), 'Refuse duplicate progress entry'
    path.write_bytes(encoded + original)
    assert path.read_bytes()[len(encoded):] == original
    receipt[relative] = {'original_sha256': hashlib.sha256(original).hexdigest(),
                         'new_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'original_bytes_preserved': True}
print(json.dumps(receipt, indent=2))
