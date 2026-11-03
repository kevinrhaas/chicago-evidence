from pathlib import Path
import json,hashlib,datetime,shutil
R=Path('/workspace/.cloud-setup/transport-current-20261103');V=Path('/workspace/.cloud-setup/transport-driver-motion-20261103');D=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence/transport-pr1649-world-and-ci-progress-2026-11-03-2125Z');orig=json.loads((D/'COPY-ORIGINS.json').read_text())
def cp(p,rel):
 b=p.read_bytes();q=D/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);orig.append(dict(path=rel,original=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
for n in ['T2804-FRESH-REMOTE-BEFORE-RENEW.json','T2804-NATIVE-RENEW.log','T2804-REMOTE-AFTER-NATIVE-RENEW.json']:cp(R/n,'T2804-OWN-NATIVE-RENEWAL/'+n)
p=V/'NEXT-INCREMENT-INTEGRATION-PREPARED.json';j=json.loads(p.read_text());assert j['status']=='NEXT_INCREMENT_INTEGRATION_PREPARED_NOT_APPLIED';cp(p,'UNAPPLIED-NEXT-DRIVER-INCREMENT/'+p.name)
for key in ['actual_receiving_preview','guarded_adoption_script']:
 row=j[key];p=V/row['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'];cp(p,'UNAPPLIED-NEXT-DRIVER-INCREMENT/'+p.name)
(D/'COPY-ORIGINS.json').write_text(json.dumps(orig,indent=2)+'\n');p=D/'README.md';p.write_text(p.read_text()+'''\nAdditional small records preserve ROOT's successful native renewal of its own T-2804 claim and the later remote contents readback. The next driver-increment audit and guarded preparation script are **prepared only, not applied**. The earlier preparation's stale ownership note is historical; the separate renewal records contain the actual subsequent update. No broad ticket was marked done.\n''')
cp(Path(__file__),'ARCHIVE-RECIPE/extend_packet.py');M=json.loads((D/'MANIFEST.json').read_text());rows=[]
for p in sorted(D.rglob('*')):
 if p.is_file() and p!=D/'MANIFEST.json':
  b=p.read_bytes();rows.append(dict(path=str(p.relative_to(D)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
M.update(records=rows,packet_bytes_without_manifest=sum(r['bytes'] for r in rows),own_T2804_native_renewal_preserved=True,next_driver_increment='PREPARED_NOT_APPLIED',manifest_finalized_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());(D/'MANIFEST.json').write_text(json.dumps(M,indent=2)+'\n');assert len(rows)==len([p for p in D.rglob('*') if p.is_file()])-1
print(json.dumps(dict(records=len(rows),bytes=M['packet_bytes_without_manifest'],manifest_sha256=hashlib.sha256((D/'MANIFEST.json').read_bytes()).hexdigest()),indent=2))
