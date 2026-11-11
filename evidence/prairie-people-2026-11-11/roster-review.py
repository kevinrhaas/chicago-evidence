import csv, json, hashlib, subprocess
from collections import Counter
from pathlib import Path
root=Path('/workspace/chicago/chicago/4d')
out=Path('/workspace/chicago-evidence/evidence/prairie-people-2026-11-11')
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
catalog=json.loads((root/'data/humans/prairie_1904.json').read_text())['people']
coverage={p['person_id']:p for p in json.loads((root/'docs/RESEARCH/prairie-portraits-3546/search-coverage.json').read_text())['people']}
people={}
for file in sorted((root/'data/residents_1904/households').glob('*.json')):
 hh=json.loads(file.read_text())
 for p in hh['persons']:
  assert p['id'] not in people
  people[p['id']]=(hh,p,file.relative_to(root))
rows=[]
for entry in catalog:
 pid=entry['person']; hh,p,file=people[pid]; born=p.get('born') or {}; search=coverage[pid]
 rows.append({'person_id':pid,'name':p['name'],'household_id':hh['id'],'household':hh['name'],'scene_status':entry['status'],'model_age_1904':entry.get('age_1904',''),'birth_record':born.get('value',''),'birth_grade':born.get('confidence',''),'birth_sources':'; '.join(born.get('sources',[])),'birth_note':born.get('note',''),'portrait_status':entry.get('portrait',''),'canonical_card':p.get('own_card',''),'role':entry.get('role',''),'appearance_grade':entry.get('casting_grade',''),'existing_sources':'; '.join(p.get('sources',[])),'book_search_hits':len(search.get('book_hits',[])),'museum_search_hits':len(search.get('museum_hits',[])),'commons_search_status':search.get('commons',{}).get('status',''),'card_source_file':f'https://github.com/kevinrhaas/chicago/blob/{sha}/chicago/4d/{file}'})
rows.sort(key=lambda r:(r['household'].casefold(),r['name'].casefold()))
assert len(rows)==445 and len({r['household_id'] for r in rows})==71
csv_path=out/'roster-review.csv'
with csv_path.open('w',newline='',encoding='utf-8') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
summary={'source_commit':sha,'generated_by':'roster-review.py (copied alongside this index)','entries':len(rows),'households':71,'statuses':dict(Counter(r['scene_status'] for r in rows)),'csv_sha256':hashlib.sha256(csv_path.read_bytes()).hexdigest(),'note':'model_age_1904 is the scene casting age, including disclosed reconstructions. Only birth_record, birth_grade, birth_sources and birth_note describe the retained birth evidence. Missing portrait means no portrait identified in the bounded searches, not that no photograph exists. Search hits are leads, not identity or source acceptance.'}
(out/'roster-review.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
