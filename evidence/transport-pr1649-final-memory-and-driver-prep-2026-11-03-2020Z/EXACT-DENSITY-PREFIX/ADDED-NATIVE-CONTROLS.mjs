// Exact configured-tier density prefixes: original JS-double comparisons, not
// Float32 thresholds or rounded keep values. Every earlier lifecycle oracle stays.
{
 const prefix=(keeps,threshold)=>{let n=0;while(n<keeps.length&&keeps[n]<threshold)n++;return n;};
 const datasets=[[],[-0,0,Number.MIN_VALUE,.25-Number.EPSILON,.25,.25+Number.EPSILON,.5,.6,1],
  [-Infinity,-0,0,.1,Infinity],[.1,NaN,.2],[.2,.8,.1],[NaN]];
 for(const raw of datasets)for(const initial of[null,.3])for(const dens of[
  {full:4,balanced:2,light:1},{full:0,balanced:0,light:0},
  {full:1,balanced:NaN,light:-0},{full:2,balanced:Infinity,light:-1},
 ]){
  // The existing Light constructor's filter precedes the original sort; kept
  // rows remain a subsequence. Direct unsorted cases also retain old stop-first.
  const kept=initial===null?raw.slice():raw.filter(k=>k<initial);
  const share={full:1,balanced:.6,light:.3},rock={userData:{keeps:kept.slice()},count:0};
  const zone={rockMeshes:[rock],tuftMesh:{count:0},tuftKeeps:kept.slice()};
  const f=Function('zones','dens','rockShare','REACH',`let level='light';const out={census:{}};${detailSource};return out;`)([zone],dens,share,reach);
  let expectedLevel='light';
  for(const next of['full','balanced','light','bogus','',null,undefined,'toString','constructor','light','full']){
   if(reach[next])expectedLevel=next;f.setDetail(next);
   const rocks=prefix(kept,share[expectedLevel]),tufts=prefix(kept,(dens[expectedLevel]??0)/(dens.full||1));
   assert.equal(rock.userData.rockWanted,rocks);assert.equal(rock.count,rocks);assert.equal(f.census.rocks,rocks);
   assert.equal(zone.tuftWanted,tufts);assert.equal(zone.tuftMesh.count,tufts);assert.equal(f.census.tufts,tufts);checks+=6;
  }
  assert.equal(Object.hasOwn(rock.userData,'keeps'),false);assert.equal(Object.hasOwn(zone,'tuftKeeps'),false);
  assert.equal(Object.getPrototypeOf(rock.userData.densityCounts),null);assert.equal(Object.getPrototypeOf(zone.tuftDensityCounts),null);
  assert.deepEqual(Object.keys(rock.userData.densityCounts),['full','balanced','light']);
  assert.deepEqual(Object.keys(zone.tuftDensityCounts),['full','balanced','light']);checks+=6;
 }
}
console.log(`PASS ${checks} total native CPU checks, including exact configured density prefixes; browser/memory UNRUN.`);
