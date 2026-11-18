from pathlib import Path
import json,subprocess,hashlib
root=Path('/workspace/chicago'); snapshot=Path('/tmp/t3654-shadow-candidate'); head='3f81ece88f0d57d26063d786e6bccd9658ab89c3'
index='data/sidecars/1835/sources/index.json';cur=json.loads((snapshot/index).read_text());old=json.loads(subprocess.check_output(['git','show','ae259f9a5ddd4e79e1c82cd40e5084d6dcf42290:chicago/4d/'+index],cwd=root));oldids={s['source_id'] for s in old['sources']};new=[s for s in cur['sources'] if s['source_id'] not in oldids]
paths=[index,'data/sidecars/1871/sources/uses.json','data/context/1871.json','data/context/1871/kit.json']+[f"data/sidecars/1835/sources/{s['source_id']}.json" for s in new]+['walk/js/'+x for x in ['main.js','city-context.js','popup.js','sources.js','citations.js','inspect-sources.js','reader-text.js','evidence.js','liberties.js']]
bindings={}
for p in paths:
 src='chicago/4d/'+ ('renderers/web/'+p.removeprefix('walk/') if p.startswith('walk/') else p)
 actual=(snapshot/p).read_bytes();committed=subprocess.check_output(['git','show',head+':'+src],cwd=root)
 assert actual==committed,(p,'does not match 3f81')
 bindings[p]={'source':src,'sha256':hashlib.sha256(actual).hexdigest()}
rows=[]
uses=json.loads((snapshot/'data/sidecars/1871/sources/uses.json').read_text())['uses']
for row in new:
 d=json.loads((snapshot/f"data/sidecars/1835/sources/{row['source_id']}.json").read_text());rows.append({'id':row['source_id'],'citation':row['citation'],'use':uses[row['source_id']],'source':d['source'],'edges':len(d['edges'])})
kit=json.loads((snapshot/'data/context/1871/kit.json').read_text())
result={'tested_source_commit':head,'candidate_origin':'92ac published mirror with only city-context.js patched to exact 3f81 bytes; all catalog/runtime files below independently match 3f81','snapshot':str(snapshot),'bindings':bindings,'new_sources':rows,'context_citation_ids':[c['source_id'] for c in kit['citations']]}
Path('/tmp/t3654-citation-proof/inputs.json').write_text(json.dumps(result,indent=2)+'\n');print('Bound',len(paths),'inputs and',len(rows),'new sources to',head)
