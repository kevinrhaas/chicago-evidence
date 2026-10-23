#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Pinned b880 sidecar-only adapter; never opens a GLB for writing."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from surface_metadata import clean_surface_manifest, require

GLB_SHA256 = 'b880dce59fda746969b7fefe91d8ba0f5478208d73f821e7efa319bdb49ca8d4'
MANIFEST_SHA256 = '3a88ff16f3fd945cd9e7f27c88a5751793eff51af9626504166b6e6d8ea3afd6'

def coat_indices(raw):
    magic, version, length = struct.unpack_from('<III', raw)
    require((magic, version, length) == (0x46546c67, 2, len(raw)), 'Invalid GLB header')
    json_length, kind = struct.unpack_from('<II', raw, 12)
    require(kind == 0x4e4f534a, 'Missing JSON chunk')
    document = json.loads(raw[20:20 + json_length])
    binary_header = 20 + json_length
    binary_length, kind = struct.unpack_from('<II', raw, binary_header)
    require(kind == 0x004e4942 and binary_header + 8 + binary_length == len(raw), 'Invalid BIN chunk')
    meshes = [m for m in document['meshes'] if m.get('name') == 'skinned_equine_coat']
    require(len(meshes) == 1 and len(meshes[0]['primitives']) == 1, 'Ambiguous coat primitive')
    primitive = meshes[0]['primitives'][0]
    accessor = document['accessors'][primitive['indices']]
    view = document['bufferViews'][accessor['bufferView']]
    require(primitive.get('mode', 4) == 4 and accessor['type'] == 'SCALAR', 'Nontriangle coat')
    require(not accessor.get('sparse') and not view.get('byteStride') and view.get('buffer', 0) == 0, 'Unsupported index storage')
    require(accessor['componentType'] in (5123, 5125), 'Unsupported index type')
    code = {5123: 'H', 5125: 'I'}[accessor['componentType']]
    offset = view.get('byteOffset', 0) + accessor.get('byteOffset', 0)
    return list(struct.unpack_from('<' + code * accessor['count'], raw, binary_header + 8 + offset))

def clean(glb, manifest, output):
    glb, manifest, output = map(Path, (glb, manifest, output))
    require(output.resolve() not in {glb.resolve(), manifest.resolve()}, 'Output must be a new sidecar')
    raw, metadata = glb.read_bytes(), manifest.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == GLB_SHA256, 'Wrong protected horse GLB')
    require(hashlib.sha256(metadata).hexdigest() == MANIFEST_SHA256, 'Wrong authoritative source manifest')
    result = clean_surface_manifest(json.loads(metadata), coat_indices(raw))
    result['sidecar_cleanup_provenance'] = {
        'scope': 'Sidecar metadata only; GLB extras and all geometry/nodes/skins/animations untouched',
        'source_glb_sha256': GLB_SHA256,
        'source_manifest_sha256': MANIFEST_SHA256,
        'surface_tables': 'Pinned original producer manifest validated against actual current coat triangles',
    }
    require(glb.read_bytes() == raw and manifest.read_bytes() == metadata, 'Inputs changed during cleanup')
    with output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    require(glb.read_bytes() == raw and manifest.read_bytes() == metadata, 'Protected inputs changed')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('glb'); parser.add_argument('manifest'); parser.add_argument('output')
    args = parser.parse_args()
    clean(args.glb, args.manifest, args.output)
