import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import vm from 'node:vm';
const source=await fs.readFile(new URL('./desktop-post-a-image-2c.mjs',import.meta.url),'utf8');
const start=source.indexOf('async function clearVisitorUI(){'),end=source.indexOf('\nasync function progress(',start);
assert(start>=0&&end>start);
const clicks=[],keys=[],phases=[],state={errors:[]};let navOpen=true;
const document={pointerLockElement:null,querySelector:()=>({get offsetParent(){return navOpen?{}:null;}})};
const sandbox={state,document,progress:async name=>phases.push(name),stage:async(name,run)=>run(),
 page:{locator:id=>({isVisible:async()=>id==='#nav-close'&&navOpen,
  boundingBox:async()=>id==='#view'?{x:0,y:0,width:1280,height:800}:{x:10,y:20,width:20,height:30},
  click:()=>{throw Error('Locator stability click must not be used');}}),
  mouse:{click:async(x,y)=>{clicks.push([x,y]);if(x===20)navOpen=false;if(x===640)document.pointerLockElement={};}},
  keyboard:{press:async key=>{keys.push(key);document.pointerLockElement=null;}},evaluate:async fn=>fn()}};
vm.createContext(sandbox);
const api=vm.runInContext(source.slice(start,end)+';({clearVisitorUI,observeIndependent});',sandbox);
const ui=await api.clearVisitorUI();
assert.deepEqual(clicks,[[20,35],[640,400]],'actual bounding boxes determine trusted mouse targets');
assert.deepEqual(keys,['Escape']);assert.equal(ui.afterClick.pointerLocked,true);assert.equal(ui.afterEscape.pointerLocked,false);assert.equal(ui.afterEscape.navOpen,false);
const failure=await api.observeIndependent('controlled-ui',async()=>{throw Error('controlled gesture failure');});
assert.equal(failure,null);assert.equal(state.errors.length,1);assert.equal(state.independentFailures.length,1);
let captured=false;await api.observeIndependent('controlled-independent-image',async()=>{captured=true;});
assert(captured,'UI failure must not abandon independent image capture');
assert.match(phases[0],/NONPASS-SAVED/);
console.log('PASS: exact bbox/real mouse API flow, Escape, strict UI NONPASS serialization and independent image continuation');
