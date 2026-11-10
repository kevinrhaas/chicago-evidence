from pathlib import Path
import hashlib,json,shutil
own=Path('/tmp/nov9-group-green_tree/chicago/4d');root=Path('/tmp/chicago-west-wicket-20261109/chicago/4d');base=Path('/tmp/nov10-final-three-native/green-tree-after');fixture=base/'chicago/4d';hist=own/'docs/RESEARCH/green-tree-annex-T-2376';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='114b98c2dc057bbc47f66ce158bc984be438399e0c4984222b93e810d542714f';rows=[]
for view in ['andreas_1838','trowbridge_1902','kurz_1893_panel11']:
 cam=Path('data/reference_views/green_tree_tavern')/(view+'.json');mf=cam.with_suffix('.match.json');old=json.load(open(own/mf));assert old['verdict']=='differs'and old['glb_sha256']=='124bf0599a8900855c02a1e7b90ac57c2097718a2bf2f7985e9d58f7c7dab84a'
 oldpair=own/old['side_by_side'];before_name=view+'-BEFORE-upper-row-native9dd-20261110';shutil.copyfile(own/mf,hist/(before_name+'.match.json'));shutil.copyfile(oldpair,hist/(before_name+'.jpg'))
 m=json.load(open(fixture/mf));assert m['verdict']=='unreviewed'and m['glb_sha256']==expected;assert sha(root/cam)==sha(own/cam)==m['camera_sha256'];photo=(root/cam.parent/json.load(open(root/cam))['photo']).resolve();assert sha(photo)==m['photo_sha256'];source_id=json.load(open(root/cam))['source_id'];source=json.load(open(root/'data/sources'/(source_id+'.json')));assert source['verified']and source['rights_status']=='public_domain'
 shutil.copyfile(fixture/mf,hist/(view+'-AFTER-native6908-unreviewed-20261110.match.json'));shutil.copyfile(fixture/m['side_by_side'],own/m['side_by_side']);shutil.copyfile(base/'raw'/(view+'-render.png'),hist/(view+'-AFTER-native6908-render.png'));shutil.copyfile(base/'logs'/(view+'.log'),hist/(view+'-AFTER-native6908-render.log'))
 opened=[x for x in m['differences']if x['status']=='open'];assert len(opened)==1
 opened[0].update(status='fixed',what='Actually viewed this whole final native6908/source pair and its preserved native9dd/source BEFORE pair at the same exact camera. The main upper front-gable row now has THREE readable sash, replacing the former pair; the categorical Trowbridge opening-count omission is physically fixed, not waived as camera tolerance. The three reconstructed .20/.50/.78 stations retain existing stock sash sections and vertical band. The lower front two-sash/rightmost-door row, side/rear/attic openings and completed left group remain present. Earlier uncertain readings of Andreas/Kurz left-edge detail do not establish a historical two-window phase; no conversion date is invented.')
 if view=='andreas_1838':
  m['differences'].append({'status':'within tolerance','what':'The main attic light is retained from John Gray testimony and Trowbridge, although not resolved in Andreas/Kurz. That remaining source-to-source detail and residual drawing/camera projections are explicitly within tolerance under T3153. The upper-storey count itself is now physically three and is not included in this tolerance disposition.'})
 m['verdict']='matches';m['review']={'rule':'AGENTS.md rule11/T3153 visitor stopping rule after physical upper-row correction','native_run_id':42758213227,'native_source':'b9c767997c452740c6b690cf2d280d7f75c8c9d5','retained_native':'6908d896ffba7af2e99d9e5daffd1b49f3f1c9c1','MASTER_sha256':expected,'actual_three_upper_front_sash_visible':True,'actual_source_before9dd_after6908_whole_pairs_viewed':True,'previous_missing_upper_bay_physically_fixed':True,'literal_pixel_or_historical_camera_match_claimed':False,'app_acceptance_claimed':False}
 assert not any(x['status']=='open'for x in m['differences']);(own/mf).write_text(json.dumps(m,indent=2)+'\n')
 rows.append({'view':view,'verdict':'matches','open_differences':0,'upper_front_sash_actually_readable':3,'MASTER_sha256':expected,'camera_sha256':m['camera_sha256'],'photo_sha256':m['photo_sha256'],'source_id':source_id,'source_creator':source.get('author'),'source_url':source['url'],'canonical_pair':m['side_by_side'],'pair_sha256':sha(own/m['side_by_side']),'before_9dd_differs_record':str((hist/(before_name+'.match.json')).relative_to(own)),'before_9dd_pair':str((hist/(before_name+'.jpg')).relative_to(own))})
sc=root/'data/sidecars/1835/green_tree_tavern.json';sidecar=json.load(open(sc));assert sidecar['attributes']['front_upper_layout']['value']==[.2,.5,.78];assert sha(root/'assets/gltf/green_tree_tavern__frame_1833.glb')==expected
receipt={'status':'FINAL_B_THREE_ACTUAL_VIEWS_MATCHES_AFTER_PHYSICAL_UPPER_ROW_FIX','not_a_reading':'Adjudication of existing admitted source pictures, not a new archival source or measured survey.','native_run_id':42758213227,'native_source':'b9c767997c452740c6b690cf2d280d7f75c8c9d5','retained_native':'6908d896ffba7af2e99d9e5daffd1b49f3f1c9c1','MASTER_sha256':expected,'MASTER_bytes':297628,'compiled_sidecar_sha256_at_final_read':sha(sc),'compiled_upper_layout':[.2,.5,.78],'actual_all_three_source_before9dd_after6908_whole_pairs_viewed':True,'views':rows,'finite_adjudication':'All three actual new renders visibly carry three upper front sash. The prior categorical omission is fixed in geometry. Earlier left group corrections remain present. Residual projected spacing/eave/roof tilt, attic/open-bay source conflicts and nonmetric historical date uncertainty remain explicit underT3153, without relabeling the former missing upper sash as tolerance.','rights_and_picture_coverage':'Three verified public-domain source artworks: Andreas1884, Trowbridge1902 and Kurz1893, retrospective and potentially dependent; both named smaller reproductions are covered by their originals. Held/unverified CHM c1859 remains text-only, unseen and check_required; neither it nor the site1859 engraving supplies geometry or an invented match.','limits':'Three isolated genuine native asset/source comparisons only; no survey, literal pixel match, exact historical camera/date, app terrain/yard/WEB/UI acceptance, publication or original-ticket closure claimed here.'}
(hist/'FINAL-B-PICTURE-REVIEW-20261110.json').write_text(json.dumps(receipt,indent=2)+'\n');shutil.copyfile(base/'RENDER-BINDINGS.json',hist/'B-AFTER-RENDER-BINDINGS-20261110.json')
p=hist/'whole-picture-coverage-20261110.json';j=json.load(open(p));j['status']='final_B_three_actual_views_matches_after_physical_upper_row_fix';j['final_native_MASTER_sha256']=expected;j['final_native_review']='FINAL-B-PICTURE-REVIEW-20261110.json'
for x in j['sources']:
 if x['comparison_view']:x['comparison_verdict']='matches';x['actual_review']='Actually viewed the whole source, native9dd BEFORE with two upper sash, and native6908 AFTER with three readable upper sash. The categorical omission is physically corrected; three canonical comparisons match underT3153 with explicit retrospective/source/camera limits.'
p.write_text(json.dumps(j,indent=2)+'\n')
p=hist/'README.md';old=p.read_text();p.write_text('''# Final B picture acceptance — native6908, 2026-11-10

All three canonical comparisons now **match under T-3153 after physically adding
the missing upper sash**. Every actual source/9dd-BEFORE/6908-AFTER whole pair was
viewed. The final render has three readable upper front-gable sash; the previous
pair is retained in the three DIFFERS records and whole BEFORE pictures here.
The earlier missing-opening tolerance assessment remains withdrawn.

The genuine final MASTER is114b98c2 (297,628 bytes), from run42758213227, source
b9c76799 and retained6908d896. Existing cameras and photo bytes are unchanged.
Ground, side, rear and attic openings and completed left group remain present.
Residual projected proportions and source conflicts are recorded explicitly;
this is not a literal pixel match, metric survey or precise stage date claim.

See FINAL-B-PICTURE-REVIEW-20261110.json and the canonical whole pairs under
`docs/RESEARCH/photo-match/green_tree_tavern/`. New raw PNGs, render logs,
unreviewed records and exact bindings are retained beside the DIFFERS history.
The three admitted source artworks retain their authors/credits and public-domain
status. The held c1859 museum lead remains unseen/unverified/check_required,
text-only and excluded from geometry/asset derivation.

Parent separately owns actual current-WEB, terrain/yard, desktop/phone UI review,
publication and original T-2376 closure. These isolated comparisons claim none of
those application checks.

---

## Historical native9dd review — retained below

'''+old)
print(json.dumps({'views':[{k:x[k]for k in ['view','verdict','open_differences','upper_front_sash_actually_readable']}for x in rows],'MASTER_sha256':expected,'sidecar_final_sha256':sha(sc)},indent=2))
