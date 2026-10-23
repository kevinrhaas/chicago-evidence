from pathlib import Path
import copy,hashlib,json,sys,time
B=Path(__file__).resolve().parent;T=B/'REGISTRATION-V3/chicago/4d/tools/transport/brougham';sys.path.insert(0,str(T));from check_mid import check_mid_provenance
side=json.loads((B/'REGISTRATION-V3/chicago/4d/renderers/web/transport/parked-brougham/brougham.json').read_text());near=json.loads((T/'near-contract.json').read_text());mid=json.loads((T/'mid-contract.json').read_text());check_mid_provenance(side,near,mid)
cases=[('old_V17_near_hash',['mid_provenance','source_master_near_sha256'],'b74e00937871eef8666fe048501456a8409b18df185c87a0905b083b7a2448fa'),('old_V17_MID_receipt_hash',['mid_provenance','build_receipt_sha256'],'59ea93e112172e94fb9cf435eb01bae6f9b804a28931b0bd679af16920ab1862'),('wrong_recipe_hash',['mid_provenance','recipe_sha256'],'0'*64),('old_nested_appearance_acceptance',['mid_provenance','distance_lod_native_appearance_accepted'],True),('old_V17_revision',['revision'],'v17_recessed_opaque_quarter_near_study'),('old_V17_subdivision_record_counts',['mid_provenance','subdivision_records'],{'near':468,'mid':302}),('old_V17_near_triangle_count',['mid_provenance','triangles'],{'near':33502,'mid':11706}),('unearned_photographic_acceptance',['mid_provenance','photographic_accepted'],True),('unearned_world_budget_acceptance',['mid_provenance','world_budget_accepted'],True),('wrong_recipe_path',['mid_provenance','recipe'],'tools/transport/brougham/lods.json')]
results={}
for name,path,value in cases:
 s=copy.deepcopy(side);o=s
 for key in path[:-1]:o=o[key]
 o[path[-1]]=value
 try:check_mid_provenance(s,near,mid)
 except AssertionError as e:results[name]={'rejected':True,'reason':str(e)}
 else:raise AssertionError('Metadata regression not rejected: '+name)
s=copy.deepcopy(side);s['mid_provenance']['distance_lod_native_appearance_accepted']=s['lod_appearance_accepted']['mid']=True
try:check_mid_provenance(s,near,mid)
except AssertionError as e:results['consistent_but_unearned_both_appearance_true']={'rejected':True,'reason':str(e)}
else:raise AssertionError('Matching unearned true appearance claims were accepted')
out={'pass':True,'scope':'Actual V18 mid-provenance consistency and stale V17 regression controls; no geometry/browser/world/photo qualification','good_current_metadata_pass':True,'negative_count':len(results),'controls':results};(B/'REGISTRATION-V3/MID-PROVENANCE-NEGATIVE-CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
