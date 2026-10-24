from pathlib import Path
import hashlib,importlib.util
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rows=[('/workspace/abandoned-fetch-scratch-cleanup-20261024.json','a7b8939e8531ea4a5751a700b4fdb0a58aaf987de767517132bc09a47d2b9d8e',1803),('/workspace/abandoned-fetch-scratch-cleanup-batch2-20261024.json','7575fa5dab2eb9e64c8a01215430f197c11c8cdde14fffd5c278802bb21e4680',11356)]
entries=[]
for name,expected,size in rows:
 p=Path(name);assert p.is_file() and not p.is_symlink();data=p.read_bytes();assert len(data)==size and hashlib.sha256(data).hexdigest()==expected;entries.append((p,p.name,expected))
mod.archive('ROOT-author-incomplete-fetch-scratch-cleanup-RECEIPTS-ONLY',entries,'Exact two closed root-author operational cleanup receipts, preserved as records only. Root reports removal exclusively of checksum-invalid,>20hour-old unopened/unindexed incomplete failed-fetch scratch, no source/archive/indexedGitobjects. First receipt4rows/742604796bytes,second36rows/6755958727bytes. Archivist verifies receipt bytes/hashes and archives records;performsNOcleanup/pruning/deletion and doesnot rerun author scripts. No source/gate/PR/image acceptance or independently reexecuted removal claim.')
