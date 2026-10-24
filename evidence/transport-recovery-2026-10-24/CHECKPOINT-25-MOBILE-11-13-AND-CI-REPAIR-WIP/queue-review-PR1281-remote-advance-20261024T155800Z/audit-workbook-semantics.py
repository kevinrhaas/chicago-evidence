import pathlib,subprocess,zipfile,io,hashlib,xml.etree.ElementTree as E,json,time,collections
start=time.monotonic();out=pathlib.Path(__file__).parent;repo='/workspace/chicago-resume-1281';path='chicago/reference/resident-research/final/audit/resident_audit_master.xlsx'
refs={'remote-a1f-old-PR':'a1f8176e9271b7a23b489ec00587ec0961aacd16','incoming-DEV':'de91c45b314a705a6cc2fb9430becb666dfbded6'}
blobs={k:subprocess.check_output(['git','show',v+':'+path],cwd=repo) for k,v in refs.items()};zips={k:zipfile.ZipFile(io.BytesIO(v)) for k,v in blobs.items()}
for k,b in blobs.items():(out/(k+'-resident_audit_master.xlsx')).write_bytes(b)
def logical_xml(b):
 def node(e):
  return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else '',[node(c) for c in e],e.tail if e.tail and e.tail.strip() else '']
 return node(E.fromstring(b))
labels=list(refs);za,zb=[zips[k] for k in labels];members=sorted(set(za.namelist())|set(zb.namelist()));rows=[];logical_diffs=[]
for name in members:
 a=za.read(name) if name in za.namelist() else None;b=zb.read(name) if name in zb.namelist() else None
 row={'member':name,'byte_equal':a==b,'bytes':{labels[0]:len(a) if a is not None else None,labels[1]:len(b) if b is not None else None},'sha256':{labels[0]:hashlib.sha256(a).hexdigest() if a is not None else None,labels[1]:hashlib.sha256(b).hexdigest() if b is not None else None}}
 if a!=b:
  if a is not None and b is not None and (name.endswith('.xml') or name.endswith('.rels')):
   aa=logical_xml(a);bb=logical_xml(b);row['expanded_name_XML_tree_equal']=aa==bb
   if aa!=bb:
    logical_diffs.append(name)
    for label,data in zip(labels,[aa,bb]):(out/(label+'-'+name.replace('/','__')+'.logical.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
  else:row['expanded_name_XML_tree_equal']=False;logical_diffs.append(name)
 rows.append(row)
# Actual worksheet cell values, formulae, style references and geometry/settings remain in parsed tree comparison above.
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def cells(z):
 shared=[]
 if 'xl/sharedStrings.xml' in z.namelist():shared=[''.join(si.itertext()) for si in E.fromstring(z.read('xl/sharedStrings.xml'))]
 result={}
 for n in z.namelist():
  if n.startswith('xl/worksheets/') and n.endswith('.xml'):
   cs=[]
   for c in E.fromstring(z.read(n)).findall('.//m:c',ns):
    value=c.find('m:v',ns);value=value.text if value is not None else None
    if c.get('t')=='s' and value is not None:value=shared[int(value)]
    formula=c.find('m:f',ns);inline=c.find('m:is',ns)
    cs.append({'coordinate':c.get('r'),'style':c.get('s'),'type':c.get('t'),'value':value,'formula':formula.text if formula is not None else None,'inline':' '.join(inline.itertext()) if inline is not None else None})
   result[n]=cs
 return result
ca,cb=cells(za),cells(zb);cell_diffs=[k for k in sorted(set(ca)|set(cb)) if ca.get(k)!=cb.get(k)]
proof={'refs':refs,'source_path':path,'blobs':{k:{'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()} for k,v in blobs.items()},'outer_XLSX_byte_equal':blobs[labels[0]]==blobs[labels[1]],'member_name_sets_equal':set(za.namelist())==set(zb.namelist()),'member_count':len(members),'different_byte_member_count':sum(not r['byte_equal'] for r in rows),'logical_XML_or_binary_difference_members':logical_diffs,'worksheet_cells_formulas_style_references_equal':not cell_diffs,'worksheet_cell_difference_members':cell_diffs,'worksheet_cell_counts':{k:len(v) for k,v in ca.items()},'members':rows,'elapsed_seconds':time.monotonic()-start,'limits':'Logical XML compares expanded element/attribute names and ordered children with non-whitespace text; ignores namespace-prefix/attribute-order/indentation and outer ZIP metadata. It preserves all substantive cells, formulas, styles, relationships and document properties; no owner/rewrite/restore was executed.'}
(out/'WORKBOOK-BYTE-VS-LOGICAL-AUDIT.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items() if k!='members'},indent=2))
