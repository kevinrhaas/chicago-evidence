"""Late-fill final qualification SPEC; no browser, source, GitHub or ticket mutation."""
from pathlib import Path
import json,hashlib,argparse,subprocess
A=argparse.ArgumentParser();A.add_argument('--freeze',action='store_true');a=A.parse_args();O=Path('/tmp/nov10-pr1910-final-qualification');R=Path('/tmp/chicago-west-wicket-20261109');N=Path('/tmp/nov10-final-three-native');P=Path('/tmp/nov10-pr1910-source-checkpoint');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
prior=json.loads((P/'GITHUB-CHECKPOINT-RECEIPT.json').read_text());assert prior['commit']=='2969e726f1d28c20176174cf0ac517d915041871' and prior['exact_readbacks'];prior_hash={v['sha256']:(name,v) for name,v in prior['files'].items()};files={};reused={};git_reused={};blocked=[]
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
git_refs=[head,'0da21c5','53b9bd1a','b9c767997c452740c6b690cf2d280d7f75c8c9d5']
git_cache={}
def add(dest,p):
 p=Path(p)
 if not p.is_file():return
 if p.suffix.lower() in ['.glb','.gltf','.blend','.zip','.pyc'] or '__pycache__' in p.parts:return
 h=sha(p)
 if h in prior_hash:
  name,row=prior_hash[h];reused[dest]={'commit':prior['commit'],'path':prior['prefix']+name,'sha256':h,'bytes':row['bytes']};return
 # Source PR already durably carries accepted records and native picture pairs.
 # Reuse exact immutable Git blobs instead of duplicating committed artifacts.
 rel=None;raw=str(p)
 if '/chicago/4d/' in raw:rel='chicago/4d/'+raw.split('/chicago/4d/',1)[1]
 elif '/immutable-published-source/' in raw:
  tail=raw.split('/immutable-published-source/',1)[1]
  if tail.startswith('data/'):rel='chicago/4d/'+tail
  elif tail.startswith('walk/'):rel='chicago/4d/renderers/web/'+tail[5:]
 if rel:
  for ref in git_refs:
   key=(ref,rel)
   if key not in git_cache:
    got=subprocess.run(['git','show',ref+':'+rel],cwd=R,capture_output=True)
    git_cache[key]=hashlib.sha256(got.stdout).hexdigest() if got.returncode==0 else None
   if git_cache[key]==h:
    full=subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip();oid=subprocess.check_output(['git','rev-parse',full+':'+rel],cwd=R,text=True).strip()
    git_reused[dest]={'commit':full,'path':rel,'blob_sha1':oid,'sha256':h,'bytes':p.stat().st_size,'public_source_url':'https://github.com/kevinrhaas/chicago/blob/'+full+'/'+rel};return
 if dest in files:assert files[dest]==str(p)
 files[dest]=str(p)
def tree(dest,folder):
 folder=Path(folder)
 if folder.is_dir():
  for p in sorted(folder.rglob('*')):
   if p.is_file():add(dest+'/'+p.relative_to(folder).as_posix(),p)
# Content-addressed reuse avoids repeating the public 36MB source/before package.
for p in sorted(N.iterdir()):
 if p.is_file() and not any(x in p.name for x in ['MONITOR-','CURRENT-RUNS','ACTIVE-RUNS','PROGRESS']):add('native-and-source/'+p.name,p)
for folder,prefix in [('/tmp/nov10-final-independent-review','independent-review'),('/tmp/nov10-final-three-closure-readiness','closure-readiness'),('/tmp/nov10-final-stockade-smoke','final-stockade-stage1'),('/tmp/nov10-full-ghost-rebudget','full-ghost-priced-rebudget'),('/tmp/nov10-post-b-boot','post-b-boot'),('/tmp/nov10-secondfort-published-review/B','fort-published-UI'),('/tmp/nov10-completion-ui/green-tree-final-B','green-tree-published-UI')]:tree(prefix,folder)
for p in Path('/tmp/nov10-secondfort-published-review').glob('B-*.log'):add('fort-published-UI/'+p.name,p)
for name in ['prepare-expected.mjs','review.mjs','README.md','expected-B.json']:add('fort-published-UI/helpers/'+name,Path('/tmp/nov10-secondfort-published-review')/name)
# Nine second-fort actual AFTERs and three Green Tree AFTERs, with raw renders.
fort=Path('/tmp/nov10-complete-second-fort/chicago/4d/docs/RESEARCH/second-fort-completion-T-2388');tree('second-fort-AFTER',fort/'comparisons/after');add('second-fort-AFTER/actual-comparison-review.json',fort/'actual-comparison-review.json')
for p in (fort/'comparisons').glob('*diff*'):add('second-fort-AFTER/'+p.name,p)
gt=Path('/tmp/nov10-final-three-native/green-tree-after');tree('green-tree-AFTER/raw-and-render-bindings',gt)
for p in (N/'green-tree-gate-validation/chicago/4d/docs/RESEARCH/photo-match/green_tree_tavern').glob('*'):add('green-tree-AFTER/'+p.name,p)
for name in ['ACTUAL-REVIEW-CHECKLIST.json','RENDER-BINDINGS.json','AFTER-PREPARATION.json']:add('green-tree-AFTER/'+name,Path('/tmp/nov10-green-tree-final-review')/name)
accepted=[]
for folder in ['fort_dearborn_blockhouse','fort_dearborn_commandants_quarters','green_tree_tavern']:
 for p in sorted((R/'chicago/4d/data/reference_views'/folder).glob('*.match.json')):
  d=json.loads(p.read_text());accepted.append({'record':str(p.relative_to(R)),'verdict':d.get('verdict'),'open':sum(x.get('status')=='open' for x in d.get('differences',[])),'sha256':sha(p),'glb_sha256':d.get('glb_sha256'),'camera_sha256':d.get('camera_sha256')});add('accepted-records/'+folder+'/'+p.name,p);add('accepted-records/'+folder+'/'+p.name.replace('.match.json','.json'),p.with_name(p.name.replace('.match.json','.json')))
(O/'ACCEPTED-RECORDS-READBACK.json').write_text(json.dumps({'views':accepted,'accepted_count':sum(x['verdict']=='matches' and x['open']==0 for x in accepted),'claim':'Current records only. Actual AFTER input bindings and direct reviews are separately retained; no assumed UI/performance/source-CI success.'},indent=2)+'\n');add('qualification/ACCEPTED-RECORDS-READBACK.json',O/'ACCEPTED-RECORDS-READBACK.json')
if len(accepted)!=12 or any(x['verdict']!='matches' or x['open'] for x in accepted):blocked.append('12 relevant AFTER records are not all accepted with zero open differences')
for d,p in json.loads((O/'EXTRA-FILES.json').read_text()).items():
 if not Path(p).exists():blocked.append('Missing extra artifact '+p)
 else:add(d,p)
gates=json.loads((O/'GATE-INPUTS.json').read_text())
for key,value in gates.items():
 if not isinstance(value,dict) or key=='merge_and_final_ticket_readback':continue
 if value.get('status')!='PASS' or not value.get('receipt') or not Path(value['receipt']).is_file():blocked.append(key+' pending')
 else:add('gate-receipts/'+key+Path(value['receipt']).suffix,value['receipt'])
# Save new Git commit metadata only; model binaries live in the source/native Git refs.
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();(O/'SOURCE-COMMITS-SINCE-B9.txt').write_bytes(subprocess.check_output(['git','log','--reverse','--format=fuller','b9c767997c452740c6b690cf2d280d7f75c8c9d5..'+head],cwd=R));(O/'SOURCE-DELTA-STAT.txt').write_bytes(subprocess.check_output(['git','diff','--stat','b9c767997c452740c6b690cf2d280d7f75c8c9d5',head],cwd=R));add('source/SOURCE-COMMITS-SINCE-B9.txt',O/'SOURCE-COMMITS-SINCE-B9.txt');add('source/SOURCE-DELTA-STAT.txt',O/'SOURCE-DELTA-STAT.txt')
(O/'REUSED-PUBLIC-ARTIFACTS.json').write_text(json.dumps({'source_checkpoint_commit':prior['commit'],'artifacts':reused,'rule':'Reused only when exact SHA256 bytes match prior successful public readback; no duplicate model binaries or source package.'},indent=2)+'\n');files['REUSED-PUBLIC-ARTIFACTS.json']=str(O/'REUSED-PUBLIC-ARTIFACTS.json')
(O/'REUSED-SOURCE-GIT-ARTIFACTS.json').write_text(json.dumps({'artifacts':git_reused,'rule':'Exact SHA256 of bytes read from immutable source Git blob equals the local evidence bytes; source PR retains pairs/accepted records without checkpoint duplication.'},indent=2)+'\n');files['REUSED-SOURCE-GIT-ARTIFACTS.json']=str(O/'REUSED-SOURCE-GIT-ARTIFACTS.json')
add('prior/SOURCE-CHECKPOINT-PUBLIC-RECEIPT.json',P/'GITHUB-CHECKPOINT-RECEIPT.json');add('qualification/GATE-INPUTS.json',O/'GATE-INPUTS.json');add('qualification/refresh.py',O/'refresh.py')
status={'status':'READY_TO_FREEZE' if not blocked else 'DRAFT_LATE_FIELDS_PENDING_NOT_UPLOAD_READY','observed_source_head':head,'gate_inputs':gates,'blocked':blocked,'new_file_count':len(files),'new_bytes':sum(Path(p).stat().st_size for p in files.values()),'reused_public_artifacts':len(reused),'reused_source_git_artifacts':len(git_reused),'no_model_binaries':True,'no_GitHub_ticket_or_source_mutations':True,'merge_receipt_plan':'A second tiny postmerge checkpoint may carry final merge/ticket public readbacks; do not mislabel premerge evidence as merged.'};(O/'STATUS.json').write_text(json.dumps(status,indent=2)+'\n');files['STATUS.json']=str(O/'STATUS.json')
spec={'prefix':'evidence/2026-11-10-pr1910-final-qualification/','message':'PR1910 final native/AFTER/UI/source qualification; exact reused source checkpoint and retained actual evidence; merge and ticket public readbacks separate when available','receipt':str(O/'GITHUB-CHECKPOINT-RECEIPT.json'),'files':files};target=O/('SPEC.json' if a.freeze else 'SPEC-DRAFT.json')
if a.freeze:assert not blocked,blocked
(O/'INVENTORY.json').write_text(json.dumps({d:{'source':p,'bytes':Path(p).stat().st_size,'sha256':sha(p)} for d,p in files.items()},indent=2)+'\n');spec['files']['INVENTORY.json']=str(O/'INVENTORY.json');target.write_text(json.dumps(spec,indent=2)+'\n');(O/'SPEC-VALIDATION.json').write_text(json.dumps({**status,'spec_path':str(target),'spec_sha256':sha(target)},indent=2)+'\n');print(json.dumps({k:status[k] for k in ['status','blocked','new_file_count','new_bytes','reused_public_artifacts']},indent=2))
