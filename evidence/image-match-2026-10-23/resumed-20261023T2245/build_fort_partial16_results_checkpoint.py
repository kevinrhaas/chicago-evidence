from pathlib import Path
import hashlib,importlib.util,json
W=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('archive_exact',W/'archive_exact.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
r=Path('/tmp/PR1282-head308b-full18-watch/closed-partial16-actual-PASS');p=r/'MANIFEST.json';assert hashlib.sha256(p.read_bytes()).hexdigest()=='9ded34afef9a3700b9530ac911f9967f5d26b9998ea1c9c4bec80a5addf2b0cf';rows=json.loads(p.read_text())['files'];assert len(rows)==37 and sum(x['bytes'] for x in rows)==1119162
for x in rows:
 q=r/x['path'];assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink();b=q.read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
m.archive('PR1282-EXACT308b-ACTUAL-PARTIAL16-ALLMOBILE-PASS-DESKTOP13-14-PENDING',m.author_manifest(r,p),'Exact37closedpayloads+manifest sixteenrawexact308bPASS/fullnativefooters/env+checkout/zeroerrors. ALLmobilecomplete;desktop13+14pending16:10:50,NOcurrentFullbudget/full18/merge/PictureMatchinference. NewdevcbfHoganmergeSEPARATEfromoriginalhostedgate04bc/de91,parentownslaterbaseparity;no oldHoganPASSinheritance/sourceCIaction/liveobserverinspection.')
p=W/'write_index.py';s=p.read_text();needle='- Further producer/integration work is ongoing.';assert s.count(needle)==1
addition='- FortPR1282partial16 preserves37closedpayloads plus originalmanifest, sixteenactualexact308brawPASS with complete nativefooters/env+checkout and zeroerrors. Allmobilegroups finish; **desktop13and14remainpending16:10:50**, no currentFullbudget/full18/merge/PictureMatchinference. NewdevcbfHoganmerge is separate from priorhostedgate04bc/de91; root owns laterbaseparity and oldHoganresults are not borrowed. No source/CIaction or liveobserverinspection occurs.\n'
s=s.replace(needle,addition+needle);old='The latest closed staged-smoke snapshot has fourteen passes and four running at15:55:50';assert old in s;s=s.replace(old,'The latest closed staged-smoke snapshot has sixteen passes, allmobilecomplete, with desktop13and14pending at16:10:50')
p.write_text(s)
