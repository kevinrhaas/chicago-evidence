# SPDX-License-Identifier: GPL-3.0-or-later
"""Light independent active hierarchy/pose and receipt audit; no generation/SAT sweep."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import numpy as np
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('subject',P/'test_carriage_c02_door.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# Explicit composition: parent translation, Y rotation hinge, nonuniform scaled child.
nodes=[{'translation':[3,4,5],'children':[1]}, {'translation':[.5,.25,-.75],'children':[2]}, {'translation':[.2,.3,.4],'scale':[2,3,4]}]
parents={1:0,2:1};angle=.6;c,s=math.cos(angle),math.sin(angle)
pose=np.array([[c,0,s,.5],[0,1,0,.25],[-s,0,c,-.75],[0,0,0,1.]])
p=np.array([.1,.2,.3]);actual=m.transformed(p,m.world(nodes,parents,2,{1:pose}))
scaled=p*np.array([2,3,4])+np.array([.2,.3,.4])
expected=np.array([c*scaled[0]+s*scaled[2],scaled[1],-s*scaled[0]+c*scaled[2]])+np.array([.5,.25,-.75])+np.array([3,4,5])
assert np.max(np.abs(actual-expected))<1e-12
# Synthetic selected-scene picks only its own active nodes; cycles/multiparents refuse.
parents,active=m.active_hierarchy({'scene':1,'scenes':[{'nodes':[0]},{'nodes':[1]}],'nodes':[{}, {'children':[2]},{}]})
assert active=={1,2} and parents=={2:1}
for nodes,roots in [([{'children':[1]},{'children':[0]}],[0]),([{'children':[2]},{'children':[2]},{}],[0,1])]:
 try:m.active_hierarchy({'scenes':[{'nodes':roots}],'nodes':nodes})
 except ValueError:pass
 else:raise AssertionError('Invalid active hierarchy accepted')
control=json.loads((P/'controls.json').read_text());assert hashlib.sha256((P/'test_carriage_c02_door.py').read_bytes()).hexdigest()==control['new_checker_sha256']
for name,fixture in control['fixtures'].items():assert hashlib.sha256(Path(fixture['path']).read_bytes()).hexdigest()==fixture['sha256']
rows=[]
for row in control['rows']:
 receipt=json.loads((P/row['receipt']).read_text())
 if row['checker']=='old-checker.py':assert row['returncode']==0
 else:
  assert receipt['passed']==row['expected_success']
  if row['expected_success']:
   assert len(receipt['rows'])==15 and receipt['actual_active_moving_triangle_count']==424
   assert all(r['triangle_intersections_including_contact']==0 for r in receipt['rows'])
  else:assert receipt.get('error') and receipt['passed'] is False
 rows.append({'name':row['name'],'checker':row['checker'],'stage':receipt.get('stage'),'passed':receipt.get('passed'),'error':receipt.get('error')})
output={'scope':'independent lightweight actual-function composition/selectedscene/hierarchy refusal and existing receipts/hash audit; no generator/browser/full15angle rerun','composition_max_error_m':float(np.max(np.abs(actual-expected))),'controls_receipts':rows,'passed':True}
(P/'independent-canary-receipt.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'passed':True,'composition_max_error_m':output['composition_max_error_m'],'audited_receipts':len(rows)}))
