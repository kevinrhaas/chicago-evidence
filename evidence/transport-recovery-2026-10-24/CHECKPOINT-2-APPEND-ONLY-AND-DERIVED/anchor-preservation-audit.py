#!/usr/bin/env python3
"""Read-only Git/source audit; emits evidence JSON and never edits application files."""
import datetime,difflib,json,math,subprocess
from pathlib import Path
REPO=Path('/workspace/chicago');APP=REPO/'chicago/4d'
OLD='e5ed3ff6e5a62f70ae8a1c3c0c88c29e977cf02a';LATEST='origin/dev'
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
def show(ref,p):return git('show',ref+':chicago/4d/'+p)
def paths(*args):return set(git(*args).decode().splitlines())
changed=paths('diff','--name-only',OLD,LATEST,'--','chicago/4d')
working=paths('diff','--name-only',LATEST,'--','chicago/4d')
old=show(LATEST,'docs/LIBERTIES.md');now=(APP/'docs/LIBERTIES.md').read_bytes();lines=old.splitlines(keepends=True)
starts=[i for i,l in enumerate(lines) if l.startswith(b'### ')];bounds=list(zip(starts,starts[1:]+[len(lines)]))
glessner=[(i,j) for i,j in bounds if b'glessner' in lines[i].lower()]
missing_glessner=[lines[i].decode().strip() for i,j in glessner if b''.join(lines[i:j]) not in now]
base=show(OLD,'docs/LIBERTIES.md').splitlines(keepends=True);sm=difflib.SequenceMatcher(a=base,b=lines,autojunk=False)
incoming=[x for op,i,j,k,l in sm.get_opcodes() if op in ('insert','replace') for x in lines[k:l]]
it=iter(now.splitlines(keepends=True));raw_all=all(any(n==line for n in it) for line in lines)
a=json.loads(show(LATEST,'data/liberties.json'))['liberties'];b=json.loads((APP/'data/liberties.json').read_bytes())['liberties'];a={x['id']:x for x in a};b={x['id']:x for x in b}
ids=[k for k in a if 'glessner' in k.lower()]
scene=json.loads((APP/'data/scenes/1835.json').read_bytes());oldscene=json.loads(show(OLD,'data/scenes/1835.json'));oldanchors={x['id']:x for x in oldscene['anchors']};anchors={x['id']:x for x in scene['anchors']};point=anchors['western_hotel_yard']
horse=json.loads((APP/'data/transport/parked/standing-horses.json').read_bytes())['scenes']['1835'][0];east,north=horse['at_local_enu_m']
roadmap=(APP/'docs/ROADMAP.md').read_bytes();invalid=None
try:roadmap.decode('utf8')
except UnicodeDecodeError as exc:invalid=hex(roadmap[exc.start])
reading=json.loads((APP/'data/render/anchor_ground_reading.json').read_bytes())
result={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'working_head':git('rev-parse','HEAD').decode().strip(),'comparison_dev':git('rev-parse',LATEST).decode().strip(),'handover_base':OLD,'latestdev_changed_paths':len(changed),'latestdev_paths_unchanged':len(changed-working),'expected_shared_overlap_paths':sorted(changed&working),'glessner_markdown_blocks':len(glessner),'missing_or_changed_glessner_markdown_blocks':missing_glessner,'incoming_liberty_added_or_replaced_lines':len(incoming),'incoming_liberty_lines_preserved_byte_exact':all(x in now for x in incoming),'all_old_liberty_raw_lines_retained_in_order':raw_all,'glessner_json_ids':len(ids),'changed_glessner_json_ids':[k for k in ids if b.get(k)!=a[k]],'missing_old_liberty_json_ids':sorted(a.keys()-b.keys()),'changed_existing_liberty_json_ids':[k for k in a if k in b and a[k]!=b[k]],'prior_anchor_count':len(oldanchors),'prior_anchors_preserved':all(anchors[k]==v for k,v in oldanchors.items()),'new_anchor_ids':sorted(anchors.keys()-oldanchors.keys()),'non_anchor_scene_fields_preserved':{k:v for k,v in scene.items() if k!='anchors'}=={k:v for k,v in oldscene.items() if k!='anchors'},'new_anchor_yaw_declared':point['yaw_deg'],'new_anchor_yaw_to_horse':math.degrees(math.atan2(east-point['local_e'],north-point['local_n']))%360,'saved_anchor_reading_totals':reading['totals'],'roadmap_original_invalid_utf8_byte':invalid,'limitations':['This is a read-only preservation/data audit, not full preflight, browser, native, photographic or DEV delivery acceptance.','Owner-tail may be running; recapture after final source corrections and settling.']}
print(json.dumps(result,indent=2))
