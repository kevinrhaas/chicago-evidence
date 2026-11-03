#!/usr/bin/env python3
"""Read pinned GitHub trees/blobs; never write the application checkout or Git DB."""
from pathlib import Path
import argparse, base64, hashlib, json, re, urllib.request

OUT = Path('/tmp/wolf-lap-route-20261103')
REPO = 'kevinrhaas/chicago'
OLD = '1855273d9d8d423db20ea072a95d8169bda7ae71'
OLD_TREE = 'c109504d5fc6ced7c4203c8f90b7adb3b95cc46a'
R = Path('/workspace/chicago-bridge-increment-20261102')
EXCEPTION_MESH = 'keith_house_1808_prairie__as_built_1886.glb'

def get(endpoint):
    request = urllib.request.Request('https://api.github.com/' + endpoint,
        headers={'Accept': 'application/vnd.github+json', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(request, timeout=40) as response:
        raw = response.read(20 * 1024 * 1024 + 1)
    assert len(raw) <= 20 * 1024 * 1024
    return json.loads(raw)

def tree(head):
    cache = OUT / (head + '.tree.json')
    if cache.exists():
        document = json.loads(cache.read_text())
    else:
        commit = get(f'repos/{REPO}/git/commits/{head}')
        assert commit['sha'] == head
        document = get(f'repos/{REPO}/git/trees/{commit["tree"]["sha"]}?recursive=1')
        assert not document.get('truncated'), 'A truncated tree cannot prove preservation'
        assert document['sha'] == commit['tree']['sha']
        cache.write_text(json.dumps(document, indent=2) + '\n')
    assert not document.get('truncated')
    if head == OLD:
        assert document['sha'] == OLD_TREE
    return {x['path']: x for x in document['tree'] if x['type'] == 'blob'}

def blob(oid):
    cache = OUT / 'blobs' / oid
    if cache.exists():
        body = cache.read_bytes()
    else:
        data = get(f'repos/{REPO}/git/blobs/{oid}')
        assert data['sha'] == oid and data['encoding'] == 'base64'
        assert data['size'] <= 12 * 1024 * 1024
        body = base64.b64decode(data['content'])
        assert len(body) == data['size']
        cache.parent.mkdir(exist_ok=True)
        cache.write_bytes(body)
    assert hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() == oid
    return body

def json_at(mapping, path):
    return json.loads(blob(mapping[path]['sha']))

def registry_check(before, after, path, key):
    a, b = json_at(before, path), json_at(after, path)
    assert {k:v for k,v in a.items() if k != key} == {k:v for k,v in b.items() if k != key}, path
    assert set(a[key]) == set(b[key]), path
    changed = []
    for name in a[key]:
        if a[key][name] == b[key][name]:
            continue
        changed.append(name)
        if name == EXCEPTION_MESH:
            continue
        x, y = a[key][name], b[key][name]
        if key == 'masters':
            raise AssertionError(f'Unexpected non-Keith MASTER hash change: {name}')
        assert isinstance(x, dict) and isinstance(y, dict), (path, name)
        assert {k:v for k,v in x.items() if k != 'inputs_sha256'} == {k:v for k,v in y.items() if k != 'inputs_sha256'}, (path, name)
    return {'path': path, 'changed_entries': changed,
            'non_Keith_changes_only_native_input_qualification': True}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--new-head', required=True)
    args = parser.parse_args()
    assert re.fullmatch('[0-9a-f]{40}', args.new_head)
    before, after = tree(OLD), tree(args.new_head)
    incoming = {x['path'] for x in json.loads((OUT / 'INCOMING-PATHS.json').read_text())}
    changed = sorted(p for p in set(before) | set(after)
                     if before.get(p, {}).get('sha') != after.get(p, {}).get('sha'))
    unexpected, protected = [], []
    for path in changed:
        if not path.startswith('chicago/4d/'):
            continue
        runtime = path.startswith(('chicago/4d/renderers/', 'chicago/4d/assets/', 'chicago/4d/data/'))
        if runtime and path not in incoming:
            # The version registry can carry native input-hash refreshes, verified below.
            if path != 'chicago/4d/assets/manifest.versions.json':
                unexpected.append(path)
        if path.startswith('chicago/4d/renderers/') and path != 'chicago/4d/renderers/web/js/changelog.js':
            protected.append(path)
        if path.startswith('chicago/4d/assets/') and not path.endswith(('manifest.json', 'manifest.web.json', 'manifest.versions.json')):
            if Path(path).name != EXCEPTION_MESH:
                protected.append(path)
        if path.startswith('chicago/4d/data/sidecars/1835/') and '/sources/' not in path:
            protected.append(path)
        if any('/' + name + '.' in path or '/' + name + '/' in path for name in
               ['wolf_point_tavern', 'sauganash_hotel', 'philo_carpenter_log_shop']):
            protected.append(path)
    payload = {'status': 'SOURCE_RUNTIME_PARITY_REFUSED' if unexpected or protected else 'SOURCE_RUNTIME_PARITY_PASS',
               'old_head': OLD, 'new_head': args.new_head, 'actual_changed_paths': changed,
               'unexpected_runtime_changes': unexpected, 'protected_runtime_changes': sorted(set(protected)),
               'browser_was_not_rerun_on_new_head': True,
               'whole_tree_native_smoke_hash_match_is_not_claimed': True}
    try:
        assert not unexpected and not protected, payload
        payload['registries'] = [registry_check(before, after, 'chicago/4d/assets/manifest.json', 'assets'),
                                 registry_check(before, after, 'chicago/4d/assets/manifest.web.json', 'masters')]
        versions = 'chicago/4d/assets/manifest.versions.json'
        if before[versions]['sha'] != after[versions]['sha']:
            payload['registries'].append(registry_check(before, after, versions, 'assets'))
        index = json_at(before, 'chicago/4d/data/sidecars/1835/index.json')
        ids = {x['id'] for x in index['structures']}
        old_lib, new_lib = (json_at(t, 'chicago/4d/data/liberties.json') for t in [before, after])
        # Same subjects predicate as the unchanged libertiesFor() browser function;
        # include subjectless standing entries as a stronger preservation condition.
        projection = lambda d: [x for x in d['liberties']
            if not x.get('subjects') or ids.intersection(x.get('subjects', []))]
        assert projection(old_lib) == projection(new_lib), 'An 1835 or standing liberty changed'
        for key in ['standard', 'note', 'source']:
            assert old_lib.get(key) == new_lib.get(key), 'Liberties metadata changed: ' + key
        names = lambda d: [x for x in d['names'] if x['id'] in ids]
        assert names(old_lib) == names(new_lib), 'An 1835 liberty subject name changed'
        payload['liberties_projection'] = {'scene_structures': len(ids), 'preserved_entries': len(projection(old_lib)),
            'all_1835_subjects_and_subjectless_standing_entries_exact': True}
        # These are the existing reviewed probe's 609 source/published bindings.
        # Check all tracked source members here. Published members require the
        # separate post-publish comparison; never assume a source match publishes.
        bindings = json.loads((OUT / 'BEFORE-CONTENT-BINDINGS.json').read_text())
        checked = 0
        for absolute, expected in bindings.items():
            if not Path(absolute).is_relative_to(R):
                assert hashlib.sha256(Path(absolute).read_bytes()).hexdigest() == expected['sha256'], absolute
                continue
            relative = Path(absolute).relative_to(R).as_posix()
            if relative.startswith('site/') or relative not in before:
                continue
            if relative == 'chicago/4d/renderers/web/js/changelog.js':
                continue
            assert before[relative]['sha'] == after[relative]['sha'], relative
            checked += 1
        payload['reviewed_probe_tracked_bindings_exact'] = checked
        payload['status'] = 'SOURCE_RUNTIME_PARITY_PASS_PUBLISHED_COMPARISON_STILL_REQUIRED'
    except AssertionError as exc:
        payload['status'] = 'SOURCE_RUNTIME_PARITY_REFUSED'
        payload['reason'] = str(exc)
        (OUT / (args.new_head + '.SOURCE-PARITY.json')).write_text(json.dumps(payload, indent=2) + '\n')
        raise
    (OUT / (args.new_head + '.SOURCE-PARITY.json')).write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps({k:v for k,v in payload.items() if k != 'actual_changed_paths'}, indent=2))

if __name__ == '__main__':
    main()
