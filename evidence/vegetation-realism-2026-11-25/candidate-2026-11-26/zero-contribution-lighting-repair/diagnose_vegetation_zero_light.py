"""A-B-A stock Light diagnostic; only a private shader override differs."""
import datetime, hashlib, json, os, signal, stat, subprocess, time
from pathlib import Path

w = Path('/workspace/work')
repo = w / 'better-trees-integration'
app = repo / 'chicago/4d'
archive = w / 'vegetation-published-m2-18606-current-1871-before'
root = w / 'vegetation-zero-light-diagnostic'
result = w / 'vegetation-zero-light-diagnostic.json'
assert not root.exists() and not result.exists()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip() == '1605dcbd4b58bedf98084a16d4b32d95a59bd20e'
for p in Path('/proc').glob('[0-9]*/cmdline'):
    try: a = p.read_bytes().split(b'\0')
    except OSError: continue
    assert not (a and b'/workspace/work/pw-browsers/' in a[0] and b'--type=gpu-process' in a), 'GPU active'
    assert not (len(a) > 1 and Path(os.fsdecode(a[0])).name == 'bash' and a[1] in [b'tools/check.sh', b'./tools/check.sh']), 'Native active'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
runtime = {}
for p in (app / 'renderers/web/js').rglob('*.js'):
    rel = p.relative_to(app / 'renderers/web')
    if rel.as_posix() == 'js/changelog.js': continue
    assert (archive / 'walk' / rel).read_bytes() == p.read_bytes(), str(rel)
    runtime[str(rel)] = sha(p)
original = (app / 'renderers/web/js/leaf-light.js').read_text()
old = '''  RE_Direct_Physical(light, position, normal, viewDir, clearcoatNormal, material, reflectedLight);
  float chiBack = max(-dot(normal, light.direction), 0.0);'''
new = '''  // Shadowed and inactive lights contribute exactly zero, including transmission.
  if (all(equal(light.color, vec3(0.0)))) return;
  float chiCos = dot(normal, light.direction);
#ifdef USE_CLEARCOAT
  // The clearcoat normal may face the light while the base normal faces away.
  RE_Direct_Physical(light, position, normal, viewDir, clearcoatNormal, material, reflectedLight);
#else
  if (chiCos > 0.0) {
    RE_Direct_Physical(light, position, normal, viewDir, clearcoatNormal, material, reflectedLight);
  }
#endif
  float chiBack = max(-chiCos, 0.0);'''
assert original.count(old) == 1
variant = original.replace(old, new).replace('|leaf-light-3747-${mask}-${lowSpec}', '|leaf-light-3747-zero-light-${mask}-${lowSpec}')
root.mkdir()
(root / 'leaf-light.variant.js').write_text(variant)
receipt = {'purpose': 'Local controlled A-B-A diagnostic only; does NOT resolve the calibrated EPYC failure. Stock timing helper, all samples, raster, geometry, population, assets and limits unchanged. Private shader skips only zero direct-light contributions; clearcoat base call retained.', 'head': '1605dcbd4b58bedf98084a16d4b32d95a59bd20e', 'archive': str(archive), 'runtime_sha256': runtime, 'original_shader_sha256': hashlib.sha256(original.encode()).hexdigest(), 'variant_shader_sha256': hashlib.sha256(variant.encode()).hexdigest(), 'jobs': []}
env = {**os.environ, 'PATH': str(w/'node22/bin')+':'+os.environ['PATH'], 'NODE_PATH': str(w/'node22/lib/node_modules'), 'PW_EXECUTABLE': str(w/'pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell')}
for label, candidate in [('original-a', False), ('zero-light-b', True), ('original-a2', False)]:
    at = root / label
    site = at / 'site/4d'
    site.mkdir(parents=True)
    # Symlinks point only to a verified, independently immutable archive. One
    # private walk/js directory provides the single controlled runtime override.
    for p in archive.iterdir():
        if p.name != 'walk': (site/p.name).symlink_to(p, target_is_directory=p.is_dir())
    walk = site / 'walk'; walk.mkdir()
    for p in (archive/'walk').iterdir():
        if p.name != 'js': (walk/p.name).symlink_to(p, target_is_directory=p.is_dir())
    js = walk/'js'; js.mkdir()
    for p in (archive/'walk/js').iterdir():
        if p.name == 'leaf-light.js': (js/p.name).write_text(variant if candidate else original)
        else: (js/p.name).symlink_to(p, target_is_directory=p.is_dir())
    tools = at/'chicago/4d/tools'; tools.mkdir(parents=True)
    for name in ['measure_still_frame.mjs', 'still_frame_ceilings.json']:
        (tools/name).write_bytes((app/'tools'/name).read_bytes())
    out = root/f'{label}.json'; log = root/f'{label}.log'
    args = ['node','tools/measure_still_frame.mjs','--year','1835','--only','desktop','--tiers','light','--stands','town_backyard','--capture',str(root/label/'captures'),'--json',str(out)]
    print('START', label, flush=True); start=time.monotonic()
    with log.open('w') as stream:
        child = subprocess.Popen(args, cwd=tools.parent, env=env, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try: code=child.wait(timeout=590)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGTERM)
            try: child.wait(timeout=10)
            except subprocess.TimeoutExpired: os.killpg(child.pid,signal.SIGKILL);child.wait()
            code=124
    row={'label':label,'variant':candidate,'exit_code':code,'seconds':round(time.monotonic()-start,1),'log':str(log),'log_sha256':sha(log),'result':str(out),'result_sha256':sha(out) if out.exists() else None}
    receipt['jobs'].append(row);receipt['time_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();receipt['complete']=len(receipt['jobs'])==3 and all(x['exit_code']==0 for x in receipt['jobs']);result.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(row),flush=True)
    if code: raise SystemExit(code)
print('COMPLETE diagnostic; calibrated hold remains active.',flush=True)
