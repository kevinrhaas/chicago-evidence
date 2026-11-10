from pathlib import Path
import re,json,hashlib
R=Path('/tmp/chicago-west-wicket-20261109/chicago/4d');P=Path('/tmp/nov10-b3-liberty-resolution');f=R/'docs/LIBERTIES.md';old=f.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();originals={};ranges=[]
for lid in ['L45','L47','L225']:
 m=re.search(rb'^### '+lid.encode()+rb' [^\r\n]*',old,re.M);assert m
 nxt=re.search(rb'^#{2,3} ',old[m.end():],re.M);end=m.end()+nxt.start() if nxt else len(old);raw=old[m.start():end];originals[lid]=raw;ranges.append((m.start(),end,lid));(P/(lid+'-ORIGINAL-VERBATIM.md')).write_bytes(raw)
assert not re.search(rb'^### L-second-fort-(garden-fence-metrics|palisade-fabric-metrics)-2388 ',old,re.M)
successors={'L45':'L-second-fort-garden-fence-metrics-2388','L47':'L-second-fort-palisade-fabric-metrics-2388'}
resolved={
'L45':'2026-11-10, T-2388. Only the historical planting-omission claim is settled: the existing flora layer already supplies the young fruit trees and currant bushes through data/flora/plantings/fort_company_garden_1835.json, while this fence record’s attested planting description is record_only. This is not new garden vegetation in this source group; its species/count/row liberties remain L-fruit-trees-1835-2809. All four reconstructed fence metrics and the survey-symbol interpretation remain standing in L-second-fort-garden-fence-metrics-2388. The original text above is preserved as history; no fence dimension is resolved by moving it.',
'L47':'2026-11-10, T-2388. Only the former posterns-omission claim represented by the original Covers token is settled at the source level: the attested descriptive posterns boolean is now record_only, and the separate consumed gate controls select two bounded side openings. Genuine native output and actual interaction/street review are still pending and required before merge; no built-geometry acceptance is asserted here. The six reconstructed picket, main-gate and bastion metrics, together with all prior source and medium-resolution qualifications, remain standing in L-second-fort-palisade-fabric-metrics-2388. The separate reconstructed postern seats, width and make remain admitted by L-second-fort-side-posterns-2388. No blanket settlement of the stockade fabric is intended.',
'L225':'2026-11-10, T-2388. The source-level refusal/absence declaration is superseded: the named cupola occurrence remains attested and record_only, while the consumed cupola_shape and three metric controls now select a bounded boarded body and pyramid cap. Their shape, seat and dimensions remain standing liberties in L-second-fort-big-barn-cupola-2388. The original omission rationale above is kept verbatim. Actual genuine native output, picture comparison and published street review remain pending and must qualify before merge; this line does not claim that the pending mesh has already been built or accepted.'}
base=old
for start,end,lid in sorted(ranges,reverse=True):base=base[:start]+base[end:]
resolved_head=re.search(rb'^## Resolved\r?\n',base,re.M);assert resolved_head
next_section=re.search(rb'^## ',base[resolved_head.end():],re.M);assert next_section;insert_at=resolved_head.end()+next_section.start()
moved=b''.join(originals[lid]+('**Resolved:** '+resolved[lid]+'\n\n\n').encode() for lid in ['L45','L47','L225']);intermediate=base[:insert_at]+moved+base[insert_at:]
covers={}
for lid,omit in [('L45','form.planting'),('L47','form.posterns')]:
 line=re.search(rb'^\*\*Covers:\*\* (.*)$',originals[lid],re.M).group(1);tokens=[x.decode() for x in re.findall(rb'`([^`]+)`',line)];covers[lid]=[x for x in tokens if not x.endswith('.'+omit)]
assert len(covers['L45'])==4 and len(covers['L47'])==6
new1='''### L-second-fort-garden-fence-metrics-2388 — the standing worm-fence dimensions from historical L45

**Decision:** Retain the current reconstructed garden fence at 1.30 m high, three rail courses, 3.0 m panel length and 0.90 m panel offset. The Harrison plan’s zigzag boundary supports the inferred worm-fence interpretation, not those measurements. Every height, course count, panel rhythm and zigzag dimension remains this project’s choice.

The full historical argument is preserved verbatim in resolved L45; only its obsolete planting-omission statement has been settled. The existing flora layer already supplies the garden planting, whose own source/selection liberties remain separate. Neither that vegetation nor this successor adds a new garden or changes the fence’s geometry. The first-fort pre-1812 garden passage remains excluded as evidence for this second-fort garden.

**Covers:** '''+', '.join('`'+x+'`' for x in covers['L45'])+'''.

**Sources:** `harrison_1830_river_mouth` for the labelled plot and boundary convention; `kinzie_waubun_1856` for the separately recorded company-garden planting, not fence dimensions.

**How to resolve:** A contemporary measured fence description, timber return or detailed plan identifying this garden could replace the chosen dimensions. Existing planting does not measure the fence.

**Ticket:** T-2388; successor to L45’s four continuing fence admissions.
**Recorded:** 2026-11-10.
'''
new2='''### L-second-fort-palisade-fabric-metrics-2388 — the six standing stockade metrics from historical L47

**Decision:** Retain the current reconstructed picket height 3.70 m, picket width 0.24 m, picket spacing 0.30 m, main-gate width 3.60 m, bastion length 7.0 m and bastion projection 3.20 m. The written high-picket description and plan arrangement do not measure any of these six controls. The wall’s visible scale, transparency, large-gate aperture and corner-work proportions therefore remain declared inventions.

Historical L47, including its 2026-08-28 measured print-resolution discussion, is preserved verbatim in Resolved. Only its posterns-omission claim is superseded at source level; that move does not resolve any picket, main-gate or bastion metric or promote a coarse lithograph rhythm to a timber measurement. The two reconstructed side-postern seats and narrow leaves have their own standing admission, L-second-fort-side-posterns-2388, and still require actual native and interaction review. The attested north/south large-gate disposition is not replaced by those additional small openings.

**Covers:** '''+', '.join('`'+x+'`' for x in covers['L47'])+'''.

**Sources:** `kinzie_waubun_1856`, `andreas_1884_v1`, `harrison_1830_river_mouth`, for the described stockade and plan arrangement; none supplies these six exact dimensions.

**How to resolve:** A contemporary quartermaster return, repair estimate, engineer’s report or measured plan for the 1816–1836 work could replace the invented timber, gate and bastion controls. New postern geometry does not settle their dimensions.

**Ticket:** T-2388; successor to L47’s six continuing fabric admissions.
**Recorded:** 2026-11-10.
'''
append=('\n\n'+new1+'\n\n'+new2).encode();new=intermediate+append;f.write_bytes(new)
# Prove all old evidence and all unrelated bytes survive: undo only the explicit insertion/removals.
assert intermediate[:insert_at]+intermediate[insert_at+len(moved):]==base
for lid,raw in originals.items():assert new.count(raw)==1
receipt={'protocol':'LIBERTIES intro: preserve verbatim, move under Resolved AND add Resolved line. Mixed entries get standing successors for all continuing R admissions. Explicit root authorization limits this exception to L45/L47/L225.','old_file_sha256':sha(old),'new_file_sha256':sha(new),'all_unrelated_old_bytes_exact':True,'standing_successor_Covers':covers,'mapping':[],'native_status':'SOURCE IMPLEMENTED; genuine new native and visitor qualification pending, required before merge. Garden flora already existed; no new planting claim.'}
for start,end,lid in ranges:
 raw=originals[lid];newpos=new.index(raw);receipt['mapping'].append({'old_id':lid,'old_start_byte':start,'old_end_byte':end,'old_bytes':len(raw),'old_body_sha256':sha(raw),'new_start_byte':newpos,'new_original_body_end_byte':newpos+len(raw),'new_original_body_sha256':sha(new[newpos:newpos+len(raw)]),'new_section':'Resolved','verbatim_exact':True,'standing_successor':successors.get(lid,'L-second-fort-big-barn-cupola-2388 (already standing)'),'settlement_scope':'only planting omission' if lid=='L45' else 'only posterns omission, source-level/native pending' if lid=='L47' else 'cupola refusal/absence declaration, source-level/native pending'})
(P/'VERBATIM-MOVE-AND-SUCCESSOR-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('Moved3originalentries byte-verbatim; addednarrowResolvedlines; appended2standingsuccessors coveringexact4+6Rmetrics; allotheroldbytespreserved')
