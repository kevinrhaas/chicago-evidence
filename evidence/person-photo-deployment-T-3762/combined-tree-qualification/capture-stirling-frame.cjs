const fs=require('node:fs');
module.exports=async function capture({p,ids,key,frame='face',side=0,settle=true}){
 const result=await p.evaluate(async({id,frame,side,settle})=>{
  const THREE=await import('three');
  const skin=await import('./js/human-skin.js');
  const a=window.__chicago4d,x=a.humans.get(id);
  if(!x?.body||x.personId!==id)throw Error('Wrong or missing town actor');
  x.root.updateMatrixWorld(true);
  const base=x.root.getWorldPosition(new THREE.Vector3());
  const eyes=['eye_l','eye_r'].map(n=>x.root.getObjectByName(n)).filter(Boolean);
  let centre=frame==='face'&&eyes.length?eyes.reduce((v,e)=>v.add(e.getWorldPosition(new THREE.Vector3())),new THREE.Vector3()).multiplyScalar(1/eyes.length).add(new THREE.Vector3(0,-.025,0)):base.clone().add(new THREE.Vector3(0,.87,0));
  const forward=new THREE.Vector3(0,0,1).applyQuaternion(x.root.getWorldQuaternion(new THREE.Quaternion())).normalize();
  const distance=frame==='face'?.85:3.5;
  a.camera.fov=frame==='face'?32:36;
  a.camera.near=.06;
  a.camera.position.copy(centre).addScaledVector(forward,distance);
  a.camera.position.addScaledVector(new THREE.Vector3(1,0,0).applyQuaternion(x.root.getWorldQuaternion(new THREE.Quaternion())),side);
  if(frame!=='face')a.camera.position.y+=.1;
  a.camera.lookAt(centre);a.camera.updateProjectionMatrix();a.camera.updateMatrixWorld();
  a.world.follow(a.camera.position);a.world.aim(a.camera);a.terrain.updateGroundReach(a.camera.position);
  a.humans.update(0,a.camera,a.walker.state,0);
  await x.setLod(1);
  x.path=null;x.setState('standing');
  // Let the actor's native gaze settle at the portrait camera after the door walk.
  // A frozen pose aimed at the old, higher stoop camera looks upward in a close-up.
  for(let pass=0;pass<(settle?2:0);pass++){
   x.life?.attend?.(a.camera.position.clone(),10);
   for(let i=0;i<60;i++)x.update(.05,a.camera.position,.05);
   x.root.updateMatrixWorld(true);
   if(frame==='face'&&eyes.length){
    centre=eyes.reduce((v,e)=>v.add(e.getWorldPosition(new THREE.Vector3())),new THREE.Vector3()).multiplyScalar(1/eyes.length).add(new THREE.Vector3(0,-.025,0));
    a.camera.position.copy(centre).addScaledVector(forward,distance);
    a.camera.position.addScaledVector(new THREE.Vector3(1,0,0).applyQuaternion(x.root.getWorldQuaternion(new THREE.Quaternion())),side);
    a.camera.lookAt(centre);a.camera.updateMatrixWorld();
   }
  }
  // Choose a native frame between blinks for an eye-placement review. Advance
  // the same life/face animation; never force an eyelid morph or replace eyes.
  const blinkNow=()=>x.life?.bound?x.life.blink:(x.blinkClock%4<.15?1:0);
  for(let i=0;i<24&&blinkNow()>.001;i++)x.update(.025,a.camera.position,.025);
  const neighbors=a.humans.actors.filter(other=>other!==x).map(other=>[other.root,other.root.visible]);
  for(const[root]of neighbors)root.visible=false;
  try{
  window.__appRender(a.scene3d,a.camera);
  await skin.photoFacePagesReady();
  window.__appRender(a.scene3d,a.camera);
  return {png:a.renderer.domElement.toDataURL('image/png').split(',')[1],meta:{personId:id,photoId:x.body.scene.userData.chiPhotoFace?.id??null,instanceId:x.id,frame,year:a.year,detail:a.detail,lod:x.lod,position:x.position,camera:a.camera.position.toArray(),heading:x.heading,nativeGazeSettledAtCamera:settle,sideOffset:side,naturalBlink:blinkNow(),restingLid:x.variation?.photoFace?.eyes?.lid_rest??null,otherFiguresHiddenForPortrait:true,photoPages:skin.photoFaceTextureStats(),renderer:'Actual published app renderer and scene; Chromium SwiftShader; camera framed for review'}};
  }finally{for(const[root,visible]of neighbors)root.visible=visible;}
 },{id:ids[key],frame,side,settle});
 fs.mkdirSync('work/historical-inapp',{recursive:true});
 const file=`work/historical-inapp/${key}-in-app-${frame}.png`;
 fs.writeFileSync(file,Buffer.from(result.png,'base64'));
 fs.writeFileSync(file+'.json',JSON.stringify(result.meta,null,2)+'\n');
 console.log('CAPTURED',file,JSON.stringify(result.meta));return file;
};
