window.comparisonInputHash=async()=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',buffer))).map(x=>x.toString(16).padStart(2,'0')).join('');
window.disposeComparison=()=>{
 const gs=new Set(),ms=new Set();scene.traverse(n=>{if(n.geometry)gs.add(n.geometry);for(const m of Array.isArray(n.material)?n.material:[n.material])if(m)ms.add(m);});
 let g=0,m=0;gs.forEach(x=>x.addEventListener('dispose',()=>g++));ms.forEach(x=>x.addEventListener('dispose',()=>m++));
 window.disposeBrougham();const once={geometryEvents:g,materialEvents:m};window.disposeBrougham();
 const row={expectedGeometries:gs.size,expectedMaterials:ms.size,geometryEvents:g,materialEvents:m,idempotent:once.geometryEvents===g&&once.materialEvents===m,sceneChildren:scene.children.length,remainingGeometries:renderer.info.memory.geometries,remainingTextures:renderer.info.memory.textures,disposed,resourceCleanup:window.broughamCleanupReceipt};
 if(g!==gs.size||m!==ms.size||!row.idempotent||row.sceneChildren!==0||row.remainingGeometries!==0||row.remainingTextures!==0||!disposed)throw Error('Actual disposal guard failed '+JSON.stringify(row));return row;
};

window.broughamReady=true;
