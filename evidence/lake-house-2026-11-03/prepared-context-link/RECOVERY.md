# T-2379: credited later completed-state picture — prepared increment

Prepared against Chicago dev `d30700af3afff7296841cfbdc7dbca564eb3b727` on 2026-11-03. This packet is a six-file candidate, not an applied source change or PR. Original T-2379 remains open; no ticket claim or completion was made.

The sole original ticket picture is `chicago/reference/images/chicago/chicago_fort_dearborn_river_mouth_1830.jpg`. Direct inspection of that crop and the larger NYPL-credited Commons scan identifies the same 1856 Kellogg/Blanchard print. The labelled Lake House is RIGHT of the foreground fort blockhouse, partly behind a tree; it is the later completed hotel with regular windows and a cupola. Existing catalogs date the depicted scene approximately 1836–1849. The direct NYPL catalog URL returned an automated-access placeholder. Current Commons metadata explicitly credits that NYPL object and records 1856/Public domain/PD-scan/PD-old-auto-expired; its full scan's lithographer and publisher imprints were read. No live NYPL catalog access is claimed.

## Prepared visible increment

The new tier-5 public-domain cross-check SourceRecord is named in the existing structure's research note. The native Pictures compiler now derives one credited link titled “Old Fort Dearborn — later completed Lake House, about 1836–1849.” It is contextual, never July 1835 construction evidence. All non-research-note structure fields remain identical; no camera, grade ruling, geometry, position, confidence, phase date or exclusions changed. The dossier and progress records append this limit; one pending What's-New entry describes the visible Images link.

`MANIFEST.json` binds all six before/after bodies. `source.patch` preserves the inherited invalid bytes in ROADMAP. `apply_prepared.py` is dry-run by default: exact original hashes are required for changed records; progress logs accept only an intact original byte prefix and append without replacing concurrent later text. It must run only in a separately owned source checkout after checking latest dev and taking the original claim. Re-evaluate any changed record instead of weakening a guard.

## Actual validation

- SourceRecord and prepared structure passed the current JSON schemas.
- Unmodified public d307 `compile_pictures.derive`: explicit-input Images **0 → 1**.
- Unmodified public d307 `grade_structure`: real `shell_1835` existence confidence and current rulings, no cameras: **inferred → inferred**. No fake `not_pictured` ruling.
- Dry-run applicator verified all six paths and byte-exact append baselines.
- No full four-part source gate, sidecar compilation, authored commit, PR, browser QA, or image-gate match has run on this candidate. Those remain required before shipping. Derived sidecar(s) may become an additional path after actual compilation.

## Original acceptance still open

There are no canonical Lake House reference views at this baseline, no fitted camera, no current-GLB side-by-side and no accepted match record. The print cannot establish the roof/height/progress of July 1835. The June 10, 1835 Democrat notice only establishes an active named project; the existing T-3123 correction already treats roof absence as reconstructed. Preserve that distinction.

## Concrete path beyond links — current limits

An honest later-state comparison is feasible as a PRIVATE explicit-GLB diagnostic, not by backdating the completed hotel into the 1835 default scene:

1. Current `tools/photo_match.mjs` supports `--glb <private specimen>`; a private camera/specimen can compare visible completed-hotel features while preserving the town shell. This packet does not create that geometry or solve that camera. The present tier-5 source is cross-check only and must not be silently promoted into tracing authority.
2. Current `fort_structure` parameters can express up to three storeys, face openings on quarters/barracks and several roof types, but have no hotel cupola/roof-balustrade control. Its lantern controls are lighthouse-tower-only. A faithful later hotel needs an explicitly supported producer extension or provenance-compliant authored specimen, not just `stories: 3`.
3. A dated version does not solve reachability: native `build.resolve_phase`, tested on actual committed scene dates 1812-08-14, 1835-07-01 and 1904-07-01, selects no phase in a hypothetical 1837–1849 comparison interval. Targeted bake builds only phases reached by committed scenes, including versions. `compile_scene.compile_versions` also resolves by scene date. Do not backdate the specimen or invent a historical date to evade this.
4. Current image-gate `glbFor` hashes the default `assets/manifest.json` entry; a successful private version comparison cannot be represented as the default shell's `matches`. Current grader also counts canonical camera records for the structure without filtering by scene or `diagnostic_only`, so a later-state canonical camera would incorrectly attest the 1835 shell. No such camera is prepared.

For an original-ticket finish beyond this visible context link, scope an explicit later-state diagnostic producer and honest state-aware acceptance/grade semantics with the parent. Keep the original open; do not file a photo follow-up. A subsequent normal targeted bake, when supported and coordinated, is `gh workflow run chicago-4d-bake.yml --repo kevinrhaas/chicago --ref OWN_SOURCE_BRANCH -f only=lake_house_construction`; use the workflow's pinned Blender environment. It was not dispatched here.
