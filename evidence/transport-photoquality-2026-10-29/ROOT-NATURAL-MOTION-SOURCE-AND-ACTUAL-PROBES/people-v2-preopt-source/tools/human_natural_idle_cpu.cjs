// SPDX-License-Identifier: GPL-3.0-or-later
// Actual native loader/mixer/skinning inspection. No renderer or WebGL.
const fs=require('node:fs/promises'),path=require('node:path'),http=require('node:http'),crypto=require('node:crypto');
const {chromium}=require('playwright');
const APP=path.resolve(__dirname,'..'),args=process.argv.slice(2);
function arg(name){const i=args.indexOf(name);if(i<0||!args[i+1])throw Error(`${name} required`);return path.resolve(args[i+1]);}
const candidate=arg('--candidate'),output=arg('--output'),controlOldIdle=args.includes('--control-old-idle'),witnessOnly=args.includes('--clearance-witness'),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
let browser,server;const report={scope:'Actual native GLTFLoader/Meshopt/AnimationMixer/skin readback without WebGL; no visual/photographic or full continuous garment proof',files:[],passed:false};
(async()=>{
  await fs.mkdir(output,{recursive:false});
  const recipe=JSON.parse(await fs.readFile(path.join(APP,'data/humans/animations/natural-standing-v1.json'),'utf8'));
  const derivation=JSON.parse(await fs.readFile(path.join(candidate,'DERIVATION.json'),'utf8'));
  if(derivation.generator_sha256!==sha(await fs.readFile(path.join(APP,'tools/human_natural_idle.py')))||derivation.recipe_sha256!==sha(await fs.readFile(path.join(APP,'data/humans/animations/natural-standing-v1.json'))))throw Error('Candidate generation implementation/recipe mismatch');
  const before={};for(const row of recipe.parents){const p=path.join(candidate,row.file);before[row.file]=sha(await fs.readFile(p));}
  for(const row of derivation.files)if(before[row.file]!==row.sha256)throw Error('Candidate differs from actual derivation receipt');
  const implementation=['tools/human_natural_idle.py','tools/human_natural_idle_cpu.html','tools/human_natural_idle_cpu.cjs','data/humans/animations/natural-standing-v1.json','renderers/web/js/humans.js','renderers/web/js/main.js'];
  const pins={};for(const p of [...implementation,...recipe.parents.map(r=>r.file)])pins[p]=sha(await fs.readFile(path.join(APP,p)));
  report.implementation_and_parent_pins_before=pins;
  const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.wasm':'application/wasm','.glb':'model/gltf-binary'};
  server=http.createServer(async(req,res)=>{try{const url=new URL(req.url,'http://local'),isCandidate=url.pathname.startsWith('/candidate/'),root=isCandidate?candidate:APP,relative=isCandidate?url.pathname.slice(11):url.pathname.slice(1),file=path.resolve(root,decodeURIComponent(relative));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}res.setHeader('Content-Type',mime[path.extname(file)]??'application/octet-stream');res.end(await fs.readFile(file));}catch{res.writeHead(404).end();}});
  await new Promise(r=>server.listen(0,'127.0.0.1',r));
  browser=await chromium.launch({executablePath:process.env.PW_EXECUTABLE||undefined,args:['--no-sandbox','--disable-gpu']});
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.stack??e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  await page.goto(`http://127.0.0.1:${server.address().port}/tools/human_natural_idle_cpu.html`);await page.waitForFunction(()=>window.cpuReady);
  report.lifecycle=await page.evaluate(()=>inspectLifecycle());
  if(witnessOnly)report.clearance_witness=await page.evaluate(file=>inspectClearanceWitness(file),recipe.parents[0].file);
  else for(const row of recipe.parents){console.log(`native CPU inspect ${row.file}${controlOldIdle?' ORIGINAL IDLE CONTROL':''}`);const result=await page.evaluate(({file,control})=>inspectNatural(file,control),{file:row.file,control:controlOldIdle});report.files.push({...result,sha256:before[row.file]});await fs.writeFile(path.join(output,'RESULT.json'),JSON.stringify(report,null,2)+'\n');if(!result.passed||controlOldIdle)break;}
  report.errors=errors;report.source_guards={};
  for(const row of recipe.parents){const exact=sha(await fs.readFile(path.join(candidate,row.file)))===before[row.file];report.source_guards[row.file]=exact;if(!exact)throw Error('Candidate changed during actual readback');}
  report.implementation_and_parent_pins_after={};for(const p of Object.keys(pins)){const hash=sha(await fs.readFile(path.join(APP,p)));report.implementation_and_parent_pins_after[p]=hash;if(hash!==pins[p])throw Error('Implementation/parent changed during native readback: '+p);}
  report.diagnostic_only=controlOldIdle||witnessOnly;
  report.passed=!controlOldIdle&&!witnessOnly&&errors.length===0&&report.lifecycle.passed&&report.files.length===recipe.parents.length&&report.files.every(r=>r.passed&&r.webgl_requests===0);
  if(!report.passed)process.exitCode=1;
})().catch(e=>{report.error=e.stack??String(e);process.exitCode=1;}).finally(async()=>{await browser?.close();if(server)await new Promise(r=>server.close(r));await fs.writeFile(path.join(output,'RESULT.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:report.passed,files:report.files.length,error:report.error??null}));});
