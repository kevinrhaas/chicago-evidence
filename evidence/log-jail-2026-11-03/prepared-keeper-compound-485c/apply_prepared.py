"""Guarded source-only candidate application. Default is a no-write dry run."""
from pathlib import Path
import argparse,hashlib,json,os
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True,help='Separately owned checkout chicago/4d directory');ap.add_argument('--apply',action='store_true');a=ap.parse_args();O=Path(__file__).resolve().parent;R=a.root.resolve();m=json.loads((O/'MANIFEST.json').read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();actions=[]
assert R.is_dir(),R
for row in m['postimages']:
 rel=row['path'];assert not Path(rel).is_absolute()and'..'not in Path(rel).parts
 p=R/rel;assert not p.is_symlink(),p
 new=(O/'postimages'/rel).read_bytes();assert sha(new)==row['after']['sha256']
 old=p.read_bytes()if p.exists()else None
 if row['before']is None:assert old is None,f'New path already exists: {rel}'
 elif row['apply']=='exact':assert old is not None and sha(old)==row['before']['sha256'],f'Changed authored preimage: {rel}'
 else:
  baseline=(O/'baselines'/rel).read_bytes();assert sha(baseline)==row['before']['sha256'];assert old is not None and old.startswith(baseline),f'Append baseline changed: {rel}'
  delta=new[len(baseline):];assert delta not in old,f'Append already applied: {rel}'
  new=old+delta
 actions.append((p,new,{'path':rel,'sha256':sha(new),'bytes':len(new),'preserved_concurrent_suffix':row['apply']=='append'and old is not None and len(old)>row['before']['bytes']}))
# All guards pass before the first write. Caller owns source/ticket/CPU leases.
if a.apply:
 for p,b,_ in actions:
  p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.t2380-prepared-tmp');assert not tmp.exists();mode=(p.stat().st_mode&0o777)if p.exists()else 0o644;tmp.write_bytes(b);tmp.chmod(mode);os.replace(tmp,p)
print(json.dumps({'mode':'APPLIED_SOURCE_ONLY'if a.apply else'DRY_RUN_NO_WRITES','paths':len(actions),'files':[row for _,_,row in actions],'native_assets_installed':False,'registries_installed':False,'native_family_parity_claimed':False,'next':'Native current-family qualification/entrywise registration and ordered derivation before full source/browser checks; original remains DIFFERS.'},indent=2))
