"""External-only PR1685 runtime qualification on a final committed, published, writer-frozen tree."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,stat,subprocess,tempfile,time
ap=argparse.ArgumentParser();ap.add_argument('--head',required=True);ap.add_argument('--tree',required=True);ap.add_argument('--run',action='store_true');args=ap.parse_args();assert args.run
P=Path(__file__).resolve().parent;N=Path('/workspace/chicago-bridge-increment-20261102');A=N/'chicago/4d';S=N/'site/4d';H=args.head;TREE=args.tree;O=P/'custom';K=P/'native3';FREEZE=P/'WRITER-FREEZE.json';sha=lambda b:hashlib.sha256(b).hexdigest();pf=lambda p:sha(Path(p).read_bytes());canonical=lambda d:(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode();E=os.environ.copy()
for key in list(E):
 if key.startswith('GIT_')or key.startswith('SMOKE_')or key=='CHICAGO_TICKETS_DIR':E.pop(key,None)
E.update(GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK='1')
def git(*args):return subprocess.check_output(['/usr/local/bin/git','-C',str(N),*args],env=E)
def dump(path,obj):Path(path).write_text(json.dumps(obj,indent=2)+'\n')
def floor():
 d={p:shutil.disk_usage(p).free for p in ['/workspace','/tmp']};assert d['/workspace']>=536870912 and d['/tmp']>=1800000000,d;return d
def metadata():
 d={n:sha(git(*args))for n,args in {'index_stage':['ls-files','--stage','-z'],'index_flags':['ls-files','-v','-z'],'refs':['for-each-ref','--format=%(refname) %(objectname)'],'config':['config','--local','--list','--null'],'untracked':['ls-files','--others','--exclude-standard','-z']}.items()};d['head']=git('rev-parse','HEAD').decode().strip();d['tree']=git('rev-parse','HEAD^{tree}').decode().strip()
 for name in ['index','HEAD','MERGE_HEAD','MERGE_MSG','ORIG_HEAD','packed-refs','shallow','objects/info/alternates']:
  p=Path(git('rev-parse','--path-format=absolute','--git-path',name).decode().strip());d[name]={'sha256':pf(p),'mode':stat.S_IMODE(p.stat().st_mode),'mtime_ns':p.stat().st_mtime_ns,'ctime_ns':p.stat().st_ctime_ns}if p.exists()else None
 return d
def pubmap():
 d={p.relative_to(S).as_posix():{'bytes':p.stat().st_size,'sha256':pf(p),'mode':stat.S_IMODE(p.stat().st_mode),'symlink':os.readlink(p)if p.is_symlink()else None}for p in sorted(S.rglob('*'))if p.is_file()};assert len(d)>5000;return d
def bindings():
 files=set()
 for root in [A/'renderers/web',S/'walk']:
  for ext in ['*.js','*.mjs','*.css','*.html']:files.update(root.rglob(ext))
 files.update([FREEZE,A/'tools/smoke_renderer.mjs',A/'tools/compile_pictures.py',A/'tools/grade_structures.py',A/'data/structure_grades.json',A/'assets/manifest.json',A/'assets/manifest.web.json',A/'assets/manifest.versions.json'])
 sid='first_fort_dearborn_small_house_ne';files.add(A/f'data/structures/{sid}.json')
 # The presence repair must bind the real parade asset, sidecar and ground owner too.
 parade='first_fort_dearborn_parade';asset='first_fort_dearborn_parade__first_fort_1803.glb'
 files.update([A/f'data/structures/{parade}.json',A/f'data/sidecars/1812/{parade}.json',S/f'data/sidecars/1812/{parade}.json',A/'assets/gltf'/asset,A/'assets/web'/asset,S/'data/gltf'/asset])
 for base in [A,S]:
  files.update([base/'data/enclosures/1812/index.json',base/'data/enclosures/1812/first_fort_dearborn_parade_ground.json'])
 assert (A/'assets/web'/asset).read_bytes()==(S/'data/gltf'/asset).read_bytes()
 for scene in ['1812','1835']:
  for rel in [f'data/pictures/{scene}.json',f'data/reader/structures_{scene}.json']:
   for base in [A,S]:
    if(base/rel).exists():files.add(base/rel)
 for scene in ['1812']:
  source=A/f'data/sidecars/{scene}/{sid}.json';published=S/f'data/sidecars/{scene}/{sid}.json';doc=json.loads(source.read_bytes());shipped=json.loads(published.read_bytes());files.update([source,published]);assert dict(shipped,residents=doc['residents'])==doc if doc.get('residents') else shipped==doc
  asset=Path(doc['asset']);assert not asset.is_absolute()and'..'not in asset.parts;files.update([A/'assets'/asset,A/'assets/web'/asset.name,S/'data'/asset]);assert(A/'assets/web'/asset.name).read_bytes()==(S/'data'/asset).read_bytes()
  for c in doc['citations']:files.add(A/'data/sources'/(c['source_id']+'.json'))
 for p in(A/'data/reference_views/first_fort_dearborn_pickets_outer').glob('*.json'):
  files.add(p)
  if not p.name.endswith('.match.json'):
   camera=json.loads(p.read_bytes());files.update([(p.parent/camera['photo']).resolve(),A/'data/sources'/(camera['source_id']+'.json')])
 return{str(p):{'bytes':p.stat().st_size,'sha256':pf(p),'mode':stat.S_IMODE(p.stat().st_mode)}for p in sorted(files)}
assert not O.exists()and not K.exists();assert git('rev-parse','HEAD').decode().strip()==H and git('rev-parse','HEAD^{tree}').decode().strip()==TREE;assert not git('status','--porcelain','--untracked-files=normal');assert H.startswith(json.loads((S/'build.json').read_bytes())['version'])
dump(FREEZE,{'head':H,'tree':TREE,'source_root':str(N),'publication':str(S),'source_writer_frozen':True,'no_source_Git_publication_ticket_mutations_during_QA':True,'root_exclusive_GPU_grant':True,'scope':'Target1812 NE separatecards/bodylegs perviewport + unchanged1835 nativeStage3regression; sourcegradeinferred/oneCurreylink0heldnoSpot; no originalcompletion.'})
before_meta=metadata();before_inputs=bindings();before_pub=pubmap();helpers={n:pf(P/n)for n in ['run.py','probe.mjs']};reaper_sha=pf('/workspace/shared/run-with-reaping.py');sid='first_fort_dearborn_small_house_ne';rows=json.loads((S/'data/pictures/1812.json').read_bytes())['by_structure'].get(sid,[]);assert [x['id']for x in rows]==['currey_1912_first_fort_birdseye']and all(not x.get('held')and not x.get('spot')for x in rows);doc=json.loads((S/f'data/sidecars/1812/{sid}.json').read_bytes());assert doc['scene']=='1812'and doc['phase']=='first_fort_1803'and doc['target_date']=='1812-08-14'and doc['grade']['value']=='inferred';assert doc['attributes']['roof_type']['value']=='pyramid'and doc['attributes']['roof_type']['confidence']=='inferred';assert{'currey_1912_first_fort_birdseye','whistler_1808_fort_dearborn_draught'}<=set(c['source_id']for c in doc['citations'])
reader=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import fs from 'node:fs';import{pathToFileURL}from'node:url';const r=process.argv[1];const{readerCopy}=await import(pathToFileURL(r+'/walk/js/reader-text.js'));console.log(JSON.stringify(readerCopy(JSON.parse(fs.readFileSync(r+'/data/sidecars/1812/first_fort_dearborn_small_house_ne.json')),JSON.parse(fs.readFileSync(r+'/data/reader/structures_1812.json'))).research_note));",str(S)],env=E));scratch=Path(tempfile.mkdtemp(prefix='fortq-'));plan={'expected_head':H,'expected_tree':TREE,'source_root':str(N),'site_parent':str(N/'site'),'fort_picture_rows':rows,'expected_picture_ids':[x['id']for x in rows],'expected_picture_count':len(rows),'expected_held_count':0,'fort_entrance':None,'fort_reference_camera':{'eye':[6,8,5],'scope':'Curated exterior inspection offset only; neither sourcecamera nor solvedpicture'},'expected_research_note':reader,'expected_phase':doc['phase'],'expected_target':doc['target_date'],'input_bindings':before_inputs,'source_scope_sha256':sha(canonical(before_inputs)),'metadata':before_meta,'helpers':helpers,'reaper_sha256':reaper_sha,'full_published_members':len(before_pub),'full_published_map_sha256':sha(canonical(before_pub)),'writer_freeze_sha256':pf(FREEZE),'TMP':str(scratch),'scope':'Actual1812 NE current pyramidroof NormalByGrade, exactRecord/evidence/CurreyWhistlercredits/oneCurreysourcelink_0held_noSpot/inferredgrade/groundednativearrival both1280x800and390x780. Separate official1835Stage3both107regression. Directrootpixelsrequired; originalT2387partial.'};dump(P/'PLAN.json',plan);dump(P/'BEFORE-PUBMAP.json',before_pub);plan_sha=pf(P/'PLAN.json')
def guard():
 assert metadata()==before_meta,'Git metadata drift';assert bindings()==before_inputs,'Selected source/published inputs drift';assert pubmap()==before_pub,'Full publication map drift';assert {n:pf(P/n)for n in helpers}==helpers and pf('/workspace/shared/run-with-reaping.py')==reaper_sha;assert pf(P/'PLAN.json')==plan_sha;floor()
def command(cmd,env,receipt,log):
 with log.open('xb')as f:r=subprocess.run(['python','/workspace/shared/run-with-reaping.py',str(receipt),'--','timeout','--signal=TERM','--kill-after=15s','600s','taskset','-c','0-4',*cmd],cwd=A,env=env,stdout=f,stderr=subprocess.STDOUT)
 rr=json.loads(receipt.read_bytes());assert r.returncode==rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup']and rr['interrupted_signal']is None,(r.returncode,rr,str(log));return rr
O.mkdir();K.mkdir();env=dict(E,TMPDIR=str(scratch),TMP=str(scratch),TEMP=str(scratch),NODE_COMPILE_CACHE=str(scratch/'node-cache'));steps=[];native=[];error=None;started=time.monotonic();dump(O/'OWNER.json',{'pid':os.getpid(),'head':H,'plan_sha256':plan_sha,'input_count':len(before_inputs),'pub_members':len(before_pub),'resources':floor()})
try:
 for viewport in ['desktop','mobile']:
  for leg in ['cards','body']:
   guard();t=time.monotonic();label=viewport+'-'+leg;ve=dict(env,FORT_PROBE_PLAN=str(P/'PLAN.json'),FORT_PROBE_OUT=str(O/label),FORT_PROBE_VIEWPORT=viewport,FORT_PROBE_LEG=leg);rr=command(['node',str(P/'probe.mjs')],ve,O/(label+'-REAPER.json'),O/(label+'.log'));result=json.loads((O/label/'RESULT.json').read_bytes());assert result['status']==('ACTUAL_FORT_CARDS_PASS'if leg=='cards'else'ACTUAL_FORT_BODY_PASS');closed=json.loads((O/label/'CLOSURE.json').read_bytes());assert closed['failure']is None and all(not closed[k]for k in ['errors','network','consoleErrors','serverErrors']),closed;guard();steps.append({'viewport':viewport,'leg':leg,'seconds':time.monotonic()-t,'reaper':rr,'status':result['status'],'page_errors':0,'noncancelled_network_errors':0,'console_errors':0,'server_errors':0,'cancelled_requests':closed['cancelled'],'cancelled_request_count':len(closed['cancelled'])});dump(O/'STEPS.json',steps);print(json.dumps({'custom_closed':label,'seconds':steps[-1]['seconds'],'output':str(O/label)}),flush=True)
 assert{(s['viewport'],s['leg'])for s in steps}=={(v,l)for v in ['desktop','mobile']for l in ['cards','body']}
 for viewport in ['mobile','desktop']:
  guard();t=time.monotonic();ve=dict(env,SMOKE_VIEWPORT=viewport,SMOKE_STAGE='3',SMOKE_YEAR='1835',SMOKE_ROOT=str(S),SMOKE_SHOTS=str(K/(viewport+'-shots')));rr=command(['node','tools/smoke_renderer.mjs','--published'],ve,K/(viewport+'-REAPER.json'),K/(viewport+'.log'));text=(K/(viewport+'.log')).read_text(errors='replace');counts=re.findall(r'(\d+) passed, (\d+) failed',text);assert counts and counts[-1]==('107','0')and'SMOKE PASS'in text;guard();native.append({'viewport':viewport,'scene':'1835','seconds':time.monotonic()-t,'passed':107,'failed':0,'reaper':rr});dump(K/'PROGRESS.json',native);print(json.dumps({'native_closed':viewport,'seconds':native[-1]['seconds'],'passed':107,'failed':0}),flush=True)
except BaseException as exc:error=repr(exc);dump(P/'FAILURE.json',{'error':error,'custom':steps,'native':native});print(error,flush=True)
finally:
 try:guard();exact=True
 except BaseException as exc:exact=False;error=(error+'; 'if error else'')+'Final guard:'+repr(exc)
 closure={'status':'FINAL_FIRST_FORT_SPLIT_CUSTOM_NATIVE3_BOTH_CLOSED_PASS'if error is None and len(steps)==4 and len(native)==2 else'NOT_QUALIFIED','head':H,'tree':TREE,'custom_viewports':steps,'native_viewports':native,'selected_input_count':len(before_inputs),'full_published_members':len(before_pub),'full_published_map_sha256':sha(canonical(before_pub)),'source_Git_publication_helpers_plan_exact':exact,'all_owned_process_groups_reaped':all(x['reaper']['all_children_reaped']and not x['reaper']['leftover_cleanup']for x in steps+native),'error':error,'seconds':time.monotonic()-started,'resources':floor()};dump(P/'FINAL-CLOSURE.json',closure);print(json.dumps({'final_status':closure['status'],'error':error}),flush=True)
raise SystemExit(1 if error else 0)
