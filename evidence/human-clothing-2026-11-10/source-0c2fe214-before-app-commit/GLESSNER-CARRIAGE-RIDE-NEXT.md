# Glessner-front carriage: next bounded ride work

Read-only implementation audit. Source HEAD: `c6dc330d9bfd69fbbfe07d0feb2fb24f3c74fbcd` in `/tmp/chicago-queue-refresh-20261109`. All source paths below were verified byte-for-byte against that committed HEAD when saving this note. No APP changes, claims, native/browser execution or new asset adoption were made by this audit. Keep unfinished work on existing T-2795, T-2801 and T-2797; no new ticket is needed.

## Existing carriage and models

`chicago/4d/data/transport/parked/placements.json` has exactly one 1904 parked row: `prairie_parked_studebaker_brougham`, model `studebaker_brougham_1893`, ENU `[1397.9,-3240]`, bearing `178.99`. Its stop is Prairie Avenue south of Eighteenth Street, in front of Glessner House. The catalogue supports the type; the individual vehicle, location, owner and household connection remain reconstructed. Current row explicitly says empty, unhitched, closed doors and no boarding, traffic or driving.

Preserve this row's identity, stand, accepted geometry and current finish:

| Asset under `chicago/4d/renderers/web/` | SHA256 |
|---|---|
| `transport/parked-brougham/brougham-near-delivery-v1.glb` | `b5b183b4f115c5c7779ba0cb4ccba83fbffb62349647a9a6487f50cde49aef77` |
| `transport/parked-brougham/brougham-mid-delivery-v1.glb` | `16daaf1d5003aae3ea64de9d037962aaabf2a5c8638ac77a5a2e037564ef2d63` |
| `transport/parked-brougham/brougham-near.glb` (separate moving assembly's older model) | `3d2f3a802f4b32dba6a3e61f2c188dddce4db05cecfcbba81e1e8d369d5dfe89` |

The delivery GLBs retain `vehicle_steer_front`, `vehicle_team_pole`, `vehicle_hitch_team`, driver seat and two passenger seat nodes. This does not establish occupied or coupled acceptance. Do not substitute the moving assembly's older model to obtain a hitch and lose the current parked finish.

## Existing people and moving circuit

`chicago/4d/data/humans/instances/1904/hi_pa1904_glessner_john_j_c1900_charles_nelson_1904.json` identifies Glessner's coachman as `pa1904_glessner_john_j_c1900_charles_nelson`, depicted by `nelson_charles_1904_coachman`, standing beside the stable doors at ENU `[1341.6,-3216.95]`, heading 35 degrees. His current clip is standing `idle`; selection opens his resident card. The census supports the occupation in 1900; continuing presence in 1904 and depiction remain inferred/reconstructed. The record expressly distinguishes Charles's standing livery from Hans Johnson's box coat and cape.

The separate already-live row `prairie_driven_brougham_loop_1904` in `chicago/4d/data/transport/driven/loops.json` uses `anonymous_working_driver_1904`, clip `sit_drive_look_v2`, with identity `pa1904_otis_f_r_c1900_hans_johnson`. Hans is not Glessner's coachman. It uses two `current26_walk_v2` horses on the existing rounded block circuit. Keep this circuit and identity intact; do not duplicate or relabel it as Glessner's carriage.

John Glessner already has instance `hi_glessner_john_j_1904`, asset `glessner_john_j_1904`, initially ENU `[1390.9,-3226.7]`. An optional passenger depiction later needs actual seated fit, identity ownership/withholding and boarding qualification; no passenger fit is established here.

`standing-horses.json` contains only the separate 1835 Western Hotel yard horse; it explicitly lacks hitch/riding/boarding interfaces. There is no already-placed 1904 standing horse to silently move into the parked carriage.

## Hitch interface and stock-pole limitations

`renderers/web/js/draft-hitch.js` requires exactly **two horses**, a real `driver.root`, the actual current26 skeleton, source-fitted collar/girth assets, actual front-axle/pole/tip hierarchy and driver-specific palm bindings for reins. `driven-assembly-loader.js` additionally requires a seated human and the exact vehicle-byte seat binding. It cannot attach one horse to the parked row unchanged. Charles's current standing model is not Hans's seated fit or palm binding.

The carriage has a central **team pole**, not single-horse shafts. One horse casually placed beside this pole is not a valid hitch. A single-horse version requires actual shafts and associated fit work. The currently reusable bounded configuration is the existing two-horse team/fitter, subject to checks against the exact current delivery clone.

`data/transport/driven/hitch-bindings-v2.json` has `studebaker_brougham_1893`: explicit front-axle lift pivot `[0,0.553,1.15]`, horse centre `+Z 3.08`, team half-spacing 0.65 m. These bindings belong to the separate driven configuration. The parked pole is fixed down with a ground shoe: the static sidecar expressly prohibits treating it as a root hinge or simply rotating it around the vehicle root. Any hitch-ready derivative of the current delivery hierarchy needs its own source binding and ground/contact qualification.

`renderers/web/js/parked-transport.js` merges all rigid meshes into material groups via `staticBatches()` and rejects skinned meshes. That loses the hierarchy needed by a live hitch. Compose from an owned source hierarchy before flattening; keep the team/tack separate and the moving pole out of the rigid batch, or retain a bounded hitch-ready owned clone. Preserve current near/mid policy, source finish and shared asset ownership/disposal.

## Doors, seats and real interaction reuse

`renderers/web/transport/parked-brougham/brougham.json` provides measured boarding/entry/step and seat targets, plus conservative obstacle bounds. It explicitly says `driver_passenger_fit=false`, `boarding=false`, `door_operation=false`, no independent door node and no known hinge axis. The closed door blocks entry. GLB passenger seat nodes are `[+/-0.23,1.3069,-0.72]`; named points alone do not establish human fit or a traversable interior.

`transport-interactions.js` currently offers moving drivers only Stop, Continue and Step back, through the shared engine at reach 6 m. The parked carriage has an inspect card; Charles and John are selectable people, with no carriage boarding action.

Reuse the actual shared `interact.js` engine: stateful actions, prompts, refusal reasons and world-completion waits already exist. For the later passenger adapter, real production `crossings.js` implements step-in, a seat-relative camera during travel and step-out. `main.js` installs its `onRide` ownership hook to stop competing travel/follow. This is a useful ownership/sequence pattern, not proof that carriage doors or fit work, and it must not be confused with old transport demo fixtures or the camera-only horse travel pace.

## First bounded visible increment

Work under T-2795/T-2801 toward a stationary attached **team on this existing parked carriage**, retaining its row, stand and current delivery finish. Bind the actual delivery hierarchy and working-height pole to existing qualified current26/harness components, keep rigid and skinned ownership separate, and qualify wheels/hooves, connection geometry and clearance at this stand. Make driver/rein participation explicit; do not invent a dummy driver, fake Charles's seated fit or copy Hans's identity. If driverless parked reins are needed, that is an explicit bounded fit/lifecycle change, not an already-supported mode.

Keep the existing moving circuit unchanged. Then T-2797 can add approach-coachman -> ask to board -> enter -> passenger camera -> safe disembark after actual door/entry/seated-fit work. John Glessner may be an optional reconstructed passenger with explicit actor ownership. The owner's desired interaction is authorized; these are implementation facts and remaining acceptance work, not a new approval requirement.
