import {createServer} from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import playwright from '/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js';
const {chromium}=playwright;
const app='/workspace/chicago/chicago/4d',site='/workspace/chicago/site/4d';
const artifacts=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);await fs.mkdir(out,{recursive:true});
const configs=[
 ['child_boy_1904','pa1904_walker_james_r_c1900_arthur_m_walker','Arthur M. Walker',8,'male',1],
 ['child_girl_1904','pa1904_shortall_john_l_c1900_margaret_shortall','Margaret Shortall',8,'female',1],
 ['child_toddler_1904','pa1904_glessner_john','John Glessner',2,'male',.94],
 ['teen_boy_1904','pa1904_longini_a_c1900_marcel_longini','Marcel Longini',14,'male',.98],
 ['teen_girl_1904','pa1904_cunningham_elizabeth_s','Elizabeth S. Cunningham',15,'female',1]
].map(([role,person,name,age,sex,height])=>({role,person,name,age,sex,height}));
const people=JSON.parse(await fs.readFile(path.join(site,'data/sidecars/1904/people.json'))).people;
const header=JSON.parse(await fs.readFile(path.join(site,'data/humans/web/hm08_variation_kit.json')));
const persons=JSON.parse(await fs.readFile(path.join(site,'data/humans/web/hm08_variation_persons.json')));
const assets=new Map();
for(const c of configs){if(!people.some(p=>p.id===c.person))throw Error('Missing actual child card: '+c.person);
 header.assets[c.role]={base_age_years:c.role.startsWith('teen')?15:c.role.includes('toddler')?3:8,sex:c.sex,age_drive:false,height_clip:[.85,1.18]};
 const cut=c.role.includes('toddler')?'toddler_curls_1812':c.sex==='female'?'girl_plait_1812':'short_side_part_1904';
 persons.persons[c.person]={scene:'1904',age:{years:c.age,band:[c.age,c.age],grade:'inferred'},sex:c.sex,
  looks:{grade:'reconstructed',height_scale:c.height,complexion:{drawn:'fair'},hair:{drawn:'mid_brown',cut,facial:[]},eyes:{drawn:'brown'}},
  dress:{asset:c.role,colours:{},hide:[],...(c.sex==='female'?{tail_cm:c.age>12?25:18}:{})}};
 const dir=path.join(artifacts,c.role,'exports/web');for(const f of await fs.readdir(dir))if(f.endsWith('.glb'))assets.set(f,path.join(dir,f));}
const mime={'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.json':'application/json','.bin':'application/octet-stream','.glb':'model/gltf-binary','.wasm':'application/wasm','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2'};
const server=createServer(async(req,res)=>{try{const rel=decodeURIComponent(new URL(req.url,'http://x').pathname);let body,f=path.resolve(site,'.'+rel);if(!f.startsWith(site+'/'))throw Error('outside mirror');
 if(rel.endsWith('/data/humans/web/hm08_variation_kit.json'))body=JSON.stringify(header);
 else if(rel.endsWith('/data/humans/web/hm08_variation_persons.json'))body=JSON.stringify(persons);
 else if(rel.includes('/data/humans/web/')&&assets.has(path.basename(rel)))f=assets.get(path.basename(rel));
 if(!body){if((await fs.stat(f)).isDirectory())f=path.join(f,'index.html');body=await fs.readFile(f);}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(body);
 }catch{res.writeHead(404).end('not found');}});await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({executablePath:'/tmp/routines-browsers/chromium-1194/chrome-linux/chrome',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const sha=x=>createHash('sha256').update(x).digest('hex');const report={source_sha:(await fs.readFile(path.join(artifacts,'source-sha.txt'),'utf8')).trim(),scope:'Actual published town renderer with temporary asset/appearance overlays; review staging at Glessner, not historical placement or production activation. Existing named children, reconstructed clothes and looks. Native pixel ratio.',header_sha256:sha(JSON.stringify(header)),persons_sha256:sha(JSON.stringify(persons)),assets:Object.fromEntries(await Promise.all([...assets].map(async([name,file])=>[name,sha(await fs.readFile(file))]))),viewports:[],errors:[]};
try{for(const[viewport,size]of Object.entries({desktop:{width:1280,height:800},phone:{width:390,height:780}})){
 console.log('boot town',viewport);const page=await browser.newPage({viewport:size,deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(({detail})=>{localStorage.setItem('chicago4d.settings',JSON.stringify({quality:1,detail,timeOfDay:'10:00'}));localStorage.setItem('chicago4d.help.seen','1');},{detail:viewport==='phone'?'balanced':'full'});
 await page.goto(base+'/1904/',{waitUntil:'domcontentloaded',timeout:180000});await page.waitForFunction(()=>window.__chicago4d?.ready,null,{timeout:400000});
 await page.evaluate(()=>{const a=window.__chicago4d;window.__draw=a.renderer.render;a.renderer.render=(_s,c)=>c?.updateMatrixWorld?.();});
 await page.waitForFunction(()=>['welcome','world'].includes(window.__chicago4d.welcome.state),null,{timeout:90000});
 await page.evaluate(()=>{if(window.__chicago4d.welcome.state==='welcome')document.getElementById('home-roam').click();});await page.waitForFunction(()=>window.__chicago4d.welcome.state==='world',null,{timeout:90000});
 await page.evaluate(()=>{const a=window.__chicago4d;a.navigator?.dock?.();a.renderer.setAnimationLoop(null);a.renderer.render=window.__draw;a.world.setSun({date:'1904-07-01',time:'10:00'});a.setFly(true);});
 await page.addStyleTag({content:'body > *:not(#view){visibility:hidden!important}'});
 const row={viewport,size,stills:[]};report.viewports.push(row);
 for(const c of configs){const person=people.find(p=>p.id===c.person);await page.evaluate(({c,person})=>{const a=window.__chicago4d;if(window.__childActor)a.humans.remove(window.__childActor.id);a.humans.holdCrowd([c.person]);
  const rec={id:'review_'+c.role,contract_version:1,scene:'1904',person_id:c.person,appearance:{asset_id:c.role},placement:{local_e:1390.9,local_n:-3226.7,heading_deg:100,anchor:'terrain'},animation:{clip:'idle',loop:true,phase:0},display:'shown',grade:'reconstructed',liberty:'L-prairie-people-3548'};
  window.__childActor=a.humans.add(rec,{person});a.walker.teleport({local_e:1393.85,local_n:-3227.22,yaw_deg:280,altitude_m:1.68});a.humans.update(.1,a.camera,a.walker.state,.1);
 },{c,person});
 await page.waitForFunction(()=>{const a=window.__chicago4d;a.humans.update(.05,a.camera,a.walker.state,.05);return window.__childActor?.body&&window.__childActor.root.visible;},null,{timeout:180000,polling:250});
 for(const[band,distance,time]of[['near',3,null],['far',10,null],...(viewport==='desktop'?Array.from({length:5},(_,i)=>['walk-'+i,3,i*1.25]):[])]){const receipt=await page.evaluate(({distance,time})=>{const a=window.__chicago4d,b=window.__childActor,V=a.camera.position.constructor;const bone=b.root.getObjectByName('head');if(!bone)throw Error('No head');b.root.updateMatrixWorld(true);const head=bone.getWorldPosition(new V()),heading=100*Math.PI/180,e=head.x+Math.sin(heading)*distance,n=-head.z+Math.cos(heading)*distance,look=280;
  a.walker.teleport({local_e:e,local_n:n,yaw_deg:look,altitude_m:1.68,pitch_deg:0});const pitch=Math.atan2(head.y-.2-a.player.y,distance)*180/Math.PI;a.walker.teleport({local_e:e,local_n:n,yaw_deg:look,altitude_m:1.68,pitch_deg:pitch});a.humans.update(.05,a.camera,a.walker.state,.05);if(time!==null&&!b.play('walk',{fade:0,time}))throw Error('Missing walk clip');a.world.follow(a.camera.position);a.renderer.render(a.scene3d,a.camera);
  if(!b.root.visible)throw Error('Prototype hidden');return{clip:time===null?'idle':'walk',clip_time_s:time,head:head.toArray(),distance_m:distance,eye_m:1.68,aim_below_head_m:.2,heading_deg:100,eye_y:a.player.y,age:b.variation?.age,asset:b.instance.appearance.asset_id,visible:b.root.visible,triangles:a.renderer.info.render.triangles,calls:a.renderer.info.render.calls};
 },{distance,time});const file=`${c.role}-${band}-${viewport}.png`;await page.screenshot({path:path.join(out,file),timeout:180000});row.stills.push({file,sha256:sha(await fs.readFile(path.join(out,file))),...c,...receipt});}
 console.log('town capture',viewport,c.role);}
 report.errors.push(...errors.map(error=>({viewport,error})));await page.close();}
 await fs.writeFile(path.join(out,'town-preview.json'),JSON.stringify(report,null,2)+'\n');if(report.errors.length)throw Error(JSON.stringify(report.errors));
}finally{await browser.close();await new Promise(r=>server.close(r));}
