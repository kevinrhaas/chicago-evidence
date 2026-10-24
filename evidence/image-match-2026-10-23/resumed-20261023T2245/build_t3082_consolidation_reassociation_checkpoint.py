from pathlib import Path
import hashlib,importlib.util,json
WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('archive_exact',WORK/'archive_exact.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
root=Path('/workspace/T3082-consolidation-reassociation-20261024');manifest=root/'CLOSED-MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='f31267a2fe0fbfdfc835e028138ea8bf8bc8acfa5adb6cfb461a6c1011389d20'
author=json.loads(manifest.read_text());rows=author['files'];assert len(rows)==7 and sum(r['bytes'] for r in rows)==11661
for row in rows:
 p=root/row['path'];assert p.resolve().is_relative_to(root) and p.is_file() and not p.is_symlink();assert not any(part in ['__pycache__','node_modules','.git'] for part in p.parts) and p.suffix!='.pyc';data=p.read_bytes();assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
mod.archive('T3082-normal-ticket-PR-reassociation1273to1260-ROOT-CONSOLIDATION-PENDING',mod.author_manifest(root,manifest),'Exact7 closed LIGHT normalticketreassociationpayloads plus manifest. Rootplanned9f95consolidationinto1260,T3082REVIEWPR1273to1260by normaldone; ticketscommit12c36d47b152eda4fb71cb0c7202131c30416df7independentcontents/remoteancestryPASS. Exactlyonefrontmatterfieldchanged,allbody/state/claimexact. PR1273stillOPENDRAFT/ownlivelapretained;noforce/manualclose/matrix/sourcechanges. Consolidatedsource/native/gatesrootownedPENDING,originalT2385openDIFFERS,noreadiness/merge/imageacceptance.')
