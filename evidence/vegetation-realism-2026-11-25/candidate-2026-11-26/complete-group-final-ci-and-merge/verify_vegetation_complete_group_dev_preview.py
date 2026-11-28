"""Verify that the served Dev build contains the actual merged tree changes."""
import datetime,hashlib,json,re,subprocess,urllib.request
from pathlib import Path
W=Path('/workspace/work');R=W/'better-trees-seasons-current'
def read(p):return json.loads(Path(p).read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True).strip()
m=read(W/'vegetation-complete-group-merge-receipt.json');p=read(W/m['qualified_integration_proof'])
assert m['merged'] and m['pr']==2414 and m['head']==p['final_head']
base='https://dev.chicago.polecat.live/4d/dev/'
verification_nonce=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f')
def fetch(path):
 q=urllib.request.Request(base+path+'?better-trees='+m['merge_sha'][:12]+'&verification='+verification_nonce,headers={'Cache-Control':'no-cache'})
 with urllib.request.urlopen(q,timeout=20) as response:return response.read()
out={'complete':False,'pr':2414,'merge_sha':m['merge_sha'],'url':base,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 build=json.loads(fetch('build.json'));out['build']=build
 assert build['tier']=='dev' and build['ref']=='refs/heads/dev'
 short=build['sha'];assert re.fullmatch('[0-9a-f]{7,40}',short)
 exists=subprocess.run(['git','rev-parse','--verify',short+'^{commit}'],cwd=R,capture_output=True,text=True)
 if exists.returncode:
  subprocess.run(['git','fetch','--quiet','--no-write-fetch-head','--refmap=','origin','refs/heads/dev'],cwd=R,check=True)
  served=git('rev-parse','--verify',short+'^{commit}')
 else:served=exists.stdout.strip()
 descended=subprocess.run(['git','merge-base','--is-ancestor',m['merge_sha'],served],cwd=R).returncode==0
 out.update(served_commit=served,served_commit_contains_actual_merge=descended)
 if not descended:out['pending']='Dev is still serving a build from before the merge.'
 else:
  rows=[]
  for name in ['rough-surface-lighting.js','buildings.js','leaf-light.js','tree-model.js','season.js','city-context.js']:
   source='chicago/4d/renderers/web/js/'+name;body=fetch('walk/js/'+name)
   digest=hashlib.sha256(body).hexdigest();expected=p['source_sha256'][source]
   assert digest==expected,(name,digest,expected)
   rows.append({'path':'walk/js/'+name,'sha256':digest,'matches_qualified_merged_source':True})
  out.update(complete=True,served_feature_files=rows)
except Exception as error:
 out['pending']=str(error)
target=W/'vegetation-complete-group-dev-preview-latest.json';target.write_text(json.dumps(out,indent=2)+'\n')
if out['complete']:
 final=W/'vegetation-complete-group-dev-preview-verification.json';assert not final.exists();final.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
