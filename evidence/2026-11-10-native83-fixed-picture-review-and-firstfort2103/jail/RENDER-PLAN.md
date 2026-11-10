# T-2380 fixed-camera refresh and published-yard QA

Owner checkout: `/tmp/chicago-west-wicket-20261109`, application cwd `chicago/4d`.

## Executed 2026-11-10

Parent granted this child the exclusive GPU slot and authorized canonical jail comparison/history writes. Both real photo renders finished exit 0; GPU slot released to parent immediately. Both new full comparisons were actually viewed with `view_image`. The 2.44 m reconstructed fence now exposes the retained core roof where the prior 3.05 m fence concealed almost all of it. Both overall verdicts remain **DIFFERS**. Only complete fence concealment is recorded fixed, with separate open rows for the exposed core's wrong source silhouette. Camera, full source, core/keeper master, placement, keeper gate and native renderer hashes were verified unchanged before/after. No paint/stock fix, historic fence measurement, full match, or runtime qualification is claimed.

Receipt: `/tmp/nov10-jail-qa/render-receipt.json`; logs `gale-render.log`, `andreas-render.log`. Existing native enclosure freshness/owner/date refusal test passed: `/tmp/nov10-jail-qa/owner-freshness.log`.

Exact preceding pairs and match records are preserved in the repository:
`docs/RESEARCH/photo-match/log_jail/history/20261110-before-palisade-height-2440mm/`.
Its `bindings.json` includes all original file hashes. Prior records bind an older enclosure renderer, so their images are historical comparisons, not a single-variable pixel experiment. Current pairs are actual fresh native enclosure renders.

Changed authorized paths: two canonical JPGs, their two `.match.json` records, and the history directory. No source model/camera/data edits, publication or GitHub writes by this child.

## Immutable bindings

| Input | SHA256 |
| --- | --- |
| `data/reference_views/log_jail/gale_1902.json` | `74641a1adcba03d01345eb92734dd3c9c8b4b24fa48aea36ea33e9753dffb8c9` |
| `data/reference_views/log_jail/andreas_1884_context.json` | `22fab9978a88c613df36d100cc39e996092593be141e86695063878d7739724a` |
| Gale full `data/sources/assets/log_jail_gale_1902/page_n79.jpg` | `d1fa0afa1dcd10af3b97ba11b46510fd71dd6504f6f9574aba73828e0fefb85a` |
| Andreas full `../reference/images/chicago/chicago_first_courthouse_1835.jpg` | `1fcbfe2a1f6c1b71439e5f0ad39fba8d3d59c319be73c4d706c2f9b2d3577277` |
| `assets/gltf/log_jail__log_1833.glb` | `e767412faebcd8b77a680d188d89458ea879cf467ec56494a8df1a49a2e65dec` |
| `assets/gltf/log_jail_keeper_house__frame_1835.glb` | `91837241ab0873cbbd27c9f64cd314cc453e41addf019657da3afc8a98c6978b` |
| Candidate `data/enclosures/log_jail_palisade.json` (2.44 m) | `68d377d4dd54269c1ed939e898bb8df387ff1fd7ff5cd38483c21aa0b120d3af` |
| `data/enclosures/log_jail_keeper_link.json` | `1594cc81214cd4f5d8e3612d1e6010d4b10d5e92df95b66e892561bfb283e6ee` |
| `renderers/web/js/enclosures.js` | `f6b439fdb9d614ac2b882b0ce4c18f7a20d099b2998f0a3561ffa6e5f71d169d` |

New Gale JPG SHA: `2733f11eee812694c69772cb79f9109f6fe4252e2a7ed7a7475c748a412824c8` (317640 B).
New Andreas JPG SHA: `a06a3c46947ae1c6a05b138bbcc06ef0e58ce68e6863c14ba5081ebc2c411dac` (383871 B).
Both new enclosure aggregate: `c727e48210c74b05933163c55b089f810235ed2efeed194873a37ad4ebabdca5`.

## Exact rerender commands if any bound input changes

Run sequentially in an exclusive GPU slot. First preserve the current pair/record to a new dated history folder; rerenders overwrite the canonical pair and may reset the verdict. Do not crop, rotate or refit the authored camera. A rerun alone does not confer acceptance.

```bash
cd /tmp/chicago-west-wicket-20261109/chicago/4d
source /tmp/chicago-resume-env-20261109.sh
node tools/photo_match.mjs data/reference_views/log_jail/gale_1902.json
node tools/photo_match.mjs data/reference_views/log_jail/andreas_1884_context.json
```

Actual new review: Gale roof is now clearly exposed but remains a low retained roof rather than the drawing's tall log/gable mass. Andreas shows a shallow exposed band rather than the drawn tall core/cap. Unsolved framing, keeper elevation, native stock legibility, retrospective dates, contradictory core forms and July continuity remain. Courthouse omission remains a deliberate date decision. Neither a complete match nor closure of T-2380 is justified.

## Publication and fresh yard prebuild

Parent must finish resolving integration and adopting the other tickets' native outputs first. At initial planning the checkout had unresolved shared generated-file conflicts; inspect the current state. Do not run publication with unresolved entries or while any source input is changing. Parent controls all publication/source writes. The jail height data change itself requires no Blender bake.

```bash
cd /tmp/chicago-west-wicket-20261109/chicago/4d
source /tmp/chicago-resume-env-20261109.sh
test -z "$(git ls-files --unmerged)"
node tools/smoke_budget.mjs --for-diff origin/dev
bash tools/publish.sh
node tools/prebuild_layers.mjs --check ../../site/4d/data/prebuilt --layer yards
node tools/check_published.mjs
```

Correct prebuilder is `tools/prebuild_layers.mjs`; there is no `prebuild_yards.mjs` or scene/year selector. Official publish rebuilds all applicable `frontage,ground,base,streets,yards` layers with gzip and actual build id. A targeted `--out ../../site/4d/data/prebuilt --build BUILD --gzip --layer yards` is only suitable after the whole published source mirror is already current; it is not a substitute for publication. Do not hand stamp indexes.

The old published yard observed before this task was build `86e8653c8f`, bound palisade SHA `4de1ab8905eb5af96e3ab249e797b29e5baa8c9cd3429c9c9b1fae6f1891de8f`; it does not qualify this increment. Verify the regenerated index binds the actual candidate hash and record the real compressed payload hash. With `yards.json` fields `inputs.files`, `build`, `sha256`, `bytes`, and `bin`:

```bash
python3 - <<'PY'
from pathlib import Path
import json,hashlib,gzip
source=Path('data/enclosures/log_jail_palisade.json')
root=Path('../../site/4d/data/prebuilt/1835')
d=json.loads((root/'yards.json').read_text())
actual=hashlib.sha256(source.read_bytes()).hexdigest()
entry=next(x for x in d['inputs']['files'] if x['path']==str(source))
assert entry['sha256']==actual
assert actual=='68d377d4dd54269c1ed939e898bb8df387ff1fd7ff5cd38483c21aa0b120d3af'
b=(root/d['bin']).read_bytes(); raw=gzip.decompress(b)
assert len(raw)==d['bytes']
assert hashlib.sha256(raw).hexdigest()==d['sha256']
print(json.dumps({'build':d['build'],'enclosure_sha256':actual,'raw_sha256':d['sha256'],'gzip_sha256':hashlib.sha256(b).hexdigest(),'gzip_bytes':len(b)},indent=2))
PY
```

If parent edits the enclosure's explanatory notes after this plan, update the asserted candidate hash to the new actual reviewed source hash and regenerate; do not bypass input binding.

## Actual published runtime review (prepared, not run)

External focused helper: `/tmp/nov10-jail-qa/review.mjs`; Node syntax check passed. This helper is not repository code and has not been browser validated. Parent runs only in an exclusive GPU slot after real publication. Start a dedicated server in another process, without stealing an existing port/server:

```bash
cd /tmp/chicago-west-wicket-20261109/site/4d
python3 -m http.server 4191 --bind 127.0.0.1
```

Then run serial desktop/mobile:

```bash
cd /tmp/chicago-west-wicket-20261109/chicago/4d
source /tmp/chicago-resume-env-20261109.sh
JAIL_BUILD="$(git rev-parse --short=10 HEAD)" JAIL_VIEWPORT=desktop JAIL_OUT=/tmp/nov10-jail-qa/desktop timeout 570s node /tmp/nov10-jail-qa/review.mjs
JAIL_BUILD="$(git rev-parse --short=10 HEAD)" JAIL_VIEWPORT=mobile JAIL_OUT=/tmp/nov10-jail-qa/mobile timeout 570s node /tmp/nov10-jail-qa/review.mjs
```

The exact published HTML build must equal the helper's `JAIL_BUILD`; if official publish stamps differently, read the actual stamp and explain its association with the source commit. Helper checks scene 1835/1835-07-01, fetched current enclosure hash and loaded 2.44 m value, loaded actual jail+keeper web-GLB hashes from `/data/gltf`, retained review annotations only, no unexpected loader/network/page errors, image credits, and actual runtime standing Gale-relative / north-street / compound-overview screenshots. Desktop 1280x800 DPR1; mobile390x780 DPR2. These temporary runtime inspection poses do not change the two authored source cameras.

Inspect all 8 actual screenshots. Check the core roof is visible from suitable exterior standing view, fence heads/stock remain intact, keeper/gate relationship and terrain grounding are retained, and Images credits open correctly. Some close low views can legitimately hide the roof; record what is actually seen. Do not compare world bbox max Y to2.44 without terrain correction. The earlier pure consumer controls separately prove vertical-only stock changes and unchanged counts/topology/materials. A focused receipt explicitly requires human image review and is not the full smoke or image gate.

Raw `api.problems` can contain legitimate `review_required` notes. Helper accepts only exact once-per-record annotation messages with key/record/sidecar identity and true flag. It rejects all other messages. Do not demand zero raw notes or suppress arbitrary loader errors.

If budget requires stage3 for this group, run actual repository smoke separately, sequentially:

```bash
SMOKE_YEAR=1835 SMOKE_VIEWPORT=desktop SMOKE_STAGE=3 SMOKE_SHOTS=/tmp/nov10-jail-qa/smoke-desktop timeout 590s node tools/smoke_renderer.mjs --published > /tmp/nov10-jail-qa/smoke-desktop.log 2>&1
SMOKE_YEAR=1835 SMOKE_VIEWPORT=mobile SMOKE_STAGE=3 SMOKE_SHOTS=/tmp/nov10-jail-qa/smoke-mobile timeout 590s node tools/smoke_renderer.mjs --published > /tmp/nov10-jail-qa/smoke-mobile.log 2>&1
```

Stage3 includes real jail structural/card assertions but does not alone prove physical roof exposure or whole-suite success. Optional actual geometry parity, also exclusive GPU: `node tools/prebuild_layers.mjs --parity --root ../../site/4d --layer yards --json`. Parent selects required stages using smoke_budget for the final combined diff. Preserve failures honestly; do not publish a full PASS from focused checks.
