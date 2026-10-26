#!/usr/bin/env python3
"""Restore only the nine verified archive-backed extracts reclaimed by this receipt."""
from pathlib import Path
import hashlib
import json
import os
import zipfile

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

receipt = json.loads(Path(__file__).with_name('ARCHIVE-BACKED-FEMALE-SOURCE-EXTRACTS.json').read_text())
archive = Path(receipt['zip'])
assert digest(archive) == receipt['zip_sha256']
root = Path('/tmp/T1789-CANONICAL-40376571147-INGEST-20261026/extracted')
with zipfile.ZipFile(archive) as zipped:
    for row in receipt['files']:
        target = Path(row['path'])
        relative = target.relative_to(root).as_posix()
        assert relative == row['zip_member'].lstrip('/')
        assert not target.is_symlink()
        if target.exists():
            assert target.stat().st_size == row['bytes'] and digest(target) == row['sha256']
            continue
        temporary = target.with_name(target.name + '.root-restore-tmp')
        assert not temporary.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with zipped.open(row['zip_member']) as source, temporary.open('xb') as output:
                for block in iter(lambda: source.read(1024 * 1024), b''):
                    output.write(block)
            assert temporary.stat().st_size == row['bytes'] and digest(temporary) == row['sha256']
            temporary.chmod(row['mode'])
            os.utime(temporary, ns=(row['mtime_ns'], row['mtime_ns']))
            os.replace(temporary, target)
        finally:
            if temporary.exists():
                temporary.unlink()
print('Restored/verified all nine original extracts; archive and PNGs unchanged.')
