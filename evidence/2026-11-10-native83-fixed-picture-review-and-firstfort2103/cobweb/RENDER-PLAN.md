# Cobweb grouped-native picture comparison: fixed private camera

Prepared 2026-11-10 for `/tmp/chicago-west-wicket-20261109`, grouped branch `steward/t2374-t2376-t2380-picture-increments-20261110`; source HEAD at retained before capture `42db9ce562201f64a1ba334a3ce7b4c6a9a70c07`. This is an external-only run plan. No browser or source/GitHub mutation was performed to prepare it. Parent owns the GPU slot and must run the browser captures serially with other native/browser work.

**Actual old bytes are now saved** in `/tmp/nov10-cobweb-before/`: old MASTER, old WEB, literal camera, held model/source fixed crops, full source, prior recovery text, and `RECEIPT.json` identifying source head and hashes. Seven copied files total 842198 bytes. These are read-only copies of existing evidence, not a fresh browser capture. This archive survives native adoption; do not recopy the new MASTER over `before-master.glb`.

**Execution update:** parent granted GPU and the fixture setup plus fresh old render/preservation/review are now complete. Do **not** rerun the one-time setup or before-capture blocks. Actual fresh baseline is `/tmp/nov10-cobweb-picture/before/`, including `capture-receipt.json` and `REVIEW.md`. Fresh bare render and fixed crop reproduce prior qualified bytes exactly. GPU released; `/tmp/nov10-cobweb-picture/after/cobweb-private.json` is prepared with unchanged camera bytes for the next grant after actual native adoption.

**Final execution update:** parent subsequently adopted actual native HEAD `47f5ecbbe3a15cd0011eb6d87a619e4bd0144c4f` and granted GPU. Exactly one after capture, unchanged crop, full review and receipts are complete in `/tmp/nov10-cobweb-picture/after/`. The external private reviewed verdict is **DIFFERS**, with exact originally unreviewed tool output preserved separately. GPU released. Do not rerun either capture or preservation block over these retained outputs; both actual stages are complete. See `after/REVIEW.md` for hashes and limits.

The new lower clapboard band is a bounded reconstructed finish increment. T-2374 remains OPEN / PARTIAL / DIFFERS. This private, unsolved camera stays outside `data/reference_views`; do not change its literal bytes, enroll it, promote grade, or mark the new private match `matches`.

## Exact held inputs and prior proof

- Camera: `/tmp/nov9-cobweb-group/private-camera-used.json`, 1525 bytes, SHA256 `07f94fa8654e1c0469ad4d3df2c0c01414e15ce5cfabcdadde9260a942ea4977`.
- Full source: `/tmp/chicago-west-wicket-20261109/chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg`, 614551 bytes, 1920×1042, SHA256 `624d8f1f52a75bf30653e8cbf37a388478b0ddf5a02f1fadf727cf2144b84c3f`.
- Existing before MASTER: `chicago/4d/assets/gltf/cobweb_castle__log_1820.glb`, 139248 bytes, SHA256 `1ddf548d9a378167163d6db45e5d89e1b4c544ea176355eb7061dd99d6a1ee82`. Rechecked before plan creation. Do not assume it remains before once native adoption starts.
- Existing before WEB: `chicago/4d/assets/web/cobweb_castle__log_1820.glb`, 30304 bytes, SHA256 `99997b5f3935ceceddb072286387859a5d9a8dd3dfa112b64978d1213e20890e` (earlier packet receipt).
- Prior repaired same-camera bare render SHA256 `fe496a9fef4df97e6649a0e5a6df0473721e392c5d0507353f6b072c77e7c1c7`; held 8× model crop `/tmp/nov9-cobweb-group/current-private-crop.png`, SHA256 `76920874cce6fc8ee17ba92313ca3aaa6f761df8c045288be6520bcb1c10b9e1`.
- Held 8× source crop `/tmp/nov9-cobweb-group/source-private-crop.png`, SHA256 `955124dee76ee2d5585e0461688d9c141cad79a25d192248d8fca7c4377d4750`.

Exact old fixed rectangle is **[1380,330,1500,420]**, right/bottom exclusive, resized **960×720 using nearest-neighbor**. Verified in prior [qualified PR1690 recovery packet](https://github.com/kevinrhaas/chicago-evidence/blob/main/evidence/cobweb-2026-11-04/pr1690-exact-resume-depth-repair-qualified-41766/RECOVERY.md), Git blob `ceb1166077f5ee0f83968d86f85654bb3e43048b`. Readonly local copy: `/tmp/nov10-cobweb-prior-recovery-readonly.md`. Applying that exact recipe to the held full source reproduced the old source crop bytes/hash above in memory; no new crop file was written.

## One-time external fixture setup

Run this once. It fails instead of overwriting an earlier capture. Alias resolves the camera's unchanged literal `../chicago/chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg` from both stage directories. Nothing is written inside the repo.

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, shutil
root=Path('/tmp/nov10-cobweb-picture')
repo=Path('/tmp/chicago-west-wicket-20261109')
camera=Path('/tmp/nov9-cobweb-group/private-camera-used.json')
source=repo/'chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(camera)=='07f94fa8654e1c0469ad4d3df2c0c01414e15ce5cfabcdadde9260a942ea4977'
assert sha(source)=='624d8f1f52a75bf30653e8cbf37a388478b0ddf5a02f1fadf727cf2144b84c3f'
root.mkdir(exist_ok=False)
(root/'chicago').symlink_to(repo,target_is_directory=True)
for stage in ('before','after'):
    folder=root/stage; folder.mkdir()
    shutil.copy2(camera,folder/'cobweb-private.json')
    assert (folder/'../chicago/chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg').resolve()==source
print(root)
PY
```

## Capture before BEFORE replacing the old MASTER

Only run when parent gives the GPU slot. The assertion prevents a mislabeled after-as-before. `photo_match` auto-selects the MASTER via manifest; this private camera has no additional members. Its local server only serves files within the app root, so an arbitrary `/tmp/old.glb` supplied via `--glb` will fail.

```bash
source /tmp/chicago-resume-env-20261109.sh
cd /tmp/chicago-west-wicket-20261109/chicago/4d
python3 - <<'PY'
from pathlib import Path
import hashlib
p=Path('assets/gltf/cobweb_castle__log_1820.glb')
assert hashlib.sha256(p.read_bytes()).hexdigest()=='1ddf548d9a378167163d6db45e5d89e1b4c544ea176355eb7061dd99d6a1ee82'
assert not Path('/tmp/nov10-cobweb-picture/before/render.log').exists()
PY
timeout 570s node tools/photo_match.mjs /tmp/nov10-cobweb-picture/before/cobweb-private.json --out /tmp/nov10-cobweb-picture/before > /tmp/nov10-cobweb-picture/before/render.log 2>&1
```

Run the preservation block below with `COBWEB_STAGE=before` immediately. If native adoption already replaced the old MASTER, stop this path; parent can serve retained verified old bytes from an explicitly ignored **inside-app** fixture via `--glb`. Do not restore the active MASTER over the new output or relabel the old evidence as a fresh render. The old qualified packet remains honest baseline evidence if fresh-before rendering is unavailable.

## Capture after the actual grouped native is retained and adopted

Parent first retains the actual grouped-native source parent/run identity, inputs/master/web receipts, and control comparison for all 83 outputs. New source-only tests do not substitute for native bytes. Only after that run has supplied the actual adopted new Cobweb MASTER, and when GPU is free:

```bash
source /tmp/chicago-resume-env-20261109.sh
cd /tmp/chicago-west-wicket-20261109/chicago/4d
python3 - <<'PY'
from pathlib import Path
import hashlib
p=Path('assets/gltf/cobweb_castle__log_1820.glb')
s=hashlib.sha256(p.read_bytes()).hexdigest()
assert s!='1ddf548d9a378167163d6db45e5d89e1b4c544ea176355eb7061dd99d6a1ee82', 'MASTER still old'
assert not Path('/tmp/nov10-cobweb-picture/after/render.log').exists()
print('actual AFTER MASTER',s,len(p.read_bytes()))
PY
timeout 570s node tools/photo_match.mjs /tmp/nov10-cobweb-picture/after/cobweb-private.json --out /tmp/nov10-cobweb-picture/after > /tmp/nov10-cobweb-picture/after/render.log 2>&1
```

Run preservation block with `COBWEB_STAGE=after`. A changed SHA alone does not prove a correct native artifact; qualify it against parent's retained native run manifest.

## Preserve the raw PNG and create the unchanged diagnostic crop

Run from any cwd after each successful capture. Select `before` or `after` explicitly on the first line. This copies the untouched bare PNG whose random temporary pathname `photo_match` prints, retains the full generated comparison and private unreviewed match, and records exact hashes. No enhancement, annotation or fit is applied to crop pixels.

```bash
COBWEB_STAGE=before python3 - <<'PY'
from pathlib import Path
from PIL import Image
import os,json,hashlib,shutil
stage=os.environ['COBWEB_STAGE']; assert stage in ('before','after')
folder=Path('/tmp/nov10-cobweb-picture')/stage
assert not (folder/'capture-receipt.json').exists()
log=folder/'render.log'
rows=[x.strip() for x in log.read_text().splitlines()]
paths=[Path(x) for x in rows if x.startswith('/tmp/photo-match-') and x.endswith('-render.png')]
assert len(paths)==1 and paths[0].is_file(), 'capture failed or ambiguous; inspect render.log'
raw=folder/'model-bare.png'; shutil.copy2(paths[0],raw)
source=Path('/tmp/chicago-west-wicket-20261109/chicago/reference/images/chicago/chicago_fort_dearborn_1831_1.jpg')
for p,name in [(raw,'model-same-fixed-crop-8x.png'),(source,'source-same-fixed-crop-8x.png')]:
    with Image.open(p) as im:
        assert im.size==(1920,1042)
        im.crop((1380,330,1500,420)).resize((960,720),Image.Resampling.NEAREST).save(folder/name)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
camera=folder/'cobweb-private.json'; match=folder/'cobweb-private.match.json'
m=json.loads(match.read_text())
assert sha(camera)=='07f94fa8654e1c0469ad4d3df2c0c01414e15ce5cfabcdadde9260a942ea4977'
assert sha(source)=='624d8f1f52a75bf30653e8cbf37a388478b0ddf5a02f1fadf727cf2144b84c3f'
assert m['camera_sha256']==sha(camera) and m['photo_sha256']==sha(source)
assert m['verdict']=='unreviewed'
assert sha(folder/'source-same-fixed-crop-8x.png')=='955124dee76ee2d5585e0461688d9c141cad79a25d192248d8fca7c4377d4750'
files=[camera,source,raw,log,match,folder/'cobweb-private-side-by-side.jpg',folder/'model-same-fixed-crop-8x.png',folder/'source-same-fixed-crop-8x.png']
receipt={'stage':stage,'original_bare_path':str(paths[0]),'glb_sha256_from_match':m['glb_sha256'],'crop_box':[1380,330,1500,420],'crop_scale':8,'crop_resampling':'nearest','files':[{ 'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
(folder/'capture-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if stage=='before':
    assert m['glb_sha256']=='1ddf548d9a378167163d6db45e5d89e1b4c544ea176355eb7061dd99d6a1ee82'
else:
    assert m['glb_sha256']!='1ddf548d9a378167163d6db45e5d89e1b4c544ea176355eb7061dd99d6a1ee82'
print(folder/'capture-receipt.json')
PY
```

If the fresh before bare/crop differs from prior hashes, retain both. Report the renderer/environment difference; do not adjust the camera to force pixel identity. A fresh serial pair on the same renderer still tests the geometry change when the before MASTER hash is correct.

## Actual review and bounded conclusion

View full source, full bare before/after, full comparison, and both fixed crops. Confirm a visible lower neutral board band on exposed compound runs; upper logs, log corner tails and existing roof/stack silhouettes remain. Check the two clear dark lower upright faces and upper gable mark stay open and uninterrupted: the merged PR1690 repaired depth must not regress to horizontal striped faces. Check both wings' windows remain clear. Check no visible shift of footprint, wing, ridge, stack, door/window or camera. The supplied new pre-export prefix/control tests support this but do not replace viewing actual new native output.

The textual source supports *part-way* clapboarding, not a measured 1.30m historical finish, white paint, or verified July1835 installation. The 1.30m band is explicitly reconstructed half of the prior 2.6m wall; preserve that qualifier. Whole width/wings/sub-roofs/roof junctions and camera solve still have open discrepancies. Preserve sources and existing inferred grades. State the visible improvement and unresolved points in the ticket/PR rather than asserting picture closure.

This is the neutral single-model picture comparison. Parent separately owns the actual grouped native/control checks and browser visitor regression coverage. Do not claim global runtime, completed image gate, solved camera, or full smoke from this private render alone.
