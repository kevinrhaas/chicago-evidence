# SPDX-License-Identifier: GPL-3.0-or-later
"""Light actual-manifest coherence tests, no regeneration or asset writes."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from clean_sidecar import clean, coat_indices, GLB_SHA256, MANIFEST_SHA256
from surface_metadata import clean_surface_manifest

ROOT = Path('/workspace/shared/horse-forechest-smooth-next/trial-v2')
GLB = ROOT / 'equine_light_harness_skinned_prototype_01.glb'
MANIFEST = ROOT / 'manifest.json'

class SurfaceMetadata(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = GLB.read_bytes()
        cls.metadata = MANIFEST.read_bytes()
        cls.manifest = json.loads(cls.metadata)
        cls.indices = coat_indices(cls.raw)

    def rejected(self, change):
        candidate = copy.deepcopy(self.manifest)
        change(candidate['shoulder_join_trial'])
        with self.assertRaises((ValueError, KeyError, TypeError)):
            clean_surface_manifest(candidate, self.indices)

    def test_valid_actual_manifest_and_input_preservation(self):
        original = copy.deepcopy(self.manifest)
        indices = self.indices[:]
        result = clean_surface_manifest(self.manifest, self.indices)
        self.assertEqual(self.manifest, original)
        self.assertEqual(self.indices, indices)
        self.assertNotIn('vertex_ranges', result)
        self.assertEqual(result['surface_metadata_schema_version'], 2)
        counts = result['shoulder_join_trial']['construction_stage_counts']
        self.assertEqual(counts['pre_local_subdivision_added_bridge_triangles'], 308)
        self.assertEqual(counts['final_joined_bridge_triangles'], 1184)
        self.assertEqual(counts['final_whole_changed_triangles'], 1586)
        for record in original['shoulder_join_trial']['records']:
            self.assertEqual(len(result['active_surface_regions']['regions'][record['label'] + '_upper_joined']), 664)

    def test_missing_record(self):
        self.rejected(lambda s: s['records'].pop())

    def test_empty_records(self):
        self.rejected(lambda s: s.update(records=[]))

    def test_duplicate_labels(self):
        self.rejected(lambda s: s['records'][1].update(label='fore_l'))

    def test_empty_active_and_bridge_record(self):
        self.rejected(lambda s: s['records'][0].update(active_triangle_indices=[], new_triangle_indices=[]))

    def test_record_bridge_disagrees_global(self):
        self.rejected(lambda s: s['records'][0]['new_triangle_indices'].pop())

    def test_missing_nonbridge_active_face(self):
        def alter(s):
            r = s['records'][0]
            target = next(i for i in r['active_triangle_indices'] if i not in r['new_triangle_indices'])
            r['active_triangle_indices'].remove(target)
        self.rejected(alter)

    def test_wrong_active_face(self):
        def alter(s):
            r = s['records'][0]
            target = next(i for i in s['active_changed_body_triangle_indices'] if i not in r['active_triangle_indices'])
            r['active_triangle_indices'].append(target)
        self.rejected(alter)

    def test_wrong_active_vertex_table(self):
        self.rejected(lambda s: s['records'][0]['active_surface_vertex_indices'].pop())

    def test_global_changed_disagrees(self):
        self.rejected(lambda s: s['active_whole_changed_triangle_indices'].pop())

    def test_retired_cap_reference(self):
        indices = self.indices[:]
        indices[0] = self.manifest['shoulder_join_trial']['records'][0]['retired_unreferenced_vertices'][0]
        with self.assertRaises(ValueError):
            clean_surface_manifest(self.manifest, indices)

    def test_pinned_wrapper_new_sidecar_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'cleaned.json'
            clean(GLB, MANIFEST, output)
            self.assertTrue(output.exists())
            with self.assertRaises(FileExistsError):
                clean(GLB, MANIFEST, output)
            with self.assertRaises(ValueError):
                clean(GLB, MANIFEST, MANIFEST)
        self.assertEqual(GLB.read_bytes(), self.raw)
        self.assertEqual(MANIFEST.read_bytes(), self.metadata)
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), GLB_SHA256)
        self.assertEqual(hashlib.sha256(self.metadata).hexdigest(), MANIFEST_SHA256)

    def test_wrapper_rejects_changed_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            wrong = Path(temporary) / 'wrong.json'
            wrong.write_text(json.dumps(self.manifest) + '\n')
            with self.assertRaises(ValueError):
                clean(GLB, wrong, Path(temporary) / 'output.json')

if __name__ == '__main__':
    unittest.main()
