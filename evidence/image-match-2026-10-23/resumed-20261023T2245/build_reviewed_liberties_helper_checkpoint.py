from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/tmp/log82-reviewed-liberties-graft-20261023T2350')
manifest=root/'MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='18fcbeb3c2b3b6c219b2dfe1a8e78c860d6f04ac8954d75a8c7ed2cd583a87b9'
author=json.loads(manifest.read_text());assert len(author['files'])==29
assert sum(r['bytes'] for r in author['files'])==12682557
for row in author['files']:
    path=root/row['path']
    assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
    assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
    assert path.suffix!='.pyc'
    data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3081-single-reviewed-LIBERTIES-exception-helper-NOT-APPLIED-AT-CAPTURE',mod.author_manifest(root,manifest),'Exact29 closed helper files plus manifest. Frozen stage-only single reviewed LIBERTIES exception: incoming d872 hash must equal entire a219 raw LIBERTIES prefix plus exact2849B e5 Glessner suffix, then preserve incoming bytes and append only own12 records. Original general helper unchanged. Packet status NOT_APPLIED at capture; later root actual canonical graft/native receipts belong to a separate closed packet. No canonical writes, native/browser/fullgate or approval in this helper packet.')
