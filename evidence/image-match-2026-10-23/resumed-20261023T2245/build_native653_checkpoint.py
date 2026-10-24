from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/T3081-native653-checkpoint-20261024T0015');manifest=root/'MANIFEST.json'
expected='72e6b2097913e7ce6ecdffc17a89df63c0a561ad6d1fb62d5b1f3a16520776f9'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
author=json.loads(manifest.read_text());assert len(author['files'])==138
assert sum(r['bytes'] for r in author['files'].values())==33974577
for rel,row in author['files'].items():
    path=root/rel
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],path
ledger=WORK/'NATIVE653-SELECTION.json'
ledger.write_text(json.dumps({'status':'ALL_138_AUTHOR_FILES_VERIFIED;137_NONINDEX_PAYLOADS_ARCHIVED','author_manifest_sha256':expected,'excluded':[{'path':'index-bytes',**author['files']['index-bytes'],'reason':'Private Git index excluded by established archive policy; root explicitly confirmed exclusion. Staged/index and full binary patches retained; original author manifest preserved verbatim.'}],'all_other_manifest_files_selected':True},indent=2)+'\n')
entries=mod.author_manifest(root,manifest)
entries=[e for e in entries if e[1]!='index-bytes']
entries.append((ledger,'NATIVE653-SELECTION.json',hashlib.sha256(ledger.read_bytes()).hexdigest()))
assert len(entries)==139
mod.archive('T3081-native653-converged55step-and-root-recovery-PREFLIGHT-CANCELLED',entries,'All138 frozen author payloads verified; exact137 non-index payloads plus verbatim manifest and explicit private-index exclusion ledger archived. Root recovery includes tracked/untracked deltas, binary/full and index patches, late exact-phase side-consumer fix and actual graft/native receipts. Actual55-step converged tail:653 doors,0 obstructions,all3clearances; all82 fresh input/Hogan/22cards/ledger/orderbook guards exact. Full preflight was CANCELLED_NOT_PASS; no current whole-gate/browser/readiness/image-match approval. No live tree selected; copied private Git index remains local only by explicit root-confirmed policy.')
