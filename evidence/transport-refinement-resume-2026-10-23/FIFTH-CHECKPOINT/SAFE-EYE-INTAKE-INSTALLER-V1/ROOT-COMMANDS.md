The read-only preparation compared all 24 original preimages. Every ordinary pin matches. The only permitted drift is the exact incoming LIBERTIES SHA `346fd35e1ea7b7e1e1711ef5fa13ff36f9fb3a8e38c0922ce0605bb1c3803ae4`: 33 appended Glessner lines. Three-way base is the root-provided carriage checkpoint, SHA `ec8d8efe519dee1aaf07249798127bfc1bfc6c89c268f57e65b189db10375ba4`. All incoming bytes are preserved; only the exact 1,367-byte eye UV amendment is inserted into the unchanged horse entry.

Review `DRY-RUN-1/INCOMING-CHANGES.diff` and `DRY-RUN-1/UV-ONLY-INSTALL.diff`. `DRY-RUN-1/LIBERTIES-MERGED.md` is the computed result, SHA `f9cfd649c151c8bfcd5ec7d0dffa9cd9a39dee3654943d69fe3b9b49b173c3d7`.

Installer source SHA: `69d04fad8f5a8f420612883f484d15a570d733fe92faa231e353a5488de64368`.

Reviewed dry-run manifest SHA: `d073c0cb17f988168a62dd8011440419605d515107a65a5cb46efaad0131468f`.

Root may apply the exact reviewed plan after the ticket split/claim is settled:

```sh
python3 /workspace/shared/T2800-EYE-REFINEMENT-RESUME-20261023-2245/SAFE-EYE-INTAKE-INSTALLER-V1/install_eye_intake.py --apply --app-root /workspace/chicago-waistcoat/chicago/4d --review-manifest /workspace/shared/T2800-EYE-REFINEMENT-RESUME-20261023-2245/SAFE-EYE-INTAKE-INSTALLER-V1/DRY-RUN-1/REVIEW-MANIFEST.json --review-sha256 d073c0cb17f988168a62dd8011440419605d515107a65a5cb46efaad0131468f --out-dir /workspace/shared/T2800-EYE-REFINEMENT-RESUME-20261023-2245/SAFE-EYE-INTAKE-INSTALLER-V1/APPLY-1
```

Use root's owned bounded command wrapper. This preparation has **not** executed apply, app/runtime checks or Git/index mutations. Apply installs exactly 23 files, skips `changelog.d/T-2800.json`, and writes a durable outside-app receipt and exact preimage backups. Root supplies one merged group entry under T-3083 independently. The selected source proposal remains the already audited 24-file intake; no other file is allowed.

Apply rechecks all proposal and current file hashes, source bytes and mode bits against the reviewed manifest before any app write. It refuses any additional drift. It uses atomic file replacements and readback; if a write fails, rollback restores only exact owned installed bytes and preserves concurrent changes. It never invokes Git or touches the index, source refs, ticket claims, publication or generated compiler outputs. Existing b479 source assets and historical results are outside the write allowlist.

To generate another read-only review after confirming inputs remain unchanged, use a fresh output folder:

```sh
python3 /workspace/shared/T2800-EYE-REFINEMENT-RESUME-20261023-2245/SAFE-EYE-INTAKE-INSTALLER-V1/install_eye_intake.py --dry-run --app-root /workspace/chicago-waistcoat/chicago/4d --out-dir /workspace/shared/T2800-EYE-REFINEMENT-RESUME-20261023-2245/SAFE-EYE-INTAKE-INSTALLER-V1/DRY-RUN-2
```

If there is new drift, stop and reconcile the affected source explicitly. There is no force or fuzzy merge option. Root must still run compiler regeneration, the source-boundary/idle contract checks and required integration gates from the intake's `ROOT-INTEGRATION.md`. CPU/software evidence does not become native/mobile/PBR/world/photographic acceptance.
