from pathlib import Path
import hashlib,importlib.util,json
W=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('archive_exact',W/'archive_exact.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
r=Path('/tmp/PR1282-head308b-full18-watch/closed-started-bound18-noresults');p=r/'MANIFEST.json';assert hashlib.sha256(p.read_bytes()).hexdigest()=='12732a1d2d6d23d715035aa53175d4b402828a5bf2ce2cc5fc43e99dfcda9119';rows=json.loads(p.read_text())['files'];assert len(rows)==8 and sum(x['bytes'] for x in rows)==76011
for x in rows:
 q=r/x['path'];assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink();b=q.read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
m.archive('PR1282-308b-FULL18-GETONLY-OBSERVER-STARTED-BOUND-ZERO-RESULTS',m.author_manifest(r,p),'Exact8closedpayloads+manifest startedseparateobserver/public308b738e6e6716a7a1411aa6c178e196eb17a719/all18rootacceptedheadbound. Initial13running5queued/ZEROactualresults/noPASSinference. ExistingGETonlyPID1812700/300snotduplicated;separatePR1283observer17PASS/lastdesktop13pending. No liveobserverinspection/start/CIactions/mutation or oldPASSinheritance byarchivist.')
p=W/'write_index.py';s=p.read_text();old='[1229, 1239, 1256, 1260, 1273]';assert s.count(old)==2;s=s.replace(old,'[1229, 1239, 1256, 1260, 1273, 1282, 1283]')
needle='- School T-2372:';assert s.count(needle)==1
anchors="- [PR1282](https://github.com/kevinrhaas/chicago/pull/1282): state `{prs[1282]['state']}`, draft={str(prs[1282]['draft']).lower()}, head `{prs[1282]['head']['sha']}`. Fortbeamrepair plus scopedflora utilities, exact308bsource/native/localQA/fullgate proof below; accepted18hosteddispatches are not results or originalpictureacceptance.\n- [PR1283](https://github.com/kevinrhaas/chicago/pull/1283): state `{prs[1283]['state']}`, draft={str(prs[1283]['draft']).lower()}, head `{prs[1283]['head']['sha']}`. Hoganpictured-detail utility, exact6esource/localgate/actualQA plus separately bound hostedresults below; pendingcoverage/merge are not inferred from metadata.\n"
s=s.replace(needle,anchors+needle)
end='- Further producer/integration work is ongoing.';assert s.count(end)==1
addition='- PR1282separateobserverstart preserves eight closedpayloads plus manifest, exact308b738eall18rootaccepted/headbound. Initial13running/5queued/**ZEROactualresults**; GET-onlyPID1812700/300scadence remains unduplicated and its liveoutput is excluded. PR1283observer remains separate17PASS/desktop13pending at capture. No observerstart/inspection/CIaction byarchivist and no oldresultinheritance or newPASSinference. ActivePR1282/1283dated read-onlymetadataanchors are added above without mutation or approval.\n'
s=s.replace(end,addition+end);s=s.replace('Roothosted18runs on frozen308bare still pending at capture;','Roothosted18runs on frozen308bare accepted/headbound in a separateobserverstart snapshot (13running/5queued/ZEROactualresults);')
p.write_text(s)
