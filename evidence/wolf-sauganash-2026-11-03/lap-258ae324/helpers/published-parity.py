#!/usr/bin/env python3
"""Compare the actual new published 1835 inputs to the recorded 1855 publication."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, re

P = Path('/tmp/wolf-lap-route-20261103')
spec = importlib.util.spec_from_file_location('source_parity', P / 'strict-source-parity.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--site', required=True)
    ap.add_argument('--new-head', required=True)
    args = ap.parse_args()
    site = Path(args.site)
    old = json.loads((P / 'BEFORE-PUBLISHED-MEMBERS.json').read_text())
    current = {x.relative_to(site).as_posix(): {'bytes': x.stat().st_size, 'sha256': sha(x.read_bytes())}
               for x in site.rglob('*') if x.is_file()}
    changed = sorted(x for x in set(old) | set(current) if old.get(x) != current.get(x))
    allowed, protected, manifests = [], [], []
    global_known = {'data/liberties.json', 'data/sidecars/1835/sources/index.json',
                    'data/sidecars/1835/sources/habs_glessner_house_il_1015_drawings.json'}
    changelog = {'js/changelog.js', 'walk/js/changelog.js'}
    for name in changed:
        is_1904 = '/1904/' in name or name.endswith('/1904.json') or name.startswith('1904/')
        if name == 'data/reader/structures_1904.json':
            assert json.loads((site / name).read_text())['family'] == 'structures_1904'
            allowed.append(name)
            continue
        if name == 'data/prebuilt/index.json':
            body = (site / name).read_bytes()
            assert json.loads(body)['build'] == args.new_head[:10]
            reverse, count = re.subn(rb'("build"\s*:\s*")[0-9a-f]+(")',
                rb'\g<1>1855273d9d\2', body)
            assert count == 1 and sha(reverse) == old[name]['sha256'], 'Global prebuilt index changed beyond build'
            manifests.append(name)
            continue
        if name in changelog or name in {'walk/index.html', 'build.json'} or name.startswith('offline/'):
            allowed.append(name)
            continue
        if name in global_known or is_1904 or Path(name).name == native.EXCEPTION_MESH:
            allowed.append(name)
            continue
        if name.startswith('data/prebuilt/1835/') and name.endswith('.json'):
            before = (P / 'verified-old-published-bodies' / name).read_bytes()
            after = (site / name).read_bytes()
            assert sha(before) == old[name]['sha256']
            pattern = rb'("build"\s*:\s*")[0-9a-f]+(")'
            x, count_a = re.subn(pattern, rb'\1<build>\2', before)
            y, count_b = re.subn(pattern, rb'\1<build>\2', after)
            assert count_a == count_b == 1 and x == y, 'Prebuilt input changed beyond build: ' + name
            assert json.loads(after)['build'] == args.new_head[:10]
            manifests.append(name)
            continue
        if name.startswith(('data/', 'walk/js/', 'walk/css/', 'vendor/')):
            protected.append(name)
    result = {'status': 'PUBLISHED_1835_SCOPED_PARITY_REFUSED' if protected else 'PUBLISHED_1835_SCOPED_PARITY_PASS',
              'old_head': native.OLD, 'new_head': args.new_head,
              'protected_payload_differences': protected,
              'prebuilt_manifests_exact_except_build': manifests,
              'known_1904_global_or_build_differences': allowed,
              'browser_was_not_rerun_on_new_head': True,
              'new_head_required_CI_is_still_required': True,
              'whole_tree_or_all_15_smoke_parts_not_claimed': True}
    if protected:
        (P / (args.new_head + '.PUBLISHED-PARITY-REFUSED.json')).write_text(json.dumps(result, indent=2) + '\n')
    assert not protected, result
    old_tree = native.tree(native.OLD)
    old_lib = native.json_at(old_tree, 'chicago/4d/data/liberties.json')
    new_lib = json.loads((site / 'data/liberties.json').read_text())
    ids = {x['id'] for x in native.json_at(old_tree, 'chicago/4d/data/sidecars/1835/index.json')['structures']}
    projection = lambda d: [x for x in d['liberties']
        if not x.get('subjects') or ids.intersection(x.get('subjects', []))]
    assert projection(old_lib) == projection(new_lib), 'Published 1835/standing liberties differ'
    for key in ['standard', 'note', 'source']:
        assert old_lib.get(key) == new_lib.get(key), key
    old_index = native.json_at(old_tree, 'chicago/4d/data/sidecars/1835/sources/index.json')
    new_index = json.loads((site / 'data/sidecars/1835/sources/index.json').read_text())
    assert {k:v for k,v in old_index.items() if k != 'sources'} == {k:v for k,v in new_index.items() if k != 'sources'}
    a = {x['source_id']:x for x in old_index['sources']}
    b = {x['source_id']:x for x in new_index['sources']}
    assert set(a) == set(b)
    changed_sources = [key for key in a if a[key] != b[key]]
    assert set(changed_sources) <= {'habs_glessner_house_il_1015_drawings'}, changed_sources
    for key in changed_sources:
        assert a[key]['use'] != 'scene' and b[key]['use'] != 'scene', key
    result['liberties_1835_projection_exact_entries'] = len(projection(old_lib))
    result['global_source_catalog_only_non_1835_row_changed'] = changed_sources
    result['old_member_count'] = len(old)
    result['new_member_count'] = len(current)
    result['actual_changed_member_count'] = len(changed)
    result['source_template_and_publisher_must_be_verified_exact_separately'] = ['walk/index.html']
    (P / (args.new_head + '.PUBLISHED-PARITY.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
