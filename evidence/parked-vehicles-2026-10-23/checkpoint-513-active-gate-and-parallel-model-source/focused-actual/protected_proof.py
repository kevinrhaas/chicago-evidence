from pathlib import Path
import subprocess,hashlib,json,re,datetime,difflib
R=Path('/tmp/chicago-covered-sag/chicago/4d');D=Path(__file__).resolve().parent
OLD='13375406538e76e8c1deadf18165089f7145ea28';BASE='5135fb7674eea8cf5b140a7cf0c8bc208b0b1f4e';PRIOR='575b4968569283177e36e92878b2a84c5554068e';PFX='chicago/4d/'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def blob(ref,p):return git('show',ref+':'+p)
def work(p):return (R/p.removeprefix(PFX)).read_bytes()
def sha(x):return hashlib.sha256(x).hexdigest()
assert git('rev-parse','HEAD').decode().strip()==OLD
assert git('rev-parse','MERGE_HEAD').decode().strip()==BASE
assert git('rev-parse','origin/dev').decode().strip()=='824957fe47dd70fad729c3b117cb18b695d54b0b'
assert not git('ls-files','-u');assert not git('diff','--name-only')
inv=json.loads(Path('/workspace/shared/T2794-W01-MID11706-CLOTH-DEV575-FULLGATE-COMMIT-ACTUAL-20261023/COMPLETE-PR-DIFF-SOURCE-INVENTORY.json').read_text())
owned={x['path'] for x in inv['paths']}
incoming=set(git('diff','--name-only',PRIOR,BASE,'--','.').decode().splitlines())
shared=owned&incoming
assert shared=={PFX+x for x in ['data/liberties.json','docs/LIBERTIES.md','docs/measurements/source_use_coverage.md','renderers/web/js/main.js','tools/smoke_renderer.mjs']}
fixture=PFX+'tools/transport/brougham/legacy-card-contract.json';protected=owned-shared-{fixture}
for p in protected:assert work(p)==blob(OLD,p),p
incoming_exact=incoming-shared
for p in incoming_exact:assert work(p)==blob(BASE,p),p
assert sha(work(fixture))=='66c973fdda170150dd7a1accd32bdf39aeb25d2dadc714e58e9580a194d9360d'
assert work(PFX+'tools/test_brougham_card.mjs')==blob(OLD,PFX+'tools/test_brougham_card.mjs')
# Exactly the two accepted parked transport callback lines differ from incoming main.
main=work(PFX+'renderers/web/js/main.js');trim=main
for line in [b'  const parkedDrawingBuffer = new THREE.Vector2();\n',b'    getDrawingBufferHeight: () => renderer.getDrawingBufferSize(parkedDrawingBuffer).y,\n']:
 assert trim.count(line)==1;trim=trim.replace(line,b'',1)
assert trim==blob(BASE,PFX+'renderers/web/js/main.js')
# Every native transport GLB and its whole checked-in near/proxy sidecar remain exact133.
transport=[]
for p in git('ls-tree','-r','--full-name','--name-only',OLD,'--','.').decode().splitlines():
 if ('/transport/' in p and p.endswith('.glb')) or p==PFX+'renderers/web/transport/parked-brougham/brougham.json':
  assert work(p)==blob(OLD,p),p;transport.append(p)
# Fixture222, all new Calumet IDs and exact initial/Home glossary guards.
sm=work(PFX+'tools/smoke_renderer.mjs').decode();match=re.search(r'const PLACED_1904 = \[(.*?)\]\.sort\(\);',sm,re.S);assert match
clean=re.sub(r'//[^\n]*','',match.group(1));ids=re.findall(r"'([A-Za-z0-9_]+)'",clean)
actual={r['id'] for r in json.loads((R/'data/sidecars/1904/index.json').read_text())['structures']}
assert len(ids)==len(set(ids))==222 and set(ids)==actual
assert 'guideWords.tap = firstTermTap' not in sm and 'guideWords.firstTermTap = firstTermTap;' in sm
for guard in ["guideWords.tap.term === 'Confidence view'",'guideWords.tap.inTile && guideWords.tap.onTop',"guideWords.tap.app === 'home'",'guideWords.tap.inView && guideWords.tap.away',"guideWords.firstTermTap?.term === 'Reconstructed'","guideWords.firstTermTap.phase === 'welcome'", "guideWords.firstTermTap.journey === 'landed'",'111470']:
 assert guard in sm,guard
# Incoming text edits apply disjointly: each added source block remains verbatim.
incsm=blob(BASE,PFX+'tools/smoke_renderer.mjs').decode();priorsm=blob(PRIOR,PFX+'tools/smoke_renderer.mjs').decode()
blocks=[]
for tag,i,j,k,l in difflib.SequenceMatcher(a=priorsm.splitlines(keepends=True),b=incsm.splitlines(keepends=True),autojunk=False).get_opcodes():
 if tag in ('replace','insert'):
  s=''.join(incsm.splitlines(keepends=True)[k:l]);assert s in sm,'Incoming smoke block lost';blocks.append({'lines':l-k,'sha256':sha(s.encode())})
# Incoming liberty row changes remain exact; unrelated own edits remain exact.
def rows(ref):return {r['id']:r for r in json.loads(blob(ref,PFX+'data/liberties.json'))['liberties']}
prior,inc,old=rows(PRIOR),rows(BASE),rows(OLD);cur={r['id']:r for r in json.loads(work(PFX+'data/liberties.json'))['liberties']}
incchanged={k for k,v in inc.items() if prior.get(k)!=v};ownchanged={k for k,v in old.items() if prior.get(k)!=v}
assert not (incchanged&ownchanged)
for k in incchanged:assert cur[k]==inc[k],k
for k in ownchanged:assert cur[k]==old[k],k
assert set(cur)==set(inc)|set(old)
# Semantic card data, openings, design hashes retained exactly.
a=json.loads(blob(OLD,fixture));b=json.loads(work(fixture));assert len(a['cases'])==len(b['cases'])==6
for x,y in zip(a['cases'],b['cases']):
 assert {k:v for k,v in x.items() if k!='popup_html_sha256'}=={k:v for k,v in y.items() if k!='popup_html_sha256'}
assert (R/'changelog.d/T-2794.json').read_bytes()==blob(OLD,PFX+'changelog.d/T-2794.json')
assert len(list((R/'changelog.d').glob('T-2794*.json')))==1
for name in ['source-vs-513.patch','source-vs-133.patch']:
 ref=BASE if '513' in name else OLD
 (D/name).write_bytes(git('diff','--cached','--binary',ref,'--','.'))
full=[]
for p in sorted(owned):
 data=work(p);rel=p.removeprefix(PFX);target=D/'actual-owned-source'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 full.append({'path':p,'sha256':sha(data),'bytes':len(data),'git_blob':git('hash-object',rel).decode().strip()})
(D/'COMPLETE-OWNED-SOURCE-INVENTORY.json').write_text(json.dumps(full,indent=2)+'\n')
proof={'pass':True,'terminal':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':OLD,'merge_head':BASE,'expected_parents':[OLD,BASE],'staged_tree':git('write-tree').decode().strip(),'lease':'950ce00ce394fc30547294ef731738f6e08138b7','origin_dev_frozen':'824957fe47dd70fad729c3b117cb18b695d54b0b','conflicts':[],'unstaged':[],'owned63':len(owned),'own_protected_byte_exact133_count':len(protected),'protected_paths':sorted(protected),'shared5_paths':sorted(shared),'intentional_fixture_sha256':sha(work(fixture)),'incoming_changed_paths':len(incoming),'incoming_nonshared_byte_exact513_count':len(incoming_exact),'incoming_nonshared_paths':sorted(incoming_exact),'transport_glbs_and_near_sidecar_exact133_count':len(transport),'transport_paths':transport,'main_exception':'Only exact accepted two-line drawing buffer callback addition; all other incoming main bytes exact','smoke_incoming_changed_blocks_verbatim':blocks,'fixture_ids':222,'both_Home_and_initial_Welcome_assertions_retained':True,'incoming_liberty_rows_exact':sorted(incchanged),'owned_liberty_rows_exact':sorted(ownchanged),'legacy_case_json_opening_design_pins_unchanged':6,'original_full_card_LOD_test_source_byte_exact133':True,'single_original_changelog_entry_unchanged':True,'no_rederive_needed':'Tracked incoming Ames GLBs installed by normal merge; source freshness validated separately.'}
(D/'PROTECTED-STAGED-SOURCE-PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items() if not isinstance(v,list)},indent=2))
