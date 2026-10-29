// Source-only policy arithmetic, not a native-render/physical/camera qualification.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const root='/tmp/chicago-wagon-20261029/chicago/4d';
const sourcePath=path.join(root,'renderers/web/js/railway.js'),dataPath=path.join(root,'data/railway/1904_context.json');
const source=fs.readFileSync(sourcePath,'utf8'),data=JSON.parse(fs.readFileSync(dataPath,'utf8'));
assert(source.includes("sceneId === '1904' ? '1904_context' : sceneId"));
const rng=Function(source.slice(source.indexOf('function rng('),source.indexOf('/* -------------------------------------------------------------------------- */\n/* a track'))+';return rng;')();
const trackPath=Function(source.slice(source.indexOf('function trackPath('),source.indexOf('/* -------------------------------------------------------------------------- */\n/* draped ribbons'))+';return trackPath;')();
const tracks=data.tracks.filter(t=>t.centreline_local_m.length>=2);
// Native grade affects only path.y. Zone eSum/eCount and distance below read
// only e/n, so a flat terrain stub avoids starting the real terrain/renderers.
const paths=tracks.map(t=>trackPath(t.centreline_local_m,{surfaceHeight:()=>0}));
const zoneM=Number(source.match(/const ZONE_M = ([\d.]+);/)[1]);
const reach=Function('return '+source.match(/const REACH = (\{[\s\S]*?\n\});/)[1])();
let code=source.slice(source.indexOf('  const ns = tracks.flatMap('),source.indexOf('  const profNear = railProfile('));
code+=source.slice(source.indexOf('  const ties = spec.ties;'),source.indexOf('  /* ---- tufts: the verges'))+';return zones;';
const zones=Function('tracks','paths','spec','rng','GROUND','tierLevel','ZONE_M',code)(tracks,paths,data,rng,{bed:{lift:.024}},()=>1,zoneM);
const planPath=path.join(__dirname,'../RAIL-LIFECYCLE-DESKTOP-03/source-plan.json'),plan=JSON.parse(fs.readFileSync(planPath,'utf8'));
const z=zones[plan.zone],centreE=z.eSum/z.eCount;
// Exact default diagnostic stand. Actual native desktop before/after receipts
// establish its eye height is below30m; mobile run must independently capture
// its actual camera and successful geometry/release/defaultDPR/pick assertions.
const camera={e:plan.targets.track.e-3,n:plan.targets.track.n-3,eyeYUpperBound:30};
const dn=camera.n>z.nHi?camera.n-z.nHi:camera.n<z.nLo?z.nLo-camera.n:0;
const de=Math.max(0,Math.abs(camera.e-centreE)-30),heightTerm=Math.max(0,camera.eyeYUpperBound-30),distance=Math.hypot(dn,de,heightTerm);
assert.equal(zones.length,57);assert.equal(plan.zone,28);assert.equal(distance,0);
assert.ok(distance<reach.light.near);assert.equal(reach.light.near,60);assert.equal(reach.light.ties,220);
const pins=[sourcePath,dataPath,planPath].map(f=>({path:f,bytes:fs.statSync(f).size,sha256:crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')}));
const result={scope:'SOURCE POLICY ARITHMETIC ONLY; NO PHONE/NATIVE RENDER/GPU EXECUTED',zone:plan.zone,zoneCount:zones.length,centreE,eCount:z.eCount,nHi:z.nHi,nLo:z.nLo,camera,dn,de,heightTerm,distance,REACH:reach,LightNearVisible:true,LightFarVisible:false,assumptions:['flat terrain stub changes only unused grade/y','actual mobile eye height <=30m must be captured by native run'],pins};
console.log(JSON.stringify(result,null,2));
