from pathlib import Path
P=Path(__file__).parent;old=Path('/tmp/fort-parade-recovery-20261104/runtime/probe.mjs').read_text();prefix=old[:old.index("  if (leg === 'cards') {")];body=old[old.index('  // Trusted native skyclick'):old.index('\n  }\n  guard();',old.index('  // Trusted native skyclick'))];body='\n'.join(l for l in body.splitlines()if not l.strip().startswith('const byGrade='))+'\n';tail=old[old.index('\n  guard();',old.index('  // Trusted native skyclick')):];tail=tail.replace("status: leg === 'cards' ? 'ACTUAL_FORT_CARDS_PASS' : 'ACTUAL_FORT_BODY_PASS'","status: 'ACTUAL_MAGAZINE_BODY_DESIGN_SOURCES_PASS'")
for before,after in [('first_fort_dearborn_small_house_ne','first_fort_dearborn_magazine'),('First Fort NE house','First Fort magazine'),('First Fort NE','First Fort magazine')]:prefix=prefix.replace(before,after);body=body.replace(before,after);tail=tail.replace(before,after)
presence=r'''
  const magazinePresence = await page.evaluate(async expected => {
    const a=window.__chicago4d,id='first_fort_dearborn_magazine';
    const matrix=a.buildings.matrixOf(id),box=a.buildings.instanceBounds()[id];
    if(!matrix||!box||a.buildings.missing.has(id))throw Error('Actual magazine building/transform missing');
    const THREE=await import('three');
    const crown=new THREE.Vector3(expected.width/2,expected.wall+expected.rise,-expected.depth/2).applyMatrix4(matrix);
    const camera=new THREE.PerspectiveCamera(35,1,.1,40);camera.position.copy(crown).add(new THREE.Vector3(0,15,0));camera.up.set(0,0,-1);camera.lookAt(crown);camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
    const hit=await a.buildings.pickAtAsync(new THREE.Vector2(0,0),camera);
    if(hit?.id!==id||!Number.isFinite(hit.distance)||!hit.point?.toArray().every(Number.isFinite))throw Error('Real GPU ray missed native magazine roof');
    if(hit.point.distanceTo(crown)>.02)throw Error('Magazine roof crown differs from current declared rise');
    return{id,box,matrix:matrix.elements,expectedCrown:crown.toArray(),nativeRay:{id:hit.id,point:hit.point.toArray(),distance:hit.distance},scope:'Actual current uploaded native roof GPU hit at current reconstructed crown. No proxy/bbox-only proof or historical metric claim.'};
  },plan.magazineDimensions);
  save('MAGAZINE-REAL-GPU-PRESENCE.json',magazinePresence);
'''
cards=r'''
  await page.evaluate(async id=>{const a=window.__chicago4d;a.popup.close();a.pick(id);await a.navigator.select('inspect');a.navigator.open(2);},'first_fort_dearborn_magazine');
  await page.waitForFunction(()=>{const r=document.getElementById('nav-app-inspect');return r?.dataset.structure==='first_fort_dearborn_magazine'&&!!r.querySelector('.insp-tabs');});
  const inspect=page.locator('#nav-app-inspect');
  await inspect.locator('[data-insp-tab="design"]').click();
  await page.waitForFunction(()=>document.querySelector('#nav-app-inspect [data-insp-pane="design"]')?.dataset.filled==='yes');
  const design=inspect.locator('[data-insp-pane="design"]');assert(await design.isVisible());
  const designState=await design.evaluate(el=>({text:el.innerText,rows:[...el.querySelectorAll('.insp-hot')].map(x=>({label:x.querySelector('.insp-hot-text')?.textContent,detail:x.querySelector('.insp-hot-detail')?.textContent,grade:x.dataset.grade})),rect:(()=>{const r=el.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height};})()}));
  const roof=designState.rows.find(x=>x.label==='Roof'),rise=designState.rows.find(x=>x.label==='Barrel rise');assert(roof&&roof.detail==='barrel vault'&&roof.grade==='inferred');assert(rise&&rise.grade==='reconstructed'&&rise.detail.includes(String(plan.magazineDimensions.rise)));assert(!designState.rows.some(x=>/roof pitch/i.test(x.label)));
  save('MAGAZINE-ACTUAL-DESIGN.json',designState);
  await design.locator('.insp-hot').filter({has:page.locator('.insp-hot-text',{hasText:/^Roof$/})}).evaluate(el=>el.scrollIntoView({block:'start'}));
  await page.screenshot({path:path.join(out,'magazine-design-roof-rise.jpg'),type:'jpeg',quality:92});
  await inspect.locator('[data-insp-tab="sources"]').scrollIntoViewIfNeeded();await inspect.locator('[data-insp-tab="sources"]').click();
  await page.waitForFunction(()=>document.querySelector('#nav-app-inspect [data-insp-pane="sources"]')?.dataset.filled==='yes');
  const sources=inspect.locator('[data-insp-pane="sources"]');assert(await sources.isVisible());
  const roofFact=sources.locator('details.src-fact').filter({has:page.locator('.src-label',{hasText:/^Roof type$/i})});assert.equal(await roofFact.count(),1);await roofFact.locator(':scope > summary').scrollIntoViewIfNeeded();await roofFact.locator(':scope > summary').click();
  const roofState=await roofFact.evaluate(el=>({open:el.open,grade:el.dataset.grade,text:el.textContent,note:el.querySelector('.src-why')?.textContent??'',noteWithheld:!!el.querySelector('.src-why-later')}));assert(roofState.open&&roofState.grade==='inferred'&&/barrel vault/i.test(roofState.text)&&/1912/.test(roofState.text)&&/1808/.test(roofState.text));assert.equal(roofState.noteWithheld,plan.expectedRoofNoteWithheld,'Visitor Sources intentionally refers notes with ticket plumbing to the researcher record');
  await roofFact.locator('.src-why').evaluate(el=>el.scrollIntoView({block:'start'}));await page.screenshot({path:path.join(out,'magazine-sources-roof-note.jpg'),type:'jpeg',quality:92});
  const citeFold=roofFact.locator('details.src-cites');assert.equal(await citeFold.count(),1);await citeFold.locator(':scope > summary').scrollIntoViewIfNeeded();await citeFold.locator(':scope > summary').click();
  const citations=[];
  for(const [label,pattern]of [['whistler',/Whistler/],['currey',/Currey/]]){
    const row=citeFold.locator('ol.cites > li').filter({hasText:pattern});assert.equal(await row.count(),1);await row.evaluate(el=>el.scrollIntoView({block:'start'}));
    const actual=await row.evaluate(el=>{const r=el.getBoundingClientRect();return{text:el.innerText,links:[...el.querySelectorAll('a[href]')].map(a=>a.href),rect:{x:r.x,y:r.y,width:r.width,height:r.height,intersects:r.bottom>0&&r.top<innerHeight}}});assert(actual.rect.intersects&&actual.links.length);assert(new RegExp(label==='whistler'?'1808':'1912').test(actual.text));citations.push({label,...actual});await page.screenshot({path:path.join(out,`magazine-sources-${label}-credit.jpg`),type:'jpeg',quality:92});
  }
  const riseFact=sources.locator('details.src-fact').filter({has:page.locator('.src-label',{hasText:/^Barrel rise \(m\)$/i})});assert.equal(await riseFact.count(),1);await riseFact.locator(':scope > summary').scrollIntoViewIfNeeded();await riseFact.locator(':scope > summary').click();
  const riseState=await riseFact.evaluate(el=>({open:el.open,grade:el.dataset.grade,text:el.textContent,note:el.querySelector('.src-why')?.textContent??''}));assert(riseState.open&&riseState.grade==='reconstructed'&&/not a measured vault rise/i.test(riseState.note)&&/varying tangent/i.test(riseState.note));
  await riseFact.locator('.src-why').evaluate(el=>el.scrollIntoView({block:'start'}));await page.screenshot({path:path.join(out,'magazine-sources-reconstructed-rise.jpg'),type:'jpeg',quality:92});
  save('MAGAZINE-ACTUAL-SOURCES.json',{roofState,riseState,citations,scope:'Actual current1812 Inspect Sources expanded notes and citations; screenshot crop limits require direct pixel review. No full long text visibility claim.'});
'''
prefix=prefix.replace("/** Actual published1812 First Fort NE house evidence/one Currey source link, zero held pictures card and current pyramidroof exterior/arrival per viewport. No source or renderer overrides. */","/** Actual current1812 Magazine body/Design/Sources with real native GPU roof/ground presence. No scene/renderer/source overrides. */")
tail=tail.replace('Normal/ByGrade exterior','normal-view exterior').replace('Separate actual full-detail native world on the same frozen head; curated','Actual full-detail native world on the frozen current head; curated')
prefix='/** Actual current1812 Magazine body/Design/Sources with native GPU roof/ground presence. No scene/renderer/source overrides. */\n'+prefix.split('\n',1)[1]
prefix=prefix.replace("assert(['cards', 'body'].includes(leg));","assert.equal(leg, 'body');")
tail='\n'.join("  save('RESULT.json', {status:'ACTUAL_MAGAZINE_BODY_DESIGN_SOURCES_PASS', viewport,leg,head:plan.expected_head,qualified_source_scope_sha256:plan.source_scope_sha256,magazinePresence,fortExterior,fortArrival,designState,roofState,riseState,citations,errors,network,cancelled,consoleErrors,serverErrors,wall_ms:performance.now()-started,native_capture_timeout_unchanged:true,no_wallclock_10s_or_FPS_claim:true,no_retry:true,scope:'Actual current1812 Magazine normal exterior, native crown GPU pick, real ground/parade presence, safe native arrival, and physically opened Inspect Design/Sources. No ByGrade, full long-paragraph visibility, old107 run, historical camera, whole-fort match or completion claimed.'});" if "save('RESULT.json'" in l else l for l in tail.splitlines())+'\n'
(P/'probe.mjs').write_text(prefix+presence+body+cards+tail)
