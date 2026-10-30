# Closed11d9 native mobile-memory cap failure

This packet preserves the completed native integration attempt on wagon PR1340 public HEAD `11d9c41405d4af74ebf2f036082c47b82240c8b2`, TREE `f33056e53b760803601c2b4daee8f328ae51d4cd`, APP `561705518933dc3a4c6ac260e7ffcf5af857987e`. The actual closure is dated2026-10-30 20:17:34UTC. **The mobile native memory cap failed and blocks merge. PR1340 is unmerged at this cutoff.**

Native publication and source readback passed in47.725180seconds under its original300-second budget. The unchanged native1904 desktop Full meter passed its1300MiB ceiling in241.851698seconds under600:1,195,513,008bytes (1140.130MiB). The separate1125MiB T3173 goal remains unmet and open. This is never called a1125MiB pass.

The unchanged native1904 mobile Light meter measured432,028,870bytes (412.015MiB), exceeding its419,430,400-byte/400MiB native ceiling by12,598,470bytes. It returned1 in68.811417seconds under its original600-second budget. This is an actual native NONPASS, not an observer/setup-only failure or timeout. Native assertions, caps and budgets were not modified.

The controller stopped before either focused lifecycle profile. Original focused code and its separately prepared static loader correction are archived **UNRUN**. The loader correction was found by source inspection; no execution of that loader or corrected controls is claimed. No browser quality acceptance, memory retry, new app source change, complete current-HEAD published suite or ticket closure is claimed.

All three native stages retain actual result/logs, original source bindings, HTTP response records, native output JSON, resources and zero-remaining-owned-child cleanup. The full5734-member published mirror inventory is retained as a manifest, with the closed attempt's exact complete-mirror/source/index equality proof. Actual HTTP769desktop/760mobile responses matched the frozen mirror; both profiles loaded current Kimball and street-tree payloads. Native published shared-sheet readback supplies the transformed GLB source binding; no direct master-versus-transformed byte-equivalence is invented. Mirror members/models themselves are excluded.

The closed comparison retains old-source measurements and current layer changes as bounded diagnosis. It does not establish one cause or attribute the cap failure to Kimball alone. Device DPR3 and native renderer pixelRatio1 on mobile are separately recorded. The separate root desktop decision accepts only the actual1300MiB native result while preserving the unmet1125MiB goal and remaining gates.

Active f560 feature qualification and current11d9 ordinary CI are excluded. Earlier402097b/752b86 packets remain immutable; no earlier results are retargeted. No horse/Otis pass, broad photographic/rider/driver/traffic acceptance, physical-phone/GPU certification or production promotion is claimed.

`MANIFEST.json` maps original paths/modes to lossless gzip payloads with raw and encoded SHA256/length. `python verify_packet.py` verifies all records. No models, images, RAW, actual mirror payloads or Git objects are embedded.
