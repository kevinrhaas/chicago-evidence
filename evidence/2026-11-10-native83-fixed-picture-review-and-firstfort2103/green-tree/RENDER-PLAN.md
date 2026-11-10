# T-2376 fixed-camera refresh after grouped native83

Run only after the parent has integrated and verified the authentic grouped native's `green_tree_tavern__frame_1833.glb` and source trial (`shoulder.roof_high_m=4.6`). This is one picture refresh, not another bake, source rewrite or camera solve. Commands were read against the current west checkout; no render was run for this plan.

## 1. Preserve the exact held comparison before overwriting it

```bash
source /tmp/chicago-resume-env-20261109.sh
cd /tmp/chicago-west-wicket-20261109/chicago/4d
python3 - <<'PYTHON'
from pathlib import Path
import hashlib,json
root=Path.cwd()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cam=root/'data/reference_views/green_tree_tavern/andreas_1838.json'
photo=(cam.parent/json.loads(cam.read_text())['photo']).resolve()
held=root/'data/reference_views/green_tree_tavern/andreas_1838.match.json'
pair=root/'docs/RESEARCH/photo-match/green_tree_tavern/andreas_1838-side-by-side.jpg'
assert sha(cam)=='9439f5f7e6f3138e53328647456d332110948ef8421692f951827e48eb274f6b'
assert sha(photo)=='bfaa184f9043ea94560eb74e44926c631f06338bc90e6ba54951a610edef119a'
assert sha(held)=='0edb709f43ed1370c1730227dca78c7c0f359b8a15656b33a2a466a9239efa76'
assert sha(pair)=='ddb7d84654f116be69ed37cd1cc6e57a2f5a315ac53053a92617e20d6e7c93ef'
assert json.loads(held.read_text())['glb_sha256']=='f213818f5a686d31bfbb07217233a7021c514be64b841035d3c29996a380807b'
history=root/'docs/RESEARCH/green-tree-annex-T-2376'
for src,name in [(pair,'andreas_1838-side-by-side-before-shoulder-rise-20261110.jpg'),(held,'andreas_1838-before-shoulder-rise-20261110.match.json')]:
    dst=history/name
    if dst.exists(): assert dst.read_bytes()==src.read_bytes(),f'conflicting existing history: {dst}'
    else: dst.write_bytes(src.read_bytes())
print('Held camera/photo/comparison verified; historical pair and bindings preserved.')
PYTHON
```

The preserved historical match retains its original canonical side-by-side path as evidence of its historical contents, not a new canonical review. Do not enroll that historical record as a separate gate view.

## 2. Render once with exactly the existing camera and source

```bash
node tools/photo_match.mjs data/reference_views/green_tree_tavern/andreas_1838.json
```

The owner selects `assets/gltf/green_tree_tavern__frame_1833.glb`. Do not pass a WEB derivative or a different camera; do not crop, rescale, refit or edit camera `solve`. The source remains the exact 1600×1000 Andreas image. Output is the canonical `docs/RESEARCH/photo-match/green_tree_tavern/andreas_1838-side-by-side.jpg`, 3224×1000 with 24px divider. The renderer writes the adjacent canonical `.match.json`, retains old difference descriptions and resets verdict to `unreviewed` because the MASTER changed. It also emits a small temporary raw PNG path in its log; retain that path for the actual inspection if useful.

## 3. Verify binding before any visual verdict

```bash
python3 - <<'PYTHON'
from pathlib import Path
import hashlib,json
r=Path.cwd();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c=r/'data/reference_views/green_tree_tavern/andreas_1838.json'
m=json.loads(c.with_suffix('.match.json').read_text())
p=(c.parent/json.loads(c.read_text())['photo']).resolve()
g=r/'assets/gltf/green_tree_tavern__frame_1833.glb'
assert sha(c)==m['camera_sha256']=='9439f5f7e6f3138e53328647456d332110948ef8421692f951827e48eb274f6b'
assert sha(p)==m['photo_sha256']=='bfaa184f9043ea94560eb74e44926c631f06338bc90e6ba54951a610edef119a'
assert m['glb']=='assets/gltf/green_tree_tavern__frame_1833.glb'
assert sha(g)==m['glb_sha256']
assert sha(g)!='f213818f5a686d31bfbb07217233a7021c514be64b841035d3c29996a380807b'
assert (r/m['side_by_side']).is_file()
assert m['verdict']=='unreviewed'
f=json.loads((r/'data/structures/green_tree_tavern.json').read_text())['phases'][0]['form']['enclosed_left_annex']['value']
assert f['shoulder']['roof_high_m']==4.6
print(json.dumps({'model':m['glb'],'model_sha256':m['glb_sha256'],'camera_sha256':m['camera_sha256'],'photo_sha256':m['photo_sha256'],'pair':m['side_by_side'],'verdict':m['verdict']},indent=2))
PYTHON
```

## 4. Actually view before adjudicating

Open the new canonical JPG and the preserved before JPG through `view_image`; inspect the shoulder's rise/eave junction against the image at the same framing. Expected data-only change: attachment rises 4.0→4.6m, outer eave remains3.2m, peak4.85m; roof slope12.53°→21.25°. The producer probe changed only eight z coordinates in the shoulder roof/upper infill; no occupied ring, footprint, opening, camera or placement changed. If actual new native shows other visible changes or intersections, investigate rather than accepting from input intent.

Only after viewing, split existing difference row3 honestly: whether the shoulder roof attachment/slope improved or is fixed, and what remains unresolved in the shoulder/connector/turned-range proportions. Existing wider T-2376 picture coverage and Trowbridge open-bay counterevidence remain incomplete. Retain overall `differs` while visitor-visible differences remain. Do not automatically mark the entire compound row fixed or close original T-2376. This isolated asset render does not qualify published terrain, native yards/signage, current WEB, desktop or phone review; parent handles those grouped release checks separately.

## Scope and exact invariant bytes

Only intended refresh writes: canonical JPG and canonical `.match.json`, plus the two historical files above. The original camera and source are read-only. Historical pair479426B; photo970135B; camera1772B. No source/network lookup, native bake, dependency install or GitHub action is needed for these commands.
