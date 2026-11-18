
import { createNavigator } from '/js/navigator.js';
import jump from '/js/apps/jump.js';
let conditional = true;
const mount = (name) => (el) => {
  const h=document.createElement('h2'); h.textContent=name;
  const p=document.createElement('p'); p.textContent='Keyboard fixture: no town or world assets are loaded.';
  const b=document.createElement('button'); b.type='button'; b.id='fixture-'+name.toLowerCase(); b.textContent=name+' control';
  el.append(h,p,b);
};
const apps=[
  {id:'home', label:'Home', order:0, panel:'nav-home'},
  {id:'map', label:'Map', order:20, mount:mount('Map')},
  {id:'inspect', label:'Inspect', order:30, when:c=>c.conditional, mount:mount('Inspect')},
  {id:'settings', label:'Settings', order:100, pin:'bottom', mount:mount('Settings')},
  {...jump, load:undefined, mount:mount('Jump')},
  {id:'move', label:'Move', order:60, inRail:false, mount:mount('Move')},
];
const nav=createNavigator({root:document.getElementById('navigator'), apps,
  scene:{id:'1835',target_date:'1835-07-01',lighting:{local_time:'10:30'}},
  context:()=>({conditional}), storage:null,
});
// The same listener as main.js:4135; only the fixture's year chip supplies its DOM.
document.getElementById('year-badge').addEventListener('click',()=>void nav.select('jump'));
window.qa={nav, async conditional(value){conditional=value; await new Promise(r=>setTimeout(r,270)); nav.update();},
  unregister(id){return nav.unregister(id);},
  snapshot(){
    const tabs=[...document.querySelectorAll('.nav-tabs [role=tab]')].map(b=>({id:b.dataset.app,hidden:b.hidden,tabIndex:b.tabIndex,
      selected:b.getAttribute('aria-selected'),visible:b.getClientRects().length>0&&getComputedStyle(b).visibility!=='hidden'}));
    const el=document.activeElement, css=el?getComputedStyle(el):null;
    return {app:nav.app,level:nav.level,detent:nav.detent,tabs,focus:el?.id??null,
      focusVisible:!!el&&el.matches(':focus-visible')&&css.outlineStyle!=='none'&&parseFloat(css.outlineWidth)>0,
      canvases:document.querySelectorAll('canvas').length};
  }
};
window.fixtureReady=true;
