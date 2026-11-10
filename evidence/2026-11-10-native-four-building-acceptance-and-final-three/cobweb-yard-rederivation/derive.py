from pathlib import Path
import sys,json,hashlib
F=Path('/tmp/chicago-west-wicket-20261109/chicago/4d');O=Path('/tmp/nov10-cobweb-complete/yard-rederive');sys.path.insert(0,str(F/'tools'))
import generate_woodpiles as g
import check_structure_clearance as c
before=g.load(g.OUT);lots,refused,counts=g.build();after=g.record(lots,refused,counts);text=json.dumps(after,indent=1,ensure_ascii=False)+'\n';(O/'town_woodpiles.json').write_text(text)
old={r['structure_id']:r for r in before['lots']};new={r['structure_id']:r for r in after['lots']};changed={sid:{'before':old.get(sid),'after':new.get(sid)} for sid in sorted(set(old)|set(new)) if old.get(sid)!=new.get(sid)}
layers=c.layer_files();baseline=c.judge(c.survey(layers=layers));layers['yard/town_woodpiles.json']=after;fixed=c.judge(c.survey(layers=layers))
receipt={'qualification':'Official full generator g.build/g.record against actual integrated full sidecars and inputs; output external only, no hand coordinates or waiver','original_path':str(g.OUT),'before_sha256':hashlib.sha256(g.OUT.read_bytes()).hexdigest(),'after_sha256':hashlib.sha256(text.encode()).hexdigest(),'counts':counts,'changed_lots':changed,'baseline_faults':baseline[0],'after_faults':fixed[0],'after_stale_rulings':fixed[2]};(O/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('CHANGED LOTS',list(changed));print('BASELINE FAULTS',baseline[0]);print('AFTER FAULTS',fixed[0]);print('STALE RULINGS',fixed[2]);assert not fixed[0] and not fixed[2]
