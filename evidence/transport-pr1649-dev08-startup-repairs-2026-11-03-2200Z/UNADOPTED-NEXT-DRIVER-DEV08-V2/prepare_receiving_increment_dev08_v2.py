"""Guarded adoption of the already qualified driver-look payloads; dry-run by default.

This does not generate, stage, commit, push, run owners, or claim a gate verdict.
ROOT may apply only after reviewing the new receiving HEAD and merging PR1649.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ADOPTION_SHA = 'dfed77bd219c8147fa17fd3e2a065b1c08dffe17293d4a32d25f4ff7629967ac'
PATCH_SHA = '6ccfbd60a146f7c548b8ab155cdfb0c28af0bd56f07aa2a07a2ebefe9a274e84'
REQUIRED_DEV = '08d3f3d7c85545013eaca18a9d256fe63a8e17e0'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def run(target, *args, check=True):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(target), *args],
                          check=check, capture_output=True, text=True, timeout=5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=pathlib.Path, required=True)
    parser.add_argument('--expected-head', required=True)
    parser.add_argument('--receipt', type=pathlib.Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    target = args.target.resolve()
    receipt = args.receipt.resolve()
    assert not receipt.is_relative_to(target), 'Receipt must stay outside application checkout'
    assert not receipt.exists(), 'Use a new receipt path'
    assert sha(HERE / 'DEV08-COMPATIBLE-NEXT-V2-PROFILE.json') == ADOPTION_SHA
    adoption = json.loads((HERE / 'DEV08-COMPATIBLE-NEXT-V2-PROFILE.json').read_text())
    preview = json.loads((HERE / adoption['text_patch_current_root_readonly_preview']).read_text())
    patch = HERE / adoption['text_patch']
    assert sha(patch) == PATCH_SHA
    assert sha(HERE / 'generated/DERIVATION.json') == adoption['generated_receipt_sha256']
    derivation = json.loads((HERE / 'generated/DERIVATION.json').read_text())
    head = run(target, 'rev-parse', 'HEAD').stdout.strip()
    assert head == args.expected_head, ('Receiving HEAD changed', head)
    dev_present = run(target, 'merge-base', '--is-ancestor', REQUIRED_DEV, 'HEAD', check=False).returncode == 0
    # Check all original text targets and all actual generated/active model bytes.
    for relative, expected in preview['target_file_pins'].items():
        assert sha(target / relative) == expected, ('Text target differs; review before adoption', relative)
    for row in derivation['files']:
        relative = pathlib.Path('chicago/4d') / row['file']
        assert sha(target / relative) == row['parent_sha256'], ('Recipe parent differs', str(relative))
        assert sha(HERE / 'generated' / row['file']) == row['sha256'], ('Generated child differs', row['file'])
    fixture = json.loads((HERE / 'FIXTURE-COMPATIBILITY-WITH-CURRENT-ROOT.json').read_text())
    for relative, reading in fixture['critical_sources'].items():
        assert sha(target / 'chicago/4d' / relative) == reading['qualified'], ('Fixture-critical reader changed', relative)
    supplement = (HERE / adoption['status_append']).read_bytes()
    status_path = target / 'chicago/4d/docs/STATUS.md'
    previous_status = status_path.read_bytes()
    assert supplement not in previous_status, 'Supplement already present'
    rows = json.loads((HERE / adoption['registry_rows']).read_text())
    registry_operations = []
    for section, filename in [('writer_inventory', 'writer_inventory.json'), ('step_isolation', 'step_isolation.json')]:
        path = target / 'chicago/4d/tools' / filename
        old = json.loads(path.read_text())
        row = rows[section]
        assert row['key'] not in old['tools'], ('Registry entry already present; review', row['key'])
        new = json.loads(json.dumps(old))
        new['tools'][row['key']] = row['entry']
        registry_operations.append((path, old, new))
    with tempfile.TemporaryDirectory(prefix='driver-receiving-preview-', dir=HERE) as temporary:
        snapshot = pathlib.Path(temporary)
        for relative in preview['paths']:
            source = target / relative
            if source.exists():
                output = snapshot / relative
                output.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, output)
        subprocess.run(['git', 'apply', '--check', str(patch)], cwd=snapshot,
                       check=True, capture_output=True, text=True, timeout=5)
    affected = preview['paths'] + ['chicago/4d/docs/STATUS.md'] + [str(p.relative_to(target)) for p, _, _ in registry_operations] + [str(pathlib.Path('chicago/4d') / r['file']) for r in derivation['files']]
    before = {relative: sha(target / relative) for relative in affected}
    result = {'status': 'READ_ONLY_ADOPTION_PREVIEW_PASS_NOT_APPLIED', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'head': head, 'required_dev': REQUIRED_DEV, 'required_dev_is_ancestor': dev_present,
              'patch_sha256': PATCH_SHA, 'eight_actual_parent_and_child_hashes_pass': True,
              'fixture_critical_sources_exact': True, 'before': before,
              'must_regenerate_on_receiving_base': adoption['receiving_owner_commands_original120_each'],
              'no_gate_world_photo_commit_push_or_dev_acceptance_claim': True}
    if args.apply:
        assert dev_present, 'Receiving HEAD must include reviewed DEV08; merge PR1649 first'
        assert not run(target, 'status', '--porcelain', '--untracked-files=no').stdout, 'Receiving tracked tree must be clean'
        assert run(target, 'rev-parse', 'HEAD').stdout.strip() == head
        subprocess.run(['git', 'apply', str(patch)], cwd=target, check=True, capture_output=True, text=True, timeout=5)
        status_path.write_bytes(previous_status + (b'\n' if previous_status.endswith(b'\n') else b'\n\n') + supplement)
        for path, old, new in registry_operations:
            path.write_text(json.dumps(new, indent=2) + '\n')
            reread = json.loads(path.read_text())
            for key, value in old.items():
                if key != 'tools': assert reread[key] == value
            for key, value in old['tools'].items(): assert reread['tools'][key] == value
        for row in derivation['files']:
            shutil.copyfile(HERE / 'generated' / row['file'], target / 'chicago/4d' / row['file'])
        assert status_path.read_bytes().startswith(previous_status)
        result['status'] = 'APPLIED_EXACT_PAYLOADS_OWNERS_AND_GATE_PENDING'
        result['after'] = {relative: sha(target / relative) for relative in affected}
    else:
        assert before == {relative: sha(target / relative) for relative in affected}, 'Target changed during read-only preview'
    receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ['status', 'head', 'required_dev_is_ancestor']}))


if __name__ == '__main__':
    main()
