#!/usr/bin/env python3
"""Native publication of preserved e97; not a whole-gate or image qualification."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,time
R=pathlib.Path('/tmp/chicago-photo-worker-t3084-20261026');A=R/'chicago/4d';H='e97b67d549882b13fd858e714e73fb11da5aa006';T='c4247f16a7e4672ee265715b2cd0a8b03e9b0225'
E={k:v for k,v in os.environ.items()if k not in ('CHICAGO_TICKETS_DIR','GIT_NO_LAZY_FETCH')};E['GIT_OPTIONAL_LOCKS']='0'
# Keep the offline setting ONLY on our read-only source guards. Native tooling
# owns its fetch/materialization semantics and must not inherit a global ban.
G={**E,'GIT_NO_LAZY_FETCH':'1'}
O=pathlib.Path(sys.argv[1]);O.mkdir(exist_ok=False)
primary={'/workspace/chicago/.git/index':'195237adc725ac313d1bce7befc622cad8c54650218648c69eb781142c13f359','/workspace/chicago/site/4d/tickets.json':'4e2514c9a1d70b7df3747d5c44a297c5331a3721186d6e9444368e8e8e30962b'}
def sha(p):
 h=hashlib.sha256()
 with pathlib.Path(p).open('rb')as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
def save(n,v):(O/n).write_text(json.dumps(v,indent=2)+'\n')
def git(*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=R,env=G,text=True).strip()
def snapshot():
 assert git('rev-parse','HEAD')==H and git('rev-parse','HEAD^{tree}')==T
 assert not (R/'.git/MERGE_HEAD').exists()and not git('status','--porcelain')
 assert {p:sha(p)for p in primary}==primary,'Primary work changed'
 assets={}
 for n,d in [('brougham-source.glb','206cd7a9141896361abd312ce73cd4de0e0868eca532b097a995a0488fa3dfe4'),('brougham-near.glb','3d2f3a802f4b32dba6a3e61f2c188dddce4db05cecfcbba81e1e8d369d5dfe89'),('brougham-mid-source.glb','560373980cc70524c4f85071fb4e3df6bc29df8a884f3dc17960fabcaa625f9d'),('brougham-mid.glb','d5cdd34e981d29db41634ac780c22526742f6a20527b5866d2349c727a67400d')]:
  assets[n]=sha(A/'renderers/web/transport/parked-brougham'/n);assert assets[n]==d
 return {'head':H,'tree':T,'APP_tree':git('rev-parse','HEAD:chicago/4d'),'clean':True,'index_sha256':sha(R/'.git/index'),'primary':primary,'physical_carriage_assets':assets}
before=snapshot();save('BEFORE.json',before)
space={'tmp_free':shutil.disk_usage('/tmp').free,'workspace_free':shutil.disk_usage('/workspace').free,'minimum_tmp_free':500*1024**2}
save('CAPACITY-GUARD.json',space);assert space['tmp_free']>=space['minimum_tmp_free'],'Need native mirror capacity plus reserve before launch'
start=time.monotonic()
with(O/'native-publish.log').open('wb',buffering=0)as f:p=subprocess.run(['bash','tools/publish.sh'],cwd=A,env=E,stdout=f,stderr=subprocess.STDOUT)
save('NATIVE-RESULT.json',{'command':['bash','tools/publish.sh'],'returncode':p.returncode,'seconds':time.monotonic()-start})
after=snapshot();save('AFTER.json',after);assert before==after and p.returncode==0
site=R/'site/4d';assert site.is_dir()and not site.is_symlink()
stamp=json.loads((site/'build.json').read_text());assert len(stamp['version'])>=7 and H.startswith(stamp['version'])
manifest=[{'path':p.relative_to(site).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(site.rglob('*'))if p.is_file()]
save('PUBLISHED-MANIFEST.json',manifest)
binding={'schema':'T3084-clean-e97-publisher-v1','pass':True,'head':H,'candidate_tree':T,'candidate_APP_tree':before['APP_tree'],'repo':str(R),'mirror':str(site),'build':stamp,
 'source_unchanged':True,'primary_unchanged':True,'native_result':'NATIVE-RESULT.json','native_result_sha256':sha(O/'NATIVE-RESULT.json'),
 'manifest':'PUBLISHED-MANIFEST.json','manifest_sha256':sha(O/'PUBLISHED-MANIFEST.json'),'count':len(manifest),'bytes':sum(x['bytes']for x in manifest),
 'qualification':'Native source publication ONLY. Whole native gate and shipping optical delivery adoption NOT RUN.'}
save('BINDING.json',binding);print(json.dumps(binding))
