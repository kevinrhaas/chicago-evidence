"""Prepared native canonical owners; unchanged 120s per command."""
from pathlib import Path
import fcntl, hashlib, importlib.util, json, os, subprocess, sys

D = Path(__file__).resolve().parent
R = Path('/workspace/chicago-driver-motion-20261103'); A = R/'chicago/4d'
O = D/sys.argv[1]; O.mkdir(exist_ok=False)
lock = open('/workspace/.cloud-setup/transport-8cec-generated-lap-20261030/ROOT-SOLE-CANONICAL-OWNER.lock', 'a+')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
spec = importlib.util.spec_from_file_location('guard', '/workspace/.cloud-setup/transport-current-20261103/resource_guard.py')
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
def git(*args): return subprocess.check_output(['git','-C',str(R),*args],timeout=30)
def save(name,value): (O/name).write_text(json.dumps(value,indent=2)+'\n')
def sha(raw): return hashlib.sha256(raw).hexdigest()
manifest = json.loads((A/'tools/derived_manifest.json').read_text())
commands = [['python3','tools/compile_liberties.py'],['python3','tools/compile_source_use.py']]
resume = '--resume-owner-1' in sys.argv[2:]
prior = None
if resume:
    prior_path = D/'owners-01/CLOSED.json'
    prior = json.loads(prior_path.read_text())
    first = prior['ledger'][0]
    assert first['command'] == commands[0] and first['result']['returncode'] == 0
    assert first['result']['effective_timeout_seconds'] == first['result']['requested_timeout_seconds'] == 120
    assert not first['result']['timed_out'] and first['cleanup']['cleanup_complete'] and first['resources']['accepted']
    saved = json.loads((D/'owners-01/SOURCE-AFTER.json').read_text())
    for rel in ['docs/LIBERTIES.md','data/liberties.json','tools/compile_liberties.py','tools/readable_text.py']:
        assert sha((A/rel).read_bytes()) == saved['chicago/4d/'+rel]
owners = [row for row in manifest['steps'] if row['command'] in commands]
assert len(owners)==2
allowed = {p for row in owners for p in row['resolves']}
allowed.add('chicago/4d/tools/derived_manifest.json')
def snapshot():
    names = git('ls-files','-z').split(b'\0') + git('ls-files','--others','--exclude-standard','-z').split(b'\0')
    out={}
    for raw in names:
        if not raw: continue
        name=os.fsdecode(raw); p=R/name
        if p.is_symlink(): out[name]=sha(os.fsencode(os.readlink(p)))
        elif p.is_file(): out[name]=sha(p.read_bytes())
    return out
before=snapshot();save('SOURCE-BEFORE.json',before)
ledger=[];error=None
try:
    actual_commands = (commands[1:] if resume else commands) + [c+['--check']for c in commands]
    for i,command in enumerate(actual_commands,1):
        first=g.snapshot();assert g.check(first)['accepted'];prefix=O/('owner-'+str(i))
        q=subprocess.run([sys.executable,'/workspace/.cloud-setup/transport-supervise.py','--prefix',str(prefix),'--cwd',str(A),'--timeout','120','--',*command],stdout=(O/('owner-'+str(i)+'.stdout')).open('xb'),stderr=subprocess.STDOUT)
        result=json.loads(Path(str(prefix)+'.result.json').read_text());cleanup=json.loads(Path(str(prefix)+'.cleanup.json').read_text());resources=g.pair(first,g.snapshot())
        ledger.append(dict(command=command,result=result,cleanup=cleanup,resources=resources));save('LEDGER.json',ledger)
        assert q.returncode==result['returncode']==0 and not result['timed_out']
        assert result['effective_timeout_seconds']==result['requested_timeout_seconds']==120 and result['timeout_override_reason']is None
        assert cleanup['cleanup_complete'] and not cleanup['remaining_owned_children'] and resources['accepted']
except BaseException as e:error=repr(e)
after=snapshot();save('SOURCE-AFTER.json',after)
changed=sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p))
if not set(changed)<=allowed:error=(error or'')+' native owner changed a path outside its registered resolves'
save('CLOSED.json',dict(passed=error is None and len(ledger)==(3 if resume else 4),error=error,ledger=ledger,
                      resumes_actual_owner1_partial=str(D/'owners-01/CLOSED.json') if resume else None,
                      prior_owner1_closure_sha256=sha((D/'owners-01/CLOSED.json').read_bytes()) if resume else None,
                      allowed_resolves=sorted(allowed),actual_changed_paths=changed,all_other_actual_worktree_paths_exact=set(changed)<=allowed))
print(json.dumps(dict(passed=error is None,output=str(O),error=error,changed=changed)))
raise SystemExit(0 if error is None else 1)
