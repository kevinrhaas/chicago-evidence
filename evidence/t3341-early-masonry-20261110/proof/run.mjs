import fs from 'node:fs';
import {chromium} from '/tmp/chicago-browser-tools/node_modules/playwright/index.mjs';
const dir='/tmp/nov10-brick-3341/proof';const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const rows=[];
try {
 for(const [name,query] of [['after-full',''],['before-flat','?before'],['after-light','?light'],['after-webp','?fallback']]) {
  const context=await browser.newContext({viewport:{width:1280,height:800}});const page=await context.newPage();const errors=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  await page.goto('http://127.0.0.1:4211/'+query,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.PROOF,{timeout:120000});const result=await page.evaluate(()=>window.PROOF);
  await page.screenshot({path:`${dir}/${name}.png`});rows.push({name,query,result,errors});fs.writeFileSync(`${dir}/RESULTS.json`,JSON.stringify(rows,null,2));console.log(name,result.status,JSON.stringify(result.errors??result.error??null),errors.length);
  await context.close();if(result.status!=='READY'||errors.length)throw new Error(`Failed ${name}`);
 }
} finally {await browser.close()}
