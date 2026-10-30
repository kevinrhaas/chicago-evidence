import datetime,gzip,hashlib,json,os,pathlib,subprocess
B=pathlib.Path(__file__).parent; G=B/'GENERATED'; G.mkdir(exist_ok=True); (B/'PAYLOAD').mkdir(exist_ok=True)
O=pathlib.Path('/tmp/HORSE-ACTUAL-SOURCE-USE-TAIL53-20261030-01')
R=pathlib.Path('/tmp/HORSE-SOURCE-USE-CLOSED-REPAIR-LIGHT-20261030-01')
repo='/tmp/chicago-horse-20261029'; env={**os.environ,'GIT_NO_LAZY_FETCH':'1'}
def sha(b):return hashlib.sha256(b).hexdigest()
def jwrite(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
files=[];snapshots=[]
def freeze(p,label):
 p=pathlib.Path(p);raw=p.read_bytes();out=G/label;out.write_bytes(raw);snapshots.append({'captured_from':str(p),'frozen_path':str(out),'bytes':len(raw),'sha256':sha(raw)});files.append(out);return out
closed=json.loads((O/'ACTUAL-SOURCE-USE-TAIL-CLOSED.json').read_text());assert sha((O/'ACTUAL-SOURCE-USE-TAIL-CLOSED.json').read_bytes())=='60c38c665bbbcd84dff0a70546e7e00d7428084a3ce90dd6e4b7b91bcf4f0a7e'
assert not closed['errors'] and closed['resource10_pair']['accepted'] and closed['owned_SHM_scratch_removed'] and not closed['full_check_sh_PASS_claimed']
for p in sorted(O.rglob('*')):
 if p.is_file():files.append(p)
for p in sorted(R.iterdir()):
 if p.is_file():files.append(p)
for folder in ['HORSE-SOURCE-USE-TAIL53-PREP-20261030','HORSE-FULL-GATE-RETRY03-PREP-20261030','HORSE-CHECKED-FEATURE-PUSH-SOURCEUSE-PREP-20261030']:
 for p in sorted((pathlib.Path('/tmp')/folder).iterdir()):
  if p.is_file():freeze(p,folder+'--'+p.name)
freeze('/tmp/HORSE-SOURCE-USE-TAIL53-INDEPENDENT-SOURCE-REVIEW-20261030-01.json','TAIL53-INDEPENDENT-SOURCE-REVIEW-FROZEN.json')
freeze('/tmp/horse-quiet-head-neck-v6-source-use-closed-source-freeze-20261030-01.json','H117-SOURCEUSE-CLOSED-GUARD-FROZEN.json')
prefix=pathlib.Path('/workspace/.cloud-setup/logs/transport-recovery/horse-native-source-use-tail53-all-affected-checks-20261030-01')
for suffix in ['.log','.result.json','.cleanup.json']:files.append(pathlib.Path(str(prefix)+suffix))
outer=json.loads(pathlib.Path(str(prefix)+'.result.json').read_text());cleanup=json.loads(pathlib.Path(str(prefix)+'.cleanup.json').read_text())
assert outer['returncode']==0 and not outer['timed_out'] and outer['requested_timeout_seconds']==outer['effective_timeout_seconds']==1200
assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
settle=json.loads((O/'NATIVE-SETTLEMENT.json').read_text());assert settle['actual_laps']==2 and settle['actual_last_lap_moved_nothing'] and not settle['native_warning_accepted']
assert settle['manifest_before']['sha256']==settle['manifest_after']['sha256']
mapping=json.loads((R/'EXACT-9E3D-TO-SOURCE-USE-CLOSED-MAP.json').read_text());new=mapping['after_TREE'];old=mapping['before_TREE'];path='chicago/4d/docs/measurements/source_use_coverage.md'
changed=subprocess.check_output(['git','-C',repo,'diff','--name-only',old,new],env=env).decode().splitlines();assert changed==[path]
patch=subprocess.check_output(['git','-C',repo,'diff','--binary',old,new],env=env);assert patch==(R/'EXACT-9E3D-TO-SOURCE-USE-CLOSED.patch').read_bytes()
newdata=subprocess.check_output(['git','-C',repo,'show',new+':'+path],env=env);assert len(newdata)==3589 and sha(newdata)==mapping['changes'][0]['after']['sha256']
newreport=G/'EXACT-NEW-3589B-source_use_coverage.md';newreport.write_bytes(newdata);files.append(newreport)
assert subprocess.check_output(['git','-C',repo,'rev-parse',new+':chicago/4d'],env=env).decode().strip()==mapping['after_APP']
assert sha((R/'COMPLETE-SOURCE-USE-CLOSED-SEMANTIC-INDEX.z').read_bytes())=='8805fc7bd8ae522a83d86654160257336efba95c6b5730199b827b89fe513ff9'
readonly_map=G/'ACTUAL-READONLY-TREE-PATCH-AND-SETTLEMENT-PROOF.json';jwrite(readonly_map,{'old_tree':old,'new_tree':new,'old_app':mapping['before_APP'],'new_app':mapping['after_APP'],'only_changed_path':path,'patch_sha256':sha(patch),'new_report_bytes':len(newdata),'new_report_sha256':sha(newdata),'native_settlement':settle,'outer_actual_result':outer,'outer_actual_cleanup':cleanup,'all_models_runtime_63code_certificate_unchanged':closed['source_after']['all63_qualifier_code_pins_exact'] and closed['source_after']['finite_certificate_exact'],'full03_feature_push':'UNRUN at capture','old_full_failures':'Preserved public bcebb64/d260790; never relabeled PASS','primary_source_index_Git_changes_by_packet':False});files.append(readonly_map)
sm=G/'FROZEN-HELPER-CONFIG-SOURCE-GUARD-COPY-MAP.json';jwrite(sm,snapshots);files.append(sm);files.append(pathlib.Path(__file__))
old_sha='277c26af03ece19bf0d26e3a37494cafe592be8f4bb769c5fd096ef908a58ed4'
previous=json.loads(pathlib.Path('/tmp/PREPARED-H3-P1-REPAIRS-AND-ACTUAL-MEASUREMENTS-20261030/ENCODED-PAYLOAD-MANIFEST.json').read_text())
prior=next(r for r in previous['files'] if r['original_sha256']==old_sha)
public_commit='c8daf128b2d1f150bfc09fcad8e9f8ff27327883';public_path='evidence/transport-photoquality-2026-10-29/ROOT-HORSE-AND-OTIS-REAL-ISOLATION-REPAIRS-AND-SOURCE/'+prior['payload_path']
rows=[];unique={}
for p in dict.fromkeys(files):
 raw=p.read_bytes();h=sha(raw)
 if h==old_sha:
  row={**prior,'original_path':str(p),'storage':'already-public-byte-exact-reference','public_commit':public_commit,'public_path':public_path}
 elif h in unique:row={**unique[h],'original_path':str(p),'storage':'same-checkpoint-byte-exact-alias'}
 else:
  enc=gzip.compress(raw,compresslevel=1,mtime=0);rel=pathlib.Path('PAYLOAD')/(h+'-'+p.name+'.gz');(B/rel).write_bytes(enc);assert gzip.decompress(enc)==raw
  row={'original_path':str(p),'original_bytes':len(raw),'original_sha256':h,'storage':'new-encoded-payload','payload_path':str(rel),'encoding':'gzip-mtime0-level1','encoded_bytes':len(enc),'encoded_sha256':sha(enc)};unique[h]=row
 rows.append(row)
manifest={'schema':'root-normal-git-evidence-packet-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'Actual native53tail settled2laps and all56affected checks PASS; one native-derived coverage-report source repair staged. Full03/feature push/DEV acceptance UNRUN at capture.','outer_actual_result':outer,'outer_actual_cleanup':cleanup,'actual_native_phases':closed['phases'],'native_settlement':settle,'source_repair_map':mapping,'helper_status':'Tail53 source-cleared/executed. Full03 and checked-push frozen prepared/unrun; independent final review pending at capture.','file_count':len(rows),'new_unique_payload_count':len(unique),'encoded_payload_bytes':sum(r['encoded_bytes'] for r in unique.values()),'original_bytes':sum(r['original_bytes'] for r in rows),'files':rows,'preservation':'Existing public full failures retained. No model/asset/runtime63/cert changes. No source/shared-index/primary-Git writes, browser, active P03/H03 logs or mutable global state included. Root sole Git publisher.'}
jwrite(B/'ENCODED-PAYLOAD-MANIFEST.json',manifest)
(B/'README.md').write_text('Closed H native source-use tail53: two actual laps, final lap moved nothing, no native-warning acceptance; then all56 actual affected checks PASS. Actual outer627.601s/original1200 with cleanup0 and healthy resource10 pair. Only source change is3589-byte source_use_coverage.md; exact old/new patch/map/tree/index/proof included. Models/runtime63/certificate unchanged. Original full02 NONPASS remains public; full03 and checked feature push are prepared/unrun, final source review pending at capture. Assets and active P03/H03/global logs excluded. Old semantic index is referenced by exact already-public c8daf blob. Root owns normal Git publication.\n')
print(json.dumps({'manifest':str(B/'ENCODED-PAYLOAD-MANIFEST.json'),'sha256':sha((B/'ENCODED-PAYLOAD-MANIFEST.json').read_bytes()),'records':len(rows),'new_unique_payloads':len(unique),'encoded_bytes':manifest['encoded_payload_bytes']},indent=2))
