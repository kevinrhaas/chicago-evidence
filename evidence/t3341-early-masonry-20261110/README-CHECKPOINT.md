# T-3341: actual early brick and clay surface qualification

Source PR: https://github.com/kevinrhaas/chicago/pull/1918.
Runtime source: `cab45145391cccb84ab408123b70207c32634fcc`.

**Runtime acceptance passes.** Both scenes boot with ordinary upload release and default device selection. The 28 accepted surface frames and two detail-roundtrip frames were directly opened and reviewed. The source changes do not edit native assets, geometry, confidence, or 1904 material bindings. Nine protected source checks (eight parts and aggregate) are green on `cab4514539`. Moving-frame and upload-release checks also pass on that runtime. The final documentation head must pass its own protected checks before the ordinary dev merge; no unmerged work is called released.

| Actual gate | Result | Ceiling |
| --- | ---: | ---: |
| Default 1835 first-visit gzip wire | 46,888,266 bytes / 44.716135  MiB | 44.9  MiB |
| Default 1812 phone memory |320,512,587 bytes / 305.664622  MiB | 350 MiB, unchanged |
| Default 1835 phone memory |533,963,944 bytes / 509.227699  MiB | 550 MiB, unchanged |

Official tools are run unmodified: `measure_boot_payload.mjs --check --json --entries …`, and `measure_memory.mjs --gate --year 1812,1835 --only mobile --no-snapshot --json …`. The raw memory meter's ticket field names its own T-2546 provenance; this packet's wrapper identifies the T-3341 qualification. No refused resources, forced tier, retained-geometry route, cap waiver, or phone-geometry removal is used. The boot's 1,207 requests have zero failures. Both memory rows use Light and have zero page errors. Whole-boot before/after source/build identity stays fixed.

The new masonry group has nine actually requested resources totaling 927,833 gzip-wire bytes. There is no newly fetched albedo URL in the normal after boot. The prior 45,948,374-byte post-B baseline predates other source integrated through PR1910, so the 939,892-byte whole-boot difference includes upstream horse, asset-publication and metadata changes; it is not all attributed to T-3341. Exact per-URL entries and deltas are retained. Whole current boot is gated regardless of cause.

`full-review/` has exact publishedGLB SHA256 and sidecar/grade pins, actual instance matrices and camera stations, map dimensions and binding counts, production release state and all error/request lists. The actual 1835 visual build is `39df38072a`, built 2026-11-10T12:29:18Z. The 1812/resource build is `cab4514539`, built 2026-11-10T12:54:09Z. Their only runtime difference is behavior-identical material ownership initialization rewritten in the existing T-3226 guard's literal form; actual 33-house and three negative-fixture checks pass without changing that owner. The research-doc count is corrected to14 mapped early material instances including the LakeHouse shell.

The 14 mapped controls retain their period sheets and existing shuffle. Newly bound meshes:1835 brick 357/clay 63;1812 brick 4/clay 11. Desktop maps are 1024 pixels; default 390x780 phone maps are 512. Both 1835 detail roundtrips retain material bindings. All actual visual legs have zero page, console, failed-request and bad-response errors. Existing declared review annotations are classified separately (14 in 1835,26 in 1812), not silently ignored.

**View limits:** these are reconstructed diagnostic camera stations, not historical source-picture cameras. Actual production UI is retained. Desktop People cards sit beside, clear of, the target stack faces. Six original phone frames were rejected when that card covered the stacks; their `*-navigator-obstructed/` originals are preserved. Corrected captures dock the real navigator through its app API; the stack faces are fully exposed. The accepted before-magazine phone capture catches its closing transition over the lower door; the full upper brick-wall control is unobstructed and qualifies brick appearance only. It does not qualify the door. Screenshots are never CSS-edited or replaced. Each capture draws the real app; ordinary draws are held between shots to keep review bounded.

`proof/` contains standalone shader-development views, including compressed512/1024 and full WebP fallback, and explicitly rejected setup404 fixtures. It does not substitute for full-app acceptance or prove fallback phone memory. `CURRENT-CI-PART6.log` retains the old39df literal-source failure; cab451 fixes it. Earlier checkpoint CI logs retain the initially stale liberties and unpriced storage failures, later corrected. See the final qualification wrapper for actual success and remaining release gates.

## Post-dev integration: actual resource gates pass

Final integration head `4ec8b2578578416fa7c5535d1a788b26cd0b9bf5` merges concurrent dev `8aa1afcac4` without changing any of the three qualified masonry runtime blobs. Both reconstruction admissions are preserved, canonical liberties count 1090 and source-use remains 659 sources /270168 index bytes. The feature diff against dev touches no native GLB, WEB, sidecar or human instance. DEV-INTEGRATION-PROOF.json records exact blob identities; the canonical owners and negative fixtures pass again. No sourceRoot feature file was edited by the masonry agent.

`resource-integrated/` contains the official normal-production readings from the exact integrated publication built 2026-11-10T13:29:59Z, with fixed source/build identity before and after:

| Gate | Actual | Ceiling |
| --- | ---: | ---: |
|1835 gzip-wire boot |46,890,182 bytes / 44.717962 MiB | 44.9 MiB |
|1812 default-phone memory |319,410,638 bytes / 304.613722 MiB | 350 MiB, unchanged |
|1835 default-phone memory |525,145,446 bytes / 500.817724 MiB | 550 MiB, unchanged |

Boot has 1,207 actual requests, zero failures and 190,880 whole bytes spare; integration adds only 1,916 bytes versus the earlier qualified boot. Both actual memory rows use default Light, report zero page errors and keep normal upload release. No retained-geometry route, refused resource or changed phone cap is used. All measurement browsers exit and the GPU is released. These integrated values supersede the prior cab451 resource readings above; the older raw readings and 28-view appearance packet are preserved.

Current-head protected CI and the ordinary dev merge remain the release gate, recorded live in PR #1918. No further source polish is planned.
