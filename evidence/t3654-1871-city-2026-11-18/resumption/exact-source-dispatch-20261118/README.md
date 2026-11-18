# Current guarded dispatch procedure

This is the latest temporary dispatch helper/procedure archived for T-3654. The helper SHA256 is 45b62f693e39ac8678b82089fd46ca2c875496631fd0fe7a45a8373d311287b3. The two `before-*` files and the older parent-directory helper/plan are historical execution evidence; restore this version when resuming.

The checkpoint bypass is removed. Before ledger mutation or dispatch, the helper requires literal true complete source proof for the exact requested commit, the expected repository/PR/run and dev-base identities, eight distinct verified successful source jobs, a successful aggregate, no hold, matching current local/remote heads, a clean tracked checkout, the unchanged verified dev base and matching live GitHub success metadata. Reconcile saved run IDs before retrying interrupted work. The recovery snapshot identifies the required summary fields and reconstruction rules; an absent or partial source summary is not authorization to dispatch.

The focused proof records two positive controls and 22 refusals, with zero real external commands, dispatches or source-repository mutations. Positive controls used simulated live metadata and an empty plan. This is procedure testing, not proof that the current hosted source gate passed. The actual source guard remained false and no fresh legacy runs had been dispatched at capture.

The scripts retain their executed `/tmp` and `/workspace` paths; restore or deliberately adjust those paths and use the existing real-metadata/log procedure before use. Authentication remains delegated to gh; no credentials or environment dumps are included. The archived test writes its proof path if rerun, so preserve the frozen proof and run any new reproduction in a separate location.
