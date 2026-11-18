from pathlib import Path
import json,subprocess,hashlib,os
root=Path('/workspace/chicago'); snapshot=Path(os.environ['CITATION_ROOT']); head=os.environ['CITATION_COMMIT']
index='data/sidecars/1835/sources/index.json';cur=json.loads((snapshot/index).read_text());old=json.loads(subprocess.check_output(['git','show','ae259f9a5ddd4e79e1c82cd40e5084d6dcf42290:chicago/4d/'+index],cwd=root));oldids={s['source_id'] for s in old['sources']};wanted={s['id'] for s in json.loads(Path('/tmp/t3654-citation-proof/inputs.json').read_text())['new_sources']};new=[s for s in cur['sources'] if s['source_id'] in wanted];assert len(new)==11
paths=[index,'data/sidecars/1871/sources/uses.json','data/context/1871.json','data/context/1871/kit.json']+[f"data/sidecars/1835/sources/{s['source_id']}.json" for s in new]+['walk/js/'+x for x in ['main.js','scene-loader.js','city-context.js','popup.js','sources.js','citations.js','inspect-sources.js','reader-text.js','evidence.js','liberties.js']]
bindings={}
for p in paths:
 src='chicago/4d/'+ ('renderers/web/'+p.removeprefix('walk/') if p.startswith('walk/') else p)
 actual=(snapshot/p).read_bytes();committed=subprocess.check_output(['git','show',head+':'+src],cwd=root)
 assert actual==committed,(p,'does not match source commit')
 bindings[p]={'source':src,'sha256':hashlib.sha256(actual).hexdigest()}
rows=[]
uses=json.loads((snapshot/'data/sidecars/1871/sources/uses.json').read_text())['uses']
for row in new:
 d=json.loads((snapshot/f"data/sidecars/1835/sources/{row['source_id']}.json").read_text());rows.append({'id':row['source_id'],'citation':row['citation'],'use':uses[row['source_id']],'source':d['source'],'edges':len(d['edges'])})
kit=json.loads((snapshot/'data/context/1871/kit.json').read_text())
result={'tested_source_commit':head,'candidate_origin':'Fresh root-authorized immutable snapshot; all catalog/runtime files below independently match tested_source_commit','snapshot':str(snapshot),'bindings':bindings,'new_sources':rows,'context_citation_ids':[c['source_id'] for c in kit['citations']]}
source_index_bytes=subprocess.check_output(['git','show',head+':chicago/4d/data/sidecars/1871/index.json'],cwd=root)
published_index=json.loads((snapshot/'data/sidecars/1871/index.json').read_text())
boot=published_index.pop('boot')
assert published_index==json.loads(source_index_bytes) and published_index['structures']==[]
assert boot=={'shared':'sidecars/1871/boot/shared.json','dir':'sidecars/1871/boot/','per_part':50}
assert json.loads((snapshot/'data'/boot['shared']).read_text())=={'values':[]}
assert sorted(p.name for p in (snapshot/'data'/boot['dir']).iterdir())==['shared.json']
result['publication_bindings']={p:hashlib.sha256((snapshot/p).read_bytes()).hexdigest() for p in ['data/sidecars/1871/index.json','data/'+boot['shared']]}
result['empty_boot']={'descriptor':boot,'structures':0,'shared_values':0,'parts':0,'source_index_sha256':hashlib.sha256(source_index_bytes).hexdigest(),'packer_source_sha256':hashlib.sha256(subprocess.check_output(['git','show',head+':chicago/4d/tools/pack_boot_sidecars.mjs'],cwd=root)).hexdigest(),'binding':'Published index equals committed source index plus its boot descriptor; the empty shared table and absence of parts are published outputs, bound separately by hash.'}
Path('/tmp/t3654-citation-proof-after/inputs.json').write_text(json.dumps(result,indent=2)+'\n');print('Bound',len(paths),'inputs and',len(rows),'new sources to',head)
