# T1789: independent bounded clothing review

Source commit `a64f26fa2fc3e05dd39cd8e55df5384646786d7b`, tree `0c2fe214e0c41f127282f82b04b3754279baf526`. Reviewed the six-cell actual HumanActor studio receipt plus eight existing screenshots. No APP changes or new tests/rendering.

**Verdict: favorable as an incremental clothing surface change.** Peck’s pale trousers now read with restrained cloth variation and crease shading on phone, while the navy coat, buff waistcoat, hat, palette and silhouette remain consistent. Otis’s source standing/walking comparison has a smaller, visible garment shading change. Current published desktop/phone walking samples show no obvious new clipping, detached pieces, missing surfaces or shader color spilling onto the face/shoes. This remains a smooth, reconstructed figure rather than full photo-quality acceptance.

## Pre-existing source pattern

Otis already has a fine wavy pattern in the source baseline, including his face and shoes. In the exactly framed source-desktop standing pair, face rectangle `[614,142,656,196]` has 0/2,268 changed pixels. Shoe interiors `[586,630,611,643]` and `[649,639,676,653]` have 0/703 changed pixels combined. Garment rectangles do change (waistcoat 7,286/8,385 pixels; trousers 15,394/18,540). These are fixed screenshot samples; they do not diagnose the origin of the old surface pattern.

## Receipt comparison

| Paired cell | Resident | Calls | Triangles | Geometries | Textures |
|---|---|---:|---:|---:|---:|
| source-desktop-current | hi_rc_bardwell_otis_1835 | 21 | 103874 | 12 | 18 |
| source-desktop-current | hi_peck_philip_1835 | 37 | 112310 | 20 | 26 |
| published-phone-current | hi_rc_bardwell_otis_1835 | 10 | 12511 | 10 | 16 |
| published-phone-current | hi_peck_philip_1835 | 18 | 13838 | 18 | 24 |

Every value above equals its own baseline and remains the same in that pair’s walking snapshot. Map names/presence/dimensions also match; the shader additions are confined to garment materials (`chicago-fabric-v1`, `chiFabric`/`chiFabricWear`). Skin, hair, eye, footwear and other non-garment shader records remain unchanged. The published phone pair requests the same five image paths (separate studio server origins ignored). There is no added image texture resource in these paired records. This is map-inventory/resource-count evidence, not byte-level image or full-geometry comparison.

All six receipts have no browser errors. Every resident disposal returns the studio to its recorded empty baseline of one geometry and three textures, with no loaded actors left. Both residents’ walking snapshots retain `gaitBound=true`. Otis’s adopted clip list still includes idle, sit_drive, walk, idle_natural_v1 and sit_drive_look_v2 in the full source cell.

Viewed: source desktop baseline/current Otis standing and walking; published phone baseline/current Peck standing; current published desktop and phone Peck walking. Exact image/receipt hashes and compact comparison values are in the companion JSON.

Limits: still-image review cannot assess temporal shimmer; this is controlled HumanActor studio evidence, not whole-town smoke, final garment fit, canonical PBR, likeness or full photographic acceptance.
