"""HELD recipe only: explicit execution flag, fixed-old-owner CAS; never overwrites a new owner or retries."""
import argparse,datetime,json,os,pathlib,secrets,subprocess
EXPECTED='234f1ccdd2aa49803718851cb16b675ab35383cb';REF='refs/heads/lap/pr-1175';REPO='/workspace/chicago'
def main():
 p=argparse.ArgumentParser();p.add_argument('--renew-owned-marker',action='store_true');a=p.parse_args();assert a.renew_owned_marker,'HELD: recipe only; no reads or mutations without explicit execution flag'
 out=pathlib.Path(__file__).resolve().parent/'RENEWAL-ACTUAL-ONCE';out.mkdir(exist_ok=False)
 def run(name,args,**kwargs):
  r=subprocess.run(args,capture_output=True,timeout=45,**kwargs);(out/(name+'.stdout')).write_bytes(r.stdout);(out/(name+'.stderr')).write_bytes(r.stderr);assert r.returncode==0,'Refused/ambiguous '+name+': preserve and STOP, no retry';return r.stdout
 def api(name,route):return json.loads(run(name,['gh','api','--method','GET','repos/kevinrhaas/chicago/'+route]))
 assert api('BEFORE-REF','git/ref/heads/lap/pr-1175')['object']['sha']==EXPECTED,'Different owner: STOP'
 old=api('BEFORE-COMMIT','git/commits/'+EXPECTED);assert old['tree']['sha']=='4b825dc642cb6eb9a060e54bf8d69288fbee4904' and old['parents']==[] and 'nonce: a9ca9f017c0f0d909c79cc696208e0f472fbfc441d99350f'in old['message'],'Owned marker contents differ: STOP'
 at=datetime.datetime.now(datetime.timezone.utc).isoformat();nonce=secrets.token_hex(24);message='lap PR #1175 — root continued ownership; source476 saved, desktop14 actual budget failure held '+at+'\nnonce: '+nonce+'\nrenewed-from: '+EXPECTED
 env=os.environ.copy();env.update(GIT_AUTHOR_NAME=env.get('GIT_AUTHOR_NAME')or'polecat-steward',GIT_AUTHOR_EMAIL=env.get('GIT_AUTHOR_EMAIL')or'steward@polecat.live',GIT_COMMITTER_NAME=env.get('GIT_COMMITTER_NAME')or'polecat-steward',GIT_COMMITTER_EMAIL=env.get('GIT_COMMITTER_EMAIL')or'steward@polecat.live',GIT_AUTHOR_DATE=at,GIT_COMMITTER_DATE=at)
 tree=run('EMPTY-TREE',['git','-C',REPO,'hash-object','-w','-t','tree','/dev/null']).decode().strip();assert tree=='4b825dc642cb6eb9a060e54bf8d69288fbee4904'
 new=run('NEW-COMMIT',['git','-C',REPO,'commit-tree',tree,'-m',message],env=env).decode().strip();assert len(new)==40 and new!=EXPECTED
 (out/'NEW-MARKER-PRE-PUSH.json').write_text(json.dumps({'new':new,'expected_old':EXPECTED,'ref':REF,'at':at,'message':message,'app_source_edit':False,'approval':'root explicit execution required'},indent=2)+'\n')
 run('CAS-PUSH',['git','-C',REPO,'push','origin',new+':'+REF,'--force-with-lease='+REF+':'+EXPECTED])
 actual=api('AFTER-REF','git/ref/heads/lap/pr-1175');assert actual['object']['sha']==new,'Actual marker differs: STOP, no retry'
 result={'renewed_old':EXPECTED,'actual_new':new,'ref':REF,'utc':at,'atomic_fixed_old_owner_CAS':True,'retries':0,'overwriting_new_owner':False,'app_source_edit':False,'next_step':'Rebind all future final merge/release lease constants to actual_new; retain old marker receipt. No CI dispatch implied.'}
 (out/'RENEWAL-RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
