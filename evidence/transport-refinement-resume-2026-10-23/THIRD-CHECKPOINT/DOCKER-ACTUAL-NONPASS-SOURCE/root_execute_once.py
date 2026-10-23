import os,sys,pathlib,json,hashlib,datetime
sys.path.insert(0,'/workspace/shared');import owned_child_reaper_20261023 as owned
P=pathlib.Path(__file__).resolve().parent;D=P/'ROOT-DOCKER-ACTUAL';D.mkdir(exist_ok=False)
TAG='codex-t2794-source8-scratch:20261023';NAME='t2794-native-source8-20261023-owned1';CID=None
ENV=os.environ.copy()
for k in ['DOCKER_HOST','DOCKER_CONTEXT','DOCKER_TLS','DOCKER_TLS_VERIFY','DOCKER_CERT_PATH']:ENV.pop(k,None)
DOCKER=['docker','--host=unix:///var/run/docker.sock'];now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def run(n,args,limit=90,required=True):
 r=owned.run(args,P,ENV,D/(n+'.log'),limit);save(n+'-process.json',{k:v for k,v in r.items()if k!='new_owned_orphans_reaped'});print(n,r['returncode'],flush=True)
 if required:assert r['returncode']==0,(D/(n+'.log')).read_text()[-2000:]
 return r,(D/(n+'.log')).read_text().strip()
def inspect(n,cid):
 _,text=run(n,DOCKER+['inspect','--format','{{json .State}}',cid]);state=json.loads(text)
 _,label=run(n+'-ownership',DOCKER+['inspect','--format','{{index .Config.Labels "codex.owner"}}',cid]);assert label=='t2794-native-source8-20261023'
 save(n+'-state.json',state);return state
owned.enable()
try:
 for name,h in [('scratch-context/Dockerfile','24b564d2707c0d5761c4bc485370084df80021589a694cbf1739639a11ebe895'),('DOCKER-BUILD-ARGV-PROPOSED.json','6034afbc6db78219dd7de52fad738cb07204f2572d01e13acfb485dbe6575eaf'),('DOCKER-RUN-ARGV-PROPOSED.json','0c718bf6519e538bfe04423979e94db05f41a1c5769fab00b4d8131e39de345a')]:assert hashlib.sha256((P/name).read_bytes()).hexdigest()==h,name
 r,text=run('00-owned-name-absent',DOCKER+['container','inspect','--format','{{.Id}}',NAME],required=False);assert r['returncode']!=0 and ('No such' in text),'Owned name already exists or daemon error'
 build=json.loads((P/'DOCKER-BUILD-ARGV-PROPOSED.json').read_text());save('BUILD-ARGV.json',build);run('01-build-local-scratch',build,100)
 _,image_id=run('02-image-id',DOCKER+['image','inspect','--format','{{.Id}}',TAG]);save('IMAGE.json',{'id':image_id,'tag':TAG,'no_network_build':True})
 release=json.loads((P/'ROOT-RELEASE-PROPOSED-HELD.json').read_text());release.update(release_preview=True,current_root_exclusive_browser_slot=True,scope='Root-reviewed one finite same-runtime native comparison inside owned isolated container; no photographic or performance equivalence acceptance implied.')
 f=P/'ROOT-RELEASE.json';assert not f.exists();f.write_text(json.dumps(release,indent=2)+'\n')
 args=json.loads((P/'DOCKER-RUN-ARGV-PROPOSED.json').read_text());assert args[2]=='run' and args[3]=='--rm';args[2]='create';del args[3]
 i=args.index(TAG);args[i:i]=['--mount',f'type=bind,src={f},dst={f},readonly'];save('CREATE-ARGV.json',args)
 _,CID=run('03-create-owned-container',args);assert len(CID)==64 and all(x in '0123456789abcdef'for x in CID);save('OWNED-CONTAINER.json',{'id':CID,'name':NAME,'label_owner':'t2794-native-source8-20261023','created':now()})
 state=inspect('04-before-start',CID);assert not state['Running']
 result,_=run('05-start-attach',DOCKER+['start','--attach',CID],190,required=False)
 state=inspect('06-after-start',CID);receipt=P/'actual/receipt.json';capture=json.loads(receipt.read_text())if receipt.exists()else None
 ok=result['returncode']==0 and state['ExitCode']==0 and not state['Running'] and capture is not None and capture.get('pass')is True and len(capture.get('rows',[]))==8 and not capture.get('errors')
 save('TERMINAL.json',{'status':'ACTUAL_CONTAINER_NATIVE_CAPTURE_PASS'if ok else'ACTUAL_CONTAINER_NATIVE_CAPTURE_NONPASS','at':now(),'container':CID,'image':image_id,'container_exit':state['ExitCode'],'capture_exists':receipt.exists(),'capture_pass':capture.get('pass')if capture else None,'capture_rows':len(capture.get('rows',[]))if capture else 0,'source_caller_unchanged':True,'photographic_acceptance':False,'performance_equivalence_claim':False});print('native capture',ok,flush=True)
finally:
 if CID:
  state=inspect('07-final-owned-state',CID)
  if state['Running']:run('08-stop-only-owned-container',DOCKER+['stop','--time','5',CID],20)
  run('09-remove-only-owned-container',DOCKER+['rm',CID],20)
  r,t=run('10-verify-owned-container-absent',DOCKER+['container','inspect','--format','{{.Id}}',CID],20,required=False);assert r['returncode']!=0 and 'No such'in t
  save('CONTAINER-CLOSED.json',{'id':CID,'removed':True,'at':now(),'no_other_containers_or_daemon_touched':True})
 save('OWNED-CLI-CLEANUP.json',owned.finish())
