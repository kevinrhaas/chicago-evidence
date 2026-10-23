"""Finite source/data/GLB compatibility review; no app/browser/full-gate writes."""
from pathlib import Path,PurePosixPath
import copy,hashlib,importlib.util,json,math,struct,subprocess,sys
sys.dont_write_bytecode=True
D=Path('/workspace/shared/covered-wagon-integration-proposal-2026-10-21');OUT=Path(__file__).parent;BASE='2aebef95f6a5b6fa1bd8353db936c7674a73c32f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,s):
 if not x:raise AssertionError(s)
need(sha(D/'CAPSULE-MANIFEST.json')=='2796e929a2952ea1afd60fd5aff897b7512c1c6853462316b061a03ed7b47832','capsule pin')
manifest=json.loads((D/'CAPSULE-MANIFEST.json').read_text());need(manifest['base_commit']==BASE,'base exact')
for r in manifest['files']:need(sha(D/r['path'])==r['sha256'],'packet pin '+r['path'])
proposed=json.loads((D/'PROPOSED-FILES.json').read_text());pre=json.loads((D/'PREIMAGES.json').read_text())
for r in proposed:need(sha(D/'proposed'/r['path'])==r['sha256'],'proposed pin')
for r in pre['files']:need(sha(D/'preimage'/r['path'])==r['sha256'],'preimage pin')
def read(path):
 p=D/'proposed'/path
 return p if p.exists() else D/'preimage'/path
def j(path):return json.loads(read(path).read_text())
prefix='chicago/4d/';placements=j(prefix+'data/transport/parked/placements.json');prior=json.loads((D/'preimage'/prefix/'data/transport/parked/placements.json').read_text());source=j(prefix+'assets/authored/transport/wagon_covered/SOURCE.json');recipe=j(prefix+'data/transport/parked/covered-w01.json');original={r['id']:r for r in j(prefix+'data/yard/town_trade_goods.json')['wagons']}
for year,rows in prior['scenes'].items():need(placements['scenes'][year][:len(rows)]==rows,'all old placement rows exact')
for key,value in prior['models'].items():need(placements['models'][key]==value,'all old model manifests exact')
need(sum(map(len,placements['scenes'].values()))==6,'six total placements')
changed={r['path'] for r in proposed}
for path in ['renderers/web/js/yard.js','renderers/web/js/main.js','renderers/web/js/parked-transport.js','tools/publish.sh']:
 need(prefix+path not in changed,'renderer/yard/main/publisher unmodified')
 # Verify selected frozen preimages against actual committed Git bytes, read-only.
 result=subprocess.run(['git','show',BASE+':'+prefix+path],cwd='/workspace/chicago',capture_output=True,check=True)
 if (D/'preimage'/prefix/path).is_file():need(result.stdout==(D/'preimage'/prefix/path).read_bytes(),'base Git preimage exact '+path)
for path in ['assets/LICENSES.md','renderers/web/transport/LICENSES.md','docs/LIBERTIES.md','docs/STATUS.md','docs/ROADMAP.md']:
 need(read(prefix+path).read_bytes().startswith((D/'preimage'/prefix/path).read_bytes()),'append-only old bytes preserved '+path)

# Read-only virtual overlay avoids creating another worktree/checkout or writing
# any frozen proposal files while exercising its scoped identity validator.
class Overlay:
 def __init__(self,path=PurePosixPath('chicago/4d')):self.path=PurePosixPath(path)
 def __truediv__(self,path):return Overlay(self.path/str(path))
 def with_suffix(self,suffix):return Overlay(self.path.with_suffix(suffix))
 def read_bytes(self):return read(str(self.path)).read_bytes()
 def read_text(self):return read(str(self.path)).read_text()
 def is_file(self):return read(str(self.path)).is_file()
spec=importlib.util.spec_from_file_location('frozen_covered_identity',read(prefix+'tools/transport/wagon_covered/check.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
need(module.validate_covered(placements,original,Overlay())==2,'actual scoped identity validator')
negatives=[]
def refuse(label,mutate):
 p,o=copy.deepcopy(placements),copy.deepcopy(original);mutate(p,o)
 try:module.validate_covered(p,o,Overlay())
 except (AssertionError,KeyError):negatives.append(label)
 else:raise AssertionError('negative accepted '+label)
def row(p):return next(r for r in p['scenes']['1835'] if r['model']=='covered_w01_western_blue')
target='town_wagon_western_hotel_wagon_yard_1'
for kind in ['cart','farm_box']:refuse(kind+' cannot become covered',lambda p,o,k=kind:o[target].update(kind=k))
refuse('yoke retained',lambda p,o:o[target].update(yoke=False));refuse('stand exact',lambda p,o:row(p).update(at_local_enu_m=[-136.04,-291]));refuse('bearing exact',lambda p,o:row(p).update(bearing_deg=356.3));refuse('identity exact',lambda p,o:row(p).update(replaces='town_wagon_western_hotel_wagon_yard_2'));refuse('duplicate refused',lambda p,o:p['scenes']['1835'].append(copy.deepcopy(row(p))))
def wrong_era(p,o):
 r=row(p);p['scenes']['1835'].remove(r);p['scenes']['1904'].append(r)
refuse('era exact',wrong_era)

def rng(seed):
 s=seed or 1
 while True:
  s=(s+0x6d2b79f5)&0xffffffff;t=((s^(s>>15))*(s|1))&0xffffffff;t=(t^((t+(((t^(t>>7))*(t|61))&0xffffffff))&0xffffffff))&0xffffffff
  yield ((t^(t>>14))&0xffffffff)/4294967296
schemes=[(3,'blue','oxide'),(2,'red','oxide'),(1,'green','oxide'),(1,'blue','greybrown'),(2,'greybrown','greybrown'),(2,'silver','silver'),(1,'oak','darkoak'),(1,'pine','oxide')]
coats=[]
for v in recipe['variants']:
 old=original[v['id']];c=v['coat'];seed='|'.join(['wagon',old['id'],*[format(x,'.15g') for x in old['at_local_enu_m']]]);hashed=2166136261
 for char in seed:hashed=((hashed^ord(char))*16777619)&0xffffffff
 need(c['seedText']==seed and c['seedUint32']==hashed,'old ID/coordinates seed exact')
 stream=rng(hashed);draws=[next(stream) for _ in range(4)];need(draws==c['firstFourDraws'],'actual Mulberry stream exact');choice=draws[0]*sum(s[0] for s in schemes)
 for sc in schemes:
  choice-=sc[0]
  if choice<0:break
 need(c['scheme']==dict(zip(['weight','body','gear'],sc)),'old seeded scheme exact')
 need(c['ageScalar']==.88+draws[1]*.18 and c['gearMultiplier']==.92+draws[2]*.1 and c['canvasScalar']==.84+draws[3]*.18,'old scalar formulas exact')
 need(c['boardVariation']['floorScalar']==.94+next(stream)*.08,'floor RNG consumption exact')
 need(c['boardVariation']['sideAndEndBoardScalars']==[.86+next(stream)*.2 for _ in range(8)],'board RNG consumption exact')
 need(c['boardVariation']['stakeScalars']==[.9+next(stream)*.12 for _ in range(6)],'stake RNG consumption exact')
 for key in ['kind','confidence','at_local_enu_m','bearing_deg','belongs_to','in_enclosure','under_shed','yoke','tilt']:need(v.get(key)==old.get(key),'actual original variant context '+key)
 coats.append({'legacy_id':v['id'],'seed':seed,'scheme':c['scheme'],'ageScalar':c['ageScalar'],'canvasScalar':c['canvasScalar'],'yoke':v['yoke']})

def glb(path):
 raw=read(path).read_bytes();length=struct.unpack_from('<I',raw,12)[0];g=json.loads(raw[20:20+length]);return g,raw[28+length:]
parent,parentbin=glb(prefix+'renderers/web/transport/parked-wagon/wagon-w01.glb');need(sha(read(prefix+'renderers/web/transport/parked-wagon/wagon-w01.glb'))==source['reviewed_parent_sha256'],'actual donor parent pin');models=[]
for v in recipe['variants']:
 model=v['asset_id'];path=prefix+'renderers/web/transport/covered-wagon/'+model+'/covered-w01.glb';g,binary=glb(path);need(binary[:len(parentbin)]==parentbin,'exact donor binary prefix')
 signatures={};triangles=0
 for mesh in g['meshes']:
  for prim in mesh['primitives']:
   sig=tuple(sorted((name,g['accessors'][i]['type'],g['accessors'][i]['componentType'],g['accessors'][i].get('normalized',False)) for name,i in prim['attributes'].items()));mi=prim['material'];signatures.setdefault(mi,set()).add(sig);triangles+=g['accessors'][prim['attributes']['POSITION']]['count']//3
 need(all(len(s)==1 for s in signatures.values()) and len(signatures)==9,'same-material rigid stream compatibility')
 need(triangles==17292 and not g.get('skins') and not g.get('animations'),'static native source product')
 oldmeshes={m['name']:m for m in parent['meshes']};protected=0
 for mesh in g['meshes']:
  if mesh['name'] in oldmeshes and not mesh['name'].startswith('vehicle_body_'):
   need([p['attributes'] for p in mesh['primitives']]==[p['attributes'] for p in oldmeshes[mesh['name']]['primitives']],'protected running gear stream references exact');protected+=1
 sockets=g['extras']['covered_derivative']['unsupported_inherited_sockets'];nodes={n['name']:n for n in g['nodes']};need(len(sockets)==10 and all(nodes[n]['extras']['covered_empty_interface_supported'] is False for n in sockets),'all inherited sockets actually present and unsupported')
 need('covered_preserved_laid_by_yoke' in nodes,'retained physical yoke mesh')
 models.append({'model':model,'triangles':triangles,'material_groups':len(signatures),'native_bytes':read(path).stat().st_size,'protected_nonbody_meshes':protected,'same_material_signatures_compatible':True,'unsupported_sockets':len(sockets)})
terrain=json.loads((D/'actual-terrain-query/receipt.json').read_text());need(terrain['pass'] and terrain['inputsUnchanged'] and terrain['closed'] and terrain['commit']==BASE,'actual terrain query terminal receipt')
for path,pin in source['actual_terrain_qualification']['data_sha256'].items():need(sha(read(path))==pin,'actual terrain meta/binary pin')
stands=[]
for s in source['actual_terrain_qualification']['stands']:
 need(s in terrain['result']['stands'],'source stand equals actual browser query')
 yaw=math.pi-s['bearing_deg']*math.pi/180;c,sn=math.cos(yaw),math.sin(yaw)
 for contact in s['contacts']:
  x,z=contact['local'];need(abs(contact['e']-(s['at_local_enu_m'][0]+c*x+sn*z))<1e-12 and abs(contact['n']-(s['at_local_enu_m'][1]-(-sn*x+c*z)))<1e-12,'renderer contact transform exact')
 heights=[p['height'] for p in s['contacts']];span=max(heights)-min(heights);need(span==s['wheel_plane_span_m']<=.03,'actual 30mm wheel rule')
 stands.append({'id':s['id'],'wheel_plane_span_m':span})
for r in manifest['files']:need(sha(D/r['path'])==r['sha256'],'proposal immutable after finite review')
report={'scope':'Finite proposal source/data/GLB compatibility only; no browser, full gate, integration, publisher or world run','base_commit':BASE,'manifest_sha256':sha(D/'CAPSULE-MANIFEST.json'),'proposal_patch_sha256':sha(D/'covered-2980-proposal.patch'),'source_invariants_PASS':True,'old_placement_rows_and_manifests_exact':True,'available_renderer_yard_publisher_preimage_git_blobs_verified':True,'main_absent_from_proposed_edit_inventory':True,'main_preimage_not_in_packet':True,'append_only_old_bytes_exact':True,'identity_negative_refusals':negatives,'independently_reproduced_coats':coats,'static_models':models,'actual_terrain_receipt_sha256':sha(D/'actual-terrain-query/receipt.json'),'pinned_actual_wheel_samples':stands,'limits':['Two native near GLBs only; Balanced reuses near; Light/far retain legacy. No distinct compressed near/mid/far exports or MeshoptDecoder changes.',
 'Production parked-module fallback/card/disposal/static-batch behavior is supported by unchanged source and compatible GLB streams; prepared actual module fixture has NOT run.',
 'Terrain receipt qualifies four finite wheel samples only; no independent terrain query, actual ground-mesh/body/yoke/host clearance or source/published main/popup/shadow/budget acceptance.',
 'Source wrapper and exact seven-product regeneration PASS are author evidence read and pinned, not independently regenerated by this review. No cached parent is a declared production input.',
 'Seeded scheme/scalars/board draws are exact against current base; no pixel-identical legacy shader/color-cache claim. Guards hash palettes/hash/stream/wagonCoat, but future toneOf changes are not included in that source-contract hash set.',
 'Source integration may be a bounded partial increment; T2980/model acceptance remains OPEN for all absent canonical LOD/compression, actual module/main/published/visual/production-shadow and mobile budget outputs.']}
(OUT/'INDEPENDENT-COVERED-REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
