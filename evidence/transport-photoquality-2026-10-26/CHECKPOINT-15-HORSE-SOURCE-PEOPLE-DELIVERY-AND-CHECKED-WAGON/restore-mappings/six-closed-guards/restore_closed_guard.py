import gzip,hashlib,json,os,shutil,sys
from pathlib import Path
x=json.loads(Path(__file__).with_name("MANIFEST.json").read_text());p=Path(sys.argv[1]);r=next(r for r in x["rows"]if r["original"]==str(p));assert not p.exists();a=Path(r["archive"]);z=a.read_bytes();assert hashlib.sha256(z).hexdigest()==r["archive_sha256"];b=gzip.decompress(z);assert len(b)==r["original_bytes"]and hashlib.sha256(b).hexdigest()==r["original_sha256"];assert shutil.disk_usage(p.parent).free>len(b)+268435456;q=Path(str(p)+".restore.partial");assert not q.exists()
with q.open("xb")as f:f.write(b);f.flush();os.fsync(f.fileno())
os.chmod(q,r["original_mode"]);os.rename(q,p);print(str(p))
