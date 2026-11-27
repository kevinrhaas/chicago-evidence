"""Verify the entire existing project gate before the actual source commit; browser release checks follow."""
import hashlib,json,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
w=Path('work');read=lambda name:json.loads((w/name).read_text());f=read('visual-photo-combined-fixture.json');d=read('visual-photo-combined-dispatch.json');sha=f['fixture_sha'];tree=f['tree']
assert d['qualification_fixture'] and d['source_sha']==sha and d['source_tree']==tree
assert subprocess.check_output(['git','write-tree'],text=True).strip()==tree
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==f['source_parent']
assert subprocess.run(['git','diff','--quiet']).returncode==0
assert subprocess.check_output(['git','rev-parse',sha+'^{tree}'],text=True).strip()==tree
state=read('visual-photo-current-ci.json');assert state['source_sha']==sha and state['source_tree']==tree and not state['bad']
local_path=w/'visual-photo-combined-local-complete-gate.json'
if local_path.exists():
 local=read(local_path.name)
 assert local['tree']==tree and local['fixture_sha']==sha and local['full_gate_covered'] and not local['failures']
 assert local['conditions']=={'CHECK_JOBS':2,'C4D_GATE_REQUIRE_READERS':1,'C4D_GATE_REQUIRE_BASE':1,'foreground_cap_seconds':600}
 residues=[];logs=[]
 for row in local['executed_parts']:
  k,n=row['k'],row['n'];assert row['exit_code']==0 and n in [16,32] and row['seconds']<605
  residues.extend([k,k+16]if n==16 else[k])
  p=Path(row['log']);raw=p.read_bytes();clean=re.sub(r'\x1b\[[0-9;]*m','',raw.decode('utf-8-sig'))
  verdict=re.findall(rf'CHECK PASS — part {k}/{n}: (\d+) steps, none red\.',clean);assert len(verdict)==1 and int(verdict[0])==row['steps']>0
  assert subprocess.check_output(['git','write-tree'],cwd=row['copy'],text=True).strip()==tree
  assert subprocess.run(['git','diff','--quiet'],cwd=row['copy']).returncode==0
  logs.append({**row,'log_sha256':hashlib.sha256(raw).hexdigest()})
 assert sorted(residues)==list(range(1,33)) and len(logs)==20
 proof=read('final-photo-writer-reproduction.json')
 for path,h in {**proof['inputs_sha256'],**proof['output_sha256']}.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h,path
 result={'qualification_fixture_sha':sha,'qualified_tree':tree,'entire_project_gate_parts':20,'project_gate_steps':sum(p['steps']for p in logs),'gate_logs':logs,'method':'Complete local unchanged gate; documented T3654 partition refinement covers every ordinal exactly once','coverage_residues_32':sorted(residues),'native_gate_and_required_readers_base_retained':True,'conditions':local['conditions'],'photo_outputs_verified':536,'verified_at':datetime.now(timezone.utc).isoformat(),'browser_and_auxiliary_checks_required_before_merge':True,'scope':'Complete unchanged check.sh before the actual source commit, as AGENTS.md requires. Full hosted desktop/mobile, project gate and auxiliary release checks still required before merging to dev.'}
 (w/'visual-photo-combined-precommit-gate.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS: entire unchanged local project gate on exact combined tree; source commit allowed, hosted release qualification still required before merge',flush=True)
 raise SystemExit(0)
gate_id=next(r['run_id']for r in d['auxiliary_runs']if r['name']=='Chicago 4D — gate');run=next(r for r in state['runs']if r['id']==gate_id);assert run['conclusion']in [None,'success'] and run['head_sha']==sha
gj=read('visual-photo-combined-gate-jobs.json');assert gj['source_sha']==sha and gj['source_tree']==tree and gj['run_id']==gate_id
parts=[];logs=[]
for j in gj['jobs']:
 m=re.fullmatch(r'gate part (\d+)/8',j['name'])
 if not m:continue
 k=int(m[1]);parts.append(k);assert j['conclusion']=='success' and j.get('head_sha',sha)==sha
 p=w/'visual-photo-hosted'/f"gate-part-{k}-of8-run-{gate_id}-job-{j['id']}.log";raw=p.read_bytes();text=raw.decode('utf-8-sig');clean=re.sub(r'\x1b\[[0-9;]*m','',text)
 assert sha in text
 verdict=re.findall(rf'CHECK PASS — part {k}/8: (\d+) steps, none red\.',clean);assert len(verdict)==1 and int(verdict[0])>0
 for name in ['C4D_GATE_REQUIRE_READERS','C4D_GATE_REQUIRE_BASE']:assert re.search(name+r':\s*1\s*$',text,re.M)
 assert re.search(r'timeout\s+--kill-after=5s\s+900s\s+\./tools/check\.sh\s+--part\s+[\"\x27]?'+str(k)+r'/8',clean)
 logs.append({'part':str(k)+'/8','job_id':j['id'],'steps':int(verdict[0]),'log':str(p),'log_sha256':hashlib.sha256(raw).hexdigest()})
assert sorted(parts)==list(range(1,9))
aggregate=[j for j in gj['jobs']if j['name']=='gate'];assert len(aggregate)==1 and aggregate[0]['conclusion']in [None,'success']
# Every unchanged check.sh part above has actually passed before this commit.
# The aggregate only reports those results; its green status remains mandatory
# in validate-combined-photo-qualification.py before any dev merge.
proof=read('final-photo-writer-reproduction.json')
for path,h in {**proof['inputs_sha256'],**proof['output_sha256']}.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h,path
result={'qualification_fixture_sha':sha,'qualified_tree':tree,'entire_project_gate_parts':8,'project_gate_steps':sum(p['steps']for p in logs),'gate_logs':logs,'native_gate_and_required_readers_base_retained':True,'photo_outputs_verified':536,'verified_at':datetime.now(timezone.utc).isoformat(),'browser_and_auxiliary_checks_required_before_merge':True,'aggregate_status_at_source_commit':{k:aggregate[0][k]for k in ['id','status','conclusion']},'aggregate_green_still_required_before_merge':True,'scope':'All eight unchanged check.sh parts passed before the actual source commit, as AGENTS.md requires. The reporting aggregate, full desktop/mobile and auxiliary release checks still must all be green before merging to dev.'}
(w/'visual-photo-combined-precommit-gate.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: entire unchanged8-partprojectgate on exact combined tree; actual source commit may now be created, with all browser/auxiliary checks still required before merge',flush=True)
