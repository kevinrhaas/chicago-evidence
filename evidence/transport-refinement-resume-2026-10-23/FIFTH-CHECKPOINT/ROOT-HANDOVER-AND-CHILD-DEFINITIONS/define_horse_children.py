from pathlib import Path
import json
root=Path('/workspace/chicago/chicago/4d/tickets')
specs=[
('Repair planted horse eye UVs while preserving its mechanics','S',False,'''## Scope and acceptance

Deliver the bounded dark-eye UV repair to the existing licensed planted-standing
horse, preserving its original body and mechanics. This is not the photographic master.

- Reproduce the versioned d4544c28 derivative from the unchanged b479442c canonical
  baseline using a portable stdlib recipe. Preserve every geometry/normal, rig,
  weight, clip, material and embedded image byte; only the declared ocular UV
  accessor/bounds and explicit derivative notice may change. Reject independent
  non-UV binary/JSON mutations and meaningful destructive controls.
- Root must inspect fixed-camera actual source/candidate textured comparisons on
  both eyes, with all non-eye pixels protected. CPU software-render limitations,
  reconstructed pupil/gaze and the modern model's licence remain explicit.
- Load the exact new SHA through the real GLTFLoader, production clone and Mixer
  at all 65 keys and 64 midpoints with unchanged physical/contact/loop controls.
  Bind the current CPU receipt to its actual fixture; never transfer historical
  b479 browser/world/appearance acceptance to the derivative.
- Update the selected versioned runtime asset and provenance without changing
  placement, natural planted weight shift, budgets or capability/visibility clocks.
  Preserve original assets/receipts and complete integrated app/normal PR gates.

## Saved work

Root reviewed both actual whole-horse quarter comparison pairs. Exact source,
portable recipe, five mutation controls and fresh d454 Mixer129 proof are in
https://github.com/kevinrhaas/chicago-evidence/tree/main/evidence/transport-refinement-resume-2026-10-23
(THIRD-CHECKPOINT and FOURTH-CHECKPOINT). Native/mobile/photographic acceptance
remains open in the sibling master/qualification work.
'''),
('Add a safe viewpoint at the Western Hotel yard horse','S',False,'''## Scope and acceptance

Make the existing 1835 planted yard horse discoverable through a camera-only
viewpoint; do not move the animal or claim a newly attested individual.

- Add the named Western Hotel yard and horse point to the existing 1835 anchor
  data consumed by the viewpoint list and direct anchor URL. Aim its unchanged
  camera convention toward the existing horse coordinate.
- Prove the arrival is on dry ground and outside every roof using the actual
  anchor-ground/roof measurement and regenerated reading. Retain the first
  rejected inside-stable candidate instead of relabeling it accepted.
- Preserve all previous viewpoints, scene date, actor placement and Full/Balanced,
  reconstructed-confidence and Light policies. Complete integrated app and normal
  required PR checks. The parent's native photographic/world qualification remains
  separate; the point itself is a navigation increment, not that acceptance.
'''),
('Refine the horse anatomy and near silhouette against cleared views','M',True,'''## Scope and acceptance

Finish one horse's source-bounded anatomical near master, retaining T-2800's
unmet anatomy/topology and source-comparison requirements. No fleet/breed variants.

- Use cleared anatomical and dated period references to define scale, body
  proportions, head/eyes/ears/muzzle, neck/shoulder, limbs/joints/hooves, mane and
  tail. Keep this a generic working animal, not an identified horse or claimed breed.
- Resolve actual near silhouette/anatomy discrepancies at matched front, profile,
  quarter and detail views. Inspect the actual images and maintain a discrepancy
  register; do not treat the eye-only child as acceptance of the whole head/body.
- Provide a source-bounded canonical master with clean supported topology for
  T-2803. Test metre scale/axes, connected joints and weight-bearing hoof contact;
  every changed geometry/skin must have fresh protected-source and exported proof.
- Retain rights/modern attribution, per-attribute confidence and liberties for
  coat, grooming, unknown dimensions and unpictured features. Do not derive from
  rights-pending references or invent Chicago ownership.
- Use the supported canonical build path, without installing Blender on the
  improve runner. Hand exact accepted master hashes to the surface/LOD sibling.
'''),
('Qualify horse surface materials and portable distance exports','M',True,'''## Scope and acceptance

Qualify the single accepted anatomical master from the sibling anatomy child as
the full static photographic/portable horse delivery originally required by T-2800.

- Skin/coat, eyes, muzzle, hair and hooves must read at near view. Use browser-suitable
  mane/tail geometry and materials, declared reconstructed colour/grooming, and
  preserve the accepted exact anatomical shape unless a new proof accompanies it.
- Produce compressed near/mid/far GLBs, engine-neutral sidecars, tested metres/axes,
  licence provenance and bounded material/texture reuse through the supported
  export pipeline. A single unqualified near GLB is not complete.
- Compare actual native front/profile/quarter/detail renders with cleared reference
  plates at the same views, inspect the images, resolve the discrepancy register
  and record which surfaces/dimensions/colours remain reconstructed.
- Load the exact published exports in current desktop and phone browsers; measure
  triangles, materials/draws, textures/memory, bytes and frame cost at unchanged
  caps, including near/mid/far transitions and actual placement/support clearance.
- Complete normal source and published desktop/mobile qualification. Do not infer
  walking/trot, tack, riders, teams, driving or boarding from a static-animal pass;
  those remain the existing T-2803/T-2804 and gear/traffic tickets.
''')]
found=[]
for title,effort,bake,body in specs:
    matches=[]
    for path in root.glob('T-3000-3249/T-*.md'):
        text=path.read_text()
        if '\nparent: T-2800\n' in text and '\ntitle: '+title+'\n' in text:
            matches.append((path,text))
    assert len(matches)==1,(title,len(matches))
    path,text=matches[0]
    marker='**Acceptance:** (state it before working — one demonstration, never weakened to pass)'
    assert text.count(marker)==1
    text=text.replace('effort: S\n','effort: '+effort+'\n',1)
    text=text.replace('needs_bake: false\n','needs_bake: '+str(bake).lower()+'\n',1)
    path.write_text(text.replace(marker,body.strip(),1))
    found.append({'id':text.split('id: ',1)[1].splitlines()[0], 'title':title, 'file':str(path)})
parent=list(root.glob('T-2750-2999/T-2800-*.md'))[0]
with parent.open('a') as out:
    out.write('\n\n## Preserved scope after split — 2026-10-23\n\n')
    for row in found:
        out.write(row['id']+' — '+row['title']+'.\n\n')
    out.write('The eye and viewpoint children are bounded increments only. The anatomy and\nsurface/portable children retain every unmet original photographic/master/LOD\nrequirement above. Existing planted-standing DEV delivery is credited history;\nthis parent is not photographic done, and no animation/interaction acceptance\nis manufactured by the split.\n')
Path('/workspace/shared/ROOT-TRANSPORT-INTAKE-20261023-2315/HORSE-CHILD-IDS.json').write_text(json.dumps(found,indent=2)+'\n')
print(json.dumps(found,indent=2))
