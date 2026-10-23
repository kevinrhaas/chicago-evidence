import subprocess,json,hashlib
from pathlib import Path
R=Path('/workspace/chicago');O=Path('/workspace/shared/merge-cycle-input-audit')
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
a=git('rev-parse','HEAD').decode().strip();b=git('rev-parse','MERGE_HEAD').decode().strip();base=git('merge-base',a,b).decode().strip()
def blob(ref,p):
 try:return git('show',ref+':'+p)
 except subprocess.CalledProcessError:return None
def changes(x,y,p=''):
 if type(x)!=type(y):return [p]
 if isinstance(x,dict):return sum((changes(x.get(k),y.get(k),p+'/'+k)for k in x.keys()|y.keys()),[])
 if isinstance(x,list):
  if len(x)!=len(y):return[p+'/#length']
  return sum((changes(v,w,p+'/'+str(i))for i,(v,w)in enumerate(zip(x,y))),[])
 return []if x==y else[p]
paths=git('ls-files','chicago/4d/data','chicago/4d/tools').decode().splitlines();paths=sorted(set(paths))
# broad corpus, excludes human assets not in either data or tools
rows=[];changed=[]
for p in paths:
 f=R/p
 if not f.is_file():continue
 cur=f.read_bytes(); old=blob(a,p)
 if old==cur:continue
 if p.startswith('chicago/4d/data/'):
  rec={'path':p,'sha256_current':hashlib.sha256(cur).hexdigest(),'equals_incoming':cur==blob(b,p)}
  try:rec['json_changed_paths_vs_head']=changes(json.loads(old),json.loads(cur))if old else['NEW']
  except Exception:rec['json_changed_paths_vs_head']=['NON_JSON']
  changed.append(rec)
# exact identity of all secondpass readers, declared reads and key corpus
m=json.loads((R/'chicago/4d/tools/derived_manifest.json').read_text()); keys=set()
for e in m['second_pass']:
 keys.add('chicago/4d/'+e['command'][1]);keys.update(e.get('reads_rebuilt',[]))
for p in paths:
 if any(x in p for x in ['1835_address_book','1835_platted','1835_off_plat','1835_lot_ledger','1835_trade_roof','1835_town_model','town_census','1835_housing_seats','1835_held_head','measure_north_branch_banks','north_branch_banks','derived_manifest']):keys.add(p)
for p in sorted(keys):
 cur=(R/p).read_bytes()if(R/p).is_file()else None
 vals={r:blob(r,p)for r in[a,b,base]}
 rows.append({'path':p,'sha256_current':hashlib.sha256(cur).hexdigest()if cur else None,'equals_head':cur==vals[a],'equals_incoming':cur==vals[b],'head_equals_mergebase':vals[a]==vals[base],'incoming_equals_mergebase':vals[b]==vals[base]})
d={'head':a,'incoming':b,'mergebase':base,'key_cycle_and_source_identity':rows,'all_changed_data':changed}
(O/'audit.json').write_text(json.dumps(d,indent=2)+'\n')
print('key mismatches',json.dumps([r for r in rows if not r['equals_head']],indent=2));print('changed data',len(changed));print('changed leaf key names',sorted(set(v.rsplit('/',1)[-1]for r in changed for v in r.get('json_changed_paths_vs_head',[]))))
