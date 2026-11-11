"""Definitions only; ROOT admits one exact three-path S4 index apply after real controls."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,stat,subprocess
P=Path(__file__).resolve().parent
ROOT=Path('/dev/shm/chicago-t1789-charles-gate-20261110');APP=ROOT/'chicago/4d'
HEAD='0a57979840bea7c37ba41ba4e24133a9510b59b9';BASE_TREE='3229a20188497ff74d9d1af51d13b886cadb1315'
BRANCH='steward/t1789-1812-loose-linen-seat-20261111';PROTECTED='refs/heads/steward/t1789-charles-woven-coat-20261110';PRIMARY='9453fa44842225bdb9de2c687cf7dca2f8a8211d'
BASE=Path('/tmp/t1789-settler-s3-source-full-gate-prep-20261111/FREEZE.json');BASE_SHA='6944115f9392d917e16bcc4fe0c1adf490bc58ec64373b09d25467118084fa41'
EXPECTED={'.github/workflows/chicago-4d-humans.yml','chicago/4d/docs/STATUS.md','chicago/4d/docs/ROADMAP.md'}
DOCS={p for p in EXPECTED if '/docs/' in p}
NATIVE={f'chicago/4d/assets/humans/{web}settler_1812.lod{lod}.glb' for web in ['', 'web/'] for lod in range(4)}|{'chicago/4d/data/humans/fixture.measure.json'}
ENV=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):assert p.is_file() and not p.is_symlink();return json.loads(p.read_bytes())
def fixed(p,h):assert re.fullmatch('[0-9a-f]{64}',h) and sha(p)==h,str(p)
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a],env=ENV).decode().strip()
def run_git(*a):subprocess.run(['git','-C',str(ROOT),*a],env=ENV,check=True)
def facts(name):
 p=ROOT/name;s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and p.resolve().is_relative_to(ROOT.resolve()),name
 h=hashlib.sha256();g=hashlib.sha1(b'blob '+str(s.st_size).encode()+b'\0')
 with p.open('rb') as stream:
  while b:=stream.read(1024*1024):h.update(b);g.update(b)
 return dict(file=name,bytes=s.st_size,sha256=h.hexdigest(),Git_mode='100755' if s.st_mode&stat.S_IXUSR else '100644',Git_blob_OID=g.hexdigest())
def baseline():
 fixed(BASE,BASE_SHA);d=load(BASE);assert d['frozen_file_count']==len(d['rows'])==301 and len({r['file'] for r in d['rows']})==301
 assert d['root']==str(ROOT) and d['branch']==BRANCH and d['index_tree']==BASE_TREE and d['protected_ref']==PROTECTED and d['protected_ref_head']==PRIMARY
 assert NATIVE<=set(r['file'] for r in d['rows']) and not NATIVE&EXPECTED
 return d
def verify(after=None):
 d=baseline();old={r['file']:r for r in d['rows']};assert EXPECTED<=set(old)
 assert git('rev-parse','HEAD')==HEAD and git('rev-parse','HEAD^{tree}')==BASE_TREE and git('branch','--show-current')==BRANCH
 assert git('rev-parse','--verify',PROTECTED)==PRIMARY
 assert not (Path(git('rev-parse','--absolute-git-dir'))/'MERGE_HEAD').exists(),'S4 is a normal single-parent source change, no pending merge'
 assert git('ls-files','-u')=='' and git('diff','--name-only')==''
 staged=git('diff','--cached','--name-status').splitlines();expected=EXPECTED if after is not None else set()
 assert {x.split('\t',1)[1] for x in staged}==expected and all(x.startswith('M\t') for x in staged)
 if after is None:assert git('status','--porcelain=v1','--untracked-files=no')=='' and git('write-tree')==BASE_TREE
 else:assert set(after)==EXPECTED
 index={}
 for line in git('ls-files','--stage','--',*sorted(old)).splitlines():
  meta,name=line.split('\t',1);mode,oid,stage=meta.split();assert stage=='0';index[name]=(mode,oid)
 assert set(index)==set(old)
 rows=[]
 for name,r in sorted(old.items()):
  actual=facts(name);assert actual['Git_mode']==r['Git_mode'] and index[name]==(actual['Git_mode'],actual['Git_blob_OID']),name
  target=after[name] if after is not None and name in after else r
  assert all(actual[k]==target[k] for k in ['bytes','sha256']),name
  if name not in expected:assert actual['Git_blob_OID']==r['Git_blob_OID'],name
  rows.append(actual)
 assert not (ROOT/'chicago/4d/changelog.d/T1789.json').exists(),'do not resurrect already folded primary entry'
 return rows

def admission(path,h):
 fixed(path,h);d=load(path);assert d['schema']=='t1789_s4_three_path_browser_source_apply_v1' and d['head']==HEAD and d['baseline301_SHA256']==BASE_SHA and d['future_tree'] is None
 assert len(d['rows'])==3 and {r['file'] for r in d['rows']}==EXPECTED
 fixed(Path(d['combined_patch']),d['combined_patch_SHA256']);fixed(Path(d['candidate_manifest']),d['candidate_manifest_SHA256'])
 for r in d['rows']:
  q=Path(r['candidate_after']);assert q.is_file() and not q.is_symlink() and q.stat().st_size==r['after_bytes'] and sha(q)==r['after_sha256']
 return d

def main(a):
 assert not (P/'APPLY-RECEIPT.json').exists()
 d=admission(a.admission,a.admission_sha256);before=verify();old={r['file']:r for r in before}
 for r in d['rows']:assert all(old[r['file']][k]==r['before_'+k] for k in ['bytes','sha256'])
 patch=d['combined_patch'];num=subprocess.check_output(['git','-C',str(ROOT),'apply','--numstat','-z',patch],env=ENV)
 assert {os.fsdecode(row.split(b'\t',2)[2]) for row in num.split(b'\0') if row}==EXPECTED
 assert git('apply','--summary',patch)==''
 run_git('apply','--check','--index',patch);suffix={n:(ROOT/n).read_bytes() for n in DOCS}
 run_git('apply','--index',patch)
 after={r['file']:dict(bytes=r['after_bytes'],sha256=r['after_sha256']) for r in d['rows']};rows=verify(after)
 for n,raw in suffix.items():assert (ROOT/n).read_bytes().endswith(raw)
 import yaml
 wf=ROOT/'.github/workflows/chicago-4d-humans.yml'
 oldwf=yaml.safe_load(subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:.github/workflows/chicago-4d-humans.yml'],env=ENV));newwf=yaml.safe_load(wf.read_bytes())
 assert {k:v for k,v in oldwf['jobs'].items() if k!='humans'}=={k:v for k,v in newwf['jobs'].items() if k!='humans'}
 oh=oldwf['jobs']['humans'];nh=newwf['jobs']['humans'];assert oh['steps'][:-3]==nh['steps'][:-1]
 assert {k:v for k,v in oh.items() if k!='steps'}=={k:v for k,v in nh.items() if k!='steps'} and nh['timeout-minutes']==45
 shell=nh['steps'][-1]['run'];assert shell.count('node tools/human_fixture.mjs')==shell.count('node tools/human_actor.mjs')==1
 assert '--user pwuser' in shell and 'readonly' in shell and 'playwright@1.56.1' in shell
 assert 'sha256:42f02d323c310069b4d54c94bd91a608966a486c3492c48ae0b1cea747ec5ca2' in shell
 subprocess.run(['bash','-n'],input=shell.encode(),check=True)
 for cmd in [['python3','tools/test_human_clothing_capture_v2.py'],['python3','tools/check_runner_images.py','--gate']]:subprocess.run(cmd,cwd=APP,env=ENV,check=True)
 run_git('diff','--cached','--check');tree=git('write-tree');assert tree!=BASE_TREE
 result=dict(status='S4_THREE_PATH_BROWSER_SOURCE_STAGED_GATE_AND_CI_PENDING',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=HEAD,index_tree=tree,branch=BRANCH,baseline301_SHA256=BASE_SHA,admission=str(a.admission),admission_SHA256=a.admission_sha256,combined_patch_SHA256=d['combined_patch_SHA256'],rows=[r for r in rows if r['file'] in EXPECTED],staged_paths=sorted(EXPECTED),deleted_paths=[],preserved_old301_outside_declared_paths=True,native8_and_fixture_unchanged=True,primary_ref_unchanged=True,docs_original_suffix_bytes_preserved=True,new_native_parents=False,production_action=False,controls={'actual_existing_workflow_checks_PASS':True,'YAML_and_shell_static_PASS':True,'Docker_or_native_browser_execution':False,'actual_container_compatibility':'PENDING_CI'},source_checkpoint_only=True,needs_final_DEV_integration=True,merge_ready=False)
 (P/'APPLY-RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--admission',type=Path,required=True);parser.add_argument('--admission-sha256',required=True);main(parser.parse_args())
