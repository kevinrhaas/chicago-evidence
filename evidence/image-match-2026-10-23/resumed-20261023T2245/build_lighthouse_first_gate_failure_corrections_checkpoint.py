from pathlib import Path
import contextlib, hashlib, importlib.util, io, json
W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('archive_exact', W / 'archive_exact.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = Path('/workspace/T3122-T3123-T3124-integration-20261024/closed-T3122-first-gate-fail-and-corrections')
p = r / 'MANIFEST.json'
assert hashlib.sha256(p.read_bytes()).hexdigest() == '26b04925dea96d4c826cb8a47ae4412020dd6ecf02368df073fa7453efdb37f2'
rows = json.loads(p.read_text())['files']
assert len(rows) == 19 and sum(z['bytes'] for z in rows) == 1403164
for z in rows:
    rel = Path(z['path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    q = r / rel
    assert q.resolve().is_relative_to(r) and q.is_file() and not q.is_symlink()
    b = q.read_bytes()
    assert len(b) == z['bytes'] and hashlib.sha256(b).hexdigest() == z['sha256']
name = 'T3122-FIRST-FULLGATE-FAIL2-CONCRETE-CORRECTIONS-SECOND-GATE-PENDING'
note = ('Exact19 closed payloads plus manifest. First whole required-reader FAIL2/1065/384 with47source paths unchanged '
    'and no commit retained. New lantern_profile citation/note now solely PD Castelnau, oldbanked citations/rightsbaseline '
    'unchanged; only pendingT3105 removed after exact incomingAbb v2256 fold proof, ownT3122 retained. Assertions unchanged, '
    'both focused rights/changelog tools PASS. Producera0bcd unchanged; genuine pinnedoneexport+nativeweb provenance refresh '
    'and all50 master/web bytes exact to980703 priorM25. Native61 two stablelaps/audit12XML-nonXMLmembers/package5PASS, '
    '341/955/bothactualAbbbooks/fullpredictedpolicy guards PASS. Secondgate startupbinding only; LIVE secondfullcheck '
    'excluded/PENDING, no app/commit/PR/merge/imageacceptance. T3124unadopted/originalsOPEN-DIFFERS. No live tree/cache or '
    'researchGLB copying/stampminting.')
with contextlib.redirect_stdout(io.StringIO()):
    row = m.archive(name, m.author_manifest(r,p),note)
p=W/'write_index.py';s=p.read_text();needle='- Further producer/integration work is ongoing.'
assert s.count(needle)==1
addition=('- The first lighthouse M full required-reader gate is preserved as **FAIL2/1065 with384 self-tests**, '
    '47 source paths unchanged and no commit. Its two concrete corrections keep assertions intact: only the new '
    'lantern_profile source/note drops the unresolved modern corroborating citation in favor of public-domain Castelnau, '
    'leaving old banked citations/rights unchanged; and only the pending T3105 entry is removed after exact proof it '
    'was already folded in incoming Abb v2256, with own T3122 entry retained. Both unchanged focused rights/changelog '
    'tools then pass. Producer a0bcd0e stays byte exact; a genuine pinned single-target export and native web refresh '
    'provenance, and all50 master/web files remain byte exact to the prior actual M25 packet. Native61 tail settles '
    'in two laps, all12 actual incoming Abb workbook XML/nonXML members prove semantic equality before byte restoration, '
    'package5 stabilizes, and341 raw/955 nonfort rows/both books/full predicted policy guards pass. These19 closed '
    'files plus manifest include only the immutable second-gate startup binding: **the live second fullcheck is pending '
    'and excluded**. No app, commit, PR, merge or original-image acceptance follows; T3124 is unadopted and the original '
    'tickets remain OPEN/DIFFERS. Recover from980703 plus these corrective deltas, never copied research GLBs or minted stamps.\n')
p.write_text(s.replace(needle,addition+needle))
print(json.dumps({'archive':name,'bytes':row['bytes'],'readback':'PASS','inventory_count':len(json.loads((W/'ARCHIVES.json').read_text()))}))
