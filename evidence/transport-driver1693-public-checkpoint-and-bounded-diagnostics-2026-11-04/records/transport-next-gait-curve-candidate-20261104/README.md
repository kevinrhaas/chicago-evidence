# CURRENT-ad9 constrained0.20m curve-only attempt — PREPARED, UNRUN

No authoring, model parse/decode, native pose, GPU job, candidate GLB, asset or
application edit has run. The unbound GO template is not approval. ROOT alone
binds a fresh clean public checkout/source, exact output root, approved=true,
template_only=false and short future UTC expiry after the exclusive lane closes.

This is one intentionally bounded local search, not a claim that0.20m is feasible
or natural. Target stride0.20m at1.6s implies0.125m/s with external distance once.
Duty0.75,10mm fore/hind lifts and existing5.236874mm root crouch stay fixed. All
seven physical limits, both original1nm endpoint loop limits and the three
original physical fault controls remain unchanged; no gate or fixture is edited.

The original authoring recipe is in:

* ../transport-T2803-grounded-gait-nextstep-20261031/SEALED-CURRENT26-WALK-SOURCE-MODEL-BF519-20261102/surface_pose_solver.py
* ../transport-T2803-grounded-gait-nextstep-20261031/BARE-CURRENT26-WALK-SPECIMEN-11-BOUNDED-CAREFUL-WALK/author_dense_knot_chunk.py
* ../transport-T2803-grounded-gait-nextstep-20261031/SEALED-CURRENT26-WALK-SOURCE-MODEL-BF519-20261102/smooth_two_nullspace_windows.py
* ../transport-T2803-grounded-gait-nextstep-20261031/SEALED-CURRENT26-WALK-SOURCE-MODEL-BF519-20261102/pack_endpoint_encoded_specimen.py
* ../transport-T2803-grounded-gait-nextstep-20261031/SEALED-CURRENT26-WALK-SOURCE-MODEL-BF519-20261102/generate_from_authored_controls.py
* ../transport-T2803-grounded-gait-nextstep-20261031/INPLACE-CURRENT26-WALK-20261102/author_inplace_derivative.py

Original commands (provenance only; DO NOT run them on their old parents):

    python author_dense_knot_chunk.py fore_r 0
    # original authoring used limb hind_l/fore_l/hind_r/fore_r, blocks0..16
    python smooth_two_nullspace_windows.py
    python pack_endpoint_encoded_specimen.py
    python generate_from_authored_controls.py --parent PARENT-CURRENT26-QUIET-V6-7CE84.glb --controls AUTHORED-WALK-CONTROL-FLOAT32-DATA-SMOOTH-UNIT.json --out FRESH.glb
    python author_inplace_derivative.py

Those packers bind old7ce/BF519 and must never overwrite the current ad9 body,
weights, UVs, eyes/images, materials, quiet graph or old clips. Here, source math,
hinges and original optimizer are frozen as ORIGINAL_*.py. The class body is
loaded without executing its old relative import/configuration preamble. The
math module's SOURCE and EXPECTED are set to current ad9 before constructing
PoseSolver. Old parent paths are never read, and the old producer's main/weight
refinement function is never called. The existing ad9 WALK's20 quaternion
channels are sampled only as initial guesses. Their amplitudes are not scaled.

Cause/degree-of-freedom basis: the current worst edge2923–2924 is a BODY/fore_r
shoulder/elbow blend, not a tail witness. Its two vertices mix fixed body and
proximal foreleg at different ratios. Four sagittal hinge angles can redistribute
proximal bending while holding the2D hoof endpoint; the final hoof angle cancels
the accumulated angle, keeping the rigid sole orientation. There are two free
allocation dimensions after the endpoint equations. The original SLSQP solver
minimizes the maximum edge distortion and half the area distortion over the
actual unchanged BODY triangles incident to each limb. This task reuses that
surface minimax allocation instead of amplifying all channels or changing skin.
We do not assume the two free dimensions have enough remaining strain margin.

The exact actual worst fore_r native phases1.1781249642372131 and
1.1828124821186066 are tried first, then phase-related fore_l/hind_r/hind_l
interface probes. If any local solve fails success, endpoint1e-8 source authoring
residual, unchanged edge0.9..1.1, area0.8..1.2 or normal-sign bounds, it saves the
angles, target residual, edge/area extrema, SLSQP termination and current-curve
seed, and refuses with no GLB. The1e-8 joint-target residual is an authoring
prefilter, not a replacement for original full-hoof stance1e-5 or segment1e-9.
Failure means this bounded local search did not find an admissible posture; it
is not a proof that all curve-only solutions are impossible.

If those probes pass, it attempts129 knots for every limb, using the same
original optimizer and actual current geometry/weights. Original analytic task
velocity tangents and strict Float32 endpoint encoding construct a CUBICSPLINE
clip. No old allocation-transition overrides are blindly reused: those windows
were specific to the old0.135m target. New allocation transitions must be detected
in subsequent dense checks. It only emits an UNQUALIFIED-REVIEW-ONLY GLB if every
knot completes inside the one budget and the exact original4MiB cap. No candidate
is accepted by this producer. It appends only accessors, one bufferView, new curve
bytes and one new animation. Recovery removes those new entries and restores the
buffer length; recovery must exactly equal the complete current parent JSON.
The entire current BIN is verified byte-for-byte as the new BIN prefix. All old
animations, geometry/rest/IBMs, skin weights, UVs, eye/image/texture/material data
and metadata therefore remain exact. Root stays in-place at Z0.

Run only after an explicit ROOT120s CPU grant:

    source /workspace/.cloud-setup/transport-activate.sh
    python /workspace/.cloud-setup/transport-next-gait-curve-candidate-20261104/launch_detached_attempt.py --binding /outside/app/ACTUAL-ROOT-GO.json --out /outside/app/FRESH-ONE-ATTEMPT

The wrapper binds exact clean HEAD/TREE/APP/index and all source/helper hashes,
requires fresh external output, obtains the existing canonical exclusive heavy
lock, records before/after source and paired memory/swap/CPU/GPU resources, and
runs one process-tree supervisor with requested/effective timeout120s. The worker
has110s internal wall-clock cancellation and CPU115/116s. Refusal/timeout never
retries, promotes, mutates the app or raises thresholds. The supervised receipt
must show complete owned-process cleanup; a negative authoring outcome can be a
successfully closed attempt, never a gait pass. Detached owner PID/start ticks/
PGID/SID are recorded explicitly for polling and ownership.

A produced candidate still needs full serialized-source and actual native r185
GLTFLoader/Meshopt/SkeletonUtils/AnimationMixer/getVertexPosition plus original
Float32 bone-palette qualification of all seven predicates across the dense
schedule; both original1nm endpoint loop checks; unchanged three original fault
controls; fresh full hoof-support domain; full-route wheel/horse/driver/hitch
contacts; and actual published desktop/phone visual, memory and frame review.
The1.6s/0.20m/0.125mps clip metadata, actor distance-once driver and route speed
must agree in a later scoped change. Natural walk and photographic acceptance
remain UNACCEPTED; standing quiet remains separate.
