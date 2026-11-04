"""One exclusive120s curve-only authoring attempt; ROOT GO required, no runtime adoption."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.util,json,os,subprocess,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
GUARD=Path('/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
LOCK=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
POLICY='ROOT_AUTHORIZED_ONE_120S_CURRENT_AD9_CURVE_ONLY_STRIDE016_DUTY78_CUBIC129_ONE_AUTHORING_ATTEMPT'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def source(repo,mode,expected):
 def git(*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(repo),*args],timeout=15)
 head=git('rev-parse','HEAD').decode().strip();index=git('ls-files','--stage','-z');semantic=hashlib.sha256(index).hexdigest()
 assert not git('ls-files','--others','--exclude-standard','-z'),'No untracked source admission'
 assert subprocess.run(['git','--no-optional-locks','-C',str(repo),'diff','--quiet','--'],check=False).returncode==0,'Unstaged changes refused'
 if mode=='CLEAN_COMMITTED':
  assert not git('status','--porcelain').strip(),'Clean source required'
  tree=git('rev-parse','HEAD^{tree}').decode().strip()
 elif mode=='EXACT_ROOT_BOUND_STAGED_TREE':
  # ROOT supplies an already existing exact tree. Read it; never write index/tree objects.
  assert expected and expected['HEAD']==head and expected['semantic_index_sha256']==semantic
  tree=expected['TREE'];assert git('cat-file','-t',tree).strip()==b'tree'
  staged=[]
  for row in index.split(b'\0'):
   if not row:continue
   fields,path=row.split(b'\t',1);mode_i,blob,stage=fields.split();assert stage==b'0';staged.append((path,mode_i,blob))
  frozen=[]
  for row in git('ls-tree','-r','-z',tree).split(b'\0'):
   if not row:continue
   fields,path=row.split(b'\t',1);mode_i,kind,blob=fields.split();frozen.append((path,mode_i,blob))
  assert sorted(staged)==sorted(frozen),'Staged index differs from ROOT bound tree'
 else:raise AssertionError('Unknown source admission mode')
 return dict(HEAD=head,TREE=tree,APP=git('rev-parse',tree+':chicago/4d').decode().strip(),semantic_index_sha256=semantic)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--binding',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();b=load(a.binding)
 assert b['policy']==POLICY and b['approved']is True and b['template_only']is False
 assert b['authoring_phase_seconds']==120 and b['authoring_approved']is True
 assert not b['gait_acceptance']and not b['world_acceptance']and not b['runtime_adoption']
 assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(b['expires_utc'].replace('Z','+00:00'))
 assert b['originalLimits']==load(P/'ORIGINAL-UNCHANGED-LIMITS.json')
 assert b['keys']==129 and b['max_solver_calls']==516 and b['candidate_count']==1
 assert b['immutable_prior_pins']==load(P/'IMMUTABLE-PRIOR-RECEIPT-PINS.json')
 for path,pin in b['immutable_prior_pins'].items():assert sha(path)==pin
 for path,pin in b['pins'].items():assert sha(path)==pin
 for path,pin in b['helper_pins'].items():assert sha(path)==pin
 repo=Path(b['repo']).resolve();out=a.out.resolve();before=source(repo,b['source_mode'],b['source']);assert before==b['source'];assert not out.exists()
 assert out==Path(b['output_root']).resolve()and not out.is_relative_to(repo)and not a.binding.resolve().is_relative_to(repo)
 lane=LOCK.open('a+');fcntl.flock(lane,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('curve_resource_guard',GUARD);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 rb=g.snapshot();assert g.check(rb)['accepted'];out.mkdir(parents=True)
 save(out/'SOURCE-BEFORE.json',before);save(out/'RESOURCES-BEFORE.json',rb);save(out/'ACTUAL-ROOT-GO.json',b)
 prefix=out/'author';report_path=out/'AUTHORING.json';r={};cleanup={};error=None;after=None;report={}
 try:
  with(out/'author.stdout').open('xb')as stream:
   q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(P),'--timeout','120','--',sys.executable,str(P/'attempt_curve_candidate.py'),'--binding',str(out/'ACTUAL-ROOT-GO.json'),'--out',str(out)],stdout=stream,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1'))
  r=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');report=load(report_path)if report_path.exists()else{}
  completed=q.returncode==r['returncode']and r['returncode']in(0,2)and not r['timed_out']and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason']is None and cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and report.get('status')in('REFUSED_NO_CANDIDATE_LOCAL_SOLVER_OR_BUDGET','CURVE_ONLY_CANDIDATE_AUTHORED_UNQUALIFIED_REVIEW_ONLY')
 except BaseException as ex:completed=False;error=repr(ex)
 try:after=source(repo,b['source_mode'],b['source'])
 except BaseException as ex:completed=False;error=(error or'')+' source_after='+repr(ex)
 resources=g.pair(rb,g.snapshot());pins_equal=all(sha(path)==pin for path,pin in b['pins'].items())and all(sha(path)==pin for path,pin in b['helper_pins'].items())and all(sha(path)==pin for path,pin in b['immutable_prior_pins'].items());completed=completed and before==after and resources['accepted']and pins_equal
 glbs=list(out.glob('*.glb'));expected_glb=out/'UNQUALIFIED-REVIEW-ONLY-stride016-duty78-cubic129.glb';one_or_none=len(glbs)==(1 if report.get('candidate')else 0)and all(x==expected_glb for x in glbs);completed=completed and one_or_none and report.get('solver_calls',517)<=516
 closed=dict(immutable_prior_receipts_unchanged=pins_equal,source_mode=b['source_mode'],bounded_candidate_output=one_or_none,sourceEndpointLoopCheck=report.get('sourceEndpointLoopCheck'),quaternionContinuity=report.get('quaternionContinuity'),supportRisk='Two/three stance feet; balance and natural gait unqualified',status='BOUNDED_CURVE_AUTHORING_ATTEMPT_CLOSED_NO_ACCEPTANCE'if completed else'CURVE_AUTHORING_ATTEMPT_NONCOMPLETE_OR_RESOURCE_NONPASS',source_before=before,source_after=after,result=r,cleanup=cleanup,resources=resources,pins_equal=pins_equal,authoring_status=report.get('status'),candidate=report.get('candidate'),candidateSHA256=report.get('candidateSHA256'),reason=report.get('reason'),error=error,originalLimits=b['originalLimits'],all_seven_physical_predicates_requalified=False,native_qualification=False,three_original_fault_controls='UNRUN',hoof_support_domain='UNRUN',full_route='UNRUN',visual_memory='UNRUN',current_model_or_threshold_changed=False,gait_acceptance=False,world_or_visual_or_photo_acceptance=False,runtime_adoption=False)
 save(out/'CLOSED.json',closed);print(json.dumps(dict(status=closed['status'],authoring_status=closed['authoring_status'],receipt=str(out/'CLOSED.json'))));raise SystemExit(0 if completed else 1)
if __name__=='__main__':main()
