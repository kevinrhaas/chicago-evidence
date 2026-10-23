"""Archive only explicitly selected files, verify author hashes and archive readback."""
from pathlib import Path
import argparse,json,hashlib,tarfile,io,datetime,gzip,os
HERE=Path(__file__).resolve().parent
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def archive(name,entries,note):
 out=HERE/'archives'/f'{name}.tar.gz';out.parent.mkdir(exist_ok=True)
 assert not out.exists(),out
 manifest=[];seen=set()
 for src,dst,expected in entries:
  p=Path(src);assert p.is_file(),p
  assert dst not in seen and not dst.startswith('/') and '..' not in Path(dst).parts,dst;seen.add(dst)
  actual=SHA(p)
  if expected:assert expected==actual,(str(p),expected,actual)
  manifest.append({'source':str(p),'path':dst,'sha256':actual,'bytes':p.stat().st_size})
 payload={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'name':name,'scope_note':note,'source_file_count':len(manifest),'files':manifest}
 raw=json.dumps(payload,indent=2).encode()+b'\n'
 with out.open('wb') as sink,gzip.GzipFile(filename='',mode='wb',fileobj=sink,compresslevel=1,mtime=0) as gz,tarfile.open(fileobj=gz,mode='w|') as tf:
  for entry in manifest:
   p=Path(entry['source']);assert SHA(p)==entry['sha256'],'changed before archive '+str(p)
   info=tarfile.TarInfo(entry['path']);info.size=entry['bytes'];info.mode=0o644;info.mtime=0
   with p.open('rb') as f:tf.addfile(info,f)
   assert SHA(p)==entry['sha256'],'changed during archive '+str(p)
  info=tarfile.TarInfo('ARCHIVE-MANIFEST.json');info.size=len(raw);info.mode=0o644;info.mtime=0;tf.addfile(info,io.BytesIO(raw))
 with tarfile.open(out,'r:gz') as tf:
  members={m.name:m for m in tf.getmembers()};assert set(members)==seen|{'ARCHIVE-MANIFEST.json'}
  assert tf.extractfile('ARCHIVE-MANIFEST.json').read()==raw
  for entry in manifest:
   f=tf.extractfile(entry['path']);h=hashlib.sha256();n=0
   while chunk:=f.read(1024*1024):h.update(chunk);n+=len(chunk)
   assert h.hexdigest()==entry['sha256'] and n==entry['bytes'],entry['path']
 record={'name':name,'archive':str(out),'sha256':SHA(out),'bytes':out.stat().st_size,'source_file_count':len(manifest),'source_bytes':sum(e['bytes'] for e in manifest),'readback':'PASS; every archived payload hash/size and member list verified','scope_note':note}
 out.with_suffix(out.suffix+'.manifest.json').write_bytes(raw)
 out.with_suffix(out.suffix+'.receipt.json').write_text(json.dumps(record,indent=2)+'\n')
 index=HERE/'ARCHIVES.json';rows=json.loads(index.read_text()) if index.exists() else [];rows.append(record);index.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(record,indent=2));return record

def flat(root,prefix=''):
 root=Path(root);return [(p,str(Path(prefix)/p.relative_to(root)),None) for p in sorted(root.iterdir()) if p.is_file()]
def author_manifest(root,manifest):
 root=Path(root);mp=Path(manifest);d=json.loads(mp.read_text());entries=[]
 if isinstance(d,dict) and all(isinstance(v,str) and len(v)==64 for v in d.values()):items=[{'path':k,'sha256':v} for k,v in d.items()]
 elif isinstance(d,list):items=d
 elif isinstance(d,dict):items=d.get('files',d.get('entries',[]))
 else:raise ValueError('unknown manifest')
 if isinstance(items,dict):items=[{'path':k,'sha256':v if isinstance(v,str) else v['sha256']} for k,v in items.items()]
 assert items,'empty or unsupported author manifest '+str(mp)
 for item in items:
  rel=item.get('path',item.get('relative_path'));sha=item['sha256'];p=Path(rel) if Path(rel).is_absolute() else root/rel
  entries.append((p,str(p.relative_to(root)),sha))
 if mp not in [Path(e[0]) for e in entries]:entries.append((mp,str(mp.relative_to(root)),None))
 return entries
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('name');ap.add_argument('--root',type=Path,required=True);ap.add_argument('--manifest',type=Path);ap.add_argument('--note',required=True);args=ap.parse_args();entries=author_manifest(args.root,args.manifest) if args.manifest else flat(args.root);archive(args.name,entries,args.note)
