import datetime,gzip,hashlib,json,os,pathlib,subprocess,time,urllib.request,traceback
P=pathlib.Path(__file__).resolve().parent
EXPECTED=json.loads((P/'EXPECTED-A620-ASSETS.json').read_text())
HEADS=['9881d782370d612c3ca521df383d67b1bb48487f','aa4f5cc8057bdd04a20c832a05bf4e4195807347']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def get(url):
 req=urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Chicago-DEV-source-verification'})
 with urllib.request.urlopen(req,timeout=35) as r:b=r.read();headers=dict(r.headers);status=r.status
 enc=headers.get('Content-Encoding',headers.get('content-encoding',''))
 decoded=gzip.decompress(b) if enc.lower()=='gzip' else b
 return decoded,{'url':url,'observed_at':now(),'http_status':status,'headers':headers,'raw_bytes':len(b),'raw_sha256':sha(b),'decoded_bytes':len(decoded),'decoded_sha256':sha(decoded)}
start=time.monotonic(); seq=0; closed=None
while time.monotonic()-start<600:
 seq+=1; d=P/f'poll-{seq:02d}';d.mkdir(exist_ok=False)
 try:
  r=subprocess.run(['gh','api','repos/kevinrhaas/chicago/actions/workflows/deploy.yml/runs?per_page=12'],capture_output=True,text=True,timeout=40)
  (d/'runs.json').write_text(r.stdout);runs=json.loads(r.stdout)['workflow_runs'] if r.returncode==0 else []
  b,meta=get('https://chicago.polecat.live/4d/dev/build.json?verify=pr1649-'+str(int(time.time())))
  (d/'build.body').write_bytes(b);(d/'build-http.json').write_text(json.dumps(meta,indent=2)+'\n');build=json.loads(b);seen=build.get('sha','')
  print(now(),'public',seen,'runs',[(x['id'],x['head_sha'][:8],x['status'],x['conclusion']) for x in runs[:5]],flush=True)
  matched=[h for h in HEADS if len(seen)>=7 and h.startswith(seen)]
  if matched:
   results=[]
   for entry in EXPECTED:
    body,m=get('https://chicago.polecat.live/4d/dev/'+entry['public_relative']+'?verify=pr1649-'+str(int(time.time())))
    m.update({'expected':entry,'matches_native_source':m['decoded_sha256']==entry['sha256']})
    if entry['public_relative'].endswith('.json'):(d/pathlib.Path(entry['public_relative']).name).write_bytes(body)
    results.append(m);print('asset',entry['public_relative'],m['matches_native_source'],flush=True)
   (d/'ASSET-READBACK.json').write_text(json.dumps(results,indent=2)+'\n')
   b2,m2=get('https://chicago.polecat.live/4d/dev/build.json?verify=pr1649-after-'+str(int(time.time())))
   (d/'build-after.body').write_bytes(b2);(d/'build-after-http.json').write_text(json.dumps(m2,indent=2)+'\n')
   after=json.loads(b2)
   closed={'status':'PUBLIC_DEV_BUILD_AND_SELECTED_ASSETS_MATCH' if all(x['matches_native_source'] for x in results) and after.get('sha')==seen else 'PUBLIC_READBACK_NONPASS','observed_at':now(),'public_build':build,'public_build_after':after,'full_dev_head':matched[0],'merge_commit':'9881d782370d612c3ca521df383d67b1bb48487f','qualified_source_head':'a6207b493f7ce06052e9e211245631a1e07f8df1','source_tree':'0472b3e7d758fe265e93b2d6f508cf91564286f6','poll_dir':str(d),'asset_count':len(results),'assets_all_match':all(x['matches_native_source'] for x in results),'same_build_before_after':after.get('sha')==seen,'new_browser_or_GPU_launched':False,'screenshot':'not captured; canonical GPU owned by ROOT supplemental B','dispatches_performed':0,'production_promotion_performed':False}
   break
 except Exception as e:
  (d/'ERROR.txt').write_text(traceback.format_exc());print(now(),'ERROR',repr(e),flush=True)
 remaining=600-(time.monotonic()-start)
 if remaining>0:time.sleep(min(40,remaining))
if closed is None:closed={'status':'BOUNDED_WINDOW_CLOSED_WITHOUT_NEW_PUBLIC_BUILD','observed_at':now(),'polls':seq,'elapsed_seconds':time.monotonic()-start,'dispatches_performed':0,'production_promotion_performed':False,'new_browser_or_GPU_launched':False}
(P/'WATCH-CLOSED.json').write_text(json.dumps(closed,indent=2)+'\n');print('CLOSED',closed,flush=True)
