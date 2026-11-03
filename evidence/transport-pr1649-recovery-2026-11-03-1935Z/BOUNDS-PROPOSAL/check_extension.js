// The exact former Float32 cache is the oracle, including its outward rounding.
// Kept inline so CI does not need Git history or an external fixture.
if (!SELF_TEST) {
  const legacyCompact = Function('THREE', 'floorF32', 'ceilF32', %%LEGACY%% + '; return compactBatchBounds;')(THREE, floorF32, ceilF32);
  const same = (a, b, label) => assert.ok(Object.is(a, b), `${label}: ${Object.is(a,-0)?'-0':a} != ${Object.is(b,-0)?'-0':b}`);
  const equalBounds = (a, b, id) => {
    const x = a.getBoundingBoxAt(id, new THREE.Box3()), y = b.getBoundingBoxAt(id, new THREE.Box3());
    if (x === null || y === null) { assert.equal(x,y); return; }
    for (const k of ['x','y','z']) { same(x.min[k],y.min[k],`box ${id} min.${k}`);same(x.max[k],y.max[k],`box ${id} max.${k}`); }
    const u=a.getBoundingSphereAt(id,new THREE.Sphere()),v=b.getBoundingSphereAt(id,new THREE.Sphere());
    for (const k of ['x','y','z']) same(u.center[k],v.center[k],`sphere ${id}.${k}`);
    same(u.radius,v.radius,`sphere ${id} radius`);
  };
  function gridPiece(i) {
    const g = new THREE.BoxGeometry(1,1,1), a=g.attributes.position.array;
    const lo=[-30000+i%19,-22000+i%11,-15000+i%7],hi=[18000+i%13,27000+i%17,22000+i%5];
    const p=new Int16Array(a.length);
    for(let j=0;j<a.length;j++)p[j]=a[j]<0?lo[j%3]:hi[j%3];
    g.setAttribute('position',new THREE.Int16BufferAttribute(p,3,true));g.deleteAttribute('uv');return g;
  }
  function gridBatch(n, kind='quantized') {
    const gs=Array.from({length:n},(_,i)=>gridPiece(i));
    const out=new THREE.BatchedMesh(n+8,n*24+64,n*36+128,new THREE.MeshBasicMaterial({side:THREE.DoubleSide}));
    for(let i=0;i<n;i++)out.setMatrixAt(out.addInstance(out.addGeometry(gs[i])),new THREE.Matrix4().makeTranslation((i%32)-16,Math.floor(i/32)*3,0));
    for(let i=0;i<n;i++) {
      out.getBoundingBoxAt(i,new THREE.Box3());out.getBoundingSphereAt(i,new THREE.Sphere());
      const gi=out._geometryInfo[i];
      if(kind==='exceptions'&&i%17===0)gi.boundingSphere.center.set(-0,.123456789,-.34567891);
      if(kind==='dictionary16')gi.boundingSphere.radius=1000+(i%300)/1000;
      if(kind==='unique-radii')gi.boundingSphere.radius=1000+i/128;
    }
    if(kind==='nonnormalized')out.geometry.attributes.position.normalized=false;
    if(kind==='off-grid')out._geometryInfo[0].boundingBox.min.x=-.123456789;
    if(kind==='exceptions') {
      const gi=out._geometryInfo[1];gi.boundingBox.min.x=-0;gi.boundingSphere.center.x=-0;
      out._geometryInfo[2].boundingSphere.center.set(0,0,0);out._geometryInfo[2].boundingSphere.radius=-Number.MIN_VALUE;
      out._geometryInfo[3].boundingSphere.radius=0;
    }
    for(const g of gs)g.dispose();return out;
  }
  check('7. q16 cache answers the exact former Float32 oracle and retains native lifecycle/cull/raycast',()=>{
    const n=512,a=gridBatch(n,'exceptions'),b=gridBatch(n,'exceptions');legacyCompact(a);compactBatchBounds(b);
    assert.equal(b.userData.compactBounds.codec,'q16-bit-exact');assert.ok(b.userData.compactBounds.centerExceptions>0);
    assert.ok(b.userData.compactBounds.radiusDictionaryEntries>0);assert.equal(b.userData.compactBounds.radiusIndexBytes,1);
    assert.ok(b.userData.compactBounds.bytes<a.userData.compactBounds.bytes);
    for(let i=0;i<n;i++)equalBounds(a,b,i);
    // Cached getters historically require only center.set(), as the old oracle does.
    const makeTarget=()=>({center:{set(x,y,z){this.x=x;this.y=y;this.z=z;return this;}},radius:0});
    const oldTarget=makeTarget(),newTarget=makeTarget();a.getBoundingSphereAt(0,oldTarget);b.getBoundingSphereAt(0,newTarget);
    for(const k of ['x','y','z'])same(oldTarget.center[k],newTarget.center[k],`set-only center ${k}`);same(oldTarget.radius,newTarget.radius,'set-only radius');
    assert.ok(Object.is(b.getBoundingBoxAt(1,new THREE.Box3()).min.x,-0),'negative-zero endpoint survives');
    assert.ok(Object.is(b.getBoundingSphereAt(2,new THREE.Sphere()).radius,-0),'negative-zero radius word survives');
    const replacement=gridPiece(901);a.setGeometryAt(4,replacement);b.setGeometryAt(4,replacement);equalBounds(a,b,4);
    for(const z of [a,b]) {
      z._geometryInfo[5].boundingBox=new THREE.Box3(new THREE.Vector3(-.13,-.27,-.39),new THREE.Vector3(.21,.33,.47));
      z._geometryInfo[6].boundingSphere=new THREE.Sphere(new THREE.Vector3(-0,3.14159,-2.7),4.123456789);
      z.deleteInstance(7);z.deleteGeometry(7);
    }
    equalBounds(a,b,5);equalBounds(a,b,6);equalBounds(a,b,7);
    const reusedA=a.addGeometry(replacement),reusedB=b.addGeometry(replacement);assert.equal(reusedA,reusedB);equalBounds(a,b,reusedA);
    const laterA=a.addGeometry(replacement),laterB=b.addGeometry(replacement);assert.equal(laterA,laterB);assert.ok(laterA>=n);equalBounds(a,b,laterA);
    assert.equal(compactBatchBounds(b),0);equalBounds(a,b,b._geometryCount+3);
    const cam=new THREE.PerspectiveCamera(60,1,.1,300);cam.position.set(0,10,30);cam.lookAt(0,10,0);cam.updateMatrixWorld();cam.updateProjectionMatrix();
    a.updateMatrixWorld(true);b.updateMatrixWorld(true);
    const ray=new THREE.Raycaster();ray.setFromCamera(new THREE.Vector2(),cam);
    const hits=z=>ray.intersectObject(z,true).map(h=>[h.distance,h.faceIndex,h.batchId]);assert.deepEqual(hits(a),hits(b));
    // Both caches answer exactly after upload. Draw-range culling uses the same
    // getters and neither representation regenerates source geometry.
    for(const z of [a,b]) {z.geometry.attributes.position.array=null;z.geometry.index.array=new Uint16Array(0);}
    for(let i=0;i<n;i++)equalBounds(a,b,i);
    for(const z of [a,b]) {const scene=new THREE.Scene();scene.add(z);z.perObjectFrustumCulled=true;z.onBeforeRender({info:{render:{}}},scene,cam,z.geometry,z.material,null);}
    assert.equal(a._multiDrawCount,b._multiDrawCount);
    assert.deepEqual(a._multiDrawCounts,b._multiDrawCounts);assert.deepEqual(a._multiDrawStarts,b._multiDrawStarts);
    console.log(JSON.stringify({fixtureRows:n,oldBytes:a.userData.compactBounds.bytes,newBytes:b.userData.compactBounds.bytes,codec:b.userData.compactBounds,exactOldFloat32Values:true}));
    a.dispose();b.dispose();replacement.dispose();
  });
  check('8. q16 center exception IDs cover large row IDs; radius dictionaries preserve exact words',()=>{
    for(const [n,kind]of[[2048,'dictionary16'],[128,'unique-radii']]) {
      const a=gridBatch(n,kind),b=gridBatch(n,kind);legacyCompact(a);compactBatchBounds(b);
      assert.equal(b.userData.compactBounds.codec,'q16-bit-exact');
      if(kind==='dictionary16'){assert.ok(b.userData.compactBounds.radiusDictionaryEntries>256);assert.equal(b.userData.compactBounds.radiusIndexBytes,2);}
      else assert.equal(b.userData.compactBounds.radiusDictionaryEntries,0);
      for(let id=0;id<n;id++)equalBounds(a,b,id);a.dispose();b.dispose();
    }
    // Sparse real-BatchedMesh metadata isolates the 32-bit ID boundary without
    // allocating tens of thousands of source meshes or instances.
    const wide=()=>{
      const b=gridBatch(1);const gi=b._geometryInfo[0];b._geometryInfo.length=65538;b._geometryCount=65538;
      b._geometryInfo[65537]={...gi,boundingBox:gi.boundingBox.clone(),boundingSphere:new THREE.Sphere(new THREE.Vector3(.123456789,-0,.987654321),1)};
      return b;
    };
    const a=wide(),b=wide();legacyCompact(a);compactBatchBounds(b);assert.equal(b.userData.compactBounds.codec,'q16-bit-exact');
    equalBounds(a,b,0);equalBounds(a,b,65537);a.dispose();b.dispose();
  });
  check('9. nonnormalized, off-grid and unprofitable batches retain the original Float32 representation',()=>{
    for(const [n,kind]of[[64,'nonnormalized'],[64,'off-grid'],[1,'quantized']]){
      const a=gridBatch(n,kind),b=gridBatch(n,kind);legacyCompact(a);compactBatchBounds(b);
      assert.equal(b.userData.compactBounds.codec,undefined);assert.equal(b.userData.compactBounds.bytes,a.userData.compactBounds.bytes);
      for(let id=0;id<n;id++)equalBounds(a,b,id);a.dispose();b.dispose();
    }
  });
  // Independent mutations add to, rather than replace, the nearest-rounding twin.
  const brokenZero=source.replace('floorF32(qValue(packed.boxes[b])),','(floorF32(qValue(packed.boxes[b])) + 0),');
  assert.notEqual(brokenZero,source);
  const load=async text=>(await import('data:text/javascript;base64,'+Buffer.from(text.replace("from 'three'",`from '${threeURL}'`)).toString('base64'))).compactBatchBounds;
  const zeroCodec=await load(brokenZero),bad=gridBatch(64,'exceptions');zeroCodec(bad);
  assert.equal(bad.userData.compactBounds.codec,'q16-bit-exact');
  const goodZero=gridBatch(64,'exceptions');legacyCompact(goodZero);assert.throws(()=>equalBounds(goodZero,bad,1),assert.AssertionError);goodZero.dispose();bad.dispose();
  const brokenAdmission=source.replace('if (!Object.is(restored, value)) return null;','if (false) return null;');assert.notEqual(brokenAdmission,source);
  const badAdmission=gridBatch(64,'off-grid'),goodAdmission=gridBatch(64,'off-grid');legacyCompact(goodAdmission);(await load(brokenAdmission))(badAdmission);
  assert.equal(badAdmission.userData.compactBounds.codec,'q16-bit-exact');assert.throws(()=>equalBounds(goodAdmission,badAdmission,0),assert.AssertionError);badAdmission.dispose();goodAdmission.dispose();
  console.log('ok   10. original Float32 oracle rejects broken signed-zero and non-grid admission');
  const { quantizePositions } = await import(pathToFileURL(path.join(web,'js/compact-attributes.js')));
  check('11. the actual building quantizer produces eligible caches with exact former Float32 answers',()=>{
    const make=()=>{
      const out=new THREE.BatchedMesh(264,256*24,256*36,new THREE.MeshBasicMaterial());
      for(let id=0;id<256;id++) {
        const g=new THREE.BoxGeometry(.13+(id%17)/100,.25+(id%11)/100,.37+(id%7)/100);
        g.translate((id%23)-11,Math.floor(id/23),.123456789);g.rotateY(id*.071);
        quantizePositions(g,32);assert.equal(g.attributes.position.normalized,true);assert.ok(g.attributes.position.array instanceof Int16Array);
        out.addInstance(out.addGeometry(g));g.dispose();
      }
      for(let id=0;id<256;id++){out.getBoundingBoxAt(id,new THREE.Box3());out.getBoundingSphereAt(id,new THREE.Sphere());}
      return out;
    };
    const a=make(),b=make();legacyCompact(a);compactBatchBounds(b);assert.equal(b.userData.compactBounds.codec,'q16-bit-exact');
    for(let id=0;id<256;id++)equalBounds(a,b,id);
    console.log(JSON.stringify({actualBuildingQuantizerRows:256,oldBytes:a.userData.compactBounds.bytes,newBytes:b.userData.compactBounds.bytes,codec:b.userData.compactBounds,officialWholeSceneSaving:'UNMEASURED'}));
    a.dispose();b.dispose();
  });
}
