PREP ONLY. Browser helpers are byte-exact V7, including per-poll original P14 condition/timestamp trace.
Staged wrapper uses V6 source guard and explicit ROOT GO; fixed HEAD d067 and reviewed MERGE_HEAD42b9.
Final TREE/APP/index are deliberately UNBOUND; ROOT fills them only from actual owner/staging closure.
No hardcoded historical APP, no fake gate/commit/memory PASS. Native owner receipt must be fresh and match
actual APP/HEAD/MERGE_HEAD, with status TARGETED_FIXTURES_AND_NATIVE_OWNERS_PASS_NOT_FULL_PREFLIGHT;
its native ledger, cleanup/resources, and fix file pins are checked. Native publication/check receipts must
bind actual source before/after and original180/120caps. Exact original600/300/240/30world limits remain.
If actual new owner closure uses a different schema, stop and adapt to that observed schema explicitly.
ROOT copies/fills V8-ROOT-GO-UNBOUND-TEMPLATE.json, enables only its desired explicit GO and template_only=false.
Native publication: python3 publish_staged_source.py --binding /ROOT/GO.json --out /ROOT/new-publication
Then fill publication receipt path/hash. World: python3 run_current_world_case.py --binding /ROOT/GO.json --year 1904 --viewport mobile --scope C --out /ROOT/new-world
