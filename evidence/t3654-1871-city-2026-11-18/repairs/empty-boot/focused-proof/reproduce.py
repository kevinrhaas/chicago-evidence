#!/usr/bin/env python3
"""Focused CLI reproduction using committed indexes/records, without app assets."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
repo,candidate,node,out=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3],Path(sys.argv[4])
commit='7e99cd8c363baced005d691b3eb1eec086a90202'
fixture=out/'committed-index-fixture';tool=fixture/'chicago/4d/tools/pack_boot_sidecars.mjs'
tool.parent.mkdir(parents=True,exist_ok=True)
source='chicago/4d/tools/pack_boot_sidecars.mjs'
original=subprocess.check_output(['git','show',commit+':'+source],cwd=repo)
bindings={}
for scene in ['1835','1871']:
 prefix=f'chicago/4d/data/sidecars/{scene}/'
 tree=subprocess.check_output(['git','ls-tree','-r','-z',commit,prefix],cwd=repo)
 blobs={}
 for entry in tree.split(b'\0'):
  if not entry:continue
  meta,name=entry.split(b'\t');blobs[name.decode()]=meta.split()[2].decode()
 def committed(rel):
  b=(repo/rel).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blobs[rel],rel
  bindings[rel]=hashlib.sha256(b).hexdigest();return b
 index_bytes=committed(prefix+'index.json');index=json.loads(index_bytes)
 for sub in ['chicago/4d/data','site/4d/data']:
  p=fixture/sub/f'sidecars/{scene}/index.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(index_bytes)
 for row in index['structures']:
  row={'id':row} if isinstance(row,str) else row
  rel=row.get('sidecar',f'sidecars/{scene}/{row["id"]}.json')
  b=committed('chicago/4d/data/'+rel)
  p=fixture/'site/4d/data'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def run(label,*args,expected):
 r=subprocess.run([node,str(tool),*args],capture_output=True,text=True,timeout=30)
 (out/(label+'.log')).write_text(r.stdout+r.stderr)
 assert r.returncode==expected,(label,r.returncode,r.stdout+r.stderr)
 return r
# The exact old CLI reproduces the actual CI failure on the unchanged 1871 index.
tool.write_bytes(original)
run('original-writer',expected=0)
r=run('original-checker', '--check',expected=1)
assert '1871/index.json: no `boot`' in r.stderr
# The candidate uses the same records/indexes. Nonempty records must rehydrate exactly.
tool.write_bytes(candidate.read_bytes())
run('candidate-writer',expected=0);run('candidate-checker','--check',expected=0)
for name,old,new in [
 ('old-writer-negative','    const { values, packed } = pack(present.map(({ row }) => read(recordPath(site, scene, row))));','    if (!present.length) continue;\n    const { values, packed } = pack(present.map(({ row }) => read(recordPath(site, scene, row))));'),
 ('old-checker-negative','      if (!existsSync(rec)) { problems.push(`${scene}/index.json: missing indexed record ${path.relative(path.dirname(site), rec)}`); continue; }','      if (!existsSync(rec)) continue;')]:
 text=candidate.read_text();assert text.count(old)==1
 tool.write_text(text.replace(old,new));run(name,'--self-test',expected=1)
tool.write_bytes(candidate.read_bytes());run('candidate-selftest','--self-test',expected=0)
summary={'base_commit':commit,'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'node':subprocess.check_output([node,'--version'],text=True).strip(),'committed_input_sha256':bindings,'original_check_exit':1,'original_failure':'1871/index.json: no `boot`','candidate_check_exit':0,'candidate_selftest_exit':0,'negative_controls':{'original_writer_in_candidate_selftest':1,'original_checker_in_candidate_selftest':1},'scope':'Real committed1835 records and empty1871 index; CLI fixture and nine corruption refusals. No browser, full publisher, full source gate or CI acceptance claimed.'}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'bound_inputs':len(bindings),'candidate_sha256':summary['candidate_sha256'],'all_expected_statuses_verified':True}))
