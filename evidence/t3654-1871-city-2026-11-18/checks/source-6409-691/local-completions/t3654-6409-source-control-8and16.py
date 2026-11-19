"""Fresh, bounded 6409-only native source receipts. Never imports historical coverage."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json
import re
import shlex
import subprocess
import sys
import time

APP=Path('/workspace/chicago/chicago/4d')
HEAD='6409dda1222e1284e111ab0efde1c471f3284d60'
TREE='eeaaefef97d3275b048f308c57c3df5514dbb028'
BASE='c676aa2f4ad6ee8cff0521da6ba8add70d55949c'
RUN=44421763389
OUT=Path('/tmp/t3654-6409-source-ledger.json')
STOP=Path('/tmp/t3654-6409-source-stop')
ALLOWED=('16/16','8/16')
ANSI=re.compile(r'\x1b\[[0-9;]*m')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=APP,text=True).strip()

def snapshot():
    return {'head':git('rev-parse','HEAD'),'tree':git('rev-parse','HEAD^{tree}'),
            'included_dev_base':git('rev-parse','origin/dev'),'status_porcelain':git('status','--porcelain'),
            'harness_sha256':{p:sha(APP/p) for p in ('tools/check.sh','tools/check_harness.sh','tools/test_check_harness.sh')}}

def clean(s):
    return s['head']==HEAD and s['tree']==TREE and s['included_dev_base']==BASE and not s['status_porcelain']

def declarations():
    rows=[]
    for n,line in enumerate((APP/'tools/check.sh').read_text().splitlines(),1):
        m=re.match(r'^\s*(every_part )?(step|selftest) "((?:\\.|[^"\\])*)"',line)
        if m:
            label=re.sub(r'\\([$`"\\])',r'\1',m[3])
            rows.append({'ordinal':len(rows)+1,'line':n,'every_part':bool(m[1]),'kind':m[2],'label':label})
    assert len(rows)==1379 and [r['ordinal'] for r in rows if r['every_part']]==[319,320,321]
    return rows

def selected(part,rows):
    k,n=map(int,part.split('/'))
    return [r['ordinal'] for r in rows if r['every_part'] or (r['ordinal']-1)%n+1==k]

def save(d):
    rows=d['declarations']; ordinary={r['ordinal'] for r in rows if not r['every_part']};required={r['ordinal'] for r in rows if r['every_part']}
    accepted=[r for r in d['attempts'] if r['status']=='pass' and r['exit_code']==0 and clean(r['start_snapshot']) and clean(r['end_snapshot'])]
    counts=Counter(i for r in accepted for i in r['selected_ordinals'])
    d['coverage']={'accepted_parts':[r['part'] for r in accepted],'ordinary_covered':sum(bool(counts[i]) for i in ordinary),
                   'omitted_ordinary_ordinals':sorted(i for i in ordinary if not counts[i]),
                   'duplicate_ordinary_ordinals':sorted(i for i in ordinary if counts[i]>1),
                   'every_part_execution_counts':{str(i):counts[i] for i in sorted(required)}}
    d['full_gate_pass']=False
    pending=OUT.with_suffix('.next.json');pending.write_text(json.dumps(d,indent=2)+'\n');pending.replace(OUT)

mode=sys.argv[1]
if mode=='start':
    part=sys.argv[2];assert part in ALLOWED,'Only the two parent-authorized partitions may run'
    assert not STOP.exists(),'Root requested a boundary hold'
    s=snapshot();assert clean(s),'Source head/tree/base changed or checkout dirty'
    ci=subprocess.run(['gh','run','view',str(RUN),'--repo','kevinrhaas/chicago','--json','headSha,status,conclusion'],cwd=APP,text=True,capture_output=True,timeout=30)
    if ci.returncode==0:
        state=json.loads(ci.stdout)
        if state.get('headSha')==HEAD and state.get('conclusion')=='success':
            print(json.dumps({'stopped':'exact-current hosted source succeeded','run':RUN,'head':HEAD}));sys.exit(75)
    rows=declarations()
    if OUT.exists():d=json.loads(OUT.read_text())
    else:d={'schema':'t3654-6409-source-ledger-v1','scope':'Fresh6409 receipts only; run only explicitly authorized native partitions; no historical evidence or full-gate claim.',
            'source_commit':HEAD,'source_tree':TREE,'included_dev_base':BASE,'hosted_run_id':RUN,'prepared_snapshot':s,
            'declarations':rows,'declaration_snapshot':s['harness_sha256']['tools/check.sh'],'planned_parts':list(ALLOWED),'attempts':[]}
    assert d['source_commit']==HEAD and d['declarations']==rows and not any(r['status']=='running' for r in d['attempts'])
    d['scope']='Fresh6409 receipts only; run only explicitly authorized native partitions; no historical evidence or full-gate claim.'
    d['planned_parts']=list(dict.fromkeys([r['part'] for r in d['attempts']]+list(ALLOWED)))
    attempt=1+sum(r['part']==part for r in d['attempts']);base=Path('/tmp/t3654-6409-source-'+part.replace('/','of')+f'-attempt{attempt}')
    log=Path(str(base)+'.log');timings=Path(str(base)+'-timings.tsv');process=Path(str(base)+'.process.json');wrapper=Path(str(base)+'-wrapper.sh')
    assert log!=process and not any(p.exists() for p in (log,timings,process,wrapper)),'Refuse to overwrite evidence'
    q=shlex.quote
    body='\n'.join(['#!/bin/bash','source /tmp/t3654-runtime.sh','c4d_gate_started_ns=$(date +%s%N)',
      f'timeout --kill-after=5s 590s env C4D_GATE_REQUIRE_READERS=1 C4D_GATE_REQUIRE_BASE=1 CHECK_PART={q(part)} CHECK_JOBS=4 CHECK_TIMINGS={q(str(timings))} bash tools/check.sh > {q(str(log))} 2>&1',
      'c4d_gate_rc=$?','c4d_gate_ended_ns=$(date +%s%N)',
      f'python3 - {q(str(process))} "$c4d_gate_rc" "$c4d_gate_started_ns" "$c4d_gate_ended_ns" <<\'PY\'',
      'import json,sys','from pathlib import Path',
      f'Path(sys.argv[1]).write_text(json.dumps({{"part":{part!r},"head":{HEAD!r},"exit_code":int(sys.argv[2]),"start_epoch_ns":int(sys.argv[3]),"end_epoch_ns":int(sys.argv[4])}},indent=2)+chr(10))',
      'PY','exit "$c4d_gate_rc"',''])
    wrapper.write_text(body)
    run={'part':part,'status':'running','start_epoch_s':time.time(),'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'start_snapshot':s,'declaration_snapshot':s['harness_sha256']['tools/check.sh'],'declared_steps':len(rows),'selected_ordinals':selected(part,rows),
         'log':str(log),'timings':str(timings),'wrapper':str(wrapper),'wrapper_sha256':sha(wrapper),'process_receipt_path':str(process),
         'required_readers':True,'required_base':True,'timeout_s':590,'kill_after_s':5,'jobs':4,
         'controller':str(Path(__file__)), 'controller_sha256':sha(__file__)}
    d['attempts'].append(run);d['state']='running';save(d)
    print(json.dumps({k:run[k] for k in ['part','log','timings','wrapper','wrapper_sha256','process_receipt_path']}))
elif mode=='finish':
    code=int(sys.argv[2]);d=json.loads(OUT.read_text());run=next(r for r in reversed(d['attempts']) if r['status']=='running')
    p=Path(run['process_receipt_path']);process=json.loads(p.read_text())
    assert process['part']==run['part'] and process['head']==HEAD and process['exit_code']==code and process['end_epoch_ns']>=process['start_epoch_ns']
    text=ANSI.sub('',Path(run['log']).read_text());matches=re.findall(r'^CHECK PASS — part (\d+/\d+): (\d+) steps, none red\.$',text,re.M)
    end=snapshot();passing=code==0 and matches==[(run['part'],str(len(run['selected_ordinals'])))] and not re.search(r'^CHECK FAIL\b|^   \^ .+ failed$',text,re.M) and clean(end) and end['harness_sha256']==run['start_snapshot']['harness_sha256']
    run.update(status='pass' if passing else 'timeout' if code in (124,137) else 'fail',exit_code=code,end_snapshot=end,
               end_epoch_s=process['end_epoch_ns']/1e9,duration_s=round((process['end_epoch_ns']-process['start_epoch_ns'])/1e9,3),
               process_receipt=str(p),process_receipt_sha256=sha(p),log_sha256=sha(run['log']),timings_sha256=sha(run['timings']),
               head_changed_during_call=run['start_snapshot']['head']!=end['head'],tail=text.splitlines()[-8:])
    failure=re.search(r'^CHECK FAIL[^\n]*\n((?:[^\n]*\*[^\n]*\n)+)',text,re.M)
    if failure:run['failure_summary']=failure[0]
    d['state']='boundary' if passing else 'stopped_after_nonpassing';save(d)
    Path(run['log']).with_suffix('.receipt.json').write_text(json.dumps(run,indent=2)+'\n')
    print(json.dumps({k:run[k] for k in ['part','status','exit_code','duration_s','log','tail']},indent=2));sys.exit(0 if passing else 1)
else:raise SystemExit('Expected start <part> or finish <actual exit>')
