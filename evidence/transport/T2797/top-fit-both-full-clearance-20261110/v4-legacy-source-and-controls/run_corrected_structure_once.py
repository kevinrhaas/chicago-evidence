from pathlib import Path
import hashlib,json,subprocess,sys,time,traceback

PREP=Path(__file__).parent
OUT=Path(sys.argv[1]);assert not OUT.exists();OUT.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=json.loads((PREP/'EXPECTED-PARENTS.json').read_text())
before={name:sha(Path(name))for name in expected}
assert before==expected,'Reviewed source/input/tool binding changed before execution'
(OUT/'PARENTS-BEFORE.json').write_text(json.dumps(before,indent=2)+'\n')
start=time.monotonic();error=None;result='CORRECTED_STRUCTURE_CONTROLS_NONPASS'
try:
    subprocess.run([sys.executable,str(PREP/'legacy_distance_controls.py'),str(OUT/'LEGACY-DISTANCE-CONTROLS.json')],check=True)
    # Reuse the exact original32-control runner and actual producer receipts;
    # no rewritten metadata or regenerated geometry is necessary for a pure
    # checker-only correction. Its original copied checker is still exact.
    subprocess.run([sys.executable,
        str(PREP/'structure_and_controls.py'),
        str(OUT/'structure-controls'),
        '/tmp/T2797-CAP-UP-PRODUCER-STRUCTURE-ATTEMPT1-20261110/results/candidate'],check=True)
    actual=json.loads((OUT/'structure-controls/STRUCTURE-CONTROLS-RESULT.json').read_text())
    assert actual['result']=='STRUCTURE_ONLY_CONTROLS_PASS' and len(actual['rows'])==34
    result='CORRECTED_STRUCTURE_CONTROLS_PASS'
except BaseException:
    error=traceback.format_exc();raise
finally:
    after={name:sha(Path(name))for name in expected}
    record={'schema':'chicago-t2797-legacy-distance-corrected-structure-controls-v4','result':result,
        'seconds':time.monotonic()-start,'parents_unchanged':before==after,
        'error':error,'mesh_generation_run':False,'sweep_run':False,'qualification':False,
        'all_original32_controls_required':True,'producer_attempt1_NONPASS_preserved':True,
        'diagnostic_setup1_NONPASS_preserved':True}
    (OUT/'PARENTS-AFTER.json').write_text(json.dumps(after,indent=2)+'\n')
    (OUT/'RESULT.json').write_text(json.dumps(record,indent=2)+'\n')
    assert after==before,'Reviewed source/input/tool binding changed during execution'
