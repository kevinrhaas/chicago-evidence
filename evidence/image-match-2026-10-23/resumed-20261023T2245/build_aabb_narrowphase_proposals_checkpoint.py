from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packets=[('/tmp/PR1260-aabb-narrowphase-proposal-school-20261024','f955b4248b0f349d3bee7f5c83ac943830b4edc5752ccaf4b5147b48006ddf07',14,122666,'PR1260-AABB-narrowphase-v1-PROPOSAL-UNAPPLIED-SCOPE-GAPS','Exact14 closed original AABBproposal files plus manifest. UNAPPLIED CPUonlyknownFullrigidopaquebatches,twoauthoredpaths;44actualThree smallcontrols/read-onlyguard/isolatedoverlayPASS. RootlaterfoundFullscope/arrayguardgaps,retainedasv1timepoint;twodraftCPUfixturefailurelogs preserved. Existingc297A/Bunchanged,real1782overshoot unresolved. No actualbrowser/savings/fullstage/fullgate orcanonicaladoption.'),('/tmp/PR1260-aabb-narrowphase-proposal-v2-school-20261024','981e4e55285ca9c1963cf640a94a1e378a90bea472e198dd3d520760fed14a5a',18,171844,'PR1260-AABB-narrowphase-v2-PROPOSAL-UNAPPLIED-47CPU','Exact18 closed corrected AABBv2proposal files plus manifest,v1immutable. ConcretefixesexactFullpreserveMaterials&&spatialCellsnull plusposition/indexarrayidentity/typeguards.47CPU andunchangednativesidecar temporaryfullrendereroverlaypositive/rednegativePASS,novalidatorallowance;existingcoalescerunchanged. v1-v2patch/originalmanifestref retained. UNAPPLIEDatcapture,noactualbrowser/current saving/fullstage/fullgate;rootgrantedfutureexclusiveA/Bseparate/liveexcluded.')]
for directory,expected,count,total,name,note in packets:
 root=Path(directory);manifest=root/'MANIFEST.json';assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
 author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==count
 if isinstance(rows,dict):rows=[{'path':k,**v} for k,v in rows.items()]
 assert sum(r['bytes'] for r in rows)==total
 for row in rows:
  p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 mod.archive(name,mod.author_manifest(root,manifest),note)
