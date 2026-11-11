"""Definitions only; ROOT admits one exact four-path S3 index apply after real controls."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,stat,subprocess
P=Path(__file__).resolve().parent
ROOT=Path('/dev/shm/chicago-t1789-charles-gate-20261110');APP=ROOT/'chicago/4d'
HEAD='c9990d8b32517612a94e339a98bd5700436b5689';BASE_TREE='1dced78ea49426b9f4c4b9f52ef79db47f06facf'
BRANCH='steward/t1789-1812-loose-linen-seat-20261111';PROTECTED='refs/heads/steward/t1789-charles-woven-coat-20261110';PRIMARY='9453fa44842225bdb9de2c687cf7dca2f8a8211d'
BASE=Path('/tmp/t1789-settler-s2-source-full-gate-prep-20261111/FREEZE.json');BASE_SHA='97a2d891a72d62898170279ace4c2832fe76dd36e4719c84a3fd68e408f7133f'
EXPECTED={'chicago/4d/tools/human_clothing_capture_v2.py','chicago/4d/tools/test_human_clothing_capture_v2.py','chicago/4d/docs/STATUS.md','chicago/4d/docs/ROADMAP.md'}
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
 assert not (Path(git('rev-parse','--absolute-git-dir'))/'MERGE_HEAD').exists(),'S3 is a normal single-parent source change, no pending merge'
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
 fixed(path,h);d=load(path);assert d['schema']=='t1789_s3_four_path_source_apply_v1' and d['head']==HEAD and d['baseline301_SHA256']==BASE_SHA and d['future_tree'] is None
 assert len(d['rows'])==4 and {r['file'] for r in d['rows']}==EXPECTED
 fixed(Path(d['combined_patch']),d['combined_patch_SHA256']);assert Path(d['combined_patch']).is_file() and not Path(d['combined_patch']).is_symlink() and Path(d['combined_patch']).stat().st_size<=8*1024**2
 for c in d['components']:fixed(Path(c['patch']),c['patch_SHA256']);fixed(Path(c['manifest']),c['manifest_SHA256'])
 assert len(d['components'])==2
 for r in d['rows']:
  assert type(r['before_bytes']) is int and type(r['after_bytes']) is int and r['before_bytes']>0 and r['after_bytes']>0
  assert re.fullmatch('[0-9a-f]{64}',r['before_sha256']) and re.fullmatch('[0-9a-f]{64}',r['after_sha256'])
  q=Path(r['candidate_after']);assert q.is_file() and not q.is_symlink() and q.stat().st_size==r['after_bytes'] and sha(q)==r['after_sha256']
 return d

def controls(d,receipt_sha,closed_path,closed_sha):
 path=Path(d['controls_json']);fixed(path,receipt_sha);c=load(path)
 assert c['status']=='PASS' and c['returncode']==0 and c['error'] is None and len(c['tests'])==3 and len(set(c['tests']))==3
 assert c['wall_cap_seconds']==c['CPU_cap_seconds']==5 and c['address_space_cap_bytes']==67108864
 assert c['APP_operations'] is False and c['Blender_or_native_producer_execution'] is False and c['actual_canonical_codec_fixture_SHA256']=='2083c5797bbe53c24f5d79e0a222320c5b29d1ffb4b9588731ccf0f94adc62c8'
 fixed(Path(d['controls_harness']),d['controls_harness_SHA256']);fixed(closed_path,closed_sha);closed=load(closed_path);r,k,g=closed['result'],closed['cleanup'],closed['resources']
 assert closed['accepted'] and r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==120 and r['timeout_override_reason'] is None
 assert k['cleanup_complete'] and not k['remaining_owned_children'] and g['accepted']
 return dict(controls_receipt=str(path),controls_SHA256=receipt_sha,controls_outer_CLOSED=str(closed_path),controls_outer_CLOSED_SHA256=closed_sha,actual_three_controls_PASS=True,original_limits='5CPU/5wall/64MiB plus original120 outer')

def main(a):
 assert not (P/'APPLY-RECEIPT.json').exists(),'first attempt only'
 d=admission(a.admission,a.admission_sha256);proof=controls(d,a.controls_sha256,a.controls_closed,a.controls_closed_sha256);before=verify();old={r['file']:r for r in before}
 for r in d['rows']:assert all(old[r['file']][k]==r['before_'+k] for k in ['bytes','sha256'])
 patch=str(Path(d['combined_patch']).resolve())
 num=subprocess.check_output(['git','-C',str(ROOT),'apply','--numstat','-z',patch],env=ENV)
 names={os.fsdecode(row.split(b'\t',2)[2]) for row in num.split(b'\0') if row};assert names==EXPECTED
 assert git('apply','--summary',patch)=='','only four existing regular files, no mode/add/delete/rename'
 run_git('apply','--check','--index',patch)
 suffix={name:(ROOT/name).read_bytes() for name in DOCS}
 run_git('apply','--index',patch)
 after={r['file']:dict(bytes=r['after_bytes'],sha256=r['after_sha256']) for r in d['rows']};rows=verify(after)
 for name,raw in suffix.items():assert (ROOT/name).read_bytes().endswith(raw),'opaque original document suffix must stay byte-exact'
 run_git('diff','--cached','--check');tree=git('write-tree');assert re.fullmatch('[0-9a-f]{40}',tree) and tree!=BASE_TREE
 result=dict(status='S3_REVIEWED_FOUR_SOURCE_PATHS_STAGED_UNCOMMITTED_GATE_PENDING',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=HEAD,index_tree=tree,branch=BRANCH,baseline301_SHA256=BASE_SHA,admission=str(a.admission),admission_SHA256=a.admission_sha256,combined_patch_SHA256=d['combined_patch_SHA256'],rows=[r for r in rows if r['file'] in EXPECTED],staged_paths=sorted(EXPECTED),deleted_paths=[],preserved_old301_outside_declared_paths=True,native8_and_fixture_unchanged=True,primary_ref_unchanged=True,docs_original_suffix_bytes_preserved=True,new_native_parents=False,production_action=False,controls=proof)
 (P/'APPLY-RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--admission',type=Path,required=True);parser.add_argument('--admission-sha256',required=True);parser.add_argument('--controls-sha256',required=True);parser.add_argument('--controls-closed',type=Path,required=True);parser.add_argument('--controls-closed-sha256',required=True);main(parser.parse_args())
