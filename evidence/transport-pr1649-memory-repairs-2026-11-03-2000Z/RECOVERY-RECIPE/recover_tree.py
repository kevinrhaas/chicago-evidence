#!/usr/bin/env python3
"""Restore this immutable source TREE using its required public prior packet.

Usage: python recover_tree.py --repo ISOLATED_CHICAGO_CLONE
Keep evidence/transport-pr1649-recovery-2026-11-03-1935Z beside this packet.
Fetch both public app parent commits first. No checkout/index/commit is changed.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,os,subprocess,sys
P=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',required=True);a=p.parse_args();R=Path(a.repo)
def git(*args,input=None):return subprocess.check_output(['git','-C',str(R),*args],input=input,env=dict(os.environ,GIT_NO_LAZY_FETCH='1'),timeout=120)
M=json.loads((P/'SOURCE-SNAPSHOT/CLOSED-SOURCE-RECOVERY-MAP.json').read_text());dep=M['public_prior_packet'];prior=P.parent/Path(dep['topic']).name
assert hashlib.sha256((prior/'MANIFEST.json').read_bytes()).hexdigest()==dep['manifest_sha256']
PM=json.loads((prior/'SOURCE-SNAPSHOT/CLOSED-SOURCE-RECOVERY-MAP.json').read_text());assert PM['source']['TREE']==dep['TREE']
for parent in M['public_parents']:git('cat-file','-e',parent+'^{commit}')
# Reuse previously recovered prior objects when present; otherwise invoke the
# required prior packet's exact recipe. This packet intentionally omits its16blobs.
need=False
for row in PM['novel_blobs']:
 q=subprocess.run(['git','-C',str(R),'cat-file','-e',row['oid']+'^{blob}'],env=dict(os.environ,GIT_NO_LAZY_FETCH='1'),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
 if q.returncode:need=True;break
if need:
 subprocess.run([sys.executable,str(prior/'RECOVERY-RECIPE/recover_tree.py'),'--repo',str(R)],check=True,timeout=600)
for row in M['novel_blobs']:
 b=gzip.decompress((P/('SOURCE-SNAPSHOT/novel-blobs/'+row['oid']+'.blob.gz')).read_bytes())
 assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
 assert git('hash-object','-w','--stdin',input=b).decode().strip()==row['oid']
raw=gzip.decompress((P/'SOURCE-SNAPSHOT/TREE.ls-tree.z.gz').read_bytes());assert hashlib.sha256(raw).hexdigest()==M['source_tree_listing_sha256'];root={}
for entry in raw.split(b'\0'):
 if not entry:continue
 meta,path=entry.split(b'\t',1);mode,kind,oid=meta.split();parts=path.split(b'/');d=root
 for name in parts[:-1]:d=d.setdefault(name,{})
 d[parts[-1]]=(mode,kind,oid)
def tree(d):
 rows=[]
 for name,value in d.items():
  if isinstance(value,dict):mode,kind,oid=b'040000',b'tree',tree(value).encode()
  else:mode,kind,oid=value
  rows.append(mode+b' '+kind+b' '+oid+b'\t'+name+b'\0')
 return git('mktree','-z','--missing',input=b''.join(rows)).decode().strip()
actual=tree(root);assert actual==M['source']['TREE'],(actual,M['source']['TREE'])
print(json.dumps(dict(status='EXACT_UNCOMMITTED_TREE_RECONSTRUCTED_WITH_PUBLIC_PRIOR_DEPENDENCY',TREE=actual,source=M['source'],prior_packet=dep,prior_recipe_rerun=need,no_index_or_checkout_changed=True),indent=2))
