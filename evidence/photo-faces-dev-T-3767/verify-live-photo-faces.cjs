const fs=require('node:fs'),crypto=require('node:crypto'),assert=require('node:assert/strict'),{chromium}=require('playwright');
const origin=process.env.PHOTO_VERIFY_ORIGIN||'https://dev.chicago.polecat.live/4d/dev/',sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const get=async path=>{const r=await fetch(new URL(path,origin),{headers:{'Cache-Control':'no-cache'}});assert(r.ok,`${r.status}: ${path}`);return Buffer.from(await r.arrayBuffer());};
(async()=>{
 const build=JSON.parse(await get('build.json'));if(!process.env.PHOTO_VERIFY_ORIGIN)assert.equal(build.tier,'dev');
 const files=[['walk/js/human-variation.js','renderers/web/js/human-variation.js'],['walk/js/human-skin.js','renderers/web/js/human-skin.js'],['walk/js/photo-face-pages.js','renderers/web/js/photo-face-pages.js']];
 for(const [remote,local]of files)assert.equal(sha(await get(remote)),sha(fs.readFileSync(local)),`served ${remote} matches the checked source`);
 const libraries=[];
 for(const name of ['pilot','children']){
  const base=`data/humans/web/photo_faces/${name}/`,blob=await get(base+'review.json');
  const lib=JSON.parse(blob);assert.deepEqual(lib,JSON.parse(fs.readFileSync(`assets/humans/web/photo_faces/${name}/review.json`)),`published ${name} catalog retains every source field through JSON minification`);
  assert.equal(lib.review_only,false);assert.equal(lib.activation.requested_by,'owner');assert.deepEqual(lib.activation.years,['1812','1835','1871','1904']);
  for(const t of [lib.textures.light,...lib.pages.map(p=>p.textures.full)])assert.equal(sha(await get(base+t.file)),t.sha256,`served ${name}/${t.file} hash`);
  libraries.push({name,faces:lib.faces.length,pages:lib.pages.length});
 }
 const proxyUrl=process.env.HTTPS_PROXY?new URL(process.env.HTTPS_PROXY):null;
 const proxy=proxyUrl?{server:proxyUrl.origin,...(proxyUrl.username?{username:decodeURIComponent(proxyUrl.username),password:decodeURIComponent(proxyUrl.password)}:{}),bypass:process.env.NO_PROXY||''}:undefined;
 const b=await chromium.launch({proxy,headless:true,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  const p=await b.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto(origin+'data/humans/web/hm08_variation_persons.json',{timeout:180000});
  await p.addScriptTag({type:'importmap',content:JSON.stringify({imports:{three:origin+'walk/vendor/three-0.185.1/three.module.js'}})});
  const coverage=await p.evaluate(async origin=>{
   const V=await import(origin+'walk/js/human-variation.js'),base=origin+'data/humans/web/';
   const kit=await V.loadVariationKit(base);if(!kit?.photoFaces||!kit.photoChildren)throw Error('default libraries did not load');
   const main=(await(await fetch(base+'hm08_variation_persons.json')).json()).persons,out=[];
   for(const year of ['1812','1835','1871','1904']){
    const own=['1835','1871'].includes(year)?(await(await fetch(base+`hm08_variation_persons_${year}.json`)).json()).persons:{};
    const records={...own,...main},inside=await(await fetch(origin+`data/humans/inside_${year}.json`)).json();let adults=0,children=0,protectedCount=0;
    for(const row of inside.people??[]){if(!row.asset_id)continue;const record=records[row.person];
     if(!record)throw Error('missing record '+row.person);
     const v=V.personVariation({kit,key:row.person,record,assetId:row.asset_id,sceneYear:Number(year)});
     if(record.face?.values||record.skin||record.looks?.face_pick){if(v.photoFace)throw Error('personal face overwritten');protectedCount++;}
     else if(v.age<18){if(v.photoFace?.population!=='child'||!v.photoFace.texture_only)throw Error('child missing '+row.person);children++;}
     else{if(!v.photoFace||v.photoFace.age<18)throw Error('adult missing '+row.person);adults++;}
    }
    out.push({year,adults,children,protected:protectedCount});
   }return out;
  },origin);
  assert(coverage.every(y=>y.adults>0&&y.children>0));assert.equal(errors.length,0,errors.join('\n'));
  fs.writeFileSync(process.env.PHOTO_VERIFY_REPORT||'work/dev-photo-live-verification.json',JSON.stringify({build,libraries,coverage,errors,servedModulesMatchCheckedSource:true,allCrowdAndDetailPagesMatch:true},null,2));
  console.log(JSON.stringify({build,libraries,coverage}));console.log('PASS: served modules, default adult and child libraries, all 17 detail pages and actual inside populations in all four years');
 }finally{await b.close();}
})().catch(e=>{console.error(e);process.exit(1)});
