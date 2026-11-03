"""Read scoped receipts only; no browser, source or API changes."""
from pathlib import Path
import sys,json
paths=[Path(p)for p in sys.argv[1:]];assert paths
rows=[json.loads(p.read_text())for p in paths];sources={(r['source_before']['HEAD'],r['source_before']['TREE'],r['source_before']['APP'])for r in rows};assert len(sources)==1,'Different source identities require explicit review, never implicit proof retargeting'
expected={(y,v,s)for y in['1835','1904']for v in['desktop','mobile']for s in['A','B','C']};seen={};predicates=set()
for p,r in zip(paths,rows):
 k=(r['scene'],r['viewport'],r['scope']);assert k not in seen,'Duplicate case receipt';seen[k]=str(p)
 assert r['status']=='ACTUAL_CURRENT_PUBLISHED_WORLD_SCOPE_PASS'and r['source_before']==r['source_after']and r['resources']['accepted']and r['cleanup']['cleanup_complete']and not r['cleanup']['remaining_owned_children']
 predicates.update(r['predicate_ids'])
missing=sorted(expected-set(seen));complete=not missing and len(predicates)==16
print(json.dumps({'status':'ALL_FOUR_PUBLISHED_YEAR_VIEWPORT_COMPOSITES_ALL16_SCOPED_PREDICATES_PASS'if complete else'PARTIAL_SCOPED_PROOF_NOT_ALL_CASES','source':list(sources)[0],'case_count':len(seen),'missing':missing,'predicate_count':len(predicates),'all_in_one_case_PASS':False,'full_native_smoke_or_photo_PASS':False,'receipts':seen and list(seen.values())},indent=2))
