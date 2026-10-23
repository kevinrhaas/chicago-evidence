# Minimal metadata-only proposal; NOT executed/applied

Root resource hold remains in force. No regeneration, metadata-adapter execution, geometric tests, app writes or changes to testedb880/459pair or immutable archives occurred. Proposed Python files were AST syntax checked only.

`metadata-only.patch` targets the frozen outside V2 generator, not today's app baseline generator: add one metadata helper and call it **after the GLB bytes have already been written**, before final sidecar write. The adapter deep-copies input metadata and never changes geometry/indices/weights. A future application must prove the GLB remains exactb880 and inputs are not mutated; no such rebuild is claimed here.

Changes:

1. Replace ambiguous `added_face_count`/`removed_face_count` with stage-labeled construction counts.308added bridge triangles is pre-local-subdivision; final1184bridge+402body=1586changed triangles. Full asset count15392 remains authoritative existingfield.
2. Replace obsolete numeric `joint_policy` prose (incorrect.12/.55/.88 and original-root-boundary claim) with final decoded JOINTS_0/WEIGHTS_0 authority, declared changed-old-weight mask and shared-index interface explanation. It does not duplicate a ring-weight recipe that can drift again.
3. Rename `vertex_ranges` to `source_vertex_ranges` and explicitly mark audit-only. This is deliberately FAIL-CLOSED for old range-only consumers, not a compatibility alias capable of quietly omitting new bridges. Add versioned `active_surface_regions`: full torso, whole changed forechest and each joined foreupper appendage, with actual current coat triangle IDs. Full torso combines unchanged original-body-index triangles and the exact refined-body descendant IDs. Real decoded coat indices reject retired-cap revival, out-of-bounds/duplicate IDs and missing body/bridge coverage.

All range consumers named in the prior integration PLAN must be migrated in the same later integration parcel. In particular, `measure_forelimbs.py` and old torso studies must select current triangle IDs; don't apply this manifest patch alone and suppress their failures. Runtime demo/contact consumers currently don't need original construction vertex ranges. Whole-horse head-fit and mechanical predicates remain geometrically unchanged.

`proposed/test_surface_metadata.py` is a proposed read-only actual-fixture test against a directory containing frozenb880GLB/current sidecar. It verifies byte identity/no input mutation, proves that a simulated old range-only selector actually omits bridge faces, and rejects three real malformed contracts: missing bridges, an appendage region missing its bridge, and a revived retired-cap vertex. This test is UNRUN during root's gate hold. Future command:

    python proposed/test_surface_metadata.py /workspace/shared/horse-forechest-smooth-next/trial-v2

Then a separately authorized future temporary rebuild with proposed generator/helper must still produce exactb880GLB; sidecar is expected to change and needs a new hash. Do not overwrite the frozenV2sidecar/SAT witness inputs. Geometry/pair distance/stand-off qualification still precedes any app/body adoption, regardless of this cleanup.

Original helper CC0-1.0; proposed tests GPL-3.0-or-later. No extra framework, bone/material or asset changes.
