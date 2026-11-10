import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
const require=createRequire('/tmp/chicago-browser-tools/package.json');
const {chromium}=require('playwright');
const expected=process.argv[2];if(!expected)throw Error('Pass the actual combined published build prefix');
const base=process.env.QA_BASE||'http://127.0.0.1:4207/4d/';
const out='/tmp/nov10-t2023-evidence/ui-label-fix';fs.mkdirSync(out,{recursive:true});
const ids=['rc_thayer_warren','rc_wadsworth_george','rc_mahoney_michael','rc_rice_reuben','rc_chevalier_archange','rc_ingalls_lydia','rc_bourassa_victoire','rc_bourassa_marie','rc_bourassa_archange','rc_hastings_mary','rc_robillard_catherine','rc_stiles_lydia','rc_wadsworth_almira'];
const build=await(await fetch(new URL('build.json',base))).json();if(!String(expected).startsWith(build.version)&&!String(build.version).startsWith(expected))throw Error('Published build mismatch '+JSON.stringify(build));
const res=await fetch(new URL('data/sidecars/1835/people.json',base)),body=await res.text(),people=JSON.parse(body).people;
const selected=people.filter(p=>ids.includes(p.id));if(selected.length!==13||selected.some(p=>p.grade!=='reconstructed'||p.how_known!=='reconstructed'))throw Error('Published invented-name labels are not all corrected');
const result={build,expected,actual_published_people_sha256:crypto.createHash('sha256').update(body).digest('hex'),all13_published_categories_correct:selected.map(({id,name,grade,how_known})=>({id,name,grade,how_known})),results:[],failure:null};
fs.writeFileSync(path.join(out,'RESULTS.json'),JSON.stringify(result,null,2));
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader']});
try{
 for(const [label,viewport,detail] of [['phone',{width:390,height:780},'light'],['desktop',{width:1280,height:800},'full']]){
  const context=await browser.newContext({viewport,deviceScaleFactor:1,isMobile:label==='phone',hasTouch:label==='phone'});const page=await context.newPage();page.setDefaultTimeout(90000);const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.addInitScript(d=>localStorage.setItem('chicago4d.settings',JSON.stringify({detail:d})),detail);
  console.log(label,'actual normal boot starting');await page.goto(base+'1835/',{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.__chicago4d?.ready||window.__chicago4d?.error,null,{timeout:240000,polling:500});
  await page.waitForFunction(()=>__chicago4d.welcome.state==='welcome',null,{timeout:240000,polling:500});
  await page.evaluate(()=>{const a=__chicago4d;if(a.error)throw Error(a.error);if(!a.welcome.enter('spawn'))throw Error('normal entry failed');document.exitPointerLock?.();document.getElementById('control-help-gotit')?.click();a.renderer.setAnimationLoop(null);a.step();});
  await page.evaluate(async()=>{const a=__chicago4d;a.hud.setPanel(true);a.hud.selectTab('people');await a.people.open('rc_chevalier_archange');});
  await page.waitForFunction(()=>Array.from(document.querySelectorAll('.people-card')).some(e=>e.innerText.includes('Archange Chevalier')&&e.innerText.includes('reconstructed identity')));
  const card=await page.evaluate(()=>Array.from(document.querySelectorAll('.people-card')).find(e=>e.innerText.includes('Archange Chevalier'))?.innerText||'');
  if(card.includes('named in a source')||!card.includes('reconstructed identity'))throw Error('Actual person card still contradicts the model identity');
  await page.screenshot({path:path.join(out,label+'-archange-reconstructed-identity.png')});fs.writeFileSync(path.join(out,label+'-archange-card.txt'),card);
  result.results.push({label,viewport,detail,normal_boot:true,actual_reconstructed_identity_label:true,false_source_named_label_absent:true,page_errors:errors});fs.writeFileSync(path.join(out,'RESULTS.json'),JSON.stringify(result,null,2));if(errors.length)throw Error(JSON.stringify(errors));await context.close();console.log(label,'corrected actual card PASS');
 }
}catch(e){result.failure=String(e);console.error(result.failure);}finally{await browser.close();fs.writeFileSync(path.join(out,'RESULTS.json'),JSON.stringify(result,null,2));}
if(result.failure)process.exit(1);
