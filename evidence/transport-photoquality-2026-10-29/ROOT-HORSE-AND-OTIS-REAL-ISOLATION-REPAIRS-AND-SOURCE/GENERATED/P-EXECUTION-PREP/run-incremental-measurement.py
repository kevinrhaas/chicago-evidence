#!/usr/bin/env python3
"""Prepared outside controller. Native --tool only; root owns execution gap."""
from pathlib import Path
import argparse,ast,datetime,hashlib,importlib.util,json,os,subprocess,sys,time
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
R=Path('/tmp/chicago-transport-resume-20261029');A=R/'chicago/4d';L=A/'tools/step_isolation.json'
G=Path('/tmp/human-world-motion-v4-20261030/CURRENT-UNCHANGED-SOURCE-GUARD.json')
OLD='9400c662b24909598fa6afdea2df4d3b89e7f25d';TREE='eee92b422b653b68593fbfeab11c3c4b37122247';APP='44d9d0908178710474c4003e1631dcb8f01f8f84'
INDEX='371981aa663e1a99dbeb4adc83a56992745af12f8680b8f4912a5de6f9887d34'
COMMANDS=[('tools/human_natural_idle.py','python3 tools/human_natural_idle.py --check'),('tools/test_human_natural_idle.py','python3 tools/test_human_natural_idle.py'),('tools/test_human_frame_time.mjs','node tools/test_human_frame_time.mjs'),('tools/test_human_body_ray_grid.mjs','node tools/test_human_body_ray_grid.mjs')]
E={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','GIT_TERMINAL_PROMPT':'0','GIT_OPTIONAL_LOCKS':'0'}
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);assert p.is_file() and not p.is_symlink(),p;b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b))
def load(p):return json.loads(Path(p).read_bytes())
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*args):return subprocess.check_output(['git','-c','gc.auto=0','-c','maintenance.auto=false',*args],cwd=R,env={**E,'GIT_NO_LAZY_FETCH':'1'})
def source(allow_ledger):
 assert git('rev-parse','HEAD').decode().strip()==OLD and git('branch','--show-current').decode().strip()=='steward/t1790-natural-human-idle-20261029'
 assert sha(git('ls-files','--stage','-z'))==INDEX and git('rev-parse',TREE+':chicago/4d').decode().strip()==APP
 dirty=git('diff','--name-only','-z','--').split(b'\0');dirty={x for x in dirty if x};assert dirty<=({b'chicago/4d/tools/step_isolation.json'} if allow_ledger else set()),dirty
 assert not git('ls-files','--others','--exclude-standard','-z')
 assert pin(G)['sha256']=='0cacf9f7ebc8b650b139a6ef7c9e5148180b87ed0142dbbe5bd0812ef3ea4948'
 rows=load(G)['source_files'];assert len(rows)==53 and sum(x['path'].endswith('.glb') for x in rows)==16
 for r in rows:
  p=pin(A/r['path']);assert (p['bytes'],p['sha256'])==(r['bytes'],r['sha256']),r['path']
 return dict(head=OLD,tree=TREE,app_tree=APP,semantic_index_sha256=INDEX,source53_human16_exact=True,unstaged_paths=[os.fsdecode(x) for x in sorted(dirty)],old_published_mirror_exact_claimed=False)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root-owned-measurement-go',action='store_true',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();assert out.is_relative_to(Path('/tmp')) and not out.is_relative_to(R) and not out.exists();out.mkdir(mode=0o700)
 state=dict(at=now(),status='ACTUAL_INCREMENTAL_MEASUREMENT_PENDING',commands=[],source_or_index_staged=False,full_gate_or_photo_acceptance=False,old_partial_mirror_repaired=False)
 def save():(out/'ACTUAL-INCREMENTAL-ISOLATION-REPAIR.json').write_text(json.dumps(state,indent=2)+'\n')
 save()
 try:
  cfg=load(P/'PINS.json')
  for r in cfg['files']:assert pin(r['path'])==r,r['path']
  c=load('/tmp/OTIS-ACTUAL-FULL-GATE-SHM-20261030-01/ACTUAL-WHOLE-GATE-CLOSED.json');assert c['worker']=='P' and c['native_result']['returncode']==130 and c['native_cleanup']['cleanup_complete'] and c['native_cleanup']['remaining_owned_children']==[] and c['source_index_unchanged']
  policy_path=Path(cfg['resource_policy']['path']);assert pin(policy_path)==cfg['resource_policy'];spec=importlib.util.spec_from_file_location('otis_iso_resource10',policy_path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  def resources(label):
   snap=m.snapshot();assess=m.check_snapshot(snap);(out/(label+'.json')).write_text(json.dumps(dict(snapshot=snap,assessment=assess),indent=2)+'\n');assert assess['accepted'];return snap
  before_resources=resources('RESOURCES-BEFORE');state['source_before']=source(False)
  for d in Path('/proc').iterdir():
   if not d.name.isdecimal():continue
   try:
    words=[os.fsdecode(x) for x in (d/'cmdline').read_bytes().split(b'\0') if x];exe=Path(os.readlink(d/'exe')).name
   except (FileNotFoundError,PermissionError,ProcessLookupError):continue
   assert exe not in {'chrome','chromium','headless_shell','chrome-headless-shell'},('Active browser owner',d.name)
   assert not any(Path(x).name in {'check.sh','preflight.sh','publish.sh','smoke_renderer.mjs','rederive.mjs','measure_step_isolation.mjs'} for x in words[:5]),('Active heavy/measurement owner',d.name,words[:5])
  original=L.read_bytes();assert sha(original)==cfg['original_ledger_sha256'];(out/'ORIGINAL-step_isolation.json').write_bytes(original);old=load(L);assert old['schema']==2 and all(t not in old['tools'] for t,_ in COMMANDS)
  measured=set()
  for i,(tool,declared) in enumerate(COMMANDS,1):
   source(True);sub=out/f'{i:02d}';sub.mkdir();rcfile=sub/'declared-command.rc';log=sub/'declared-command.log'
   env={**E,'BASH_ENV':str(P/'observe-declared-command.bash'),'OTIS_ISO_DECLARED_COMMAND':declared,'OTIS_ISO_COMMAND_RC':str(rcfile),'OTIS_ISO_COMMAND_LOG':str(log)}
   olddirs=set(Path('/tmp').glob('c4d-iso1-*'));started=time.monotonic();argv=['node','tools/measure_step_isolation.mjs','--tool',tool]
   try:r=subprocess.run(argv,cwd=A,env=env,capture_output=True,timeout=30)
   except subprocess.TimeoutExpired as error:
    (sub/'native-measurer.log').write_bytes((error.stdout or b'')+(error.stderr or b''));state['commands'].append(dict(tool=tool,argv=argv,timed_out=True,seconds=time.monotonic()-started));save();raise
   (sub/'native-measurer.log').write_bytes(r.stdout+r.stderr);row=dict(tool=tool,argv=argv,declared_command=declared,native_measurer_returncode=r.returncode,seconds=time.monotonic()-started,timed_out=False);state['commands'].append(row);save();assert r.returncode==0
   assert rcfile.is_file() and rcfile.read_text().strip()=='0',('Actual native declared command failed or never exited',tool)
   assert log.is_file() and log.stat().st_size>0
   newdirs=set(Path('/tmp').glob('c4d-iso1-*'))-olddirs;assert len(newdirs)==1,newdirs;raw=next(iter(newdirs))/'probe.jsonl';probe=raw.read_bytes();(sub/'probe.jsonl').write_bytes(probe)
   records=[json.loads(line) for line in probe.splitlines() if line.strip()];matched=[]
   for record in records:
    argv0=(record.get('argv') or [''])[0];key='tools/'+argv0.split('tools/')[-1] if 'tools/' in argv0 else str(Path(argv0).relative_to(R)) if Path(argv0).is_absolute() and Path(argv0).is_relative_to(R) else argv0
    if key==tool:matched.append(record)
   assert matched and all(x['wrote']==[] for x in matched),('Tool did not produce clean actual native probe row',tool,matched)
   actual=load(L);measured.add(tool);assert set(actual['tools'])==set(old['tools'])|measured
   for k,v in old['tools'].items():assert actual['tools'][k]==v,('Preexisting measured row changed',k)
   for k in measured:assert actual['tools'][k]=={'wrote':[],'wrote_ignored':[]},('Unexpected actual measured row',k,actual['tools'][k])
   assert {k:v for k,v in actual.items() if k not in {'tools','measured'}}=={k:v for k,v in old.items() if k not in {'tools','measured'}}
   row.update(actual_declared_returncode=0,declared_log=pin(log),original_probe=pin(raw),preserved_probe=pin(sub/'probe.jsonl'),actual_matching_probe_records=matched,measured_row=actual['tools'][tool],ledger_after=pin(L));save()
  state['source_after']=source(True);after_resources=resources('RESOURCES-AFTER');pair=m.check_pair(before_resources,after_resources);assert pair['accepted'];state.update(at=now(),status='PASS_FOUR_ACTUAL_NATIVE_INCREMENTAL_MEASUREMENTS_LEDGER_UNSTAGED',resource10_pair=pair,original_ledger_sha256=sha(original),actual_ledger_after=pin(L),all_preexisting_rows_unchanged=True,actual_measured_tools=sorted(measured),published_mirror_restore='PENDING_NATIVE_PUBLISH_OWNED_SLOT',new_full_gate='PENDING_AFTER_NEW_SOURCE_FREEZE');save();print(json.dumps(state));return 0
 except BaseException as error:
  state.update(at=now(),status='STOPPED_ACTUAL_PARTIAL_MEASUREMENTS_AND_SOURCE_RETAINED',error=repr(error));save();raise
if __name__=='__main__':raise SystemExit(main())
