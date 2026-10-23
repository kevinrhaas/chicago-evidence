# T-2803 contact-target stop/replant source study — UNAPPLIED

Original finite stop transitions on the exact current skinned horse. Outside app/tickets only; no Blender/browser. BaselineinputSHA89b048b7cda748e6f3a7111aa8e4f3198b01fabf6015cae644c78ed02d385bc6 retained in input/. Original mesh/skin/skeleton/materials/socket/rest arrays and all prior idle/walk/trot bytes unchanged (preservation-validation.json). StopGLB1452656bytesSHA17f83d58236e13860a4751d9df34ff692be8a0ab95d9c08f32bf86c010702b00,10newfiniteclips. Deterministic repeat generation sameSHA; Khronos0errors/0warnings.

## Preserved actual failure and replacement scope

input/recovery-* retains carriageagent's rejected walk→idle jointblend source+actualsole receipt:worst−22.9066247mm atwalkphase.13/weight.5. This was a failed proposed jointblend, not failure of existing walk. We do NOT interpolate jointposes to idle, lift rootY, scale, alterhoofgeometry or replace authoredsole markers.

New original plan_stop.py +limb_ik.py solve actual foot targets. capture.mjs samples real decoded source GLTFLoader bonepositions/secondaryquaternions at entry. Fiveentryphases0,.13,.37,.62,.89 EACHwalk+trot. Existing airborne feet finish a reconstructed swing; planted feet stay fixed in world; late feet/newreplants use original3Dsphere-intersectionIK,flatfetlock counterrotation and positivequarticlift. Later feet replant to finalneutral support. At leasttwofeet remain plannedplanted when startingnewsteps. Root decelerates with smooth cosinevelocity for.6s; no rootYmotion. Existinggeometry/rest axes preserved.

This is straight+Z,stationaryheading sourceproof for10entrycases, not arbitraryphase/curvedroute/biological/gear/render acceptance. Start and walk↔trot transitions are separate nextwork. Explicit latersteps prevent an instantaneousneutralposepop.

## Required playback/distance contract

Use finiteGLBclip with LoopOnce+clampWhenFinished. stop-profiles.json is authoritative external actor +Zdistance/time; interpolate this EXACT profile alongside animationtime. DO NOT also add constantstride/rootmotion; clips are in-place in the actorframe. Jointtargets already compensate for this external actortravel. Do not loop a stop or crossfade it to idle. After awaitedfinalpose, actualneutralgeometry matches idle0 numerically, so switching then causes no posepop.

Walkcoast.278709677m;trotcoast.544871795m. Velocity startsat exportedgaitspeed and reaches0 at.6s; feet finish replanting later (walk1.3375–1.5s,total;trot.945833–1.175s). This requires remainingroute/brakingspace; current2mrouteadapter cannot blindly use it after reachingrouteend. Curvedheading/turning must use worldhip/footframe solve or be separately engineered/tested. Signal/cancel/dispose generationguards and mountcamera/route integration NOT implemented here; do not hide them behind immediateidle reset or advance userexit before complete.

## Actual decoded mesh/LBS proof

validate_stops.mjs uses actual GLTFLoader,AnimationMixer,SkinnedMesh and worldtransforms,1001poses/case,unchanged100authoredrestsolevertices. It applies the externalprofiletranslation exactly; no substitute contactpoints. At each sample separate plannedplantedsegments have realsoleworld3Dtracking.

actual-stop-validation.json:all10cases pass original20mmslide/5mmheight/−1mmpenetration gates. WorstactualsoleY−30.076µm,maxplantedheight30.076µm,maxworldZdrift6.522µm,full3Dplanteddriftbound30.586µm.24sharedheadneckpairs gap0. Wholemeshsurfaceentrydifference≤.085µm,finalneutraldifference≤.017µm afterremovingexternaltravel. No initial/final posejump at these sampledcases. Minplanned2feet support; no force/balance/pressure certificate.

Reachgate uses strict geometric r<1.20m and r>.10m,never clips. Defaultmaxreach1.197094963m. Negative stressSTOP_DECEL_S=2 rejects all10cases with actualunreachabletarget/time/limb vectors in rejected-long-decel-planner-failures.json. These are retained validfailures, not relaxedthresholds. Aninitialnegative-stresssummary max(empty)printbug occurred after receiptswerewritten; fixeddiagnosticdefaultNone, geometricrejections unchanged.

## Rebuild

node --experimental-loader ./three-loader.mjs ./capture.mjs
python plan_stop.py
python export_stops.py
python check_preservation.py
node khronos.cjs
node --experimental-loader ./three-loader.mjs ./validate_stops.mjs
STOP_DECEL_S=2 STOP_PREFIX=rejected-long-decel- python plan_stop.py

Nodeoutsideproof uses existing installedThree/validator paths; no app dependency mutation. Mainplanner/exporter Pythonstdlib; solver is bundledoriginalCC0. CPUonly, no browser/sourceimages. Rig/geometry originalCC0; originalplanner/IK/exportCC0; projectintegration/testglueGPL. License/liberty proposal separate. No production API/scene release or ticketclosure requested.

Next after this stablearchive: separate source-only idle→gait/ walk↔trot contacttargetcontroller, denseentryphase coverage, actualextremagear+collision checks, asynchronouscancel/routeadapter+browsercontrolledvisuals, sourceboundedbiomechanics/rig andphotographic review. Keepallpriorfailures; no instantneutralfallthrough.
