from pathlib import Path
import datetime
import hashlib
import json
import os

BASE = Path('/workspace/shared')
OUT = BASE / 'ROOT-TRANSPORT-EVIDENCE-FIFTH-20261024'
assert not OUT.exists(), 'Never overwrite an existing frozen transfer'
OUT.mkdir()
inventory = {}
duplicates = []
seen = {}
packets = []

def digest(data):
    return hashlib.sha256(data).hexdigest()

def copy_file(src, dst):
    assert src.is_file() and not src.is_symlink(), src
    data = src.read_bytes()
    pin = digest(data)
    dst.parent.mkdir(parents=True, exist_ok=True)
    assert not dst.exists(), dst
    if len(data) >= 128 * 1024 and pin in seen:
        os.link(seen[pin], dst)
        duplicates.append({'path': str(dst.relative_to(OUT)),
                           'first_destination_copy': str(seen[pin].relative_to(OUT)),
                           'sha256': pin, 'bytes': len(data)})
    else:
        dst.write_bytes(data)
        if len(data) >= 128 * 1024:
            seen[pin] = dst
    assert digest(src.read_bytes()) == pin, 'Source changed during copy: ' + str(src)
    assert digest(dst.read_bytes()) == pin, 'Copy mismatch: ' + str(dst)
    inventory[str(dst.relative_to(OUT))] = {'source': str(src), 'sha256': pin, 'bytes': len(data)}

def copy_tree(source, label):
    src = BASE / source
    assert src.is_dir(), src
    paths = [p for p in sorted(src.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    assert all(not p.is_symlink() for p in paths), src
    for p in paths:
        copy_file(p, OUT / label / p.relative_to(src))
    packets.append({'source': str(src), 'destination': label, 'files': len(paths),
                    'logical_bytes': sum(p.stat().st_size for p in paths)})

for source, label in [
    ('T2803-GAIT-RESUME-20261023-2245/CHECKPOINT-7', 'HORSE-GAIT-CHECKPOINT-7'),
    ('T2803-GAIT-RESUME-20261023-2245/CHECKPOINT-8', 'HORSE-GAIT-CHECKPOINT-8'),
    ('T2803-GAIT-RESUME-20261023-2245/CHECKPOINT-9', 'HORSE-GAIT-CHECKPOINT-9'),
    ('T2800-EYE-REFINEMENT-RESUME-20261023-2245/SAFE-EYE-INTAKE-INSTALLER-V1', 'SAFE-EYE-INTAKE-INSTALLER-V1'),
    ('T2800-EYE-INTAKE-INDEPENDENT-REVIEW-20261023', 'INDEPENDENT-EYE-FINAL-FREEZE-REVIEW'),
]:
    copy_tree(source, label)

root_source = BASE / 'ROOT-TRANSPORT-INTAKE-20261023-2315'
root_names = ['TRANSPORT-HANDOVER-2026-10-24.md', 'define_carriage_children.py',
              'define_horse_children.py', 'HORSE-CHILD-IDS.json', 'update_progress_docs.py']
for name in root_names:
    copy_file(root_source / name, OUT / 'ROOT-HANDOVER-AND-CHILD-DEFINITIONS' / name)
packets.append({'source': str(root_source), 'destination': 'ROOT-HANDOVER-AND-CHILD-DEFINITIONS',
                'files': len(root_names), 'selected_frozen_files_only': root_names,
                'logical_bytes': sum((root_source / n).stat().st_size for n in root_names)})

# These are preparation files only. The installer is preserved, never executed here.
prep_pins = {
    'DRY-RUN-1/INCOMING-CHANGES.diff': '4d0fd735e2fafb2510260c65f42b0c8a61fa3de7c93e0341d3817ba32db2da7d',
    'DRY-RUN-1/LIBERTIES-MERGED.md': 'f9cfd649c151c8bfcd5ec7d0dffa9cd9a39dee3654943d69fe3b9b49b173c3d7',
    'DRY-RUN-1/REVIEW-MANIFEST.json': 'd073c0cb17f988168a62dd8011440419605d515107a65a5cb46efaad0131468f',
    'DRY-RUN-1/UV-AMENDMENT.md': 'b47872ddfc38105c17cad6c9144c7e9e46caf8aa4f9d987fd26ba246fbedf579',
    'DRY-RUN-1/UV-ONLY-INSTALL.diff': '048c6350f9e09d86579048d5ec3d5bf5869afca1155e5b6787599dc99fc6dd6b',
    'ROOT-COMMANDS.md': '7228f7398704fa98bfecbf0609b2cf09b2db880a88a2aedcadd36ba7e5ebd3d3',
    'install_eye_intake.py': '69d04fad8f5a8f420612883f484d15a570d733fe92faa231e353a5488de64368',
}
for rel, pin in prep_pins.items():
    assert digest((OUT / 'SAFE-EYE-INTAKE-INSTALLER-V1' / rel).read_bytes()) == pin, rel

glbs = sorted(OUT.glob('HORSE-GAIT-CHECKPOINT-*/*/*.glb'))
assert len(glbs) == 3
for p in glbs:
    assert p.stat().st_size == 5545416
    assert digest(p.read_bytes()) == '8fc20cf20549d9588c56202d93315dc9f718531fc7a285de2208ce4e36ba9a7b'
assert len({p.stat().st_ino for p in glbs}) == 1, 'Use destination-only exact GLB deduplication'

omissions = [
    {'kind': 'V31 original native geometry', 'bytes': 142554816,
     'sha256': '15c06d3515a24355f0a3a7cc151c467c50017d716efd011e20b60a0dd07c4cbb',
     'original_workspace_parent': '/workspace/shared/T2803-GAIT-RESUME-20261023-2245/V31-SPLIT-PORTABLE-CREEPING-PROTOTYPE',
     'included_proof_pointer': 'HORSE-GAIT-CHECKPOINT-8/V31-SPLIT-PORTABLE-CREEPING-PROTOTYPE/ACTUAL-PORTABLE-257-GUARDS.json'},
    {'kind': 'V32 actual native LoopRepeat265 geometry', 'bytes': 146992320,
     'sha256': 'c7ec8ec28513bdfd51a72e7bfb72ae781a40ede9cc3853b45278f98138ceb639',
     'original_workspace_parent': '/workspace/shared/T2803-GAIT-RESUME-20261023-2245/V32-NATIVE-REPEAT-ONLY-PROOF',
     'included_proof_pointer': 'HORSE-GAIT-CHECKPOINT-9/V32-NATIVE-REPEAT-ONLY-PROOF/ACTUAL-PORTABLE-257-GUARDS.json'},
]
for item in omissions:
    proof = (OUT / item['included_proof_pointer']).read_text()
    assert item['sha256'] in proof, 'Recorded raw geometry pin absent from frozen proof'
    item['proof_field'] = 'actual_positions_normals_sha256'
    item['hash_policy'] = 'Recorded frozen proof hash verified present in included JSON; omitted raw file was not opened or rehashed by assembler.'

# Recheck every original settled source after the entire copy; do not inspect live app.
for rel, pin in inventory.items():
    assert digest(Path(pin['source']).read_bytes()) == pin['sha256'], 'Settled source drift: ' + rel

def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

write_json('SOURCE-COPY-INVENTORY.json', {
    'status': 'FROZEN_SETTLED_SOURCE_BYTES_EXACT_BEFORE_AND_AFTER_COPY',
    'assembled_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'packets': packets, 'files': inventory,
    'live_app_read_or_copied': False, 'Git_operation_performed': False,
    'installer_executed': False, 'actual_numerical_or_browser_checks_performed': False,
})
write_json('DEDUPLICATION-AND-OMISSIONS.json', {
    'strategy': 'Files >=128KiB with identical SHA256 are hardlinked inside the destination only. Original source files are never hardlinked or mutated. All original frozen paths remain; Git naturally deduplicates identical content.',
    'duplicate_files': duplicates,
    'destination_only_hardlink_saved_bytes': sum(x['bytes'] for x in duplicates),
    'excluded_raw_geometry': omissions,
    'same_5545416_byte_GLB_preserved_at_all_three_frozen_paths': [str(p.relative_to(OUT)) for p in glbs],
    'runtime_dependencies_or_node_modules_copied': False,
})

(OUT / 'README.md').write_text('''# Fifth people and transport recovery transfer

This transfer copies settled frozen evidence outside Git for root's next evidence checkpoint. The assembler performs only Python standard-library copying and SHA256 verification under its owned subreaper wrapper. It does not read or copy the live app, run the installer, alter tickets or refs, stage/commit/push, or run Node, a numerical check, browser, container or heavy process. Every original included source is checked before/after copying and rechecked across the complete copy. Frozen files and historical failures remain unchanged.

## Integration status at root's assembly request

Root reports evidence already published through **3ae9f38**. Claims for **T3083, T3086 and T3087** have been pushed, while the full remaining parent scope is preserved by **T3084, T3085, T3088 and T3089**. Claim publication does not mean an app change is committed or merged. The current app refinements are locally installed; the canonical-owner rederive/final gate is **running/pending**, with **no new app commit or PR yet** at this checkpoint. Historical merged standing-horse work is separate. This is recovery evidence, not a green final gate, DEV merge, live deployment or photographic completion. Root alone owns integration, final verification, tickets, Git and publication.

## Gait checkpoints preserve distinct outcomes

- **CHECKPOINT-7 / V30 original resource FAIL:** the exact original encoder exceeded its unchanged 512MiB RSS guard at 597,954,560 bytes, after about 8.14 seconds. It emitted a held 5,545,416-byte diagnostic GLB before the assertion. Its native 257-pose checker was not launched. No end-to-end bounded upstream source/SVD generation pass is claimed.
- **CHECKPOINT-8 / V31 LoopOnce FAIL:** extraction of the pinned V30 basis boundary and byte-identical fresh serialization were followed by actual GLTFLoader, SkeletonUtils clone and native AnimationMixer readback across 257 poses, 11,556 vertices and 14,986 triangles. The original physical guards pass, but clamped LoopOnce endpoint drift fails the unchanged strict 1nm/1e-9 loop guards: about 11.11nm joint-position and 12.33nm surface drift. The actual failure remains included. This split boundary does not fix the earlier upstream memory failure.
- **CHECKPOINT-9 / V32 real native LoopRepeat265 PASS:** actual GLTFLoader, SkeletonUtils clone and AnimationMixer LoopRepeat readback covers 257 keys/midpoints plus eight matched wrap samples. The unchanged contact, domain, physical and strict loop guards pass; loop joint/surface/normal errors are zero. Matched before/after-cycle residual is at most 2.7894e-16m. The held derivative, original guards and failure receipts remain unchanged. Runtime was about 11.314 seconds and max RSS 366,268,416 bytes under the 512MiB bound. This proves the bounded actual readback unit, not bounded upstream generation.

The 0.24m stride / 1.6s / 0.15m/s study is constrained creeping motion. No natural-gait, stop/clamp, standing-to-walking transition, visual, browser/GPU, world/traffic, performance acceptance or riding claim is made. The inherited lateral-sequence label was incorrect for the actual HL -> FR -> HR -> FL offset order and is not silently repaired in frozen source. The original V30 resource FAIL and V31 LoopOnce FAIL are not replaced by V32's limited success. The gait GLB is a held study and is not installed by this transfer.

## Eye intake and source review

**SAFE-EYE-INTAKE-INSTALLER-V1** retains the exact seven preparation files identified by INSTALLER-MANIFEST.json, that manifest, and the ROOT-APPLY-1 receipt, review manifest and original preimages. Seven preparation SHA pins are explicitly checked by this assembler. The original installer and commands are recovery source only; they are not executed. No live app is copied while root's canonical-owner unit is running.

**INDEPENDENT-EYE-FINAL-FREEZE-REVIEW** includes the final APPROVED_SOURCE_FOR_FINAL_FREEZE review, installed-23 source audit, earlier review and reconstructed pre-edit check.sh witness. This is read/hash source approval with its original limited scope: protected original commands, assertions and caps remain; the named stale V17 check label and already-reviewed boundary-check invocation are the scoped changes. It does not constitute a runtime, final-gate, native-browser, world or photographic pass. STATUS/ROADMAP prose differences are intentional scoped child/improvement updates; original b479 assets and historical receipts remain separate.

**ROOT-HANDOVER-AND-CHILD-DEFINITIONS** preserves root's transport handover, carriage and horse child-definition scripts, horse child IDs, and progress-document script. These record the remaining ticket scope and narrow installed improvements. They are copied source, not newly executed ticket mutations or workflow dispatches. Ordinary/fallback Chromium failures before a frame and Docker OCI process-start failure remain nonpasses; no healthy-host native review is invented.

## Integrity, omissions and publication

The outer SHA256 manifest covers every payload file, including frozen inner manifests; it excludes only itself. SOURCE-COPY-INVENTORY.json binds original paths and copied bytes. Exact large duplicates are hardlinked only within this destination. The same 5,545,416-byte held gait GLB (SHA256 8fc20cf20549d9588c56202d93315dc9f718531fc7a285de2208ce4e36ba9a7b) remains at all three frozen checkpoint paths, and Git naturally stores it once.

The 146,992,320-byte V32 raw native geometry and the earlier 142,554,816-byte V31 raw geometry are intentionally excluded. DEDUPLICATION-AND-OMISSIONS.json retains their hashes, original workspace parents and included compact proof pointers. Those recorded pins are verified against included frozen proof JSON; the omitted raw files are not opened or rehashed during this transfer. Compact actual readback JSON, exact source scripts, guard outputs, receipts and held GLBs remain available. No node_modules or runtime dependencies are copied.

The evidence clone uses sparse checkout; root's eventual chosen evidence staging requires **git add --sparse**. This is guidance only, not a performed Git operation. Root must bind the final canonical-owner result before making an app commit/PR claim.
''')

# Preserve the assembler itself as reviewable provenance, without a self-hashing loop.
copy_file(Path(__file__), OUT / 'assemble_transport_fifth_checkpoint_20261024.py')
payload = {str(p.relative_to(OUT)): {'sha256': digest(p.read_bytes()), 'bytes': p.stat().st_size}
           for p in sorted(OUT.rglob('*')) if p.is_file() and p != OUT / 'SHA256-MANIFEST.json'}
write_json('SHA256-MANIFEST.json', payload)
assert all(digest((OUT / rel).read_bytes()) == pin['sha256'] for rel, pin in payload.items())
result = {
    'status': 'FIFTH_EXTERNAL_TRANSFER_READY_ROOT_PUBLICATION_PENDING',
    'path': str(OUT), 'payload_files': len(payload),
    'logical_payload_bytes': sum(x['bytes'] for x in payload.values()),
    'destination_only_hardlink_saved_bytes': sum(x['bytes'] for x in duplicates),
    'manifest_sha256': digest((OUT / 'SHA256-MANIFEST.json').read_bytes()),
    'all_original_settled_sources_rechecked': True, 'outer_manifest_verified': True,
    'omitted_raw_geometry_opened_or_rehashed': False,
    'live_app_read_or_copied': False, 'app_or_evidence_Git_mutations': 0,
    'extra_heavy_processes': 0, 'final_canonical_owner_gate': 'PENDING_AT_ASSEMBLY_REQUEST',
    'new_app_commit_or_PR': False,
}
(BASE / 'ROOT-TRANSPORT-EVIDENCE-FIFTH-20261024-TRANSFER-RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
