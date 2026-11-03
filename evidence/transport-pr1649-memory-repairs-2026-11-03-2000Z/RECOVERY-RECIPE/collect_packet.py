from pathlib import Path
import shutil,json,hashlib
R=Path('/workspace/.cloud-setup/transport-current-20261103');B=Path('/workspace/.cloud-setup/transport-recovery-20261103');D=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence/transport-pr1649-memory-repairs-2026-11-03-2000Z');origins=[]
def cp(p,rel):
 q=D/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);origins.append(dict(path=rel,original=str(p),sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
for n in ['PLANAR-ADOPTION.json','TREE-SCRATCH-ADOPTION.json','RAIL-WORD-CACHE-ADOPTION.json','RUNTIME-EPOCH-METADATA-ERRATUM.json','CURRENT.md','RESTORED-RUNTIME-BASELINE.json','resource_guard.py','run_mobile_memory.py','run_steps.py']:
 cp(R/n,'ROOT-ADOPTIONS-AND-RUNTIME/'+n)
for n in ['adopted-planar-controls','actual-073-bounds-1904-retainers','actual-073-planar-1812-mobile','actual-073-planar-1812-retainers','actual-073-tree-scratch-1812-mobile']:
 for p in sorted((R/n).rglob('*')):
  if p.is_file():cp(p,'ACTUAL-CLOSED-RESULTS/'+n+'/'+str(p.relative_to(R/n)))
for n in ['planar-prefix-proposal','tree-flood-scratch-proposal']:
 for p in sorted((B/n).rglob('*')):
  if p.is_file():cp(p,'EXTERNAL-PROPOSALS/'+n+'/'+str(p.relative_to(B/n)))
rail=Path('/workspace/.cloud-setup/transport-rail-cache-proposal-20261103')
for p in sorted(rail.rglob('*')):
 if p.is_file():cp(p,'EXTERNAL-PROPOSALS/rail-cache-proposal/'+str(p.relative_to(rail)))
cp(R/'periodic-evidence-memory/capture_immutable.py','RECOVERY-RECIPE/capture_immutable.py');cp(R/'periodic-evidence-memory/collect_packet.py','RECOVERY-RECIPE/collect_packet.py')
(D/'COPY-ORIGINS.json').write_text(json.dumps(origins,indent=2)+'\n');print('copied',len(origins),'records')
