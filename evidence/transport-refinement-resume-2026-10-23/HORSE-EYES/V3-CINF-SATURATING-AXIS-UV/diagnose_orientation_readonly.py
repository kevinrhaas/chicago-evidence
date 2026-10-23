from pathlib import Path
import copy,hashlib,json,math,struct
D=Path(__file__).parent
source=(D/'generate_eye_uv_candidate.py').read_text()
exec(compile(source[source.index('BASE='):source.index('def main():')],'reviewed-prefix','exec'))
body=source[source.index('        raw=BASE.read_bytes()'):source.index('        newbin=bytearray(B)')]
body='\n'.join(l[8:]if l.startswith('        ')else l for l in body.splitlines())
body=body.replace("need(area*expected>0,'Isolated reversed/folded ocular UV triangle')","\n    if area*expected<=0:folds.append({'side':side,'chart':chart,'tri':tri,'uv':[(quantized[i])for i in tri],'area':area,'expected':expected,'outward':outward,'positions':[points[i]for i in tri]})")
folds=[];exec(compile(body,'read-only-fold-localization','exec'))
report={'status':'ACTUAL_READ_ONLY_V3_ORIENTATION_FAILURE','source_sha256':sha(source.encode()),'baseline_unchanged':sha(BASE.read_bytes())==BASE_SHA,'candidate_written':False,'components':component_receipts,'fold_count':len(folds),'folds':folds,'scope':'Only failed-guard metric localization, no candidate write or waived production/source criterion.'}
(D/'ACTUAL-ORIENTATION-DIAGNOSIS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
