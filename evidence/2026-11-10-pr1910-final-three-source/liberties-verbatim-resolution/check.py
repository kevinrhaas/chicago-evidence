from pathlib import Path
import sys,json,copy,hashlib
R=Path('/tmp/chicago-west-wicket-20261109/chicago/4d');sys.path.insert(0,str(R/'tools'));import compile_liberties as c;import validate as v
structures={p.stem:json.loads(p.read_text()) for p in (R/'data/structures').glob('*.json')};known={k:d.get('name','') for k,d in structures.items()};raw=(R/'docs/LIBERTIES.md').read_bytes();entries,problems=c.parse(raw.decode(),known);assert not problems,problems
receipt=json.loads(Path('/tmp/nov10-b3-liberty-resolution/VERBATIM-MOVE-AND-SUCCESSOR-RECEIPT.json').read_text());idx={e['id']:e for e in entries}
for item in receipt['mapping']:
 assert idx[item['old_id']]['section']=='resolved';assert any(f['label']=='Resolved' for f in idx[item['old_id']]['fields']);body=Path('/tmp/nov10-b3-liberty-resolution',item['old_id']+'-ORIGINAL-VERBATIM.md').read_bytes();assert raw[item['new_start_byte']:item['new_original_body_end_byte']]==body
for old,new in [('L45','L-second-fort-garden-fence-metrics-2388'),('L47','L-second-fort-palisade-fabric-metrics-2388')]:
 e=idx[new];assert e['section']!='resolved';actual=['.'.join((x['structure'],x['phase'],x['aspect'])) for x in e['covers']];assert sorted(actual)==sorted(receipt['standing_successor_Covers'][old])
 for token in actual:
  sid,phase,_,key=token.split('.');d=next(p for p in structures[sid]['phases'] if p['id']==phase)['form'][key];assert d['confidence']=='reconstructed'
 for f in e['fields']:
  if f['label']=='Sources':
   import re
   for sid in re.findall(r'`([^`]+)`',f['text']):assert (R/'data/sources'/f'{sid}.json').is_file()
# The actual validator's complete forward/reverse coverage logic, scoped to these3
# records with only matching claims. No validator code or assertion is altered.
ids={'fort_dearborn_garrison_garden','fort_dearborn_palisade','fort_dearborn_big_barn'};scoped=[]
for e in entries:
 cs=[x for x in e.get('covers',[]) if x.get('domain')!='terrain' and any(x.get('structure')==sid or (x.get('structure','').endswith('*') and sid.startswith(x['structure'][:-1])) for sid in ids)]
 if cs:
  q=copy.deepcopy(e);q['covers']=cs;scoped.append(q)
rep=v.Report();consumed=v.archetype_consumed(rep);v.check_liberties_coverage({sid:structures[sid] for sid in ids},{'liberties':scoped},rep,consumed=consumed)
assert not rep.errors,rep.errors
print('PASS actual readonly parser:',len(entries),'entries;3oldResolved with exact verbatim bodies;2standing successors exact4+6R Covers;realSources resolve')
print('PASS actual validate.check_liberties_coverage on3real target records:',len(scoped),'matching claim entries;',len(rep.errors),'errors;',len(rep.warnings),'warnings')
for n in rep.notes:print(n)
