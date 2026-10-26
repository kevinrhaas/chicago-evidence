#!/usr/bin/env python3
"""Materialize observation inputs from an ALREADY verified deployed snapshot.
Read-only bare Git and existing receipt/body reads; no fetch, browser or app job.
"""
import argparse
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

LOG=Path('/workspace/.cloud-setup/logs/transport-recovery')
M='e03404d2cc275acfa06316835e088a1892289ab8'
TITLE='Rounder carriage lamps and clearer horse eyes'
SUFFIX=': review_required is set — review annotation retained; this flag does not block scene release'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def require(ok,message):
 if not ok: raise RuntimeError(message)
def reference(file):
 p=Path(file).resolve();b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def bound(file,wanted):
 p=Path(file).resolve();b=p.read_bytes();require(re.fullmatch('[0-9a-f]{64}',wanted) and sha(b)==wanted,'Input receipt changed: '+str(p));return json.loads(b)
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['deployed-head','http-receipt','http-receipt-sha256','review-contract','review-contract-sha256','out']: p.add_argument('--'+name,required=True)
 p.add_argument('--bare-repository',default='/workspace/.cloud-setup/chicago-delivery-audit.git')
 p.add_argument('--service-receipt',default=str(LOG/'20261025T2225-FRESH-ENDGAME-METADATA/pr1279.json'))
 p.add_argument('--old-pending',default=str(LOG/'folded-notes-exact-visitor-entry-spec-20261025/T-3083-PENDING-EXACT.json'))
 a=p.parse_args();D=a.deployed_head;require(re.fullmatch('[0-9a-f]{40}',D),'Actual deployed full40 commit required')
 out=Path(a.out).resolve();repo=Path(a.bare_repository).resolve()
 require(out.is_relative_to(LOG) and not out.exists(),'Use a NEW external input directory')
 require(repo.is_relative_to(Path('/workspace/.cloud-setup')) and repo.name.endswith('.git'),'Use separately materialized bare audit repository, never primary Git')
 env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'}
 def git(*args): return subprocess.check_output(['git','--git-dir',str(repo),*args],cwd='/workspace',env=env,stderr=subprocess.PIPE)
 require(git('rev-parse','--is-bare-repository').decode().strip()=='true','Actual source repository is not bare')
 require(git('rev-parse',D+'^{commit}').decode().strip()==D,'Pinned deployed commit object absent')
 git('merge-base','--is-ancestor',M,D)
 http=bound(a.http_receipt,a.http_receipt_sha256);reviews=bound(a.review_contract,a.review_contract_sha256)
 require(http['schema']=='chicago-current-dev-external-merge-selected-http-v1' and http['result']=='PASS' and http['current_dev']==D and http['external_transport_M']==M and http['all_12_served_bytes_match_actual_D'] is True and len(http['http_checks'])==14,'Actual successful deployed-D HTTP14 receipt required')
 builds=[]
 for row in http['http_checks']:
  data=Path(row['body']).read_bytes();require(row['status']=='200' and row['returncode']==0 and len(data)==row['bytes'] and sha(data)==row['sha256'],'Retained actual HTTP response changed')
  if row['path']=='build.json': builds.append(data)
 require(len(builds)==2 and builds[0]==builds[1],'Official before/after build bytes differ')
 build=json.loads(builds[0]);require(build['tier']=='dev' and build['app']=='chicago/4d' and build['ref']=='refs/heads/dev' and len(build['sha'])>=8 and D.startswith(build['sha']),'Official build does not identify actual D')
 ids=reviews['expected_ids'];require(reviews['schema']=='chicago-current-D-exact-nonblocking-review-annotations-v1' and reviews['current_dev']==D and len(ids)==14 and ids==sorted(set(ids)) and reviews['expected_messages']==[x+SUFFIX for x in ids],'Exact shared native-D14 annotation contract required')
 require(sorted(r['id'] for r in reviews['records'])==ids,'Native review sidecar set differs')
 for r in reviews['records']:
  data=Path(r['path']).read_bytes();doc=json.loads(data);blob=git('rev-parse',D+':'+r['source_path']).decode().strip();require(r['source_commit']==D and doc['id']==r['id'] and doc['review_required'] is True and len(data)==r['bytes'] and sha(data)==r['sha256'] and blob==r['source_git_blob'] and git('cat-file','blob',blob)==data,'Native review sidecar/body/Git object differs')
 service=json.loads(Path(a.service_receipt).read_bytes());require(service['number']==1279 and service['merged'] is True and service['state']=='closed' and service['merge_commit_sha']==M,'Actual external merged PR1279 service fact required')
 notespath='chicago/4d/renderers/web/js/changelog.js';notes=git('show',D+':'+notespath)
 string="'(?:\\\\.|[^'\\\\])*'"
 pattern=re.compile(r'\{ v: (\d+), ts: ('+string+r'), date: ('+string+r'), title: ('+string+r'), kind: ('+string+r'),\s*items: \[(.*?)\]\s*\}',re.S)
 found=[]
 for m in pattern.finditer(notes.decode()):
  if ast.literal_eval(m[4])==TITLE: found.append(({'v':int(m[1]),'ts':ast.literal_eval(m[2]),'date':ast.literal_eval(m[3]),'title':TITLE,'kind':ast.literal_eval(m[5]),'items':[ast.literal_eval(x) for x in re.findall(string,m[6])]},m[0]))
 require(len(found)==1,'Target entry absent/duplicated; no guessed fold identity')
 entry,literal=found[0];pendingpath='chicago/4d/changelog.d/T-3083.json';pending=git('show',M+':'+pendingpath);oldpending=Path(a.old_pending).read_bytes()
 require(len(entry['items'])==4 and {k:entry[k] for k in ['title','kind','items']}==json.loads(pending)==json.loads(oldpending),'Original folded title/kind/four ordered items changed')
 shimpath='chicago/4d/tools/changelog_shim.mjs';shimsrc=git('show',D+':'+shimpath);sm=re.search(r'export const WALK_SHIM = `([\s\S]*?)`;\s*$',shimsrc.decode());require(sm is not None,'Native publisher walk shim format changed')
 source_files=[]
 current_paths=[notespath,shimpath]+['chicago/4d/renderers/web/js/'+n for n in ['whatsnew.js','settings-app.js','apps/settings.js','apps/drawer-host.js','navigator.js','about.js']]+['chicago/4d/renderers/web/css/walk.css','.github/chicago-4d-dev-preview.mjs']
 for revision,name in [(D,n) for n in current_paths]+[(M,pendingpath)]:
  data=git('show',revision+':'+name);source_files.append({'revision':revision,'path':name,'git_blob':git('rev-parse',revision+':'+name).decode().strip(),'bytes':len(data),'sha256':sha(data)})
 out.mkdir();payload={'D-CHANGELOG.js':notes,'M-PENDING-T-3083.json':pending,'OLD-PENDING-T-3083.json':oldpending,'TARGET-ENTRY.json':(json.dumps(entry,indent=2)+'\n').encode(),'TARGET-ENTRY-LITERAL.txt':literal.encode(),'D-WALK-CHANGELOG-SHIM.js':sm[1].encode()}
 for name,data in payload.items(): (out/name).write_bytes(data)
 binding={'schema':'chicago-current-dev-targeted-folded-notes-input-v1','prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_dev':D,'external_transport_merge':M,'source_repository':str(repo),'http_receipt':reference(a.http_receipt),'external_PR1279_service':reference(a.service_receipt),'source_files':source_files,'files':{name:reference(out/name) for name in payload},'target':entry,'limits':{'title_words':12,'items':6,'item_words':450},'native_review_annotation_contract':reference(a.review_contract),'responsive_preview_contract':{'mobile':'DEV pill visible/fullbannerhidden','desktop':'fullbanner visible/pillhidden','underlying_identity':'actualdev@D gate/banner URL/base/noindex'},'scope':'Prepared targeted actual official deployed-D observation inputs only; no legacy H3/full24/whole-APP/own-merge or runtime UI result.'}
 (out/'INPUT-BINDING.json').write_text(json.dumps(binding,indent=2)+'\n')
 files=[{'path':str(f.relative_to(out)),**{k:v for k,v in reference(f).items() if k!='path'}} for f in sorted(out.iterdir()) if f.is_file()]
 (out/'MANIFEST.json').write_text(json.dumps({'schema':'pinned-deployed-notes-input-files-v1','current_dev':D,'files':files},indent=2)+'\n')
 print(json.dumps({'result':'PREPARED INPUTS ONLY','current_dev':D,'input_binding':reference(out/'INPUT-BINDING.json'),'review_contract':reference(a.review_contract),'manifest':reference(out/'MANIFEST.json'),'entry_v':entry['v'],'entry_items':len(entry['items'])}))
if __name__=='__main__': main()
