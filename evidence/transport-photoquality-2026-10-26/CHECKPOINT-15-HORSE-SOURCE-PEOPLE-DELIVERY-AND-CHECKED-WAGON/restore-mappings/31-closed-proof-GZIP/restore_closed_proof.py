#!/usr/bin/env python3
"""Offline restore: python3 restore_closed_proof.py /exact/original/path (no Git/network)."""
from pathlib import Path
import gzip,hashlib,json,os,shutil,sys
base=Path(__file__).resolve().parent;manifest=json.loads((base/'LOSSLESS-ARCHIVE-MANIFEST.json').read_bytes());assert len(sys.argv)==2,'Pass exactly one listed original path';wanted=Path(sys.argv[1]);rows=[r for r in manifest['rows'] if r['original_path']==str(wanted)];assert len(rows)==1,'Only explicitly archived closed proof paths may be restored';r=rows[0];archive=Path(r['archive_path']);h=lambda b:hashlib.sha256(b).hexdigest();z=archive.read_bytes();assert h(z)==r['archive_sha256'];raw=gzip.decompress(z);assert len(raw)==r['original_bytes'] and h(raw)==r['original_sha256']
if wanted.exists():assert h(wanted.read_bytes())==r['original_sha256'];print('Already present with exact original SHA');raise SystemExit(0)
assert shutil.disk_usage(wanted.parent).free>=r['original_bytes']+256*1048576,'Restoration would violate 256MiB reserve; first make space';temp=Path(str(wanted)+'.restoring');assert not temp.exists()
with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
os.chmod(temp,r['original_mode']);assert h(temp.read_bytes())==r['original_sha256'];os.replace(temp,wanted);print(json.dumps({'restored':str(wanted),'bytes':len(raw),'sha256':r['original_sha256'],'archive_retained':True}))
