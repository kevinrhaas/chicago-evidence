from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packets=[('/workspace/T3081-T3082-preflight06-dev85-closed','e1623d2df6254306fc96cd7659afe480d2067cddb8a322cf773ffe6c1990dcf8',34,7616252,'T3081-T3082-CONSOLIDATED-publicda65119-FULLGATE1063-PASS-SMOKES-PENDING','Exact34 closed consolidatedpublicmilestonepayloads plus manifest. Finalcommitted/pushedda65119e52d6bb615bcdd72ef6dd14230e30414etreed2ec7070e0cc8e59e3f21ffab76740d42c163d0fbyteexactfullpreflight1063/383scientificreadersrequired. Native9PASS/105fresh210assetsexact/13LIBsuffix+incoming85rawprefixpreserved;wholeownpatchagainstpublicdev85/postcommitchecks retained. PR1260includesTremont9f95+root5,T3082associated1260,1273supersessionpendingatcapture. Finalnew18smokesDISPATCHING/NOTRESULTS,oldH4/H5historical,nofinalcurrentsmokegate/imageacceptance. Allsourcefrozen/public,nolivejobharvesting.'),('/tmp/PR1260-H5-replacements-watch/closed-both-H5-replacements-and-gate','e80ba7959532075f678d1c4a19df700754e0ef1494a8144c6fdc0b26133bd5c5',11,2001766,'PR1260-H5-BOTH-replacements194-PASS-hosted1062-HISTORICAL','Exact11 closed actualH5replacement/gatepayloads plus manifest. Desktop/mobile1-2each194PASS0FAIL/exactH5checkout/zeropageerrors,H4-H5whole4dtreebc25faexact. OldfailedattemptsNEVERrelabeled. H5gate1062/383PASSmergebinding262bc8592d85b0f8401943ba42d5ac254638f614=H5+29ea. H5separatemovingframessetupFAIL/automaticwholepending retained;H4desktop13stillpendingatcapture. Historicalnotfullcoverage/currentconsolidatedheadapproval,no mutations/liveoutputsselected.')]
for directory,expected,count,total,name,note in packets:
 root=Path(directory);manifest=root/'MANIFEST.json';assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
 author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==count
 if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
 assert sum(r['bytes'] for r in rows)==total
 for row in rows:
  p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 mod.archive(name,mod.author_manifest(root,manifest),note)
