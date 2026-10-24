#!/usr/bin/env python3
"""Read-only audit of the pinned uncommitted staged merge. No app or Git writes."""
import collections,datetime,hashlib,json,re,subprocess
from pathlib import Path
REPO=Path('/workspace/chicago');R=Path('/workspace/.cloud-setup/logs/transport-recovery')
OLD='3290195d40cbacf5cbfd0c76f14119d6712aa30c'
BASE='de91c45b314a705a6cc2fb9430becb666dfbded6'
TREE='a38d9b3efebb79ba4b3cb7a7c283360fe8139aa5'
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args])
def blob(ref,p):return git('show',ref+':'+p)
def paths(*args):return set(git(*args).decode().splitlines())
def sha(b):return hashlib.sha256(b).hexdigest()
def sublines(old,new):
 it=iter(new.splitlines(keepends=True));return all(any(x==o for x in it) for o in old.splitlines(keepends=True))
mb=git('merge-base',OLD,BASE).decode().strip()
incoming=paths('diff','--name-only',mb,BASE);ours=paths('diff','--name-only',mb,OLD)
vs_base=paths('diff','--name-only',BASE,TREE);vs_old=paths('diff','--name-only',OLD,TREE)
allowed={'chicago/4d/data/liberties.json','chicago/4d/docs/LIBERTIES.md','chicago/4d/docs/ROADMAP.md','chicago/4d/docs/STATUS.md','chicago/4d/tools/check.sh','chicago/4d/tools/step_isolation.json'}
receipt=json.loads((R/'app-commit-receipt.json').read_bytes());ownpaths={x['path'] for x in receipt['files']}
old_source_changed=[p for p in sorted(ownpaths) if blob(OLD,p)!=blob(TREE,p)]
result={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old_source_head':OLD,'incoming_dev':BASE,'common_base':mb,'audited_staged_tree':TREE,'index_matches_audited_tree':subprocess.run(['git','-C',str(REPO),'diff','--cached','--quiet',TREE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0,'incoming_path_count':len(incoming),'incoming_paths_byte_unchanged':len(incoming-vs_base),'incoming_expected_shared_overlap_paths':sorted(incoming&vs_base),'unexpected_incoming_path_changes':sorted((incoming&vs_base)-allowed),'own_path_count':len(ours),'staged_recovery_diff_path_count':len(vs_base),'unexpected_recovery_diff_paths':sorted(vs_base-ownpaths),'old59_source_paths_byte_unchanged':len(ownpaths)-len(old_source_changed),'old59_source_changed_paths':old_source_changed,'unexpected_old_source_changes':sorted(set(old_source_changed)-allowed),'doc_conflict_blocks':{},'parent_acceptance_lines':{}}
critical=re.compile(rb'T-?(?:2794|2800|308[3456789]|2803|2804)\b')
for name in ['STATUS.md','ROADMAP.md']:
 p='chicago/4d/docs/'+name;resolved=blob(TREE,p);old=blob(OLD,p);incomingdoc=blob(BASE,p)
 marked=(R/'latest-dev-doc-conflicts'/(name+'.with-markers')).read_bytes();blocks=[];current=None;side=None
 for line in marked.splitlines(keepends=True):
  if line.startswith(b'<<<<<<< '):current={'ours':b'','incoming':b''};side='ours'
  elif current is not None and line.startswith(b'||||||| '):side='base'
  elif current is not None and line.rstrip(b'\r\n')==b'=======':side='incoming'
  elif current is not None and line.startswith(b'>>>>>>> '):blocks.append(current);current=None;side=None
  elif current is not None and side in ['ours','incoming']:current[side]+=line
 result['doc_conflict_blocks'][name]=[{'ours_bytes':len(x['ours']),'incoming_bytes':len(x['incoming']),'ours_retained_byte_exact':x['ours'] in resolved,'incoming_retained_byte_exact':x['incoming'] in resolved,'ours_sha256':sha(x['ours']),'incoming_sha256':sha(x['incoming'])} for x in blocks]
 lines=[x for x in old.splitlines(keepends=True) if critical.search(x)]
 result['parent_acceptance_lines'][name]={'old_critical_line_count':len(lines),'missing_or_changed_critical_line_count':sum(x not in resolved for x in lines)}
 if name=='ROADMAP.md':result['roadmap_FC_byte_counts']={'old_head':old.count(bytes([252])),'incoming_dev':incomingdoc.count(bytes([252])),'staged_tree':resolved.count(bytes([252]))}
p='chicago/4d/docs/LIBERTIES.md';old=blob(BASE,p);now=blob(TREE,p);lines=old.splitlines(keepends=True);starts=[i for i,l in enumerate(lines) if l.startswith(b'### ')];blocks=list(zip(starts,starts[1:]+[len(lines)]));g=[(i,j) for i,j in blocks if b'glessner' in lines[i].lower()]
result['incoming_liberty_raw_lines_all_retained']=sublines(old,now)
result['incoming_glessner_markdown_blocks']=len(g)
result['changed_incoming_glessner_markdown_blocks']=[lines[i].decode().strip() for i,j in g if b''.join(lines[i:j]) not in now]
def liberties(ref):return {x['id']:x for x in json.loads(blob(ref,'chicago/4d/data/liberties.json'))['liberties']}
a=liberties(BASE);b=liberties(TREE);c=liberties(OLD);g=[k for k in a if 'glessner' in k.lower()]
result['incoming_glessner_json_records']=len(g);result['changed_incoming_glessner_json_records']=[k for k in g if b.get(k)!=a[k]];result['missing_incoming_liberty_ids']=sorted(a.keys()-b.keys());result['old_transport_liberty_records_preserved']={k:b.get(k)==c[k] for k in ['L-brougham-parked-2794','L-brougham-distance-replacement-2794','L-standing-horse-development-2800']}
merged_rows=json.loads(blob(TREE,'chicago/4d/tools/step_isolation.json'))['tools'];result['isolation_registry_parent_preservation']={}
for label,ref in [('incoming_dev',BASE),('old_source_head',OLD)]:
 rows=json.loads(blob(ref,'chicago/4d/tools/step_isolation.json'))['tools'];result['isolation_registry_parent_preservation'][label]={'old_count':len(rows),'staged_count':len(merged_rows),'missing_rows':sorted(rows.keys()-merged_rows.keys()),'changed_rows':[k for k,v in rows.items() if merged_rows.get(k)!=v],'added_rows':sorted(merged_rows.keys()-rows.keys())}
sp='chicago/4d/tools/dev-smoke-state.json';saved=(R/'old-H-dev-smoke-state-original.json').read_bytes();bank=(R/'old-H-recorded-passing-smoke-state.json').read_bytes();original=json.loads(saved)['readings'];recorded=json.loads(bank)['readings'];canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'));a={canon(x) for x in original};b={canon(x) for x in recorded}
result['external_state_restore']={'original_backup_sha256':sha(saved),'recorded_bank_sha256':sha(bank),'original_backup_equals_old_tracked_bytes':saved==blob(OLD,sp),'staged_state_equals_incoming_dev':blob(TREE,sp)==blob(BASE,sp),'incoming_state_equals_old_tracked_bytes':blob(BASE,sp)==blob(OLD,sp),'original_readings_count':len(original),'recorded_bank_readings_count':len(recorded),'original_records_absent_from_rolling_bank_but_safe_in_original_backup_and_restored_state':len(a-b),'new_records_saved_in_external_bank':len(b-a),'original_and_recorded_banks_both_retained':True,'scope':'Preservation of this specific STATE operation; rolling-bank record counts are not run-leg counts.'}
p=R/'latest-dev-smoke-post-restart-binding.json'
if p.is_file():
 old_binding=json.loads(p.read_bytes());result['old_source_smoke_bank']={'head':old_binding.get('head'),'tree':old_binding.get('tree'),'status':old_binding.get('status'),'verified_pass_leg_count':sum(x.get('verified_pass') is True for x in old_binding.get('completed',[])),'active':old_binding.get('active'),'note':'Historical old-source results only. They do not validate this staged tree.'}
result['fresh_validation_required']=True;result['limitations']=['Audits the pinned staged merge only; no app commit or push is implied.','Incoming core renderer, generator, CI and test-harness changes require new canonical derivation/full preflight/browser matrix; old source passes are not transferred.','No heavy tests, app writes, network requests, process signals or restarts were performed.']
protected_incoming={p for p in incoming if ('/assets/' in p or '/data/' in p) and p!='chicago/4d/data/liberties.json'}
result['protected_incoming_asset_and_data_path_count']=len(protected_incoming)
result['changed_protected_incoming_asset_and_data_paths']=sorted(protected_incoming&vs_base)
status_old=blob(OLD,'chicago/4d/docs/STATUS.md');status_new=blob(TREE,'chicago/4d/docs/STATUS.md')
heading=b'## T-3083 / T-3086 / T-3087'
start=status_old.find(heading)
if start>=0:
 end=status_old.find(b'\n## ',start+len(heading));section=status_old[start:end if end>=0 else len(status_old)]
 result['old_complete_transport_status_section']={'bytes':len(section),'retained_byte_exact':section in status_new}
result['old_source_smoke_bank']['binding_file']='latest-dev-smoke-post-restart-binding.json'
for label in ['latest-dev-smoke-desktop-12-after-runtime-restart','latest-dev-smoke-desktop-13']:
 rr=json.loads((R/(label+'.result.json')).read_bytes());cc=json.loads((R/(label+'.cleanup.json')).read_bytes())
 result.setdefault('old_source_terminal_leg_receipts',{})[label]={'returncode':rr.get('returncode'),'seconds':rr.get('seconds'),'cleanup_complete':cc.get('cleanup_complete'),'remaining_owned_children':len(cc.get('remaining_owned_children',[])),'note':'Recorded result only. Desktop13 return130 is not a pass; root intentionally stopped that owned run before merging new DEV.'}
print(json.dumps(result,indent=2))
