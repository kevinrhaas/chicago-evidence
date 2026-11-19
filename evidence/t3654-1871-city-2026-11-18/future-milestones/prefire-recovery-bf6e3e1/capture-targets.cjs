const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require('playwright');
const root = '/tmp/t3654-prefire-research-worktree/site';
const mime = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.jpg':'image/jpeg'};
for (const stem of ['chamber-source','alexander']) for (const size of ['mobile','desktop']) {
  const file=path.join(__dirname,`${stem}-${size}.png`);
  if(fs.existsSync(file)) fs.renameSync(file,file.replace('.png','.misframed.png'));
}
const server = http.createServer((req,res) => {
  const file = path.resolve(root, '.' + new URL(req.url, 'http://local').pathname);
  if (!file.startsWith(root + '/') || !fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404).end(); return; }
  res.writeHead(200, {'content-type':mime[path.extname(file)] || 'application/octet-stream'});
  fs.createReadStream(file).pipe(res);
});
(async () => {
  await new Promise(r => server.listen(0,'127.0.0.1',r));
  const base=`http://127.0.0.1:${server.address().port}/pre-fire/viewer/`;
  const browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true});
  const evidence=[];
  try {
    for(const [size,width,height] of [['mobile',390,780],['desktop',1280,800]]) {
      const context=await browser.newContext({viewport:{width,height},reducedMotion:'reduce'});
      const page=await context.newPage();
      for(const [stem,id] of [['chamber-source','source-illustrated-chamber-8'],['alexander','record-worker-alexander-jc-carpenter']]) {
        await page.goto(base+'notebook.html#'+id);
        await page.waitForSelector('#'+id+'[open]');
        await page.evaluate(async () => { await document.fonts.ready; document.documentElement.style.scrollBehavior='auto'; });
        if(stem==='chamber-source') {
          await page.waitForFunction(id=>document.querySelector('#'+id+' img')?.naturalWidth>0,id);
          await page.locator('#'+id+' img').evaluate(img=>img.decode());
        }
        const rects=await page.evaluate(async id => {
          const target=document.getElementById(id);
          target.scrollIntoView({behavior:'instant',block:'start'});
          const boxes=[];
          for(let frame=0;frame<5;frame++) {
            await new Promise(requestAnimationFrame);
            const r=target.getBoundingClientRect();boxes.push({top:r.top,bottom:r.bottom,left:r.left,right:r.right});
          }
          return boxes;
        },id);
        const rect=rects.at(-1);
        assert.ok(rect.top>=-1 && rect.top<height/3,JSON.stringify({id,rect,height}));
        assert.ok(rect.left>=-1 && rect.right<=width+1,JSON.stringify({id,rect,width}));
        assert.ok(rects.every(r=>Math.abs(r.top-rect.top)<1),'Target position changed over five frames');
        assert.match(await page.locator('#'+id).innerText(),stem==='chamber-source'?/Chamber of Commerce lithograph/:/J\. C\. Alexander/);
        const file=path.join(__dirname,`${stem}-${size}.png`);
        await page.screenshot({path:file});
        evidence.push({file,id,viewport:{width,height},rects,fontsReady:true,imageDecoded:stem==='chamber-source'});
        console.log('PASS stable visible target '+size+' '+id+' at top='+rect.top);
      }
      await context.close();
    }
    fs.writeFileSync(path.join(__dirname,'capture-targets-evidence.json'),JSON.stringify(evidence,null,2)+'\n');
  } finally {await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;server.close();});
