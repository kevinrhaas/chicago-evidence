import json,hashlib,os,shutil,subprocess,sys
from pathlib import Path
M=Path(__file__).with_name("ACTUAL-ARCHIVE-MAPPING.json")
x=json.loads(M.read_text());target=Path(sys.argv[1]);row=next(r for r in x["rows"] if r["original"]==str(target));assert not target.exists()
a=next(Path(p) for p in [row.get("final_archive",""),row.get("workspace_archive","")] if p and Path(p).is_file())
def digest(p):
 h=hashlib.sha256()
 with p.open("rb")as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()
assert digest(a)==row["archive_sha256"]
assert shutil.disk_usage(target.parent).free>row["original_stat"]["bytes"]+268435456
p=target.with_name(target.name+".restore.partial");assert not p.exists()
with p.open("xb")as out:
 rc=subprocess.run(["xz","--decompress","--stdout","--memlimit-decompress=128MiB","--",str(a)],stdout=out).returncode;out.flush();os.fsync(out.fileno())
assert rc==0 and p.stat().st_size==row["original_stat"]["bytes"] and digest(p)==row["original_sha256"]
os.chmod(p,row["original_stat"]["mode"]);os.rename(p,target);print(str(target))
