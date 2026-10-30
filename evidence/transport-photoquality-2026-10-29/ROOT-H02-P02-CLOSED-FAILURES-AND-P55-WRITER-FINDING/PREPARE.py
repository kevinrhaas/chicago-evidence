import datetime, gzip, hashlib, json, os, pathlib, subprocess

B = pathlib.Path(__file__).parent
G = B / 'GENERATED'
G.mkdir(exist_ok=True)
(B / 'PAYLOAD').mkdir(exist_ok=True)
D = pathlib.Path('/tmp/OTIS-NATURAL-IDLE-ACTUAL-WRITER-MEASUREMENT-20261030-01')
repo = pathlib.Path('/tmp/chicago-transport-resume-20261029')
env = {**os.environ, 'GIT_NO_LAZY_FETCH': '1'}
def sha(b): return hashlib.sha256(b).hexdigest()
def write_json(path, data): path.write_text(json.dumps(data, indent=2)+'\n')
def freeze(p, label):
    p=pathlib.Path(p); data=p.read_bytes(); q=G/label; q.write_bytes(data)
    frozen.append({'captured_from':str(p),'frozen_path':str(q),'bytes':len(data),'sha256':sha(data)})
    return q

frozen=[]
files=[]
closed_summaries={}
for name in ['HORSE','OTIS']:
    out=pathlib.Path(f'/tmp/{name}-ACTUAL-FULL-GATE-SHM-20261030-02')
    closed=json.loads((out/'ACTUAL-WHOLE-GATE-CLOSED.json').read_text())
    result=json.loads((out/'native-check.result.json').read_text())
    cleanup=json.loads((out/'native-check.cleanup.json').read_text())
    assert result['returncode']==1 and not result['timed_out']
    assert result['requested_timeout_seconds']==result['effective_timeout_seconds']==1200
    assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children']
    closed_summaries[name]={'actual_result':result,'actual_cleanup':cleanup,'closure_status':closed['status'],'tree':closed['tree'],'app_tree':closed['app_tree']}
    files.extend(p for p in sorted(out.iterdir()) if p.is_file())

writer=json.loads((D/'ACTUAL-WRITER-MEASUREMENT-CLOSED.json').read_text())
assert writer['native_result']['returncode']==0 and not writer['native_result']['timed_out']
assert writer['native_cleanup']['cleanup_complete'] and not writer['native_cleanup']['remaining_owned_children']
assert writer['decoded_JSON_difference_count']==1 and writer['receipt_byte_length_delta']==53 and writer['generated_GLB_mismatch_count']==0
assert writer['actual_differences'][0]['json_pointer']=='/scope'
files.extend(p for p in sorted(D.iterdir()) if p.is_file())
files.append(D/'generated/DERIVATION.json')
receipt=writer['committed_receipt']
frozen_receipt=freeze(receipt['path'],'P-COMMITTED-DERIVATION-6234-BYTES.json')
assert frozen_receipt.stat().st_size==receipt['bytes'] and sha(frozen_receipt.read_bytes())==receipt['sha256']
files.append(frozen_receipt)

new_tree='bed69364051ee11b8684c9a02793d40e9b870a4f'
new_app='a6b4c60ac78d108eacb394d86a218a82438eff77'
old_tree='222273b4b2e118885887ebb94f7778b70029ddbd'
old_app='3fc00238e7435a9ee5566e38b8d05d0618ee6355'
inventory_path='chicago/4d/tools/writer_inventory.json'
new_inventory=subprocess.check_output(['git','-C',str(repo),'show',f'{new_tree}:{inventory_path}'],env=env)
old_inventory=subprocess.check_output(['git','-C',str(repo),'show',f'{old_tree}:{inventory_path}'],env=env)
assert old_inventory==(D/'ORIGINAL-writer_inventory.json').read_bytes()
new_inventory_file=G/'EXACT-NEW-P55-writer_inventory.json'; new_inventory_file.write_bytes(new_inventory); files.append(new_inventory_file)
actual_patch=subprocess.check_output(['git','-C',str(repo),'diff','--binary',old_tree,new_tree],env=env)
assert actual_patch==(D/'ONE-WRITER-INVENTORY-REPAIR.patch').read_bytes()
changed=subprocess.check_output(['git','-C',str(repo),'diff','--name-only',old_tree,new_tree],env=env).decode().splitlines()
assert changed==[inventory_path]
assert subprocess.check_output(['git','-C',str(repo),'rev-parse',f'{new_tree}:chicago/4d'],env=env).decode().strip()==new_app

guard=json.loads((D/'SOURCE55-AFTER-WRITER-INVENTORY-REFREEZE.json').read_text())
assert guard['TREE']==new_tree and guard['APP']==new_app and guard['source_files']==55
files.append(freeze(guard['guard']['path'],'P55-SOURCE-GUARD-FROZEN.json'))
for item in guard['native_checks']:
    log=pathlib.Path(item['log'])
    for suffix in ['.log','.result.json','.cleanup.json']:
        p=log.with_name(log.name[:-4]+suffix)
        assert p.is_file(),str(p)
        files.append(p)
    assert item['native_result']['returncode']==item['expected_returncode']
    assert item['native_cleanup']['cleanup_complete'] and not item['native_cleanup']['remaining_owned_children']

failure_prefix=pathlib.Path('/workspace/.cloud-setup/logs/transport-recovery/otis-measured-writer-inventory-native-coverage-20261030-01')
for suffix in ['.log','.result.json','.cleanup.json']:
    files.append(pathlib.Path(str(failure_prefix)+suffix))
for prepname in ['OTIS-WHOLE-GATE-AFTER-WRITER-INVENTORY-PREP-20261030','OTIS-CHECKED-FEATURE-PUSH-AFTER-WRITER-INVENTORY-PREP-20261030']:
    for p in sorted((pathlib.Path('/tmp')/prepname).iterdir()):
        if p.is_file(): files.append(freeze(p,prepname+'--'+p.name))

asset_refs=[]
for asset in writer['generated_glbs']:
    generated=pathlib.Path(asset['generated_path']); active=pathlib.Path(asset['active_path'])
    gb=generated.read_bytes(); ab=active.read_bytes()
    assert gb==ab and len(gb)==asset['bytes'] and sha(gb)==asset['sha256']
    asset_refs.append({**asset,'storage':'existing-original-generated-and-active-files-retained-not-copied','verified_byte_exact_now':True})
assert len(asset_refs)==8
refs=G/'EIGHT-GLB-EXACT-SHA-REFERENCES-NO-ASSET-PAYLOAD.json'; write_json(refs,asset_refs);files.append(refs)
map_file=G/'P55-ONE-INVENTORY-REPAIR-AND-RECEIPT-CLASSIFICATION-MAP.json'
write_json(map_file,{'old_tree':old_tree,'old_app':old_app,'new_tree':new_tree,'new_app':new_app,'only_changed_path':inventory_path,'old_inventory_sha256':sha(old_inventory),'new_inventory_sha256':sha(new_inventory),'patch_sha256':sha(actual_patch),'semantic_index_sha256':guard['semantic_index_sha256'],'semantic_index_entries':guard['semantic_index_entries'],'generated_receipt':writer['generated_receipt'],'committed_receipt':receipt,'decoded_difference':writer['actual_differences'],'receipt_length_delta_bytes':53,'classification':'not_derivable: eight GLBs reproduce exactly; authored scope in committed receipt differs from generator output','no_GLB_generator_code_or_receipt_source_edits':True,'full03_pass_or_feature_push':False})
files.append(map_file)
fm=G/'FROZEN-MUTABLE-INPUT-COPY-MAP.json';write_json(fm,frozen);files.append(fm)
files.append(pathlib.Path(__file__))
rows=[];encoded_by_sha={}
for p in dict.fromkeys(files):
    raw=p.read_bytes(); h=sha(raw)
    if h in encoded_by_sha:
        prior=encoded_by_sha[h]
        row={**prior,'original_path':str(p),'storage':'same-checkpoint-byte-exact-alias'}
    else:
        enc=gzip.compress(raw,compresslevel=1,mtime=0)
        rel=pathlib.Path('PAYLOAD')/(h+'-'+p.name+'.gz');(B/rel).write_bytes(enc)
        assert gzip.decompress(enc)==raw
        row={'original_path':str(p),'original_bytes':len(raw),'original_sha256':h,'storage':'new-encoded-payload','payload_path':str(rel),'encoding':'gzip-mtime0-level1','encoded_bytes':len(enc),'encoded_sha256':sha(enc)}
        encoded_by_sha[h]=row
    rows.append(row)
manifest={'schema':'root-normal-git-evidence-packet-v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'Closed H02/P02 original1200 NONPASS preserved; actual P writer and single measured-not-derivable inventory repair staged. New full03/feature push/DEV acceptance UNRUN.','closed_full_gates':closed_summaries,'P_writer_actual_result':writer['native_result'],'P_writer_actual_cleanup':writer['native_cleanup'],'P55_only_source_repair':json.loads(map_file.read_text()),'file_count':len(rows),'new_unique_payload_count':len(encoded_by_sha),'encoded_payload_bytes':sum(r['encoded_bytes'] for r in encoded_by_sha.values()),'original_bytes':sum(r['original_bytes'] for r in rows),'files':rows,'preservation':'No source, shared index, primary Git object, native assertion or active H-tail log changes. Generated GLBs remain original and are referenced by exact SHA only. Root sole normal Git publisher.'}
write_json(B/'ENCODED-PAYLOAD-MANIFEST.json',manifest)
(B/'README.md').write_text('Closed H02/P02 full-native failures and measured P55 writer-inventory repair. Both native full gates returned1 under original1200 and clean owned cleanup; never relabeled PASS. Actual writer returned0 under original30 and reproduced all8 GLBs byte-exact; committed DERIVATION scope is the one authored difference (53-byte length delta), measured not_derivable. The only P staged repair is writer_inventory.json. Both small receipts, source provenance, native affected-contract outcomes (including expected ownership refusal1), complete indices/source/mirror guards and raw logs are retained. No generated GLB payloads or active Htail/global logs. Normal Git publication belongs to root.\n')
print(json.dumps({'manifest':str(B/'ENCODED-PAYLOAD-MANIFEST.json'),'sha256':sha((B/'ENCODED-PAYLOAD-MANIFEST.json').read_bytes()),'records':len(rows),'unique':len(encoded_by_sha),'encoded_bytes':manifest['encoded_payload_bytes']},indent=2))
