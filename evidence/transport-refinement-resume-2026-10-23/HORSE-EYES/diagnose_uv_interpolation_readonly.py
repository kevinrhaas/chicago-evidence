"""Read-only localization of actual fixed-guard generator failure. No derivative written."""
from pathlib import Path
import ast,hashlib,json,math,struct,copy
D=Path(__file__).parent
source=(D/'generate_eye_uv_candidate.py').read_text();tree=ast.parse(source)
# Execute the original constants/helper functions and source-decode body only;
# omit main/release/output creation and all output mutation/GLB construction.
prefix=source[source.index('BASE='):source.index('def main():')]
exec(compile(prefix,'reviewed-generator-prefix','exec'))
body=source[source.index('        raw=BASE.read_bytes()'):source.index("        need(all(v is not None for v in UV)")]
body='\n'.join(line[8:]if line.startswith('        ')else line for line in body.splitlines())
body=body.replace("need(worst<=MAX_UV_CENTROID_ERROR,'Existing tessellation undersamples ocular field')","pass # Diagnostic only: record the actual failed fixed guard; no candidate writer follows.")
body=body.replace("worst=max(worst,math.hypot(actual[0]-linear[0],actual[1]-linear[1]))","error=math.hypot(actual[0]-linear[0],actual[1]-linear[1]);worst=max(worst,error);errors.append({'side':side,'chart':charts[tri[0]],'triangle':tri,'error_uv':error,'centroid_alpha':polar(centroid)[0],'vertex_alpha':[polar_vertex[i][0]for i in tri]})")
errors=[];exec(compile(body,'reviewed-readonly-interpolation-body','exec'))
report={'status':'ACTUAL_READ_ONLY_FAILURE_LOCALIZATION','baseline_sha256':sha(BASE.read_bytes()),'source_generator_sha256':sha(source.encode()),'fixed_threshold_uv':MAX_UV_CENTROID_ERROR,'candidate_written':False,'scope':'Read-only metric localization only. A failed candidate guard is not waived or counted passed. No new generator sweep/retry or GLB write.','components':component_receipts,'errors_top20':sorted(errors,key=lambda x:x['error_uv'],reverse=True)[:20],'by_chart':{side+':'+chart:{'triangles':len(rows),'above_fixed_guard':sum(r['error_uv']>MAX_UV_CENTROID_ERROR for r in rows),'max_error_uv':max(r['error_uv']for r in rows)}for side in ['positive_X','negative_X']for chart in ['front','back']for rows in [[r for r in errors if r['side']==side and r['chart']==chart]]},'unchanged_after':sha(BASE.read_bytes())==BASE_SHA}
(D/'ACTUAL-INTERPOLATION-DIAGNOSIS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
