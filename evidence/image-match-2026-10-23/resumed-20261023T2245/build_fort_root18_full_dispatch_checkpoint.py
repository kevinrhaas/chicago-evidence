from pathlib import Path
import hashlib,importlib.util,json
W=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('archive_exact',W/'archive_exact.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
r=Path('/workspace/PR1282-head308b-full18-dispatch-20261024');p=r/'MANIFEST.json';assert hashlib.sha256(p.read_bytes()).hexdigest()=='b256ca8e7bb5032489f427429fadbcc6ba064e5894dfd258f59390b6cfdb78da';rows=json.loads(p.read_text())['files'];assert len(rows)==22
for x in rows:
 q=r/x['path'];assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink();b=q.read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
m.archive('PR1282-ROOT-FULL18-EXACT308b-DISPATCH-ACCEPTED-NOT-RESULTS',m.author_manifest(r,p),'Exact22closedpayloads+manifest rootall18dispatchpayloads/controller/fullsourcecommit/BOUND. All18accepteduniqueIDs/actual308b738e6e6716a7a1411aa6c178e196eb17a719/tree4cc2f87e5809f849406ca262cfdee17e3a46d10a verifiedAPI,coverage1-15onceeachviewport. NOTRESULTS;upstreamHogan6ependingdependencyexplicit. ExistingobserverPID1812700elsewhereuntouched,liveT2388trial/unclosedcheckoutrecordsEXCLUDED,no outcome/adoption/CI/sourceaction byarchivist.')
p=W/'write_index.py';s=p.read_text();needle='- Further producer/integration work is ongoing.';assert s.count(needle)==1
addition='- Rootfullfort18dispatch receipt preserves22closedpayloads plus originalmanifest: all18payloads/controller/fullsourcecommit/BOUND, each acceptedunique and independently API-bound exact308b738e/tree4cc2f87e. Coverage tiles1–15once across eachviewport, **DISPATCHED NOT RESULTS**, with upstreamHogan6edependency explicitlypending. The existing separateobserverPID1812700 is untouched; live second-fortresearchtrial and unclosedcheckoutrecords are not selected, and no actualoutcome/adoption/CIaction follows from this dispatch receipt.\n'
s=s.replace(needle,addition+needle);p.write_text(s)
