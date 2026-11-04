from pathlib import Path
import os,json,subprocess,hashlib,stat,shutil,time
P=Path(__file__).parent;W=Path('/tmp/wolf-poster-source-20261103');A=W/'chicago/4d';S=W/'site/4d';H='6e23cbf1b382c39ea2e259147422a9b6d3103a0e';F=P/'W-FROZEN-JAIL-6E23.json';O=P/'runtime-6e23-body';E=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1');sha=lambda b:hashlib.sha256(b).hexdigest();pf=lambda p:sha(Path(p).read_bytes());canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode();git=lambda *a:subprocess.check_output(['git','-C',str(W),*a],env=E)
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def floor():
 d={p:shutil.disk_usage(p).free for p in ['/workspace','/tmp']};assert d['/workspace']>=536870912 and d['/tmp']>=1800000000,d;return d
def metadata():
 d={n:sha(git(*v))for n,v in {'index':['ls-files','--stage','-z'],'flags':['ls-files','-v','-z'],'refs':['for-each-ref','--format=%(refname) %(objectname)'],'config':['config','--local','--list','--null'],'untracked':['ls-files','--others','--exclude-standard','-z'],'diff':['diff','--binary'],'staged':['diff','--cached','--binary']}.items()};d['head']=git('rev-parse','HEAD').decode().strip()
 for n in ['index','HEAD','MERGE_HEAD','ORIG_HEAD','packed-refs','shallow','objects/info/alternates']:
  p=Path(git('rev-parse','--path-format=absolute','--git-path',n).decode().strip());d[n]={'sha256':pf(p),'mode':stat.S_IMODE(p.stat().st_mode),'mtime_ns':p.stat().st_mtime_ns}if p.exists()else None
 return d
def pubmap():return {p.relative_to(S).as_posix():{'sha256':pf(p),'bytes':p.stat().st_size,'mode':stat.S_IMODE(p.stat().st_mode)}for p in sorted(S.rglob('*'))if p.is_file()}
def bindings():
 files={F}
 for d in [A/'renderers/web',S/'walk']:
  for x in ['*.js','*.mjs','*.css','*.html']:files.update(d.rglob(x))
 for base in [A,S]:
  for path in ['data/reader/structures_1835.json','data/pictures/1835.json','data/inspect/1835.json','data/liberties.json','data/sidecars/1835/log_jail_keeper_house.json','data/sidecars/1835/log_jail.json']:
   if(base/path).exists():files.add(base/path)
 for sid,key in [('log_jail_keeper_house','log_jail_keeper_house__frame_1835.glb'),('log_jail','log_jail__log_1833.glb')]:
  files.add(A/'data/structures'/(sid+'.json'));files.add(A/'assets/gltf'/key);files.add(A/'assets/web'/key);doc=json.loads((S/f'data/sidecars/1835/{sid}.json').read_text());pub=S/'data'/doc['asset'];assert pub.read_bytes()==(A/'assets/web'/key).read_bytes();files.add(pub)
  for c in doc.get('citations',[]):
   x=A/'data/sources'/(c['source_id']+'.json')
   if x.exists():files.add(x)
 for name in ['assets/manifest.json','assets/manifest.web.json','assets/manifest.versions.json','generators/archetypes/frame_dwelling.py','tools/smoke_renderer.mjs']:
  files.add(A/name)
 return {str(p):{'sha256':pf(p),'bytes':p.stat().st_size,'mode':stat.S_IMODE(p.stat().st_mode)}for p in sorted(files)}
assert not O.exists();assert git('rev-parse','HEAD').decode().strip()==H and not git('status','--porcelain');assert H.startswith(json.loads((S/'build.json').read_text())['version']);floor();dump(F,{'head':H,'sourcePubGPUexclusive':True,'sourceGitPublicationFrozen':True,'historicalCameraOrGradePromotion':False})
meta=metadata();bound=bindings();pub=pubmap();helpers={n:pf(P/n)for n in ['run_jail_body.py','probe_jail_east.mjs']};a=json.loads((P.parent/'INDEPENDENT-MATERIAL-AND-SCOPE-AUDIT.json').read_text());tri=a['moved_triangle_positions'];centroid=[sum(v[i]for v in tri)/3 for i in range(3)];plan={'expected_head':H,'expected_tree':git('rev-parse','HEAD^{tree}').decode().strip(),'site_parent':str(W/'site'),'input_bindings':bound,'source_scope_sha256':sha(canon(bound)),'east_face':{'centroid':centroid,'eye':[15.5,10.5,centroid[2]]},'scope':'Curated current published1835 keeper east face BOTH, no historical camera/grade/passage/fullcompound acceptance'};dump(P/'JAIL-BODY-PLAN.json',plan);dump(P/'JAIL-BODY-BEFORE-PUBMAP.json',pub);ph=pf(P/'JAIL-BODY-PLAN.json');O.mkdir();scratch=Path('/tmp/jq/e23');scratch.mkdir(parents=True,exist_ok=True);env=dict(E,TMPDIR=str(scratch),TMP=str(scratch),TEMP=str(scratch),NODE_COMPILE_CACHE=str(P/'node-cache'),XDG_CACHE_HOME=str(P/'cache'));steps=[];error=None
def guard():
 assert metadata()==meta,'Git/source metadata drift';assert bindings()==bound,'Selected bindings drift';assert pubmap()==pub,'Full publication changed';assert {n:pf(P/n)for n in helpers}==helpers;assert pf(P/'JAIL-BODY-PLAN.json')==ph;floor()
try:
 for viewport in ['desktop','mobile']:
  guard();t=time.monotonic();ve=dict(env,JAIL_PROBE_PLAN=str(P/'JAIL-BODY-PLAN.json'),JAIL_PROBE_OUT=str(O/viewport),JAIL_PROBE_VIEWPORT=viewport,JAIL_PROBE_LEG='body');rr=O/(viewport+'-REAPER.json')
  with (O/(viewport+'.log')).open('xb')as out:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(rr),'--','timeout','--signal=TERM','--kill-after=15s','600s','taskset','-c','0-4','node',str(P/'probe_jail_east.mjs')],cwd=A,env=ve,stdout=out,stderr=subprocess.STDOUT)
  receipt=json.loads(rr.read_text());assert r.returncode==receipt['command_exit']==0 and receipt['all_children_reaped']and not receipt['leftover_cleanup'],receipt;result=json.loads((O/viewport/'RESULT.json').read_text());assert result['status']=='ACTUAL_KEEPER_EAST_BODY_INSPECT_PASS';closed=json.loads((O/viewport/'CLOSURE.json').read_text());assert closed['failure']is None and all(not closed[k]for k in ['errors','network','consoleErrors','serverErrors']);guard();steps.append({'viewport':viewport,'head':H,'seconds':time.monotonic()-t,'result':result['status'],'reaper':receipt,'output':str(O/viewport)});dump(O/'PROGRESS.json',steps);print('ACTUAL VIEWPORT CLOSED',viewport,steps[-1]['seconds'],flush=True)
except BaseException as exc:error=repr(exc);print(error,flush=True)
finally:
 try:guard();exact=True
 except BaseException as exc:exact=False;error=(error+'; 'if error else'')+repr(exc)
 dump(O/'FINAL-CLOSURE.json',{'status':'ACTUAL_KEEPER_EAST_BOTH_CLOSED_PASS'if not error and len(steps)==2 else'NOT_QUALIFIED','head':H,'steps':steps,'error':error,'sourceGitSelectedInputsFullPublicationHelpersPlanExact':exact,'selectedInputs':len(bound),'fullPublishedMembers':len(pub),'fullPubmapSHA':sha(canon(pub)),'resources':floor(),'allOwnedChildrenReaped':all(s['reaper']['all_children_reaped']for s in steps)});print('BOTH FINAL',error or'PASS',flush=True)
raise SystemExit(1 if error else 0)
