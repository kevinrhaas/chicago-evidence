import subprocess,json,os,time,hashlib
from pathlib import Path
R=Path('/tmp/chicago-transport-resume-20261029');A=R/'chicago/4d';O=Path(__file__).resolve().parent
BASE='9e14c138848ef854a535271fbd3feaae52dd4aa2';TREE='e873ea8531ab1a8f8bb74434976ace6234c3d6e6';BRANCH='steward/t1789-people-photoquality-20261026'
env=dict(os.environ,C4D_GATE_REQUIRE_BASE='1',PYTHONDONTWRITEBYTECODE='1');env.pop('GIT_NO_LAZY_FETCH',None)
def g(*args):return subprocess.check_output(['git',*args],cwd=R,env=env,text=True).strip()
def save(name,data):(O/name).write_text(json.dumps(data,indent=2)+'\n')
def remote():
 lines=g('ls-remote','origin','refs/heads/'+BRANCH).splitlines();assert len(lines)==1,lines
 sha,ref=lines[0].split();assert ref=='refs/heads/'+BRANCH;return sha
assert g('rev-parse','HEAD')==BASE and g('write-tree')==TREE and g('branch','--show-current')==BRANCH
assert not g('diff','--name-only') and not g('ls-files','-u')
assert len(g('diff','--cached','--name-only').splitlines())==19
b=json.loads(Path('/workspace/.cloud-setup/logs/transport-recovery/T1789-SIGNOFF-REPORT-REPAIR-20261029/FROZEN-19-SOURCE-BINDING.json').read_text())
for row in b['all_staged_paths']:assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256']
pre=remote();g('fetch','--no-tags','origin',pre);subprocess.run(['git','merge-base','--is-ancestor',pre,BASE],cwd=R,env=env,check=True)
save('BEFORE.json',dict(BASE=BASE,TREE=TREE,branch=BRANCH,remote_before=pre,staged_paths=19,source19_exact=True))
with (O/'COMMIT.log').open('w') as log:subprocess.run(['git','commit','-m','T-1789: add optional people finishing and guarded source delivery'],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
HEAD=g('rev-parse','HEAD');assert g('rev-parse','HEAD^{tree}')==TREE and not g('status','--porcelain')
checks=[('CHANGELOG-ENTRY',['node','tools/check-changelog-entry.mjs',BASE,HEAD]),('ID-COLLISION',['node','tools/resolve_id_collisions.mjs','--base',BASE,'--check']),('FOLDED-CHANGELOG-FORMAT',['node','tools/check-changelog.mjs']),('SHIPPED-HISTORY',['node','tools/changelog-history.mjs','--base',BASE])]
rows=[]
for label,args in checks:
 t=time.monotonic()
 with(O/(label+'.log')).open('w')as log:p=subprocess.run(args,cwd=A,env=env,stdout=log,stderr=subprocess.STDOUT)
 row=dict(label=label,command=args,returncode=p.returncode,seconds=time.monotonic()-t);rows.append(row);save('CHECKS.json',rows);assert p.returncode==0,row
assert remote()==pre,'remote feature branch changed during checks'
subprocess.run(['git','merge-base','--is-ancestor',pre,HEAD],cwd=R,env=env,check=True)
assert g('rev-parse','HEAD')==HEAD and g('rev-parse','HEAD^{tree}')==TREE and not g('status','--porcelain')
with(O/'PUSH.log').open('w')as log:subprocess.run(['git','push','origin','HEAD:refs/heads/'+BRANCH],cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
post=remote();assert post==HEAD and not g('status','--porcelain')
save('RESULT.json',dict(result='PASS normal checked source-feature commit and push',HEAD=HEAD,BASE=BASE,TREE=TREE,APP=g('rev-parse','HEAD:chicago/4d'),branch=BRANCH,remote_before=pre,remote_after=post,remote_exact=True,clean=True,checks=rows,limits='Source feature only. No canonical generated humans, PR ready, DEV merge or workflow dispatch.'))
print((O/'RESULT.json').read_text(),flush=True)
