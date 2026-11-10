# Actual A5 baseline before the B29 parcel

Measured the unchanged published c5551fdd66 app/models from native9dd9ba7ddd22c6ff87e52522497205f62133fa1f, run42745792113. Root source84628e5945100671ec899b351379d778d9f15ebe changes only storage validation/documentation, not these app/model bytes. Commands used the existing `/usr/bin/chromium` and `/tmp/chicago-browser-tools/node_modules`. No source, tool, app, ceiling or Light-floor edits were made. GPU has been released.

Official commands, serially:

```
node tools/measure_boot_payload.mjs --json --entries /tmp/nov10-a5-pre-b-budget/boot-entries.json
node tools/measure_detail_ceilings.mjs --only desktop --levels balanced --json /tmp/nov10-a5-pre-b-budget/balanced-six-stands-desktop.json
```

The boot tool measured **45,932,852 bytes =43.804981 MiB**,1196 requests, ready plus3-second settle, zero failed requests. This still exceeds the old40.2 MiB allowance by3.604981 MiB. Its exit0 is measurement completion, not an old-budget PASS. A44.1 MiB proposal would leave at most309,349 whole wire bytes for additions; that is conditional room, not a measured B delta.

The official normal-loop, desktop1280x800 Balanced sweep covers all six gate stands:

| Stand | Triangles | Calls |
| --- | ---: | ---: |
| lake_at_canal | 2471852 | 5617 |
| the_forks | 2064595 | 4244 |
| from_above | 1676670 | 2826 |
| lake_and_market | 2341912 | 4007 |
| prairie_west | 2595407 | 6441 |
| sauganash_26 | 1731348 | 2853 |

Its own current2,625,000 ceiling clears the new sweep worst2,595,407 at West prairie by29,593, with zero page errors. However, the retained actual native full smoke measured **2,657,398 triangles/6441 calls** at that same named worst stand, exceeding the old ceiling by32,398. That literal RED and its raw log hash are retained in the JSON receipt. The61,991-triangle instrument/context difference is not explained or discarded. For pricing, use the **higher retained full-smoke cost**, giving only**17,602 drawn triangles** of room under a proposed2,675,000 ceiling, rather than claiming79,593 from the lower sweep.

B29 means the25-output frame family, including its two variants, plus officer stairs, barn cupola, palisade posterns and the reconstructed commandant gallery. These pre-B runs do not measure that new geometry or its gzip cost. The parent must price the exact source union inside309,349 additional wire bytes and17,602 additional worst-frame triangles, then verify the actual retained native/published output. Neither a B-fit result nor a budget approval is fabricated here. Light's floor and all other bars remain unchanged.

`INPUT-BINDINGS.json` records source/published/native/tool hashes; `COMMAND-RECEIPT.json` records exact commands, exits and timings. Raw boot JSON plus all1196 entry byte counts, six-stand JSON and literal stdout/stderr are retained beside this report. Both official runs exited0; their timings were52.83s boot and195.31s six-stand sweep. This report does not claim full smoke or source CI passed.
