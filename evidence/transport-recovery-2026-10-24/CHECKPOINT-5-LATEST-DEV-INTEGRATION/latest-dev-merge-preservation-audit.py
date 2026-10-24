#!/usr/bin/env python3
"""Read-only committed-tree audit pinned to the merged transport HEAD and its DEV parent."""
import datetime,difflib,hashlib,json,subprocess
from pathlib import Path
REPO=Path('/workspace/chicago')
BASE='29ea317f30ea110c4477e84a8d34b55f9fc50e55'
HEAD='3290195d40cbacf5cbfd0c76f14119d6712aa30c'
PRIOR_BASE='84f68e9fde5e7193037cde3b52b9251bd5497600'
R=Path('/workspace/.cloud-setup/logs/transport-recovery')
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
def blob(ref,p):return git('show',ref+':'+p)
def paths(*args):return set(git(*args).decode().splitlines())
receipt=json.loads((R/'app-commit-receipt.json').read_bytes());expected={x['path']:x for x in receipt['files']}
changed=paths('diff','--name-only',BASE,HEAD)
old=blob(BASE,'chicago/4d/docs/LIBERTIES.md');now=blob(HEAD,'chicago/4d/docs/LIBERTIES.md')
lines=old.splitlines(keepends=True);iterator=iter(now.splitlines(keepends=True));raw_all=all(any(line==oldline for line in iterator) for oldline in lines)
starts=[i for i,line in enumerate(lines) if line.startswith(b'### ')];blocks=list(zip(starts,starts[1:]+[len(lines)]));glessner=[(i,j) for i,j in blocks if b'glessner' in lines[i].lower()]
a=json.loads(blob(BASE,'chicago/4d/data/liberties.json'))['liberties'];b=json.loads(blob(HEAD,'chicago/4d/data/liberties.json'))['liberties'];a={x['id']:x for x in a};b={x['id']:x for x in b};gids=[k for k in a if 'glessner' in k.lower()]
roadmap=blob(HEAD,'chicago/4d/docs/ROADMAP.md');invalid=None
try:roadmap.decode('utf8')
except UnicodeDecodeError as exc:invalid=hex(roadmap[exc.start])
source_mismatches=[]
for p,spec in expected.items():
 data=blob(HEAD,p)
 if len(data)!=spec['bytes'] or hashlib.sha256(data).hexdigest()!=spec['sha256']:source_mismatches.append(p)
newdevpaths=paths('diff','--name-only',PRIOR_BASE,BASE)
result={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'comparison_dev':BASE,'audited_commit':HEAD,'audited_tree':git('rev-parse',HEAD+'^{tree}').decode().strip(),'recovery_path_count':len(changed),'expected_path_count':len(expected),'unexpected_changed_paths':sorted(changed-expected.keys()),'expected_paths_missing_from_diff':sorted(expected.keys()-changed),'all59prior_committed_source_hashes_preserved':not source_mismatches,'source_hash_mismatches':source_mismatches,'new_dev_paths_since_original_audited_base':len(newdevpaths),'incoming_dev_paths_untouched_by_recovery':len(newdevpaths-changed),'incoming_dev_expected_shared_overlap_paths':sorted(newdevpaths&changed),'all_old_liberty_raw_lines_retained_in_order':raw_all,'glessner_markdown_blocks':len(glessner),'missing_or_changed_glessner_markdown_blocks':[lines[i].decode().strip() for i,j in glessner if b''.join(lines[i:j]) not in now],'glessner_json_ids':len(gids),'changed_glessner_json_ids':[k for k in gids if b.get(k)!=a[k]],'missing_old_liberty_json_ids':sorted(a.keys()-b.keys()),'roadmap_original_invalid_utf8_byte':invalid,'preserved_child_commits':{x['ticket']:subprocess.run(['git','-C',str(REPO),'merge-base','--is-ancestor',x['commit'],HEAD],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0 for x in receipt['commits']},'limitations':['Audits the pinned committed merge tree, not transient writes from the currently running owner tail.','No full preflight, browser, CI, DEV merge, photographic or production acceptance is inferred.']}
# Four shared files legitimately gain incoming DEV additions; preserve both parents.
prior_head='8c45c899f696eb87da9f818828bed36668bdfa2b'
allowed_merged={'chicago/4d/tools/check.sh','chicago/4d/tools/step_isolation.json','chicago/4d/data/liberties.json','chicago/4d/docs/LIBERTIES.md'}
result['byte_identical_prior_source_file_count']=len(expected)-len(source_mismatches)
result['expected_shared_file_source_changes']=sorted(allowed_merged&set(source_mismatches))
result['unexpected_source_hash_mismatches']=sorted(set(source_mismatches)-allowed_merged)
result['all_non_shared_prior_source_hashes_preserved']=not result['unexpected_source_hash_mismatches']
for p,key in [('chicago/4d/docs/LIBERTIES.md','prior_head_liberty_raw_lines_retained'),('chicago/4d/tools/check.sh','prior_head_gate_raw_lines_retained')]:
 it=iter(blob(HEAD,p).splitlines(keepends=True))
 result[key]=all(any(line==oldline for line in it) for oldline in blob(prior_head,p).splitlines(keepends=True))
isolation=json.loads(blob(HEAD,'chicago/4d/tools/step_isolation.json'))['tools']
result['registry_preservation_by_parent']={}
for label,ref in [('latest_dev',BASE),('prior_transport_head',prior_head)]:
 oldrows=json.loads(blob(ref,'chicago/4d/tools/step_isolation.json'))['tools']
 result['registry_preservation_by_parent'][label]={'old_row_count':len(oldrows),'merged_row_count':len(isolation),'missing_rows':sorted(oldrows.keys()-isolation.keys()),'changed_rows':[k for k,v in oldrows.items() if isolation.get(k)!=v],'added_rows':sorted(isolation.keys()-oldrows.keys())}
prior_libs={x['id']:x for x in json.loads(blob(prior_head,'chicago/4d/data/liberties.json'))['liberties']}
result['prior_transport_liberty_records_preserved']={k:b.get(k)==prior_libs[k] for k in ['L-brougham-parked-2794','L-brougham-distance-replacement-2794','L-standing-horse-development-2800']}
print(json.dumps(result,indent=2))
