#!/usr/bin/env python3
"""Reconstruct the immutable source Git TREE, without changing a checkout/index.

Usage: python recover_tree.py --repo ISOLATED_CHICAGO_CLONE
Fetch the two public commits in SOURCE-SNAPSHOT/CLOSED-SOURCE-RECOVERY-MAP.json
first. This writes novel blobs and tree objects only; it creates no app commit.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,subprocess
P=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',required=True);a=p.parse_args();R=Path(a.repo)
def git(*args,input=None):return subprocess.check_output(['git','-C',str(R),*args],input=input,timeout=120)
M=json.loads((P/'SOURCE-SNAPSHOT/CLOSED-SOURCE-RECOVERY-MAP.json').read_text())
for parent in M['public_parents']:git('cat-file','-e',parent+'^{commit}')
for row in M['novel_blobs']:
 b=gzip.decompress((P/('SOURCE-SNAPSHOT/novel-blobs/'+row['oid']+'.blob.gz')).read_bytes())
 assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
 assert git('hash-object','-w','--stdin',input=b).decode().strip()==row['oid']
raw=gzip.decompress((P/'SOURCE-SNAPSHOT/TREE.ls-tree.z.gz').read_bytes())
assert hashlib.sha256(raw).hexdigest()==M['source_tree_listing_sha256']
root={}
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
print(json.dumps(dict(status='EXACT_UNCOMMITTED_TREE_RECONSTRUCTED_NO_INDEX_OR_CHECKOUT_CHANGED',TREE=actual,source=M['source']),indent=2))
