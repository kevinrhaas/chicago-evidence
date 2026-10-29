import os,json,hashlib,subprocess,importlib.util,shutil
from pathlib import Path
R=Path('/tmp/chicago-transport-resume-20261029');A=R/'chicago/4d';O=Path(__file__).resolve().parent;P=A/'data/research/check_gate_baseline.json';F=Path('/workspace/.cloud-setup/logs/transport-recovery/T1789-CHECKED-W-INTAKE-20261029/FROZEN-CHECKED-W-SOURCE15.json');B=json.loads(F.read_text())
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
assert git('rev-parse','HEAD').decode().strip()==B['HEAD']and not git('ls-files','-u')
for row in B['source_paths']:
 data=(R/row['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256']and data==git('show',':'+row['path'])
rows=json.loads((O/'COMMANDS.json').read_text());assert len(rows)==5 and all(r['returncode']==0 for r in rows)
old=json.loads((O/'ORIGINAL-CHECK-GATE-BASELINE.json').read_text());new=json.loads(P.read_text());oldmap={r['tool']:r for r in old['ungated']};newmap={r['tool']:r for r in new['ungated']}
assert set(newmap)-set(oldmap)=={'tools/human_delivery.py'}and all(newmap[k]==v for k,v in oldmap.items())
assert[r for r in new['ungated']if r['tool']!='tools/human_delivery.py']==old['ungated']
assert all(new[k]==v for k,v in old.items()if k not in('counts','ungated'))
spec=importlib.util.spec_from_file_location('native_audit',A/'tools/audit_check_gates.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);found=m.survey();counts=dict(check_capable=len(found['check_capable']),gated=len(found['check_capable'])-len(found['ungated']),ungated=len(found['ungated']))
assert new['counts']==counts and counts['ungated']==11,(new['counts'],counts)
assert not m.verdicts(found['ungated'],m.by_tool(new))and not m.borrowed_verdicts()
changed=git('diff','--name-only').decode().splitlines();assert changed==['chicago/4d/data/research/check_gate_baseline.json'],changed
subprocess.run(['git','add','--',*changed],cwd=R,check=True);assert not git('diff','--name-only')and len(git('diff','--cached','--name-only').decode().splitlines())==18
source=B['source_paths']+[dict(path=changed[0],bytes=P.stat().st_size,sha256=hashlib.sha256(P.read_bytes()).hexdigest(),new_supported_inventory_classification=True)]
tree=git('write-tree').decode().strip();app=git('rev-parse',tree+':chicago/4d').decode().strip()
S=dict(HEAD=B['HEAD'],TREE=tree,APP=app,source_paths=source,source_count=16,total_staged_paths=18,first15_exact=True,baseline_existing10rows_exact=True,native_assertions_and_tools_unchanged=True,inventory_counts_current=counts)
(O/'FROZEN-AUTHORED16-SOURCE.json').write_text(json.dumps(S,indent=2)+'\n')
result=dict(result='PASS targeted documented inventory row and all native affected controls; fullpreflight rerun still required',HEAD=B['HEAD'],TREE=tree,APP=app,counts=counts,old_stale_counts=old['counts'],old10rows_exact=True,native_commands=rows,authored16_total18=True,original_full_failure_preserved=True,external_summary_guard_failure_preserved=True,SourceUse_check0_no_tail_rerun=True,tmp_free=shutil.disk_usage('/tmp').free)
(O/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
