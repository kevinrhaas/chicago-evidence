from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3081-full-preflight-and-PR1260-closed');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='31cd8178d87f57619586907c8fd6008bf3f4c3efe7d27e10d072b4928e15c4db'
author=json.loads(manifest.read_text());assert len(author['files'])==18
for rel,row in author['files'].items():
 p=root/rel;assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-ACTUAL-fullpreflight1060-PASS-exit0-and-PR1260-6bf',mod.author_manifest(root,manifest),'Exact18 closed root files plus manifest. Actual repaired fullpreflight1060/383PASS exit0 withscientificreadersrequired; rawgate/changelog/idlogs/durableexitreceipt. All99code/data/native/asset snapshot files byteexact throughoutgate, onlytwo documentation paragraphs addedaftergate;postcommitT3081changelog/idchecksPASS. Committed6bf9d0e91/pushednormally,normalPR1260 openeddev/ownedlapacquired/reviewtoolpushed;binarypatchversuslandeddev026/PRpayload included. At capture publishedappQA/remotefullsmokes were LIVE andexcluded,notclaimedPASS. Originalpicturecases OPEN,no production/main deployment or finalmergeapproval. Later smoke failures remain in separate checkpoints; native/source unchanged by this archive.')
