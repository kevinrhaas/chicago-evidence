from pathlib import Path
import shutil,json,hashlib,gzip
R=Path('/workspace/.cloud-setup/transport-current-20261103');B=Path('/workspace/.cloud-setup/transport-recovery-20261103');D=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence/transport-pr1649-final-memory-and-driver-prep-2026-11-03-2020Z');V=Path('/workspace/.cloud-setup/transport-driver-motion-20261103');W=Path('/workspace/chicago-driver-motion-20261103');origins=[]
def cp(p,rel,force_gzip=False):
 b=p.read_bytes();compressed=force_gzip or len(b)>512*1024;q=D/(rel+'.gz' if compressed else rel);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(gzip.compress(b,mtime=0) if compressed else b);origins.append(dict(path=str(q.relative_to(D)),original=str(p),original_bytes=len(b),original_sha256=hashlib.sha256(b).hexdigest(),lossless_gzip=compressed,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
for n in ['DEV92-FINAL-SOURCE-BEFORE-FULL-GATE.json','DEV92-COLUMN-ASSET-DELTA.json','DEV92-RESTORED-CUSTOM-SOURCE-PREP.json','DENSITY-PREFIX-ADOPTION.json','normal-dev-92-merge.log','REVIEWABLE-COMMIT-MESSAGE.txt','run_mobile_pair.py','run_fourpart_preflight.py','RESTORED-RUNTIME-BASELINE.json','RUNTIME-EPOCH-METADATA-ERRATUM.json','resource_guard.py']:
 cp(R/n,'ROOT-SOURCE-AND-RUNTIME/'+n)
cp(R/'BEFORE-92-SAVED-SOURCE/MANIFEST.json','INTERMEDIATE-5EDE-SOURCE/MANIFEST.json');cp(R/'BEFORE-92-SAVED-SOURCE/TREE-ENTRIES.z','INTERMEDIATE-5EDE-SOURCE/TREE-ENTRIES.z',True)
for n in ['actual-final-mobile-pair-01','dev92-native-owners']:
 for p in sorted((R/n).rglob('*')):
  if p.is_file():cp(p,'ACTUAL-CLOSED-RESULTS/'+n+'/'+str(p.relative_to(R/n)))
for p in sorted((B/'rail-density-prefix-proposal-v3-current-phases').rglob('*')):
 if p.is_file() and 'overlay' not in p.relative_to(B/'rail-density-prefix-proposal-v3-current-phases').parts:cp(p,'EXACT-DENSITY-PREFIX/'+str(p.relative_to(B/'rail-density-prefix-proposal-v3-current-phases')))
# Preserve code/proofs, not the41MB generated models or dependency installs.
for p in sorted(V.iterdir()):
 if p.is_file():cp(p,'DRIVER-UNADOPTED/'+p.name)
for n in ['generated','native-01','native-02','fixture-01','owners-01','owners-02','writer-instrumented','writer-measured-repeat']:
 for p in sorted((V/n).rglob('*')):
  if p.is_file() and p.suffix not in ['.glb','.pyc','.node']:cp(p,'DRIVER-UNADOPTED/'+n+'/'+str(p.relative_to(V/n)))
for rel in ['chicago/4d/tools/human_seated_look.py','chicago/4d/tools/human_natural_idle.py','chicago/4d/data/humans/animations/seated-driver-look-v2.json','chicago/4d/data/humans/animations/seated-driver-look-v2.binding-refresh.json','chicago/4d/data/humans/animations/seated-driver-look-v2.derivation.json','chicago/4d/data/humans/animations/seated-driver-look-v2.native.json']:
 cp(W/rel,'DRIVER-UNADOPTED/EXACT-PRODUCER-AND-RECIPES/'+rel)
cp(R/'periodic-evidence-final-prep/capture_immutable.py','RECOVERY-RECIPE/capture_immutable.py');cp(R/'periodic-evidence-final-prep/collect_packet.py','RECOVERY-RECIPE/collect_packet.py')
(D/'COPY-ORIGINS.json').write_text(json.dumps(origins,indent=2)+'\n');print('copied',len(origins),'records')
