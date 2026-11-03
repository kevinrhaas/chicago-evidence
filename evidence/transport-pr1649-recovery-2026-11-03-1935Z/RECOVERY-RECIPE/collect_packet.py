from pathlib import Path
import json,shutil,hashlib,datetime
D=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence/transport-pr1649-recovery-2026-11-03-1935Z');R=Path('/workspace/.cloud-setup/transport-current-20261103');B=Path('/workspace/.cloud-setup/transport-recovery-20261103/bounds-proposal')
origins=[]
def cp(p,rel):
 q=D/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);origins.append(dict(path=rel,original=str(p),sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
for name in ['RESTORED-RUNTIME-BASELINE.json','resource_guard.py','run_fourpart_preflight.py','FOURPART-HELPER-PREPARED.json','run_mobile_memory.py','run_steps.py','MERGED-073-BEFORE-BOUNDS.json','normal-dev-merge.log','lap-take.log','renew-T3088.log','tickets-setup.log']:
 cp(R/name,'RUNTIME-AND-INTEGRATION/'+name)
cp(Path('/workspace/.cloud-setup/transport-supervise.py'),'RUNTIME-AND-INTEGRATION/transport-supervise.py')
for name in ['derived-owners-073','native-mayer-repair-073','adopted-bounds-controls']:
 for p in sorted((R/name).rglob('*')):
  if p.is_file():cp(p,'ACTUAL-CLOSED-CONTROLS/'+name+'/'+str(p.relative_to(R/name)))
for p in sorted(B.rglob('*')):
 if p.is_file():cp(p,'BOUNDS-PROPOSAL/'+str(p.relative_to(B)))
cp(R/'periodic-evidence/capture_immutable.py','RECOVERY-RECIPE/capture_immutable.py')
(D/'COPY-ORIGINS.json').write_text(json.dumps(origins,indent=2)+'\n')
print('copied',len(origins),'records')
