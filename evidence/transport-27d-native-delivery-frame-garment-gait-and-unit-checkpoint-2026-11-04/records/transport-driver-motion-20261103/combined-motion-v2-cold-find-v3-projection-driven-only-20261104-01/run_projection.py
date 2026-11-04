from pathlib import Path
import subprocess,hashlib,json,re,os,importlib.util,datetime,tempfile,shutil
ROOT=Path('/workspace/chicago-transport-current-20261103');APP=ROOT/'chicago/4d';HERE=Path(__file__).resolve().parent;PROJ=HERE/'projection/chicago/4d';PREP=Path('/workspace/.cloud-setup/transport-cold-driver-find-prepared-v3-20261104');SUP=Path('/workspace/.cloud-setup/transport-supervise.py')
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def git(*a):return subprocess.check_output(['git','--no-optional-locks','-C',str(ROOT),*a],env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0'),timeout=20)
def snapshot():
 stage=git('ls-files','--stage','-z');expected=b''
 rows=[]
 for raw in git('ls-tree','-r','-z','f2d0bc74730766d3309a8b23900e39c112e1fffe').split(b'\0'):
  if raw:
   info,path=raw.split(b'\t',1);mode,kind,oid=info.split();rows.append((path,mode+b' '+oid+b' 0\t'+path+b'\0'))
 expected=b''.join(x for _,x in sorted(rows));assert stage==expected
 result=dict(HEAD=git('rev-parse','HEAD').decode().strip(),MERGE_HEAD=git('rev-parse','MERGE_HEAD').decode().strip(),TREE='f2d0bc74730766d3309a8b23900e39c112e1fffe',APP=git('rev-parse','f2d0bc74730766d3309a8b23900e39c112e1fffe:chicago/4d').decode().strip(),semantic_index_sha256=sha(stage),unstaged_diff_sha256=sha(git('diff','--binary')),status_sha256=sha(git('status','--porcelain=v1','--untracked-files=all')))
 assert result['HEAD']=='edfc3edc60cf00a8cf2376419d0df8fc3cd8b0a3'and result['MERGE_HEAD']=='b622c89794f3c52086421b6208ef3eb2876a0528'
 assert result['APP']=='956ba4adc9ed9d855d18c197d26e208e8f6cb2d0'and result['semantic_index_sha256']=='f1ce756b9a58dd4e4d00b06ec90ac3db5f9ae693dd129bbb4c497561cc0e6257'
 assert git('diff','--quiet')==b''
 return result
spec=importlib.util.spec_from_file_location('guard','/workspace/.cloud-setup/transport-current-20261103/resource_guard.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--go',type=Path,required=True);args=parser.parse_args();ROOT_GO=json.loads(args.go.read_text());assert ROOT_GO['approved']is True and ROOT_GO['policy']=='ROOT_AUTHORIZED_FAILED_DRIVEN_PROJECTION_TEST_ONLY';assert ROOT_GO['PREPARED_sha256']=='521d603635b55a79d954f99cce95ffdedfc248d0513aaddd4e345477071d20fb';assert ROOT_GO['tests_to_execute']==['test_driven_assembly'];assert ROOT_GO['APP_apply_authorized']is False
before=snapshot();save(HERE/'ROOT-SOURCE-BEFORE.json',before);rb=guard.snapshot();assert guard.check(rb)['accepted'];save(HERE/'RESOURCES-BEFORE.json',rb)
prepared_bytes=(PREP/'PREPARED.json').read_bytes();assert sha(prepared_bytes)=='521d603635b55a79d954f99cce95ffdedfc248d0513aaddd4e345477071d20fb'
prepared=json.loads(prepared_bytes);assert prepared['ROOT_EXPLICIT_APPLY_GO']is False
assert all(sha((PREP/p).read_bytes())==v['sha256']and (PREP/p).stat().st_size==v['bytes']for p,v in prepared['files'].items())
motion_pins=json.loads((HERE.parent/'next-motion-clock-prepared-v2-20261104/SOURCE-PINS.json').read_text());patch_names=['COMBINED-MOTION-V2-COLD-FIND-NOT-APPLIED.patch','UNIT-COMBINED-MOTION-V2-COLD-FIND-NOT-APPLIED.patch']
pins=dict(source_sha256=motion_pins['source_sha256'],patch_sha256={p:prepared['files'][p]['sha256']for p in patch_names},prepared_sha256=sha(prepared_bytes),prepared_apply_GO=False,projection_only_ROOT_authorized=True)
assert all(sha((ROOT/p).read_bytes())==h for p,h in pins['source_sha256'].items());assert all(sha((PREP/p).read_bytes())==h for p,h in pins['patch_sha256'].items());assert subprocess.check_output(['node','--version']).decode().startswith('v22.')
seen=set();todo=[APP/'tools/test_transport_loop.mjs',APP/'tools/test_driven_assembly.mjs',APP/'renderers/web/js/interact.js',APP/'renderers/web/js/transport-interactions.js',APP/'renderers/web/js/travel.js']
while todo:
 p=todo.pop()
 if p in seen:continue
 seen.add(p);s=p.read_text()
 for match in re.findall(r"(?:from\s*['\"]|import\s*\(\s*['\"]|import\s*['\"])([^'\"]+)",s):
  if match.startswith('.'):
   q=(p.parent/match).resolve()
   if q.is_file():todo.append(q)
for p in list(seen):
 if p.suffix=='.mjs':
  for match in re.findall(r"new URL\(\s*['\"]([^'\"]+)['\"],\s*import.meta.url",p.read_text()):
   if match.startswith('.'):
    q=(p.parent/match).resolve()
    if q.is_file():seen.add(q)
records=[]
for p in sorted(seen):
 rel=p.relative_to(APP);target=PROJ/rel;target.parent.mkdir(parents=True,exist_ok=True);data=p.read_bytes();target.write_bytes(data);records.append(dict(path=str(rel),bytes=len(data),sha256=sha(data)))
assert 24 <= len(records) <= 40 and sum(x['bytes']for x in records)<5*1024**2
save(HERE/'PROJECTION-BASE-MANIFEST.json',dict(scope='MINIMAL_SOURCE_PROJECTION_NOT_ROOT_APP_OR_FULL_NATIVE_GATE',records=records,source_pins=pins))
for name in patch_names:
 q=subprocess.run(['git','apply','--check',str(PREP/name)],cwd=PROJ.parents[1],capture_output=True,text=True,timeout=10);assert q.returncode==0,(name,q.stderr)
 q=subprocess.run(['git','apply',str(PREP/name)],cwd=PROJ.parents[1],capture_output=True,text=True,timeout=10);assert q.returncode==0,(name,q.stderr)
for name in ['tools/test_transport_loop.mjs','tools/test_driven_assembly.mjs']:assert (PROJ/name).read_bytes().startswith((APP/name).read_bytes()),'Original test content must remain an exact prefix'
changed=[p for p in records if sha((PROJ/p['path']).read_bytes())!=p['sha256']];assert sorted(x['path']for x in changed)==sorted(p.replace('chicago/4d/','',1)for p in pins['source_sha256'])
save(HERE/'PROJECTION-AFTER-PATCH.json',dict(changed=[dict(path=x['path'],sha256=sha((PROJ/x['path']).read_bytes()))for x in changed],original_tests_exact_prefix=True,patch_pins=pins['patch_sha256']))
PRIOR=HERE.parent/'combined-motion-v2-cold-find-v2-projection-units-20261104-01';prior_closed=json.loads((PRIOR/'CLOSED.json').read_text());assert prior_closed['status']=='PROJECTION_NONPASS'and prior_closed['ROOT_source_before']==prior_closed['ROOT_source_after']==before and prior_closed['resources']['accepted']
prior_loop=prior_closed['ledger'][0];assert prior_loop['name']=='test_transport_loop'and prior_loop['result']['returncode']==0 and not prior_loop['result']['timed_out'];assert prior_loop['result']['effective_timeout_seconds']==prior_loop['result']['requested_timeout_seconds']==30 and prior_loop['result']['timeout_override_reason']is None;assert prior_loop['cleanup']['cleanup_complete']and not prior_loop['cleanup']['remaining_owned_children']
for path in ['renderers/web/js/main.js','renderers/web/js/town-transport.js','renderers/web/js/transport-loop.js','tools/test_transport_loop.mjs']:assert (PROJ/path).read_bytes()==(PRIOR/'projection/chicago/4d'/path).read_bytes(),'Prior loop proof requires exact runtime/test byte identity'
reused_loop=dict(prior_closed_sha256=sha((PRIOR/'CLOSED.json').read_bytes()),prior=prior_loop,exact_runtime_and_loop_test_unchanged=True,artifacts={str(p):sha(p.read_bytes())for p in [PRIOR/'test_transport_loop.log',PRIOR/'test_transport_loop.result.json',PRIOR/'test_transport_loop.cleanup.json']});save(HERE/'VERIFIED-PRIOR-UNCHANGED-LOOP-PASS.json',reused_loop)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('GIT_NO_LAZY_FETCH',None);env.pop('CHICAGO_TICKETS_DIR',None)
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:assert env.get(k)=='1'
syntax=[]
for row in [x for x in changed if x['path']=='tools/test_driven_assembly.mjs']:
 q=subprocess.run(['node','--check',row['path']],cwd=PROJ,env=env,capture_output=True,text=True,timeout=5);syntax.append(dict(path=row['path'],returncode=q.returncode,stdout=q.stdout,stderr=q.stderr));assert q.returncode==0,syntax[-1]
save(HERE/'NODE-SYNTAX.json',syntax)
ledger=[];error=None
try:
 for name in ['test_driven_assembly']:
  tmp=Path(tempfile.mkdtemp(prefix=name+'-',dir=HERE));childenv=dict(env,TMPDIR=str(tmp));prefix=HERE/name
  q=subprocess.run(['python',str(SUP),'--prefix',str(prefix),'--cwd',str(PROJ),'--timeout','30','--','node','tools/'+name+'.mjs'],env=childenv,stdout=(HERE/(name+'-owner.stdout')).open('xb'),stderr=subprocess.STDOUT,timeout=40)
  result=json.loads(Path(str(prefix)+'.result.json').read_text());cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text());row=dict(name=name,result=result,cleanup=cleanup);ledger.append(row)
  shutil.rmtree(tmp);row['owned_TMPDIR_removed']=not tmp.exists();save(HERE/'LEDGER.json',ledger)
  assert q.returncode==result['returncode']==0 and not result['timed_out'],row
  assert result['effective_timeout_seconds']==result['requested_timeout_seconds']==30 and result['timeout_override_reason']is None
  assert cleanup['cleanup_complete']and not cleanup['remaining_owned_children']
except BaseException as e:error=repr(e)
after=snapshot();resources=guard.pair(rb,guard.snapshot());assert before==after;assert resources['accepted'];save(HERE/'ROOT-SOURCE-AFTER.json',after)
closed=dict(status='ACTUAL_COMBINED_MOTION_V2_COLD_FIND_V3_DRIVEN_ONLY_PASS_WITH_VERIFIED_UNCHANGED_PRIOR_LOOP_PASS_NOT_APP_OR_FULL_GATE'if error is None else'PROJECTION_NONPASS',error=error,ROOT_source_before=before,ROOT_source_after=after,resources=resources,projection_files=len(records),projection_base_bytes=sum(x['bytes']for x in records),source_pins=pins,original_tests_exact_prefix=True,node_syntax=syntax,ledger=ledger,verified_prior_unchanged_loop_pass=reused_loop,ROOT_GO_sha256=sha(args.go.read_bytes()),APP_written=False,ROOT_Git_refs_written=False,assets_generated=False,browser_or_GPU_used=False,canonical_lock_acquired=False,full_native_gate_qualification=False)
save(HERE/'CLOSED.json',closed);print(json.dumps(dict(status=closed['status'],error=error,tests=[dict(name=x['name'],returncode=x['result']['returncode'],seconds=x['result']['seconds'])for x in ledger],source_unchanged=before==after,resources_accepted=resources['accepted'])));raise SystemExit(0 if error is None else 1)
