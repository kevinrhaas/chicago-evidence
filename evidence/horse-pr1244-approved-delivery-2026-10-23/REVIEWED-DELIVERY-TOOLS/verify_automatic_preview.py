import os,sys,pathlib,json,hashlib,datetime,time
sys.path.insert(0,'/workspace/shared');import owned_child_reaper_20261023 as owned
R=pathlib.Path('/workspace/chicago-waistcoat');BASE=pathlib.Path(__file__).resolve().parent
H='f225b8ae541173e2dde6e576bb20c103f4c87106';T='43665a4b692d5283defba96f236aed14b3c02623'
merge=json.loads((BASE/'NORMAL-GREEN-MERGE/TERMINAL.json').read_text());assert merge['status']=='MERGED_VERIFIED' and merge['source']==H and merge['source_tree']==T
M=merge['DEV_merge_commit'];D=BASE/'AUTOMATIC-PREVIEW-DELIVERY';D.mkdir(exist_ok=False)
files=['walk/transport/standing-horse/horse-sevket-v16-planted-standing-v1.glb','data/transport/parked/standing-horses.json','data/scenes/1835.json','walk/js/standing-horses.js','walk/js/standing-horse-planted-idle.js','walk/js/standing-horse-card.js','walk/js/yard-static-support.js','walk/js/main.js','walk/js/yards.js']
expected={f:hashlib.sha256((R/'site/4d'/f).read_bytes()).hexdigest()for f in files}
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def run(n,args,timeout=90):
 f=D/(n+'.log');v=owned.run(args,R,os.environ.copy(),f,timeout);save(n+'-process.json',{k:x for k,x in v.items()if k!='new_owned_orphans_reaped'});assert v['returncode']==0,f.read_text()[-1500:];return f.read_text().strip()
def api(n,route):return json.loads(run(n,['gh','api','repos/kevinrhaas/chicago/'+route]))
def get(n,path):
 body=D/(n+'.body');headers=D/(n+'.headers');url='https://chicago.polecat.live/4d/dev/'+path
 run(n,['curl','--silent','--show-error','--fail','--max-time','45','-H','Cache-Control: no-cache','-D',str(headers),'-o',str(body),url],55)
 data=body.read_bytes();return data,{'url':url,'at':now(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'headers':headers.name}
owned.enable()
try:
 assert run('local-source',['git','rev-parse','HEAD'])==H and run('local-tree',['git','rev-parse','HEAD^{tree}'])==T and not run('local-clean',['git','status','--porcelain'])
 save('EXPECTED.json',{'source':H,'source_tree':T,'merged_DEV':M,'published_mirror_sha256':expected,'scope':'Asset delivery only; no photographic/world/interaction acceptance. Normal automatic deploy only; no dispatch or source/ref writes.'})
 seen={};polls=[];delivered=False
 for i in range(45):
  deployments=api(f'{i:02d}-normal-deploy-runs','actions/workflows/deploy.yml/runs?per_page=10')
  data,receipt=get(f'{i:02d}-public-build','build.json');build=json.loads(data);assert build['tier']=='dev' and build['ref']=='refs/heads/dev'
  short=build['sha']
  if short not in seen:
   c=api(f'{i:02d}-public-build-commit','commits/'+short);full=c['sha'];comparison=api(f'{i:02d}-merged-to-public-ancestry','compare/'+M+'...'+full);seen[short]={'full':full,'contains_merged':comparison['status']in['ahead','identical'],'comparison_status':comparison['status']}
  row={'at':now(),'build':build,'build_receipt':receipt,'ancestry':seen[short],'normal_deploys':[{'id':x['id'],'event':x['event'],'head_branch':x['head_branch'],'head_sha':x['head_sha'],'status':x['status'],'conclusion':x['conclusion'],'created_at':x['created_at']}for x in deployments['workflow_runs']]};polls.append(row);save('LATEST.json',row);save('POLLS.json',polls)
  print('preview',i,short,'contains horse merge',seen[short]['contains_merged'],flush=True)
  if seen[short]['contains_merged']:delivered=True;break
  time.sleep(55)
 assert delivered,'Normal DEV preview not yet observed within bounded polling window; do not claim delivery'
 results=[]
 for i,f in enumerate(files):
  data,receipt=get('asset-'+str(i),f);receipt.update(path=f,expected_sha256=expected[f],PASS=receipt['sha256']==expected[f]);results.append(receipt);save('ASSET-RESULTS.json',results);assert receipt['PASS'],'Published asset differs from reviewed source: '+f
 assert all(hashlib.sha256((R/'site/4d'/f).read_bytes()).hexdigest()==expected[f]for f in files),'Local published expectations changed'
 save('TERMINAL.json',{'status':'PASS_EXACT_PUBLIC_ASSET_DELIVERY','at':now(),'PR':1244,'source':H,'source_tree':T,'DEV_merge_commit':M,'public_build':build,'public_full_commit':seen[short]['full'],'merged_source_is_ancestor_public_build':True,'asset_count':len(results),'assets':results,'dispatches':0,'source_ref_writes':0,'photographic_completion':False,'scope':'HTTP delivery of exact published source bytes only; no browser image, world, gait, photographic or interaction PASS implied.'})
 print('PASS EXACT PUBLIC ASSET DELIVERY',flush=True)
finally:save('OWNED-CLEANUP.json',owned.finish())
