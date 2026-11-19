#!/usr/bin/env python3
"""Make a deterministic archive from the candidate's explicit safe-file whitelist."""
from pathlib import Path
import gzip,hashlib,io,json,os,tarfile
ROOT=Path(__file__).resolve().parent.parent
TOP={'assets','camera','data','generators','references','review','tools'}
BASE={'README.md','HANDOFF.txt'}
rows=[]
for directory,dirs,files in os.walk(ROOT,followlinks=False):
    path=Path(directory)
    dirs[:]=sorted(d for d in dirs if not (path/d).is_symlink() and d!='__pycache__' and (path!=ROOT or d in TOP) and not (path==ROOT/'review' and d=='tmp'))
    for name in sorted(files):
        p=path/name;rel=p.relative_to(ROOT)
        if p.is_symlink() or (path==ROOT and name not in BASE):continue
        blob=p.read_bytes();rows.append({'path':rel.as_posix(),'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest()})
rows.sort(key=lambda x:x['path'])
manifest={'schema':'chamber-original1865-candidate-public-whitelist-v1','scope':'Isolated model/source/camera candidate; both image verdicts differ; not an application integration.','rights':'Only cleared public-domain-original reference routes and original generated code/geometry/materials. No CHM poster bytes. See assets/LICENSES.md and data/sources.','excluded':['All symlinks and external dependencies','review/tmp browser profiles and temporary captures','__pycache__','Whole source books and unrelated assets','Archive/checkpoint outputs themselves'],'files':rows,'file_count':len(rows),'uncompressed_bytes':sum(x['bytes']for x in rows)}
m=(json.dumps(manifest,indent=2)+'\n').encode();(ROOT/'public-archive-manifest.json').write_bytes(m)
archive=ROOT/'public-archive.tar.gz'
with archive.open('wb')as out,gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0)as gz,tarfile.open(fileobj=gz,mode='w')as tf:
    for row in rows+[{'path':'public-archive-manifest.json'}]:
        name=row['path'];blob=(ROOT/name).read_bytes();info=tarfile.TarInfo(name);info.size=len(blob);info.mode=0o644;info.mtime=0;tf.addfile(info,io.BytesIO(blob))
with tarfile.open(archive,'r:gz')as tf:
    assert sorted(tf.getnames())==sorted([x['path']for x in rows]+['public-archive-manifest.json'])
    for row in rows:assert hashlib.sha256(tf.extractfile(row['path']).read()).hexdigest()==row['sha256']
result={'archive':'public-archive.tar.gz','bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'manifest_sha256':hashlib.sha256(m).hexdigest(),'whitelist_files':len(rows),'verification':'All archive member names and file hashes match the explicit whitelist; no symlinks.'}
(ROOT/'archive-checkpoint.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
