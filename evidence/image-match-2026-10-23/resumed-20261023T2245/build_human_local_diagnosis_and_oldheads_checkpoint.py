from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-human-reproduction-da65119');manifest=root/'MANIFEST.json'
expected='99a0f6102eba5593b7eb3da4a6cec8de2fc2e073e2439d129e05de02e0f0dce1';assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
rows=json.loads(manifest.read_text())['files'];assert len(rows)==1259 and sum(r['bytes'] for r in rows)==11535978
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['node_modules','.git','__pycache__'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
excluded=[r for r in rows if 'node-compile-cache' in Path(r['path']).parts];assert len(excluded)==1146 and sum(r['bytes'] for r in excluded)==2992992
ledger=WORK/'HUMAN-DIAGNOSIS-CACHE-SELECTION.json';ledger.write_text(json.dumps({'status':'ALL1259_AUTHOR_HASHES_VERIFIED_113_NONCACHE_PAYLOADS_ARCHIVED','original_manifest_sha256':expected,'policy':'Generated cache files omitted under established evidence policy; original manifest preserved verbatim and all actual blends/raw LOD/output sets/input shadow/CI logs retained.','excluded_cache_files':excluded,'excluded_bytes':2992992},indent=2)+'\n')
entries=[e for e in mod.author_manifest(root,manifest) if 'node-compile-cache' not in Path(e[1]).parts];entries.append((ledger,'HUMAN-DIAGNOSIS-CACHE-SELECTION.json',hashlib.sha256(ledger.read_bytes()).hexdigest()))
mod.archive('PR1260-human-local-ACTUAL-two-FAIL8of8-JSON-socket-diagnosis-NO-FIX',entries,'All1259authorhashesverified;113exactnoncachepayloads plus verbatimauthormanifest/cacheexclusionledger.1146generatedNodecompilecachefilesomitted. UnchangedpinnedBlender/gltfverifytwicered8of8,contract8PASSSEPARATE. Rebuildsetsrepeatbyteexact/committedBINall8exact,JSONonlytwohand-socketquats/eightscalars+4Bfile. Actualblends/rawLOD/eightoutputsets/original4.88MBGitblobshadow/CIlog/68exactinputsretained. Minimal9pathremedyUNAPPLIED/realbrowser8measureUNRUN;no source/assertion/fixture/measurement/CI/PR edits. LocalNode24vsCI22disclosed/exactCIgeneratedbytesnotpreserved/no baseline85CIverdict;NOenvironmentalorbaselinecause/waiver. OriginalgoldenFAILremainsFAILuntilactualfix.')
root=Path('/tmp/PR1260-head-da65119-watch/humans-older-public-heads/closed-older-public-comparison');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='0508139e7d56d5949e0e5f06a1725258398e35c91e9ddbf0fcfdf9c0075dab21'
rows=json.loads(manifest.read_text())['files'];assert len(rows)==6 and sum(r['bytes'] for r in rows)==251042
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['node_modules','.git','__pycache__','node-compile-cache'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-older-public-human-check-NO-RESULT-source-guards-ONLY',mod.author_manifest(root,manifest),'Exact6 closed olderpubliccomparisonpayloads plus manifest. Public5d9d4464/6024f073/9f95f8eecomplete27/6/7checkrunscontainNOhumansresult,NOearlierOS/verifyPASSinference.72humancommittedpathsexacteacholdheadtoda65119. SourceguardONLY,nobaseline/environmentalconclusion/fixture refresh/rerun/writer/waiver. Currentd0e63actualhumansFAILseparate,pinnedlocaldiagnosisrednotCIbyteequivalence. No livejobs/source/mutations orapproval.')
