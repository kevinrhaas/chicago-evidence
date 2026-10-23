#!/usr/bin/env python3
"""Read-only exact-commit push/PR trigger pricing; no workflow invocation."""
import argparse,hashlib,json,os,pathlib,re,subprocess,yaml
ROOT=pathlib.Path('/workspace/chicago');BRANCH='steward/parked-period-vehicles-20261021'
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a],env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
def sha(b):return hashlib.sha256(b).hexdigest()
def match(value,pattern):
 # Current workflow filters use literals,* or **. Unknown minimatch syntax stops.
 if any(c in pattern for c in '[]+?{}\\'):raise ValueError('Unsupported workflow glob; inspect '+pattern)
 return bool(re.fullmatch(re.escape(pattern).replace(r'\*\*','.*').replace(r'\*','[^/]*'),value))
def accepts(value,patterns):
 selected=False
 for p in patterns:
  negative=p.startswith('!');p=p[1:] if negative else p
  if match(value,p):selected=not negative
 return selected
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sha',required=True);p.add_argument('--push-base',default='0a037632481037dcc903fa11697da5681b519f80');p.add_argument('--pr-base',default='origin/dev');a=p.parse_args()
assert re.fullmatch('[0-9a-f]{40}',a.sha)
head=git('rev-parse',a.sha).decode().strip();pushbase=git('rev-parse',a.push_base).decode().strip();prbase=git('rev-parse',a.pr_base).decode().strip();mb=git('merge-base',prbase,head).decode().strip()
pushfiles=git('diff','--name-only',pushbase,head).decode().splitlines();prfiles=git('diff','--name-only',mb,head).decode().splitlines();paths=git('ls-tree','-r','--name-only',head,'.github/workflows').decode().splitlines();workflows=[];predicted=[]
for path in paths:
 if not path.endswith(('.yml','.yaml')):continue
 raw=git('show',head+':'+path);d=yaml.load(raw,Loader=yaml.BaseLoader);events=d.get('on',{});assert isinstance(events,dict),'Inspect non-map workflow events: '+path
 for event,files,branch in [('push',pushfiles,BRANCH),('pull_request',prfiles,'dev')]:
  if event not in events:continue
  rule=events[event] or {};assert isinstance(rule,dict),'Inspect event rule: '+path
  ok=True
  if 'branches' in rule:ok=ok and accepts(branch,rule['branches'])
  if 'branches-ignore' in rule:ok=ok and not accepts(branch,rule['branches-ignore'])
  matched=files
  if 'paths' in rule:matched=[f for f in files if accepts(f,rule['paths'])];ok=ok and bool(matched)
  if 'paths-ignore' in rule:matched=[f for f in files if not accepts(f,rule['paths-ignore'])];ok=ok and bool(matched)
  item={'workflow_path':path,'workflow_sha256':sha(raw),'event':event,'branch_filter_value':branch,'rule':rule,'matches':matched,'predicted_trigger':bool(ok)};workflows.append(item)
  if ok:predicted.append({'path':path,'event':event})
expected=[{'path':'.github/workflows/chicago-4d-check.yml','event':'pull_request'},{'path':'.github/workflows/chicago-4d-moving-frames.yml','event':'pull_request'},{'path':'.github/workflows/chicago-4d-pr-stuck.yml','event':'push'}]
report={'repository':'kevinrhaas/chicago','branch':BRANCH,'sha':head,'tree':git('rev-parse',head+'^{tree}').decode().strip(),'push_base':pushbase,'pr_base':prbase,'pr_merge_base':mb,'push_diff_paths':pushfiles,'pr_diff_paths':prfiles,'workflow_trigger_pricing':workflows,'predicted_normal_runs':predicted,'expected_three_normal':sorted(predicted,key=str)==sorted(expected,key=str),'selected_manual_requests':18,'selected_cells':[[v,s] for v in ['desktop','mobile'] for s in ['1-2','3-4','5','6-7','8','9-12','13','14','15']],'manual_workflow':'.github/workflows/chicago-4d-smoke.yml','smoke_job_cap_minutes':150,'selected_runner_cap_minutes_upper_bound':2700,'price_scope':'Source-trigger/job-cap pricing, not predicted bill or runtime; current actual workflow runs must reconcile independently. No bake/canonical human/unfiltered smoke/production dispatch.','read_only':True,'POSTs':0}
print(json.dumps(report,indent=2))
