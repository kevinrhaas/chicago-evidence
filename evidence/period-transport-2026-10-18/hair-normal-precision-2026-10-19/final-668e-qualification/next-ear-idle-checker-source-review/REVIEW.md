# Exact owned-point certificate review — source only

Reviewed exact_contact.py, source_edges.py, ownership.py, unchanged official SAT/proper predicate source, and all seven test_exact_contact.py controls. No actual horse capture, source candidate, exporter, SAT sweep, tests, browser, app or ticket mutation performed by this reviewer. No JSON control-execution receipt was present in the directory snapshot; the seven controls below are source inspection, not independently rerun evidence.

## Mathematical certificate

No false-positive certificate defect identified in the current helper. All finite captured float64 coordinates are dyadic rationals; as_integer_ratio and a common power-of-two lattice retain their exact values. Python integer dot/cross products avoid floating tolerance and overflow. For a candidate axis, both noncommon A vertices must be on its nonnegative side and B vertices on its nonpositive side, with common P on the plane. Every common point therefore lies on that zero plane. The zero feature of each triangle is either P alone, a ray segment from P, or the full triangular cone at P. The helper accepts only when those zero features have no common nonzero ray: one feature is P, two rays are noncollinear/opposed, or a single ray is outside the opposing exact cone. Thus its certificate proves intersection exactly{P}. It does not accept mere proximity.

The determinant-based ray_inside_cone test uses exact planar membership and sign-independent a*den/b*den coefficients. Degenerate triangles return no certificate. Coplanar two-cone cases with both complete triangles in the separator plane are conservatively unaccepted. The candidate axis list need not be complete: missing a valid separator yields None/failure, not an unsafe exemption.

The seven authored controls cover coplanar/noncoplanar point-only positives, shared-point interior crossing, unowned edge overlap, coplanar area overlap, nonidentical worldpoint rejection and exact cone membership. These support the intended boundary but do not themselves verify the eventual dispatch or actual horse.

## Required caller rules and current review limit

The helper accepts ia/ib indices; it cannot independently establish source ownership. Only the actual checker may call it after proving exactly one registered common source identity and exact worldpoint equality. A broad nearest-position match or bbox coincidence must not mint that ownership. ownership.py uses pinned source/producer/maps and semantic ranges, not whole-coat position welding; source_edges.py adds whole-pair exclusions only for exactly two unique opposite-directed owners of an actual source edge, including explicit protected neckportal aliases. A single shared source vertex is NOT a whole-pair exclusion.

Keep unchanged SAT1e-8 and proper predicates. Require proper-crossing evaluation first and never waive a nonempty proper-crossing result through this helper, even if it proposes a certificate. Then an owned-single-point SAT-positive pair may be classified only with the exact certificate. Unregistered coplanar/edge/area contacts must remain failures. Baseline twelve unregistered contacts must still fail through the same eventual dispatch. Neither official_fit_predicates.py nor exact_contact.py proves this integration by itself; no complete pair-dispatch implementation was present in this review snapshot. Therefore those actual negative results are NOT certified here.

## Bounded source-release recommendation

The exact certificate helper has no identified source blocker for integration into a separately reviewed checker. Permit only a future bounded synthetic/registration-dispatch qualification first: prove a shared-onevertex proper crossing fails, same-source/differentworldpoint fails, unregistered edge/area contacts fail, declared opposite-edge adjacency alone can skip wholepair, and original twelve baseline contacts remain red. Persist first failing pair and evidence rather than broadening ownership or changing tolerances. Review actual dispatch before any horse capture/SAT run; this is not permission for current frozen-run work, a dense sweep, or candidate acceptance.

## Root geometric-edge qualification (required)

Opposite SOURCE-edge orientation establishes registration, not geometric nonoverlap after deformation. The current source_edges.py emits adjacency pair sets without an actual-coordinate foldover certificate. Two coplanar triangles sharing the same exact owned edge can overlap on the same side even when their source edge order is opposite. Therefore the eventual caller MUST NOT unconditionally skip those pairs.

Before whole-pair exemption, require an exact actual shared-edge certificate: noncoplanar triangle planes with the same nondegenerate actual edge intersect only on that line (each triangle's intersection with the line is its edge); or, when coplanar, the two actual third vertices lie on strictly opposite half-planes of the common edge. Same-side coplanar overlap, degenerate edge/triangle, mismatched world endpoints or unknown registration must fail. Unchanged proper-crossing guard still cannot be waived. This is an additional caller source blocker, communicated to the author before actual execution. The owned-single-point helper's cone proof is unchanged.
