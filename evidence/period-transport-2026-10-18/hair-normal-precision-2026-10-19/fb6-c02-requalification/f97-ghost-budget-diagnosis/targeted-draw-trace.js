// Proposed page.evaluate body ONLY; not executed. Run after root full preflight,
// at the existing T2648 row ghost state/camera on a qualified published mirror.
() => {
  const a=window.__chicago4d, renderer=a.renderer;
  const original=renderer.renderBufferDirect, rows=[];
  renderer.renderBufferDirect=function(camera,scene,geometry,material,object,group){
    const before=this.info.render.calls;
    try{return original.call(this,camera,scene,geometry,material,object,group);}
    finally{
      const chain=[];for(let o=object;o;o=o.parent)if(o.name)chain.push(o.name);
      rows.push({object:object?.name,type:object?.type,ancestors:chain,
        material:material?.name,materialType:material?.type,
        cameraIsMain:camera===a.camera,cameraLayerMask:camera.layers.mask,
        callDelta:this.info.render.calls-before,group:group??null});
    }
  };
  try {
    a.step();
    return {stats:a.stats(),ghost:a.confidence.ghostStats,
      modes:a.confidence.modes,camera:{position:a.camera.position.toArray(),quaternion:a.camera.quaternion.toArray()},
      shadow:{autoUpdate:renderer.shadowMap.autoUpdate,needsUpdate:renderer.shadowMap.needsUpdate},rows};
  } finally {renderer.renderBufferDirect=original;}
};
