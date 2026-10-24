#!/usr/bin/env bash
set -euo pipefail
# PROPOSAL ONLY: stop before any filesystem/dependency/Git/publisher/browser mutation.
# ROOT must arrange a quiet resource handoff; no environment-variable bypass exists.
python3 -B - <<'TRANSPORT_SETUP_FREEZE_GUARD'
import json
from pathlib import Path
setup = Path('/workspace/.cloud-setup')
queue = setup/'queue-session.json'
if queue.exists():
    state = json.loads(queue.read_text())
    labels = [state.get('current_phase', ''), state.get('resource_owner', {}).get('state', '')]
    if any('FROZEN' in str(label).upper() or 'RUNNING' in str(label).upper() for label in labels):
        raise SystemExit('Setup blocked: current recovery state owns source/index/mirror or heavy resources; ROOT must reconcile actual receipts and release the freeze first.')
if (setup/'transport-browser-resource-pause.json').exists():
    raise SystemExit('Setup blocked by retained ROOT resource reservation; inspect and release it through the current owner workflow.')
for proc in Path('/proc').iterdir():
    if not proc.name.isdigit():
        continue
    try:
        names = [Path(x.decode(errors='replace')).name for x in (proc/'cmdline').read_bytes().split(b'\0') if x]
    except (FileNotFoundError, ProcessLookupError):
        continue
    if any(x in {'transport-supervise.py', 'smoke_renderer.mjs', '70b-browser-pipeline.py', '70b-browser-pipeline-attempt2.py', 'check.sh', 'preflight.sh'} or x.endswith('_transport_ui_matrix_driver.py') for x in names):
        raise SystemExit('Setup blocked: an actual qualification/supervisor process remains; inspect actual owned results and cleanup, do not relaunch or signal it.')
TRANSPORT_SETUP_FREEZE_GUARD
SETUP=/workspace/.cloud-setup
mkdir -p "$SETUP/downloads" "$SETUP/logs"
cd "$SETUP/downloads"
if [ ! -x "$SETUP/node-v22.22.0-linux-x64/bin/node" ]; then
  curl -fsSL https://nodejs.org/dist/v22.22.0/node-v22.22.0-linux-x64.tar.xz -o node-v22.22.0-linux-x64.tar.xz
  echo '9aa8e9d2298ab68c600bd6fb86a6c13bce11a4eca1ba9b39d79fa021755d7c37  node-v22.22.0-linux-x64.tar.xz' | sha256sum --check
  tar -xJf node-v22.22.0-linux-x64.tar.xz -C "$SETUP"
fi
export PATH="$SETUP/node-v22.22.0-linux-x64/bin:$SETUP/system/usr/bin:$PATH"
if ! command -v bc >/dev/null; then
  mkdir -p "$SETUP/apt/empty" "$SETUP/apt/lists/partial" "$SETUP/apt/cache/archives/partial" "$SETUP/system"
  cat > "$SETUP/apt/sources.list" <<'SOURCES'
deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main
SOURCES
  cat > "$SETUP/apt/apt.conf" <<'APTCONF'
Dir::Etc::parts "/workspace/.cloud-setup/apt/empty";
Dir::Etc::main "/dev/null";
Dir::Etc::sourcelist "/workspace/.cloud-setup/apt/sources.list";
Dir::Etc::sourceparts "-";
Dir::State::lists "/workspace/.cloud-setup/apt/lists";
Dir::Cache "/workspace/.cloud-setup/apt/cache";
APTCONF
  APT_CONFIG="$SETUP/apt/apt.conf" apt-get update -o APT::Update::Error-Mode=any
  APT_CONFIG="$SETUP/apt/apt.conf" apt-get download bc
  for deb in bc_*.deb; do dpkg-deb -x "$deb" "$SETUP/system"; done
fi
python3 -m venv "$SETUP/venv"
cat > "$SETUP/python-requirements.txt" <<'REQUIREMENTS'
attrs==26.1.0
certifi==2026.10.18
et_xmlfile==2.0.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
numpy==2.5.4
openpyxl==3.1.5
pillow==13.0.0
pypdf==6.21.1
pyproj==3.8.0
PyYAML==6.0.3
referencing==0.37.0
rpds-py==2026.9.1
scipy==1.18.1
typing_extensions==4.16.0
REQUIREMENTS
"$SETUP/venv/bin/python" -m pip install --cache-dir "$SETUP/pip-cache" -r "$SETUP/python-requirements.txt"
if [ -f "$SETUP/npm/package-lock.json" ]; then
  npm ci --prefix "$SETUP/npm" --cache "$SETUP/npm-cache" --no-audit --no-fund
else
  npm install --prefix "$SETUP/npm" --cache "$SETUP/npm-cache" --save-exact --no-audit --no-fund playwright@1.56.1
fi
# Both projects resolve Playwright through this common ancestor directory.
if [ ! -e /workspace/node_modules ] && [ ! -L /workspace/node_modules ]; then
  ln -s "$SETUP/npm/node_modules" /workspace/node_modules
fi
cat > "$SETUP/activate.sh" <<'ACTIVATE'
export PATH=/workspace/.cloud-setup/node-v22.22.0-linux-x64/bin:/workspace/.cloud-setup/system/usr/bin:/workspace/.cloud-setup/venv/bin:$PATH
export NODE_PATH=/workspace/.cloud-setup/npm/node_modules
export PW_EXECUTABLE=/usr/bin/chromium
export PW_CHROMIUM=/usr/bin/chromium
export C4D_GATE_REQUIRE_READERS=1
export C4D_GATE_REQUIRE_BASE=1
export CHECK_JOBS=5
ACTIVATE
source "$SETUP/activate.sh"
# Dedicated transport runtime; preserve the generic venv for the other setup paths.
# The managed base must provide the observed reviewed uv version; no bootstrap curl pipe.
command -v uv >/dev/null || { echo 'Reviewed uv 0.12.23 must be supplied by the managed base before setup.' >&2; exit 1; }
case "$(uv --version)" in
  'uv 0.12.23 ('*) ;;
  *) echo 'Unexpected uv version; review the Python bootstrap before installing.' >&2; exit 1 ;;
esac
uv python install --install-dir "$SETUP/uv-python" --no-bin --no-registry 3.11.17
cloud_transport_python="$SETUP/uv-python/cpython-3.11.17-linux-x86_64-gnu/bin/python3.11"
[ -x "$cloud_transport_python" ] || { echo 'Expected reviewed Linux x86_64 CPython3.11.17 runtime is missing.' >&2; exit 1; }
[ "$($cloud_transport_python --version)" = 'Python 3.11.17' ]
if [ ! -e "$SETUP/venv311" ]; then
  uv venv --no-project --no-python-downloads --python "$cloud_transport_python" "$SETUP/venv311"
else
  [ -f "$SETUP/venv311/pyvenv.cfg" ] && [ -x "$SETUP/venv311/bin/python" ] || { echo 'Preserve and inspect unexpected existing venv311; no deletion/reset.' >&2; exit 1; }
  [ "$("$SETUP/venv311/bin/python" --version)" = 'Python 3.11.17' ]
fi
cat > "$SETUP/transport-python311-requirements.txt" <<'TRANSPORT311_REQUIREMENTS'
attrs==26.1.0
certifi==2026.10.23
et_xmlfile==2.0.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
numpy==2.4.6
openpyxl==3.1.5
pillow==13.0.0
pypdf==6.21.2
pyproj==3.7.2
PyYAML==6.0.3
referencing==0.37.0
rpds-py==2026.9.1
scipy==1.17.1
typing_extensions==4.16.0
TRANSPORT311_REQUIREMENTS
uv pip install --python "$SETUP/venv311/bin/python" --no-deps --only-binary :all: --requirement "$SETUP/transport-python311-requirements.txt"
uv pip check --python "$SETUP/venv311/bin/python"
# Compare installed distribution metadata without requiring pip inside venv311.
"$SETUP/venv311/bin/python" -B - <<'TRANSPORT311_METADATA_CHECK'
import importlib.metadata as metadata
from pathlib import Path
expected = dict(line.strip().split('==', 1) for line in Path('/workspace/.cloud-setup/transport-python311-requirements.txt').read_text().splitlines() if line.strip())
actual = {d.metadata['Name']: d.version for d in metadata.distributions()}
assert actual == expected, 'Dedicated311 package census differs; preserve it for explicit review.'
TRANSPORT311_METADATA_CHECK
# Recreate only reusable common helpers; never restore or auto-run an old job driver.
cat > "$SETUP/transport-activate.sh" <<'TRANSPORT_COMMON_HELPER_0'
source /workspace/.cloud-setup/activate.sh
export PATH=/workspace/.cloud-setup/venv311/bin:$PATH
unset CHICAGO_TICKETS_DIR
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export CHECK_JOBS=4
TRANSPORT_COMMON_HELPER_0
echo 'dfb5f69d0e43089c6ca76e8816f585ad41c38d3361fdc424bc646d77abc177b7  /workspace/.cloud-setup/transport-activate.sh' | sha256sum --check
cat > "$SETUP/transport-supervise.py" <<'TRANSPORT_COMMON_HELPER_1'
#!/usr/bin/env python3
import argparse, ctypes, json, os, signal, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--prefix',required=True);p.add_argument('--cwd',required=True);p.add_argument('--timeout',type=float,default=5400);p.add_argument('--browser-pause-file',default='/workspace/.cloud-setup/transport-browser-resource-pause.json');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
cmd=a.command[1:] if a.command[:1]==['--'] else a.command
assert cmd
prefix=Path(a.prefix);prefix.parent.mkdir(parents=True,exist_ok=True)
requested_timeout=a.timeout
timeout_override_reason=None
if prefix.name=='latest-dev-smoke-desktop-13' and a.timeout==1800:
 a.timeout=3600
 timeout_override_reason='Mobile stage13 completed functionally in1354.330s, above the600s budget; allow one bounded desktop UI run and retain actual timing.'
if prefix.name=='de91-integrated-smoke-desktop-13' and a.timeout==3600:
 a.timeout=10800
 timeout_override_reason='Independently verified accepted-DEV desktop13 reference completed in7767s (129m27s). Allow a bounded actual result instead of truncating that known passing cost; repository assertions and600s budget are unchanged.'
for suffix in ['.log','.result.json','.cleanup.json','.pause.json']:
 assert not Path(str(prefix)+suffix).exists(), 'Use a new log name'
wrapper_started=time.monotonic();resource_pause_seconds=0.0
pause_file=Path(a.browser_pause_file)
is_browser=any(Path(part).name=='smoke_renderer.mjs' for part in cmd)
if is_browser and pause_file.exists():
 pause_started=time.monotonic();request=json.loads(pause_file.read_text())
 pause_receipt={'state':'waiting before browser launch','reason':request.get('reason'),'request_file':str(pause_file),'started_unix':time.time(),'browser_launched':False}
 pause_output=Path(str(prefix)+'.pause.json');pause_output.write_text(json.dumps(pause_receipt,indent=2)+'\n')
 while pause_file.exists():time.sleep(.25)
 resource_pause_seconds=time.monotonic()-pause_started
 pause_receipt.update(state='released before browser launch',resource_pause_seconds=resource_pause_seconds,released_unix=time.time())
 pause_output.write_text(json.dumps(pause_receipt,indent=2)+'\n')
if ctypes.CDLL(None,use_errno=True).prctl(36,1,0,0,0)!=0:raise OSError(ctypes.get_errno(),'Unable to own descendant cleanup')
started=wrapper_started;command_started=time.monotonic();child=None;rc=1;timed_out=False;reaped=[]
try:
 with open(str(prefix)+'.log','wb',buffering=0) as log:
  child=subprocess.Popen(cmd,cwd=a.cwd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  try:rc=child.wait(timeout=a.timeout)
  except subprocess.TimeoutExpired:timed_out=True;rc=124
except KeyboardInterrupt:rc=130
finally:
 if child:
  try:os.killpg(child.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  if child.poll() is None:
   try:child.wait(timeout=10)
   except subprocess.TimeoutExpired:
    os.killpg(child.pid,signal.SIGKILL);child.wait()
 # Drain every newly owned descendant; never cap the number of reaps.
 cleanup_started=time.monotonic();remaining=[]
 while True:
  try:
   pid,status=os.waitpid(-1,os.WNOHANG)
   if pid:
    reaped.append({'pid':pid,'status':status});continue
  except ChildProcessError:
   remaining=[];break
  remaining=[]
  for proc in Path('/proc').iterdir():
   if not proc.name.isdigit():continue
   try:
    stat=(proc/'stat').read_text().rsplit(')',1)[1].split()
    if int(stat[1])==os.getpid():remaining.append(int(proc.name))
   except (OSError,ValueError,IndexError):pass
  if not remaining:continue
  for pid in remaining:
   try:
    fd=os.pidfd_open(pid)
    try:
     stat=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
     if int(stat[1])==os.getpid() and stat[0]!='Z':
      sig=signal.SIGKILL if time.monotonic()-cleanup_started>2 else signal.SIGTERM
      signal.pidfd_send_signal(fd,sig,None,0)
    finally:os.close(fd)
   except (OSError,ValueError,IndexError):pass
  if time.monotonic()-cleanup_started>15:break
  time.sleep(.05)
 result={'returncode':rc,'seconds':time.monotonic()-started,'command_seconds':time.monotonic()-command_started,'resource_pause_seconds':resource_pause_seconds,'command':cmd,'cwd':a.cwd,'main_child_pid':child.pid if child else None,'timed_out':timed_out,'requested_timeout_seconds':requested_timeout,'effective_timeout_seconds':a.timeout,'timeout_override_reason':timeout_override_reason}
 Path(str(prefix)+'.result.json').write_text(json.dumps(result,indent=2)+'\n')
 Path(str(prefix)+'.cleanup.json').write_text(json.dumps({'reaped_owned_descendants':reaped,'remaining_owned_children':remaining,'cleanup_complete':not remaining},indent=2)+'\n')
 try:os.write(1,(json.dumps(result)+'\n').encode())
 except BrokenPipeError:pass
raise SystemExit((rc if rc>=0 else 128-rc) if not remaining else 70)
TRANSPORT_COMMON_HELPER_1
echo 'a312967552479c5a85f4de3ffb398ee2dd6007190e6fff9666689792c6b2452c  /workspace/.cloud-setup/transport-supervise.py' | sha256sum --check
cat > "$SETUP/ensure-chromium-runtime-ca.py" <<'TRANSPORT_COMMON_HELPER_2'
import hashlib, json, os, re, subprocess
from pathlib import Path

LOG = Path('/workspace/.cloud-setup/logs/transport-recovery')
DB = Path.home()/'.pki/nssdb'
CA = Path(os.environ['CODEX_PROXY_CERT'])
NODE_CA = Path(os.environ['NODE_EXTRA_CA_CERTS'])
assert DB.is_dir() and (DB/'cert9.db').is_file(), 'Preserve existing NSS database; do not recreate it'

def run(args, data=None):
    return subprocess.check_output(args, input=data, stderr=subprocess.PIPE)

def fingerprint(data):
    text = run(['openssl', 'x509', '-noout', '-fingerprint', '-sha256'], data).decode()
    return text.split('=', 1)[1].strip()

expected = fingerprint(CA.read_bytes())
assert expected == fingerprint(NODE_CA.read_bytes()), 'Use only the same provided CA already trusted by Node'
constraints = run(['openssl', 'x509', '-in', str(CA), '-noout', '-ext', 'basicConstraints']).decode()
assert 'CA:TRUE' in constraints

def certificates():
    listing = run(['certutil', '-L', '-d', 'sql:'+str(DB)]).decode()
    rows = []
    for line in listing.splitlines():
        match = re.match(r'^(.*?)\s{2,}([pPcCTu]*,[pPcCTu]*,[pPcCTu]*)\s*$', line)
        if match and match[1].strip():
            nickname, trust = match[1].strip(), match[2]
            public = run(['certutil', '-L', '-d', 'sql:'+str(DB), '-n', nickname, '-a'])
            rows.append((nickname, trust, fingerprint(public)))
    return rows

matches = [x for x in certificates() if x[2] == expected]
action = 'already trusted'
if matches:
    nickname, trust, _ = matches[0]
    if 'C' not in trust.split(',')[0]:
        parts = trust.split(','); parts[0] = 'C'
        run(['certutil', '-M', '-d', 'sql:'+str(DB), '-n', nickname, '-t', ','.join(parts)])
        action = 'enabled SSL CA trust for the provided current runtime CA'
else:
    nickname = 'Codex runtime proxy CA '+expected.replace(':', '')[:16]
    run(['certutil', '-A', '-d', 'sql:'+str(DB), '-n', nickname, '-t', 'C,,', '-i', str(CA)])
    action = 'imported provided public runtime CA with SSL CA trust'
assert any(fp == expected and 'C' in trust.split(',')[0] for _, trust, fp in certificates())
result = {'action': action, 'provided_ca_sha256_fingerprint': expected, 'nss_directory': str(DB), 'tls_verification_disabled': False, 'private_keys_read_or_exported': False}
(LOG/'chromium-runtime-ca-configuration.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
TRANSPORT_COMMON_HELPER_2
echo 'dbc11a6fdb1711bb34782cc6f59673312dbe082aec1f49064c4161dca2389dcf  /workspace/.cloud-setup/ensure-chromium-runtime-ca.py' | sha256sum --check
cat > "$SETUP/probe-image-cdn-browser.mjs" <<'TRANSPORT_COMMON_HELPER_3'
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire('/workspace/.cloud-setup/npm/package.json');
const { chromium } = require('playwright');
const resultPath = process.env.TRANSPORT_CDN_PROBE_RESULT || '/workspace/.cloud-setup/logs/transport-recovery/post-restart-image-browser-result.json';
if (fs.existsSync(resultPath)) throw new Error('Preserve previous probe; choose a fresh result path');
const browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE, args: ['--enable-unsafe-swiftshader'] });
const result = { route: 'Actual Chromium HTTPS image navigation with normal certificate validation', errors: [] };
try {
  const page = await browser.newPage();
  page.on('requestfailed', r => result.errors.push(r.failure()?.errorText));
  const response = await page.goto('https://kevinrhaas.github.io/chicago-images/prairie-1904/files/a18-gh-courtyard-watercolor-thumb.jpg', { waitUntil: 'load', timeout: 60000 });
  result.status = response.status();
  result.image = await page.evaluate(() => ({ complete: document.images[0]?.complete, width: document.images[0]?.naturalWidth, height: document.images[0]?.naturalHeight }));
  result.pass = result.status === 200 && result.image.complete && result.image.width === 400 && result.image.height === 218 && result.errors.length === 0;
} catch (e) { result.pass = false; result.error = String(e); }
finally { await browser.close(); }
// Include any request failure delivered during browser closure in the final result.
result.pass = result.pass === true && result.errors.length === 0;
fs.writeFileSync(resultPath, JSON.stringify(result, null, 2)+'\n');
console.log(JSON.stringify(result));
if (!result.pass) process.exitCode = 1;
TRANSPORT_COMMON_HELPER_3
echo 'a5c33c7eb08b4e27950d67526935c6798daa741391c5d497e12f3adfa1f62244  /workspace/.cloud-setup/probe-image-cdn-browser.mjs' | sha256sum --check
# Generate only: do NOT execute the CA helper or CDN browser probe here.
# The CA helper CAN import/update only the supplied public runtime CA trust. Invoke
# it only after explicit scoped filesystem permission for the existing NSS directory;
# a prior turn's grant is not transferable. It never reads/exports private keys.
# This installer never grants permissions, runs certutil or configures NSS trust.
# Never use TLS bypass flags or assume generated files prove browser readiness.
source "$SETUP/transport-activate.sh"
cd /workspace/chicago
# Base refs are needed by the repository's history guards. Do not switch/reset HEAD.
if ! git show-ref --verify --quiet refs/remotes/origin/main; then
  git fetch origin refs/heads/main:refs/remotes/origin/main
fi
# A selected-main clone can have only a main fetch mapping and a stale origin/dev.
# Preserve every existing mapping; add DEV tracking only when it is not covered.
cloud_dev_fetch_refspec='refs/heads/dev:refs/remotes/origin/dev'
cloud_dev_tracking_present=0
while IFS= read -r cloud_existing_fetch_refspec; do
  case "$cloud_existing_fetch_refspec" in
    "$cloud_dev_fetch_refspec"|"+$cloud_dev_fetch_refspec"|"refs/heads/*:refs/remotes/origin/*"|"+refs/heads/*:refs/remotes/origin/*")
      cloud_dev_tracking_present=1 ;;
  esac
done < <(git config --get-all remote.origin.fetch || true)
if [ "$cloud_dev_tracking_present" -eq 0 ]; then
  git config --add remote.origin.fetch "$cloud_dev_fetch_refspec"
fi
# Refresh the actual tracking ref even when it already exists; FETCH_HEAD alone is insufficient.
git fetch origin "$cloud_dev_fetch_refspec"
bash chicago/4d/tools/setup-merge-drivers.sh
cd chicago/4d
# Recursive validators require a real directory; use the repository-supported dependency clone.
bash tools/tickets.sh
python3 tools/check_gate_readers.py
node -e 'if(require("playwright/package.json").version!=="1.56.1") throw Error("Wrong Playwright version"); require("playwright").chromium.launch({executablePath:process.env.PW_EXECUTABLE,args:["--no-sandbox"]}).then(async b=>{console.log("Chromium launch OK");await b.close()})'
bash tools/publish.sh
# Generated files and local Git configuration are allowed; tracked files stay unchanged.
for repo in chicago chicago-images chicago-tickets polecat-platform; do
  git -C "/workspace/$repo" diff --exit-code
  git -C "/workspace/$repo" diff --cached --exit-code
done

cat > /workspace/.cloud-setup/start-services.sh <<'CLOUD_SERVICES'
#!/usr/bin/env bash
set -euo pipefail
source /workspace/.cloud-setup/activate.sh
mkdir -p /workspace/.cloud-setup/logs /workspace/.cloud-setup/pids
start_server() {
  local name=$1 port=$2 directory=$3
  local pidfile="/workspace/.cloud-setup/pids/$name.pid"
  if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null && [[ "$(ps -p "$(cat "$pidfile")" -o stat=)" != Z* ]]; then
    return
  fi
  nohup python3 -m http.server "$port" --bind 127.0.0.1 --directory "$directory" > "/workspace/.cloud-setup/logs/$name-server.log" 2>&1 < /dev/null &
  echo "$!" > "$pidfile"
}
start_server chicago 8000 /workspace/chicago/site
start_server polecat 8001 /workspace/polecat-platform
start_server images 8002 /workspace/chicago-images
python3 - <<'PY'
import json, time, urllib.request
checks = [
 (8000, '/4d/1835/', lambda b: b'<html' in b),
 (8000, '/4d/data/scenes/1835.json', lambda b: json.loads(b)['id'] == '1835'),
 (8001, '/lib/demo/', lambda b: b'Polecat' in b),
 (8001, '/site/', lambda b: b'themeToggle' in b),
 (8002, '/prairie-1904/MANIFEST.json', lambda b: len(json.loads(b)['files']) > 1000),
]
for port,path,verify in checks:
 for attempt in range(20):
  try:
   with urllib.request.urlopen(f'http://127.0.0.1:{port}{path}', timeout=5) as r: body=r.read()
   assert verify(body), f'Unexpected response at {port}{path}'
   print(f'Functional HTTP check passed: port {port} {path}')
   break
  except OSError:
   if attempt == 19: raise
   time.sleep(.25)
PY
CLOUD_SERVICES
chmod +x /workspace/.cloud-setup/start-services.sh
