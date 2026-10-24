from pathlib import Path
import hashlib, importlib.util, json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
packages=[
('/tmp/log82-reviewed-liberties-kimball-graft-20261024T0010','8d57e767e4fc253413636f852d05019d63f7c09328079893f1c1e034b4356b1e',33,18572070,'T3081-Kimball-bound-LIBERTIES-graft-helper-NOT-APPLIED','Exact33 closed LIGHT files plus manifest. Staging-only reviewed3fa6/PR1256 LIBERTIES formula preserves entire a219 history plus2849B Glessner and2331B Kimball appends before own12.29 formula/refusal checks, zero-conflict clean-parent18-file preview and source-proof receipts. NOT_APPLIED at capture; actual root merged target needs fresh guards, late exact-phase consumer/STATUS correction and official82 outputs separately restored from verified bindings. No canonical write, native/heavy/browser/fullgate or adoption.'),
('/tmp/log82-wolf-site-audit-20261023T2358','d0833ab85ac77b0ef02cdbbf7b85cf5e3c8a157b9018a70a5f905a0be182c632',81,10326854,'T3081-WOLF-fixed653-readonly-site-audit-NO-HISTORICAL-SETBACK','Exact81 closed read-only LIGHT files plus manifest. Fixed653 native snapshot binds70 exact source/input files, actual55-step converged tail and replay proof. Concave occupied body, both entry aprons/clearances, river polygons, sampled raw ground and3515 native object points/segments measured; no intrusions in measured body/door zones, old four coordinates absent. Exact-phase consumer resolves both Wolf entries; historical omission retained separately. Model distances only, not historical setbacks/mesh contact/object radii or future-parent gate. No canonical changes/native writer/heavy/browser/fullgate.')]
for directory,expected,count,total,name,note in packages:
    root=Path(directory);manifest=root/'MANIFEST.json'
    assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
    author=json.loads(manifest.read_text());assert len(author['files'])==count
    assert sum(r['bytes'] for r in author['files'])==total
    for row in author['files']:
        path=root/row['path']
        assert path.resolve().is_relative_to(root) and path.is_file() and not path.is_symlink()
        assert not any(part in ['__pycache__','node_modules','.git'] for part in path.parts)
        assert path.suffix!='.pyc'
        data=path.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    mod.archive(name,mod.author_manifest(root,manifest),note)
