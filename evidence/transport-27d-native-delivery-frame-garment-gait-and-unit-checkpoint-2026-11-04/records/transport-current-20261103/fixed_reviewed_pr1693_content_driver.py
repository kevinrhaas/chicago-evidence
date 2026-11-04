"""Apply only two explicitly owner-reviewed three-way resolutions; never guess."""
from pathlib import Path
import hashlib, json, subprocess, sys

PROOF = Path('/workspace/.cloud-setup/transport-driver1693-owner-content-resolution-20261104/RESOLUTION-PROOF.json')
PROOF_SHA = '46f557adad69e862a8b0f6ae0a19ceb65cf846379526f0a40e8f9a2a1fd160a4'
WORK = Path('/tmp/chicago-pr1693-official-refresh-20261104')
EXPECTED_HEAD = '27d52718290a2708f70ca536c6b796a83a936601'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def approved_bytes(base, ours, theirs, repo_path):
    assert sha(PROOF.read_bytes()) == PROOF_SHA, 'Reviewed proof changed'
    rows = [r for r in json.loads(PROOF.read_text())['files'] if r['repo_path'] == repo_path]
    assert len(rows) == 1, 'Unreviewed path'
    row = rows[0]
    for key, data in [('BASE', base), ('OURS', ours), ('THEIRS', theirs)]:
        assert sha(data) == row['preimages'][key]['sha256'], 'Unreviewed ' + key + ' input'
    resolved = Path(row['resolved_path']).read_bytes()
    assert sha(resolved) == row['resolved_sha256']
    start = row['insert_offset']
    count = row.get('authored_block_bytes', row.get('authored_row_bytes'))
    assert resolved[:start] + resolved[start + count:] == theirs, 'Upstream bytes not preserved'
    return resolved

def main():
    assert len(sys.argv) == 5
    base, ours, theirs = map(Path, sys.argv[1:4])
    path = sys.argv[4]
    head = subprocess.check_output(['git', '-C', str(WORK), 'rev-parse', 'HEAD'], timeout=10).decode().strip()
    assert head == EXPECTED_HEAD, 'Unreviewed feature HEAD'
    assert ours.resolve().is_relative_to(WORK), 'Merge output must be an owned checkout temporary file'
    result = approved_bytes(base.read_bytes(), ours.read_bytes(), theirs.read_bytes(), path)
    ours.write_bytes(result)
    assert sha(ours.read_bytes()) == sha(result)
    print('ROOT owner-reviewed fixed-input content resolution:', path)
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, subprocess.SubprocessError) as exc:
        print('REFUSED owner-reviewed resolution:', str(exc), file=sys.stderr)
        raise SystemExit(1)
