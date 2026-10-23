At close range in 1835, three existing Western Hotel/Wolf Point farm-box wagons now use refined original meshes and materials. An empty reconstructed enclosed carriage stands beside Prairie Avenue in 1904. Each vehicle opens its own inspection record; Light detail, distance and failed loads preserve the earlier 1835 props.

Wheel contacts use the actual yard terrain or the rendered depressed 1904 carriageway. The wagon tongue rests on the ground and a separate small timber support carries the unhitched carriage shafts. Static material batches keep the upgrade bounded to the selected stands.

The models remain type reconstructions with unknown maker/owner. They do not represent a Studebaker or Kinzie Dearborn replica. Photographic quality, occupied people/horses, traffic and boarding remain open under the parent tickets. T-2979 is the bounded parked-scene delivery. This follows the owner’s explicit parked-vehicles-first priority; the source-matched Studebaker and named human repairs are being developed separately.

Validation: deterministic model reproduction and Khronos validation passed. Independent runtime lifecycle/fallback/picking checks passed; actual road-versus-wheel comparison agrees within 0.7 mm. Final source/published runtime fixtures passed 168 assertions across desktop/mobile. Main-scene inspection includes 11 normal browser screenshots and two explicitly canvas-only 1904 desktop views, with real vehicle-card DOM checks, unchanged canonical budgets, and zero GL/page/console errors. Desktop Full's normal screenshot timed out locally; the same production renderer/camera/tier was captured directly, with no app or official smoke assertion changes. The original incomplete request-error and interrupted receipts are preserved. Fresh source/published mobile captures identify the existing people.json HEAD abort under the official exclusion and otherwise pass. Full corrected preflight passed all 1,038 checks, including 380 deliberate refusal self-tests. Exact-commit changelog and ID checks also passed.

Remote qualification: all18 published smoke runs are now terminal at `2aebef95`. Seventeen passed; desktop part13/run39673247878 failed two actual driver-draw checks: X-RAY8,223 and reconstructed Ghost40%8,469 against the existing7,800 ceiling. The remaining151 assertions passed with zero page errors. All three normal workflows passed. The PR stays draft while the exact-pose baseline and draw-cost defect are diagnosed. Full failed logs and exact-head proof are preserved; fresh green qualification and required-check review remain required before DEV merge.

[Final local evidence and recovery manifest](https://github.com/kevinrhaas/chicago-tickets/tree/main/evidence/parked-vehicles-2026-10-21/checkpoint-2118). The owner requests that later upgraded covered wagons retain their deliberate variation; this PR replaces farm boxes only and leaves covered examples intact.

Ticket: T-2979

Actual first-phase street views (type reconstructions; photographic parent acceptance remains open):

<img src="https://raw.githubusercontent.com/kevinrhaas/chicago-tickets/main/evidence/parked-vehicles-2026-10-21/checkpoint-2017/desktop-1835-western-yard.png" alt="Refined parked wagons at the Western Hotel in1835" width="720">

[1904 mobile carriage view](https://github.com/kevinrhaas/chicago-tickets/blob/main/evidence/parked-vehicles-2026-10-21/checkpoint-2017/mobile-1904-carriage-close.png)
