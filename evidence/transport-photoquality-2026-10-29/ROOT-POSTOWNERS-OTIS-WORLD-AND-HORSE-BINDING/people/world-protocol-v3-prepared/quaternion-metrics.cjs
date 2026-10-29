// Numerical observation only; never writes to a native actor or quaternion.
function quaternionMotion(a,b){
 if(a.length!==4||b.length!==4||[...a,...b].some(x=>!Number.isFinite(x)))throw Error('Finite quaternion components required');
 const normA=Math.hypot(...a),normB=Math.hypot(...b);if(!(normA>0&&normB>0))throw Error('Nonzero quaternion norms required');
 const dot=a.reduce((s,v,i)=>s+v*b[i],0),maximumComponentDelta=Math.max(...a.map((v,i)=>Math.abs(v-b[i]))),normalizedDot=Math.min(1,Math.max(0,Math.abs(dot)/(normA*normB)));
 const normalizedAngleRadians=maximumComponentDelta===0?0:2*Math.acos(normalizedDot);
 return {normA,normB,rawDot:dot,normalizedDot,normalizedAngleRadians,maximumComponentDelta,changed:normalizedAngleRadians>1e-7&&maximumComponentDelta>1e-10};
}
module.exports={quaternionMotion};
