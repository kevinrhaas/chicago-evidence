# Gait strict physical failure checkpoint2

V23 triangle deformation-gradient local/global correction FAILS minedge0.88705; other edge/area/contact/normal/seam/loop bounds pass. The local clamp is soft after global reconstruction: singular values .831–1.114, so it does not enforce the proposed envelope globally. Saved fixed-edge diagnosis proves all8270 fullyfixed edges remain0.999990–1.000005 and worst strain witnesses are unprotected/free; no protected-anchor impossibility was found.

V24 uses ADMM dual enforcement of F(q)=projectedF, same .95–1.05 local singular envelope and original physical limits. Actual65 physical edge/area/contact/seam/loop bounds PASS: edges .94804–1.05139, areas .90401–1.09797. But one small upper-chest triangle5381 reverses its rest-relative normal at t1.1 (dot−.29785); overallFAIL. Primal residual .16012 means no convergence certificate. Max corrective displacement32.98mm; exact corrective position/normal loop0. Actual103.70s, ownedcleanup empty. No export/app/browser action or accepted gait.

The local strain-only SVD projection does not constrain triangle normal hemisphere. A next source correction can add an explicit orientation cone using a proper rotation of projectedF (preserves singular values) with fixed protected rows and unchanged original normals guard. No screen is to be weakened. Naturalness/portableGLTF/midpoint contact/selfcollision/photo/teams/riding remain unproved. A65target morph asset is not approved; report exact serialized-payload and GPUtexture estimates BEFORE any export.

Raw corrected frameNPZ files are diagnostic arrays, not installed/exported models. Baseline GLB is not duplicated; immutable external pins remain. CHECKPOINT1 preserves earlier V20–22 failures separately. Root owns tickets and GitHub checkpoints.
