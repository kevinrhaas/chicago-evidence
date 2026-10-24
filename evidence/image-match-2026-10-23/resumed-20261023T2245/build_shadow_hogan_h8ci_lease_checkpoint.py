from pathlib import Path
import hashlib,importlib.util,json,zipfile,stat,gzip
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packets=[('/tmp/PR1260-shadow-ray-contingency','MANIFEST.json','1508a9236f4f4ce6807213cf2184af4044c6cd24f2843f774a11027b43caac28',27,924753,'PR1260-Full-shadow-ray-CPU-PROPOSAL-UNAPPLIED-AT-CAPTURE','Exact27 closed shadowcandidate payloads plus original manifest. Three paths from H835f0,47existing+28newCPU controlsPASS;actualshadowlist away-ray proof,toward/filter-edge kept and unknown light/filter/cadence/inverse/depth/imagesize failopen. Scope stockreceivers+Fullfreshmap,PCF/bias marginnotreduced; no geometry/caps/tier/camera change. Draftunexportedclass/testorder errorsretained. UNAPPLIED/actualsavingUNMEASUREDatclosure;parentlaterapprovedactualtestseparateLIVE/excluded,resultPENDING. RejectedOBBzero-saving andoriginal66kbudgetFAIL remain separate,no actualPASSclaim.'),('/tmp/chicago-next-model/T-3118-hogan-H8/closed-authored-H8-light-v1','MANIFEST.json','e035a1cc225a3dc20ef232167fcc6a046dc039b0277ffe0816b8f642cda0b73c',13,249870,'T3118-Hogan-H8-data-only-authored6-UNCOMMITTED-UNBAKED','Exact13 closed Hogan authored-recovery payloads plus original path-map manifest. Claimed/ticketacceptancepushedutilityT3118,H8data-onlysixauthoredpathsUNCOMMITTED;rawgeometrybyteequalprioractual470trianglecandidate,81otherfamilymembers+113generatorfilesexact. Source/date limits andoriginalT2377OPEN/DIFFERS retained. No officialbake/derive/publish/browser/native/fullgate/sourcecommit/PR atcapture;futureHoganworkseparate/noliveparentfoldercheckoutselected.'),('/workspace/PR1260-H8-actual-CI-closed-20261024','CLOSED-MANIFEST.json','cdfa7d25000f478ee205c8241170e1942c0f5d25d65f875427aa9c46dcfbe3e9',34,6335595,'PR1260-H8-ACTUAL-three-CI-SUCCESS-SYNTHETIC070582-BUDGET-FAIL-SEPARATE','Exact34 closed H8CI payloads plus originalmanifest and independentZIP/tree-readbackledger. Threeactualruns/jobs/rawlogs+ZIPs,rawwholejobbytesexactZIPentries/CRC/SHApass. Gate1063/383,moving,humansSUCCESS at actualsynthetic070582parentsc968+35f. FulluntruncatedrecursiveGitGETtreescomparedallnon-treeleafmode/type/SHA:onlyglobalchangelog/T3096 differ,whole4dtreeNOTIDENTICALexplicit. H8actualFull4666158budgetFAIL/stage14HOLD remain separate,NOTmergeapproval/newcandidatePASS;GET/read-onlyonly,noretry/POST/source/browserchanges. Activeshadowtestexcluded.'),('/workspace/T3081-own-lap-f83-expiry-guard/closed-final-receipt','MANIFEST.json','00cbf089bdeb602f15d892c39b51782a40e0741b0141646d1c496f4a3c9b3df7',8,30098,'PR1260-ownf83-EXPIRED-one-normal-CAS-1d653-FINAL-RECEIPT','Exact8 closed final operationalclaim payloads plus original manifest. Positive nativeSTALE10:48:37thenONEnormalCASexit0,new1d65324087b2e918fe94fc5580dbade40d721ed6created10:48:38/expiry13:48:38UTC. Independentref/owner/date/emptytree/HELDexit3/PRopen,primary35f0HEAD/index/cf3toolunchanged. Correctnewprimarypath,no oldforttmpaccess,guardexited. Noforce/release/manualtime/retry/stage14POST;datedoperationalproofonly/futureownershipfreshreadrequired,no source/CI/mergeapproval byarchivist.')]
for directory,filename,expected,count,total,name,note in packets:
 root=Path(directory);manifest=root/filename;assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
 author=json.loads(manifest.read_text());rows=author.get('files',author) if isinstance(author,dict) else author
 if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
 assert len(rows)==count and sum(r['bytes'] for r in rows)==total
 entries=[]
 for row in rows:
  p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','node-compile-cache','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'];entries.append((p,row['path'],row['sha256']))
 entries.append((manifest,filename,expected))
 if 'H8-actual-CI-closed' in directory:
  ziprows=[]
  for phase in ['gate','humans','moving-frames']:
   zp=root/phase/'run-logs.zip';raw=(root/phase/'job.log.raw').read_bytes()
   with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    whole=[i for i in z.infolist() if '/' not in i.filename and not i.is_dir()];assert len(whole)==1 and z.read(whole[0])==raw
    for i in z.infolist():
     p=Path(i.filename);assert not p.is_absolute() and '..' not in p.parts and not stat.S_ISLNK(i.external_attr>>16);data=z.read(i);ziprows.append({'phase':phase,'path':i.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
  head='35f0c564cc25303d3f5641812d532dd9d2166b64';actual='07058209d81b91ec19a9d871a0f9ca0c83079c9c'
  trees=[]
  for commit in [head,actual]:
   d=json.loads(gzip.decompress((root/(commit+'-TREE.json.gz')).read_bytes()));assert d.get('truncated') is False;trees.append({r['path']:(r['mode'],r['type'],r['sha']) for r in d['tree'] if r['type']!='tree'})
  diffs=sorted(k for k in set(trees[0])|set(trees[1]) if trees[0].get(k)!=trees[1].get(k));assert diffs==['chicago/4d/changelog.d/T-3096.json','chicago/4d/renderers/web/js/changelog.js']
  commit=json.loads((root/(actual+'-COMMIT.json')).read_text());assert [r['sha'] for r in commit['parents']]==['c96846f15ba1dec54530f8056a347695616f38e9',head]
  ledger=WORK/'H8-CI-ZIP-TREE-READBACK.json';ledger.write_text(json.dumps({'status':'PASS_ALL_ZIP_CRC_HASH_RAWWHOLEJOB_EQUAL_AND_NON_TREE_LEAVES','declared_head':head,'actual_checkout':actual,'actual_parents':[r['sha'] for r in commit['parents']],'non_tree_leaf_counts':[len(t) for t in trees],'changed_only_paths':diffs,'whole4d_tree_equal':False,'zip_members':ziprows},indent=2)+'\n');entries.append((ledger,'H8-CI-ZIP-TREE-READBACK.json',hashlib.sha256(ledger.read_bytes()).hexdigest()))
 mod.archive(name,entries,note)
