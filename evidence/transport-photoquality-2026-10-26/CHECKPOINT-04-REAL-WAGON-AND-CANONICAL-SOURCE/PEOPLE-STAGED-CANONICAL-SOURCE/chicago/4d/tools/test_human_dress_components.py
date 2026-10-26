# SPDX-License-Identifier: GPL-3.0-or-later
"""Actual opt-in source-consumer and identity controls; never a Blender claim."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from human_dress_components import prepare_dress_assembly, BODY_SHA256
from human_teamster_blend import validate_input, resolve_person_reference
from human_base_prepare import prepare

ROOT = Path(__file__).resolve().parent.parent


class DressComponents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipe = json.loads((ROOT/'data/humans/recipes/adult_dress_1835.json').read_text())
        cls.variant = cls.recipe['proof_variants'][0]
        cls.bodypath = ROOT/cls.variant['body_input']
        cls.raw = cls.bodypath.read_bytes(); cls.body = json.loads(cls.raw)

    def test_actual_canonical_source_consumer_preserves_body(self):
        before = copy.deepcopy(self.body)
        bundle = prepare_dress_assembly(ROOT, self.recipe, self.variant, self.body)
        self.assertEqual(before, self.body)
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), BODY_SHA256)
        self.assertEqual(bundle['skeleton'], self.body['skeleton'])
        self.assertEqual([p['name'] for p in bundle['meshes']],
                         ['plain_closed_bodice', 'gathered_ankle_skirt', 'separate_plain_apron', 'closed_low_shoes'])
        self.assertGreater(bundle['meshes'][1]['receipt']['standing_body_core_clearance_m']-.0015, .015)
        for mesh in bundle['meshes']:
            for face in mesh['triangles']:
                self.assertEqual(len(set(face)), 3)
        self.assertFalse(bundle['meshes'][1]['receipt']['walking_or_seated_accepted'])

    def test_unqualified_pose_or_source_changes_are_refused(self):
        for key, bad, message in [('production_eligible', True, 'promotion'),
                                  ('walking_seated_or_photo_accepted', True, 'promotion'),
                                  ('body_sha256', '0'*64, 'body source')]:
            recipe = copy.deepcopy(self.recipe); recipe['dress_components'][key] = bad
            with self.assertRaisesRegex(ValueError, message):
                prepare_dress_assembly(ROOT, recipe, self.variant, self.body)
        variant = copy.deepcopy(self.variant); variant['person_reference_id'] = 'invented_new_person'
        with self.assertRaisesRegex(ValueError, 'existing reconstructed Mary Flynn'):
            prepare_dress_assembly(ROOT, self.recipe, variant, self.body)
        body = copy.deepcopy(self.body); body['meshes'][0]['positions_m'][0][0] += .001
        with self.assertRaisesRegex(ValueError, 'anatomy'):
            prepare_dress_assembly(ROOT, self.recipe, self.variant, body)

    def test_real_person_and_contract_source_bounds(self):
        contract = json.loads((ROOT/'data/humans/contract.json').read_text())
        bones = validate_input(self.body, contract)
        self.assertEqual(len(bones), 56)
        person = resolve_person_reference(self.variant, ROOT)
        self.assertEqual((person['name'], person['age_band'], person['presence']), ('Mary Flynn', '20-29', 'present'))
        # Original male resident recipes retain their unchanged identity path.
        male = json.loads((ROOT/'data/humans/recipes/worker_1835.json').read_text())
        for variant in male['proof_variants']:
            self.assertEqual(resolve_person_reference(variant, ROOT)['name'], variant['reference_summary']['name'])
        wrong = copy.deepcopy(self.variant); wrong['person_reference_grade'] = 'attested'
        with self.assertRaisesRegex(ValueError, 'grade differs'):
            resolve_person_reference(wrong, ROOT)
        wrong = copy.deepcopy(self.variant); wrong['person_reference_record'] = 'data/residents/households/hh_rc_unknown.json'
        with self.assertRaisesRegex(ValueError, 'explicit existing Mary Flynn'):
            resolve_person_reference(wrong, ROOT)

    def test_explicit_female_manifest_and_unsafe_selection(self):
        source = ROOT/'assets/authored/humans/makehuman_hm08'
        # The original SOURCE.json remains complete and byte-identical; the
        # female preparation explicitly opts into its separate complete manifest.
        manifest = json.loads((source/'SOURCE.json').read_text())
        self.assertFalse(any('female' in row['path'] for row in manifest['files']))
        female = prepare(source, 1.65, source/'adult_female_25.recipe.json', 'SOURCE-female.json')
        encoded = (json.dumps(female, separators=(',', ':'))+'\n').encode()
        self.assertEqual(encoded, self.raw)
        for unsafe in ['../SOURCE.json', '/tmp/SOURCE.json', '', 'SOURCE.txt']:
            with self.assertRaisesRegex(ValueError, 'local JSON filename'):
                prepare(source, 1.65, source/'adult_female_25.recipe.json', unsafe)


if __name__ == '__main__':
    unittest.main()
