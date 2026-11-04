from pathlib import Path
import os,subprocess,json,base64,hashlib,concurrent.futures,time,shutil
P=Path(__file__).parent;F=P.parent;R=Path('/workspace/chicago-bridge-increment-20261102');O=P/'objects';O.mkdir(exist_ok=True);M=F/'current-dev-aa4-metadata';D='96d0612d940e3652af24875674a2e17feeb38184';H='aa4f5cc8057bdd04a20c832a05bf4e4195807347';E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',GIT_ALTERNATE_OBJECT_DIRECTORIES=str(O))
ns={'__file__':'/workspace/cobweb-resume-recovery-20261103/adopt_latest.py'};exec(Path(ns['__file__']).read_text().split('comparison =')[0],ns);ns['P']=P;ns['O']=O
while not(F/'qualified-push/PUSHED.json').exists():
 rr=F/'FINISH-CONTROLLER-REAPER.json'
 if rr.exists():assert json.loads(rr.read_bytes())['command_exit']is None,'Qualified source controller ended beforePUSHED; inspect'
 time.sleep(5)
assert shutil.disk_usage('/workspace').free>536870912 and shutil.disk_usage('/tmp').free>1800000000
comp=json.loads((M/'COMPARE.json').read_bytes());assert comp['ahead_by']==28 and comp['behind_by']==0 and len(comp['commits'])==28
commits={}
def existing(s):return subprocess.run(['/usr/local/bin/git','-C',str(R),'cat-file','-e',s],env=E,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
for row in comp['commits']:
 s=row['sha']
 if not existing(s):commits[s]=ns['commit'](s)
for s,d in commits.items():
 for p in d['parents']:assert p['sha']in commits or existing(p['sha']),('unknownparent',s,p['sha'])
print('commits exact',len(commits),flush=True)
def trees(s):
 data=ns['api']('git/trees/'+s+'?recursive=1');assert not data['truncated'];dirs={'':{}};ids={'':s};files={}
 for e in data['tree']:
  parent,_,name=e['path'].rpartition('/');dirs.setdefault(parent,{})[name]=e
  if e['type']=='tree':dirs.setdefault(e['path'],{});ids[e['path']]=e['sha']
  else:files[e['path']]=e
 for path,children in dirs.items():
  raw=b''.join(e['mode'].lstrip('0').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(e['sha'])for name,e in sorted(children.items(),key=lambda x:(x[0]+('/'if x[1]['type']=='tree'else'')).encode()));ns['put']('tree',raw,ids[path])
 return files
for s,d in commits.items():trees(d['tree']['sha']);print('trees exact',s,flush=True)
files=json.loads((M/'FILES.json').read_bytes());blobs={e['sha']:e for e in files.values()};ids=sorted(blobs);checks=subprocess.check_output(['/usr/local/bin/git','-C',str(R),'cat-file','--batch-check'],input=('\n'.join(ids)+'\n').encode(),env=E).decode().splitlines();missing=[line.split()[0]for line in checks if line.endswith(' missing')];assert len(missing)<=256 and sum(blobs[s]['size']for s in missing)<=256*1024**2 and all(blobs[s]['size']<32*1024**2 for s in missing)
print('TIPblobbudget',len(missing),sum(blobs[s]['size']for s in missing),flush=True)
def fetch(s):
 d=ns['api']('git/blobs/'+s);raw=base64.b64decode(d['content']);assert len(raw)==blobs[s]['size'];ns['put']('blob',raw,s);return {'git_blob':s,'path':blobs[s]['path'],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
 for row in pool.map(fetch,missing):rows.append(row);print('blob',len(rows),row['path'],flush=True)
result={'base':D,'tip':H,'tip_tree':json.loads((M/'COMMIT.json').read_bytes())['tree']['sha'],'all_28_missing_commit_raw_IDs_verified':True,'all_missing_commit_trees_verified':True,'all_missing_current_TIP_blobs_verified':True,'missing_commits':list(commits),'changed_TIP_inventory':json.loads((M/'SUMMARY.json').read_bytes()),'fetched_TIP_blobs':rows,'fetched_bytes':sum(x['bytes']for x in rows),'per_blob_cap':32*1024**2,'total_blob_cap':256*1024**2,'object_store':str(O),'standalone_no_alternates':not(O/'info/alternates').exists(),'no_active_source_Git_ref_index_worktree_mutations':True,'read_only_cache_for_R_N_no_GC_repack_delete':True,'no_intermediate_superseded_large_blobs_fetched':'Only commits/trees forbounded28 introducedcommits pluscurrentTIPmissingblobs; no foreignarchive needed.'};(P/'READY.json').write_text(json.dumps(result,indent=2)+'\n');print('READY '+H,flush=True)
