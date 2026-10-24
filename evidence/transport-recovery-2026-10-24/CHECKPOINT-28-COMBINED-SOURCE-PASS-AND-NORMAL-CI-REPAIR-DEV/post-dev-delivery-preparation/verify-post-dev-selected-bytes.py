#!/usr/bin/env python3
"""Explicit READ-ONLY public DEV HTTP verification; never launches a browser or writes a repository."""
import argparse,hashlib,json,os,re,subprocess,time
from pathlib import Path
ROOT=Path('/workspace/chicago'); DEV='https://chicago.polecat.live/4d/dev/'
TARGETS={
 'walk/transport/parked-brougham/brougham-near.glb':'chicago/4d/renderers/web/transport/parked-brougham/brougham-near.glb',
 'walk/transport/parked-brougham/brougham-mid.glb':'chicago/4d/renderers/web/transport/parked-brougham/brougham-mid.glb',
 'walk/transport/parked-brougham/brougham.json':'chicago/4d/renderers/web/transport/parked-brougham/brougham.json',
 'data/transport/parked/placements.json':'chicago/4d/data/transport/parked/placements.json',
 'data/transport/parked/standing-horses.json':'chicago/4d/data/transport/parked/standing-horses.json',
 'data/transport/parked/horse-sevket-sidecar.json':'chicago/4d/data/transport/parked/horse-sevket-sidecar.json',
 'walk/transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb':'chicago/4d/renderers/web/transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb',
 'walk/js/standing-horses.js':'chicago/4d/renderers/web/js/standing-horses.js',
 'walk/js/standing-horse-planted-idle.js':'chicago/4d/renderers/web/js/standing-horse-planted-idle.js',
 'walk/js/parked-transport.js':'chicago/4d/renderers/web/js/parked-transport.js',
 'walk/css/walk.css':'chicago/4d/renderers/web/css/walk.css',
 'data/scenes/1835.json':'chicago/4d/data/scenes/1835.json',
}
REQUIRED_HASHES={
 'walk/transport/parked-brougham/brougham-near.glb':'bce1ecc757a7175cb193b1263fc8dbcdf1ce76a263916d3cff5e41dc4a835938',
 'walk/transport/parked-brougham/brougham-mid.glb':'65eec8b7e04e636c90e2d797f5e7e8c1d2695f0f45c6fb5c7f340f73e5616fa1',
 'walk/transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb':'d4544c2845256858dfa614235bcb37cb964ab63095a53a2436225182cefbb914',
 'walk/css/walk.css':'e780623862943720d6d30322423c4f7e3ed886f80064dbfaa2bb6f9aa85c55ce',
}
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},stderr=subprocess.PIPE)
def main():
 q=argparse.ArgumentParser();q.add_argument('--execute-read-only-dev-check',action='store_true');q.add_argument('--merge-head',required=True);q.add_argument('--source-head',required=True);q.add_argument('--source-manifest',required=True);q.add_argument('--manifest-sha256',required=True);q.add_argument('--out',required=True);a=q.parse_args()
 need(a.execute_read_only_dev_check,'Preparation only; explicit execution flag required')
 need(all(re.fullmatch('[0-9a-f]{40}',v) for v in [a.merge_head,a.source_head]),'Supply complete actual M and tested H commit SHAs')
 need(re.fullmatch('[0-9a-f]{64}',a.manifest_sha256),'Supply the final source-H published manifest file SHA256')
 out=Path(a.out).resolve();need(str(out).startswith('/workspace/.cloud-setup/') and not out.exists(),'Use NEW external output directory')
 # No fetch or repository mutation: root must make both reviewed commit objects available first.
 for h in [a.merge_head,a.source_head]:need(git('rev-parse',h+'^{commit}').decode().strip()==h,'Commit object missing/mismatched')
 need(subprocess.run(['git','merge-base','--is-ancestor',a.source_head,a.merge_head],cwd=ROOT,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True).returncode==0,'Tested H is not an ancestor of supplied ordinary merge M')
 raw=Path(a.source_manifest).read_bytes();need(sha(raw)==a.manifest_sha256,'Source-H manifest file hash changed');doc=json.loads(raw);rows=doc if isinstance(doc,list) else doc['files'];expected={r['path']:r for r in rows};need(len(expected)==len(rows),'Duplicate manifest paths')
 if isinstance(doc,dict) and 'head' in doc:need(doc['head']==a.source_head,'Manifest head differs')
 for public,src in TARGETS.items():
  need(public in expected,'Selected asset missing from final source-H manifest: '+public);b=git('show',a.source_head+':'+src);m=git('show',a.merge_head+':'+src)
  need(sha(b)==expected[public]['sha256'] and len(b)==expected[public]['bytes'],'Source-H manifest does not match its source: '+public);need(m==b,'Selected source changed in merge M: '+public)
  if public in REQUIRED_HASHES:need(sha(b)==REQUIRED_HASHES[public],'Reviewed feature identity changed: '+public)
 out.mkdir();start=time.monotonic();report={'scope':'PUBLIC DEV build and selected served bytes only; normal-UI yard view remains separate. Not production promotion, photographic acceptance or full renderer gate.','merge_head':a.merge_head,'tested_source_head':a.source_head,'source_manifest_sha256':a.manifest_sha256,'expected_source_tree':git('rev-parse',a.source_head+'^{tree}').decode().strip(),'http_checks':[],'normal_ui_yard_verified':False}
 def fetch(rel,stem):
  need(rel=='build.json' or rel in TARGETS,'Only reviewed DEV paths are allowed');url=DEV+rel;body=out/(stem+'.body');headers=out/(stem+'.headers');err=out/(stem+'.stderr')
  command=['curl','--silent','--show-error','--compressed','--proto','=https','--connect-timeout','15','--max-time','90','--header','Cache-Control: no-cache','--dump-header',str(headers),'--output',str(body),'--write-out','%{http_code}',url]
  # No --location: a redirect can never silently follow a production URL. --compressed hashes HTTP-decoded representation bytes, not compressed wire bytes.
  run=subprocess.run(command,capture_output=True);err.write_bytes(run.stderr);status=run.stdout.decode(errors='replace').strip();record={'url':url,'http_status':status,'curl_returncode':run.returncode,'command':command,'body_file':body.name,'headers_file':headers.name};report['http_checks'].append(record)
  need(run.returncode==0 and status=='200','DEV request failed/stale/redirected; inspect retained receipt: '+rel);b=body.read_bytes();record.update(bytes=len(b),sha256=sha(b));return b
 def verify_build(raw):
  d=json.loads(raw);v=d.get('sha','');need(d.get('tier')=='dev' and d.get('ref')=='refs/heads/dev' and d.get('app')=='chicago/4d','Not the official DEV preview build contract');need(re.fullmatch('[0-9a-f]{7,40}',v) and a.merge_head.startswith(v),'Public DEV sha does not identify supplied M');need(d.get('committedAt')==git('show','-s','--format=%cI',a.merge_head).decode().strip(),'Public DEV commit date differs from M');return d
 try:
  first=fetch('build.json','build-before');report['build_before']=verify_build(first);actual={}
  for n,rel in enumerate(TARGETS):
   b=fetch(rel,'asset-%02d'%n);want=expected[rel];need(sha(b)==want['sha256'] and len(b)==want['bytes'],'Served representation differs from tested H: '+rel)
   if rel.endswith('.json'):actual[rel]=json.loads(b)
  p=actual['data/transport/parked/placements.json']['models']['studebaker_brougham_1893'];need(p['file']=='transport/parked-brougham/brougham-near.glb' and p['delivery_lods']['mid']=='transport/parked-brougham/brougham-mid.glb' and p['delivery_lods']['runtime_distance_selection_enabled'] is True,'Public Brougham selection changed')
  horses=actual['data/transport/parked/standing-horses.json'];row=next(x for x in horses['scenes']['1835'] if x['id']=='western_hotel_yard_standing_horse_01');model=horses['models'][row['model']];spec=actual['data/transport/parked/horse-sevket-sidecar.json'];need(model['file']==spec['runtime_asset']['file']=='transport/standing-horse/horse-sevket-v16-planted-standing-eye-uv-v1.glb' and spec['runtime_asset']['sha256']==REQUIRED_HASHES['walk/'+model['file']] and spec['runtime_asset']['bytes']==3784176,'Public horse selected identity changed');need(row['at_local_enu_m']==[-127.5,-296.0],'Public horse placement changed')
  scene=actual['data/scenes/1835.json'];source_scene=json.loads(git('show',a.source_head+':chicago/4d/data/scenes/1835.json'));need(scene['anchors']==source_scene['anchors'] and len(scene['anchors'])==19,'Public nineteen-anchor inventory changed');anchor=next(x for x in scene['anchors'] if x['id']=='western_hotel_yard');need((anchor['local_e'],anchor['local_n'],anchor['yaw_deg'])==(-124.0,-292.0,221.19),'Public yard viewpoint changed');report['yard_anchor']=anchor
  last=fetch('build.json','build-after');report['build_after']=verify_build(last);need(last==first,'DEV build moved during selected-byte verification');report['result']='PASS: public DEV M and twelve selected representations verified; UI yard view pending';return 0
 except BaseException as e:report['result']='FAIL or DEPLOYMENT NOT YET MATCHING: inspect actual evidence';report['error']=str(e);return 1
 finally:
  report['seconds']=time.monotonic()-start;(out/'POST-DEV-HTTP-VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n');files=[]
  for p in sorted(out.iterdir()):
   if p.is_file():b=p.read_bytes();files.append({'path':p.name,'bytes':len(b),'sha256':sha(b)})
  (out/'OUTPUT-MANIFEST.json').write_text(json.dumps({'files':files},indent=2)+'\n');print(json.dumps({'result':report.get('result'),'output':str(out)}))
if __name__=='__main__':raise SystemExit(main())
