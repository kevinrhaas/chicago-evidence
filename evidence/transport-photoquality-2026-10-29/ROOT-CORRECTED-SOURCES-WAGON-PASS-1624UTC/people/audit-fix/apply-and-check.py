import json,hashlib,subprocess,time,os,shutil
from pathlib import Path
R=Path('/tmp/chicago-transport-resume-20261029');A=R/'chicago/4d';O=Path(__file__).resolve().parent;P=A/'data/research/check_gate_baseline.json';F=Path('/workspace/.cloud-setup/logs/transport-recovery/T1789-CHECKED-W-INTAKE-20261029/FROZEN-CHECKED-W-SOURCE15.json');B=json.loads(F.read_text());oldbytes=P.read_bytes();old=json.loads(oldbytes);(O/'ORIGINAL-CHECK-GATE-BASELINE.json').write_bytes(oldbytes)
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def guard():
 assert git('rev-parse','HEAD').decode().strip()==B['HEAD']and not git('ls-files','-u')
 for row in B['source_paths']:
  data=(R/row['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256']and data==git('show',':'+row['path'])
guard();assert len(old['ungated'])==10 and all(r['tool']!='tools/human_delivery.py'for r in old['ungated'])
reason=('This Actions-only delivery orchestrator has no --check option: its argparse interface accepts only guard, bundle, artifact, install, metadata, gate and commit. The survey matches literal --check arguments forwarded to existing native child validators, not an ungated local derivation. Its real gate mode requires the exact trusted manual workflow/repository/feature ref, current successful producer artifact and installed canonical family; it runs complete required-reader preflight before a sealed normal feature-only push. It cannot be invoked as a generic offline --check without that run context. Run tools/test_human_delivery.py for the eleven local trust/path/history/native-schema controls; the optional delivery job requires those controls before any artifact installation, and native canonical generation plus all-asset browser qualification remain separate required workflow steps. T-1789 owns actual generated-family delivery and its remaining acceptance.')
old['ungated'].append(dict(tool='tools/human_delivery.py',other_modes_in_check_sh=[],why_not_gated=reason,owner_ticket='T-1789'));P.write_text(json.dumps(old,indent=2)+'\n')
env=dict(os.environ,TMPDIR='/tmp/p29s',PYTHONDONTWRITEBYTECODE='1');env.pop('GIT_NO_LAZY_FETCH',None);rows=[]
for label,args in [('NATIVE-AUDIT-WRITE',['python3','tools/audit_check_gates.py','--write']),('NATIVE-AUDIT-GATE',['python3','tools/audit_check_gates.py','--gate','--quiet']),('NATIVE-AUDIT-SELFTEST',['python3','tools/audit_check_gates.py','--self-test']),('EXISTING-11-DELIVERY-CONTROLS',['python3','tools/test_human_delivery.py']),('NATIVE-SOURCEUSE-CHECK',['python3','tools/compile_source_use.py','--check'])]:
 guard();t=time.monotonic()
 with(O/(label+'.log')).open('wb',buffering=0)as log:q=subprocess.run(args,cwd=A,env=env,stdout=log,stderr=subprocess.STDOUT)
 row=dict(label=label,command=args,returncode=q.returncode,seconds=time.monotonic()-t);rows.append(row);(O/'COMMANDS.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(row),flush=True);assert q.returncode==0,row;guard()
new=json.loads(P.read_text());old=json.loads(oldbytes);by={r['tool']:r for r in new['ungated']};assert all(by[r['tool']]==r for r in old['ungated']);assert[r for r in new['ungated']if r['tool']!='tools/human_delivery.py']==old['ungated'];assert len(new['ungated'])==11
assert all(new[k]==v for k,v in old.items()if k not in('counts','ungated'))
assert new['counts']==dict(check_capable=336,gated=325,ungated=11),new['counts']
changed=git('diff','--name-only').decode().splitlines();assert changed==['chicago/4d/data/research/check_gate_baseline.json'],changed
subprocess.run(['git','add','--',*changed],cwd=R,check=True);guard();assert not git('diff','--name-only');assert len(git('diff','--cached','--name-only').decode().splitlines())==18
j=dict(result='PASS targeted documented audit inventory classification; audit/native assertions unchanged',original_fullpreflight='NONPASS1/886.937s with2/1105 actualstep failures retained',old_rows10_exact=True,new_row='tools/human_delivery.py',owner_ticket='T-1789',counts=new['counts'],commands=rows,SourceUse_fresh_no_tail_rerun=True,authored_source15_unchanged=True,new_authored16th_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),TREE=git('write-tree').decode().strip(),tmp_free=shutil.disk_usage('/tmp').free,next='Reseal16authored18total and fresh complete preflight; no commit/push')
(O/'RESULT.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j),flush=True)
