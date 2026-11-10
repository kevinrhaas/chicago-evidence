# Current parked Brougham versus moving original: anchor prerequisite proof

Source HEAD: `c6dc330d9bfd69fbbfe07d0feb2fb24f3c74fbcd`. Companion to `GLESSNER-CARRIAGE-RIDE-NEXT.md` and its 16-source JSON audit.

**Result: all 43 decoded GLB node objects are deep-equal, including child indices, mesh references, names and local transforms; scene roots also match.** The current delivery model retains the exact source hierarchy needed to investigate reusing the driven hitch. This is a metadata prerequisite proof, not ground/contact, coupled, occupied or boarding qualification.

Only GLB headers and JSON chunks were decoded. File bytes were streamed for SHA256 verification against the saved source audit; no BIN/accessor geometry was interpreted, no model loader, browser or native worker ran.

| Property | Current parked delivery near | Moving original near |
|---|---|---|
| Full SHA256 | `b5b183b4f115c5c7779ba0cb4ccba83fbffb62349647a9a6487f50cde49aef77` | `3d2f3a802f4b32dba6a3e61f2c188dddce4db05cecfcbba81e1e8d369d5dfe89` |
| JSON chunk SHA256 | `340a89386db50c9e9df9724e7831d586ccde1f414c040c4efad35773862571b1` | `26c0055c381d2595d6f4d3b1a9fb65396a0e80607849e685217d5bc84bd18b8b` |
| Nodes | 43 | 43 |
| Scene roots | equal | equal |

JSON chunks and model bytes differ; decoded node equality does not imply identical materials or mesh streams. JSON integer `0` and float `0.0` compare as the same exact numeric value; this is decoded equality, not equality of JSON whitespace/number formatting.

| Named node | Parent | Local translation metres, equal in both |
|---|---|---|
| `vehicle_root` | scene root | `[0, 0, 0]` |
| `vehicle_body` | `vehicle_root` | `[0, 0, 0]` |
| `vehicle_running_gear_rear` | `vehicle_root` | `[0, 0.65, -1.15]` |
| `vehicle_steer_front` | `vehicle_root` | `[0, 0.528, 1.15]` |
| `vehicle_wheel_rear_right` | `vehicle_running_gear_rear` | `[-0.67, 0, 0]` |
| `vehicle_wheel_rear_left` | `vehicle_running_gear_rear` | `[0.67, 0, 0]` |
| `vehicle_wheel_front_right` | `vehicle_steer_front` | `[-0.67, 0, 0]` |
| `vehicle_wheel_front_left` | `vehicle_steer_front` | `[0.67, 0, 0]` |
| `vehicle_team_pole` | `vehicle_root` | `[0, 0, 0]` |
| `vehicle_hitch_team` | `vehicle_team_pole` | `[0, 0.037, 3.8]` |
| `vehicle_seat_driver` | `vehicle_body` | `[0, 1.7758499999999997, 0.76]` |
| `vehicle_seat_passenger_01` | `vehicle_body` | `[0.23, 1.3068999999999997, -0.72]` |
| `vehicle_seat_passenger_02` | `vehicle_body` | `[-0.23, 1.3068999999999997, -0.72]` |

Every listed node also has equal rotation/scale defaults (identity/unit); there are no differing decoded nodes anywhere in either 43-node array.

## Existing binding versus retained source targets

- `studebaker_brougham_1893` names `vehicle_team_pole`, `vehicle_hitch_team` and `vehicle_steer_front`; all exist unchanged.
- Source front axle remains `[0,0.528,1.15]`. Existing driven configuration adds its explicit pivot at `[0,0.553,1.15]`; that is a derived working pivot, not a pre-existing parked hinge.
- Source parked pole tip remains `[0,0.037,3.8]`, down at its ground shoe. Current binding sets horse centre +Z `3.08` and uses a two-horse team. Matching source targets does not validate lifting/coupling against the actual current finish clone.
- Driver seat matches current moving row `[0,1.77585,0.76]` to 2.2204460492503131e-16 m maximum floating-point difference, within the existing 1e-6 m check. Passenger seat nodes are retained too.
- Existing moving `driver_binding.vehicle_glb_sha256` still names the moving original, not current delivery. A direct delivery substitution is therefore correctly rejected until explicitly source-rebound and qualified.

## Bounded next use

Retain the existing parked row, coordinates and current delivery near/mid finish. The equality above supports a bounded hitch-ready owned clone or pre-batch attachment path reusing the unchanged named targets, with a fresh exact-delivery source binding. Do not swap in the older moving model. The current rigid static batch flattens these nodes, so attach before flattening and keep movable pole/skinned team separate.

Current hitch requires exactly two current26 horses, a seated driver and real palm bindings; single-horse shafts are not implemented. Preserve Glessner coachman Charles Nelson versus separate moving driver Hans Johnson. Doors, passenger fit and boarding remain open on T-2795/T-2801/T-2797. No APP mutation, claim, dispatch or acceptance occurred.
