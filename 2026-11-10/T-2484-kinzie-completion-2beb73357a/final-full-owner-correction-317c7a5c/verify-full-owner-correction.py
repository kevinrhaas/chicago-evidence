"""Independently qualify the full-source owner correction after its normal FF.
Reads actual Git before/after JSON, native tree objects and dossier identities.
Does not mutate source, replace compiler logic, or treat a sparse check as full.
"""
from pathlib import Path
import subprocess,json,sys,hashlib
r=Path('/tmp/nov10-kinzie-completion');head=sys.argv[1];before='16398263d526268ef8fb89f31368c6e5d966da35';native='d6076c038f5d7e103c922110b568c3188436ec25'
def git(*a):return subprocess.check_output(['git','-C',str(r),*a])
assert git('rev-parse','HEAD').decode().strip()==head;assert not git('status','--porcelain').strip()
paths=git('diff','--name-only',before,head).decode().splitlines();assert len(paths)==615,(len(paths),paths[:10]);rows=[]
for p in paths:
 assert p.startswith('chicago/4d/data/sidecars/1835/')and p.endswith('.json'),p
 b=json.loads(git('show',before+':'+p));a=json.loads(git('show',head+':'+p));old=b.pop('research_doc');new=a.pop('research_doc');assert old==''and isinstance(new,str)and new.startswith('docs/RESEARCH/')and new.endswith('.md'),(p,old,new);assert a==b,('non-dossier field changed',p)
 doc='chicago/4d/'+new;oid=git('rev-parse',head+':'+doc).decode().strip();git('cat-file','-e',oid)
 rows.append({'sidecar':p,'before_research_doc':old,'after_research_doc':new,'dossier_git_blob':oid})
ns=['chicago/4d/assets/gltf','chicago/4d/assets/web','chicago/4d/assets/manifest.json','chicago/4d/assets/manifest.web.json','chicago/4d/assets/manifest.versions.json','chicago/4d/assets/packages'];assert not git('diff','--name-only',native,head,'--',*ns).strip()
preserve=['chicago/4d/data/sidecars/1812','chicago/4d/data/sidecars/1904','chicago/4d/data/structures','chicago/4d/data/flora','chicago/4d/data/reference_views','chicago/4d/data/humans','chicago/4d/data/scenes','chicago/4d/renderers','chicago/4d/generators'];assert not git('diff','--name-only',before,head,'--',*preserve).strip()
out={'status':'PASS_EXACT615_RESEARCH_DOC_ONLY_CORRECTIONS_AND_ALL_NATIVE_1812_UI_CONSUMERS_UNCHANGED','final_source':head,'actual_published_and_reviewed_source':before,'actual_native_retained':native,'changed_count':len(rows),'all_other_sidecar_fields_exact':True,'all_dossier_paths_existing_git_blobs':True,'all_native_outputs_registries_packages_exact_audited_native':True,'all_1812_1904_sidecars_and_all_structures_flora_views_humans_scenes_renderers_generators_exact163':True,'qualification':'Actual final163 tiny desktop+phone runtime/source/resource-policy receipts and full20 earlier target views carry across this nonphysical1835 dossier-pointer-only owner correction. Official full-root compiler/check proof is separate; sparse filesystem results are not called full-source acceptance. Current exact-source protected GitHub checks remain required.','rows':rows}
p=Path('/tmp/nov10-kinzie-ui/FINAL-FULL-OWNER-CORRECTION-INDEPENDENT.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='rows'},indent=2))
