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
const scenePath=path.join(root,'data/scenes/1904.json'),scene=JSON.parse(fs.readFileSync(scenePath,'utf8'));
const distanceAt=(e,n,eyeY=30)=>Math.hypot(n>z.nHi?n-z.nHi:n<z.nLo?z.nLo-n:0,Math.max(0,Math.abs(e-centreE)-30),Math.max(0,eyeY-30));
const spawnDistance=distanceAt(scene.spawn.local_e,scene.spawn.local_n),rows=[];
for(const [profile,tier,offset] of [['desktop','full',350],['mobile','light',150]]){
 const r=reach[tier],farDistance=distanceAt(plan.targets.track.e,plan.nHi+offset),dropDistance=distanceAt(plan.targets.track.e,plan.nHi+1000);
 assert.ok(spawnDistance>r.near,'Final native spawn pose lies outside the selected near reach; arrival history is not assumed');assert.ok(farDistance>r.near&&farDistance<r.ties);assert.ok(dropDistance>r.ties+zoneM);
 rows.push({profile,nativeTier:tier,farOffset:offset,farDistance,nearThreshold:r.near,tieThreshold:r.ties,nearVisible:false,farVisible:true,nearMustBeAbsentAfterInitialNative1000mEviction:true,dropDistance,dropBeyondTiePlusZone:true,eyeHeightMustRemainAtMost30:true});
}
pins.push({path:scenePath,bytes:fs.statSync(scenePath).size,sha256:crypto.createHash('sha256').update(fs.readFileSync(scenePath)).digest('hex')});
console.log(JSON.stringify({scope:'SOURCE POLICY ARITHMETIC ONLY; NO NATIVE/GPU FAR EXECUTION',zone:plan.zone,zoneCount:zones.length,centreE,eCount:z.eCount,nHi:z.nHi,nLo:z.nLo,spawn:{e:scene.spawn.local_e,n:scene.spawn.local_n,distanceLowerBound:spawnDistance},rows,REACH:reach,pins,note:'Real initial1000m native eviction proves both selected near/far absent before first far pose; final spawn/arrival history is not assumed. Light150 would retain hidden near if one were deliberately created first. A second1000m drop proves actual far rebuild; near-context proof remains separate.'},null,2));
