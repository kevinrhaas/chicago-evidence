import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const {chromium}=createRequire('/workspace/chicago/chicago/4d/tools/smoke_renderer.mjs')('playwright');
const root='/workspace/chicago/chicago/4d', out='/tmp/person-moment-fixture';fs.mkdirSync(out,{recursive:true});
const main=fs.readFileSync(path.join(root,'renderers/web/js/main.js'),'utf8');
const selection=main.slice(main.indexOf('  let momentSelectedPerson = null;'),main.indexOf('\n',main.indexOf('\n  }',main.indexOf('  function rememberMomentPerson('))+4));
assert.match(selection,/function rememberMomentPerson/);
const read=main.slice(main.indexOf('  function readMoment() {'),main.indexOf('\n  api.moment = {',main.indexOf('  function readMoment() {')));
assert.match(main,/onPersonSelected: rememberMomentPerson/);
const js=`import * as people from '/renderers/web/js/apps/people-view.js';
import * as inspect from '/renderers/web/js/apps/inspect-view.js';
import home from '/renderers/web/js/apps/home.js';
import {normalMoment,momentLink} from '/renderers/web/js/moment.js';
const YEAR=new URLSearchParams(location.search).get('year');
const dir=await fetch('/data/sidecars/'+YEAR+'/people.json').then(r=>r.json());
const rows=dir.people.filter(r=>r.lives_at&&r.file).slice(0,2);
const get=async p=>fetch('/data/'+p).then(r=>r.ok?r.json():null);
const gateOpen=false,DEG=Math.PI/180;
const walker={state:{e:107,n:-103,pitch:0,flying:false},bearingDeg:180};
const popup={openId:null},navigatorUi={app:'people'},inspectHold=null,targetTag=null;
const loaded={registry:new Map(),scene:{title:'Fixture view'}};
const eraWhere={at:()=>({place:'Fixture place'})},world={sunTime:'12:30',sunDate:YEAR+'-07-01'};
const api={ready:true,season:{current:'summer'}};
${selection}
${read}
api.moment={read:readMoment,link:()=>readMoment()?.url??null,capture:()=>Promise.reject(new Error('No renderer in selection fixture'))};
const actions={peopleDirectory:async()=>dir,onPersonSelected:rememberMomentPerson,
 householdRecord:file=>get('residents_'+YEAR+'/'+file),residentCitations:()=>get('sidecars/'+YEAR+'/residents_sources.json').then(x=>x?.citations),
 inspectSummaries:async()=>null,pictures:async()=>null,cardSections:async()=>({people:'',hasResidents:false,households:[]}),
 record:id=>loaded.registry.get(id)};
const peopleHost=document.querySelector('#people'),inspectHost=document.querySelector('#inspect'),homeHost=document.querySelector('#nav-home');
await people.mount(peopleHost,{scene:{id:YEAR},actions});
home.mount(homeHost,{api});
window.fixture={rows,api,selection:()=>momentSelectedPerson,
 showHome(){peopleHost.hidden=true;inspectHost.hidden=true;homeHost.hidden=false;navigatorUi.app='home';},
 async showInspect(row){const sidecar=await get('sidecars/'+YEAR+'/'+row.lives_at+'.json');loaded.registry.set(row.lives_at,{id:row.lives_at,sidecar});peopleHost.hidden=true;inspectHost.hidden=false;homeHost.hidden=true;navigatorUi.app='inspect';
 await inspect.mount(inspectHost,{selected:row.lives_at,link:{app:'inspect',id:row.lives_at,tab:'people'},scene:{id:YEAR},actions});},
 showPeople(){peopleHost.hidden=false;inspectHost.hidden=true;homeHost.hidden=true;navigatorUi.app='people';},
};`;
const html=`<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/renderers/web/css/inspect.css"><link rel="stylesheet" href="/renderers/web/css/moment.css"><style>body{margin:16px;font:16px sans-serif}button{min-height:36px}[hidden]{display:none!important}</style><script type="importmap">{"imports":{"three":"/renderers/web/vendor/three-0.185.1/three.module.js","three/addons/":"/renderers/web/vendor/three-0.185.1/addons/"}}</script></head><body><div id="people"></div><div id="inspect" hidden></div><div id="nav-home" hidden></div><script type="module" src="/fixture.js"></script></body></html>`;
const server=http.createServer((req,res)=>{const p=new URL(req.url,'http://localhost').pathname;if(p==='/'||p==='/fixture.js'){res.setHeader('Content-Type',p==='/'?'text/html':'text/javascript');return res.end(p==='/'?html:js);}const file=path.resolve(root,'.'+p);if(!file.startsWith(root+'/')){res.writeHead(403);return res.end();}try{fs.accessSync(file);res.setHeader('Content-Type',({'.js':'text/javascript','.json':'application/json','.css':'text/css'})[path.extname(file)]||'application/octet-stream');fs.createReadStream(file).pipe(res);}catch{res.writeHead(404);res.end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});const report={runs:[]};
try{for(const year of ['1812','1904']){const page=await browser.newPage({viewport:{width:390,height:780}});const errors=[];page.on('pageerror',e=>errors.push(e.message));const row={year,checks:[],errors};report.runs.push(row);
await page.goto(origin+'/?year='+year);await page.waitForFunction(()=>window.fixture);
const expected=await page.evaluate(()=>fixture.rows);assert.equal(expected.length,2);
await page.locator('[data-ppl-seg="people"]').click();await page.locator('[data-ppl-open="'+expected[0].id+'"]').first().click();
await page.waitForFunction(id=>window.fixture.selection()?.id===id,expected[0].id);
await page.evaluate(()=>fixture.showHome());await page.locator('#nav-moment summary').click();await page.getByRole('button',{name:'Copy spot link',exact:true}).click();
let m=await page.evaluate(()=>fixture.api.moment.read());assert.equal(m.person,expected[0].id);assert.equal(m.personName,expected[0].name);assert.equal(new URL(await page.locator('.moment-tools input').inputValue()).searchParams.get('person'),expected[0].id);assert.equal(await page.locator('#people').isVisible(),false);row.checks.push({label:'People selected card survives Home; real readMoment caption and copy URL match',pass:true,id:m.person,name:m.personName});
await page.evaluate(row=>fixture.showInspect(row),expected[1]);await page.locator('[data-person-card="'+expected[1].id+'"]').first().click();await page.waitForFunction(id=>fixture.selection()?.id===id,expected[1].id);
await page.evaluate(()=>fixture.showHome());await page.getByRole('button',{name:'Copy spot link',exact:true}).click();
m=await page.evaluate(()=>fixture.api.moment.read());assert.equal(m.person,expected[1].id);assert.equal(m.personName,expected[1].name);assert.equal(new URL(await page.locator('.moment-tools input').inputValue()).searchParams.get('person'),expected[1].id);assert.equal(await page.locator('#inspect').isVisible(),false);assert.equal(await page.locator('#people .insp-person-card').count(),1);row.checks.push({label:'Inspect selection replaces previous hidden People card in Home metadata and copied URL',pass:true,id:m.person,name:m.personName});
assert.deepEqual(errors,[]);await page.screenshot({path:path.join(out,year+'-home.png')});await page.close();}
}catch(e){report.failure=String(e.stack||e);process.exitCode=1;}finally{fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2));await browser.close();await new Promise(r=>server.close(r));}console.log(JSON.stringify(report,null,2));
