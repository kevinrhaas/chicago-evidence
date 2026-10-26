# SPDX-License-Identifier: GPL-3.0-or-later
"""V19 body refinement must preserve the accepted V18 physical specimen.

The baseline is the immutable accepted cb93 asset, not the new producer's idea
of its own output. Compare serialized occurrence P/N, optics, frames and actual
contacts before accepting fresh hashes. Appearance remains a separate review.
"""
import collections
import copy
import hashlib
import json

OWNED = {('deep_curved_lower_body', 'vehicle_body', 0),
         ('deep_curved_lower_body', 'vehicle_body', 1),
         ('cabin_front_lower', 'vehicle_body', 0),
         ('passenger_cushion', 'vehicle_body', 0),
         ('passenger_back', 'vehicle_body', 0)}
ADDED = {('driver_cushion_edge_piping', 'vehicle_body', 0)}


def part_rows(doc, binary):
    from check_mid import bind_parts
    occurrences = collections.Counter()
    result = {}
    for row in bind_parts(doc, binary):
        name, frame, material, triangles = row['identity']
        key = (name, frame, occurrences[(name, frame)])
        occurrences[(name, frame)] += 1
        result[key] = {'material': material, 'triangles': triangles,
                       **{kind: hashlib.sha256(row['chunks'][kind]).hexdigest()
                          for kind in ['POSITION', 'NORMAL']}}
    return result


def named_frames(doc):
    return [{**{k: v for k, v in node.items() if k != 'children'},
             'named_children': [doc['nodes'][i]['name'] for i in node.get('children', [])
                                if doc['nodes'][i]['name'].startswith('vehicle_')]}
            for node in doc['nodes'] if node['name'].startswith('vehicle_')]


def baseline_record(doc, binary, source_hash):
    from check_near import native_contacts, world_nodes, decoded_bounds
    from static_master import static_master_contract
    rows = part_rows(doc, binary)
    return {'source_sha256': source_hash,
            'parts': [{'key': list(k), **v} for k, v in rows.items()],
            'lamp_iron_glass_quarter_materials': doc['materials'][3:7],
            'named_frames': named_frames(doc),
            'contacts': native_contacts(doc, binary),
            'bounds_m': decoded_bounds(doc, binary, world_nodes(doc)),
            'static_master': static_master_contract(doc, binary, world_nodes(doc), source_hash)}


def check_preservation(doc, binary, baseline):
    from check_near import native_contacts, world_nodes, decoded_bounds
    from static_master import static_master_contract
    actual = part_rows(doc, binary)
    old = {tuple(row['key']): {k: v for k, v in row.items() if k != 'key'}
           for row in baseline['parts']}
    assert set(actual) - set(old) == ADDED and not set(old) - set(actual), 'Exact body-only added inventory'
    changed = {k for k in old if any(actual[k][kind] != old[k][kind] for kind in ['POSITION', 'NORMAL'])}
    assert changed == OWNED, 'Only the five reviewed body/pad occurrences may change geometry'
    for key, row in old.items():
        expected_material = 7 if key[0] in ['side_door_glass', 'front_glass'] else row['material']
        assert actual[key]['material'] == expected_material, 'Unexpected source component material reassignment'
        if key not in OWNED:
            assert actual[key]['triangles'] == row['triangles'], 'Protected source feature tessellation changed'
    assert doc['materials'][3:7] == baseline['lamp_iron_glass_quarter_materials'], 'Accepted lamp optics/iron/quarter changed'
    assert named_frames(doc) == baseline['named_frames'], 'Named frames/transforms/parent hierarchy changed'
    assert native_contacts(doc, binary) == baseline['contacts'], 'Wheel/pole/shoe/hitch contact geometry changed'
    world = world_nodes(doc)
    assert decoded_bounds(doc, binary, world) == baseline['bounds_m'], 'Original native outer envelope changed'
    measured = static_master_contract(doc, binary, world, baseline['source_sha256'])
    assert measured == baseline['static_master'], 'Door/seat references/targets/conservative proxy changed'
    return {'protected_occurrences': len(old) - len(OWNED),
            'changed_body_occurrences': len(OWNED), 'added_piping_occurrences': len(ADDED),
            'accepted_V18_lamps_exact': True, 'contacts_frames_proxy_exact': True}


def mutation_controls(doc, binary, baseline):
    """Exercise actual serialized protected geometry and shared optics in memory."""
    import struct
    from check_mid import bind_parts
    rows = bind_parts(doc, binary)
    protected = next(row for row in reversed(rows) if row['identity'][0] == 'solid_bright_hub_button')
    changed = bytearray(binary)
    offset = protected['offsets']['POSITION']
    struct.pack_into('<f', changed, offset, struct.unpack_from('<f', changed, offset)[0] + .001)
    variants = [('protected final hub geometry', doc, changed)]
    optics = copy.deepcopy(doc)
    optics['materials'][5]['pbrMetallicRoughness']['roughnessFactor'] += .001
    variants.append(('accepted lamp glazing', optics, binary))
    frames = copy.deepcopy(doc)
    next(n for n in frames['nodes'] if n['name'] == 'vehicle_hitch_team')['translation'][0] += .001
    variants.append(('named hitch frame', frames, binary))
    for name, candidate, payload in variants:
        try:
            check_preservation(candidate, payload, baseline)
        except AssertionError:
            continue
        raise AssertionError('Actual negative control escaped: ' + name)
    return {name: True for name, _, _ in variants}
