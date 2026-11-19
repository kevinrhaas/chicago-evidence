
import { createNavigator } from '/js/navigator.js';
import { createIntent, createBackendSwitch } from '/js/controls/intent.js';
import { createPointerLockBackend } from '/js/controls/pointerlock.js';
import { createDesktopKeyCapture } from '/js/controls/keyboard.js';
const canvas=document.getElementById('world'), popup=document.getElementById('popup');
const intent=createIntent(), backends=createBackendSwitch(intent);
let locks=0, activates=0, clicks=0, holding=false, byHand=false, preventCode=null;
// Observe the actual PointerLockControls request boundary without taking browser focus.
canvas.requestPointerLock=()=>{locks++;};
const apps=[{id:'home',label:'Home',order:0,panel:'nav-home'},...['map','inspect','settings'].map((id,i)=>({id,label:id,order:(i+1)*10,mount(el){const h=document.createElement('h2');h.textContent=id;const b=document.createElement('button');b.id=id+'-action';b.textContent='Activate '+id;b.onclick=()=>clicks++;el.append(h,b);}}))];
const nav=createNavigator({root:document.getElementById('navigator'),apps,storage:null,scene:{id:'1835',target_date:'1835-07-01',lighting:{local_time:'10:30'}}});
const backend=createPointerLockBackend({intent,domElement:canvas,holding:()=>holding,inspecting:()=>byHand&&nav.app==='inspect'});
backends.activate(backend);
window.addEventListener('keydown',e=>{if(e.code===preventCode)e.preventDefault();},{capture:true});
window.addEventListener('keydown',createDesktopKeyCapture({holding:()=>holding,inspecting:()=>byHand&&nav.app==='inspect',activate:()=>{activates++;backends.activate(backend);},lock:()=>backend.lock()}),{capture:true});
document.getElementById('outside-action').onclick=()=>clicks++;
document.getElementById('dialog-close').onclick=()=>document.getElementById('native-dialog').close();
window.qa={nav,intent,backend,canvas,
  reset(){window.dispatchEvent(new Event('blur'));intent.clear();intent.flying=false;locks=activates=clicks=0;holding=byHand=false;preventCode=null;popup.hidden=true;},
  popup(value){holding=value;popup.hidden=!value;},
  byHand(value){byHand=value;}, prevent(code){preventCode=code;}, consume(){return intent.takeInteract();},
  snap(){backend.update();return {locks,activates,clicks,forward:intent.forward,strafe:intent.strafe,rise:intent.rise,sprint:intent.sprint,interact:intent.interact,source:intent.interactSource,focus:document.activeElement?.id,app:nav.app,level:nav.level,dialogOpen:document.getElementById('native-dialog').open};}
};
window.fixtureReady=true;
