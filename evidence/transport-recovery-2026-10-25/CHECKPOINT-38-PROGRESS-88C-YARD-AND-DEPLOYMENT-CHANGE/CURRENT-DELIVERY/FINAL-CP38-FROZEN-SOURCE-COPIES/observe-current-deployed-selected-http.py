#!/usr/bin/env python3
"""Read-only official DEV deployment/selected-byte snapshot, no source qualification transfer."""
import argparse, ast, datetime, hashlib, json, subprocess
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args()
out=Path(a.out).resolve();assert str(out).startswith('/workspace/.cloud-setup/logs/transport-recovery/') and not out.exists();out.mkdir()
repo='/workspace/.cloud-setup/chicago-delivery-audit.git'
base=Path('/workspace/.cloud-setup/logs/transport-recovery')
donor=base/'70b-post-dev-composite-http-preparation-v1/verify-post-dev-selected-bytes-h3-composite-v1.py'
targets=next(ast.literal_eval(n.value) for n in ast.parse(donor.read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TARGETS' for t in n.targets))
report={'schema':'chicago-current-dev-external-merge-selected-http-v1','result':'INCOMPLETE','scope':'Actual official deployed DEV snapshot and twelve served bytes against that native Git source. No historical H3 full-renderer or whole-current-APP qualification transfer.','external_transport_M':'e03404d2cc275acfa06316835e088a1892289ab8','external_kimball_M':'19fbb127a7332776b9277763a8c7be2ed89e9a7d','http_checks':[],'selected':{},'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
def need(ok,msg):
 if not ok: raise RuntimeError(msg)
def run(cmd):
 r=subprocess.run(cmd,cwd='/workspace',capture_output=True);need(r.returncode==0,'Native read failed: '+cmd[0]);return r.stdout
def git(*args):return run(['git','--git-dir='+repo,*args])
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(rel,stem,record=True):
 cmd=['curl','--silent','--show-error','--compressed','--proto','=https','--connect-timeout','15','--max-time','90','--header','Cache-Control: no-cache','--dump-header',str(out/(stem+'.headers')),'--output',str(out/(stem+'.body')),'--write-out','%{http_code}','https://chicago.polecat.live/4d/dev/'+rel]
 r=subprocess.run(cmd,cwd='/workspace',capture_output=True);(out/(stem+'.stderr')).write_bytes(r.stderr);row={'path':rel,'url':cmd[-1],'status':r.stdout.decode().strip(),'returncode':r.returncode,'body':str(out/(stem+'.body'))}
 if record:report['http_checks'].append(row)
 need(r.returncode==0 and row['status']=='200','Official DEV request failed or redirected; preserve diagnostic')
 b=(out/(stem+'.body')).read_bytes();row.update(bytes=len(b),sha256=sha(b));return b
def ref(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
try:
 discovery=fetch('build.json','deployment-discovery',False);bd=json.loads(discovery);short=bd.get('sha','');need(8<=len(short)<=40 and all(c in '0123456789abcdef' for c in short),'Invalid official deployed commit identity')
 native=json.loads(run(['gh','api','--hostname','github.com','repos/kevinrhaas/chicago/commits/'+short]));D=native['sha'];need(len(D)==40 and D.startswith(short),'Native deployment identity ambiguous');(out/'native-deployed-commit.json').write_text(json.dumps(native,indent=2)+'\n');report['current_dev']=D
 run(['git','--git-dir='+repo,'fetch','--filter=blob:none','--no-tags','origin',D])
 for M in [report['external_transport_M'],report['external_kimball_M']]:git('merge-base','--is-ancestor',M,D)
 def verify_build(raw):
  j=json.loads(raw);need(j.get('tier')=='dev' and j.get('app')=='chicago/4d' and j.get('ref')=='refs/heads/dev' and D.startswith(j.get('sha','INVALID')),'Official DEV build moved or wrong tier');need(j.get('committedAt')==git('show','-s','--format=%cI',D).decode().strip(),'Official DEV commit date differs');return j
 first=fetch('build.json','build-before');report['build_before']=verify_build(first)
 for i,(rel,src) in enumerate(targets.items()):
  native_bytes=git('show',D+':'+src);body=fetch(rel,'asset-%02d'%i);need(body==native_bytes,'Served selected body differs from deployed native source: '+rel);report['selected'][rel]={'source_path':src,'source_git_blob':git('rev-parse',D+':'+src).decode().strip(),'bytes':len(body),'sha256':sha(body),'body':str(out/('asset-%02d.body'%i))};print('MATCH',rel,flush=True)
 last=fetch('build.json','build-after');report['build_after']=verify_build(last);need(first==last,'Official DEV deployment moved during selected-byte snapshot');need(len(report['http_checks'])==14,'Need fourteen actual recorded responses')
 h=report['selected']['walk/transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb'];need(h['sha256']=='d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914' and h['bytes']==3784176,'Selected repaired horse differs')
 scene=json.loads(Path(report['selected']['data/scenes/1835.json']['body']).read_text());anchor=next(x for x in scene['anchors'] if x['id']=='western_hotel_yard');need((anchor['local_e'],anchor['local_n'],anchor['yaw_deg'])==(-124.,-292.,221.19),'Authored yard pose differs');report['yard_anchor']=anchor
 report.update(result='PASS',all_12_served_bytes_match_actual_D=True,ui_yard_and_folded_notes_verified=False)
except BaseException as e:
 report.update(result='FAIL_OR_DEPLOYMENT_MISMATCH',error=str(e));print('STOP',str(e),flush=True)
finally:
 report['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();receipt=out/'RESULT.json';receipt.write_text(json.dumps(report,indent=2)+'\n');print('RECEIPT',str(receipt),sha(receipt.read_bytes()),report['result'],flush=True)
if report['result']!='PASS':raise SystemExit(1)
src='chicago/4d/data/render/anchor_ground_reading.json';ground=out/'current-D-anchor-ground-reading.json';ground.write_bytes(git('show',D+':'+src));pr=base/'20261025T2225-FRESH-ENDGAME-METADATA/pr1279.json';native_pr=json.loads(pr.read_text());binding={'schema':'chicago-current-dev-external-merge-yard-input-v1','scope':'Targeted official deployed D after external merge, no historical H3 qualification transfer','current_dev':D,'http_receipt':ref(receipt),'external_pr1279':{'number':1279,'head':native_pr['head']['sha'],'merge_commit':native_pr['merge_commit_sha'],'merged_at':native_pr['merged_at'],'merged':native_pr['merged'],'native_receipt':ref(pr)},'supporting_source_files':{'ground_reading':{'source_commit':D,'source_path':src,'source_git_blob':git('rev-parse',D+':'+src).decode().strip(),**ref(ground)}}};yard=out/'YARD-INPUT-BINDING.json';yard.write_text(json.dumps(binding,indent=2)+'\n')
old=read_old=base/'20261025T2225-CURRENT-DEV-REVIEW-ANNOTATION-CONTRACT/INPUT-BINDING.json';previous=json.loads(old.read_text());records=[]
for row in previous['records']:
 data=git('show',D+':'+row['source_path']);sidecar=json.loads(data);need(sidecar['id']==row['id'] and sidecar.get('review_required') is True,'Actual deployment review annotation changed');dest=out/(row['id']+'.sidecar.json');dest.write_bytes(data);records.append({'id':row['id'],'source_commit':D,'source_path':row['source_path'],'source_git_blob':git('rev-parse',D+':'+row['source_path']).decode().strip(),**ref(dest),'review_required':True,'expected_message':row['expected_message']})
contracts=[]
for row in previous['native_contracts']:
 data=git('show',D+':'+row['source_path']);excerpt=Path(row['excerpt_path']).read_bytes();need(excerpt in data,'Native annotation classification contract changed');dest=out/(Path(row['source_path']).name+'.EXACT-EXCERPT.txt');dest.write_bytes(excerpt);contracts.append({'source_commit':D,'source_path':row['source_path'],'source_git_blob':git('rev-parse',D+':'+row['source_path']).decode().strip(),'whole_source_sha256':sha(data),'excerpt_path':str(dest),'excerpt_sha256':sha(excerpt)})
review=out/'REVIEW-ANNOTATIONS-INPUT-BINDING.json';review.write_text(json.dumps({'schema':previous['schema'],'current_dev':D,'expected_ids':previous['expected_ids'],'expected_messages':previous['expected_messages'],'records':records,'native_contracts':contracts,'scope':previous['scope']},indent=2)+'\n')
print(json.dumps({'current_dev':D,'http_receipt':ref(receipt),'yard_input':ref(yard),'review_annotations_input':ref(review)}),flush=True)
