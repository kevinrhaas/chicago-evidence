"""Advance exactly one pre-reviewed foreground leg; never retry failed or running work."""
from pathlib import Path
import hashlib,json,subprocess,datetime,os
P=Path(__file__).parent;review=json.loads((P/'FINAL-HELPER-PEER-REVIEW.json').read_bytes());lease=json.loads((P/'GPU-LEASE.json').read_bytes());assert lease['root_explicit_release']and lease['source_root']=='/tmp/wolf-poster-source-20261103'
for n,h in review['hashes_exact'].items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,('unreviewed helper drift',n)
steps=[('desktop-body',['python',str(P/'run_ui_leg.py'),'--viewport','desktop','--leg','body'],P/'current-ui/desktop-body/CLOSURE.json'),('mobile-body',['python',str(P/'run_ui_leg.py'),'--viewport','mobile','--leg','body'],P/'current-ui/mobile-body/CLOSURE.json'),('desktop-cards',['python',str(P/'run_ui_leg.py'),'--viewport','desktop','--leg','cards'],P/'current-ui/desktop-cards/CLOSURE.json'),('mobile-cards',['python',str(P/'run_ui_leg.py'),'--viewport','mobile','--leg','cards'],P/'current-ui/mobile-cards/CLOSURE.json'),('mobile-native3',['python',str(P/'run_native3_leg.py'),'--viewport','mobile'],P/'current-native3/mobile/CLOSURE.json'),('desktop-native3',['python',str(P/'run_native3_leg.py'),'--viewport','desktop'],P/'current-native3/desktop/CLOSURE.json')]
C=P/'runtime-controller';C.mkdir(exist_ok=True);done=[]
for tag,cmd,closure in steps:
 rec=C/(tag+'-OUTER-REAPER.json');log=C/(tag+'.log')
 if closure.exists():
  d=json.loads(closure.read_bytes());assert d['error']is None and d['source_publication_helpers_exact']and d['status'].endswith('_PASS'),('Existing failed closure preserved; no retry',tag,d)
  rr=json.loads(rec.read_bytes());assert rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup'],('Prior outer not cleanly reaped',tag)
  done.append(tag);continue
 assert not rec.exists()and not log.exists(),('Existing started leg requires inspection, not retry',tag)
 assert lease==json.loads((P/'GPU-LEASE.json').read_bytes()),'lease changed'
 with log.open('xb')as f:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(rec),'--','timeout','--signal=TERM','--kill-after=15s','600s',*cmd],cwd=P,stdout=f,stderr=subprocess.STDOUT)
 rr=json.loads(rec.read_bytes());assert r.returncode==rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup'],('Actual leg failed; preserved, no retry',tag,rr)
 d=json.loads(closure.read_bytes());assert d['error']is None and d['source_publication_helpers_exact']and d['status'].endswith('_PASS'),('Actual closure failed',tag,d)
 done.append(tag);(C/'PROGRESS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed':done,'last':tag,'one_foreground_leg_only':True,'no_retry':True},indent=2)+'\n');print('PROPERLY CLOSED',tag,flush=True);break
else:
 (C/'ALL6-CLOSED.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed':done,'status':'ALL6_ACTUAL_PROPERLY_CLOSED_PASS','root_visual_review':'PENDING','no_complete_photo_match_claim':True},indent=2)+'\n');print('ALL6 already properly closed',flush=True)
