from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib
D=Path(__file__).resolve().parent
j=json.loads((D/'raw/DECODED-IBM-ARRAYS.json').read_text())
def mat(a):return [[F(a[c*4+r])for c in range(4)]for r in range(4)]
def mul(a,b):return [[sum((a[r][k]*b[k][c]for k in range(4)),F(0))for c in range(4)]for r in range(4)]
def inv(a):
 b=[row[:]+[F(int(r==c))for c in range(4)]for r,row in enumerate(a)]
 for c in range(4):
  pivot=next(r for r in range(c,4)if b[r][c]);b[c],b[pivot]=b[pivot],b[c];v=b[c][c];b[c]=[x/v for x in b[c]]
  for r in range(4):
   if r!=c:
    v=b[r][c];b[r]=[x-v*y for x,y in zip(b[r],b[c])]
 return [row[4:]for row in b]
def cm(a):return [float(a[r][c])for c in range(4)for r in range(4)]
def maxabs(a,b):return max(abs(float(a[r][c]-b[r][c]))for r in range(4)for c in range(4))
rows=[]
for asset in sorted({f['asset']for f in j['files']}):
 src=next(f for f in j['files']if f['asset']==asset and f['lod']==0);dst=next(f for f in j['files']if f['asset']==asset and f['lod']==3);root=None;records=[];first=None
 for s,d in zip(src['matrices'],dst['matrices']):
  assert s['name']==d['name'];S,T=mat(s['column_major_Float32']),mat(d['column_major_Float32']);C=mul(inv(T),S)
  if root is None:root=C
  exact=C==root;pred=mul(T,root);mismatches=[(r,c)for r in range(4)for c in range(4)if pred[r][c]!=S[r][c]]
  if mismatches and first is None:
   r,c=mismatches[0];first=dict(bone=s['name'],palette_index=s['palette_index'],row=r,column=c,source_IBM_value=float(S[r][c]),destination_IBM_row=[float(x)for x in T[r]],root_basis_column=[float(root[k][c])for k in range(4)],predicted_source_exact_fraction=str(pred[r][c]),actual_source_exact_fraction=str(S[r][c]),exact_residual_fraction=str(pred[r][c]-S[r][c]),absolute_residual=float(abs(pred[r][c]-S[r][c])))
  records.append(dict(name=s['name'],palette_index=s['palette_index'],IBM_bit_exact=s['column_major_Float32']==d['column_major_Float32'],IBM_max_absolute_difference=maxabs(S,T),source_IBM_column_major=s['column_major_Float32'],destination_IBM_column_major=d['column_major_Float32'],right_basis_inverse_destination_times_source_column_major=cm(C),right_basis_exactly_same_as_root=exact,right_basis_max_absolute_difference_from_root=maxabs(C,root),root_basis_prediction_max_absolute_residual=maxabs(pred,S)))
 offdiag=[abs(float(root[r][c]))for r in range(3)for c in range(3)if r!=c]
 rows.append(dict(asset=asset,matrix_equation='destination_IBM[j] * C == source_IBM[j], exact rational arithmetic on decoded Float32 values',common_right_basis_bit_exact=False if first else True,root_basis_column_major=cm(root),root_basis_invertible=True,root_basis_exact_uniform_scale_and_translation=all(root[r][c]==(root[0][0]if r==c else 0)for r in range(3)for c in range(3)),root_basis_max_offdiagonal=max(offdiag),matrices_exact_count=sum(r['IBM_bit_exact']for r in records),basis_matches_root_exact_count=sum(r['right_basis_exactly_same_as_root']for r in records),max_IBM_absolute_difference=max(r['IBM_max_absolute_difference']for r in records),max_basis_absolute_difference_from_root=max(r['right_basis_max_absolute_difference_from_root']for r in records),max_root_basis_prediction_absolute_residual=max(r['root_basis_prediction_max_absolute_residual']for r in records),exact_counterexample=first,per_joint=records))
report=dict(status='EXACT_STATIC_IBM_BASIS_DIAGNOSIS_NO_UNIFORM_BASIS_PROVED',input_sha256=hashlib.sha256((D/'raw/DECODED-IBM-ARRAYS.json').read_bytes()).hexdigest(),arithmetic='Python Fraction: exact dyadic Float32 inputs, exact inverses/multiplication; no fitted tolerance and no passing threshold',cases=rows)
(D/'EXACT-BASIS-ANALYSIS.json').write_text(json.dumps(report,indent=2)+'\n')
for r in rows:print(json.dumps({k:v for k,v in r.items()if k!='per_joint'}))
