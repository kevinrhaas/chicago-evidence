from pathlib import Path
import copy,difflib,hashlib,json,re,shutil
B=Path(__file__).resolve().parent;S=B/'REGISTRATION-V2';D=B/'REGISTRATION-V3';assert not D.exists();shutil.copytree(S,D,ignore=shutil.ignore_patterns('__pycache__'))
R=D/'chicago/4d';T=R/'tools/transport/brougham';A=R/'renderers/web/transport/parked-brougham';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
side=json.loads((A/'brougham.json').read_text());near=json.loads((T/'near-contract.json').read_text());mid=json.loads((T/'mid-contract.json').read_text())
side['revision']='v18_rounded_coach_lamps_near_mid_study'
p=side['mid_provenance'];p['source_master_near_sha256']=near['raw_sha256'];p['build_receipt_sha256']=mid['build_receipt_sha256'];p['distance_lod_native_appearance_accepted']=False
p['change']='Current V18 ring16 source tessellation: 11706 triangles and314 subdivision records versus33374 triangles and480 near records. Rounded coach-lamp geometry replaces the V17 straight cages in both levels. All physical feature names,64spokes,16leaves, seven materials,42nodes,13runtime anchors and8static targets remain. The current V18 near conservative collision proxy remains authoritative; native source8 appearance and world/photographic acceptance remain unpassed.'
p['subdivision_records']={'near':mid['subdivision_records_near'],'mid':mid['subdivision_records_mid']}
p['triangles']={'near':near['triangles'],'mid':mid['triangles']}
p['appearance_history_note']='Previous V17 distance-LOD appearance acceptance is historical only and is not carried into V18. Original V17 metadata remains byte-exact in tools/transport/brougham/archive-v17/brougham.json.'
assert p['recipe']=='tools/transport/brougham/'+mid['recipe'] and p['recipe_sha256']==mid['recipe_sha256']
side['source_history_note']='Historical V10/V11/V12 notes remain lineage. Historical V17 changed only two quarter panels, with464 other parts exact; it retained six original materials and added one explicitly unidentified dark opaque material. Current V18 replaces the coach-lamp families;450 near and284 mid non-lamp occurrences retain exact V17 P/N streams. Current V18 visual/world/photographic acceptance remains pending.'
(A/'brougham.json').write_text(json.dumps(side,indent=2)+'\n')
function='''\ndef check_mid_provenance(side,near,mid):\n    """Reject stale V17 lineage and unearned appearance acceptance in active V18 metadata."""\n    p=side['mid_provenance']\n    assert side['revision']=='v18_rounded_coach_lamps_near_mid_study', 'Active V18 revision required'\n    assert p['source_master_near_sha256']==near['raw_sha256'], 'Mid provenance binds current near master'\n    assert p['build_receipt_sha256']==mid['build_receipt_sha256'], 'Mid provenance binds current MID receipt'\n    assert p['recipe']=='tools/transport/brougham/'+mid['recipe'] and p['recipe_sha256']==mid['recipe_sha256'], 'Mid provenance binds exact current recipe'\n    assert p['distance_lod_native_appearance_accepted'] is side['lod_appearance_accepted']['mid'] is False, 'V18 mid appearance remains unaccepted'\n    assert p['photographic_accepted'] is False and p['world_budget_accepted'] is False, 'V18 mid world/photo acceptance remains unpassed'\n    assert p['subdivision_records']=={'near':mid['subdivision_records_near'],'mid':mid['subdivision_records_mid']}, 'Mid provenance actual near/mid record counts'\n    assert p['triangles']=={'near':near['triangles'],'mid':mid['triangles']}, 'Mid provenance actual near/mid triangle counts'\n\n'''
s=(T/'check_mid.py').read_text();assert s.count('\ndef verify():')==1;s=s.replace('\ndef verify():',function+'\ndef verify():',1)
line="    old,ob=read(ASSET/'brougham-source.glb');new,nb=read(ASSET/'brougham-mid-source.glb');indexed,ib=read(ASSET/'brougham-mid.glb');side=json.loads((ASSET/'brougham.json').read_bytes())"
assert s.count(line)==1;s=s.replace(line,line+'\n    check_mid_provenance(side,c,mc)',1);(T/'check_mid.py').write_text(s)
near['delivery_metadata_files']['brougham.json']=sha(A/'brougham.json');near['mid_contract_sha256']=sha(T/'mid-contract.json');(T/'near-contract.json').write_text(json.dumps(near,indent=2)+'\n')
s=(T/'check_near.py').read_text();s=re.sub("EXPECTED_CONTRACT='[0-9a-f]{64}'","EXPECTED_CONTRACT='"+sha(T/'near-contract.json')+"'",s,count=1)
line="    side=json.loads((directory/'brougham.json').read_text());assert side['source_master_sha256']==c['raw_sha256'] and side['parameters_sha256']==c['source_files']['parameters.json']"
assert s.count(line)==1;s=s.replace(line,line+"\n    assert sha(here/'mid-contract.json')==c['mid_contract_sha256'], 'Exact current mid-contract binding'\n    from check_mid import check_mid_provenance\n    check_mid_provenance(side,c,json.loads((here/'mid-contract.json').read_text()))",1);(T/'check_near.py').write_text(s)
for f in [T/'check_near.py',T/'check_mid.py']:compile(f.read_text(),str(f),'exec')
changes=[];APP=Path('/workspace/chicago-waistcoat/chicago/4d')
for f in sorted(R.rglob('*')):
 if not f.is_file()or '__pycache__'in f.parts:continue
 rel=f.relative_to(R);old=APP/rel
 if not old.exists()or f.read_bytes()!=old.read_bytes():changes.append({'path':str(rel),'bytes':f.stat().st_size,'sha256':sha(f),'preimage_sha256':sha(old)if old.exists()else None})
(D/'CHANGED-FILES.json').write_text(json.dumps(changes,indent=2)+'\n')
changed_from_v2=[]
for rel in ['renderers/web/transport/parked-brougham/brougham.json','tools/transport/brougham/check_mid.py','tools/transport/brougham/check_near.py','tools/transport/brougham/near-contract.json']:
 old=S/'chicago/4d'/rel;new=R/rel;changed_from_v2.append({'path':rel,'before':sha(old),'after':sha(new)})
 (D/(Path(rel).name+'.V2-TO-V3.diff')).write_text(''.join(difflib.unified_diff(old.read_text().splitlines(True),new.read_text().splitlines(True),fromfile='V2/'+rel,tofile='V3/'+rel)))
(D/'V2-TO-V3-METADATA-FIX.json').write_text(json.dumps({'changed_files':changed_from_v2,'scope':'Correct active V18 revision and nested current mid provenance; reject stale lineage/unearned appearance acceptance; no geometry/material/LOD/runtime predicate changes','V2_and_CHECKPOINT2_preserved':True,'current_near_sha256':near['raw_sha256'],'current_mid_receipt_sha256':mid['build_receipt_sha256'],'ring16_recipe_unchanged':mid['recipe_sha256']},indent=2)+'\n')
(D/'README.md').write_text((D/'README.md').read_text()+'\n\n## V3 metadata correction\n\nActive revision is V18; nested mid provenance now binds the current V18 near master, MID receipt and unchanged ring16 recipe,314/480 records and11706/33374 triangles. Appearance acceptance is false at both nested and top-level fields. Old V17 facts remain only in explicit history/archive. Near and mid gates reject stale binding or unearned acceptance independently of file pins. V2/CHECKPOINT2 remain preserved; geometry/runtime bytes unchanged.\n')
print('Prepared V3',len(changes),'intake files; nearcontract',sha(T/'near-contract.json'),'midreceipt',mid['build_receipt_sha256'])
