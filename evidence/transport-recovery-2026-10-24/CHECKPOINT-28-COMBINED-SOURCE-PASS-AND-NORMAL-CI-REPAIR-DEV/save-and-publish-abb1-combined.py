#!/usr/bin/env python3
import pathlib,json,subprocess,time,shutil,hashlib,re
ROOT=pathlib.Path('/workspace/chicago');LOG=pathlib.Path('/workspace/.cloud-setup/logs/transport-recovery');PREFIX='abb1-transport-ui-combined-preflight';TREE='4b2a7066a039936ddcc65d8c1c891fcf25dd7e5f'
git=lambda *a:subprocess.check_output(['git','-C',str(ROOT),*a],text=True).strip()
start=time.monotonic()
while not (LOG/(PREFIX+'.result.json')).exists():
 assert time.monotonic()-start<600,'No completed gate receipt within bounded wait'
 time.sleep(.5)
r=json.loads((LOG/(PREFIX+'.result.json')).read_text())
while not (LOG/(PREFIX+'.cleanup.json')).exists():
 assert time.monotonic()-start<600
 time.sleep(.1)
c=json.loads((LOG/(PREFIX+'.cleanup.json')).read_text())
assert r['returncode']==0 and not r['timed_out'] and c['cleanup_complete'] and not c['remaining_owned_children']
assert r['cwd']==str(ROOT/'chicago/4d') and r['command']==['bash','tools/preflight.sh']
assert git('rev-parse','HEAD')=='be56fb269eee6aa7963b8a8d76d5a950f56f857c'
assert git('rev-parse','MERGE_HEAD')=='abb1dd407a96cf64b9b04735cca432129342beb2'
assert git('write-tree')==TREE and not git('diff','--name-only')
for n in ['check','cl','ids']:
 dst=LOG/(PREFIX+'-'+n+'.log');assert not dst.exists();shutil.copyfile('/tmp/preflight-'+n+'.log',dst)
check=re.sub(r'\x1b\[[0-9;]*m','',(LOG/(PREFIX+'-check.log')).read_text(errors='replace'));assert 'CHECK PASS' in check and 'PREFLIGHT PASS' in (LOG/(PREFIX+'.log')).read_text(errors='replace')
subprocess.run(['git','-C',str(ROOT),'commit','-m','Merge DEV and wrap release notes in the Navigator (T-3125)'],check=True)
h=git('rev-parse','HEAD');assert git('rev-parse','HEAD^{tree}')==TREE and not git('status','--porcelain=v1')
b={'head':h,'tree':TREE,'app_subtree':git('rev-parse','HEAD:chicago/4d'),'parents':git('show','-s','--format=%P','HEAD').split(),'preflight_prefix':str(LOG/PREFIX),'preflight_seconds':r['seconds'],'preflight_result':r['returncode'],'cleanup_complete':c['cleanup_complete'],'remaining_owned_children':len(c['remaining_owned_children']),'tickets':['T-3083','T-3086','T-3087','T-3125'],'state':'Exact validated tree committed. Fresh browser matrix and wrapping checks pending. No DEV merge.'}
p=LOG/'abb1-transport-ui-committed-gate-binding.json';assert not p.exists();p.write_text(json.dumps(b,indent=2)+'\n');print(json.dumps(b),flush=True)
subprocess.run(['git','-C',str(ROOT),'push','origin','HEAD'],check=True)
subprocess.run(['python3','/workspace/.cloud-setup/transport-supervise.py','--prefix',str(LOG/'abb1-transport-ui-committed-head-publish'),'--cwd',str(ROOT/'chicago/4d'),'--timeout','600','--','bash','tools/publish.sh'],check=True)
