from pathlib import Path
import json,hashlib,shutil,difflib,datetime
OLD=Path('/workspace/shared/T2794-LAMP-RESUME-20261023-2245/SOURCE8-V17-V18')
OUT=Path('/workspace/shared/T2794-LAMP-RESUME-20261023-2245/SOURCE8-RESOURCE-FALLBACK-PREP')
REF=Path('/tmp/T2800-CHROME-RESOURCE-LAUNCH-FALLBACK-SOURCE-HELD-20261023')
INI=Path('/tmp/T2794-V18-SOURCE8-SWIFT1-ROOT-REVIEW-20261023/SwiftShader.ini')
OUT.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
orig_capture=(OLD/'capture.cjs').read_text();orig_owner=(OLD/'run_once.py').read_text()
for n in ['fixture','node_modules']:shutil.copytree(OLD/n,OUT/n)
shutil.copy2(OLD/'source-extension.js',OUT/'source-extension.js')
(OUT/'source-proof').mkdir()
for n in ['docs__RuntimeConfiguration.md','chromium__cc__base__switches.cc','chromium__content__public__common__content_switches.cc','src__System__SwiftConfig.cpp','src__System__SwiftConfig.hpp','MANIFEST.json']:
 shutil.copy2(REF/n,OUT/'source-proof'/n)
shutil.copy2(REF/'SwiftShader.ini.PROPOSAL',OUT/'SwiftShader.ini.PROPOSAL')
assert sha(OUT/'SwiftShader.ini.PROPOSAL')=='228340162de0f5f5ac4ca228a89f6256cc8cc9cdaee81b618ebceec2f1b2dba8'
assert not INI.exists(),'Planned private runtime must not preexist during source-only preparation'
old_line=" browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox'],timeout:15000});const bindings=new Map();"
new_lines=""" // SOURCE-ONLY scheduling variant: a real default launch failed before any page.
 // This binding changes launch scheduling only; no FPS/performance equivalence is claimed.
 const released=JSON.parse(fs.readFileSync(path.join(ROOT,'ROOT-RELEASE.json'),'utf8'));
 const fallback=released.launcher_resource_fallback;
 need(released.current_root_resource_variant_release===true&&released.execution_authorized===true&&fallback?.kind==='renderer1-raster1-swift1','Current ROOT-reviewed resource-variant execution required');
 const inputs=JSON.parse(fs.readFileSync(path.join(ROOT,'INPUTS.json'),'utf8'));
 const pinFor=p=>inputs.resource_fallback_inputs.find(row=>row.absolute_path===p);
 const failed=pinFor(fallback.default_launch_failure_receipt);
 need(failed&&hash(failed.absolute_path)===failed.sha256,'Exact original default-launch failure must be pinned');
 const failure=JSON.parse(fs.readFileSync(failed.absolute_path,'utf8'));
 need(failure.pass===false&&failure.rows.length===0&&String(failure.error).includes('pthread_create'),'Observed before-page default thread-exhaustion failure required');
 const iniPath=path.resolve(fallback.swiftshader_ini??''),iniPin=pinFor(iniPath);
 need(iniPath.startsWith('/tmp/')&&path.basename(iniPath)==='SwiftShader.ini'&&fs.realpathSync(iniPath)===iniPath&&!fs.lstatSync(iniPath).isSymbolicLink()&&!fs.lstatSync(path.dirname(iniPath)).isSymbolicLink(),'Private real /tmp SwiftShader.ini required');
 need((fs.statSync(path.dirname(iniPath)).mode&0o077)===0&&(fs.statSync(iniPath).mode&0o077)===0,'Private INI directory/file permissions required');
 need(iniPin&&iniPin.bytes===26&&iniPin.sha256==='228340162de0f5f5ac4ca228a89f6256cc8cc9cdaee81b618ebceec2f1b2dba8'&&hash(iniPath)===iniPin.sha256,'Exact private SwiftShader ThreadCount1 input required');
 process.chdir(path.dirname(iniPath)); // All fixture/caller/output paths above are already absolute.
 result.launcherResourceFallback={kind:fallback.kind,default_launch_failure_receipt:failed.absolute_path,default_launch_failure_sha256:failed.sha256,swiftshader_ini:iniPath,swiftshader_ini_sha256:iniPin.sha256,browserChildCwdRequested:process.cwd(),configuration_effect_observed:false,performance_equivalence_claimed:false};save();
 browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--renderer-process-limit=1','--num-raster-threads=1'],timeout:15000});const bindings=new Map();
 // Observation only: read this Node child's own descendant tree, never PID1/other agents.
 try{const seen=new Set(),todo=[process.pid],rows=[];while(todo.length&&seen.size<128){const pid=todo.shift();if(seen.has(pid))continue;seen.add(pid);try{const status=fs.readFileSync(`/proc/${pid}/status`,'utf8'),threads=Number(status.match(/^Threads:\\s+(\\d+)/m)?.[1]??0);rows.push({pid,cwd:fs.readlinkSync(`/proc/${pid}/cwd`),threads});for(const tid of fs.readdirSync(`/proc/${pid}/task`)){try{for(const child of fs.readFileSync(`/proc/${pid}/task/${tid}/children`,'utf8').trim().split(/\\s+/).filter(Boolean))todo.push(Number(child))}catch{}}}catch{}}result.launcherResourceFallback.observedOwnProcessInventory=rows;save()}catch(error){result.launcherResourceFallback.observationError=String(error);save()}
""".rstrip('\n')
assert orig_capture.count(old_line)==1
capture=orig_capture.replace(old_line,new_lines)
assert capture.replace(new_lines,old_line)==orig_capture,'Exact inverse capture launch-only replacement'
(OUT/'capture.cjs').write_text(capture)
needle="need(release.get('authorization_owner')=='root' and release.get('release_preview') is True and release.get('current_root_exclusive_browser_slot') is True,'Current root exclusive source8 browser release required')"
replacement=needle+"\nneed(release.get('current_root_resource_variant_release')is True and release.get('execution_authorized')is True,'ROOT-reviewed resource-variant release required; template is not execution authorization')"
assert orig_owner.count(needle)==1
owner=orig_owner.replace(needle,replacement)
needle2="need(not(HERE/'RUN-INTENT.json').exists() and not(HERE/'actual').exists(),'One intent/output exists; do not blindly replay')"
replacement2="""for row in inputs['resource_fallback_inputs']:
 file=Path(row['absolute_path']);need(file.is_absolute() and file.is_file() and file.stat().st_size==row['bytes'] and sha(file)==row['sha256'],'Pinned original failure/private INI/runtime drift: '+str(file))
fallback=release.get('launcher_resource_fallback',{})
need(fallback.get('kind')=='renderer1-raster1-swift1' and fallback.get('default_launch_failure_receipt')==inputs['default_launch_failure_receipt'] and fallback.get('swiftshader_ini')==inputs['private_swiftshader_ini'],'Exact current resource-variant binding required')
failed=json.loads(Path(fallback['default_launch_failure_receipt']).read_text())
need(failed.get('pass')is False and failed.get('rows')==[] and 'pthread_create'in str(failed.get('error')),'Original before-page thread-exhaustion failure required')
"""+needle2
assert owner.count(needle2)==1
owner=owner.replace(needle2,replacement2)
assert owner.replace(replacement2,needle2).replace(replacement,needle)==orig_owner,'Exact inverse owner binding-only replacement'
compile(owner,str(OUT/'run_once.py'),'exec')
(OUT/'run_once.py').write_text(owner)
for name,a,b in [('CAPTURE-LAUNCH-ONLY.diff',orig_capture,capture),('OWNER-BINDING-ONLY.diff',orig_owner,owner)]:
 (OUT/name).write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='default-failed/'+('capture.cjs'if'CAPTURE'in name else'run_once.py'),tofile='resource-fallback/'+('capture.cjs'if'CAPTURE'in name else'run_once.py'))))
readme='''# Source-only source8 V17/V18 scheduling fallback; NOT EXECUTED

The original source8 attempt failed before a page/request/capture due Chromium pthread_create EAGAIN. That actual failure and its clean owned cleanup remain preserved. This new unit adds official renderer-process-limit1/num-raster-threads1 scheduling plus the existing horse-style ANGLE SwiftShader backend, with a private pinned /tmp SwiftShader.ini requesting [Processor] ThreadCount=1. The runtime INI has NOT been created. ROOT must review the exact diff/pins before creating the private file and issuing a separate true release. The false template is not authorization.

Original camera, light, crop, viewport/DPR, source/model pins, depth projection, full bounds/pole visibility, all render and disposal assertions, 165s browser and175s whole-owner deadlines remain byte-exact. No single-process, in-process GPU, site-isolation changes, CPU affinity, system or process tuning. Worker/backend scheduling differs; no FPS/performance equivalence is claimed. Requested INI configuration is not proof the GPU process consumed it; actual descendant cwd/thread observations are receipt-only and cannot relax product assertions.

CAPTURE-LAUNCH-ONLY.diff and OWNER-BINDING-ONLY.diff are exact inverse-proven patches against the preserved failed source. All fixture and Playwright runtime files are copied byte-exact. source-extension.js and every rendering/camera asset are unchanged. No browser launch, server, app/ticket/ref mutation or process intervention ran during preparation.

Root-only next steps after source review: create the private /tmp directory0700 and exact SwiftShader.ini0600 from SwiftShader.ini.PROPOSAL; pin-check it; copy ROOT-RELEASE-TEMPLATE.json to ROOT-RELEASE.json and set only reviewed release/execution/exclusive-slot fields true; execute one owner through the approved own-subreeper wrapper. No automatic retries. Preserve any failure and release the exclusive browser slot after cleanup. Existing owner and outer subreaper lifecycle are retained.

Official source snapshots and their upstream URLs are recorded in SOURCE-ONLY-PROOF.json/source-proof. Chromium core args are supported flags, not invented worker switches.
'''
(OUT/'README.md').write_text(readme)
old_inputs=json.loads((OLD/'INPUTS.json').read_text())
files=[]
for folder in ['fixture','node_modules']:
 for p in sorted((OUT/folder).rglob('*')):
  if p.is_file():files.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p)})
assert files==old_inputs['files'],'All original fixture/runtime file pins unchanged'
external=[]
for p in [OLD/'actual/receipt.json',OLD/'SERVER-CLOSED.json',OLD/'COMPACT-ACTUAL-NONPASS.json',OLD.parent/'source8-one-actual.cleanup.json',Path('/usr/lib/chromium/libvk_swiftshader.so'),Path('/usr/lib/chromium/libEGL.so'),Path('/usr/lib/chromium/libGLESv2.so'),Path('/usr/lib/chromium/vk_swiftshader_icd.json')]:
 external.append({'absolute_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
external.append({'absolute_path':str(INI),'bytes':26,'sha256':sha(OUT/'SwiftShader.ini.PROPOSAL'),'not_created_at_preparation':True})
inputs={'scope':'Source-only one resource scheduling fallback for exact V17/V18 source8 near comparison; no execution','files':files,'runtime_binaries':old_inputs['runtime_binaries'],'resource_fallback_inputs':external,'default_launch_failure_receipt':str(OLD/'actual/receipt.json'),'private_swiftshader_ini':str(INI)}
(OUT/'INPUTS.json').write_text(json.dumps(inputs,indent=2)+'\n')
old_prep=json.loads((OLD/'PREPARED-CALLER.json').read_text())
prep={**old_prep,'state':'SOURCE_ONLY_RESOURCE_FALLBACK_REQUIRES_ROOT_REVIEW','caller_files':[{'path':n,'bytes':(OUT/n).stat().st_size,'sha256':sha(OUT/n)}for n in ['capture.cjs','run_once.py','source-extension.js','README.md','SwiftShader.ini.PROPOSAL']],'no_performance_equivalence_claim':True}
(OUT/'PREPARED-CALLER.json').write_text(json.dumps(prep,indent=2)+'\n')
release={'authorization_owner':'root','release_preview':False,'current_root_exclusive_browser_slot':False,'current_root_resource_variant_release':False,'execution_authorized':False,'inputs_manifest_sha256':sha(OUT/'INPUTS.json'),'prepared_manifest_sha256':sha(OUT/'PREPARED-CALLER.json'),'launcher_resource_fallback':{'kind':'renderer1-raster1-swift1','default_launch_failure_receipt':str(OLD/'actual/receipt.json'),'swiftshader_ini':str(INI)},'targeted_app_yard_or_photographic_acceptance':False,'no_FPS_or_performance_equivalence_claim':True,'no_retry':True,'review_required':'Root must inspect exact source/pins and create private runtime before an explicit once-only release'}
(OUT/'ROOT-RELEASE-TEMPLATE.json').write_text(json.dumps(release,indent=2)+'\n')
proof={'state':'SOURCE_ONLY_PREPARED_NOT_EXECUTED','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'default_failed_unit_preserved':str(OLD),'default_caller_sha256':sha(OLD/'capture.cjs'),'default_owner_sha256':sha(OLD/'run_once.py'),'fallback_caller_sha256':sha(OUT/'capture.cjs'),'fallback_owner_sha256':sha(OUT/'run_once.py'),'capture_inverse_exact':True,'owner_inverse_exact':True,'all_541_fixture_runtime_files_exact':True,'owner_syntax_compile':'PASS','capture_syntax':'NOT_YET_CHECKED','browser_launches':0,'server_launches':0,'private_INI_created':False,'root_release_template_false':True,'original_165s_browser_175s_owner_limits_unchanged':True,'no_camera_light_crop_assertion_changes':True,'no_FPS_performance_equivalence_claim':True,'reference_source_root':str(REF),'official_references':{'chromium__content__public__common__content_switches.cc':'https://raw.githubusercontent.com/chromium/chromium/main/content/public/common/content_switches.cc','chromium__cc__base__switches.cc':'https://raw.githubusercontent.com/chromium/chromium/main/cc/base/switches.cc','docs__RuntimeConfiguration.md':'https://raw.githubusercontent.com/google/swiftshader/master/docs/RuntimeConfiguration.md','src__System__SwiftConfig.hpp':'https://raw.githubusercontent.com/google/swiftshader/master/src/System/SwiftConfig.hpp','src__System__SwiftConfig.cpp':'https://raw.githubusercontent.com/google/swiftshader/master/src/System/SwiftConfig.cpp'},'reference_snapshot_files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted((OUT/'source-proof').iterdir())},'root_execution_command':['python3','/workspace/shared/run_owned_horse_cli_20261023.py',str(OUT/'one-root-released-fallback.log'),'195',str(OUT),'/workspace/shared/w01-python-sum-recovery-20261022/venv311/bin/python',str(OUT/'run_once.py'),'--release',str(OUT/'ROOT-RELEASE.json')]}
(OUT/'SOURCE-ONLY-PROOF.json').write_text(json.dumps(proof,indent=2)+'\n')
manifest={str(p.relative_to(OUT)):{'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(OUT.rglob('*'))if p.is_file()and'node_modules'not in p.parts and'fixture'not in p.parts}
(OUT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'prepared':str(OUT),'source_only':True,'caller':proof['fallback_caller_sha256'],'owner':proof['fallback_owner_sha256'],'input_manifest':sha(OUT/'INPUTS.json'),'prepared_manifest':sha(OUT/'PREPARED-CALLER.json'),'private_ini_absent':not INI.exists(),'copied_exact_inputs':len(files)},indent=2))
