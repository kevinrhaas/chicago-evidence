"""Prepared only; ROOT admits bounded metadata controls, never a real producer."""
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time
P=Path(__file__).resolve().parent
assert not (P/'CONTROLS.json').exists(),'No overwrite or automatic retry'
tools=P/'after/chicago/4d/tools'
for name,pin in {'human_clothing_capture_v2.py':'efcd568ebf5cfb16609666aa1bd4e0411b34b390deaa680773f8653b24faefb5','test_human_clothing_capture_v2.py':'2aa90f43fa63fb722613b5601a0a4342c9b58c89e29b4e9fe329f524faf97636','web_derivatives.sh':'2083c5797bbe53c24f5d79e0a222320c5b29d1ffb4b9588731ccf0f94adc62c8'}.items():
    assert hashlib.sha256((tools/name).read_bytes()).hexdigest()==pin,name
tests=['test_human_clothing_capture_v2.CaptureControls.'+name for name in [
 'test_verified_blender_cache_accepts_actual_LTS_header_only',
 'test_LTS_header_cannot_bypass_archive_checksum',
 'test_real_codec_pin_syntax_refuses_changed_missing_ambiguous_and_shell_values']]
code="import resource,sys,unittest; resource.setrlimit(resource.RLIMIT_AS,(67108864,67108864)); resource.setrlimit(resource.RLIMIT_CPU,(5,5)); unittest.main(module=None,argv=['unittest',*sys.argv[1:]],verbosity=2)"
start=time.monotonic();error=None
try:
    r=subprocess.run([sys.executable,'-B','-c',code,*tests],cwd=tools,capture_output=True,timeout=5,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    rc=r.returncode;stdout=r.stdout;stderr=r.stderr
except subprocess.TimeoutExpired as e:
    rc=124;stdout=e.stdout or b'';stderr=e.stderr or b'';error='Original5secondmetadata control cap exceeded'
(P/'controls.stdout').write_bytes(stdout);(P/'controls.stderr').write_bytes(stderr)
receipt={'status':'PASS' if rc==0 else 'NONPASS','returncode':rc,'error':error,'seconds':time.monotonic()-start,'tests':tests,'wall_cap_seconds':5,'CPU_cap_seconds':5,'address_space_cap_bytes':67108864,'max_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'actual_canonical_codec_fixture_SHA256':'2083c5797bbe53c24f5d79e0a222320c5b29d1ffb4b9588731ccf0f94adc62c8','APP_operations':False,'Blender_or_native_producer_execution':False}
(P/'CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt));print(stderr.decode());raise SystemExit(rc)
