"""Root-authorized scoped repair: new cards dirs, preserved body passes and prior red."""
from pathlib import Path
import hashlib,json,subprocess,datetime
P=Path(__file__).parent;W=Path('/tmp/wolf-poster-source-20261103');read=lambda p:json.loads(Path(p).read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();H='3f3e0bfcc99aad5d358fa8520da764fbe0aa68ff'
old=read(P/'FINAL-HELPER-PEER-REVIEW.json');new=read(P/'FINAL-CARDS-V3-PEER-REVIEW.json');assert new['root_approved']
for doc in [old,new]:
 for n,h in doc['hashes_exact'].items():assert sha(P/n)==h,('unreviewed helper drift',n)
assert subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD']).decode().strip()==H;assert not subprocess.check_output(['git','-C',str(W),'status','--porcelain'])
lease=read(P/'GPU-LEASE.json');assert lease['root_explicit_release']and lease['source_root']==str(W)
bodies=[]
for viewport in ['desktop','mobile']:
 O=P/'current-ui'/(viewport+'-body');d=read(O/'CLOSURE.json');plan=read(O/'PLAN.json');assert d['error']is None and d['source_publication_helpers_exact']and d['source']['HEAD']==H and d['status']=='JAIL_CURRENT_'+viewport.upper()+'-BODY_PASS';bodies.append(plan['full_publication_map_sha256'])
assert bodies[0]==bodies[1];assert read(P/'current-ui/desktop-cards/CLOSURE.json')['status']=='NOT_QUALIFIED','Original fixture red must remain preserved'
assert read(P/'current-ui-cards-v2/desktop-cards/CLOSURE.json')['status']=='NOT_QUALIFIED','Second inspector-selector fixture red must remain preserved'
steps=[('desktop-cards-v3',['python',str(P/'run_cards_leg_v3.py'),'--viewport','desktop','--leg','cards'],P/'current-ui-cards-v3/desktop-cards/CLOSURE.json'),('mobile-cards-v3',['python',str(P/'run_cards_leg_v3.py'),'--viewport','mobile','--leg','cards'],P/'current-ui-cards-v3/mobile-cards/CLOSURE.json'),('mobile-native3',['python',str(P/'run_native3_leg.py'),'--viewport','mobile'],P/'current-native3/mobile/CLOSURE.json'),('desktop-native3',['python',str(P/'run_native3_leg.py'),'--viewport','desktop'],P/'current-native3/desktop/CLOSURE.json')]
C=P/'runtime-controller-v3';C.mkdir(exist_ok=True);done=[]
for tag,cmd,closure in steps:
 rec=C/(tag+'-OUTER-REAPER.json');log=C/(tag+'.log')
 if closure.exists():
  d=read(closure);assert d['error']is None and d['source_publication_helpers_exact']and d['status'].endswith('_PASS'),('Existing failed v3 closure; no automatic retry',tag)
  rr=read(rec);assert rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup'];done.append(tag);continue
 assert not rec.exists()and not log.exists(),('Existing started leg needs inspection',tag)
 assert lease==read(P/'GPU-LEASE.json'),'lease changed'
 with log.open('xb')as f:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(rec),'--','timeout','--signal=TERM','--kill-after=15s','600s',*cmd],cwd=P,stdout=f,stderr=subprocess.STDOUT)
 rr=read(rec);assert r.returncode==rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup'],('Actual failed leg preserved',tag,rr)
 d=read(closure);assert d['error']is None and d['source_publication_helpers_exact']and d['status'].endswith('_PASS');done.append(tag);(C/'PROGRESS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed':done,'last':tag,'preserved_body_passes':['desktop396.35','mobile222.00'],'preserved_original_cards_fixture_red':True,'one_foreground_leg_only':True,'no_implicit_retry':True},indent=2)+'\n');print('PROPERLY CLOSED',tag,flush=True);break
else:print('All pending4 already properly closed; final cross-version ledger/root review still required',flush=True)
