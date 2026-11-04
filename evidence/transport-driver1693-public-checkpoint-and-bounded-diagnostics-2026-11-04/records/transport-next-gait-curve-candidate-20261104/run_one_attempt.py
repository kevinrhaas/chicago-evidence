"""One exclusive120s curve-only authoring attempt; ROOT GO required, no runtime adoption."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.util,json,os,subprocess,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
GUARD=Path('/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
LOCK=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
POLICY='ROOT_AUTHORIZED_ONE_120S_CURRENT_AD9_CURVE_ONLY_STRIDE_020_ATTEMPT'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def source(repo):
 def git(*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(repo),*args],timeout=15)
 assert not git('status','--porcelain').strip(),'Run only on clean receiving checkout'
 return dict(HEAD=git('rev-parse','HEAD').decode().strip(),TREE=git('rev-parse','HEAD^{tree}').decode().strip(),APP=git('rev-parse','HEAD:chicago/4d').decode().strip(),semantic_index_sha256=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest())
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--binding',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();b=load(a.binding)
 assert b['policy']==POLICY and b['approved']is True and b['template_only']is False
 assert b['authoring_phase_seconds']==120 and b['authoring_approved']is True
 assert not b['gait_acceptance']and not b['world_acceptance']and not b['runtime_adoption']
 assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(b['expires_utc'].replace('Z','+00:00'))
 assert b['originalLimits']==load(P/'ORIGINAL-UNCHANGED-LIMITS.json')
 for path,pin in b['pins'].items():assert sha(path)==pin
 for path,pin in b['helper_pins'].items():assert sha(path)==pin
 repo=Path(b['repo']).resolve();out=a.out.resolve();before=source(repo);assert before==b['source'];assert not out.exists()
 assert out==Path(b['output_root']).resolve()and not out.is_relative_to(repo)and not a.binding.resolve().is_relative_to(repo)
 lane=LOCK.open('a+');fcntl.flock(lane,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('curve_resource_guard',GUARD);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 rb=g.snapshot();assert g.check(rb)['accepted'];out.mkdir(parents=True)
 save(out/'SOURCE-BEFORE.json',before);save(out/'RESOURCES-BEFORE.json',rb);save(out/'ACTUAL-ROOT-GO.json',b)
 prefix=out/'author';report_path=out/'AUTHORING.json';r={};cleanup={};error=None;after=None;report={}
 try:
  with(out/'author.stdout').open('xb')as stream:
   q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(P),'--timeout','120','--',sys.executable,str(P/'attempt_curve_candidate.py'),'--binding',str(a.binding),'--out',str(out)],stdout=stream,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1'))
  r=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');report=load(report_path)if report_path.exists()else{}
  completed=q.returncode==r['returncode']and r['returncode']in(0,2)and not r['timed_out']and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason']is None and cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and report.get('status')in('REFUSED_NO_CANDIDATE_LOCAL_SOLVER_OR_BUDGET','CURVE_ONLY_CANDIDATE_AUTHORED_UNQUALIFIED_REVIEW_ONLY')
 except BaseException as ex:completed=False;error=repr(ex)
 try:after=source(repo)
 except BaseException as ex:completed=False;error=(error or'')+' source_after='+repr(ex)
 resources=g.pair(rb,g.snapshot());pins_equal=all(sha(path)==pin for path,pin in b['pins'].items())and all(sha(path)==pin for path,pin in b['helper_pins'].items());completed=completed and before==after and resources['accepted']and pins_equal
 closed=dict(status='BOUNDED_CURVE_AUTHORING_ATTEMPT_CLOSED_NO_ACCEPTANCE'if completed else'CURVE_AUTHORING_ATTEMPT_NONCOMPLETE_OR_RESOURCE_NONPASS',source_before=before,source_after=after,result=r,cleanup=cleanup,resources=resources,pins_equal=pins_equal,authoring_status=report.get('status'),candidate=report.get('candidate'),candidateSHA256=report.get('candidateSHA256'),reason=report.get('reason'),error=error,originalLimits=b['originalLimits'],all_seven_physical_predicates_requalified=False,native_qualification=False,three_original_fault_controls='UNRUN',hoof_support_domain='UNRUN',full_route='UNRUN',visual_memory='UNRUN',current_model_or_threshold_changed=False,gait_acceptance=False,world_or_visual_or_photo_acceptance=False,runtime_adoption=False)
 save(out/'CLOSED.json',closed);print(json.dumps(dict(status=closed['status'],authoring_status=closed['authoring_status'],receipt=str(out/'CLOSED.json'))));raise SystemExit(0 if completed else 1)
if __name__=='__main__':main()
