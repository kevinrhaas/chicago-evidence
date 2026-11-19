#!/usr/bin/env python3
"""Read the emitted GLB independently; check binary ranges and glTF mesh contracts."""
from pathlib import Path
import hashlib, json, math, struct
ROOT = Path(__file__).resolve().parent.parent
p = ROOT / 'assets/chamber_of_commerce_1865__original_1865.glb'
b = p.read_bytes()
magic, version, size = struct.unpack_from('<4sII', b)
assert (magic, version, size) == (b'glTF', 2, len(b))
n, tag = struct.unpack_from('<I4s', b, 12)
assert tag == b'JSON' and n % 4 == 0
j = json.loads(b[20:20+n]); offset = 20+n
bn, tag = struct.unpack_from('<I4s', b, offset)
assert tag == b'BIN\x00' and offset+8+bn == len(b)
data = b[offset+8:]
assert j['buffers'] == [{'byteLength': len(data)}]
for v in j['bufferViews']:
    assert v.get('buffer', 0) == 0
    assert v.get('byteOffset', 0) % 4 == 0
    assert 0 <= v.get('byteOffset', 0) <= len(data)-v['byteLength']

def read(index):
    a = j['accessors'][index]; v = j['bufferViews'][a['bufferView']]
    assert 'byteStride' not in v
    width = {'SCALAR':1, 'VEC2':2, 'VEC3':3}[a['type']]
    code = {5126:'f', 5125:'I'}[a['componentType']]
    count = a['count'] * width
    start = v.get('byteOffset', 0) + a.get('byteOffset', 0)
    assert count*4 <= v['byteLength']
    values = struct.unpack_from('<'+code*count, data, start)
    assert all(math.isfinite(x) for x in values)
    return [values[i:i+width] for i in range(0, count, width)]

triangles = 0
for primitive in j['meshes'][0]['primitives']:
    a = primitive['attributes']; pos = read(a['POSITION']); normals = read(a['NORMAL'])
    assert len(pos) == len(normals) == len(read(a['TEXCOORD_0'])) == len(read(a['_CONFIDENCE']))
    assert all(abs(math.sqrt(sum(v*v for v in n))-1) < 2e-6 for n in normals)
    indices = [v[0] for v in read(primitive['indices'])]
    assert len(indices)%3 == 0 and max(indices) < len(pos) and min(indices) >= 0
    triangles += len(indices)//3
    for index in range(0,len(indices),3):
        p0,p1,p2 = [pos[k] for k in indices[index:index+3]]
        u = [p1[k]-p0[k] for k in range(3)]; v = [p2[k]-p0[k] for k in range(3)]
        cross = [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        assert sum(x*x for x in cross) > 1e-15, 'Degenerate triangle'
        assert sum(x*y for x,y in zip(cross,normals[indices[index]])) > 0, 'Triangle winding disagrees with normal'
for im in j['images']:
    v = j['bufferViews'][im['bufferView']]; start = v.get('byteOffset',0)
    assert im['mimeType'] == 'image/png' and data[start:start+8] == b'\x89PNG\r\n\x1a\n'
    assert struct.unpack_from('>II',data,start+16) == (512,512)
result = {'status':'PASS','glb_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'triangles':triangles,'primitives':len(j['meshes'][0]['primitives']),'checks':['GLB2 container and every buffer range','Finite attribute values and matching vertex counts','Unit normals, valid indices and nondegenerate triangles','Every triangle winding agrees with its stored normal','Three self-contained 512px original PNG textures'],'limits':['Not a topology, visual or historical accuracy certification.','Visual and historical acceptance is separate; inspect the current camera match records.']}
assert len(j['images']) == 3
(ROOT/'review/geometry-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
