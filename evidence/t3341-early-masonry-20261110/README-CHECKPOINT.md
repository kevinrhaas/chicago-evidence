# T-3341: actual early brick and clay surface qualification

Source PR: https://github.com/kevinrhaas/chicago/pull/1918.
Runtime source: `cab45145391cccb84ab408123b70207c32634fcc`.

**Runtime acceptance passes.** Both scenes boot with ordinary upload release and default device selection. The 28 accepted surface frames and two detail-roundtrip frames were directly opened and reviewed. The source changes do not edit native assets, geometry, confidence, or 1904 material bindings. Nine protected source checks (eight parts and aggregate) are green on cab451. The captured moving-frame/upload-release states are identified separately; final GitHub checks and the dev merge remain release gates, not assumed successes.

| Actual gate | Result | Ceiling |
| --- | ---: | ---: |
| Default1835 first-visit gzip wire | 46,888,266 bytes /44.716135MiB |44.9MiB |
| Default1812 phone memory |320,512,587 bytes /305.664622MiB |350MiB, unchanged |
| Default1835 phone memory |533,963,944 bytes /509.227699MiB |550MiB, unchanged |

Official tools are run unmodified: `measure_boot_payload.mjs --check --json --entries …`, and `measure_memory.mjs --gate --year1812,1835 --only mobile --no-snapshot --json …`. The raw memory meter's ticket field names its own T-2546 provenance; this packet's wrapper identifies the T-3341 qualification. No refused resources, forced tier, retained-geometry route, cap waiver, or phone-geometry removal is used. The boot's1207 requests have zero failures. Both memory rows use Light and have zero page errors. Whole-boot before/after source/build identity stays fixed.

The new masonry group has nine actually requested resources totaling927,833 gzip-wire bytes. There is no newly fetched albedo URL in the normal after boot. The prior45,948,374-byte post-B baseline predates other source integrated through PR1910, so the939,892-byte whole-boot difference includes upstream horse, asset-publication and metadata changes; it is not all attributed to T-3341. Exact per-URL entries and deltas are retained. Whole current boot is gated regardless of cause.

`full-review/` has exact publishedGLB SHA256 and sidecar/grade pins, actual instance matrices and camera stations, map dimensions and binding counts, production release state and all error/request lists. The actual1835 visual build is39df38072a, built2026-11-10T12:29:18Z. The1812/resource build iscab4514539, built2026-11-10T12:54:09Z. Their only runtime difference is behavior-identical material ownership initialization rewritten in the existing T3226 guard's literal form; actual33-house and three negative-fixture checks pass without changing that owner. The research-doc count is corrected to14 mapped early material instances including the LakeHouse shell.

The14 mapped controls retain their period sheets and existing shuffle. Newly bound meshes:1835 brick357/clay63;1812 brick4/clay11. Desktop maps are1024 pixels; default390x780 phone maps are512. Both1835 detail roundtrips retain material bindings. All actual visual legs have zero page, console, failed-request and bad-response errors. Existing declared review annotations are classified separately (14 in1835,26 in1812), not silently ignored.

**View limits:** these are reconstructed diagnostic camera stations, not historical source-picture cameras. Actual production UI is retained. Desktop People cards sit beside, clear of, the target stack faces. Six original phone frames were rejected when that card covered the stacks; their `*-navigator-obstructed/` originals are preserved. Corrected captures dock the real navigator through its app API; the stack faces are fully exposed. The accepted before-magazine phone capture catches its closing transition over the lower door; the full upper brick-wall control is unobstructed and qualifies brick appearance only. It does not qualify the door. Screenshots are never CSS-edited or replaced. Each capture draws the real app; ordinary draws are held between shots to keep review bounded.

`proof/` contains standalone shader-development views, including compressed512/1024 and full WebP fallback, and explicitly rejected setup404 fixtures. It does not substitute for full-app acceptance or prove fallback phone memory. `CURRENT-CI-PART6.log` retains the old39df literal-source failure; cab451 fixes it. Earlier checkpoint CI logs retain the initially stale liberties and unpriced storage failures, later corrected. See the final qualification wrapper for actual success and remaining release gates.
