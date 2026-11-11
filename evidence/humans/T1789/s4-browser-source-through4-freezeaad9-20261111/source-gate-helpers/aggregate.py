from pathlib import Path
import hashlib,json,re,datetime
P=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in json.loads((P/'SOURCE-PINS.json').read_bytes()).items():assert sha(P/n)==h,n
assert not (P/'AGGREGATE.json').exists(),'preserve existing aggregate'
raw=(P/'FREEZE.json').read_bytes();pin=hashlib.sha256(raw).hexdigest();d=json.loads(raw);assert json.loads((P/'READY.json').read_bytes())['freeze_SHA256']==pin and d['parts']==16 and d['CHECK_JOBS']==4
parts=[];total=0
for i in range(1,17):
 p=P/f'part{i}.CLOSED.json';c=json.loads(p.read_bytes());assert c['accepted'] and c['part']==i and c['freeze_SHA256']==pin and c['CHECK_JOBS']==4 and c['partition_count']==16
 r,k,g=c['result'],c['cleanup'],c['resources'];assert r['returncode']==0 and not r['timed_out'] and r['requested_timeout_seconds']==r['effective_timeout_seconds']==600 and r['timeout_override_reason'] is None and k['cleanup_complete'] and not k['remaining_owned_children'] and g['accepted']
 log=(P/f'part{i}.log').read_bytes();assert hashlib.sha256(log).hexdigest()==c['log_SHA256'] and log.decode(errors='replace').count('S4_SOURCE_VERIFIED '+pin)==2
 assert len(c['actual_final_markers'])==1;m=re.fullmatch(r'CHECK PASS — part '+str(i)+r'/16: (\d+) steps, none red\.',c['actual_final_markers'][0]);assert m
 n=int(m.group(1));total+=n;parts.append(dict(part=i,steps=n,seconds=r['seconds'],CLOSED_SHA256=sha(p)))
a=dict(status='ALL16_S4_SOURCE_GATE_PARTS_PASS_NOT_NATIVE_QUALIFICATION',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=d['head'],branch=d['branch'],protected_primary_ref=d['protected_ref'],protected_primary_head=d['protected_ref_head'],index_tree=d['index_tree'],freeze_SHA256=pin,frozen_files=301,old_source_exceptions=d['old_source_exceptions'],incoming_dev=None,deleted_paths=[],native8_fixture_unchanged=True,parts=parts,sum_part_executions=total,prior_S2_gate_claims_reused=False,prior_S3_gate_claims_reused=False,partition_count=16,CHECK_JOBS=4,sum_includes_repeated_every_part_prerequisites=True,native_bake_fixture_pose_photo='PENDING',commit=False,push=False)
(P/'AGGREGATE.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(dict(status=a['status'],steps=total,parts=16,freeze_SHA256=pin)))
