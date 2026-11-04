from pathlib import Path
import json,subprocess,base64,hashlib,concurrent.futures,time
P=Path(__file__).parent
refs={'base':'42b9c601d51d8a93cde2706e1773f0bd00fadfbe','feature':'ba7d4bd8b1295098d458e67d7647674d61160870','incoming':'96d0612d940e3652af24875674a2e17feeb38184','integrated':'a5df5f8d0256de921762fa5a47b44c4326e1bb6f'}
paths=['assets/manifest.json','assets/manifest.web.json','data/structures/green_tree_tavern.json','data/reference_views/green_tree_tavern/andreas_1838.match.json','docs/LIBERTIES.md','docs/STATUS.md','docs/RESEARCH/green-tree-annex-T-2376/README.md']
def api(p):
 for attempt in range(3):
  r=subprocess.run(['gh','api',p],capture_output=True,timeout=40)
  if r.returncode==0:return json.loads(r.stdout)
  if any(x in r.stderr for x in [b'HTTP 503',b'HTTP 502',b'HTTP 504'])and attempt<2:time.sleep(1);continue
  raise RuntimeError(r.stderr.decode())
def read(i):
 label,ref,p=i;d=api(f'repos/kevinrhaas/chicago/contents/chicago/4d/{p}?ref={ref}');oid=d['sha'];q=P/label/p
 if q.exists()and hashlib.sha1(b'blob '+str(q.stat().st_size).encode()+b'\0'+q.read_bytes()).hexdigest()==oid:b=q.read_bytes()
 else:
  if d.get('encoding')!='base64':d=api(f'repos/kevinrhaas/chicago/git/blobs/{oid}')
  b=base64.b64decode(d['content']);assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid,(label,p)
  q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 return {'label':label,'ref':ref,'path':p,'git_blob':oid,'sha256':hashlib.sha256(b).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rows=list(ex.map(read,[(label,ref,p)for label,ref in refs.items()for p in paths]))
(P/'READBACKS.json').write_text(json.dumps(rows,indent=2));report={'refs':refs}
for path,key in [('assets/manifest.json','assets'),('assets/manifest.web.json','masters')]:
 maps=[json.load(open(P/label/path))[key]for label in refs];own={k for k in maps[0]|maps[1]if maps[0].get(k)!=maps[1].get(k)};foreign={k for k in maps[0]|maps[2]if maps[0].get(k)!=maps[2].get(k)};assert not(own&foreign),(path,own&foreign)
 for k in own:assert maps[3].get(k)==maps[1].get(k),(path,k,'lostown')
 for k in foreign:assert maps[3].get(k)==maps[2].get(k),(path,k,'lostincoming')
 for k in set(maps[3])-own-foreign:assert maps[3][k]==maps[0].get(k),(path,k,'unexpected')
 report[path]={'own_rows':sorted(own),'foreign_rows':sorted(foreign),'all_rows_exact':True}
for path in paths[2:4]+paths[6:]:assert(P/'feature'/path).read_bytes()==(P/'integrated'/path).read_bytes(),path
report['own_record_match_dossier_byte_exact']=True
for path in paths[4:6]:
 b,f,d,h=[(P/label/path).read_bytes()for label in refs];assert f.startswith(b);tail=f[len(b):];assert h.startswith(d),(path,'incomingprefixlost');assert h[len(d):].strip()==tail.strip(),(path,'tailnotexact');report[path]={'entire_incoming_raw_prefix_exact':True,'own_append_exact_ignoring_boundary_blank_lines':True,'prefix_bytes':len(d),'own_append_bytes':len(tail),'invalid_utf8_prefix_bytes':sum(0xDC80<=ord(x)<=0xDCFF for x in d.decode('utf-8','surrogateescape'))}
(P/'AUDIT.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:({a:(len(v[a])if isinstance(v[a],list)else v[a])for a in v}if isinstance(v,dict)else v)for k,v in report.items()},indent=2))
