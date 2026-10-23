from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import subprocess

WORK = Path(__file__).resolve().parent
RUN = Path('/tmp/chicago-next-model/T-2372-door-recess-next/runs/20261023-224621-281228')
AUTHOR = RUN / 'ACTUAL-RECOVERY-SHA256.json'
EXPECTED = '0c9e969c6282219d9f2b39166512027d081e79e75579d2689e06b9b5ffd8ddc6'
sha = lambda b: hashlib.sha256(b).hexdigest()
assert sha(AUTHOR.read_bytes()) == EXPECTED
author = json.loads(AUTHOR.read_text())
assert author['status'] == 'CLOSED_ACTUAL_DIFFERS'
assert len(author['files']) == 314
entries = []
excluded = []
for row in author['files']:
    rel = Path(row['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    path = RUN / rel
    assert not path.is_symlink() and path.is_file()
    assert path.resolve().is_relative_to(RUN.resolve())
    data = path.read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], path
    assert path.read_bytes() == data, path
    if '__pycache__' in rel.parts or path.suffix == '.pyc':
        excluded.append({**row, 'reason': 'Generated Python bytecode cache; parent archival scope excludes caches.'})
    else:
        assert not any(part in ['node_modules', '.git'] for part in rel.parts)
        entries.append((path, row['path'], row['sha256']))
assert len(entries) == 279 and len(excluded) == 35
ledger = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'author_manifest': str(AUTHOR),
    'author_manifest_sha256': EXPECTED,
    'all_author_files_verified': 314,
    'selected_noncache_payloads': 279,
    'excluded_caches': excluded,
    'selection_agreed_by_author': 'resume_school agreed explicit35-cache exclusion; frozen original314 manifest remains untouched.',
    'limits': 'Actual one official export and one capture; door recess visibly improves model, final verdict still differs. This archive is prototype evidence, no canonical81-family adoption, no accepted image-match record.'
}
selection = WORK / 'SCHOOL-SELECTION.json'
selection.write_text(json.dumps(ledger, indent=2) + '\n')
entries.extend([(AUTHOR, AUTHOR.name, EXPECTED), (selection, selection.name, sha(selection.read_bytes()))])
spec = importlib.util.spec_from_file_location('archive_exact', WORK / 'archive_exact.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
receipt = mod.archive(
    'SCHOOL-one-ACTUAL-blind-door-DIFFERS', entries,
    'School T2372: one actual official export + one actual capture completed on resumed session. Masterde08343a; source/camera guarded, doorway improves but full image differs. All314 author-owned files verified;279 noncache payloads archived plus originalmanifest and explicit35cache exclusion ledger. No canonical adoption or acceptance.'
)
print('SCHOOL ARCHIVE CLOSED: full author314 verified, selected279+2metadata; full tar readback PASS.')
