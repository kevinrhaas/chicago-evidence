"""Resolve the explicit 2027 phase retirement, then use the registry's owner.

This integration-only adapter handles one case the standard resolver refuses:
our old phase changed only in its input hash, while dev retired that phase and
committed its replacement. No generated hash or new geometry is chosen here.
The owning K01 emitter computes the replacement hash and must preserve dev bytes.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path('/workspace/chicago')
APP = ROOT / 'chicago/4d'
UPSTREAM = 'd47d9550bf914d33860a56b99fd11ad2f6f6018b'
MANIFEST = 'chicago/4d/assets/manifest.json'
OLD = 'house_2027_prairie__draft_1904.glb'
NEW = 'house_2027_prairie__as_mapped_1904.glb'

def git(*a, raw=False):
    return subprocess.check_output(['git', *a], cwd=ROOT, text=not raw)

spec = importlib.util.spec_from_file_location('registry_owner', APP/'tools/merge_asset_registry.py')
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
sides = [json.loads(git('show', f':{stage}:{MANIFEST}')) for stage in (1, 2, 3)]
base, ours, theirs = sides
strip = lambda row: {k:v for k,v in row.items() if k != 'inputs_sha256'}
assert OLD in base['assets'] and OLD in ours['assets'] and OLD not in theirs['assets']
assert strip(base['assets'][OLD]) == strip(ours['assets'][OLD])
assert NEW not in base['assets'] and NEW not in ours['assets'] and NEW in theirs['assets']
assert theirs['assets'][NEW]['structure_id'] == 'house_2027_prairie'
assert theirs['assets'][NEW]['generator'] == 'generators/k01_emit.py'
structure = json.loads((APP/'data/structures/house_2027_prairie.json').read_text())
phase_ids = {p['id'] for p in structure['phases']}
assert 'draft_1904' not in phase_ids and 'as_mapped_1904' in phase_ids
assert git('show', f'{UPSTREAM}:chicago/4d/data/structures/house_2027_prairie.json') == (APP/'data/structures/house_2027_prairie.json').read_text()
for kind in ('gltf', 'web'):
    old_path = f'chicago/4d/assets/{kind}/{OLD}'
    new_path = f'chicago/4d/assets/{kind}/{NEW}'
    assert not (ROOT/old_path).exists()
    assert git('ls-files', '--stage', '--', old_path).strip() == ''
    assert git('rev-parse', f':{new_path}').strip() == git('rev-parse', f'{UPSTREAM}:{new_path}').strip()
    assert (ROOT/new_path).read_bytes() == git('show', f'{UPSTREAM}:{new_path}', raw=True)

# The only semantic conflict is retirement of the old phase. Its hash-only
# branch edit cannot keep a phase the combined authored structure no longer has.
# Normalize that superseded recipe metadata to its proven base, allowing the
# standard entry-by-entry merge to apply dev's explicit deletion. Keep original
# Git stages untouched so the decision remains fully reviewable.
original_ours_hash = ours['assets'][OLD]['inputs_sha256']
ours['assets'][OLD] = base['assets'][OLD]
reemit = {}
merged = owner.merge_texts(MANIFEST, *(owner.dumps(side, True) for side in sides), reemit=reemit)
assert not reemit
before = (ROOT/MANIFEST).read_bytes()
(ROOT/MANIFEST).write_text(merged)
try:
    result = subprocess.run([sys.executable, 'generators/k01_emit.py', '--only', 'house_2027_prairie'],
                            cwd=APP, capture_output=True, text=True, check=True)
    print(result.stdout, end='')
    emitted = (APP/'assets/gltf'/NEW).read_bytes()
    expected = git('show', f'{UPSTREAM}:chicago/4d/assets/gltf/{NEW}', raw=True)
    assert emitted == expected, 'K01 replacement differs from upstream bytes; fresh derivative required'
    after = json.loads((ROOT/MANIFEST).read_text())
    pre_emit = json.loads(merged)
    changed = [k for k in set(pre_emit['assets'])|set(after['assets']) if pre_emit['assets'].get(k) != after['assets'].get(k)]
    assert changed in ([], [NEW])
    assert strip(after['assets'][NEW]) == strip(theirs['assets'][NEW])
except Exception:
    (ROOT/MANIFEST).write_bytes(before)
    raise

receipt = {'resolution':'explicit retired phase plus supported merge_texts and owning K01 emitter',
           'retired_asset':OLD,'replacement_asset':NEW,
           'superseded_ours_input_hash':original_ours_hash,
           'old_phase_absent_from_merged_authored_structure':True,
           'old_master_and_web_deleted_by_upstream':True,
           'new_master_matches_upstream_bytes':True,
           'new_master_sha256':hashlib.sha256(emitted).hexdigest(),
           'new_input_sha256':after['assets'][NEW]['inputs_sha256'],
           'original_merge_index_stages_untouched':True,
           'unrelated_entries_merged_by_standard_registry_owner':True}
Path('/tmp/t3654-upstream-21f609-registry-retirement.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Registry resolved; K01 replacement is byte-identical to upstream and has its generated combined-tree input hash.')
