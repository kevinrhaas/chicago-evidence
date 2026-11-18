from pathlib import Path
import collections
import datetime
import hashlib
import json
import re
import subprocess
import sys
import time

ROOT = Path('/workspace/chicago/chicago/4d')
OUT = Path('/tmp/t3654-source-fallback-summary.json')
ANSI = re.compile(r'\x1b\[[0-9;]*m')

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def snapshot():
    return {'head': git('rev-parse', 'HEAD'), 'tree': git('rev-parse', 'HEAD^{tree}'),
            'status_porcelain': git('status', '--porcelain'),
            'harness_sha256': {p: sha(ROOT / p) for p in
                ['tools/check.sh', 'tools/check_harness.sh', 'tools/test_check_harness.sh']}}

def declarations():
    result = []
    for line_no, line in enumerate((ROOT / 'tools/check.sh').read_text().splitlines(), 1):
        match = re.match(r'^\s*(every_part )?(step|selftest) "([^"]+)"', line)
        if match:
            result.append({'ordinal': len(result) + 1, 'line': line_no,
                           'every_part': bool(match[1]), 'kind': match[2], 'label': match[3]})
    return result

def selected(part, rows):
    k, n = map(int, part.split('/'))
    return [r['ordinal'] for r in rows if r['every_part'] or (r['ordinal'] - 1) % n + 1 == k]

def summarize(doc):
    ordinary = [r['ordinal'] for r in doc['declarations'] if not r['every_part']]
    prerequisites = [r['ordinal'] for r in doc['declarations'] if r['every_part']]
    accepted = dict((x['part'], x) for x in doc['prior_successful_receipts'])
    for run in doc['attempts']:
        if run.get('status') in ['pass', 'pass_from_terminal_log']:
            accepted[run['part']] = run
    counts = collections.Counter(i for run in accepted.values() for i in selected(run['part'], doc['declarations']) if i in ordinary)
    missing = [i for i in ordinary if counts[i] == 0]
    duplicates = [i for i in ordinary if counts[i] > 1]
    doc['ordinal_coverage_including_prior_receipts'] = {
        'accepted_parts': list(accepted), 'ordinary_covered': len(counts),
        'omitted_ordinary_count': len(missing), 'omitted_ordinary_ordinals': missing,
        'duplicate_ordinary_count': len(duplicates), 'duplicate_ordinary_ordinals': duplicates,
        'every_part_execution_counts': {str(i): len(accepted) for i in prerequisites},
        'complete_ordinal_coverage': not missing and not duplicates,
        'scope_note': 'Prior receipts are on earlier implementation snapshots, recorded explicitly. Ordinal coverage alone does not claim all checks ran on the latest HEAD; current full CI remains authoritative.'}
    OUT.write_text(json.dumps(doc, indent=2) + '\n')

mode = sys.argv[1]
if mode == 'init':
    assert not OUT.exists(), 'Refuse to overwrite existing fallback ledger'
    rows = declarations()
    assert len(rows) == 1378
    assert [r['ordinal'] for r in rows if r['every_part']] == [318,319,320]
    old = json.loads(Path('/tmp/t3654-source-gate-summary.json').read_text())
    prior = []
    for run in old['successful_parts']:
        if run['part'] not in ['17/32','1/32','3/16']:
            continue
        prior.append({**run, 'source_provenance': 'Original local gate snapshot; see /tmp/t3654-source-gate-start-inputs.json and /tmp/t3654-source-gate-summary.json. Not a run on current HEAD.'})
    log = Path('/tmp/t3654-preflight-check.log')
    text = ANSI.sub('', log.read_text())
    assert re.search(r'^CHECK PASS — part 2/16: 90 steps, none red\.$', text, re.M)
    prior.append({'part':'2/16', 'status':'pass','exit_code':0,'steps':90,'log':str(log),
                  'log_sha256':sha(log),'source_provenance':'Root preflight on ae259f9a5ddd4e79e1c82cd40e5084d6dcf42290; logfile owns the full successful verdict. See root preflight metadata.'})
    doc = {'schema':'t3654-source-fallback-v1','prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'prepared_snapshot':snapshot(),'state':'prepared_waiting_for_browser_clear',
           'selection_rule':'Ordinal i selected for k/N iff ((i-1)%N)+1==k; every_part prerequisites run in every invocation.',
           'declarations':rows,'planned_parts':[f'{k}/16' for k in range(4,17)],
           'prior_successful_receipts':prior,'attempts':[],
           'limits':{'timeout_seconds':590,'kill_grace_seconds':5,'check_jobs':4,'one_foreground_invocation_per_part':True},
           'stop_file':'/tmp/t3654-source-fallback-stop',
           'not_a_pass':'Prepared, running, failed, timed-out and partial logs never contribute to passing coverage.'}
    summarize(doc)
elif mode == 'start':
    doc=json.loads(OUT.read_text());part=sys.argv[2]
    assert not Path(doc['stop_file']).exists(), 'Root requested stop at partition boundary'
    assert not any(r['status']=='running' for r in doc['attempts']), 'An invocation is already running'
    suffix=part.replace('/','of')+'-attempt'+str(1+sum(r['part']==part for r in doc['attempts']))
    log='/tmp/t3654-source-fallback-'+suffix+'.log'
    timing='/tmp/t3654-source-fallback-'+suffix+'-timings.tsv'
    assert not Path(log).exists() and not Path(timing).exists(), 'Refuse to overwrite a log'
    run={'part':part,'status':'running','start_epoch_s':time.time(),
         'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'start_snapshot':snapshot(),
         'log':log,'timings':timing,'selected_ordinals':selected(part,doc['declarations'])}
    doc['attempts'].append(run);doc['state']='running';summarize(doc)
    print(json.dumps(run))
elif mode in ['finish', 'recover-log']:
    doc=json.loads(OUT.read_text());run=next(r for r in reversed(doc['attempts']) if r['status']=='running')
    recovered=mode=='recover-log'
    code=None if recovered else int(sys.argv[2]);text=ANSI.sub('',Path(run['log']).read_text(errors='replace'))
    match=re.search(r'^CHECK PASS — part (\d+/\d+): (\d+) steps, none red\.$',text,re.M)
    passing=(code==0 or recovered) and match and match[1]==run['part'] and int(match[2])==len(run['selected_ordinals'])
    if recovered:
        assert passing, 'Session recovery requires a complete matching terminal PASS verdict'
    ended=Path(run['log']).stat().st_mtime if recovered else time.time()
    process_path=Path(run['log']).with_suffix('.process.json')
    process_receipt=json.loads(process_path.read_text()) if process_path.exists() else None
    if process_receipt:
        assert process_receipt['part']==run['part'] and process_receipt['exit_code']==code
        ended=process_receipt['end_epoch_ns']/1e9
    run.update(exit_code=code,status=('pass_from_terminal_log' if recovered else 'pass') if passing else 'timeout' if code in [124,137] else 'fail',
               end_epoch_s=ended,duration_s=round(ended-run['start_epoch_s'],3),
               end_snapshot=snapshot(),log_sha256=sha(run['log']),tail=text.splitlines()[-8:])
    run['head_changed_during_call']=run['start_snapshot']['head']!=run['end_snapshot']['head']
    if process_receipt:
        run['process_receipt']=str(process_path)
        run['process_receipt_sha256']=sha(process_path)
        run['duration_s']=round((process_receipt['end_epoch_ns']-process_receipt['start_epoch_ns'])/1e9,3)
        run['duration_note']='Wall duration measured by nanosecond clock immediately before and after the foreground timeout subprocess.'
    if recovered:
        run['exit_code_note']='Unavailable: transient environment reconnect lost exec session 55760 and functions cell g2:54. No exit code inferred.'
        run['duration_note']='Approximate wall time from recorded start to final log mtime; no surviving process timer.'
        run['recovery_evidence']='Complete CHECK PASS terminal verdict with expected part and all 89 selected steps; exec session no longer exists and process inspection found no remaining check.sh invocation.'
    if Path(run['timings']).exists():run['timings_sha256']=sha(run['timings'])
    failure=re.search(r'^CHECK FAIL[^\n]*\n((?:[^\n]*\*[^\n]*\n)+)',text,re.M)
    if failure:run['failure_summary']=failure[0]
    doc['state']='boundary' if passing else 'stopped_after_nonpassing';summarize(doc)
    Path(run['log']).with_suffix('.receipt.json').write_text(json.dumps(run,indent=2)+'\n')
    print(json.dumps({k:run[k] for k in ['part','status','exit_code','duration_s','log','tail']},indent=2))
else:
    raise SystemExit('Expected init, start k/N, finish exit_code or recover-log')
