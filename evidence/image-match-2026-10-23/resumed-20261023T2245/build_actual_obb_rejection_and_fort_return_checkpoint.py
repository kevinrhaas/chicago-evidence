from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/PR1260-OBB-actual-001');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='873ac08e6b490c5bb183d576701aa32dab330df782671c028804865bef6efa54'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==36
if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
assert sum(r['bytes'] for r in rows)==1368399
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-OBB-ACTUAL-APPLIED-REJECTED-ZERO-SAVING-H8-RESTORED',mod.author_manifest(root,manifest),'Exact36 closed actual OBB candidate payloads plus original manifest. Candidate APPLIED/MEASURED/REJECTED:actual4666158triangles/5097calls EXACTbaseline,ZERO saving and still66158over unchanged4600000cap. Supplementalorientedcounter1is cumulative,NOT saving. ExactH8helper restored,normalpublish/mirrorPASS,sourcecleanbeforefortreturn. OriginalproposalUNMEASUREDtimepoint remains historical but latestactual is REJECTED,nofix/acceptance orstage14HOLD release. No livecanonical/watchsource selected.')
p=Path('/workspace/PR1260-fort-worktree-return-20261024.json');expected='67747e054265b1ea756d2089646a2e1956a134f4c0a3f8291281eb52ae4ae6fe';assert p.is_file() and not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==expected
r=json.loads(p.read_text());assert r['stash_retained']=='7338fd715a021ac3df9776cd208d83d88074d511' and len(r['rows'])==59
checkpoint=json.loads(Path('/tmp/chicago-fort-integration/T-3105/closed-source-handover-20261024/SOURCE-CHECKPOINT.json').read_text());assert {x['path']:x['sha256'] for x in r['rows']}=={x['path']:x['sha256'] for x in checkpoint['source_files']}
mod.archive('ROOT-author-fort-worktree-RETURN-59hashes-STASH-RETAINED',[(p,p.name,expected)],'Exact closed root-author fort-return receipt,59reported restoredpathhashes independently match frozen sourceZIPcheckpoint metadata,stash7338fd retained. Root reports restoredDAfortbranch and moves independent fullH8checkoutto/workspace/primary-human-runner-compat. IgnoredGlessner3outputs stillH8new376ae/6651e/2f142;MUSTintegrateH8beforepublishingorusenormalstalecachehandling,publishedmirrorlastH8restoreNOTrestoredfortsource. Fort resumes H8integration/native/QA separately;recordONLY,nolive59filesreadorrestoredbyarchivist. No currentfortfullgate/PR/imageacceptanceclaim.')
