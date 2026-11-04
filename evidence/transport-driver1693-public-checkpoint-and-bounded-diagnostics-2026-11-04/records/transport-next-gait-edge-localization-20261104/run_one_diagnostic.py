"""One exclusive 120s read-only native edge localization, ROOT GO required."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.util,json,os,subprocess,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
GUARD=Path('/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
LOCK=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def source(repo):
 def git(*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(repo),*args],timeout=15)
 assert not git('status','--porcelain').strip(),'Run only after current commit/push, on a clean receiving checkout'
 return dict(HEAD=git('rev-parse','HEAD').decode().strip(),TREE=git('rev-parse','HEAD^{tree}').decode().strip(),APP=git('rev-parse','HEAD:chicago/4d').decode().strip(),semantic_index_sha256=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest())
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--binding',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();b=load(a.binding)
 assert b['policy']=='ROOT_AUTHORIZED_ONE_120S_HORSE_EDGE_REGION_DIAGNOSTIC_NO_GENERATION'and b['approved']is True and b['template_only']is False
 assert b['native_phase_seconds']==120 and b['diagnostic_only']is True and not b['authoring_approved']and not b['gait_acceptance']and not b['world_acceptance']
 assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(b['expires_utc'].replace('Z','+00:00'))
 assert b['originalLimits']==load(P/'ORIGINAL-UNCHANGED-LIMITS.json')
 for path,pin in b['pins'].items():assert sha(path)==pin
 for path,pin in b['helper_pins'].items():assert sha(path)==pin
 repo=Path(b['repo']);before=source(repo);assert before==b['source'];assert not a.out.exists()
 lane=LOCK.open('a+');fcntl.flock(lane,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('edge_region_resource_guard',GUARD);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 rb=g.snapshot();assert g.check(rb)['accepted'];a.out.mkdir(parents=True)
 save(a.out/'SOURCE-BEFORE.json',before);save(a.out/'RESOURCES-BEFORE.json',rb)
 prefix=a.out/'native';report_path=a.out/'EDGE-REGIONS.json';r={};cleanup={};error=None;after=None;report={}
 try:
  with(a.out/'native.stdout').open('xb')as stream:
   q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(P),'--timeout','120','--','node',str(P/'localize_native_edges.mjs'),str(a.binding),str(report_path)],stdout=stream,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  r=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');report=load(report_path)if report_path.exists()else{}
  okay=q.returncode==r['returncode']==0 and not r['timed_out']and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason']is None and cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and report.get('status')=='DIAGNOSTIC_COMPLETE_SAME_INPUT_NATIVE_EDGE_LOCALIZATION_NOT_GAIT_ACCEPTANCE'and report.get('completed_frames')==1154
 except BaseException as ex:okay=False;error=repr(ex)
 try:after=source(repo)
 except BaseException as ex:okay=False;error=(error or'')+' source_after='+repr(ex)
 resources=g.pair(rb,g.snapshot());pins_equal=all(sha(path)==pin for path,pin in b['pins'].items())and all(sha(path)==pin for path,pin in b['helper_pins'].items());okay=okay and before==after and resources['accepted']and pins_equal
 known=Path(str(report_path)+'.KNOWN-EXTREMA-FIRST.json')
 closed=dict(status='ACTUAL_READONLY_NATIVE_EDGE_REGION_DIAGNOSTIC_COMPLETE_NOT_GAIT_ACCEPTANCE'if okay else'ACTUAL_READONLY_NATIVE_EDGE_REGION_DIAGNOSTIC_NONCOMPLETE_OR_NONPASS',source_before=before,source_after=after,result=r,cleanup=cleanup,resources=resources,pins_equal=pins_equal,completed_frames=report.get('completed_frames',0),report=str(report_path),known_four_original_extrema_path=str(known)if known.exists()else None,error=error,originalLimits=b['originalLimits'],all_seven_physical_predicates_requalified=False,source_generation_or_stride_authoring=False,current_model_or_threshold_changed=False,world_or_visual_or_photo_acceptance=False)
 save(a.out/'CLOSED.json',closed);print(json.dumps(dict(status=closed['status'],receipt=str(a.out/'CLOSED.json'))));raise SystemExit(0 if okay else 1)
if __name__=='__main__':main()
