#!/usr/bin/env python3
"""Read-only retained native audit. Usage: audit-retained.py RETAINED_SHA [--run-id ID].
Reads immutable Git blobs, never checks out files, and writes receipts only beside this
script (or --output-dir). A failed assertion is retained as FAIL, never an acceptance.
"""
from pathlib import Path
from collections import Counter
import argparse, datetime, hashlib, io, json, math, os, re, struct, subprocess, sys, traceback, zipfile

HERE = Path(__file__).resolve().parent
EXPECTED_PARENT = '5484f145fb02e51a4f43a773c4bf818ab9e46b8f'
EXPECTED_BIND_SHA = '3bc301b045728d24365ad72a124502c85b7b0029ed1bcc22a4e6220c1ee64ee2'
PREFIX = 'chicago/4d/'
CT = {5120: ('b', 1), 5121: ('B', 1), 5122: ('h', 2), 5123: ('H', 2), 5125: ('I', 4), 5126: ('f', 4)}
WIDTH = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT2': 4, 'MAT3': 9, 'MAT4': 16}
def sha(x): return hashlib.sha256(x).hexdigest()
def canon(x): return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()
def require(ok, message):
    if not ok: raise AssertionError(message)
def diff(a, b, path=''):
    if type(a) != type(b): return [{'path': path, 'before': a, 'after': b}]
    if isinstance(a, dict):
        rows = []
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b: rows.append({'path': path+'/'+key, 'before': a.get(key), 'after': b.get(key)})
            else: rows.extend(diff(a[key], b[key], path+'/'+key))
        return rows
    if isinstance(a, list):
        if len(a) != len(b): return [{'path': path+'/length', 'before': len(a), 'after': len(b)}]
        return [r for i, (x, y) in enumerate(zip(a, b)) for r in diff(x, y, path+'/'+str(i))]
    return [] if a == b else [{'path': path, 'before': a, 'after': b}]

def parse(raw):
    require(len(raw) >= 12 and struct.unpack_from('<4sII', raw) == (b'glTF', 2, len(raw)), 'invalid GLB header')
    off = 12; chunks = []
    while off < len(raw):
        require(off+8 <= len(raw), 'truncated GLB chunk header')
        size, kind = struct.unpack_from('<II', raw, off)
        require(off+8+size <= len(raw), 'truncated GLB chunk')
        chunks.append((kind, raw[off+8:off+8+size])); off += 8+size
    require(off == len(raw), 'GLB final offset')
    doc = json.loads(next(b for k, b in chunks if k == 0x4e4f534a))
    binary = next(b for k, b in chunks if k == 0x004e4942)
    def access(index):
        a = doc['accessors'][index]
        require(not a.get('sparse'), 'unsupported sparse accessor')
        v = doc['bufferViews'][a['bufferView']]
        require(v.get('buffer', 0) == 0, 'non-local GLB buffer')
        code, size = CT[a['componentType']]; width = WIDTH[a['type']]
        stride = v.get('byteStride', size*width); start = v.get('byteOffset', 0)+a.get('byteOffset', 0)
        spans = [(start+i*stride, start+i*stride+size*width) for i in range(a['count'])]
        require(all(0 <= x <= z <= len(binary) for x, z in spans), 'accessor span outside GLB buffer')
        data = b''.join(binary[x:z] for x, z in spans)
        values = [struct.unpack_from('<'+code*width, binary, x) for x, _ in spans]
        require(all(math.isfinite(v) for row in values for v in row), 'nonfinite accessor value')
        return data, values, spans
    return doc, binary, access

def compare_control(key, oldraw, newraw, webraw):
    od, ob, oa = parse(oldraw); nd, nb, na = parse(newraw)
    require(len(ob) == len(nb), key+' control binary size drift')
    require(len(od['meshes']) == len(nd['meshes']), key+' control mesh count drift')
    uv_ranges = []; uv_accessors = set(); uv_changed = 0; comparisons = []
    for mi, (om, nm) in enumerate(zip(od['meshes'], nd['meshes'])):
        require(len(om['primitives']) == len(nm['primitives']), key+' control primitive count drift')
        for pi, (op, np) in enumerate(zip(om['primitives'], nm['primitives'])):
            require(op == np, key+' control primitive topology/material binding drift')
            roles = list(op['attributes'].items()) + ([('INDICES', op['indices'])] if 'indices' in op else [])
            details = []
            for role, ai in roles:
                olddata, oldvals, oldspans = oa(ai); newdata, newvals, newspans = na(ai)
                require(oldspans == newspans, key+' control accessor spans drift')
                changed = sum(x != y for x, y in zip(oldvals, newvals))
                maximum = max((abs(x-y) for a, b in zip(oldvals, newvals) for x, y in zip(a, b)), default=0)
                if role.startswith('TEXCOORD_'):
                    uv_ranges.extend(oldspans); uv_accessors.add(ai); uv_changed += changed
                else: require(olddata == newdata, key+' control non-UV accessor drift: '+role)
                details.append({'role': role, 'accessor': ai, 'count': len(oldvals), 'raw_bytes_identical': olddata == newdata, 'decoded_changed_rows': changed, 'max_absolute_component_delta': maximum, 'before_raw_sha256': sha(olddata), 'after_raw_sha256': sha(newdata)})
            comparisons.append({'mesh': mi, 'primitive': pi, 'material': od.get('materials', [])[op['material']].get('name') if 'material' in op else None, 'attributes': details})
    mask = bytearray(len(ob))
    for x, z in uv_ranges: mask[x:z] = b'\x01'*(z-x)
    changed_offsets = [i for i, (x, y) in enumerate(zip(ob, nb)) if x != y]
    outside = [i for i in changed_offsets if not mask[i]]
    require(not outside, key+' control binary drift outside UV accessors')
    changes = diff(od, nd)
    require(all(re.fullmatch(r'/accessors/(\d+)/(min|max)/\d+', x['path']) and int(x['path'].split('/')[2]) in uv_accessors for x in changes), key+' control non-UV GLB JSON drift')
    require(od.get('materials') == nd.get('materials') and od.get('nodes') == nd.get('nodes') and od['meshes'] == nd['meshes'], key+' control materials/nodes/meshes drift')
    uv_exception = oldraw != newraw
    if uv_exception:
        require(bool(changed_offsets) and uv_changed > 0, key+' differing MASTER without measurable UV-only explanation')
        require(not od.get('textures') and not nd.get('textures') and not od.get('images') and not nd.get('images'), key+' UV exception on textured MASTER')
        wd, _, _ = parse(webraw)
        require(not wd.get('textures') and not wd.get('images'), key+' UV exception on textured WEB')
        require(not any(role.startswith('TEXCOORD_') for m in wd['meshes'] for p in m['primitives'] for role in p['attributes']), key+' UV exception while WEB consumes texture coordinates')
    return {'asset_key': key, 'master_bytes_identical': oldraw == newraw, 'unused_uv_only_exception': uv_exception, 'all_non_uv_attributes_raw_exact': True, 'materials_nodes_topology_exact': True, 'web_strict_byte_identity': True, 'json_differences': changes, 'changed_binary_bytes': len(changed_offsets), 'changed_binary_bytes_outside_uv': 0, 'changed_uv_accessor_rows': uv_changed, 'primitive_attribute_comparison': comparisons}

def geometry_summary(raw):
    doc, _, access = parse(raw); points = []; semantic = Counter(); position_multiset = Counter(); semantic_triangles = Counter(); primitive_rows = []; triangles = 0; vertices = 0; indices_total = 0
    for mi, mesh in enumerate(doc['meshes']):
        for pi, primitive in enumerate(mesh['primitives']):
            attrs = {role: access(ai)[1] for role, ai in primitive['attributes'].items() if not role.startswith('TEXCOORD_')}
            pos = attrs['POSITION']; count = len(pos); points.extend(pos); vertices += count
            require(all(len(v) == count for v in attrs.values()), 'target vertex attribute cardinality mismatch')
            indices = access(primitive['indices'])[1] if 'indices' in primitive else [(i,) for i in range(count)]
            mode = primitive.get('mode', 4); require(mode == 4 and len(indices)%3 == 0, 'unexpected target primitive mode/count')
            triangles += len(indices)//3; indices_total += len(indices)
            mat = doc.get('materials', [])[primitive['material']] if 'material' in primitive else None
            mat_sha = sha(canon(mat)); roles = sorted(attrs)
            vertex_semantics = [(mat_sha, tuple((role, tuple(attrs[role][i])) for role in roles)) for i in range(count)]
            for i, p in enumerate(pos):
                semantic[vertex_semantics[i]] += 1
                position_multiset[tuple(p)] += 1
            for offset in range(0, len(indices), 3):
                ids = [int(indices[offset+j][0]) for j in range(3)]
                require(all(0 <= i < count for i in ids), 'target index outside vertex range')
                tri = tuple(vertex_semantics[i] for i in ids)
                # Cyclic rotations preserve face orientation; export vertex splitting does not matter.
                semantic_triangles[min(tri, tri[1:]+tri[:1], tri[2:]+tri[:2])] += 1
            primitive_rows.append({'mesh': mi, 'primitive': pi, 'material': mat.get('name') if mat else None, 'material_canonical_sha256': mat_sha, 'vertices': count, 'indices': len(indices), 'triangles': len(indices)//3, 'attribute_roles': roles, 'non_uv_attribute_raw_sha256': {role: sha(access(primitive['attributes'][role])[0]) for role in roles}, 'indices_raw_sha256': sha(access(primitive['indices'])[0]) if 'indices' in primitive else None})
    bounds = {'min': [min(p[i] for p in points) for i in range(3)], 'max': [max(p[i] for p in points) for i in range(3)]}
    result = {'bytes': len(raw), 'sha256': sha(raw), 'vertices_including_export_splits': vertices, 'indices': indices_total, 'triangles': triangles, 'meshes': len(doc['meshes']), 'primitives': len(primitive_rows), 'materials': len(doc.get('materials', [])), 'local_mesh_union_bounds': bounds, 'primitive_details': primitive_rows}
    return result, semantic, position_multiset, semantic_triangles, doc

def compare_target(key, oldraw, newraw):
    old, os, op, ot, od = geometry_summary(oldraw); new, ns, np, nt, nd = geometry_summary(newraw)
    require(os != ns, key+' intended target has no non-UV semantic vertex change')
    require(old['local_mesh_union_bounds'] == new['local_mesh_union_bounds'], key+' unexpected target bounds change')
    require(od.get('nodes') == nd.get('nodes'), key+' unexpected target node transform change')
    require(od.get('materials') == nd.get('materials'), key+' unexpected target material definitions change')
    target_expectations = {}
    if key.startswith('green_tree_tavern__'):
        for field in ['vertices_including_export_splits', 'indices', 'triangles', 'meshes', 'primitives', 'materials']:
            require(old[field] == new[field], key+' unexpected target cost/topology-count change: '+field)
        # The exporter uses export_yup=True: glTF Y is height, X/Z are horizontal.
        # Require the actual scene transform before interpreting local axes as world axes.
        require(od.get('scene', 0) == 0 and od.get('scenes') == [{'name': 'Scene', 'nodes': [0]}], key+' unexpected scene transform root')
        require(len(od['nodes']) == 1 and od['nodes'][0].get('mesh') == 0 and not any(k in od['nodes'][0] for k in ['matrix','translation','rotation','scale','children']), key+' nonidentity world node transform')
        old_xz = Counter(); new_xz = Counter()
        for xyz, n in op.items(): old_xz[(xyz[0],xyz[2])] += n
        for xyz, n in np.items(): new_xz[(xyz[0],xyz[2])] += n
        require(old_xz == new_xz, key+' unexpected glTF X/Z ground-plane position multiset drift')
        expected_path=HERE/'GREEN-TREE-EXPECTED-VERTICAL-DELTA.json'; expected_raw=expected_path.read_bytes()
        require(sha(expected_raw) == '89e1c0f0a3582cef4bc02d22ab1d171ffd5ad6cff13d1775f591995e0962fc6a', key+' frozen pre-export delta receipt changed')
        expected=json.loads(expected_raw)
        expected_rows=Counter((r['material'],tuple(r['expected_gltf_before']),tuple(r['expected_gltf_after'])) for r in expected['changed_vertex_rows'])
        actual_rows=Counter(); actual_changes=[]; attribute_changes=[]
        _, _, oa=parse(oldraw); _, _, na=parse(newraw)
        for mi,(om,nm) in enumerate(zip(od['meshes'],nd['meshes'])):
            require(len(om['primitives'])==len(nm['primitives']),key+' unexpected primitive count')
            for pi,(a,b) in enumerate(zip(om['primitives'],nm['primitives'])):
                require(a==b,key+' unexpected primitive topology/material binding change')
                material=od['materials'][a['material']]['name']
                require(oa(a['indices'])[0]==na(b['indices'])[0],key+' unexpected index topology change')
                av=oa(a['attributes']['POSITION'])[1];bv=na(b['attributes']['POSITION'])[1]
                require(len(av)==len(bv),key+' vertex count drift')
                for i,(x,y) in enumerate(zip(av,bv)):
                    require(x[0]==y[0] and x[2]==y[2],key+' changed horizontal coordinate')
                    if x!=y:
                        actual_rows[(material,tuple(x),tuple(y))]+=1
                        actual_changes.append({'mesh':mi,'primitive':pi,'material':material,'position_accessor':a['attributes']['POSITION'],'row':i,'before_gltf_world':x,'after_gltf_world':y,'delta_gltf_world':[y[k]-x[k] for k in range(3)]})
                for role,ai in a['attributes'].items():
                    ad,avs,_=oa(ai);bd,bvs,_=na(b['attributes'][role])
                    if role not in ['POSITION','NORMAL'] and not role.startswith('TEXCOORD_'):
                        require(ad==bd,key+' unexpected nongeometric vertex attribute drift '+role)
                    attribute_changes.append({'mesh':mi,'primitive':pi,'role':role,'raw_exact':ad==bd,'changed_rows':sum(x!=y for x,y in zip(avs,bvs))})
        require(actual_rows==expected_rows and len(actual_changes)==8,key+' native changed positions do not exactly match frozen pre-export eight vertical-only positions')
        target_expectations={'cost_counts_unchanged':True,'gltf_y_up_export':True,'identity_scene_world_transform':True,'world_horizontal_axes':['X','Z'],'world_vertical_axis':'Y','xz_position_multiset_exact':True,'every_position_row_horizontal_coordinates_exact':True,'changed_position_rows':8,'all_eight_positions_exact_float32_mapping_of_frozen_pre_export_receipt':True,'expected_delta_receipt_sha256':sha(expected_raw),'actual_vertical_position_changes':actual_changes,'all_primitive_topology_and_confidence_exact':True,'attribute_change_counts':attribute_changes,'roof_overhang_explanation':expected['overhang_explanation'],'interpretation':'Only the existing shoulder roof/infill vertical coordinates move; 0.6m roof-high control propagates through the unchanged shed overhang interpolation. No horizontal, node, material, topology, confidence or cost change.'}
    elif key.startswith('cobweb_castle__'):
        require(new['triangles']-old['triangles'] == 1002, key+' expected 501 added clapboard quads / 1002 triangles')
        require(not (ot-nt), key+' old triangle geometry/material/normal/confidence changed')
        require(sum((nt-ot).values()) == 1002, key+' unexpected non-UV semantic triangle delta')
        target_expectations = {'added_triangles': 1002, 'old_oriented_triangle_geometry_material_normal_confidence_multiset_complete_subset': True, 'interpretation': '501 added clapboard quads; prior body geometry preserved independent of export UV seams or vertex order.'}
    else: require(False, 'unknown intended target '+key)
    paired = []
    if len(od['meshes']) == len(nd['meshes']):
        _, _, oa = parse(oldraw); _, _, na = parse(newraw)
        for mi, (om, nm) in enumerate(zip(od['meshes'], nd['meshes'])):
            if len(om['primitives']) != len(nm['primitives']): continue
            for pi, (a, b) in enumerate(zip(om['primitives'], nm['primitives'])):
                av = oa(a['attributes']['POSITION'])[1]; bv = na(b['attributes']['POSITION'])[1]
                if len(av) == len(bv):
                    changes = [(i, x, y) for i, (x, y) in enumerate(zip(av, bv)) if x != y]
                    paired.append({'mesh': mi, 'primitive': pi, 'count': len(av), 'changed_position_rows': len(changes), 'maximum_absolute_delta_by_axis': [max((abs(x[k]-y[k]) for _, x, y in changes), default=0) for k in range(3)], 'sample_changed_rows': [{'index': i, 'before': x, 'after': y} for i, x, y in changes[:24]], 'row_pairing_note': 'Index-aligned export rows; exporter reordering can inflate this count. Multiset deltas below do not assume row correspondence.'})
    return {'asset_key': key, 'before': old, 'after': new, 'cost_delta': {k: new[k]-old[k] for k in ['bytes', 'vertices_including_export_splits', 'indices', 'triangles', 'primitives', 'materials']}, 'bounds_exact': True, 'nodes_and_materials_exact': True, 'target_specific_expectations': target_expectations, 'oriented_triangle_semantic_removed': sum((ot-nt).values()), 'oriented_triangle_semantic_added': sum((nt-ot).values()), 'non_uv_semantic_multiset_removed_rows': sum((os-ns).values()), 'non_uv_semantic_multiset_added_rows': sum((ns-os).values()), 'position_multiset_removed_rows': sum((op-np).values()), 'position_multiset_added_rows': sum((np-op).values()), 'position_multiset_removed_distinct': len(op-np), 'position_multiset_added_distinct': len(np-op), 'position_multiset_removed_sample': [{'position': p, 'multiplicity': n} for p, n in sorted((op-np).items())[:32]], 'position_multiset_added_sample': [{'position': p, 'multiplicity': n} for p, n in sorted((np-op).items())[:32]], 'index_aligned_primitive_position_deltas': paired}

def audit(args):
    repo = args.repo.resolve(); output = args.output_dir.resolve()
    require(not output.is_relative_to(repo), 'audit receipts must be outside the source checkout')
    output.mkdir(parents=True, exist_ok=True)
    git_env = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0')
    def git(*argv): return subprocess.check_output(['git', *argv], cwd=repo, env=git_env)
    def blob(commit, path): return git('show', commit+':'+path)
    retained = git('rev-parse', '--verify', args.retained_sha+'^{commit}').decode().strip()
    rawcommit = git('cat-file', '-p', retained); header = rawcommit.decode().split('\n\n', 1)[0]
    parents = [x.split()[1] for x in header.splitlines() if x.startswith('parent ')]
    require(parents == [EXPECTED_PARENT], 'wrong raw native parent: '+repr(parents))
    braw = (HERE/'BEFORE-BINDING.json').read_bytes(); require(sha(braw) == EXPECTED_BIND_SHA, 'before-binding hash changed'); binding = json.loads(braw)
    require(binding['captured_HEAD'] == EXPECTED_PARENT, 'binding parent mismatch')
    foreign = json.loads((HERE/binding['foreign_default_rows_file']).read_bytes()); fv = json.loads((HERE/binding['foreign_version_rows_file']).read_bytes())
    require(sha(canon(foreign)) == binding['foreign_default_rows_set_canonical_sha256'], 'foreign default baseline changed')
    require(sha(canon(fv)) == binding['foreign_version_rows_set_canonical_sha256'], 'foreign variant baseline changed')
    regraw = {n: blob(retained, PREFIX+'assets/'+n) for n in ['manifest.json', 'manifest.web.json', 'manifest.versions.json']}
    m = json.loads(regraw['manifest.json'])['assets']; w = json.loads(regraw['manifest.web.json'])['masters']; versions = json.loads(regraw['manifest.versions.json'])['assets']
    require((len(m), len(w), len(versions)) == (1044, 1044, 6), 'registry counts drift')
    scope = {x['asset_key'] for x in binding['affected']}
    require(len(scope) == 83 and len({x['structure_id'] for x in binding['affected']}) == 83, 'scope cardinality')
    require(set(m) == scope|set(foreign) and set(w) == set(m) and set(versions) == set(fv), 'registry key drift')
    for path, receipt in binding['source_state']['source_invariance'].items():
        if path.startswith(PREFIX+'assets/manifest'): continue
        require(sha(blob(retained, path)) == receipt['sha256'], 'native source recipe/record changed: '+path)
    # Before manifests and before old models must be genuine blobs from the bound raw parent.
    for name, receipt in binding['registry_files'].items():
        require(sha(blob(EXPECTED_PARENT, PREFIX+name)) == receipt['sha256'], 'bound parent registry mismatch: '+name)
        require(sha((HERE/('BEFORE-'+Path(name).name)).read_bytes()) == receipt['sha256'], 'before registry snapshot mismatch: '+name)
    affected = []; controls = []; targets = []
    for x in binding['affected']:
        key = x['asset_key']; row = m[key]; oldrow = x['old_registry_row']
        # The bound resolved document uses mesh_inputs.structure_inputs_sha's exact JSON serialization.
        fresh = sha(json.dumps(x['current_inputs_doc'], sort_keys=True).encode())
        require(fresh == x['current_inputs_sha256'] == row['inputs_sha256'], key+' new inputs not fresh')
        expectedrow = dict(oldrow); expectedrow['inputs_sha256'] = fresh; expectedrow['bytes'] = row['bytes']
        require(row == expectedrow, key+' unexpected registry row edits')
        masterpath = x['before_master']['path']; oldraw = blob(EXPECTED_PARENT, masterpath); newraw = blob(retained, masterpath)
        require(sha(oldraw) == x['before_master']['sha256'] and len(oldraw) == x['before_master']['bytes'], key+' old MASTER mismatch')
        require(len(newraw) == row['bytes'] and sha(newraw) == w[key], key+' new MASTER/web receipt mismatch')
        webrows = []; firstweb = None
        for oldweb in x['before_web_outputs']:
            oldwebraw = blob(EXPECTED_PARENT, oldweb['path']); newwebraw = blob(retained, oldweb['path'])
            require(sha(oldwebraw) == oldweb['sha256'] and len(oldwebraw) == oldweb['bytes'], key+' old WEB mismatch')
            same = oldwebraw == newwebraw
            if not x['intentional_geometry_target']: require(same, key+' strict WEB control byte drift')
            if firstweb is None: firstweb = newwebraw
            webrows.append({'path': oldweb['path'], 'before_bytes': len(oldwebraw), 'after_bytes': len(newwebraw), 'before_sha256': sha(oldwebraw), 'after_sha256': sha(newwebraw), 'strict_identity': same})
        affected.append({'asset_key': key, 'intentional_geometry_target': x['intentional_geometry_target'], 'fresh_inputs_sha256': fresh, 'master_before_sha256': sha(oldraw), 'master_after_sha256': sha(newraw), 'master_before_bytes': len(oldraw), 'master_after_bytes': len(newraw), 'web_master_receipt_sha256': w[key], 'web_outputs': webrows})
        if x['intentional_geometry_target']: targets.append(compare_target(key, oldraw, newraw))
        else: controls.append(compare_control(key, oldraw, newraw, firstweb))
    package_members = {}; package_provenance = {}; package_loaded = False
    packaged_paths = {PREFIX+'assets/'+kind+'/glessner_house__as_built_1887'+suffix+'.glb' for kind,suffix in [('gltf',''),('web',''),('web','.light')]}
    def read_foreign_asset(path):
        nonlocal package_loaded
        if path not in packaged_paths: return blob(retained,path)
        if not package_loaded:
            package_prefix=PREFIX+'docs/RESEARCH/glessner-v4-recovery/'
            manifest_path=package_prefix+'manifest.json'
            old_manifest=blob(EXPECTED_PARENT,manifest_path); new_manifest=blob(retained,manifest_path)
            require(old_manifest==new_manifest,'foreign Glessner package manifest changed')
            manifest=json.loads(new_manifest)
            require({PREFIX+k for k in manifest['files']}==packaged_paths,'unexpected packaged Glessner member set')
            chunks=[];part_receipts=[]
            for part in manifest['parts']:
                partpath=package_prefix+part['name']
                old_oid=git('rev-parse',EXPECTED_PARENT+':'+partpath).decode().strip()
                new_oid=git('rev-parse',retained+':'+partpath).decode().strip()
                require(old_oid==new_oid,'foreign Glessner package part changed '+partpath)
                raw=blob(retained,partpath)
                require(len(raw)==part['bytes'] and sha(raw)==part['sha256'],'corrupt Glessner package part '+partpath)
                chunks.append(raw);part_receipts.append({'path':partpath,'before_after_git_blob_id':new_oid,'bytes':len(raw),'sha256':sha(raw)})
            archive=b''.join(chunks);chunks.clear()
            require(len(archive)==manifest['archive_bytes'] and sha(archive)==manifest['archive_sha256'],'Glessner committed package archive checksum')
            with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
                names=zipped.namelist();require(len(names)==len(set(names)) and set(names)==set(manifest['files']),'Glessner zip member set')
                for name,entry in manifest['files'].items():
                    raw=zipped.read(name);fullpath=PREFIX+name
                    require(len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],'Glessner archived member checksum '+name)
                    live=(repo/fullpath).read_bytes()
                    require(live==raw,'Glessner materialized bytes differ from retained committed package '+name)
                    package_members[fullpath]=raw
            package_provenance.update({'manifest_path':manifest_path,'manifest_before_after_exact':True,'manifest_sha256':sha(new_manifest),'archive_bytes':len(archive),'archive_sha256':sha(archive),'all_parts_before_after_git_blobs_exact':True,'parts':part_receipts,'all_three_archive_members_and_actual_materialized_bytes_verified':True,'members':manifest['files']})
            package_loaded=True
        return package_members[path]
    def verify_foreign(key, old, variant=False):
        row = old['row'] if variant else old['old_registry_row']
        require((versions if variant else m)[key] == row, key+' foreign registry row drift')
        if not variant: require(w[key] == old['web_receipt_master_sha256'], key+' foreign web receipt drift')
        for receipt in [old['before_master'], *old['before_web_outputs']]:
            actual = read_foreign_asset(receipt['path'])
            require(sha(actual) == receipt['sha256'] and len(actual) == receipt['bytes'], key+' foreign asset drift: '+receipt['path'])
    for key, old in foreign.items(): verify_foreign(key, old)
    for key, old in fv.items(): verify_foreign(key, old, True)
    require(len(controls) == 81 and len(targets) == 2 and len(foreign) == 961 and len(fv) == 6, 'final audit cardinalities')
    require(sha(regraw['manifest.versions.json']) == binding['registry_files']['assets/manifest.versions.json']['sha256'], 'variant manifest bytes changed')
    changes = git('diff', '--name-only', EXPECTED_PARENT, retained).decode().splitlines()
    allowed = {PREFIX+'assets/gltf/'+key for key in scope}|{oldweb['path'] for x in binding['affected'] if x['intentional_geometry_target'] for oldweb in x['before_web_outputs']}|{PREFIX+'assets/manifest.json', PREFIX+'assets/manifest.web.json'}
    require(set(changes) <= allowed, 'unexpected retained paths: '+repr(sorted(set(changes)-allowed)))
    required = {PREFIX+'assets/gltf/'+x['asset_key'] for x in binding['affected'] if x['intentional_geometry_target']}|{PREFIX+'assets/manifest.json', PREFIX+'assets/manifest.web.json'}
    require(required <= set(changes), 'missing native target/registry paths: '+repr(sorted(required-set(changes))))
    result = {'status': 'PASS_NATIVE83_FRESH_CONTROL81_GEOMETRY_EXACT_WEB81_STRICT_FOREIGN961_PLUS6_EXACT', 'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'retained_sha': retained, 'actual_raw_parents': parents, 'native_run_id_supplied': args.run_id, 'native_run_claim_limit': 'Run ID is supplied context, not independently authenticated by this local Git audit.', 'raw_commit_sha256': sha(rawcommit), 'before_binding_sha256': sha(braw), 'counts': {'fresh_default_bindings': 83, 'selected_variants': 0, 'intentional_geometry_targets': 2, 'controls_geometry_material_confidence_topology_exact': 81, 'controls_master_byte_identical': sum(x['master_bytes_identical'] for x in controls), 'controls_unused_uv_only_exceptions': sum(x['unused_uv_only_exception'] for x in controls), 'controls_web_strict_byte_identity': 81, 'foreign_defaults_rows_and_assets_exact': 961, 'foreign_versions_rows_and_assets_exact': 6}, 'changed_paths': changes, 'affected_rows': affected, 'target_comparisons': targets, 'control_details': controls, 'foreign_default_keys_exact': sorted(foreign), 'foreign_variant_keys_exact': sorted(fv), 'variant_manifest_bytes_exact': True, 'packaged_foreign_asset_provenance': package_provenance, 'registry_after_sha256': {k: sha(v) for k, v in regraw.items()}, 'claim_limit': 'Read-only immutable Git object audit of retained native outputs. No browser/GPU image matching, runtime scene acceptance, image gate closure, or publish is claimed. UV exceptions are accepted only for unused UV data/bounds while every nonUV accessor/material/node/topology is exact and actual untextured TEXCOORD-free WEB bytes are strictly identical.'}
    (output/'POST-NATIVE-AUDIT.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    (output/'POST-NATIVE-CONTROLS.json').write_text(json.dumps(controls, indent=2, sort_keys=True)+'\n')
    (output/'POST-NATIVE-TARGETS.json').write_text(json.dumps(targets, indent=2, sort_keys=True)+'\n')
    return result

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('retained_sha'); p.add_argument('--run-id', default=None)
    p.add_argument('--repo', type=Path, default=Path('/tmp/chicago-west-wicket-20261109'))
    p.add_argument('--output-dir', type=Path, default=HERE)
    args = p.parse_args()
    try:
        result = audit(args)
    except Exception as error:
        failure = {'status': 'FAIL_NATIVE_AUDIT', 'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'retained_sha_supplied': args.retained_sha, 'run_id_supplied': args.run_id, 'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(), 'claim_limit': 'No native acceptance. Investigate this literal failure; do not rewrite expected scope or weaken checks to force green.'}
        failure_dir = args.output_dir.resolve()
        if failure_dir.is_relative_to(args.repo.resolve()): failure_dir = HERE
        failure_dir.mkdir(parents=True, exist_ok=True)
        (failure_dir/'POST-NATIVE-AUDIT-FAIL.json').write_text(json.dumps(failure, indent=2)+'\n')
        print(json.dumps(failure, indent=2), file=sys.stderr)
        return 1
    print(result['status']); print(json.dumps(result['counts'], indent=2)); print(args.output_dir/'POST-NATIVE-AUDIT.json')
    return 0
if __name__ == '__main__': sys.exit(main())
