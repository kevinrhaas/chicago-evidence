from pathlib import Path
import hashlib, importlib.util, json, os, subprocess, sys

R=Path('/tmp/chicago-town-transport-20261103-recovered'); A=R/'chicago/4d'
D=Path(__file__).parent/'RESOLVED-5918'; D.mkdir(exist_ok=False)
P=Path('/dev/shm/TRANSPORT-DEV-RECOVERY-READONLY-20261103')
H='1b1db388e4965a852f660a4fda2b5f467a97b907'; N='5918d14dfb9884c41c57d74d24faeef6f583ed9c'; B='ce91e60c6b283e318a4eaad0ce2c40769383ade0'
def git(*args): return subprocess.check_output(['git','-c','gc.auto=0','-c','maintenance.auto=false','-C',str(R),*args],timeout=30)
def val(*args): return git(*args).decode().strip()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,obj): (D/name).write_text(json.dumps(obj,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('guard',Path(__file__).parent/'resource_guard.py'); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
assert val('rev-parse','HEAD')==H and val('rev-parse','MERGE_HEAD')==N
assert sha('/workspace/chicago/.git/index')=='5a756f54205c7c2880065a6b5b8c50bf7cccdf56b297d734360f1f2542d580c5'
docs=['chicago/4d/docs/'+n for n in ['LIBERTIES.md','ROADMAP.md','STATUS.md']]
generated=['chicago/4d/data/liberties.json','chicago/4d/docs/measurements/source_use_coverage.md']
assert set(val('diff','--name-only','--diff-filter=U').splitlines())==set(docs+generated)
assert sha(A/'renderers/web/js/main.js')==sha(P/'MAIN-CLEAN-REVIEWED-PROPOSAL.js')
for rel in docs:
    proposed=P/(Path(rel).name+'.OURS-THEN-DEV-REVIEWED')
    body=proposed.read_bytes(); assert b'<<<<<<< ' not in body and b'>>>>>>> ' not in body
    (R/rel).write_bytes(body)
git('checkout','--ours','--',*generated);git('add','--',*docs,*generated)
manifest=json.loads((A/'tools/derived_manifest.json').read_text())
commands=[['python3','tools/compile_liberties.py'],['python3','tools/compile_source_use.py']]
owners=[row for row in manifest['steps'] if row['command'] in commands];assert len(owners)==2
allowed={p for row in owners for p in row['resolves']}; ledger=[]
for command in commands+[cmd+['--check'] for cmd in commands]:
    before=g.snapshot();assert g.check(before)['accepted']
    prefix=D/('owner-'+str(len(ledger)+1))
    q=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(A),'--timeout','120','--',*command],stdout=(Path(str(prefix)+'.stdout')).open('xb'),stderr=subprocess.STDOUT)
    result=json.loads(Path(str(prefix)+'.result.json').read_text());cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text());resources=g.pair(before,g.snapshot())
    ledger.append(dict(command=command,result=result,cleanup=cleanup,resources=resources));save('LEDGER.json',ledger)
    assert q.returncode==result['returncode']==0 and not result['timed_out'] and result['effective_timeout_seconds']==120 and result['timeout_override_reason'] is None and cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted']
assert json.loads((A/'data/liberties.json').read_text())['count']==983
assert set(val('diff','--name-only').splitlines())<=allowed
git('add','--',*sorted(allowed));assert not git('diff','--name-only').strip() and not git('ls-files','-u').strip()
T=val('write-tree')
def entries(ref):
    out={}
    for row in git('ls-tree','-rz',ref).split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);out[path.decode()]=meta.decode()
    return out
base,own,incoming,current=map(entries,[B,H,N,T]);op={p for p in base.keys()|own.keys() if base.get(p)!=own.get(p)};ip={p for p in base.keys()|incoming.keys() if base.get(p)!=incoming.get(p)}
exceptions=allowed|set(docs)|{'chicago/4d/renderers/web/js/main.js'}
assert all(current.get(p)==own.get(p) for p in op-ip-exceptions)
assert all(current.get(p)==incoming.get(p) for p in ip-op-exceptions)
assert all(current.get(p)==base.get(p) for p in (base.keys()|current.keys())-(op|ip|exceptions))
source=dict(HEAD=H,MERGE_HEAD=N,TREE=T,APP=val('rev-parse',T+':chicago/4d'),semantic_index_sha256=hashlib.sha256(git('ls-files','--stage','-z')).hexdigest())
save('CLOSED.json',dict(status='NORMAL_DEV_ROLLFORWARD_NATIVE_OWNERS_PASS_FULL_GATE_NOT_RUN',source_after=source,own_paths=len(op),incoming_paths=len(ip),all_own_and_incoming_nonoverlap_blobs_modes_exact=True,expected_liberties=983,ledger=ledger))
print(json.dumps(source))
