# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import json,sys,time
import numpy as np
P=Path(__file__).parent;sys.path.insert(0,'/workspace/shared/horse-v2-gear-v5-pair-next');import official_fit_predicates as pred
s=json.loads((P/'trial1/head-source-surface.json').read_text());positions=(np.asarray(s['positions'],dtype='<f4').astype(float)+[0,1.88,.8]).astype('<f4').astype(float);faces=np.array(s['faces']);tris=positions[faces];lo=tris.min(1);hi=tris.max(1);hits=[];started=time.time()
for i,a in enumerate(tris):
 ix=np.flatnonzero(np.all(hi>=a.min(0)-1e-8,axis=1)&np.all(lo<=a.max(0)+1e-8,axis=1)&(np.arange(len(tris))>i))
 for j in ix:
  if len(set(faces[i])&set(faces[j]))>=2:continue
  if pred.sat(a,tris[j]):
   cross=pred.proper(a,tris[j])
   if cross is not None:hits.append({'a':i,'b':int(j),'owners':[s['tags'][i],s['tags'][j]],'crossing':cross,'points':[a.tolist(),tris[j].tolist()]})
report={'pass':not hits,'strict_non_edge_adjacent_self_crossings':len(hits),'witnesses':hits,'elapsed_s':time.time()-started,'scope':'Actualfloat32sourceunifiedheadworldrest;sharededgesexclude adjacency,sharedverticesstillchecked;sourceclosed-topologyproofseparate;posed/emittedselfproofpending'};(P/'source-self.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='witnesses'});assert not hits
