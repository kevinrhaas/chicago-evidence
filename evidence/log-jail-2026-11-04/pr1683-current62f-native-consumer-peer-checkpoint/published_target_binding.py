from pathlib import Path
import json,hashlib,subprocess,datetime
P=Path(__file__).parent;Q=P/'gt26-final';W=Path('/tmp/wolf-poster-source-20261103');S=W/'site/4d';sha=lambda b:hashlib.sha256(b).hexdigest();read=lambda p:json.loads(Path(p).read_bytes());git=lambda *a:subprocess.check_output(['git','-C',str(W),*a])
H='62f4546114e252c867dc2b43f2e6cac5503b0577';assert git('rev-parse','HEAD').decode().strip()==H and not git('status','--porcelain');build=read(S/'build.json');assert H.startswith(build['version'])
for n in ['PUBLISH-REAPER.json','CHECK-PUBLISHED-REAPER.json']:
 d=read(Q/n);assert d['command_exit']==0 and d['all_children_reaped']and not d['leftover_cleanup']
old=read(P/'current-ui/desktop-body/PUBLICATION-MAP.json');rows=[]
for name,b in old.items():
 if 'log_jail'in name:
  actual=sha((S/name).read_bytes());assert actual==b['sha256']and(S/name).stat().st_size==b['bytes'],('actualpublished targetdrift',name);rows.append({'path':name,'sha256':actual})
assert len(rows)==6;expected=read(P/'current-ui-phone-cards-v4/mobile-cards/PLAN.json')['expected_picture_rows'];current=read(S/'data/pictures/1835.json')['by_structure'];assert all(current[k]==v for k,v in expected.items())
full={f.relative_to(S).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())}for f in sorted(S.rglob('*'))if f.is_file()};fullsha=sha(json.dumps(full,sort_keys=True).encode());oldsha=read(P/'FINAL-CROSS-VERSION-LEG-LEDGER.json')['full_publication_map_sha256'];assert fullsha!=oldsha
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_head':H,'source_clean':True,'current_build_version':build['version'],'current_full_publication_members':len(full),'current_full_publication_sha256':fullsha,'actual_tested3f_full_publication_sha256':oldsha,'full_publications_differ_explicitly':True,'all6_actualpublishedJail_glbs_sidecars_enclosures_exact_to_actual3f':rows,'both_current_published_picture_rows_value_exact_to_actualv4_capture':expected,'global_picture_metadata_sha256':sha((S/'data/pictures/1835.json').read_bytes()),'independent_foreign_scope_and_renderer_carry':'latest-dev-final/SCOPE-CARRY.json +gt26-final/SCOPE-CARRY.json +peer2e930/82d199','new_actual_browser_or_native_execution':False,'currenthead_hosted8':'Separate required run41782679351 still pending at proof creation','original_T2380':'partial/open; UNREVIEWED/DIFFERS retained'};(Q/'CURRENT-PUBLISHED-TARGET-BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n');print('CURRENT PUBLISHED TARGET6+PICTURE ROWS EXACT; GLOBALMIRROR DIFFERS EXPLICITLY',flush=True)
