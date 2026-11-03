from pathlib import Path
import argparse,gzip,hashlib,json,subprocess
p=argparse.ArgumentParser();p.add_argument('--git-repo',required=True);a=p.parse_args();r=Path(__file__).parent;m=json.loads((r/'MANIFEST.json').read_text());cache={}
for x in m['records']:
 if x['storage']=='prior-public-lossless-payload-reference':
  key=x['reference_public_commit']+':'+x['reference_git_path']
  if key not in cache:cache[key]=subprocess.check_output(['git','-C',a.git_repo,'show',key])
  b=cache[key]
 else:b=(r/x['payload']).read_bytes()
 assert len(b)==x['encoded_bytes']and hashlib.sha256(b).hexdigest()==x['encoded_sha256'],x['original']
 d=gzip.decompress(b);assert len(d)==x['bytes']and hashlib.sha256(d).hexdigest()==x['sha256'],x['original']
print('Verified',len(m['records']),'lossless original records including prior-public references')
