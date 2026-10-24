#!/usr/bin/env python3
"""Read-only semantic comparison of incoming generated reports and owner-tail output.
The initial working outputs were observed byte-identical to OLD; use immutable OLD
blobs as the reproducible generated candidate even if root has since restored BASE.
"""
import datetime,gzip,hashlib,io,json,struct,subprocess,xml.etree.ElementTree as ET,zipfile
from pathlib import Path
REPO=Path('/workspace/chicago');BASE='de91c45b314a705a6cc2fb9430becb666dfbded6';OLD='3290195d40cbacf5cbfd0c76f14119d6712aa30c'
def blob(ref,p):return subprocess.check_output(['git','-C',str(REPO),'show',ref+':'+p])
def sha(b):return hashlib.sha256(b).hexdigest()
def sig(e):return (e.tag,tuple(sorted(e.attrib.items())),e.text,e.tail,tuple(sig(c) for c in e))
result={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'incoming_dev':BASE,'candidate_blob_source':OLD,'candidate_equals_initial_owner_tail_working_bytes':True,'application_files_written':False,'heavy_tests_run':False}
p='chicago/4d/data/research/research_spend_ledger.json.gz';a=blob(BASE,p);b=blob(OLD,p);now=(REPO/p).read_bytes();da=gzip.decompress(a);db=gzip.decompress(b);offsets=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
result['gzip']={'path':p,'incoming_bytes':len(a),'candidate_bytes':len(b),'incoming_sha256':sha(a),'candidate_sha256':sha(b),'working_now_sha256':sha(now),'working_now_equals_incoming':now==a,'working_now_equals_candidate':now==b,'incoming_header_hex':a[:10].hex(),'candidate_header_hex':b[:10].hex(),'incoming_mtime':struct.unpack('<I',a[4:8])[0],'candidate_mtime':struct.unpack('<I',b[4:8])[0],'incoming_OS_byte':a[9],'candidate_OS_byte':b[9],'changed_raw_offsets':offsets,'payload_bytes':len(da),'payload_sha256':sha(da),'decompressed_payload_identical':da==db,'parsed_JSON_identical':json.loads(da)==json.loads(db),'compressed_deflate_bytes_identical':a[10:-8]==b[10:-8],'CRC_and_length_trailer_identical':a[-8:]==b[-8:],'classification':'Only gzip header OS byte differs; report payload and compressed data are unchanged.'}
p='chicago/reference/resident-research/final/audit/resident_audit_master.xlsx';a=blob(BASE,p);b=blob(OLD,p);now=(REPO/p).read_bytes();za=zipfile.ZipFile(io.BytesIO(a));zb=zipfile.ZipFile(io.BytesIO(b));names=sorted(set(za.namelist())|set(zb.namelist()));members=[];different=[];cells={};ns='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
for n in names:
 aa=za.read(n) if n in za.namelist() else None;bb=zb.read(n) if n in zb.namelist() else None;row={'name':n,'incoming_bytes':len(aa) if aa is not None else None,'candidate_bytes':len(bb) if bb is not None else None,'raw_identical':aa==bb}
 if aa is None or bb is None:row['semantic_identical']=False
 elif aa==bb:row['semantic_identical']=True
 else:
  ea,eb=ET.fromstring(aa),ET.fromstring(bb);row['semantic_identical']=sig(ea)==sig(eb)
  if n.startswith('xl/worksheets/'):
   ca={x.attrib['r']:sig(x) for x in ea.iter(ns+'c')};cb={x.attrib['r']:sig(x) for x in eb.iter(ns+'c')};diff=[k for k in sorted(ca.keys()|cb.keys()) if ca.get(k)!=cb.get(k)];cells[n]={'incoming_cell_count':len(ca),'candidate_cell_count':len(cb),'changed_cell_structure_value_or_style_count':len(diff),'first_changed_cells':diff[:20]}
 if not row['semantic_identical']:different.append(n)
 members.append(row)
result['xlsx']={'path':p,'incoming_bytes':len(a),'candidate_bytes':len(b),'incoming_sha256':sha(a),'candidate_sha256':sha(b),'working_now_sha256':sha(now),'working_now_equals_incoming':now==a,'working_now_equals_candidate':now==b,'incoming_member_count':len(za.namelist()),'candidate_member_count':len(zb.namelist()),'incoming_uncompressed_bytes':sum(za.getinfo(n).file_size for n in za.namelist()),'candidate_uncompressed_bytes':sum(zb.getinfo(n).file_size for n in zb.namelist()),'members':members,'worksheets':cells,'semantically_changed_members':different,'all_values_styles_relationships_and_metadata_identical':not different,'classification':'XML namespace placement and empty-element serialization differ; all expanded XML tags/attributes/text/order, cells, styles and metadata are equal.'}
result['recommendation']='Root should restore the exact incoming DEV blobs for both files before full preflight, preserving upstream encoding and avoiding generated binary churn. Do not commit these report deltas. This audit does not itself restore anything or replace the gate.'
result['freshness_reader_review']={'ledger':'read_ledger decompresses/parses JSON; check compares the semantic document and report text.','resident_audit':'--check derives CSV/README and checks person counts; the independent XML/cell/style audit covers the workbook.','xlsx_settle':'Pins ZIP ordering/timestamps/compression and core timestamps but does not canonicalize other member XML serialization.'}
print(json.dumps(result,indent=2))
if not result['gzip']['decompressed_payload_identical'] or different:raise SystemExit(1)
