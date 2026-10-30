import argparse,datetime,gzip,hashlib,json,pathlib,re,shutil
p=argparse.ArgumentParser();p.add_argument('--stages',nargs='+',required=True);p.add_argument('--out',required=True);p.add_argument('--accepted-before',type=int,required=True);p.add_argument('--unqualified-before',type=int,required=True);p.add_argument('--extra',nargs='*',default=[]);p.add_argument('--attempts',nargs='*',default=[]);a=p.parse_args();attempts=dict(x.split(':',1)for x in a.attempts)
B=pathlib.Path(a.out);assert not B.exists();B.mkdir();(B/'PAYLOAD').mkdir();(B/'GENERATED').mkdir()
O=pathlib.Path('/workspace/.cloud-setup/logs/transport-recovery/WAGON-CURRENT-DEV-20261029/PINNED-EC16-INTAKE-PRESERVED/OWNED-WAGON-BOUND-REPAIR-20261029');L=O.parent.parent
pub=json.loads(pathlib.Path('/tmp/WAGON-W4-PUBLIC330A-REFERENCE-INDEX-20261030.json').read_text());refs={r['original_sha256']:r for r in pub['manifest']['files']}
def sha(b):return hashlib.sha256(b).hexdigest()
files=[];summaries=[]
for stage in a.stages:
 attempt=attempts.get(stage,'01');assert attempt in ['01','02'];d=pathlib.Path('/tmp')/f'WAGON-OWNBOUND-PUBLISHED-DESKTOP-STAGE{stage}-{attempt}';prefix=L/f'rail-owned-wagon-bound-published-desktop-{stage}-{attempt}'
 v=json.loads((d/'ACTUAL-PARTIAL-VERDICT.json').read_text());result=json.loads(pathlib.Path(str(prefix)+'.result.json').read_text());cleanup=json.loads(pathlib.Path(str(prefix)+'.cleanup.json').read_text());pair=json.loads((d/'ACTUAL-RESOURCE-PAIR-VERDICT.json').read_text())
 assert v['viewport']=='desktop' and v['stage']==stage and result['requested_timeout_seconds']==result['effective_timeout_seconds']==600 and result['timeout_override_reason']is None
 assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
 binding_before=json.loads((d/'SOURCE-AND-MIRROR-BEFORE.json').read_text());assert binding_before==json.loads((d/'SOURCE-AND-MIRROR-AFTER.json').read_text()) and v['source_index_fullmirror_unchanged']
 text=pathlib.Path(str(prefix)+'.log').read_text(errors='replace');failures=[line for line in text.splitlines()if re.match(r'\s*(?:FAIL|fail)\b',line)]
 if v['result'].startswith('PASS'):
  assert result['returncode']==0 and not result['timed_out'] and pair['accepted'] and v['failed_checks']==0 and 'SMOKE PASS'in text
 summaries.append({'viewport':'desktop','stage':stage,'attempt':attempt,'actual_verdict':v,'original_native_result':result,'original_cleanup':cleanup,'resource10_pair_accepted':pair['accepted'],'logged_assertion_failure_lines':failures,'whole_gate':'PENDING; prior unqualified remain, each new native nonpass stays unqualified, nativePASS/resourceNONPASS remains separate pending until explicit qualification'})
 files.extend(x for x in sorted(d.rglob('*'))if x.is_file())
 files.extend(pathlib.Path(str(prefix)+s)for s in ['.log','.result.json','.cleanup.json'])
for name in ['run-other-native-published-groups-ownbound-11-PROPOSED.py','resource_admission_v10.py']:
 f=O/name;q=B/'GENERATED'/name;q.write_bytes(f.read_bytes());files.append(q)
handoff=pathlib.Path('/tmp/WAGON-W11-ACTUAL-COMMITTED-H-P-PUBLICATION-CLOSED-HANDOFF-20261030.json');files.append(handoff)
for extra in a.extra:
 f=pathlib.Path(extra);assert f.is_file();files.append(f)
proof=B/'GENERATED/ACTUAL-CLOSED-BATCH-SUMMARY.json';proof.write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closed_only':summaries,'accepted_before':a.accepted_before,'accepted_after':a.accepted_before+sum(x['actual_verdict']['result'].startswith('PASS')for x in summaries),'unqualified_before':a.unqualified_before,'unqualified_after':a.unqualified_before+sum(not x['actual_verdict']['result'].startswith('PASS')and not x['actual_verdict'].get('native_assertions_complete_PASS',False)for x in summaries),'new_separate_nativePASS_resourceNONPASS_pending':sum(x['actual_verdict'].get('native_assertions_complete_PASS',False)and not x['resource10_pair_accepted']for x in summaries),'source_HEAD':'78b11b7a8e49126a8a5724a4035ea961461a4f49','whole_gate_CI_DEV_or_broad_visual_acceptance':'PENDING/UNKNOWN; no claim','no_active_controller_global_state_or_logs_copied':True},indent=2)+'\n');files.append(proof)
q=B/'GENERATED/PREPARE-EXACT-SCRIPT.py';q.write_bytes(pathlib.Path(__file__).read_bytes());files.append(q)
rows=[];unique={}
for f in dict.fromkeys(files):
 raw=f.read_bytes();h=sha(raw)
 if h in refs:
  r=refs[h];row={**r,'original_path':str(f),'storage':'already-public-byte-exact-reference','public_commit':pub['public_commit'],'public_path':pub['public_prefix']+'/'+r['payload_path']}
 elif h in unique:row={**unique[h],'original_path':str(f),'storage':'same-checkpoint-byte-exact-alias'}
 else:
  enc=gzip.compress(raw,compresslevel=1,mtime=0);rel=pathlib.Path('PAYLOAD')/(h+'-'+f.name+'.gz');(B/rel).write_bytes(enc);assert gzip.decompress(enc)==raw
  row={'original_path':str(f),'original_bytes':len(raw),'original_sha256':h,'storage':'new-encoded-payload','payload_path':str(rel),'encoding':'gzip-mtime0-level1','encoded_bytes':len(enc),'encoded_sha256':sha(enc)};unique[h]=row
 rows.append(row)
manifest={'schema':'root-normal-git-evidence-packet-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'Only closed W native partial groups; original600/native assertions/source frozen. Whole gate pending.','closed_batch':json.loads(proof.read_text()),'file_count':len(rows),'new_unique_payload_count':len(unique),'encoded_payload_bytes':sum(r['encoded_bytes']for r in unique.values()),'original_bytes':sum(r['original_bytes']for r in rows),'files':rows,'preservation':'No app/shared-index/Git writes, active global state/logs, model assets, retries or cap/assertion changes. Original exact source/index/mirror baseline referenced already-public330a; native closed PNGs kept as limited views, not broad photoquality/motion acceptance. Root sole normal Git publisher.'}
(B/'ENCODED-PAYLOAD-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');(B/'README.md').write_text(manifest['preservation']+'\n'+manifest['state']+'\n')
print(json.dumps({'manifest':str(B/'ENCODED-PAYLOAD-MANIFEST.json'),'sha256':sha((B/'ENCODED-PAYLOAD-MANIFEST.json').read_bytes()),'records':len(rows),'new_unique_payloads':len(unique),'encoded_bytes':manifest['encoded_payload_bytes']},indent=2))
