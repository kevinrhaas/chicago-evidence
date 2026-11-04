"""Exclusive single120s fixed24 source feasibility attempt; fresh ROOT GO required."""
from pathlib import Path
import argparse,datetime,fcntl,hashlib,importlib.util,json,os,subprocess,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
GUARD=Path('/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
LOCK=Path('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock')
POLICY='ROOT_AUTHORIZED_ONE_120S_CURRENT_AD9_STRIDE016_DUTY78_FIXED24_SOURCE_PROBES_ONLY'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def source(repo):
 def git(*args):return subprocess.check_output(['git','--no-optional-locks','-C',str(repo),*args],timeout=15)
 assert not git('status','--porcelain').strip(),'Fresh current clean commit required, including after driver1693 integration'
 return dict(HEAD=git('rev-parse','HEAD').decode().strip(),TREE=git('rev-parse','HEAD^{tree}').decode().strip(),APP=git('rev-parse','HEAD:chicago/4d').decode().strip(),semantic_index_sha256=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest())
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--binding',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();b=load(a.binding)
 assert b['policy']==POLICY and b['approved']is True and b['template_only']is False
 assert b['source_phase_seconds']==120 and b['source_probe_approved']is True and b['probe_count']==24 and b['max_solver_calls']==96
 assert not b['generation_approved']and not b['gait_acceptance']and not b['world_acceptance']and not b['runtime_adoption']
 assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(b['expires_utc'].replace('Z','+00:00'))
 assert b['originalLimits']==load(P/'ORIGINAL-UNCHANGED-LIMITS.json')and b['immutable_negative_pins']==load(P/'IMMUTABLE-STRIDE020-NEGATIVE-PINS.json')
 def pins_equal():return all(sha(path)==pin for section in ('pins','helper_pins','immutable_negative_pins')for path,pin in b[section].items())
 assert pins_equal();assert sha(P/'FIXED-24-PROBES.json')==b['schedule_sha256']
 repo=Path(b['repo']).resolve();out=a.out.resolve();before=source(repo);assert before==b['source'];assert not out.exists()
 assert out==Path(b['output_root']).resolve()and not out.is_relative_to(repo)and not a.binding.resolve().is_relative_to(repo)
 lane=LOCK.open('a+');fcntl.flock(lane,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('source_feasibility_resource_guard',GUARD);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 rb=g.snapshot();assert g.check(rb)['accepted'];out.mkdir(parents=True)
 save(out/'SOURCE-BEFORE.json',before);save(out/'RESOURCES-BEFORE.json',rb);frozen_binding=out/'ACTUAL-ROOT-GO.json';save(frozen_binding,b)
 prefix=out/'source';report_path=out/'FEASIBILITY.json';r={};cleanup={};error=None;after=None;report={}
 try:
  with(out/'source.stdout').open('xb')as stream:
   q=subprocess.run([sys.executable,str(SUP),'--prefix',str(prefix),'--cwd',str(P),'--timeout','120','--',sys.executable,str(P/'probe_duty_feasibility.py'),'--binding',str(frozen_binding),'--out',str(out)],stdout=stream,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1'))
  r=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');report=load(report_path)if report_path.exists()else{}
  completed=q.returncode==r['returncode']and r['returncode']in(0,2)and not r['timed_out']and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason']is None and cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and report.get('status')in('REFUSED_FIXED_PROBE_SOURCE_CONSTRAINT','REFUSED_FIXED_PROBE_BUDGET','FIXED24_SOURCE_PROBES_COMPLETE_NOT_GAIT_OR_NATIVE_ACCEPTANCE')and report.get('generation')is False and report.get('completed_probes',25)<=24 and report.get('completed_solver_calls',97)<=96
 except BaseException as ex:completed=False;error=repr(ex)
 try:after=source(repo)
 except BaseException as ex:completed=False;error=(error or'')+' source_after='+repr(ex)
 resources=g.pair(rb,g.snapshot());same_pins=pins_equal();no_glb=not list(out.rglob('*.glb'));completed=completed and before==after and resources['accepted']and same_pins and no_glb and load(frozen_binding)==b
 closed=dict(status='FIXED_SOURCE_FEASIBILITY_ATTEMPT_CLOSED_NOT_ACCEPTANCE'if completed else'FIXED_SOURCE_FEASIBILITY_ATTEMPT_NONCOMPLETE_OR_RESOURCE_NONPASS',source_before=before,source_after=after,result=r,cleanup=cleanup,resources=resources,pins_equal=same_pins,immutable_stride020_negative_unchanged=same_pins,source_probe_status=report.get('status'),completed_probes=report.get('completed_probes',0),completed_solver_calls=report.get('completed_solver_calls',0),reason=report.get('reason'),error=error,originalLimits=b['originalLimits'],no_GLB_emitted=no_glb,dense_or_native_all_seven_requalified=False,three_original_fault_controls='UNRUN',endpoint_loops='UNRUN',hoof_support_domain='UNRUN',full_route='UNRUN',visual_memory='UNRUN',support_risk='Two/three stance feet instead of three; stability and natural gait unqualified',current_model_or_threshold_changed=False,gait_acceptance=False,world_or_visual_or_photo_acceptance=False,runtime_adoption=False)
 save(out/'CLOSED.json',closed);print(json.dumps(dict(status=closed['status'],source_probe_status=closed['source_probe_status'],receipt=str(out/'CLOSED.json'))));raise SystemExit(0 if completed else 1)
if __name__=='__main__':main()
