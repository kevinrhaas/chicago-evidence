const fs=require('node:fs');
module.exports=async function({p}){
 const capture=require('./capture-stirling-frame.cjs');
 const entries=[
  {id:'pa1904_grey_walter_c',name:'Walter C. Grey',kind:'generic adult',age:28},
  {id:'pa1904_grey_daughter',name:'Florence Grey',kind:'generic adult',age:24},
  {id:'pa1904_grey_elizabeth_w',name:'Elizabeth W. Grey',kind:'generic child',age:8},
  {id:'pa1904_young_lawrence_a_c1900_henry_w_young',name:'Henry W. Young',kind:'generic child',age:10}
 ];const results=[];
 for(const row of entries){
  console.log('GENERIC PREPARING',row.name);
  try{
   const state=await p.evaluate(async id=>{
    const a=window.__chicago4d;a.setTravelMode('teleport');await a.findPerson(id);
    const x=a.humans.get(id);if(!x)return{available:false,why:'Not available at the current scene date/time'};
    a.camera.position.set(x.root.position.x+5,x.root.position.y+1.6,x.root.position.z);a.camera.lookAt(x.root.position.x,x.root.position.y+1.2,x.root.position.z);a.camera.updateMatrixWorld();
    a.world.follow(a.camera.position);a.terrain.updateGroundReach(a.camera.position);a.humans.update(0,a.camera,a.walker.state,0);await x.setLod(1);
    for(let i=0;i<1600;i++){a.humans.update(.05,a.camera,a.walker.state,.05);a.days.update(.05);if(i>80&&!x.indoors&&!a.days.doorway(id))break;}
    a.days.pause(a.days.people.find(q=>q.actor===x)?.id??x.id);x.setState('standing');
    return{available:!x.indoors,personId:x.personId,photoId:x.body?.scene.userData.chiPhotoFace?.id??null,position:x.position};
   },row.id);
   if(!state.available){results.push({...row,...state,status:'not_captured'});continue;}
   const key='generic-'+row.id.replaceAll('_','-');
   const file=await capture({p,ids:{[key]:row.id},key,frame:'face'});
   let whole=null;if(row.kind==='generic child')whole=await capture({p,ids:{[key]:row.id},key,frame:'whole',side:1});
   results.push({...row,...state,file,whole,status:'captured',likeness:'Reconstructed library face; no individual photographic likeness claimed'});
  }catch(error){results.push({...row,status:'error',error:error.message});console.log('GENERIC CAPTURE ERROR',row.id,error.message);}
  fs.writeFileSync('work/historical-inapp/generic-captures.json',JSON.stringify(results,null,2)+'\n');
 }
 fs.writeFileSync('work/historical-inapp/generic-captures.json',JSON.stringify(results,null,2)+'\n');
 // These six actors were already posed through native Find/standing controls.
 // Keep their native front pose and frame it obliquely to inspect the actual
 // head, hairline and face/body join, rather than turning the head at the camera.
 delete require.cache[require.resolve('./capture-stirling-frame.cjs')];
 const angledCapture=require('./capture-stirling-frame.cjs'),angles=[];
 const checkViews=[...entries.map(r=>({id:r.id,name:r.name})),
  {id:'pa1904_stirling_william_r_c1900_dorothy_sterling',name:'Dorothy Sterling'},
  {id:'pa1904_stirling_william_r_c1900_alice_m_sterling',name:'Alice May Stirling'}];
 for(const row of checkViews){
  const key='oblique-'+row.id.replaceAll('_','-');
  const file=await angledCapture({p,ids:{[key]:row.id},key,frame:'face',side:.5,settle:false});
  angles.push({...row,file,status:'captured'});
 }
 fs.writeFileSync('work/historical-inapp/oblique-captures.json',JSON.stringify(angles,null,2)+'\n');
 return results;
};
