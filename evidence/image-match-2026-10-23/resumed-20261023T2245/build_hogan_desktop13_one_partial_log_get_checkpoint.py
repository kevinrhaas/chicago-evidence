from pathlib import Path
import hashlib,importlib.util,json
W=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('archive_exact',W/'archive_exact.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
r=Path('/tmp/PR1283-head6e6619-full18-watch/running-desktop13-single-log-attempt');p=r/'MANIFEST.json';assert hashlib.sha256(p.read_bytes()).hexdigest()=='aebd7f2004661a3e754c70b3c449d1edee083560871788c6c36a5e1b495d2cd5';rows=json.loads(p.read_text())['files'];assert len(rows)==4 and sum(x['bytes'] for x in rows)==1131
for x in rows:
 q=r/x['path'];assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink();b=q.read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
m.archive('PR1283-DESKTOP13-ONE-AUTHORIZED-RUNNING-LOG-GET404-NOT-CI-FAIL',m.author_manifest(r,p),'Exact4closedpayloads+manifest parentauthorizedONErunningjobpartial-logGET job120889138279/logs returns404/exit1at15:22. UNAVAILABLEnotCIFAIL/progress/result;NOretrybeforeterminal/noCImutation. SeventeenprioractualPASSremainseparate,desktop13stillpendingatcapture. No livewatcher/canonicalchanges or inferredcoverage.')
p=W/'write_index.py';s=p.read_text();needle='- Further producer/integration work is ongoing.';assert s.count(needle)==1
addition='- A tinyfour-file operational receipt plus manifest preserves one explicitlyparent-authorized partial-logGET for runningPR1283desktop13job120889138279at15:22. The endpoint returns404/exit1: **UNAVAILABLE, not CItestfailure/progress/result**. No retry beforeterminal, dispatch/cancel/source/CI mutation occurs;17prioractualPASSremainseparate and desktop13is stillpending at capture. No livewatcher output is selected.\n'
s=s.replace(needle,addition+needle);p.write_text(s)
