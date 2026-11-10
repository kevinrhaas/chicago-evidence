# SPDX-License-Identifier: GPL-3.0-or-later
"""One temporary lossless-index/optical derivation; no APP or capability writes."""
from pathlib import Path
import copy
import difflib
import hashlib
import json
import struct
import subprocess
import sys
import time
import traceback

PREP = Path(__file__).parent
CAP = 64 * 1024 * 1024
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def write(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def expanded_rows(doc, binary):
    """Independent per-primitive ordered PN hashes and actual moving ancestry."""
    parents = {c: i for i, n in enumerate(doc['nodes']) for c in n.get('children', [])}
    mesh_nodes = {}
    for i, node in enumerate(doc['nodes']):
        if 'mesh' in node:
            assert node['mesh'] not in mesh_nodes
            mesh_nodes[node['mesh']] = i
    assert len(mesh_nodes) == len(doc['meshes'])
    rows = []
    for mi, mesh in enumerate(doc['meshes']):
        node = mesh_nodes[mi]; ancestry = []; p = node
        while True:
            ancestry.append([p, doc['nodes'][p]['name']])
            if p not in parents:
                break
            p = parents[p]
        ancestry.reverse()
        for pi, primitive in enumerate(mesh['primitives']):
            assert set(primitive['attributes']) == {'POSITION', 'NORMAL'}
            assert primitive.get('mode', 4) == 4
            streams = []
            for key in ['POSITION', 'NORMAL']:
                a = doc['accessors'][primitive['attributes'][key]]
                v = doc['bufferViews'][a['bufferView']]
                assert a['componentType'] == 5126 and a['type'] == 'VEC3' and not a.get('sparse')
                assert v.get('byteStride', 12) == 12
                offset = v.get('byteOffset', 0) + a.get('byteOffset', 0)
                data = binary[offset:offset + 12 * a['count']]
                assert len(data) == 12 * a['count']
                streams.append((a['count'], data))
            assert streams[0][0] == streams[1][0]
            if 'indices' in primitive:
                a = doc['accessors'][primitive['indices']]
                v = doc['bufferViews'][a['bufferView']]
                assert a['type'] == 'SCALAR' and not a.get('sparse') and not v.get('byteStride')
                fmt = {5123: 'H', 5125: 'I'}[a['componentType']]
                offset = v.get('byteOffset', 0) + a.get('byteOffset', 0)
                indices = struct.unpack_from('<' + fmt * a['count'], binary, offset)
            else:
                indices = range(streams[0][0])
            assert len(indices) % 3 == 0
            digest = hashlib.sha256()
            for i in indices:
                assert 0 <= i < streams[0][0]
                digest.update(streams[0][1][12*i:12*i+12])
                digest.update(streams[1][1][12*i:12*i+12])
            rows.append({'mesh_index': mi, 'mesh_name': mesh['name'], 'primitive_index': pi,
                'material': primitive['material'], 'triangles': len(indices) // 3,
                'source_node_ancestry': ancestry,
                'moving': any(n == 'vehicle_door_right' for _, n in ancestry),
                'ordered_expanded_PN_sha256': digest.hexdigest()})
    return rows


def index_identity(raw, indexed, expected_triangles, expected_moving, read_glb):
    original, binary = read_glb(raw)
    doc, data = read_glb(indexed)
    expected = copy.deepcopy(original)
    for key in ['accessors', 'bufferViews', 'buffers']:
        expected[key] = doc[key]
    for a, b in zip(expected['meshes'], doc['meshes']):
        assert len(a['primitives']) == len(b['primitives'])
        for ap, bp in zip(a['primitives'], b['primitives']):
            assert 'indices' not in ap and 'indices' in bp
            ap['attributes'] = bp['attributes']
            ap['indices'] = bp['indices']
    assert expected == doc, 'Indexing changed nodes/materials/scenes/extras/primitive semantics'
    before, after = expanded_rows(original, binary), expanded_rows(doc, data)
    assert before == after, 'Per-mesh ordered source PN or moving/fixed ownership changed'
    assert sum(r['triangles'] for r in after) == expected_triangles
    assert sum(r['triangles'] for r in after if r['moving']) == expected_moving
    door, = [n for n in doc['nodes'] if n['name'] == 'vehicle_door_right']
    assert door['translation'] == [-0.655, 0, -0.43]
    assert doc['extras']['boarding_enabled'] is doc['extras']['door_interaction_enabled'] is False
    plan = doc['extras']['door_foundation']
    assert plan['boarding_enabled'] is plan['driver_passenger_fit'] is False
    assert not any(plan['qualification'].values())
    return {'entire_JSON_exact_except_index_stream_layout': True,
        'node_scene_pivot_and_all_materials_exact': True, 'ordered_primitive_PN_and_ancestry': after,
        'triangles': expected_triangles, 'moving_triangles': expected_moving}


def main():
    assert len(sys.argv) == 3, 'FRESH_OUTPUT BINDING_SHA required'
    output = Path(sys.argv[1]); binding_path = PREP / 'INPUT-BINDING.json'
    assert sha(binding_path) == sys.argv[2]
    binding = json.loads(binding_path.read_text())
    assert not output.exists(); output.mkdir()
    expected = binding['parents']
    def snapshot():
        actual = {p: sha(Path(p)) for p in expected}
        assert actual == expected, 'Reviewed inputs/source/validator changed'
        return actual
    before = snapshot(); write(output / 'PARENTS-BEFORE.json', before)
    started = time.monotonic(); rows = []; failure = None; complete = False
    def progress(stage):
        size = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
        assert size <= CAP, 'Owned output cap exceeded'
        write(output / 'PROGRESS.json', {'stage': stage, 'rows': rows,
            'elapsed_s': time.monotonic() - started, 'owned_output_bytes': size,
            'qualification': False, 'native_visuals_run': False})
    try:
        # Preserve the copied module's original four-level ROOT calculation;
        # only its pure read/compare/controls functions are called here.
        sys.path.insert(0, str(PREP / 'unchanged/tools/transport/brougham'))
        from index_streams import write_indexed, read_glb
        import optical_delivery
        indexed_dir = output / 'physical-indexed'; indexed_dir.mkdir()
        final_inputs = []
        for item in binding['inputs']:
            raw = Path(item['raw'])
            proof = json.loads(Path(item['proof']).read_text())
            closure = json.loads(Path(item['closure']).read_text())
            assert proof['PASS'] is True and proof['candidate_sha256'] == sha(raw) == item['raw_sha256']
            assert proof['checker_sha256'] == sha(Path(binding['checker']))
            assert proof['recipe_sha256'] == sha(Path(binding['recipe']))
            assert proof['source_receipt_sha256'] == sha(Path(item['source_receipt']))
            assert proof['intersection_tolerance_m'] == 1e-8 and proof['max_interval_depth'] == 12
            assert len(proof['sampled']) == 15 and all(r['triangle_contacts'] == 0 for r in proof['sampled'])
            counts = proof['interval_counts']
            assert counts['moving_triangles_completed'] == counts['moving_triangles_total'] == item['moving_triangles']
            assert counts['pairs_completed'] == counts['pairs_proven_clear'] == item['interval_pairs']
            assert counts['unresolved_or_intersecting_pairs'] == 0
            assert closure['result']['returncode'] == 0 and not closure['result']['timed_out']
            assert closure['resources']['accepted'] and closure['cleanup']['cleanup_complete']
            assert not closure['cleanup']['remaining_owned_children']
            indexed = indexed_dir / ('brougham-' + item['detail'] + '.glb')
            record = write_indexed(raw, indexed)
            identity = index_identity(raw, indexed, item['triangles'], item['moving_triangles'], read_glb)
            rows.append({**item, 'indexer_receipt': record, 'index_identity': identity,
                'indexed_file': str(indexed), 'indexed_sha256': sha(indexed),
                'indexed_bytes': indexed.stat().st_size, 'full_surface_proof_sha256': sha(Path(item['proof']))})
            final_inputs.append([item['detail'], sha(indexed), item['triangles']])
            progress('LOSSLESS_INDEX_' + item['detail'].upper())
        write(output / 'INDEX-IDENTITY.json', rows)

        stock = (PREP / 'generate_optical_delivery.stock.mjs').read_text()
        template = (PREP / 'generate_optical_delivery.template.mjs').read_text()
        final = template
        for detail, digest, triangles in final_inputs:
            token = '__' + detail.upper() + '_INDEXED_SHA256__'
            assert final.count(token) == 1
            final = final.replace(token, digest)
        # A literal two-record substitution is the entire producer adaptation.
        old = [('near', '3d2f3a802f4b32dba6a3e61f2c188dddce4db05cecfcbba81e1e8d369d5dfe89', 45338),
               ('mid', 'd5cdd34e981d29db41634ac780c22526742f6a20527b5866d2349c727a67400d', 23062)]
        exact = stock
        for (detail, old_sha, old_tri), (_, new_sha, new_tri) in zip(old, final_inputs):
            old_line = " ['%s','%s',%s]," % (detail, old_sha, old_tri)
            new_line = " ['%s','%s',%s]," % (detail, new_sha, new_tri)
            assert exact.count(old_line) == 1
            exact = exact.replace(old_line, new_line)
        assert final == exact, 'Optical producer changed beyond the two pinned input records'
        producer = output / 'generate_optical_delivery.articulated.mjs'; producer.write_text(final)
        (output / 'ACTUAL-PRODUCER-INPUT-PINS-ONLY.diff').write_text(''.join(difflib.unified_diff(
            stock.splitlines(True), final.splitlines(True), fromfile='stock', tofile='articulated')))
        producer_sha = sha(producer)
        for name in ['optical', 'optical-replay']:
            log = output / (name + '-producer.log')
            with log.open('w') as stream:
                subprocess.run(['node', str(producer), '--source-dir', str(indexed_dir),
                    '--output', str(output / name)], stdout=stream, stderr=subprocess.STDOUT, check=True)
        assert (output / 'optical/CANDIDATE.json').read_bytes() == (output / 'optical-replay/CANDIDATE.json').read_bytes()
        validation = []
        for row in rows:
            detail = row['detail']; filename = 'brougham-' + detail + '-delivery-v1.glb'
            indexed = Path(row['indexed_file']); delivery = output / 'optical' / filename
            assert delivery.read_bytes() == (output / 'optical-replay' / filename).read_bytes()
            original, source_bin, source_sha = optical_delivery.read(indexed)
            doc, binary, delivery_sha = optical_delivery.read(delivery)
            optical_delivery.compare(original, source_bin, doc, binary, source_sha, producer_sha)
            negatives = optical_delivery.controls(original, source_bin, doc, binary, source_sha, producer_sha)
            assert len(negatives) == 9
            row.update(optical_file=str(delivery), optical_sha256=delivery_sha,
                optical_bytes=delivery.stat().st_size, optical_binary_chunk_sha256=hashlib.sha256(binary).hexdigest(),
                entire_optical_BIN_and_geometry_layout_identity=True, independent_negative_controls=negatives,
                deterministic_optical_regeneration_byte_exact=True)
            for file in [indexed, delivery]:
                validation.append({'path': str(file), 'sha256': sha(file)})
        progress('INDEPENDENT_OPTICAL_IDENTITY_AND_ALL18_NEGATIVE_CONTROLS')
        write(output / 'VALIDATOR-INPUTS.json', validation)
        with (output / 'validator.log').open('w') as stream:
            subprocess.run(['node', str(PREP / 'validate_outputs.cjs'), str(output / 'VALIDATOR-INPUTS.json'),
                str(output / 'KHRONOS-REPORTS.json')], stdout=stream, stderr=subprocess.STDOUT, check=True)
        progress('OFFICIAL_KHRONOS_ALL_FOUR_OUTPUTS')
        complete = True
    except BaseException:
        failure = traceback.format_exc()
        raise
    finally:
        after = snapshot(); write(output / 'PARENTS-AFTER.json', after)
        record = {'schema': 'chicago-t2797-temporary-articulated-optical-candidate-v1',
            'state': 'TEMPORARY_OPTICAL_IDENTITY_CONFORMANCE_PASS' if complete else 'NONPASS',
            'input_binding_sha256': sys.argv[2], 'rows': rows,
            'elapsed_s': time.monotonic() - started, 'failure': failure,
            'immutable_parents_unchanged': before == after, 'geometry_proof_domain_unchanged': complete,
            'native_GLTFLoader_run': False, 'closed_visual_review': 'UNRUN',
            'photographic_accepted': False, 'world_budget_accepted': False,
            'all_qualification_flags_remain_false': True, 'boarding_enabled': False,
            'driver_passenger_fit': False, 'APP_mutation': False, 'adoption': False}
        write(output / 'OPTICAL-CANDIDATE.json', record)
        assert sum(p.stat().st_size for p in output.rglob('*') if p.is_file()) <= CAP
        print(json.dumps({'state': record['state'], 'elapsed_s': record['elapsed_s'],
            'qualification': False, 'rows': len(rows)}), flush=True)


if __name__ == '__main__':
    main()
