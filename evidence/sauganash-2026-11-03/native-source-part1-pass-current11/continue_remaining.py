"""Continue native parts 2-4 only after the already-running owned part1 retry closes PASS."""
from pathlib import Path
import json,subprocess,time,os
P=Path(__file__).parent;assert not(P/'REMAINING-CONTROLLER.json').exists();(P/'REMAINING-CONTROLLER.json').write_text(json.dumps({'pid':os.getpid(),'dependency':'PART1-LINK-FIXTURE-ENV-RETRY-RESULT.json','source_commit_authorization':'NONE; only sequential native parts2-4 after part1 PASS','started':time.time()},indent=2)+'\n');deadline=time.monotonic()+650
while not(P/'PART1-LINK-FIXTURE-ENV-RETRY-RESULT.json').exists():
 assert time.monotonic()<deadline,'Part1 retry did not close within own deadline'
 time.sleep(1)
r=json.loads((P/'PART1-LINK-FIXTURE-ENV-RETRY-RESULT.json').read_bytes());assert r['status']=='NATIVE_SOURCE_PART_PASS'and r['source11_and_staged_postimages_exact'];rr=r['reaper'];assert rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup']and rr['interrupted_signal']is None
for part in range(2,5):
 print('Starting native source part',part,flush=True);x=subprocess.run(['python',str(P/'run_part.py'),str(part)]);assert x.returncode==0,('Native part failed',part,x.returncode)
print('ALL FOUR NATIVE PARTS CLOSED PASS; source authored commit still pending',flush=True)
(P/'SOURCE4-CLOSED.json').write_text(json.dumps({'status':'ALL_FOUR_NATIVE_SOURCE_PARTS_CLOSED_PASS','base':r['head'],'parts':['PART1-LINK-FIXTURE-ENV-RETRY-RESULT.json','PART2-RESULT.json','PART3-RESULT.json','PART4-RESULT.json'],'source_authored_commit':'PENDING'},indent=2)+'\n')
