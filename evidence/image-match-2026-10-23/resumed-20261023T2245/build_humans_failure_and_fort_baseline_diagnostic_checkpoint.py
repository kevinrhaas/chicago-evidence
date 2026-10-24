from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packets=[('/tmp/PR1260-head-da65119-watch/non-summary-checks/closed-humans-reproduction-failure','d0e63e2bc4c2b25f0fa90314b79104b4579aac75b14a88630842174ba0b2259b',6,83354,'PR1260-da65119-ADDITIONAL-human-reproduction-ACTUAL-FAIL','Exact6 closed additionalhumanscheckfailurepayloads plus manifest. Exactda65119/merge4e877run40074598625job120815159950,eightfixtureGLBscontractOKthenall8master/weboutputsDIFFERSexit1.72humanpathGitblobguardsexactbase85toda;base85NOhumanscheckresult,NOenvironmental/baselineCIconclusion. No nativeexport/writer/retry/waiverbyreviewer/archivist. Distinctfromgate1063/383-movingPASS/staged17of18PASSdesktop13pending,additionalFAILexplicit,nofinalapproval/currentdevinheritance.'),('/workspace/T3105-baseline-da65119-diagnostic-20261024','2d0fe455cb84ccd5b594132788a6321701c95a28c984559a48f4571e027629d1',24,3535447,'T3105-clean-public-da65119-ACTUAL-baseline-diagnostic-FAIL-FLORA-ABORT','Exact24 closed externalreadonlybaseline diagnosticpayloads plus manifest. Actualcleanpublicda65119nativepublish+ONEmobile1812northrangebrowserreproduceelevenoriginalhardfloraproblemsandpeople.jsonERR_ABORTED;bothFAILreceiptsseparatelyretained. DIAGNOSIS/nativepolicyhash-excerpts/actualscreenshot/input/helperbindingspreserved. Nocodefix/waiver/acceptanceimplication;heavyCLEAR,nocanonical/liveforttreeorQAselection. Distinctdiagnosticbaseline,notpassinggate/imageacceptance.')]
for directory,expected,count,total,name,note in packets:
 root=Path(directory);manifest=root/'MANIFEST.json';assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
 author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==count
 if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
 assert sum(r['bytes'] for r in rows)==total
 for row in rows:
  p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 mod.archive(name,mod.author_manifest(root,manifest),note)
