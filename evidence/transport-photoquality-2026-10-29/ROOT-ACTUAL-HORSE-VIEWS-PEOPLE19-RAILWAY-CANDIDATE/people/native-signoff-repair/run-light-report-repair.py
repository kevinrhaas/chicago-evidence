import os,json,hashlib,subprocess,time,shutil,importlib.util
from pathlib import Path
R=Path('/tmp/chicago-transport-resume-20261029');A=R/'chicago/4d';O=Path(__file__).resolve().parent;F=Path('/workspace/.cloud-setup/logs/transport-recovery/T1789-AUDIT-INVENTORY-FIX-20261029/FROZEN-AUTHORED16-SOURCE.json');B=json.loads(F.read_text());REPORT=A/'docs/RESEARCH/research-signoff-2026-09.md';old=REPORT.read_bytes();(O/'BEFORE-RESEARCH-SIGNOFF.md').write_bytes(old)
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def guard():
 assert git('rev-parse','HEAD').decode().strip()==B['HEAD']and not git('ls-files','-u')
 for row in B['source_paths']:
  data=(R/row['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256']and data==git('show',':'+row['path'])
guard();assert not git('diff','--name-only')
# Read native ownership and direct dependency facts; do not invent a full-tail need.
manifest=json.loads((A/'tools/derived_manifest.json').read_text());in_manifest=[s['command']for s in manifest['steps']if any('report_research_signoff.py'in t for t in s['command'])];assert in_manifest==[['python3','tools/report_research_signoff.py','--build']]
readers=[]
for p in(A/'tools').glob('*.py'):
 text=p.read_text(errors='replace')
 if 'research-signoff-2026-09.md'in text:readers.append(p.relative_to(A).as_posix())
assert readers==['tools/report_research_signoff.py'],readers
source=(A/'tools/report_research_signoff.py').read_text();assert 'check_gate_baseline.json'in source
commands=[];env=dict(os.environ,TMPDIR='/tmp/p29s',PYTHONDONTWRITEBYTECODE='1');env.pop('GIT_NO_LAZY_FETCH',None)
for label,args in [('NATIVE-REPORT-BUILD',['python3','tools/report_research_signoff.py','--build']),('NATIVE-REPORT-CHECK',['python3','tools/report_research_signoff.py','--check','--quiet']),('NATIVE-REPORT-SELFTEST',['python3','tools/report_research_signoff.py','--self-test']),('NATIVE-SOURCEUSE-CHECK',['python3','tools/compile_source_use.py','--check']),('NATIVE-CLOSING-AUDIT-CHECK',['python3','tools/report_research_closing_audit.py','--check','--quiet']),('NATIVE-CLOSING-SET-CHECK',['python3','tools/rebuild_closing_set.py','--check','--quiet'])]:
 guard();start=time.monotonic()
 with(O/(label+'.log')).open('wb',buffering=0)as f:q=subprocess.run(args,cwd=A,env=env,stdout=f,stderr=subprocess.STDOUT)
 row=dict(label=label,command=args,returncode=q.returncode,seconds=time.monotonic()-start);commands.append(row);(O/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n');print(json.dumps(row),flush=True);assert q.returncode==0,row;guard()
changed=git('diff','--name-only').decode().splitlines();assert changed==['chicago/4d/docs/RESEARCH/research-signoff-2026-09.md'],changed
diff=git('diff','--',changed[0]);(O/'ACTUAL-NATIVE-REPORT.diff').write_bytes(diff)
new=REPORT.read_bytes();assert b'**362**'in new or b'362'in new;assert b'human_delivery.py'in new
subprocess.run(['git','add','--',*changed],cwd=R,check=True);guard();assert not git('diff','--name-only');paths=git('diff','--cached','--name-only').decode().splitlines();assert len(paths)==19
j=dict(result='PASS light native report rebuild/check/selftest and affected downstream checks; FULLGATE HOLD for H slot',HEAD=B['HEAD'],TREE=git('write-tree').decode().strip(),authored16_exact=True,total_staged_paths=19,native_report_sha256=hashlib.sha256(new).hexdigest(),old_report_sha256=hashlib.sha256(old).hexdigest(),commands=commands,dependency=dict(report_has_native_build_check=True,native_manifest_step=197,only_direct_Python_reader=readers,reads_audit_inventory=True,SourceUse_fresh_no_tail_rerun=True),source_code_or_assertions_edited=False,next='Wait ROOT heavyGO then fresh fullpreflight; no commit/push')
(O/'RESULT.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j),flush=True)
