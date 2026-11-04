#!/usr/bin/env python3
"""One ROOT-admitted current staged-source technical browser fixture; no source writes."""
import argparse,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,d):Path(p).write_text(json.dumps(d,indent=2)+'\n')
def git(root,*args,check=True):return subprocess.run(['git','--no-optional-locks','-C',str(root),*args],check=check,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'),timeout=30)
def source(root,expected):
 assert set(expected)=={'HEAD','TREE','APP','semantic_index_sha256'}
 for k in ['HEAD','TREE','APP']:assert re.fullmatch('[a-f0-9]{40}',expected[k])
 assert git(root,'rev-parse','HEAD').stdout.decode().strip()==expected['HEAD']
 assert git(root,'rev-parse','--verify','MERGE_HEAD',check=False).returncode!=0
 assert git(root,'diff','--quiet',check=False).returncode==0,'Unstaged source differs'
 assert not git(root,'ls-files','--others','--exclude-standard','-z').stdout,'Untracked source'
 rows=[]
 for raw in git(root,'ls-tree','-r','-z',expected['TREE']).stdout.split(b'\0'):
  if raw:
   info,path=raw.split(b'\t',1);mode,kind,oid=info.split();rows.append((path,mode+b' '+oid+b' 0\t'+path+b'\0'))
 staged=b''.join(row for _,row in sorted(rows))
 assert git(root,'ls-files','--stage','-z').stdout==staged,'Exact staged TREE admission differs'
 assert hashlib.sha256(staged).hexdigest()==expected['semantic_index_sha256']
 assert git(root,'rev-parse',expected['TREE']+':chicago/4d').stdout.decode().strip()==expected['APP']
 return dict(expected)
def main():
 p=argparse.ArgumentParser(description='ROOT-bound real stopped driver look rendered fixture. Original600s outer and120s complete perviewport deadlines. No town/walk-up/trustedUI/photo claim.')
 p.add_argument('--root',type=Path,required=True);p.add_argument('--go',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 root=a.root.resolve();app=root/'chicago/4d';out=a.out.resolve();assert not out.is_relative_to(root);out.mkdir(exist_ok=False)
 go=load(a.go);manifest=load(D/'MANIFEST.json')
 assert go['approved']is True and go['policy']=='ROOT_AUTHORIZED_ACTUAL_STAGED_DRIVER_LOOK_TECHNICAL_FIXTURE'
 assert go['manifest_sha256']==sha(D/'MANIFEST.json')
 for name,h in manifest['fixture_pins'].items():assert sha(D/name)==h,(name,'fixture changed')
 assert go['asset_pins']==manifest['expected_child8_pins']
 for name,h in go['asset_pins'].items():assert sha(app/name)==h,(name,'actual selected asset differs')
 before=source(root,go['source']);save(out/'SOURCE-BEFORE.json',before)
 lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('guard','/workspace/.cloud-setup/transport-current-20261103/resource_guard.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 resources_before=g.snapshot();assert g.check(resources_before)['accepted']
 cfg=dict(go,browser=manifest['browser']);save(out/'CONFIG.json',cfg)
 prefix=out/'rendered-look';command=['node',str(D/'run_browser.cjs'),str(app),str(out/'browser'),str(out/'CONFIG.json')]
 env=dict(os.environ,PW_EXECUTABLE=manifest['browser'],PLAYWRIGHT_BROWSERS_PATH='/workspace/.cloud-setup/transport-browser141-20261103');env.pop('CHICAGO_TICKETS_DIR',None)
 error=None;result=cleanup=resources=report=after=None
 try:
  assert subprocess.check_output([manifest['browser'],'--version'],timeout=5).decode().strip()=='Chromium 141.0.7390.37'
  q=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(app),'--timeout','600','--',*command],env=env,stdout=(out/'SUPERVISOR.stdout').open('xb'),stderr=subprocess.STDOUT)
  result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');resources=g.pair(resources_before,g.snapshot());report=load(out/'browser/REPORT.json')
  assert q.returncode==result['returncode']==0 and not result['timed_out']
  assert result['requested_timeout_seconds']==result['effective_timeout_seconds']==600 and result['timeout_override_reason']is None
  assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted']
  assert report['passed']and len(report['runs'])==8 and report['browser_closed']and report['server_closed']
  for row in report['runs']:
   assert row['passed']and row['actual']['changed_render_pixels']>0 and row['actual']['max_head_world_delta']>.001
   assert row['viewport_elapsed_seconds']<=120
  after=source(root,go['source']);assert before==after
 except BaseException as e:error=repr(e)
 try:after=source(root,go['source'])
 except BaseException as e:error=(error+'; 'if error else'')+'source_after: '+repr(e)
 if resources is None:resources=g.pair(resources_before,g.snapshot())
 save(out/'CLOSED.json',dict(status='ACTUAL_NATIVE_DRIVER_LOOK_RENDERED_FIXTURE_PASS'if error is None else'NONPASS',error=error,source_before=before,source_after=after,manifest_sha256=sha(D/'MANIFEST.json'),ROOT_GO_sha256=sha(a.go),result=result,cleanup=cleanup,resources=resources,report=report,full_world_pass=False,photographic_acceptance=False))
 print(json.dumps(dict(passed=error is None,out=str(out),error=error)));return 0 if error is None else 1
if __name__=='__main__':raise SystemExit(main())
