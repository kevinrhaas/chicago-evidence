"""Exact source-ID join/expand feasibility, outside only; no Blender authoring."""
import collections,copy,hashlib,json,math,sys
from pathlib import Path
def audit(mesh):
 old=copy.deepcopy(mesh);ids=mesh['source_vertex_indices'];groups=collections.defaultdict(list)
 for i,sid in enumerate(ids):groups[sid].append(i)
 order=list(groups);new_index={sid:i for i,sid in enumerate(order)};old_to_new=[new_index[sid]for sid in ids]
 positions=[];weights=[]
 for sid in order:
  members=groups[sid];first=members[0]
  if any(mesh['positions_m'][i]!=mesh['positions_m'][first]or mesh['weights'][i]!=mesh['weights'][first]for i in members):raise ValueError('join would merge different positions/weights')
  positions.append(copy.deepcopy(mesh['positions_m'][first]));weights.append(copy.deepcopy(mesh['weights'][first]))
 faces=[[old_to_new[i]for i in face]for face in mesh['triangles']]
 if any(len(set(face))<3 for face in faces):raise ValueError('join collapses triangle')
 # Blender UV coordinates must move from POINT to CORNER domain explicitly.
 corners=[{'vertex':old_to_new[i],'uv':copy.deepcopy(mesh['uvs'][i]),'old_vertex':i}for face in mesh['triangles']for i in face]
 original=[(mesh['positions_m'][i],mesh['uvs'][i],mesh['weights'][i])for face in mesh['triangles']for i in face]
 expanded=[(positions[c['vertex']],c['uv'],weights[c['vertex']])for c in corners]
 if expanded!=original:raise ValueError('oriented triangle corner attributes changed')
 if mesh!=old:raise ValueError('input mutated')
 return {'split_vertices':len(ids),'source_vertices':len(order),'duplicate_source_groups':sum(len(v)>1 for v in groups.values()),'triangles':len(faces),'triangle_corner_count':len(corners),'position_weight_exact_duplicate_checks':True,'oriented_corner_position_uv_weight_expansion_exact':True,'input_unchanged':True,'not_proven':'BPy normals, smooth/sharp fans, morph export, source/web buffer parity, decimation, loaded motion or visible seam quality'}
def main(paths):
 reports=[]
 for p in paths:
  data=Path(p).read_bytes();d=json.loads(data);reports.append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'meshes':[audit(m)for m in d['meshes']]})
 return reports
if __name__=='__main__':print(json.dumps(main(sys.argv[1:]),indent=2))
