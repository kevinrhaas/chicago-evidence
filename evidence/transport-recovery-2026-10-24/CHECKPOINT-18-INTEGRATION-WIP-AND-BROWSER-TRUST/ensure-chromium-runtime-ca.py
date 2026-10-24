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
