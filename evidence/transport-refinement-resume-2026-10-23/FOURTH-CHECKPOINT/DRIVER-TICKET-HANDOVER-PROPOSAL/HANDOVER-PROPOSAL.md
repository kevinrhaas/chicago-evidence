# Resumed people and transport work — 23 October 2026, 23:31 UTC

PR #1244 remains merged to DEV as `fa115d7`; its standing horse in the 1835 Western Hotel yard was publicly verified at 19:08 UTC. PR #1175 previously delivered parked wagons, distinct canvas finishes, a Brougham and Otis Bardwell. **The resumed work below is local and has not been newly pushed or merged.** An actual GitHub API read returned HTTP 401, and the evidence push could not authenticate. Verify a successful push before calling the new checkpoints GitHub-backed.

Root claimed T-2794, T-2800, T-2803 and T-2804 at 22:45–22:46 UTC. Those claims are active at this observation; T-2803/T-2804 form one group. Exact ownership is in OWNERSHIP-SNAPSHOT.json. The existing `pr: 1244` on T-2800/T-2803 refers to the earlier standing increment. None of these broad tickets is complete. Preserve queue order and renew or release claims through the normal CLI as work continues.

The resumed source base was DEV `5f15de2ba89a9aeef602b01462c0c688fe27280e`; root's recorded branch is `steward/t2794-t2800-photographic-refinement-20261023-2245`. Check actual current source and intake state before using this snapshot.

## T-2804: seated driver fit

Existing reconstructed 1835 teamster **Otis Bardwell** (`rc_bardwell_otis`) already has idle, sit_drive and walk assets. Original exported trousers crossed the W01 bench by 7.818 mm across 56 triangles while his shoes met the footboard. A 14.08 mm internal pelvis/trunk correction fixes source foot and ball frames. Actual written engineering GLBs, reloaded through GLTFLoader/Mixer, then pass near LOD0/1; pose-only far failures remain saved.

A separate explicit prototype retains the passing LOD1 trouser envelope at LOD2/3. All eight source/web exports pass static cloth/bench and shoe/board checks at five times: zero crossings, 0.101–0.108 mm cloth clearance, at most 0.111 micrometre complete-shoe movement. Hidden body, shirt and waistcoat also clear the bench. Human contract and Khronos checks pass for all eight, with zero errors or warnings.

The extra cost is 869 triangles at LOD2 and 1,303 at LOD3; nine draws/materials and existing textures remain. Prototype far web files are 697,816 and 387,272 bytes. These are **engineering derivatives**, with no fresh canonical Blender master, visual/GPU/world/photographic or occupied-driver acceptance. No actor was added or enabled.

Recovery: `/workspace/shared/T2804-PEOPLE-DRIVER-RESUME-20261023-2245/`. CHECKPOINT-1 preserves near outputs, original far failures and controls; CHECKPOINT-2 holds corrected far outputs, all-eight readback and a four-file canonical source proposal; BODY-SEAT-SUPPLEMENT adds body clearance. C1 manifest starts `3db9afbf`; C2 starts `522f425f`. Exact hashes and next steps are in their manifests and CANONICAL-INTEGRATION-PLAN.md.

Next: restore GitHub authorization, review and push the four-file source proposal on an owner-visible authoring PR, then use the **existing** humans workflow with `build_seated_driver_study=true`. `build_teamsters=false` is sufficient, but all three named masters build. WORKFLOW-BUILD-PATH.md provides exact commands, pins and artifacts. A normal PR humans run does not build the study. Requalify actual emitted hashes and inspect pictures and budgets; existing seated captures do not themselves prove all-LOD contact.

## Other active lanes

**T-2794:** V18 rounded coach lamps passed deterministic native generation/readback, four Khronos checks and eight corruption refusals. Actual counts are 33,374 near / 11,706 mid triangles. Inactive REGISTRATION-V3 preserves V17 history and existing guards. Browser source8 failed before page load from thread exhaustion; root owns image review and any app intake. Folder: T2794-LAMP-RESUME-20261023-2245.

**T-2800:** Eye-only UV candidate `d4544c28` has 12 actual CPU textured renders at six fixed native cameras, with no changed pixels outside projected eyes. This software diagnostic does not establish native Three PBR, browser, GPU, world or photographic acceptance. Body, hair, stance, coat and embedded image bytes remain protected. A separate inactive 1904 extension passed actual loader/clone/Mixer 129-sample CPU checks on original `b479`; canonical 1904 activation remains false. That qualification cannot silently transfer to the eye candidate's new hash. Folders: T2800-EYE-REFINEMENT-RESUME-20261023-2245 and T2800-1904-RESUME-20261023-2245.

**T-2803:** Constrained creeping-walk and corrective-basis work is still CPU progress. The rank40-plus-mean candidate needs 41 dense targets and may substantially increase shader fetches. No basis binary or gait GLB is exported or approved; portable keys/midpoints, GPU cost and natural walking remain unqualified. Continue a small/sparse correction or rig/skin improvement without widening physical limits. Folder: T2803-GAIT-RESUME-20261023-2245/CHECKPOINT-5.

Retain all failures. Photographic finish, natural gaits, harness/gear, reins/grips, rider/driver attachment, transitions, traffic circuits, boarding and riding remain unfinished. Kinzie's 1812 and Glessner's 1904 clothing/appearance studies are not substitutes for this 1835 teamster and gain no scene placement from these prototypes.
