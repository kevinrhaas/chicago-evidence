"""Exercise the fixed driver consumer with current published seasonal actors."""
import datetime, hashlib, json, os, shutil, signal, subprocess, time
from pathlib import Path
w = Path('/workspace/work'); repo = w / 'better-trees-integration'; app = repo / 'chicago/4d'
season_app = w / 'better-trees-seasons-current/chicago/4d'
scratch = w / 'vegetation-driver-metadata-browser'; scratch.mkdir(exist_ok=True)
override = scratch / 'fixed-js'; override.mkdir(exist_ok=True)
consumer = app / 'renderers/web/js/driven-assembly-loader.js'
shutil.copy2(consumer, override / consumer.name)
original = (season_app / 'tools/qa_vegetation_t3747.mjs').read_text()
needle = "        console.log('metrics', JSON.stringify({ year, detail, triangles: row.triangles, calls: row.calls, frameMs: row.frameMs }));"
assert original.count(needle) == 1
source = original.replace(needle, '''        row.transport = await page.evaluate(async () => {
          const a = __chicago4d;
          await a.townTransport.ready();
          if (a.problems.length) throw Error(a.problems.join('\\n'));
          const actors = a.townTransport.actors.map(actor => ({ id: actor.id,
            personId: actor.assembly?.driver?.actor?.personId ?? null }));
          if (!actors.some(actor => actor.id === 'prairie_driven_brougham_loop_1904'))
            throw Error('The actual previously failing 1904 driver must be mounted');
          return { actors, problems: [...a.problems] };
        });
''' + needle)
helper = scratch / 'qa_driver_metadata.mjs'; helper.write_text(source)
out = scratch / 'captures'; out.mkdir(exist_ok=True)
env = {**os.environ, 'PATH': str(w / 'node22/bin') + ':' + os.environ['PATH'],
       'NODE_PATH': str(w / 'node22/lib/node_modules'),
       'PW_EXECUTABLE': str(w / 'pw-browsers/chromium-1194/chrome-linux/chrome'),
       'QA_SITE': str(w / 'better-trees-seasons-current/site/4d'), 'QA_YEAR': '1904',
       'QA_VIEWPORT': 'desktop', 'QA_TIERS': 'light,balanced', 'QA_SEASONS': 'summer',
       'QA_PAIRS': 'light:summer,balanced:summer', 'QA_MODES': '0', 'QA_FRAMES': '3',
       'QA_STAND': 'back_yard', 'QA_TAG': 'driver-fixed', 'QA_OUT': str(out),
       'QA_BEFORE': str(override)}
log = w / 'vegetation-driver-metadata-browser.log'; started = time.monotonic()
with log.open('w') as stream:
    child = subprocess.Popen(['node', str(helper)], cwd=season_app, env=env,
                             stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
    try: code = child.wait(timeout=590)
    except subprocess.TimeoutExpired:
        os.killpg(child.pid, signal.SIGTERM)
        try: child.wait(timeout=10)
        except subprocess.TimeoutExpired: os.killpg(child.pid, signal.SIGKILL); child.wait()
        code = 124
receipt = {'complete': code == 0, 'exit_code': code, 'seconds': round(time.monotonic()-started, 1),
           'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'consumer_sha256': hashlib.sha256(consumer.read_bytes()).hexdigest(),
           'helper_sha256': hashlib.sha256(helper.read_bytes()).hexdigest(),
           'log': str(log), 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
           'note': 'Diagnostic actual current M2 publication with ONLY fixed driven-assembly-loader.js substituted by HTTP; no published/source/archive files changed. Explicitly awaits town transport, requires previously failing Hans loop mounted, and rejects every recorded problem. Not a whole Native or memory qualification.'}
result = out / 'driver-fixed-1904-desktop.json'
if result.exists(): receipt['cases'] = json.loads(result.read_text())
(w / 'vegetation-driver-metadata-browser-receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k != 'cases'}), flush=True)
raise SystemExit(code)
