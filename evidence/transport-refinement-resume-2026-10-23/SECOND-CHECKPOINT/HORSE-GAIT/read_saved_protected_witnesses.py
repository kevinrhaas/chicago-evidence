from pathlib import Path
import json,sys
import numpy as np
r=Path(__file__).parent;v=r/'V23-TRIANGLE-STRAIN-LIMIT';sys.path.insert(0,str(v));from actual_model import Model
pins=json.loads((v/'INPUT-PINS.json').read_text())
with np.load(pins['phase_a_arrays']['path'])as a:
 cls=a['vertex_classes_1'];protected=a['source_protected_class_ids'];other=np.unique(np.r_[a['vertex_classes_0'],a['vertex_classes_2']]);fixed=np.isin(cls,protected)|np.isin(cls,other)
m=Model(Path(pins['immutable_source_rig']['path']));points=m.mesh(27)[0];pr=m.g['meshes'][m.g['nodes'][27]['mesh']]['primitives'][0];tri=m.accessor(pr['indices']).astype(int).reshape(-1,3);edges=np.unique(np.sort(np.concatenate([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]]),axis=1),axis=0);pairs=edges[fixed[edges].all(axis=1)];restlen=np.linalg.norm(points[pairs[:,0]]-points[pairs[:,1]],axis=1);valid=restlen>1e-8;pairs=pairs[valid];restlen=restlen[valid]
report=json.loads((v/'ACTUAL/ACTUAL-V23-TRIANGLE-STRAIN-LIMIT-ORIGINAL65-READBACK.json').read_text());out={'scope':'Saved corrected frames/static model arrays only; no new pose/solver/skin evaluation','protected_render_rows':int(fixed.sum()),'all_fixed_edges':len(pairs),'all_fixed_edge_ratio_min':1.,'all_fixed_edge_ratio_max':1.,'witnesses':{}}
with np.load(v/'ACTUAL/DIAGNOSTIC-CORRECTED-FRAMES-NOT-MODEL.npz')as a:
 for k in range(65):
  q=a[f'{k:02d}_positions'];ratio=np.linalg.norm(q[pairs[:,0]]-q[pairs[:,1]],axis=1)/restlen;out['all_fixed_edge_ratio_min']=min(out['all_fixed_edge_ratio_min'],float(ratio.min()));out['all_fixed_edge_ratio_max']=max(out['all_fixed_edge_ratio_max'],float(ratio.max()))
for k,row in report['witnesses'].items():out['witnesses'][k]=[{'id':q['id'],'class':int(cls[q['id']]),'source_protected':bool(np.isin(cls[q['id']],protected)),'shared_with_other_mesh':bool(np.isin(cls[q['id']],other)),'fixed':bool(fixed[q['id']])}for q in row['vertices']]
(r/'V23-SAVED-PROTECTED-WITNESS-READBACK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
