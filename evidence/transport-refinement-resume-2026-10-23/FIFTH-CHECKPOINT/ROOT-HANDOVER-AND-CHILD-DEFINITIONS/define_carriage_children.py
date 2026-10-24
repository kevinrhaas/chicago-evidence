from pathlib import Path
root=Path('/workspace/chicago/chicago/4d/tickets')
def append_acceptance(ticket, effort, body):
    files=list(root.glob('T-3000-3249/'+ticket+'-*.md'))
    assert len(files)==1
    path=files[0]; text=path.read_text()
    marker='**Acceptance:** (state it before working — one demonstration, never weakened to pass)'
    assert text.count(marker)==1
    text=text.replace('effort: S\n','effort: '+effort+'\n',1).replace(marker,body.strip(),1)
    path.write_text(text)
append_acceptance('T-3083','S','''## Scope and acceptance

Deliver one bounded lamp-form refinement to the existing reconstructed 1904
1893-catalogue Brougham. This child does not close its parent's photographic master.

- Replace the tall angular coach-lamp heads with rounded upper housings and narrower
  lower bodies, comparing fixed actual V17/V18 mesh projections with the unchanged
  cleared 1893 catalogue plate. Root must inspect both full-quarter and detail pairs.
- Preserve all non-lamp geometry streams, existing materials, nodes, anchors,
  wheel/pole contacts, original near collision proxy, parked placement and runtime
  reach/selection/resource policies. Reproduce and independently validate the new
  near and genuine mid exports; reject stale receipt/acceptance metadata.
- Bind current source, assets, licences and receipts to V18. Preserve V17 producer
  and qualification history separately. CPU software-form review must never be
  labeled native Three PBR, photographic or published world acceptance.
- Complete the integrated app gate and normal required PR checks before DEV merge.
  Native materials/photo matching and full world qualification remain T-3084/T-3085.

## Saved work

Actual C3 near/mid/LOD and negative-control receipts, independent 28-file intake,
and root-reviewed CPU lamp comparisons are backed up in
https://github.com/kevinrhaas/chicago-evidence/tree/main/evidence/transport-refinement-resume-2026-10-23
(THIRD-CHECKPOINT). Original browser and OCI nonpasses remain preserved.
''')
append_acceptance('T-3084','M','''## Scope and acceptance

Finish the single already-selected Brougham's source-matched near appearance,
retaining every photographic/material requirement of T-2794 not satisfied by
the bounded T-3083 lamp refinement. This is one specimen, not a fleet or era variants.

- Credit the existing cleared 1893 Studebaker catalogue design selection, exact date
  interval and rights. Do not invent this carriage's maker, ownership or Chicago presence.
- Match separate wheels/front steering, body, suspension, fixed pole/shafts,
  steps/doors and seats to what the actual plate shows. Upholstery, wood, leather,
  iron and glass must read correctly at conversation/boarding distance. Resolve the
  remaining body/window/paint discrepancies instead of calling the current model complete.
- Compare actual native side/front/rear/three-quarter and detail renders at matched
  reference cameras. Maintain a discrepancy register and inspect the images themselves.
  Record hidden interiors, dimensions and black-and-white colour choices as liberties.
- Keep portable metres/axes, existing contacts/anchors/proxy and prior source protections;
  any necessary revision must carry its own exact export and fresh proof.
- Complete normal source gates. Hand the accepted exact asset hashes to T-3085 for
  physical-interface, portable LOD and published phone/desktop qualification.

The parent retains the entire original ask, sources and all historical increments.
No photographic acceptance exists merely because T-3083 merges.
''')
append_acceptance('T-3085','M','''## Scope and acceptance

Qualify one source-matched Brougham from T-3084 as a portable parked-town delivery.
Read T-2794 and the accepted exact T-3084 source/asset hashes before starting.

- Export supported portable master/LOD GLBs and engine-neutral sidecars, with tested
  metres/axes, licence provenance and documented visible/hidden reconstructions.
- Verify named passenger/driver seats, boarding/rein/hitch anchors, separate wheel
  and steering hierarchy, documented doors/entry clearances and the conservative
  collision proxy required by the parent's later interaction interfaces.
- Measure actual source and compressed published near/mid/far bytes, triangles,
  draws, textures/memory and frame cost in current desktop and phone scenes. Inspect
  native views and placement/body/pole/ground/tree clearance at unchanged caps.
- Retain existing wagon stands and eligibility; unknown owner/maker remains declared.
  Finish the parent's matched-render discrepancy and phone/desktop loading receipts
  on the exact accepted exports. A prior LOD-only appearance pass does not transfer.
- Complete normal integrated and published desktop/mobile gates before DEV merge.
  Door operation, occupied teams, traffic, boarding gameplay and riding remain their
  existing later interaction tickets; this child proves the parent's static interfaces.
''')
parent=list(root.glob('T-2750-2999/T-2794-*.md'))[0]
with parent.open('a') as out:
    out.write('''\n\n## Preserved scope after split — 2026-10-23

T-3083 owns the bounded rounded-lamp delivery only. T-3084 retains this specimen's
complete source-matched near appearance/materials and discrepancy register.
T-3085 retains portable distance delivery, physical interaction interfaces and
native published phone/desktop qualification. Every original acceptance clause
above remains binding across those children; this parent is not photographic done.
''')
print('Defined T-3083/T-3084/T-3085 and preserved full T-2794 scope.')
