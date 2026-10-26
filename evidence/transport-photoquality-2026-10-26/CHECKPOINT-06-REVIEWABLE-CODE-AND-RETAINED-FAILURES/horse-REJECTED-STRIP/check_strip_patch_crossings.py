"""Actual static replacement-strip crossings, without false face ancestry.

Every proper patch/body and patch/globe intersection is rejected. The immutable
925 exterior retains its own unchanged historical ledger; replaced slots have
no inherited crossing permission. No continuous-motion acceptance is implied.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import time
import numpy as np


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def module(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def function_source(path, name):
    text=path.read_text()
    return ast.dump(next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name==name),include_attributes=False)


def patch_body_pairs(body, patch, kernel):
    lo,hi=body.min(axis=1),body.max(axis=1);found=[];broad=0
    for i in sorted(patch):
        candidates=np.flatnonzero(np.all(lo<=hi[i]+kernel.TOL,axis=1)&np.all(hi>=lo[i]-kernel.TOL,axis=1))
        for j in candidates:
            j=int(j)
            if j==i or (j in patch and j<i):continue
            broad+=1
            if kernel.crosses(body[i],body[j]):found.append((i,j))
    return found,broad


def patch_globe_pairs(body, patch, globe, kernel):
    lo,hi=globe.min(axis=1),globe.max(axis=1);found=[];broad=0
    for i in sorted(patch):
        q=body[i]
        candidates=np.flatnonzero(np.all(lo<=q.max(axis=0)+kernel.TOL,axis=1)&np.all(hi>=q.min(axis=0)-kernel.TOL,axis=1))
        for j in candidates:
            broad+=1
            if kernel.crosses(q,globe[j]):found.append((i,int(j)))
    return found,broad


def controls(kernel, triangle):
    kernel.self_test()
    q=triangle.mean(axis=0);edge=triangle[1]-triangle[0]
    normal=np.cross(edge,triangle[2]-triangle[0]);normal/=np.linalg.norm(normal)
    scale=min(np.linalg.norm(edge),np.linalg.norm(triangle[2]-triangle[0]))*.1
    crossing=np.array([q-normal*scale,q+normal*scale,q+normal*scale+edge*.05])
    far=crossing+normal
    before,_=patch_body_pairs(np.array([triangle,far]),{0},kernel)
    after,_=patch_body_pairs(np.array([triangle,crossing]),{0},kernel)
    require(before==[]and after==[(0,1)],'Actual added patch/body crossing was not detected')
    before_globe,_=patch_globe_pairs(np.array([triangle]),{0},np.array([far]),kernel)
    after_globe,_=patch_globe_pairs(np.array([triangle]),{0},np.array([crossing]),kernel)
    require(before_globe==[]and after_globe==[(0,0)],'Actual added patch/globe crossing was not detected')
    # Reusing source face-slot numbers never exempts a replacement crossing.
    inherited_fake_pair={(0,1)}
    require(bool(after)and set(after)<=inherited_fake_pair,'Crossing ancestry corruption setup failed')
    require(bool(after),'A false inherited pair excused a replacement crossing')
    return {'kernel_real_crossing_boundary_interval_coplanar_and_shared_boundary_controls':True,
            'added_patch_body_crossing_detected':True,'added_patch_globe_crossing_detected':True,
            'unchanged_separated_body_and_globe_controls':True,
            'replacement_face_slot_has_no_inherited_crossing_permission':True}


def read_mesh(anatomy, doc, binary, index):
    primitive=doc['meshes'][index]['primitives'][0]
    positions=np.asarray(anatomy.read_attribute(doc,binary,primitive['attributes']['POSITION']))
    indices=np.asarray(anatomy.read_attribute(doc,binary,primitive['indices'])).reshape(-1,3)
    result=positions[indices]
    require(np.all(np.isfinite(result)),'Nonfinite mesh triangle')
    require(np.all(np.linalg.norm(np.cross(result[:,1]-result[:,0],result[:,2]-result[:,0]),axis=1)>1e-14),'Degenerate body/globe triangle')
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--app-root',type=Path,required=True);parser.add_argument('--packet',type=Path,required=True);parser.add_argument('--kernel',type=Path,required=True);parser.add_argument('--inherited-ledger',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    require(not args.out.exists(),'Use a fresh result name')
    started=time.monotonic()
    require(digest(args.kernel.read_bytes())=='8bf97472ae13d5d6d764ac9f381f0a2bfbf8aea6108932382d705a1372a4ae33','Corrected proper-crossing kernel changed')
    kernel=module(args.kernel,'strip_crossing_kernel');anatomy=kernel.anatomy
    require(kernel.TOL==1e-9,'Numerical tolerance changed')
    source=args.app_root/'assets/authored/transport/horse_standing'
    parent_path=source/'horse-sevket-anatomy-v2.glb';parent_raw=parent_path.read_bytes();parent_doc,parent_binary=anatomy.base.read_glb(parent_raw)
    original_path=source/anatomy.base.PARENT_FILE;original_raw=original_path.read_bytes();original_doc,original_binary=anatomy.base.read_glb(original_raw)
    candidate_path=args.packet/'horse-sevket-upper-lid-strip-prototype-v1.glb';candidate_raw=candidate_path.read_bytes();doc,binary=anatomy.base.read_glb(candidate_raw)
    require(digest(parent_raw)=='925fac957110b9b57b95c5abfed17fabf29f868b173f38f0569d984dd9999a48','Parent925 changed')
    require(digest(candidate_raw)=='5a2b2e87c3931e3ab82be3ce3bc69724a0a088aac30920cea9ad348bbaf8fad5','Frozen strip changed')
    recipe_raw=(args.packet/'RETOPOLOGY-RECIPE-RETURN-CHART-V2.json').read_bytes();recipe=json.loads(recipe_raw)
    qualifier_path=args.packet/'qualify_strip_topology_control_v2.py'
    require(digest(qualifier_path.read_bytes())=='eab41c8a30d7a36b377babc9c3852b4e43a54cb357882d97a8517a5e11d6d21f','Reviewed qualifier changed')
    qualification=module(qualifier_path,'strip_topology_qualification');qualification.parent_raw=parent_raw;qualification.recipe_raw=recipe_raw
    structure=qualification.inspect(doc,binary,parent_doc,parent_binary,anatomy.read_attribute(original_doc,original_binary,203),recipe,anatomy)
    patch=set(structure['removed_faces']);body=read_mesh(anatomy,doc,binary,1);globe=read_mesh(anatomy,doc,binary,2)
    old_body=read_mesh(anatomy,parent_doc,parent_binary,1);old_globe=read_mesh(anatomy,parent_doc,parent_binary,2)
    exterior=sorted(set(range(len(body)))-patch)
    require(np.array_equal(body[exterior],old_body[exterior])and np.array_equal(globe,old_globe),'Protected exterior/globe geometry changed')
    ledger_raw=args.inherited_ledger.read_bytes();ledger=json.loads(ledger_raw)
    require(digest(ledger_raw)=='c23d46bc7430a059caca290a09610d78d80c3b15edf3c42596e92daadb2a6da6','Immutable inherited ledger changed')
    require(ledger['candidate_sha256']==digest(parent_raw)and ledger['tolerance_m']==kernel.TOL,'Inherited ledger source/tolerance mismatch')
    old_checker=args.app_root/'tools/transport/check_horse_anatomy_crossings.py'
    require(digest(old_checker.read_bytes())==ledger['checker_sha256'],'Inherited ledger checker binding failed')
    require(function_source(old_checker,'crosses')==function_source(args.kernel,'crosses'),'Inherited and current mathematical kernels differ')
    old_pairs=ledger['candidate_proper_crossings'];outside_pairs=[pair for pair in old_pairs if not(set(pair)&patch)]
    removed_pairs=[pair for pair in old_pairs if set(pair)&patch]
    negative_controls=controls(kernel,body[min(patch)])
    body_pairs,body_broad=patch_body_pairs(body,patch,kernel)
    globe_pairs,globe_broad=patch_globe_pairs(body,patch,globe,kernel)
    require(parent_path.read_bytes()==parent_raw and candidate_path.read_bytes()==candidate_raw and original_path.read_bytes()==original_raw,'Input changed during checking')
    result={'schema':'canonical-upper-lid-strip-static-patch-body-globe-crossings-v1','candidate_sha256':digest(candidate_raw),'parent925_sha256':digest(parent_raw),'checker_sha256':digest(Path(__file__).read_bytes()),'kernel_sha256':digest(args.kernel.read_bytes()),'qualifier_sha256':digest(qualifier_path.read_bytes()),'inherited_ledger_sha256':digest(ledger_raw),'tolerance_m':kernel.TOL,'replacement_faces':sorted(patch),'replacement_faces_do_not_inherit_old_face_ancestry':True,'body_patch_aabb_pairs':body_broad,'globe_patch_aabb_pairs':globe_broad,'patch_body_proper_crossings':body_pairs,'patch_globe_proper_crossings':globe_pairs,'inherited925_all_body_pairs':old_pairs,'unchanged_exterior_inherited_pairs':outside_pairs,'superseded_pleat_crossing_pairs_not_inherited':removed_pairs,'controls':negative_controls,'seconds':time.monotonic()-started,'status':'NO_PROPER_REPLACEMENT_PATCH_CROSSINGS'if not body_pairs and not globe_pairs else'REPLACEMENT_PATCH_PROPER_CROSSINGS_REJECTED','scope':'Static canonical142-face replacement versus every body face including its own faces, and every Eye_brown globe face. No adjacency exemption; open-interior interval and coplanar positive-area kernel at1nm. Exterior exact geometry preserves its317 inherited source pairs, without reclassifying replacement slots. This does not certify continuous gait, hair interfaces, photorealism, native loaded129 or published world acceptance.'}
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if not isinstance(v,list)}))
    return bool(body_pairs or globe_pairs)


if __name__=='__main__':
    raise SystemExit(main())
