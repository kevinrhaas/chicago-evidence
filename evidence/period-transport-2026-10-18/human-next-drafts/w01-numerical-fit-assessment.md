# W01 bench: resident-first rest-geometry assessment

Read-only study,2026-10-18. No Blender executed or application files changed.
Reproduce: `python /workspace/shared/human-transport-draft/assess_w01_reach.py`.
Detailed measured inputs/results: `w01-rest-reach.json` in this directory.

Inputs are the current builder's actual prepared25/35 body JSON and56-bone rest
joints, with the same height_scale1.0 in `worker_1835.json`, glTF +Y-up/+Z-forward.
The recipe maps prepared25 to existing resident `bardwell_otis_1835`, prepared35
to `dufresne_joseph_1835` and `flynn_martin_1835`. These are reconstructed1.75m
authoring bodies, not measured historical residents or attested exact ages. Existing
resident/date eligibility remains the authoring recipe's responsibility; this
analysis does not invent a teamster occupation for all three.

## Proposed W01 support and numeric targets

Previous bench proposal is an optional independent reconstruction, not an attested
1835 accessory: physical plankTOP1.58 atZ.65, real supporting railsTOP1.53, footrest
TOP1.12 atZ1.27. Current W01 mesh still has none of this furniture. Its empty seat
socket is not a physical bench and cannot pass seated-human acceptance.

For numerical reach only: pelvis head(0,1.68,.65); wrists(±.20,1.92,1.04).
Pelvis head is provisionally.10 above seat, not measured buttock clearance.
Ankle X±.18,Z1.19; ankle Y derives from the actual prepared foot's ankle-to-lowest
dominantly foot-weighted vertex distance, so rigid foot soles sit atY1.12.
This improves on a guessed uniform ankleheight; it is still not a skinned pose test.

|Prepared body|Thigh+calf lengths|Hip→ankle target|Remaining extension|Upperarm+forearm lengths|Shoulder→wrist target|Remaining extension|
|---|---|---|---|---|---|---|
|25|.420784+.439549=.860334|.735895|.124439|.253940+.269529=.523470|.434478|.088991|
|35|.415276+.444140=.859416|.733314|.126102|.251847+.264292=.516139|.435385|.080754|

Values in metres; both sides give the same values to the displayed precision.
All target distances lie strictly between each chain's difference and sum lengths.
Actual first-bone tails and second-bone heads coincide (0 gap) for both arm/leg
chains, so the draft's two-link geometry assumption holds for these inputs.
Thus these proposed targets **are geometrically reachable without stretching the
rest bones**. That does not establish a comfortable or historically correct pose,
skin deformation, wrist grip, elbow/knee/body clearance or reins.

## Footboard projection from actual prepared mesh

Selected body vertices have combined foot/ball weight≥.90; this is a rigid-foot
bounding estimate, not complete linear-blend skinning. Left-foot results (right
mirrors X):

|Body|AnkleY|Rigid foot X bounds|FootY bounds|FootZ bounds|
|---|---|---|---|---|
|25|1.192059|.137941..235199|1.120000..1.189990|1.126593..1.387295|
|35|1.191633|.137585..235156|1.120000..1.190045|1.127742..1.388716|

Both fit the initially proposed platform X±.425,Z1.12..1.42. But heel margin is
only6.6–7.7mm before the builder's declared5mm shoe offset, leaving little slack.
**Revise the proposed footrest to.34m depth, centerZ1.27, bounds1.10..1.44.**
This is a bounded engineering revision, not newly discovered period evidence.
It remains inside the front box wallZ1.525 and gives approximately26–28mm bare-foot
rear margin. Still inspect actual authored shoes, deformation and braking motions;
the source/weight filter does not include every garment vertex.

## What the draft still must prove on CI

- Use actual canonical resident master and original56-bone orientation, not the
  primitive fixture. Run the solver only in authorized remote Blender CI.
- Measure skinned pelvis/buttock against real bench. A.10m pelvis-head clearance
  may penetrate or float; adjust from actual posed mesh, keeping its reconstruction
  grade. Do not convert reach success into contact success.
- Measure knees/thighs against front wall, seat edge and box sides, feet against
  actual supported footrest and shoes against wood; confirm torso/head clearance.
- Wrists are proposed reachable handtargets, not reins already fitted. Check grip,
  finger pose, rein routing/slack/tension and actual harness coupling independently.
- Draft action currently registers static seated pelvis but leaves root translation
  zero; it resets all pose matrices to REST before saving. Confirm export preserves
  original bind/rest and the sit_drive action, and that root remains zero over clip.
- Read resulting actual GLBs/reports/renders; do not claim hand/seat fit merely
  because the canonical build job succeeded.

## Period and scope boundaries

W01 with reconstructed furniture is the possible1835 driver path for an eligible
existing resident with1835 wardrobe. It is not yet implemented. Do not place every
resident on a wagon or imply a sourced occupation from an engineering test.

C01 is1904 development-only. Its existing numeric profile remains an instrument;
do not deploy a1835-clothed Bardwell as a1904 coachman. A1904 resident/wardrobe path
is separately required for scene deployment. No sit_ride is authored or accepted
until a real saddle/stirrups and physical fitting exist; empty horse sockets do
not constitute riding tack.
