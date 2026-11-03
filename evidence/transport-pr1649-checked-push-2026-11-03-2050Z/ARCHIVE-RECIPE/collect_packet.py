from pathlib import Path
import json,shutil,gzip,hashlib,datetime,re
R=Path('/workspace/.cloud-setup/transport-current-20261103');D=Path('/tmp/transport-evidence-recovery-20261103/repo/evidence/transport-pr1649-checked-push-2026-11-03-2050Z');D.mkdir(parents=True,exist_ok=False);origins=[]
def cp(p,rel):
 b=p.read_bytes();compress=len(b)>512*1024;q=D/(rel+'.gz' if compress else rel);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(gzip.compress(b,mtime=0) if compress else b);origins.append(dict(path=str(q.relative_to(D)),original=str(p),original_bytes=len(b),original_sha256=hashlib.sha256(b).hexdigest(),lossless_gzip=compress,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
for n in ['actual-dev92-fourpart-preflight-01','actual-dev92-checked-delivery-01','actual-head543-frame-dispatch','ci-head543-initial']:
 for p in sorted((R/n).rglob('*')):
  if p.is_file() and 'native-tmp' not in p.relative_to(R/n).parts:cp(p,'ACTUAL-RESULTS/'+n+'/'+str(p.relative_to(R/n)))
for n in ['run_fourpart_preflight.py','run_fourpart_preflight_v2.py','deliver_checked_pr1649.py','REVIEWABLE-COMMIT-MESSAGE.txt','FOURPART-OUTPUT-ERRATUM.json','RESTORED-RUNTIME-BASELINE.json','RUNTIME-EPOCH-METADATA-ERRATUM.json','resource_guard.py','DEV92-FINAL-SOURCE-BEFORE-FULL-GATE.json','DEV92-COLUMN-ASSET-DELTA.json']:
 cp(R/n,'EXECUTION-HELPERS-AND-CONTEXT/'+n)
cp(Path('/workspace/.cloud-setup/transport-supervise.py'),'EXECUTION-HELPERS-AND-CONTEXT/transport-supervise.py')
cp(R/'periodic-evidence-checked-push/PUBLIC-APP-COMMIT.json','PUBLIC-SOURCE/PUBLIC-APP-COMMIT.json')
for folder,name in [('periodic-evidence','0B7'),('periodic-evidence-memory','C7'),('periodic-evidence-final-prep','478')]:cp(R/folder/'PUBLICATION-CLOSED.json','PRIOR-PUBLIC-PROOF-REFERENCES/'+name+'-PUBLICATION-CLOSED.json')
g=json.loads((R/'actual-dev92-fourpart-preflight-01/CLOSED.json').read_text());assert g['status']=='PASS_ALL_FOUR_NATIVE_PREFLIGHT_PARTS_SAME_SOURCE' and len(g['ledger'])==4 and g['owned_TMPDIR_cleanup_complete'];assert g['native_distinct_steps']==1152 and g['native_selftests']==400
ansi=re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]');partrows=[]
for row in g['ledger']:
 k=row['part'];p=R/'actual-dev92-fourpart-preflight-01';body=ansi.sub('',(p/('part-'+str(k)+'-preflight-check.log')).read_text());native=ansi.sub('',(p/('native-preflight-part-'+str(k)+'.log')).read_text());r=row['result'];cl=row['cleanup'];assert r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==600 and r['timeout_override_reason']is None and cl['cleanup_complete'] and not cl['remaining_owned_children'] and row['resources']['accepted'];assert row['source_before']==row['source_after']==g['source_before']
 f=re.findall(r'^CHECK PASS[^\n]*part '+str(k)+r'/4:\s*(\d+) steps, none red\.$',body,re.M);assert len(f)==1 and int(f[0])==row['native_footer_counts']['selected_steps'];assert len(re.findall(r'^PREFLIGHT PASS\b',native,re.M))==1;assert not re.search(r'^CHECK FAIL|^PREFLIGHT FAIL',body+'\n'+native,re.M)
 partrows.append(dict(part=k,native_footer_counts=row['native_footer_counts'],seconds=r['seconds'],native_returncode=0,original_cap_seconds=600,source_exact=True,resource_and_cleanup_PASS=True))
assert sum(r['native_footer_counts']['selected_steps'] for r in partrows)-g['every_part_execution_overlap']==1152;assert sum(r['native_footer_counts']['selftests'] for r in partrows)==400
(D/'NATIVE-FOOTER-READBACK.json').write_text(json.dumps(dict(status='ALL_FOUR_ACTUAL_NATIVE_PREFLIGHT_AND_CHECK_FOOTERS_VERIFIED',source=g['source_before'],native_distinct_steps=1152,selftests=400,parts=partrows,outer_helper_returncode=1,outer_post_receipt_error_preserved=True),indent=2)+'\n')
(D/'COPY-ORIGINS.json').write_text(json.dumps(origins,indent=2)+'\n');print('copied',len(origins),'records; allnativefooters independently verified')
