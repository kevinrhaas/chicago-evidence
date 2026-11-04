"""Read actual six-leg closures and bind them to one immutable3f source/publication."""
from pathlib import Path
import hashlib,json,subprocess,re,datetime
P=Path(__file__).parent;W=Path('/tmp/wolf-poster-source-20261103');S=W/'site/4d';H='3f3e0bfcc99aad5d358fa8520da764fbe0aa68ff';sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git','-C',str(W),*a]);read=lambda p:json.loads(Path(p).read_bytes())
assert git('rev-parse','HEAD').decode().strip()==H;assert not git('status','--porcelain')
source={'HEAD':H,'index_tree':git('write-tree').decode().strip(),'working_diff_sha256':sha(git('diff','--binary')),'staged_diff_sha256':sha(git('diff','--cached','--binary')),'untracked':git('ls-files','--others','--exclude-standard').decode()}
review=read(P/'FINAL-HELPER-PEER-REVIEW.json');cardreview=read(P/'FINAL-CARDS-V3-PEER-REVIEW.json');phonereview=read(P/'FINAL-PHONE-CARDS-V4-PEER-REVIEW.json');assert phonereview['root_approved'];assert cardreview['root_approved']
for name,digest in cardreview['hashes_exact'].items():assert sha((P/name).read_bytes())==digest,('reviewedv3 drift',name)
assert read(P/'CARDS-V3-ACTUAL-POPUP-CALLSITE.json')['original_body_branch_still_exact']
assert read(P/'current-ui/desktop-cards/CLOSURE.json')['status']=='NOT_QUALIFIED'and read(P/'current-ui-cards-v2/desktop-cards/CLOSURE.json')['status']=='NOT_QUALIFIED'
for name,digest in review['hashes_exact'].items():assert sha((P/name).read_bytes())==digest,('reviewed helper drift',name)
pub={p.relative_to(S).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}for p in sorted(S.rglob('*'))if p.is_file()};pubsha=sha(json.dumps(pub,sort_keys=True).encode());assert H.startswith(read(S/'build.json')['version'])
def proper(path):
 d=read(path);assert d['command_exit']==0 and d['all_children_reaped']and not d['leftover_cleanup']and d['interrupted_signal']is None,('not properly closed',str(path));return d
rows=[];shared_inputs=None
for viewport in ['desktop','mobile']:
 for leg in ['body','cards']:
  tag=viewport+'-'+leg;O=P/('current-ui'if leg=='body'else('current-ui-cards-v3'if viewport=='desktop'else'current-ui-phone-cards-v4'))/tag;plan=read(O/'PLAN.json');closure=read(O/'CLOSURE.json');result=read(O/'actual/RESULT.json');request=read(O/'actual/CLOSURE.json')
  assert plan['source_guard']==closure['source']==source,('cross-leg source drift',tag)
  assert plan['full_publication_map_sha256']==pubsha and plan['full_publication_members']==len(pub),('cross-leg publication drift',tag)
  assert sha(json.dumps(read(O/'PUBLICATION-MAP.json'),sort_keys=True).encode())==pubsha
  assert closure['status']==('JAIL_CURRENT_PHONE_CARDS_CAPTURE_COMPLETE_VISUAL_REVIEW_PENDING'if tag=='mobile-cards'else'JAIL_CURRENT_'+tag.upper()+'_PASS')and closure['error']is None and closure['source_publication_helpers_exact']
  assert result['status']==('ACTUAL_JAIL_CARDS_CAPTURE_COMPLETE_VISUAL_REVIEW_PENDING'if tag=='mobile-cards'else'ACTUAL_JAIL_'+leg.upper()+'_PASS')and result['head']==H and result['viewport']==viewport
  assert request['failure']is None and request['zero_pre_teardown_cancellations']and not request['cancelled']
  for label in ['errors','network','consoleErrors','serverErrors']:assert not result[label]and not request[label],(tag,label)
  assert result['qualified_source_scope_sha256']==plan['source_scope_sha256'];assert sha(json.dumps(plan['input_bindings'],sort_keys=True).encode())==plan['source_scope_sha256']
  consumer_inputs={n:v for n,v in plan['input_bindings'].items()if Path(n).name not in ['jail_probe.mjs','run_ui_leg.py','jail_cards_probe_v3.mjs','run_cards_leg_v3.py','jail_phone_cards_probe_v4.mjs','run_phone_cards_leg_v4.py']}
  if shared_inputs is None:shared_inputs=consumer_inputs
  else:assert consumer_inputs==shared_inputs,('cross-leg actualconsumer drift',tag)
  expected_helpers={'jail_probe.mjs':review['hashes_exact']['jail_probe.mjs'],'run_ui_leg.py':review['hashes_exact']['run_ui_leg.py']}if leg=='body'else(cardreview['hashes_exact']if viewport=='desktop'else phonereview['hashes_exact'])
  for name,digest in expected_helpers.items():assert plan['input_bindings'][str(P/name)]['sha256']==digest,('actual helper version not proven',tag,name)
  inner=proper(O/'NATIVE-REAPER.json');outer=proper(P/('runtime-controller'if leg=='body'else('runtime-controller-v3'if viewport=='desktop'else'runtime-controller-phone-v4'))/(tag+(''if leg=='body'else('-v3'if viewport=='desktop'else'-capture'))+'-OUTER-REAPER.json'))
  shots={f.name:sha(f.read_bytes())for f in sorted((O/'actual').glob('*.jpg'))};assert len(shots)>=4
  rows.append({'leg':tag,'head':H,'full_publication_sha256':pubsha,'closure_sha256':sha((O/'CLOSURE.json').read_bytes()),'actual_result_sha256':sha((O/'actual/RESULT.json').read_bytes()),'inner_exit':inner['command_exit'],'outer_exit':outer['command_exit'],'screenshots':shots,'actual_helper_version':'originalv1'if leg=='body'else('cardsv3'if viewport=='desktop'else'phonecardsv4_manualvisualpending'),'actual_helper_hashes':expected_helpers})
for viewport in ['mobile','desktop']:
 tag=viewport+'-native3';O=P/'current-native3'/viewport;plan=read(O/'PLAN.json');closure=read(O/'CLOSURE.json')
 assert plan['source']==closure['source']==source,('native source drift',tag)
 assert plan['publication_map_sha256']==pubsha and plan['publication_members']==len(pub),('native publication drift',tag)
 assert closure['status']=='CURRENT_PUBLISHED_NATIVE_STAGE3_'+viewport.upper()+'_107_PASS'and closure['error']is None and closure['source_publication_helpers_exact']
 assert plan['helpers']['native_smoke']==sha((W/'chicago/4d/tools/smoke_renderer.mjs').read_bytes())and plan['helpers']['this']==review['hashes_exact']['run_native3_leg.py']
 log=(O/'native.log').read_text(errors='replace');counts=re.findall(r'(\d+) passed, (\d+) failed',log);assert counts and counts[-1]==('107','0')and'SMOKE PASS'in log
 inner=proper(O/'NATIVE-REAPER.json');outer=proper(P/'runtime-controller-native'/(tag+'-OUTER-REAPER.json'));rows.append({'leg':tag,'head':H,'full_publication_sha256':pubsha,'closure_sha256':sha((O/'CLOSURE.json').read_bytes()),'native_log_sha256':sha((O/'native.log').read_bytes()),'passed':107,'failed':0,'inner_exit':inner['command_exit'],'outer_exit':outer['command_exit']})
assert len(rows)==6
rootreview=read('/workspace/jail-root-ui-review-20261104/ROOT-BOTH-BODY-REVIEW.json');assert rootreview['head']==H and rootreview['direct_images_viewed']==8
for views in rootreview['images'].values():
 for item in views.values():assert sha(Path(item['path']).read_bytes())==item['sha256']
for name,binding in shared_inputs.items():assert sha(Path(name).read_bytes())==binding['sha256'],('current input drift',name)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ACTUAL_SIX_EXECUTIONS_PROPER_CLOSED_SAME3F_PHONE_VISUAL_PENDING','source':source,'full_publication_map_sha256':pubsha,'full_publication_members':len(pub),'original_frozen_helper_hashes':review['hashes_exact'],'separate_reviewed_cardsv3_hashes':cardreview['hashes_exact'],'separate_reviewed_phonev4_hashes':phonereview['hashes_exact'],'phone_acceptance':'Capture/data/error/input/reaper assertions passed; physicalvisibility requires separateROOTDIRECTSHAapproval, NOT automatedPASS','oldbody_scopedcarry':'Actual originalhelper body passes retained on byte-exact body branch and same3f publication; no claim old bodies ranv3','preserved_prior_cards_reds':[{'version':'original','seconds':164.21316198699787},{'version':'v2wrongInspector','seconds':200.4590744389934},{'version':'phonev3_whitespace_corner_false_negative','seconds':137.6176626439992}],'root_body_review_sha256':sha(Path('/workspace/jail-root-ui-review-20261104/ROOT-BOTH-BODY-REVIEW.json').read_bytes()),'legs':rows,'root_visual_review':'PENDING_SEPARATE_ROOT_REVIEW','full8_hosted':'SEPARATE_REQUIRED_GATE','original_T2380':'partial/open; no full photo-match or camera calibration claim'}
(P/'SIX-EXECUTIONS-VISUAL-PENDING-LEDGER.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)

phonepath=Path('/workspace/jail-root-ui-review-20261104/ROOT-PHONE-CARDS-V4-REVIEW.json');phone=read(phonepath)
assert sha(phonepath.read_bytes())=='5ff3ca9c9e72b09d7b0e053cd9d6eee4db9eec45ad3b4fce565eb1c4fc02bdd5'
assert phone['head']==H and phone['result']=='BOUNDED_PHONE_CARDS_VISUALLY_ACCEPTED_WITH_LIMITS'and phone['automatic_visibility_pass']is False
assert len(phone['files'])==6
for name,r in phone['files'].items():assert sha(Path(r['path']).read_bytes())==r['sha256']and r['sha256']==next(x for x in rows if x['leg']=='mobile-cards')['screenshots'][name]
result.update(status='ACTUAL_SIX_EXECUTIONS_SAME3F_PROPER_CLOSED_WITH_BOUNDED_ROOT_VISUAL_ACCEPTANCE',root_visual_review='BOUNDED_BODY_AND_PHONE_CARDS_ACCEPTED_WITH_EXPLICIT_LIMITS',phone_acceptance='Strictdata/error/input/reaper capturecomplete plus separateROOTDIRECTsiximageSHAacceptance; no automaticphysicalvisibilityPASS',root_phone_review_sha256=sha(phonepath.read_bytes()),root_phone_limits=phone['limits'],full15_native_smoke='NOT_RUN',full8_hosted={'head':H,'run':41772360078,'conclusion':'success','currentdevintegration':'Still required later; this does not qualify a future changed head'})
(P/'FINAL-CROSS-VERSION-LEG-LEDGER.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
