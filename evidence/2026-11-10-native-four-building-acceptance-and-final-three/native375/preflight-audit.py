#!/usr/bin/env python3
"""Exercise generic readers on actual pinned before objects; not a native acceptance."""
import datetime,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent;repo=Path('/tmp/chicago-west-wicket-20261109');b=json.load(open(r/'BEFORE-BINDING.json'))
spec=importlib.util.spec_from_file_location('audit',r/'audit-retained.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
controls=[];targets=[]
for x in b['affected']:
 raw=(repo/x['before_master']['path']).read_bytes();web=(repo/x['before_web_outputs'][0]['path']).read_bytes()
 if not x['intentional_geometry_target']:
  row=m.compare_control(x['asset_key'],raw,raw,web);assert row['master_bytes_identical'];controls.append(x['asset_key'])
 else:
  summary,*_=m.geometry_summary(raw);targets.append({'asset_key':x['asset_key'],'triangles':summary['triangles'],'primitives':summary['primitives']})
paths=list(b['source_files']);inp=''.join(b['captured_HEAD']+':'+p+'\n'for p in paths)
res=subprocess.run(['git','cat-file','--batch-check=%(objectname) %(objecttype)'],cwd=repo,input=inp,text=True,stdout=subprocess.PIPE,check=True)
assert all(not x.endswith(' missing')for x in res.stdout.splitlines())
receipt={'status':'PASS_READER_PREFLIGHT_NOT_NATIVE_ACCEPTANCE','pinned_HEAD':b['captured_HEAD'],'binding_sha256':hashlib.sha256((r/'BEFORE-BINDING.json').read_bytes()).hexdigest(),'actual_control_MASTER_readers_exercised':len(controls),'actual_variant_control_readers_exercised':sum(x.startswith('versions/')for x in controls),'actual_target_before_summaries':targets,'bound_source_paths_present_in_immutable_pin':len(paths),'claim_limit':'Existing genuine BEFORE GLBs were compared to themselves only to exercise accessors/topology/material reader compatibility across all selected controls. No rebuilt equality or native acceptance is claimed.'}
(r/'AUDIT-READER-PREFLIGHT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
