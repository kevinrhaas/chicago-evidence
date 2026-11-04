# Prepared controller, not dispatched

Root review target: controller.py. Workflow feature SHA b37fdeca6b74d8e3c70945a75687140c0718f549, exact branch checked. REQUEST.json contains only approved app/target/resume/slice/slices/original lane/max_turns inputs; model, effort, processor and time remain workflow defaults. Native job is targeted-chicago on Ubuntu26.04 with150minute cap.

PREPARED.json records exact PR headbc0, existing branch/dev base, old worker completed failure, T2380 OPEN/unclaimed with native preserved handoff, no other matching PR or active target/lane, native normal lap status, exact dev commit+tree plus ten guarded source blobs including current Pruyne MASTER/WEB, both manifests and frame producers. Both exact-SHA hosted CI runs were SUCCESS at preparation. Actual dispatch repeats all guards, requires prepared source tree unchanged, checks final ticket/PR/feature/dev/active-owner/lap immediately before a single POST, and saves DISPATCH-ATTEMPT before sending so no ambiguous response is retried automatically.

No source/ticket handoff edit is needed: immutable published handoff e27ec67 already explicitly requires UNQUALIFIED working-source/raw-log/hash checkpoints to chicago-evidence every15–20minutes before full gates and forbids unqualified app source commits. Both original images stay DIFFERS and source-four/both UI/native smoke/named gate remain owed.

ROOT-GO.json deliberately does not exist. ROOT-GO-TEMPLATE.json has authorized:false. Only explicit root authorization permits creating authorized:true with the exact request hash. Dispatch and monitoring are separate protected600second commands through run-with-reaping.py. They write only this outside-source packet; native lap --status reads remote marker ownership and may fetch marker metadata but changes no tracked source or ticket file. No native host Blender, code commit, merge or fallback queue operation occurs here.

Suggested invocation after root GO, each status path must be fresh:

    source /workspace/shared/resume-chicago-env.sh
    python3 /workspace/shared/run-with-reaping.py DISPATCH-REAPER.json -- timeout --signal=TERM --kill-after=15s 600s nice -n19 taskset -c2 python3 controller.py dispatch

Then monitor the discovered ACTUAL-RUN.json via the same wrapper and fresh MONITOR-REAPER.json with controller.py monitor --snapshots10 --interval30. Monitor is read-only and reports native job step/runner, exact claim URL, existing PR head/state; it stops at our exact claim, another claimant or completed run. It never cancels or force-releases a job/claim.
