from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/PR1260-readonly-watch/closed-dev8e5a-dependency-review');manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='253a09a1168ac56aeef0e7a1050d9cb30139cafd01a68beca605f2e34e60d10d'
author=json.loads(manifest.read_text());assert len(author['files'])==6 and sum(r['bytes'] for r in author['files'])==318717
for row in author['files']:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('PR1260-dev8e5a-bounded-dependency-review-NOT-FRESH-BAKE',mod.author_manifest(root,manifest),'Exact6 closed dependency-review files plus manifest.377guards026ace-to8e5a:374exact,onlyK01frontage/params andchangelog differ; entirecommon/emit/mesh_inputs/frame/log/renderer/smoke/targetsources unchanged. Recipecontractsource retained,K01outside82log/23frameinputs. This is bounded source dependency proof,NOTfreshrecipes/bake/gate. Final sharedrows/history reconciliation still required, outsideheightdiagnostic/wordingcode unaffected. No canonical changes/heavy/job/merge/lap mutation or readiness/image-match approval.')
