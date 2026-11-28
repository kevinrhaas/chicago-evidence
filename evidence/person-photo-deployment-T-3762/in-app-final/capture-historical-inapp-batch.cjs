const fs=require('node:fs');
module.exports=async function({p,only=null,includeStirling=false,report='other-people-captures'}){
 const capture=require('./capture-stirling-frame.cjs');
 const coverage=JSON.parse(fs.readFileSync('assets/humans/web/photo_faces/historical/coverage.json')).people;
 const refs=JSON.parse(fs.readFileSync('assets/humans/web/photo_faces/historical/review.json')).faces;
 const labels=Object.fromEntries(refs.map(f=>[f.id,f.label]));
 Object.assign(labels,{pa1904_grey_w_l:'William Grey',pa1904_grey_mrs_w_l:'Sarah Grey'});
 const order=['glessner_john_j','glessner_frances_m','pa1904_field_marshall','pa1904_pullman_mrs_george_m','pa1904_field_mrs_marshall_jr','glessner_williamson_martha_l','pa1904_grey_w_l','pa1904_grey_mrs_w_l'];
 const selected=coverage.filter(c=>c.active_cast&&(includeStirling||!c.person.includes('_stirling_'))&&(!only||only.includes(c.person))).sort((a,b)=>{const x=order.indexOf(a.person),y=order.indexOf(b.person);return(x<0?100:x)-(y<0?100:y);});
 const results=[];
 for(const row of selected){
  const id=row.person,key=id.replaceAll('_','-');
  try{
   console.log('PREPARING',labels[id]||id);
   const state=await p.evaluate(async id=>{
    const a=window.__chicago4d;a.setTravelMode('teleport');
    await a.findPerson(id);
    const actor=a.humans.get(id);
    if(!actor)return{available:false,why:'No actor available at this scene date/time',atHome:a.atHome(id)};
    a.camera.position.set(actor.root.position.x+5,actor.root.position.y+1.6,actor.root.position.z);
    a.camera.lookAt(actor.root.position.x,actor.root.position.y+1.3,actor.root.position.z);a.camera.updateMatrixWorld();
    a.world.follow(a.camera.position);a.terrain.updateGroundReach(a.camera.position);
    a.humans.update(0,a.camera,a.walker.state,0);await actor.setLod(1);
    for(let i=0;i<1600;i++){
     a.humans.update(.05,a.camera,a.walker.state,.05);a.days.update(.05);
     if(i>80&&!actor.indoors&&!a.days.doorway(id))break;
    }
    // A permanent household figure may not be in the directory's Find list.
    // Use that person's actual menu activity, through the native day engine.
    // Never move a figure or override its indoor/visibility state for a picture.
    if(actor.indoors){
     const offer=a.days.outdoorActivities(id).find(o=>o.span.activity==='work')??a.days.outdoorActivities(id)[0];
     if(offer){
      const requested=a.days.request(id,offer.id);
      if(requested.ok)for(let i=0;i<1600;i++){a.humans.update(.05,a.camera,a.walker.state,.05);a.days.update(.05);if(i>80&&!actor.indoors&&!a.days.doorway(id))break;}
     }
    }
    a.days.pause(a.days.people.find(q=>q.actor===actor)?.id??actor.id);actor.setState('standing');
    if(actor.indoors){const day=a.days.people.find(q=>q.id===id||q.actor.personId===id);return{available:false,why:'Actor has not come outside',nativeDay:day?{id:day.id,span:day.span,override:day.override,inside:day.inside,called:!!day.called,job:day.job?.kind,position:actor.position}:null};}
    const photo=actor.body?.scene.userData.chiPhotoFace?.id??null;
    return {available:true,personId:actor.personId,photoId:photo,instance:actor.id,position:actor.position};
   },id);
   if(!state.available){results.push({id,label:labels[id]||id,status:'not_captured',...state});console.log('NOT CAPTURED',id,JSON.stringify(state));continue;}
   if(row.status!=='existing_skin'&&state.photoId!==id)throw Error('Applied photo does not match person');
   const file=await capture({p,ids:{[key]:id},key,frame:'face'});
   results.push({id,label:labels[id]||id,status:'captured',identityBasis:row.status,file,...state});
   fs.writeFileSync('work/historical-inapp/'+report+'.json',JSON.stringify(results,null,2)+'\n');
  }catch(error){results.push({id,label:labels[id]||id,status:'error',error:error.message});console.log('CAPTURE ERROR',id,error.message);fs.writeFileSync('work/historical-inapp/'+report+'.json',JSON.stringify(results,null,2)+'\n');}
 }
 fs.writeFileSync('work/historical-inapp/'+report+'.json',JSON.stringify(results,null,2)+'\n');
 return results.map(r=>({id:r.id,status:r.status,label:r.label}));
};
