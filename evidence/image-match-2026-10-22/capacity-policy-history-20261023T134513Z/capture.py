from pathlib import Path
import json,hashlib,tarfile,datetime,io
base=Path('/tmp/frame-integration');repo=Path('/tmp/sourceS-inputs-updated-20261023T094606Z/tickets-worktree')
out=repo/'evidence/image-match-2026-10-22'/('capacity-policy-history-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'));out.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
groups=[]
def manifest_group(name,src,manifest='ARTIFACTS.json',extra=()):
 src=base/src;m=json.loads((src/manifest).read_text());files=m['files'];
 for item in files:
  b=(src/item['path']).read_bytes();assert sha(b)==item['sha256'] and len(b)==item['bytes'],item
 groups.append((name,src,[x['path'] for x in files]+[manifest]+list(extra)))
manifest_group('initial-adopted-freeze', 'lodging-capacity-allocation-freeze',extra=['review_actual.py'])
history=json.loads((base/'lodging-capacity-allocation-followup-v2/V1-HISTORY.json').read_text())
for item in history['v1_files']:
 b=(base/'lodging-capacity-allocation-followup'/item['path']).read_bytes();assert sha(b)==item['sha256'] and len(b)==item['bytes'],item
groups.append(('historical-V1-NOT-FOR-ADOPTION',base/'lodging-capacity-allocation-followup',[x['path'] for x in history['v1_files']]))
manifest_group('adopted-V2-native-accounting-and-regression', 'lodging-capacity-allocation-followup-v2')
manifest_group('final-read-only-actual-reviewer','capacity-v2-final-actual-reviewer')
for name,src in [('initial-readonly-diagnosis','M-lodging-readonly-analysis'),('initial-actual-output-independent-review','M-capacity-freeze-actual-independent-review-v1'),('V2-actual-output-root-review','M-capacity-freeze-v2-root-review'),('V2-final-actual-output-review','M-capacity-freeze-v2-independent-owner-review')]:
 p=base/src;assert p.exists(),p
 groups.append((name,p,[str(f.relative_to(p)) for f in sorted(p.rglob('*')) if f.is_file()]))
p=base/'M-capacity-freeze-v2-actual';rows=[]
for line in (p/'ARTIFACTS.sha256').read_text().splitlines():
 digest,rel=line.split('  ',1);b=(p/rel).read_bytes();assert sha(b)==digest,(p,rel);rows.append(rel)
groups.append(('V2-closed-actual-native-six-commands',p,rows+['ARTIFACTS.sha256']))
archive_rows=[]
for name,src,rels in groups:
 assert len(rels)==len(set(rels)),(name,'duplicate files')
 contents={rel:(src/rel).read_bytes() for rel in rels}
 archive=out/(name+'.tar.gz')
 with tarfile.open(archive,'w:gz',dereference=False) as tar:
  for rel,b in contents.items():
   p=src/rel;assert not p.is_symlink();info=tarfile.TarInfo(src.name+'/'+rel);info.size=len(b);info.mtime=int(p.stat().st_mtime);info.mode=0o644;tar.addfile(info,io.BytesIO(b))
 assert archive.stat().st_size<95_000_000
 with tarfile.open(archive,'r:gz') as tar:
  assert len(tar.getmembers())==len(contents)
  for rel,b in contents.items():assert tar.extractfile(src.name+'/'+rel).read()==b
 for rel,b in contents.items():assert (src/rel).read_bytes()==b,('moved while capturing',src,rel)
 capture={'source':str(src),'source_stable_before_after':True,'archive_readback_exact':True,'files':[{'path':rel,'bytes':len(b),'sha256':sha(b)} for rel,b in contents.items()]}
 (out/(name+'.capture.json')).write_text(json.dumps(capture,indent=2)+'\n')
 archive_rows.append({'path':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'source':str(src),'files':len(contents)})
(out/'ARCHIVES.json').write_text(json.dumps({'status':'CLOSED_NATIVE_V2_PASS_FINAL_ROOT_GATE_PENDING','archives':archive_rows},indent=2)+'\n')
(out/'SHA256SUMS.txt').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in archive_rows))
(out/'RECOVERY.md').write_text('''This immutable checkpoint preserves the reviewed carried ordinary-capacity policy, its correction history, actual native outputs, and independent output review. It changes no application or ticket state. All sources were double-read and every archive member was read back and compared; archives contain explicit frozen files only. No live root logs or generated outputs were captured.\n\nThe initial native unfrozen re-cut would have changed already dealt residents and seats. The initial adopted freeze retained the original allocation weights for identities while publishing current capacities. Its original quota/crowded guards remain. Historical follow-up V1 passed bounded accounting checks but kept authorization32 static; it was never adopted and must not be applied. V2 preserves the historical initial authorization32 and deducts later ordinary occupancy using the carried252-bed basis. Actual measurement220→225→230 occupants yields remaining32→27→22, so a capacity-only re-cut cannot mint new lifetime authorization. Child counts do not consume ordinary authorization.\n\nCurrent physical accounting is37 positive vacancies,215 ordinary beds occupied,220 total ordinary occupants,5 occupants above ordinary estimates, and32 net balance. Historical physical vacancies were33, not32. The initial32 was the historical net planning authorization, explicitly distinguished from physical vacancies. Staffing consumes remaining authorization and truthful ordinary occupancy. The formerly incorrect aggregate-vacancy selftest is explicitly corrected using opposing vacancy/overflow; all other original selftest statements and quota/crowded refusal guards remain exact.\n\nParent adopted exact V2 patch SHA256 2c88c4b59d365ecd0f578cb769acbacc56a4c122530fcfa9026587d575c240af. Actual native seat and staffing build/check/self-test all exit0. Independent actual review verifies22 households,157 person identities,52 seat records, quota/fill counters and current capacity metadata against the reviewed candidate. Order-book JSON remains byte-exact. The final reviewer inventories the native Markdown report too; an unavailable prebuild hash is labelled rather than inferred.\n\nRecovery: extract packages into their recorded /tmp/frame-integration names, preserving original/V1/V2 separately. The actual snapshots and proposed outputs are immutable evidence. Proposal checkers read canonical inputs and pin source hashes; prepare.py describes historical creation and must not be blindly rerun against an already adopted or later checkout. Any future application needs fresh guarded composition against its then-current source. Only the exact V2 source patch was parent-adopted. No geometry, source camera, new residents or forced migration is introduced.\n\nFinal55-step refresh/full M strict preflight, exact-final-head workflows and original picture acceptance remain pending at this checkpoint. Earlier first-tail fixedpoint and older failed preflight histories remain historical, not acceptance for V2. Existing picture verdicts remain differs.\n''')
print(json.dumps({'out':str(out),'archives':archive_rows},indent=2))
Path('/tmp/capacity-history-capture-output.txt').write_text(str(out)+'\n')
