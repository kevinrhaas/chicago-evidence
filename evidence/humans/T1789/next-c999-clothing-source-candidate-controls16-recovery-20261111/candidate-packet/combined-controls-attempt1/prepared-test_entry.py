"""Existing sixteen unittest methods only. No producer, body input or native file."""
from pathlib import Path
import hashlib, importlib, json, resource, sys, time, traceback, unittest

P = Path(__file__).resolve().parent
plan = json.loads((P/'PLAN.json').read_text())
out = Path(plan['output'])
assert sys.platform == 'linux', 'RSS units are bound to Linux'
source_pins = {Path(row['file']).resolve():row['sha256'] for row in plan['pins']}
candidate = Path(plan['candidate_tools']).resolve()
canonical = Path(plan['canonical_tools']).resolve()
sys.path[:] = [str(candidate), str(canonical)] + [x for x in sys.path if x not in (str(candidate), str(canonical))]
record = dict(status='INCOMPLETE', source_controls_only=True, expected_tests=16,
    actual_tests=0, success=False, native_fit_accepted=False, photographic_accepted=False)
started = time.monotonic()
try:
    modules = []
    for name in plan['test_modules']:
        module = importlib.import_module(name)
        assert Path(module.__file__).resolve() == candidate/(name+'.py'), name
        modules.append(module)
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(m) for m in modules)
    assert suite.countTestCases() == 16, 'Exact existing method set only'
    result = unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
    record.update(actual_tests=result.testsRun, failure_count=len(result.failures),
        error_count=len(result.errors), skipped_count=len(result.skipped),
        success=result.wasSuccessful() and result.testsRun == 16 and not result.skipped)
    record['status'] = 'SIXTEEN_SOURCE_CONTROLS_PASS' if record['success'] else 'NONPASS_FIRST_FAILURE_STOP'
except BaseException as error:
    record['status'] = 'NONPASS_IMPORT_OR_RUNNER_ERROR'
    record['error'] = repr(error)
    traceback.print_exc()
finally:
    record['seconds_inside_entry'] = time.monotonic()-started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    record['individual_test_process_peak_RSS_bytes'] = int(usage.ru_maxrss)*1024
    record['RSS_method'] = 'Linux RUSAGE_SELF.ru_maxrss KiB converted to bytes; this test process only, excluding parent/source-guard Git/supervisor'
    record['test_CPU_seconds'] = usage.ru_utime+usage.ru_stime
    record['CPU_limit'] = list(resource.getrlimit(resource.RLIMIT_CPU))
    record['AS_limit'] = list(resource.getrlimit(resource.RLIMIT_AS))
    origins = []
    for name, module in sorted(sys.modules.items()):
        if not name.startswith('human_') or not getattr(module, '__file__', None):
            continue
        file = Path(module.__file__).resolve()
        assert file.parent in (candidate, canonical), 'Unexpected human source import: '+str(file)
        digest = hashlib.sha256(file.read_bytes()).hexdigest()
        assert source_pins.get(file) == digest, 'Unpinned or changed human source import: '+str(file)
        origins.append(dict(module=name, file=str(file),
            source='candidate' if file.parent == candidate else 'read_only_c999_dependency',
            sha256=digest))
    record['actual_human_source_imports'] = origins
    with (out/'TEST-ENTRY-RESULT.json').open('x') as stream:
        json.dump(record, stream, indent=2); stream.write('\n')
    print(json.dumps(record))
raise SystemExit(0 if record['success'] else 1)
