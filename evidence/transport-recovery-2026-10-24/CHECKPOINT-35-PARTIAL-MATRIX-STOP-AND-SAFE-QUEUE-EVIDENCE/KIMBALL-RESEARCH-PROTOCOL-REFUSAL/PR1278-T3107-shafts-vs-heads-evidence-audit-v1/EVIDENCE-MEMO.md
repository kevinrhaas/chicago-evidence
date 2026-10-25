# T3107: two shaft bodies are present; complete stack acceptance is not demonstrated

**Conclusion:** both south stone bodies are built. The existing evidence does **not** establish that both stacks are built to HABS1 with only later-ticket elements remaining. A separate T3107-linked front-stack total-height discrepancy remains OPEN. The records do not isolate a bare-shaft neck measurement, so it would also be wrong to assert that the exposed shaft alone is definitively wrong, or that replacing only the heads definitely resolves the problem. The unfinished front/camera work makes that distinction unresolved.

T3107's exact title is:

> 1801 Prairie's south face from HABS photograph 1 (Harold Allen, June 1965, from the south-west): the picture ingested, its camera solved into data/reference_views/kimball_house_1801_prairie/, its match record written, and the south wall's two tall stone stacks built to it

Its unfilled Acceptance template does not narrow “two tall stone stacks built to it” to count/material alone. No acceptance, ticket or verdict was changed.

## Exact existing entries

The records have no per-difference ID field. These are exact JSON pointers within the hashed HABS1 match record, rather than newly invented IDs:

| HABS1 entry | Actual status and content | Consequence |
|---|---|---|
| `/differences/0` | FIXED: “the south wall's two tall stacks…rise from the main cornice over the wall line in pale ashlar…the front one at about u14.45…rear…u3.2…the build had one small reconstructed brick stack…” | Pair/material/coarse position are delivered. This entry does not erase the next one. |
| `/differences/1` | OPEN: “the front stack's height…the print's cap stands about167px (about3.5m) over the cresting…top at y128px; the build holds it to18.0m…so its cap renders well under the print's (L-kimball-1801-south-stacks-3107)” | An explicit T3107-linked total vertical-extent/phase issue remains. It is a separate entry from heads. |
| `/differences/2` | OPEN: moulded collar, diamond-latticed panels about1.5m deep and moulded cap; build has one plain0.8m cap, explicitly T3109. | Later head/collar work is real and separate. |
| `/differences/3` | OPEN: each shaft widens below the curb into a broader base down to cornice; build shafts run straight, explicitly T3109. | Later lower-stage work is explicit, not silently called matched shaft detail. |
| `/differences/4` | OPEN: two-storey round southwest bay and pierced balcony versus flat/chamfered corner, explicitly T3108. | Current front geometry is not a reliable solved-photo match. |
| `/differences/5` | OPEN: narrower paired-light gabled pavilion and re-centered apex, explicitly T3108. | The relevant front bearing geometry is still wrong. |
| `/differences/6` | OPEN: corner cornice about85px low, about10px at southeast end; “The camera or the corner's cornice is wrong, and the front T-3108 rebuilds decides which”. | This is an explicit geometric/camera dependency, not an arbitrary demand for more validation. |

The exact full entry strings are preserved in SHAFTS-VS-HEADS-EXACT-EVIDENCE.json and byte-exact match-record copies. In Taylor.match, `/differences/38` is **NOT SHOWN**: “this camera cannot see them; the front one, built to18.0m, stays under the deck's line from this eye”. It is not a measured period height or a photographically fixed stack. Liberty prose says the1965height is open in both records; the actual Taylor status remains NOT SHOWN.

## Actual current construction

The structure record's `/phases/0/form/chimneys` remains **reconstructed**. The first two stack rows are:

| Stack row | u/v, metres | Plan, metres | Total cap top | Cap |
|---|---|---|---|---|
| `/value/stacks/0`, front |14.45 /10.8|1.2×1.0|18.0m|0.8m deep,0.15m proud|
| `/value/stacks/1`, rear |3.2 /10.7|1.45×1.2|20.1m|0.8m deep,0.15m proud|

Both name `fabric:"stone"` and `on_cornice:true`. Current parameters give a cornice datum8.9m. Unchanged native code extends the body into the cap by half its depth: front body extrusion ends17.6m while the cap begins17.2m and tops18.0m; rear body ends19.7m, cap begins19.3m and tops20.1m. These are simple readings of current data/code, not a new generator execution or emitted-vertex measurement.

The source note reads a provisional HABS1 front cap at about19.25m but deliberately builds18.0m under its Taylor phase ruling. It explicitly acknowledges the uncertain camera and open1965height. The retained HABS1 comparison visibly shows that low front total cap and the unarticulated head/base shapes. Missing head geometry can contribute to the total-height difference; there is no independently quantified neck/collar control here to prove how much belongs to shaft height versus the future head. The known corner/camera error also prevents treating the provisional19.25m as a calibrated1904 height.

## Source identity

The existing side-by-sides were actually viewed; no new render ran. Each current master/camera/photo matches its recorded SHA256. Exact comparison-file hashes are additionally preserved. The main pins are:

- Master: `39ed6df6e220bf154aeba2bbe776c00db29741fd4e3c9b2c74a4fce7adbb8285`.
- Web: `879c691d8853476499af1d06c4e4fed63f4018b273e72f17cb3f3b12a591f7c3`.
- HABS1 camera: `f46ae16fefb6fcc9978291adbe19363723815faa4c42f16927fd46e51084a5bc`.
- HABS1 reference photo: `be2d21b595907011c7fe29c3e3765f754486cee1acdd321fed62f683ae6e0cbf`.
- HABS1 comparison: `6886f382862fd3cc35284e4964abdc38eede0e2e5daa97353f9b603e2cb45a7b`.
- Taylor camera: `c265b79cad9c28ef67d0c64b0fe0f9f9a0a11d9d207a242a01fdf8c03bcd810e`.
- Taylor photo: `91af36528e241b89c9bb900758c26cbe876741fb8761b7f58b34ae2bbf42de34`.
- Taylor comparison: `20586a17aa229f452256a5aa9d868adcd46c29d809719568b622f0fb00de07dc`.

These are retained source/record linkages and exact existing comparison bytes, not a fresh regeneration/reproducibility claim. H747/treefc8 remains unchanged.

## Binary demonstration criteria and dependency

- Two pale south bodies, rather than one brick body, are present: **YES**.
- Every remaining discrepancy belongs exclusively to T3108/09/10 and none remains within T3107's stack extent/phase: **NO**; HABS1 entry1 remains OPEN under its T3107 liberty.
- Current front stack total height is demonstrated consistent with HABS1 and period evidence: **NO**.
- Existing evidence proves whether the bare shaft neck alone is wrong or all discrepancy is missing later head work: **NO**; that isolated measurement is absent. “Not demonstrated” is not a new assertion that the bare shaft is wrong.
- T3109 explicitly owns head/collar and lower-stage differences, and T3108 explicitly owns front/camera differences: **YES**; that ownership does not close entry1.
- T3107/full-building photographic acceptance can be certified now: **NO**.

The actual source-backed resolution route is period south-side/roof evidence **or** the camera re-solved on the rebuilt frontT3108. The available period corpus did not settle the height; the one authorized1973link-only retrieval failed CONNECT403 and remains uninspected. T3108's normal claim was refused solely because our T3107 PR1278 is in review on this same house. Therefore there is an actual ownership/dependency conflict: T3107's outstanding vertical/phase interpretation cannot currently be settled through the front/camera work its own source record names. No force, filtered PR list, ticket release/relabel, PR closure or unclaimed implementation was used. Keep1278DRAFT and preserve that conflict; do not redefine acceptance to fit the prototype. T3109/10 and fullT1890 stayOPEN. Primary transport qualification continues independently.
