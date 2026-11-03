"""Build external next-increment overlay only; never edit the application."""
import copy
import difflib
import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path('/workspace/chicago-transport-current-20261103')
BASE = '5439723317fbb6491e837911243f2f62fb35065b'
PREFIX = 'DEV08-COMPATIBLE-NEXT-V2'


def sha(raw): return hashlib.sha256(raw).hexdigest()


def read(path): return path.read_bytes() if path.exists() else None


def main():
    original_manifest = HERE / 'ADOPTION-READY.json'
    assert sha(original_manifest.read_bytes()) == '26ba3918720a16dbab09ec84e01cc6fb41c1ddf480572087003731774aa6340d'
    adoption = json.loads(original_manifest.read_text())
    preview = json.loads((HERE / adoption['text_patch_current_root_readonly_preview']).read_text())
    original_patch = HERE / adoption['text_patch']
    assert sha(original_patch.read_bytes()) == adoption['text_patch_sha256']
    sources = {name: read(ROOT / name) for name in preview['paths']}
    test = 'chicago/4d/tools/test_driven_assembly.mjs'
    with tempfile.TemporaryDirectory(prefix='driver-dev08-overlay-build-', dir=HERE) as temporary:
        temporary = pathlib.Path(temporary)
        old, receiving = temporary / 'old', temporary / 'receiving'
        old.mkdir(); receiving.mkdir()
        old_sources = {}
        for name, expected in preview['target_file_pins'].items():
            if expected is not None:
                result = subprocess.run(['git', '--no-optional-locks', '-C', str(ROOT), 'show', BASE + ':' + name],
                                        capture_output=True, check=True, timeout=5)
                raw = result.stdout
                assert sha(raw) == expected, ('Original public parent changed', name)
                destination = old / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
                destination.chmod((ROOT / name).stat().st_mode & 0o777)
                old_sources[name] = raw
            else: old_sources[name] = None
            if sources[name] is not None:
                destination = receiving / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, destination)
        subprocess.run(['git', 'apply', str(original_patch)], cwd=old, check=True, capture_output=True, timeout=5)
        old_test = (old / test).read_bytes()
        assert old_test.startswith(old_sources[test]), 'Expected exact original EOF-only test addition'
        same_tests = old_test[len(old_sources[test]):]
        assert len(same_tests.splitlines()) == 60
        subprocess.run(['git', 'apply', '--exclude=' + test, str(original_patch)], cwd=receiving,
                       check=True, capture_output=True, timeout=5)
        (receiving / test).write_bytes(sources[test] + same_tests)
        outputs = {name: read(receiving / name) for name in preview['paths']}
        # Sixteen unmodified receiving parents give exactly the original outputs.
        changed_parents = [name for name in preview['paths'] if sources[name] != old_sources[name]]
        assert changed_parents == ['chicago/4d/renderers/web/js/town-transport.js', test]
        for name in preview['paths']:
            if name not in changed_parents:
                assert outputs[name] == (old / name).read_bytes(), ('Unexpected semantic output change', name)
        assert outputs[test].startswith(sources[test]), 'Retain every existing startup assertion byte'
        # A reversible original town patch proves the startup parent is retained.
        reverse = subprocess.run(['git', 'apply', '--reverse', '--include=chicago/4d/renderers/web/js/town-transport.js', str(original_patch)],
                                 cwd=receiving, check=True, capture_output=True, timeout=5)
        assert (receiving / 'chicago/4d/renderers/web/js/town-transport.js').read_bytes() == sources['chicago/4d/renderers/web/js/town-transport.js']
        patch_parts = []
        for name in preview['paths']:
            before, after = sources[name], outputs[name]
            assert after is not None
            patch_parts.append(f'diff --git a/{name} b/{name}\n')
            if before is None: patch_parts.append('new file mode 100644\n')
            patch_parts.extend(difflib.unified_diff((before or b'').decode().splitlines(keepends=True), after.decode().splitlines(keepends=True),
                              fromfile='/dev/null' if before is None else 'a/' + name, tofile='b/' + name, n=3))
        patch = ''.join(patch_parts).encode()
        new_patch = HERE / (PREFIX + '-18-PATH.patch')
        assert not new_patch.exists()
        new_patch.write_bytes(patch)
        # Fresh, untouched receiving snapshot verifies the complete new patch.
        fresh = temporary / 'fresh'; fresh.mkdir()
        for name in preview['paths']:
            if sources[name] is not None:
                destination = fresh / name; destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, destination)
        subprocess.run(['git', 'apply', '--check', str(new_patch)], cwd=fresh, check=True, capture_output=True, timeout=5)
        subprocess.run(['git', 'apply', str(new_patch)], cwd=fresh, check=True, capture_output=True, timeout=5)
        assert outputs == {name: read(fresh / name) for name in preview['paths']}
    assert sources == {name: read(ROOT / name) for name in preview['paths']}, 'Current ROOT changed during external preparation'
    new_preview = copy.deepcopy(preview)
    new_preview.update(status='READONLY_CURRENT_DEV08_STARTUP_SNAPSHOT_PATCH_PASS_NO_NEW_SOURCE_ACCEPTANCE',
                       patch_sha256=sha(patch), target_file_pins={name: sha(raw) if raw is not None else None for name, raw in sources.items()},
                       target_output_pins={name: sha(raw) for name, raw in outputs.items()},
                       source_context='HEAD543 with pending DEV08 merge and six-path startup/sparse fixes; not a commit or published/fixture reading',
                       original_two_parent_pin_changes=changed_parents,
                       same_60_driver_assertion_lines=True, all_existing_startup_assertion_bytes_retained=True,
                       town_startup_bytes_recover_exactly_by_reversing_original_driver_patch=True,
                       sixteen_other_outputs_byteidentical_to_original_qualified_overlay=True)
    preview_path = HERE / (PREFIX + '-PREVIEW.json')
    preview_path.write_text(json.dumps(new_preview, indent=2) + '\n')
    profile = copy.deepcopy(adoption)
    profile.update(status='OVERLAY_COMPATIBILITY_PREP_ONLY_ORIGINAL_QUALIFICATIONS_NOT_RETARGETED',
                   text_patch=new_patch.name, text_patch_sha256=sha(patch), text_patch_current_root_readonly_preview=preview_path.name,
                   original_adoption_manifest_sha256=sha(original_manifest.read_bytes()),
                   historical_qualifications_remain_at_original_source=True,
                   no_new_current_source_fixture_world_gate_commit_or_dev_claim=True)
    (HERE / (PREFIX + '-PROFILE.json')).write_text(json.dumps(profile, indent=2) + '\n')
    print(json.dumps({'patch_sha256': sha(patch), 'changed_parents': changed_parents, 'root_unchanged': True}))


if __name__ == '__main__': main()
