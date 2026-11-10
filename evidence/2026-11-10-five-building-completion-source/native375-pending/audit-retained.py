#!/usr/bin/env python3
"""Read-only retained native audit. Usage: audit-retained.py RETAINED_SHA [--run-id ID].
Reads immutable Git blobs, never checks out files, and writes receipts only beside this
script (or --output-dir). A failed assertion is retained as FAIL, never an acceptance.
"""
from pathlib import Path
from collections import Counter
import argparse, datetime, hashlib, io, json, math, os, re, struct, subprocess, sys, traceback, zipfile

HERE = Path(__file__).resolve().parent
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

def audit(args):
    repo=args.repo.resolve();out=args.output_dir.resolve();require(not out.is_relative_to(repo),'Receipt output must be outside source repo');out.mkdir(parents=True,exist_ok=True)
    git_env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
    def git(*argv):return subprocess.check_output(['git',*argv],cwd=repo,env=git_env)
    def blob(commit,path):return git('show',commit+':'+path)
    bpath=args.binding.resolve();braw=bpath.read_bytes();binding=json.loads(braw);base=binding['captured_HEAD'];base_dir=bpath.parent
    require(binding['status']=='CLEAN_HEAD_PINNED_BEFORE_BINDING'and binding['pinned_HEAD']==base,'Binding is not clean-head pinned')
    if args.binding_sha256:require(sha(braw)==args.binding_sha256,'Binding checksum differs from dispatch receipt')
    retained=git('rev-parse','--verify',args.retained_sha+'^{commit}').decode().strip();rawcommit=git('cat-file','-p',retained);header=rawcommit.decode().split('\n\n',1)[0];parents=[x.split()[1]for x in header.splitlines()if x.startswith('parent ')]
    require(parents==[base],'Wrong raw retained-native parent '+repr(parents))
    foreign_raw=(base_dir/binding['foreign_rows_file']).read_bytes();foreign=json.loads(foreign_raw);require(sha(canon(foreign))==binding['foreign_rows_canonical_sha256'],'Foreign baseline receipt changed')
    for path,receipt in binding['source_files'].items():require(sha(blob(retained,path))==receipt['sha256'],'Native changed bound geometry/source '+path)
    regraw={n:blob(retained,PREFIX+'assets/'+n)for n in ['manifest.json','manifest.web.json','manifest.versions.json']};oldraw={n:(base_dir/('BEFORE-'+n)).read_bytes()for n in regraw};reg={n:json.loads(b)for n,b in regraw.items()};before={n:json.loads(b)for n,b in oldraw.items()};m=reg['manifest.json']['assets'];w=reg['manifest.web.json']['masters'];v=reg['manifest.versions.json']['assets'];oldm=before['manifest.json']['assets'];oldw=before['manifest.web.json']['masters'];oldv=before['manifest.versions.json']['assets']
    require(set(m)==set(oldm)and set(w)==set(oldw)==set(m)and set(v)==set(oldv),'Native registry membership changed')
    for name,receipt in binding['registry_files'].items():
        require(sha(blob(base,PREFIX+name))==receipt['sha256'],'Bound raw-parent registry mismatch '+name)
        require(sha(oldraw[Path(name).name])==receipt['sha256'],'Snapshot registry mismatch '+name)
    # Producer metadata around the per-asset maps is invariant too.
    for name,field in [('manifest.json','assets'),('manifest.web.json','masters'),('manifest.versions.json','assets')]:require({k:x for k,x in before[name].items()if k!=field}=={k:x for k,x in reg[name].items()if k!=field},'Unexpected registry header drift '+name)
    affected=[];controls=[];targets=[];allowed={PREFIX+'assets/'+n for n in regraw};required={PREFIX+'assets/manifest.json',PREFIX+'assets/manifest.web.json'};scope=set();target_ids=set()
    for x in binding['affected']:
        key=x['asset_key'];kind=x['kind'];scope.add((kind,key));row=(m if kind=='default'else v)[key];oldrow=x['old_registry_row'];fresh=sha(json.dumps(x['current_inputs_doc'],sort_keys=True).encode());require(fresh==x['current_inputs_sha256']==row['inputs_sha256'],key+' not fresh against frozen resolved input doc')
        masterpath=x['before_master']['path'];a=blob(base,masterpath);b=blob(retained,masterpath);require(sha(a)==x['before_master']['sha256']and len(a)==x['before_master']['bytes'],key+' old MASTER does not match pinned parent')
        require(len(b)==row['bytes'],key+' native MASTER bytes mismatch registry');expected=dict(oldrow,inputs_sha256=fresh,bytes=len(b))
        if kind=='default':require(w[key]==sha(b),key+' web master receipt not native MASTER hash')
        else:expected['web_master_sha256']=sha(b)
        require(row==expected,key+' unexpected per-asset registry field edits')
        allowed.add(masterpath);webrows=[];firstweb=None
        for old in x['before_web_outputs']:
            aw=blob(base,old['path']);bw=blob(retained,old['path']);require(sha(aw)==old['sha256']and len(aw)==old['bytes'],key+' old WEB/LOD mismatch');same=aw==bw
            if not x['intentional_geometry_target']:require(same,key+' selected control WEB/LOD byte drift')
            else:allowed.add(old['path'])
            if firstweb is None:firstweb=bw
            webrows.append({'path':old['path'],'before_sha256':sha(aw),'after_sha256':sha(bw),'before_bytes':len(aw),'after_bytes':len(bw),'strict_identity':same})
        affected.append({'kind':kind,'asset_key':key,'structure_id':x['structure_id'],'intentional_geometry_target':x['intentional_geometry_target'],'fresh_inputs_sha256':fresh,'before_master_sha256':sha(a),'after_master_sha256':sha(b),'web_outputs':webrows})
        if not x['intentional_geometry_target']:
            controls.append({'kind':kind,**compare_control(key,a,b,firstweb)})
        else:
            target_ids.add(x['structure_id']);oa,oset,op,ot,od=geometry_summary(a);nb,nset,np,nt,nd=geometry_summary(b)
            require(oset!=nset,key+' intended target has no nonUV geometry/material semantic change')
            require(od.get('nodes')==nd.get('nodes'),key+' target node/world transform changed')
            required.add(masterpath)
            targets.append({'kind':kind,'asset_key':key,'structure_id':x['structure_id'],'before':oa,'after':nb,'cost_delta':{k:nb[k]-oa[k]for k in ['bytes','vertices_including_export_splits','indices','triangles','primitives','materials']},'bounds_equal':oa['local_mesh_union_bounds']==nb['local_mesh_union_bounds'],'node_transforms_exact':True,'materials_equal':od.get('materials')==nd.get('materials'),'non_uv_semantic_removed':sum((oset-nset).values()),'non_uv_semantic_added':sum((nset-oset).values()),'oriented_triangle_semantic_removed':sum((ot-nt).values()),'oriented_triangle_semantic_added':sum((nt-ot).values()),'claim_limit':'Target geometry change is measured, not declared visually correct. Source-specific semantic probes and actual final picture/UI review remain required.'})
    require(target_ids==set(binding['intended_geometry_structure_ids']),'Intended target ID set changed')
    # Some foreign Glessner files are materialized from its committed multipart zip,
    # not individual Git blobs. Verify that exact immutable package, never live files.
    package_members={};package_provenance={};package_loaded=False
    packaged_paths={PREFIX+'assets/'+kind+'/glessner_house__as_built_1887'+suffix+'.glb'for kind,suffix in [('gltf',''),('web',''),('web','.light')]}
    def foreign_blob(path):
        nonlocal package_loaded
        if path not in packaged_paths:return blob(retained,path)
        if not package_loaded:
            pp=PREFIX+'docs/RESEARCH/glessner-v4-recovery/';mp=pp+'manifest.json';bm=blob(base,mp);am=blob(retained,mp);require(bm==am,'Foreign recovery package manifest changed');manifest=json.loads(am);require({PREFIX+k for k in manifest['files']}==packaged_paths,'Recovery package member set changed');parts=[];parts_receipts=[]
            for part in manifest['parts']:
                pathpart=pp+part['name'];oldoid=git('rev-parse',base+':'+pathpart).decode().strip();newoid=git('rev-parse',retained+':'+pathpart).decode().strip();require(oldoid==newoid,'Foreign recovery package part changed');raw=blob(retained,pathpart);require(len(raw)==part['bytes']and sha(raw)==part['sha256'],'Recovery package part corrupt');parts.append(raw);parts_receipts.append({'path':pathpart,'git_blob_id':newoid,'sha256':sha(raw),'bytes':len(raw)})
            archive=b''.join(parts);parts.clear();require(len(archive)==manifest['archive_bytes']and sha(archive)==manifest['archive_sha256'],'Recovery archive checksum mismatch')
            with zipfile.ZipFile(io.BytesIO(archive))as z:
                require(len(z.namelist())==len(set(z.namelist()))and set(z.namelist())==set(manifest['files']),'Recovery archive names mismatch')
                for name,entry in manifest['files'].items():
                    raw=z.read(name);require(len(raw)==entry['bytes']and sha(raw)==entry['sha256'],'Recovery member checksum mismatch');package_members[PREFIX+name]=raw
            package_provenance.update({'manifest_path':mp,'manifest_sha256':sha(am),'all_parts_before_after_git_blobs_exact':True,'parts':parts_receipts,'archive_sha256':sha(archive),'members':manifest['files']});package_loaded=True
        return package_members[path]
    foreign_verified=[]
    for x in foreign:
        key=x['asset_key'];kind=x['kind'];require((m if kind=='default'else v)[key]==x['old_registry_row'],key+' foreign registry row drift')
        if kind=='default':require(w[key]==x['web_receipt_master_sha256'],key+' foreign WEB master receipt drift')
        for old in [x['before_master'],*x['before_web_outputs']]:
            raw=foreign_blob(old['path']);require(sha(raw)==old['sha256']and len(raw)==old['bytes'],key+' foreign file drift '+old['path'])
        foreign_verified.append({'kind':kind,'asset_key':key,'registry_and_all_master_web_lod_bytes_exact':True})
    require(len(affected)==binding['counts']['selected_defaults']+binding['counts']['selected_variants'],'Affected row count mismatch')
    require(len(controls)==binding['counts']['selected_control_asset_rows']and len(targets)==binding['counts']['selected_geometry_target_asset_rows'],'Control/target count mismatch')
    require(len(foreign_verified)==binding['counts']['foreign_defaults']+binding['counts']['foreign_variants'],'Foreign count mismatch')
    changes=git('diff','--name-only',base,retained).decode().splitlines();require(set(changes)<=allowed,'Unexpected retained changed paths '+repr(sorted(set(changes)-allowed)));require(required<=set(changes),'Missing intended target/native registry changes '+repr(sorted(required-set(changes))))
    result={'status':'PASS_SCOPED_NATIVE_FRESH_CONTROLS_EXACT_FOREIGN_EXACT','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retained_sha':retained,'actual_raw_parents':parents,'before_binding_sha256':sha(braw),'native_run_id_supplied':args.run_id,'run_claim_limit':'Supplied run ID is context, not independent authentication by this local Git audit.','counts':{**binding['counts'],'controls_master_byte_identical':sum(x['master_bytes_identical']for x in controls),'controls_unused_uv_only_exceptions':sum(x['unused_uv_only_exception']for x in controls),'controls_WEB_LOD_strict_identity':len(controls)},'changed_paths':changes,'affected_rows':affected,'control_details':controls,'target_comparisons':targets,'foreign_verified':foreign_verified,'foreign_package_provenance':package_provenance,'registry_after_sha256':{n:sha(raw)for n,raw in regraw.items()},'claim_limit':'Read-only immutable Git audit. All selected rows fresh to exact frozen resolved inputs; selected controls nonUV geometry/topology/material/confidence exact and WEB/LOD bytes strict; foreign rows/assets exact. Target geometry changes measured. No image match, app acceptance, publish or original-ticket closure claimed.'}
    (out/'POST-NATIVE-AUDIT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(out/'POST-NATIVE-CONTROLS.json').write_text(json.dumps(controls,indent=2,sort_keys=True)+'\n');(out/'POST-NATIVE-TARGETS.json').write_text(json.dumps(targets,indent=2,sort_keys=True)+'\n');return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('retained_sha');p.add_argument('--run-id');p.add_argument('--binding',type=Path,default=HERE/'BEFORE-BINDING.json');p.add_argument('--binding-sha256');p.add_argument('--repo',type=Path,default=Path('/tmp/chicago-west-wicket-20261109'));p.add_argument('--output-dir',type=Path,default=HERE);args=p.parse_args()
    try:r=audit(args)
    except Exception as e:
        failure={'status':'FAIL_NATIVE_AUDIT','retained_sha_supplied':args.retained_sha,'error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc(),'claim_limit':'No native acceptance. Investigate literal failure; do not weaken scope/control checks to force green.'};out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True);(out/'POST-NATIVE-AUDIT-FAIL.json').write_text(json.dumps(failure,indent=2)+'\n');print(json.dumps(failure,indent=2),file=sys.stderr);return 1
    print(r['status']);print(json.dumps(r['counts'],indent=2));return 0
if __name__=='__main__':sys.exit(main())
