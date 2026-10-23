# SPDX-License-Identifier: GPL-3.0-or-later
"""Archive only immutable completed pose artifacts; no capture or fit execution."""
from pathlib import Path
import hashlib,json,tarfile,io,time
P=Path('/workspace/shared/horse-ab70-3bb45-motion-next');S=P/'runs/full63';OUT=Path('/workspace/shared/horse-ab70-3bb45-full63-completed-chunks');OUT.mkdir()
INDEX={'scope':'Checkpoint chunks of ACTUAL COMPLETED discrete poses; full63UNACCEPTED until terminalPASS','full63_PASS':False,'chunks':[]};nextpose=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(): (OUT/'INDEX.json').write_text(json.dumps(INDEX,indent=2)+'\n')
def archive(rows,stage,extra_failure=None):
 global nextpose
 first=rows[0]['pose']['index']if rows else nextpose;last=rows[-1]['pose']['index']if rows else first-1
 name=f'poses-{first:02d}-{last:02d}'+('-FIRSTFAILURE'if extra_failure else '')+'.tar.gz';a=OUT/name;receipt={'scope':'Selected completed actual poses only; NOTfull63acceptance','source_inventory_sha256':stage['source_inventory_sha256'],'input_sha256':stage['input_sha256'],'indices':[x['pose']['index']for x in rows],'poses':[x['pose']for x in rows],'first_failure':extra_failure,'files':{}}
 with tarfile.open(a,'x:gz',compresslevel=6)as t:
  def add(n,b):
   i=tarfile.TarInfo(n);i.size=len(b);t.addfile(i,io.BytesIO(b));receipt['files'][n]=sha(b)
  for row in rows:
   d=S/f"pose-{row['pose']['index']:02d}-{row['pose']['clip']}"
   for n,w in row['artifact_hashes'].items():
    f=d/n;b=f.read_bytes()
    if sha(b)!=w:raise ValueError('completed artifact changed '+str(f))
    add(d.name+'/'+n,b)
  if extra_failure:
   for f in sorted((S/extra_failure['directory']).rglob('*')):
    if f.is_file()and'__pycache__'not in f.parts:add('FIRSTFAILURE/'+str(f.relative_to(S)),f.read_bytes())
  b=(json.dumps(receipt,indent=2)+'\n').encode();i=tarfile.TarInfo('CHUNK-RECEIPT.json');i.size=len(b);t.addfile(i,io.BytesIO(b))
 size=a.stat().st_size
 if size>40*1024**2:raise ValueError('unexpected >40MiB archive; preserved, no retry')
 meta={'file':str(a),'sha256':sha(a.read_bytes()),'bytes':size,'completed_indices':receipt['indices'],'pose_count':len(rows),'first_failure':extra_failure};INDEX['chunks'].append(meta);nextpose=last+1;save();print(json.dumps(meta),flush=True)
save()
# Source/control evidence once, not every growing snapshot.
a=OUT/'source-and-explicit-controls.tar.gz'
with tarfile.open(a,'x:gz',compresslevel=6)as t:
 for f in sorted(P.iterdir()):
  if f.is_file():t.add(f,arcname='source/'+f.name,recursive=False)
 # controls may still execute now, so source-only archive; terminal control files later.
INDEX['source_archive']={'file':str(a),'sha256':sha(a.read_bytes()),'bytes':a.stat().st_size,'scope':'frozen actual motion source/inventories only; controls are archived at terminal'};save();print(json.dumps(INDEX['source_archive']),flush=True)
while True:
 raw=(S/'RESULT.json').read_bytes()
 try:r=json.loads(raw)
 except json.JSONDecodeError:time.sleep(1);continue
 rows=r['completed_poses'];n=len(rows)
 while n-nextpose>=7:archive(rows[nextpose:nextpose+7],r)
 if r.get('error')or r.get('PASS')is True:
  if r.get('error'):
   names=[p.name for p in S.glob('pose-*')if p.is_dir()];done={f"pose-{x['pose']['index']:02d}-{x['pose']['clip']}"for x in rows};partial=sorted(set(names)-done);extra={'error':r['error'],'directory':partial[0]}if partial else {'error':r['error'],'directory':'controls'};archive(rows[nextpose:],r,extra)
  elif nextpose<n:archive(rows[nextpose:],r)
  # Terminal source result and controls, no duplicated pose payloads.
  a=OUT/'terminal-result-and-controls.tar.gz'
  with tarfile.open(a,'x:gz',compresslevel=6)as t:
   for f in [S/'RESULT.json',*sorted((S/'controls').rglob('*'))]:
    if f.is_file()and'__pycache__'not in f.parts:t.add(f,arcname=str(f.relative_to(S)),recursive=False)
  INDEX.update(full63_PASS=r.get('PASS')is True,completed_poses=n,error=r.get('error'),terminal_stage_result_sha256=sha(raw),terminal_archive={'file':str(a),'sha256':sha(a.read_bytes()),'bytes':a.stat().st_size});save();print(json.dumps({'TERMINAL':INDEX}),flush=True);break
 INDEX.update(completed_poses=n,observed_elapsed_s=r['elapsed_s'],full63_PASS=False);save();time.sleep(20)
