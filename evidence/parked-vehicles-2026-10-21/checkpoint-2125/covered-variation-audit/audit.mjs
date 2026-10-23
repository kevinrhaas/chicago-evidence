// Read-only source/data inventory: executes only extracted pure seed functions.
// No renderer imports, mesh generation, browser, network, app tests or tracked writes.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
const root='/workspace/chicago',app=path.join(root,'chicago/4d');
const output='/workspace/shared/covered-wagon-variation-audit-2026-10-21';
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const sourceFiles=['renderers/web/js/yard.js','renderers/web/js/main.js','renderers/web/js/parked-transport.js','data/transport/parked/placements.json','data/yard/index.json','tools/generate_yard_goods.py','tools/generate_trade_yards.py'];
const bytes=new Map(sourceFiles.map(p=>[p,fs.readFileSync(path.join(app,p))]));
const src=bytes.get('renderers/web/js/yard.js').toString();
const readConst=name=>vm.runInNewContext('('+src.match(new RegExp('const '+name+' = ([\\s\\S]*?);'))[1]+')');
const palette={woods:readConst('WOODS'),paint:readConst('WAGON_PAINT'),schemes:readConst('WAGON_SCHEMES'),canvasHex:readConst('CANVAS_COLOUR'),ironHex:readConst('IRON_COLOUR')};
const pure=src.slice(src.indexOf('function hashOf('),src.indexOf('/** Where a piece of timber starts'));
const {hashOf,streamOf}=vm.runInNewContext(pure+';({hashOf,streamOf})');
const hex=n=>'#'+n.toString(16).padStart(6,'0');
const linear=(n,k)=>[16,8,0].map(shift=>{let c=((n>>shift)&255)/255;return (c<=0.04045?c/12.92:((c+0.055)/1.055)**2.4)*k;});
const coatOf=w=>{
 const seedParts=['wagon',w.id??'',...(w.at_local_enu_m??[])],seedText=seedParts.join('|'),seed=hashOf(...seedParts),rng=streamOf(seed);
 const draws=[rng(),rng(),rng(),rng()];const total=palette.schemes.reduce((a,s)=>a+s[0],0);let pick=palette.schemes[0],v=draws[0]*total;
 for(const s of palette.schemes){v-=s[0];if(v<0){pick=s;break;}}
 const age=.88+draws[1]*.18,gearMultiplier=.92+draws[2]*.1,gearScale=age*gearMultiplier,canvasScale=.84+draws[3]*.18;
 const color=name=>palette.woods[name]??palette.paint[name];
 return {seedParts,seedText,seedUint32:seed,firstFourDraws:draws,scheme:{weight:pick[0],body:pick[1],gear:pick[2]},ageScalar:age,gearMultiplier,gearScalar:gearScale,canvasScalar:canvasScale,baseSrgb:{body:hex(color(pick[1])),gear:hex(color(pick[2])),canvas:hex(palette.canvasHex)},nominalUncachedLinear:{body:linear(color(pick[1]),age),gear:linear(color(pick[2]),gearScale),canvas:linear(palette.canvasHex,canvasScale)},boardVariation:{floorScalar:.94+rng()*.08,sideAndEndBoardScalars:Array.from({length:8},()=>.86+rng()*.2),stakeScalars:Array.from({length:6},()=>.9+rng()*.12)}};
};
const index=JSON.parse(bytes.get('data/yard/index.json')),rows=[],groups=[];
for(const entry of index.yard){
 const file='data/yard/'+entry.file,dataBytes=fs.readFileSync(path.join(app,file));bytes.set(file,dataBytes);const data=JSON.parse(dataBytes),wagons=data.wagons??[];
 const counts={};for(const w of wagons){let kind=w.kind??'farm_box';counts[kind]=(counts[kind]??0)+1;}
 if(wagons.length)groups.push({record:entry.id,file,declaredRows:wagons.length,byKind:counts,coveredRows:wagons.filter(w=>w.tilt).length});
 for(const w of wagons){
  if(!w.tilt)continue;
  const form=data.form??{},value=(key,fallback)=>form[key]?.value??fallback;
  const [L,W,H]=value('wagon_body_m',[3.05,1.07,.55]),[rise,over]=value('wagon_tilt_m',[1.1,.12]);
  rows.push({id:w.id,sourceFile:file,kind:w.kind??'farm_box',confidence:w.confidence??data.existence?.confidence??'reconstructed',at_local_enu_m:w.at_local_enu_m,bearing_deg:w.bearing_deg,belongs_to:w.belongs_to??null,in_enclosure:w.in_enclosure??null,in_yard_of:w.in_yard_of??null,under_shed:w.under_shed??null,stands_on:w.stands_on??null,yoke:!!w.yoke,tilt:!!w.tilt,slew_deg:w.slew_deg??null,slew_envelope_deg:w.slew_envelope_deg??null,clearance_m:w.clearance_m??null,clear_of_track_m:w.clear_of_track_m??null,loadFieldsPresent:['load','cargo','contents','items','mark'].filter(k=>k in w),geometry:{body_m:[L,W,H],bedHeight_m:.95,rearWheelDiameter_m:1.37,frontWheelDiameter_m:1.07,tongueLength_m:2.75,axleAlongCenters_m:[-L/2+.35,L/2-.35],wheelbase_m:L-.70,wheelCenterTrack_m:W+.14,outerTireWidth_m:W+.21,canvasRise_m:rise,canvasOverhangEachEnd_m:over,canvasLength_m:L+2*over,canvasWidth_m:W,canvasCrownAboveBase_m:.95+H+rise,canvasSegments:8,canvasEnds:'open',separateBowGeometry:false,yoke_m:w.yoke?value('ox_yoke_m',[1.42,.12,.34,.05]):null,yokeSideOffset_m:w.yoke?1.35:null},coat:coatOf(w)});
 }
}
const candidates=['green_tree_tavern_shed_wagon','town_wagon_western_hotel_wagon_yard_1','town_wagon_wolf_point_tavern_yard_1','town_wagon_wolf_point_tavern_yard_3','inf_teamster_stable_west_yard_wagon_2'];
const schemeCounts={};for(const row of rows){const key=row.coat.scheme.body+'/'+row.coat.scheme.gear;schemeCounts[key]=(schemeCounts[key]??0)+1;}
const ticketFiles=['T-2750-2999/T-2792-carriages-and-wagons-evidence-register-and-first.md','T-2750-2999/T-2793-build-one-articulated-period-wagon-master-from-t.md','T-2750-2999/T-2979-park-refined-wagons-and-a-period-carriage-in-the.md','T-2750-2999/T-2980-upgrade-selected-covered-wagons-while-preserving.md','QUEUE.md','HANDOVER.md'];
const ticketHashes=Object.fromEntries(ticketFiles.map(file=>[file,hash(fs.readFileSync('/workspace/chicago-tickets/'+file))]));
const result={scope:'Finite read-only source audit for T-2980 preparation; no implementation, runtime test or photographic acceptance',observedAt:new Date().toISOString(),appHead:'2aebef95f6a5b6fa1bd8353db936c7674a73c32f',sourceHashes:Object.fromEntries([...bytes].map(([file,b])=>[file,hash(b)])),ticketHashes,declaredInventory:{indexScene:index.scene,groups,totalRows:groups.reduce((a,g)=>a+g.declaredRows,0),coveredRows:rows.length,coveredWithYoke:rows.filter(w=>w.yoke).length,coveredWithoutYoke:rows.filter(w=>!w.yoke).map(w=>w.id),coveredSchemeCounts:schemeCounts,actualRuntimeDrawnCount:null,countLimits:'86 is the sum of source rows in the three indexed records with wagons:80 town_trade_goods+1 town_water_cart+5 town_trade_yards.80 in the earlier ticket/PR is the town_trade_goods group, not the complete index. Actual emitted census filters hostMissing, missing/invalid at_local_enu_m and groundAt refusal; near/far/Light visibility and replacement fallback can hide already-built meshes without removing their record/census. No runtime census was measured in this audit.'},variation:{seed:'Exact extracted hashOf/streamOf source; FNV-1a32 over JS parts.join("|") with ["wagon", originalId, exactE, exactN]; no scene, bearing, kind or row index enters wagonCoat seed.',stream:'Mulberry32-style source stream; seed0 becomes1; increments0x6d2b79f5, uses Math.imul/unsigned shifts.',schemeTotalWeight:palette.schemes.reduce((a,s)=>a+s[0],0),palette,ageRange:[.88,1.06],gearMultiplierRange:[.92,1.02],canvasScalarRange:[.84,1.02],additional:'Next draws shade the floor,8 side/end boards,and6 stakes; fixed geometry, not random body/arch deformation. Grain UV offsets use another hash of world primitive center rounded to centimetres, including terrain-dependent Y, over a4.48m tile; canvas disables grain.',linearColorLimit:'Nominal uncached linear triples are computed analytically from sRGB and exact scalar. Actual toneOf caches by hex+k.toFixed(3), so a previous nearby scalar may be reused; these triples are not claimed actual framebuffer colors or a full emitV replay.',geometry:'All18 covered rows share body/wheel/arch dimensions.17 add laid-by yoke geometry; GreenTree shed wagon has none. Orientation,exactplace,slew and host/shed context vary. No covered row supplies load/cargo/content/item/mark data.'},candidateIds:candidates,candidates:rows.filter(w=>candidates.includes(w.id)),allCovered:rows};
result.sourceInputsUnchangedAtEnd=[...bytes].every(([file,b])=>hash(fs.readFileSync(path.join(app,file)))===hash(b));
fs.writeFileSync(path.join(output,'inventory.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({declaredTotal:result.declaredInventory.totalRows,covered:rows.length,schemeCounts,candidates:result.candidates.map(w=>({id:w.id,body:w.coat.scheme.body,gear:w.coat.scheme.gear,age:w.coat.ageScalar,canvas:w.coat.canvasScalar,yoke:w.yoke})),sourceInputsUnchangedAtEnd:result.sourceInputsUnchangedAtEnd}));
