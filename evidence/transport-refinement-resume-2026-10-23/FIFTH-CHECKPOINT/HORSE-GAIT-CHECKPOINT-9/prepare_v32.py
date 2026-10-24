from pathlib import Path
import shutil
r=Path(__file__).parent;d=r/'V32-NATIVE-REPEAT-ONLY-PROOF';d.mkdir(exist_ok=False);old=r/'V31-SPLIT-PORTABLE-CREEPING-PROTOTYPE'
shutil.copy2(old/'creeping-015mps-PORTABLE-STUDY-NOT-APP.glb',d/'creeping-015mps-PORTABLE-STUDY-NOT-APP.glb')
s=(old/'read_native_mixer.mjs').read_text();s=s.replace("const start=performance.now(),bytes=read('creeping-015mps-PORTABLE-STUDY-NOT-APP.glb'),", "const start=performance.now(),bytes=read('creeping-015mps-PORTABLE-STUDY-NOT-APP.glb'),");s=s.replace("const loader=new GLTFLoader();", "assert.equal(sha(bytes),'8fc20cf20549d9588c56202d93315dc9f718531fc7a285de2208ce4e36ba9a7b');\nconst loader=new GLTFLoader();")
s=s.replace('action.setLoop(T.LoopOnce,1);action.clampWhenFinished=true;', 'action.setLoop(T.LoopRepeat,Infinity);action.clampWhenFinished=false;')
s=s.replace('actualTimes.push(encodedTimes[128]);', "actualTimes.push(encodedTimes[128]);for(const epsilon of[.001,.0001])actualTimes.push(clip.duration-epsilon,clip.duration+epsilon,epsilon,2*clip.duration-epsilon);const snapshots=new Map();")
s=s.replace('for(let k=0;k<=256;k++){', 'for(let k=0;k<actualTimes.length;k++){\n const snapshot=[];')
s=s.replace('const time=1.6*k/256;', 'const time=k<=256?1.6*k/256:actualTimes[k]/clip.duration*1.6;')
s=s.replace('fs.writeSync(fd,Buffer.from(out.buffer));', 'fs.writeSync(fd,Buffer.from(out.buffer));if(k===0||k>=256)snapshot.push(out);')
s=s.replace("frames.push({time_s:time,", "if(k===0||k>=256)snapshots.set(k,snapshot);\n frames.push({time_s:time,")
s=s.replace('fs.closeSync(fd);assert(negative>0', """fs.closeSync(fd);
function compare(ia,ib){let position=0,normal=0;const aa=snapshots.get(ia),bb=snapshots.get(ib);for(let mi=0;mi<3;mi++)for(let i=0;i<aa[mi].length;i+=6){position=Math.max(position,Math.hypot(aa[mi][i]-bb[mi][i],aa[mi][i+1]-bb[mi][i+1],aa[mi][i+2]-bb[mi][i+2]));normal=Math.max(normal,Math.hypot(aa[mi][i+3]-bb[mi][i+3],aa[mi][i+4]-bb[mi][i+4],aa[mi][i+5]-bb[mi][i+5]));}return{maximum_position_m:position,maximum_shader_normal_vector:normal};}
const wrap=[];for(let wi=0;wi<2;wi++){const epsilon=[.001,.0001][wi],minus=257+4*wi,plus=minus+1,phasePlus=minus+2,previousMinus=minus+3;let curvature=0;for(let mi=0;mi<3;mi++){const a=snapshots.get(minus)[mi],b=snapshots.get(plus)[mi],zero=snapshots.get(0)[mi];for(let i=0;i<a.length;i+=6)curvature=Math.max(curvature,Math.hypot(a[i]+b[i]-2*zero[i],a[i+1]+b[i+1]-2*zero[i+1],a[i+2]+b[i+2]-2*zero[i+2]));}wrap.push({epsilon_s:epsilon,matched_after_wrap_vs_phase_epsilon:compare(plus,phasePlus),matched_before_wrap_vs_previous_cycle:compare(minus,previousMinus),smooth_motion_across_2epsilon:compare(plus,minus),minus_to_zero:compare(minus,0),zero_to_plus:compare(0,plus),symmetric_curvature_residual_m:curvature});}
save('ACTUAL-NATIVE-LOOPREPEAT-WRAP-PROOF.json',{scope:'Native LoopRepeat only; originalLoopOnce clampFAIL and upstreamSVDmemoryFAIL remain unqualified',clip_duration_s:clip.duration,authored_duration_s:1.6,exact_boundary_phase_comparison:compare(0,256),wrap_samples:wrap,normalization_wrapper:false,stop_or_clamp_transition_qualified:false,natural_gait_accepted:false});
assert(negative>0""")
(d/'read_native_mixer.mjs').write_text(s)
s=(old/'check_actual_readback.py').read_text().replace('assert len(frames)==257','assert len(frames)==265').replace('shape=(257,sum(counts),6)','shape=(265,sum(counts),6)').replace('if k%4==0 and k>=4:', 'if k%4==0 and 4<=k<=256:').replace('last=mat.copy()', 'if k==256:last=mat.copy()').replace('raw[-1,:,:3]','raw[256,:,:3]').replace('raw[-1,:,3:]','raw[256,:,3:]')
s=s.replace("out={'status':", "out={'repeat_only_scope':'NativeLoopRepeat only, including8 matched-wrap samples; LoopOnce stop/clamp and upstream generationmemory FAIL remain', 'maximum_position_error_vs_intended_source129_m':intended_position_error,'maximum_shader_normal_error_vs_intended_source129':intended_normal_error,'status':")
(d/'check_actual_readback.py').write_text(s);print(d)
