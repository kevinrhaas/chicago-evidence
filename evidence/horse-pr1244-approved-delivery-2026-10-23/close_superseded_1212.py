import pathlib,json,sys,os
sys.path.insert(0,'/workspace/shared');import owned_child_reaper_20261023 as o
b=pathlib.Path(__file__).parent;d=b/'CLOSE-SUPERSEDED-1212';d.mkdir(exist_ok=False);o.enable()
def api(n,route,method='GET',body=None):
 args=['gh','api','--method',method,'repos/kevinrhaas/chicago/'+route]
 if body is not None:
  p=d/(n+'-request.json');p.write_text(json.dumps(body));args+=['--input',str(p)]
 f=d/(n+'.json');v=o.run(args,'/workspace/chicago-waistcoat',os.environ.copy(),f,90);assert v['returncode']==0;return json.loads(f.read_text())
try:
 m=api('merged-replacement','pulls/1244');assert m['merged'] and m['merge_commit_sha']=='fa115d72534e234fe5ac7b94fd2f1a3eb38065c8' and m['base']['ref']=='dev'
 p=api('old-draft','pulls/1212');assert p['base']['ref']=='dev' and p['head']['repo']['full_name']=='kevinrhaas/chicago' and not p['merged']
 if p['state']=='open':
  assert p['draft'],'Old horse draft no longer draft; review before closing'
  text=(p['body']or'')+'\n\n## Superseded — 2026-10-23\n\nClosed after replacement #1244 merged normally to DEV as fa115d72534e234fe5ac7b94fd2f1a3eb38065c8 with fresh green gate, moving-frame/phone and report checks. Replacement uses a redesigned planted standing clip and consumer; this is supersession, not a claim of byte containment. Historical receipts in this draft remain preserved. T-2800/T-2803 stay open for photographic refinement and full gait/gear/teams/riding acceptance.\n'
  assert len(text)<65000
  api('closed-as-superseded','pulls/1212','PATCH',{'state':'closed','body':text})
 actual=api('verify-closed','pulls/1212');assert actual['state']=='closed' and not actual['merged']
 (d/'TERMINAL.json').write_text(json.dumps({'status':'CLOSED_SUPERSEDED_DRAFT','PR':1212,'replacement_PR':1244,'replacement_DEV_merge':'fa115d72534e234fe5ac7b94fd2f1a3eb38065c8','byte_containment_claim':False},indent=2)+'\n');print('Closed superseded horse draft1212; broad acceptance remains open',flush=True)
finally:(d/'OWNED-CLEANUP.json').write_text(json.dumps(o.finish()))
