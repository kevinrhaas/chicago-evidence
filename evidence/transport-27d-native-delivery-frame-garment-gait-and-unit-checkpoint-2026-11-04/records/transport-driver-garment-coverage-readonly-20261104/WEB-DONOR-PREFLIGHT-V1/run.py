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
 p=argparse.ArgumentParser(description='ROOT-only finite native CPU WEB0/WEB3 garment donor preflight. Exactly8 read-only GLBs. Original120s supervisor; no browser/GPU/generation.')
 p.add_argument('--root',type=Path,required=True);p.add_argument('--go',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 root=a.root.resolve();app=root/'chicago/4d';out=a.out.resolve();assert not out.is_relative_to(root)and not out.is_relative_to(D)
 go=load(a.go);m=load(D/'MANIFEST.json');assert go['approved']is True and go['policy']=='ROOT_AUTHORIZED_WEB_LOD0_GARMENT_DONOR_NATIVE_PREFLIGHT_ONLY';assert go['manifest_sha256']==sha(D/'MANIFEST.json')
 for n,h in m['fixture_pins'].items():assert sha(D/n)==h,(n,'fixture changed')
 for n,h in m['input_pins'].items():assert sha(n)==h,(n,'input changed')
 before=source(root,go['source'])
 lock=open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 spec=importlib.util.spec_from_file_location('guard','/workspace/.cloud-setup/transport-current-20261103/resource_guard.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 rb=g.snapshot();assert g.check(rb)['accepted'];out.mkdir(exist_ok=False);save(out/'SOURCE-BEFORE.json',before)
 cfg=dict(go,app=str(app),cases=m['cases'],input_pins=m['input_pins'],native_canvas_module=m['native_canvas_module']);save(out/'CONFIG.json',cfg)
 prefix=out/'native-preflight';env=dict(os.environ);env.pop('CHICAGO_TICKETS_DIR',None);error=None;result=cleanup=resources=report=after=None
 try:
  q=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(D),'--timeout','120','--','node',str(D/'preflight.mjs'),str(out/'CONFIG.json'),str(out/'native')],env=env,stdout=(out/'SUPERVISOR.stdout').open('xb'),stderr=subprocess.STDOUT)
  result=load(str(prefix)+'.result.json');cleanup=load(str(prefix)+'.cleanup.json');resources=g.pair(rb,g.snapshot());report=load(out/'native/RESULT.json')
  assert q.returncode==result['returncode']==0 and not result['timed_out'];assert result['requested_timeout_seconds']==result['effective_timeout_seconds']==120 and result['timeout_override_reason']is None
  assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']and resources['accepted'];assert report['passed']and len(report['cases'])==2 and report['native_resources_disposed']
  assert all(r['web0_donor_exact_eligible']for r in report['cases']);after=source(root,go['source']);assert before==after
 except BaseException as e:error=repr(e)
 try:after=source(root,go['source'])
 except BaseException as e:error=(error+'; 'if error else'')+'source_after: '+repr(e)
 if resources is None:resources=g.pair(rb,g.snapshot())
 save(out/'CLOSED.json',dict(status='NATIVE_WEB_DONOR_PREFLIGHT_COMPLETE_NO_ASSET_GENERATED'if error is None else'NONPASS_DO_NOT_GENERATE',error=error,source_before=before,source_after=after,manifest_sha256=sha(D/'MANIFEST.json'),ROOT_GO_sha256=sha(a.go),result=result,cleanup=cleanup,resources=resources,report=report,asset_generation=False,browser_or_GPU=False,production_or_photo_acceptance=False))
 print(json.dumps(dict(passed=error is None,out=str(out),error=error)));return 0 if error is None else 1
if __name__=='__main__':raise SystemExit(main())
