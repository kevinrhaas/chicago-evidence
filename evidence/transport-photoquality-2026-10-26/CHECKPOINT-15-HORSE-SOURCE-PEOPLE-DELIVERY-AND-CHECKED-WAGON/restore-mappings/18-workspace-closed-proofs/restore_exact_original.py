#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,gzip,os,shutil
p=argparse.ArgumentParser(description="Restore one approved archived original exactly; no network or Git.");p.add_argument("original_path");p.add_argument("--manifest",default=str(Path(__file__).with_name("MAPPING.json")));a=p.parse_args();m=json.loads(Path(a.manifest).read_text());rows=[r for r in m["rows"] if r["original_path"]==a.original_path];assert len(rows)==1,"Original not in archive mapping";r=rows[0];dest=Path(r["original_path"]);arc=Path(r["archive_path"]);assert not dest.exists()and not dest.is_symlink(),"Refuse to overwrite original";h=hashlib.sha256()
with arc.open("rb")as f:
 while b:=f.read(1048576):h.update(b)
assert h.hexdigest()==r["archive_sha256"],"Archive SHA mismatch";assert shutil.disk_usage(dest.parent).free>=r["original_bytes"]+536870912,"Restore requires original bytes plus512MiB reserve";tmp=Path(str(dest)+".restore-partial");assert not tmp.exists();h=hashlib.sha256();length=0
try:
 with gzip.open(arc,"rb")as src,tmp.open("xb")as dst:
  while b:=src.read(1048576):dst.write(b);h.update(b);length+=len(b)
  dst.flush();os.fsync(dst.fileno())
 assert length==r["original_bytes"]and h.hexdigest()==r["original_sha256"],"Decoded bytes mismatch"
 os.chmod(tmp,r["original_mode"]);os.utime(tmp,ns=(r["original_mtime_ns"],r["original_mtime_ns"]));os.link(tmp,dest);tmp.unlink();fd=os.open(dest.parent,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd);print(json.dumps({"restored":str(dest),"bytes":length,"sha256":h.hexdigest(),"archive_retained":str(arc)}))
except BaseException:
 if tmp.exists():tmp.unlink()
 raise
