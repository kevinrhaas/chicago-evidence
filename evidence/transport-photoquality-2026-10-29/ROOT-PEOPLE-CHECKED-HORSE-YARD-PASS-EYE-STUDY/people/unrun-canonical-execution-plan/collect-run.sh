#!/usr/bin/env bash
# Read-only network collection, outside the app. No inferred IDs or name-only download.
set -euo pipefail
family=${1:?Usage: collect-run.sh dress|teamsters expected-source actual-run-id output-dir}
people_source=${2:?expected-source}
people_run=${3:?actual-run-id}
people_out=${4:?new persistent output-dir}
test "$family" = dress || test "$family" = teamsters
mkdir "$people_out"
gh api "repos/kevinrhaas/chicago/actions/runs/$people_run" > "$people_out/run.json"
people_attempt=$(python3 - "$people_out/run.json" "$people_source" "$family" <<'PY'
import json,sys
j=json.load(open(sys.argv[1]));assert j['head_sha']==sys.argv[2]
assert j['event']=='workflow_dispatch' and j['head_branch']=='steward/t1789-people-photoquality-20261026'
assert j['path']=='.github/workflows/chicago-4d-humans.yml'
assert j['repository']['full_name']==j['head_repository']['full_name']=='kevinrhaas/chicago'
assert not j['head_repository']['fork'] and j['status']=='completed' and j['conclusion']=='success'
print(j['run_attempt'])
PY
)
gh api "repos/kevinrhaas/chicago/actions/runs/$people_run/attempts/$people_attempt/jobs?per_page=100" > "$people_out/jobs.json"
gh api "repos/kevinrhaas/chicago/actions/runs/$people_run/artifacts?per_page=100" > "$people_out/artifacts.json"
python3 - "$people_out" "$family" "$people_source" "$people_run" "$people_attempt" <<'PY'
import json,pathlib,sys
o=pathlib.Path(sys.argv[1]);family,source,run,attempt=sys.argv[2:]
jobs=json.loads((o/'jobs.json').read_text());assert jobs['total_count']<=100
found={j['name']:j for j in jobs['jobs']}
producer='dress-study'if family=='dress'else'teamster-studies'
other='teamster-studies'if family=='dress'else'dress-study'
for n in ('humans',producer,'deliver-canonical-family'):assert found[n]['conclusion']=='success',(n,found[n]['conclusion'])
assert found[other]['conclusion']=='skipped'
names={'bundle':f'human-delivery-{family}-{run}-{attempt}','closure':f'human-delivery-closure-{run}-{attempt}'}
if family=='dress':names['study']=f'resident-dress-study-{source}'
else:
 names['study']=f'resident-teamster-studies-{source}'
 names['stills']=f'resident-teamster-blender-stills-{source}'
catalog=json.loads((o/'artifacts.json').read_text());assert catalog['total_count']<=100
rows=[]
for label,name in names.items():
 matches=[a for a in catalog['artifacts']if a['name']==name and not a['expired']]
 assert len(matches)==1,(name,len(matches));rows.append((label,matches[0]['id']))
(o/'exact-artifact-ids.tsv').write_text(''.join(f'{label}\t{aid}\n'for label,aid in rows))
PY
while IFS=$'\t' read -r people_label people_artifact; do
  gh api "repos/kevinrhaas/chicago/actions/artifacts/$people_artifact" > "$people_out/$people_label-artifact.json"
  gh api "repos/kevinrhaas/chicago/actions/artifacts/$people_artifact/zip" > "$people_out/$people_label.zip"
done < "$people_out/exact-artifact-ids.tsv"
gh run view "$people_run" --repo kevinrhaas/chicago --attempt "$people_attempt" --log > "$people_out/run.log"
printf 'Collected actual run/attempt jobs and exact-ID archives. Review CANONICAL-SEQUENCE.md before same-tree followup.\n'
