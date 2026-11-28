"""Verify all stock PR Native partitions on the actual combined checkout."""
import datetime,hashlib,json,re,subprocess
from pathlib import Path
from vegetation_exact_note_folds import verify_folds
W=Path('/workspace/work')
def qualify(prefix, composition):
    def read(p):return json.loads(Path(p).read_text())
    def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    push=read(W/(prefix+'-push-dispatch.json'))
    p=read(W/(prefix+'-final-integration-proof.json'));repo=Path(p['repo'])
    def git(*a):return subprocess.check_output(['git',*a],cwd=repo,text=True).strip()
    rows=[];checkouts=set()
    for k in range(1,9):
        folder=W/(prefix+'-final-ci')/'native-merge'/str(k)
        job=read(folder/'job.json');raw=(folder/'job.log').read_text(errors='replace')
        assert job['run_id']==push['ci_runs']['native'] and job['head_sha']==push['head']
        assert job['name']==f'gate part {k}/8' and job['conclusion']=='success'
        text=re.sub(r'\x1b\[[0-9;]*m','',raw)
        text='\n'.join(re.sub(r'^.*?\d{4}-\d\d-\d\dT[\d:.]+Z\s','',line) for line in text.splitlines())
        m=re.findall(r'\[command\].*git log -1 --format=%H\n([0-9a-f]{40})\s*\n',text)
        assert len(m)==1,'Complete checkout identity missing';checkouts.add(m[0])
        footer=re.findall(r'^CHECK PASS — part (\d+)/8: (\d+) steps, none red\.$',text,re.M)
        assert len(footer)==1 and int(footer[0][0])==k
        assert not re.search(r'^CHECK FAIL(?:\s| —)',text,re.M)
        step=next(s for s in job['steps'] if s['name']=='Run the gate')
        assert step['conclusion']=='success'
        duration=(datetime.datetime.fromisoformat(step['completed_at'].replace('Z','+00:00'))-datetime.datetime.fromisoformat(step['started_at'].replace('Z','+00:00'))).total_seconds()
        assert 0<duration<930
        rows.append({'part':f'{k}/8','steps':int(footer[0][1]),'job_id':job['id'],
                     'seconds':duration,'folder':str(folder),
                     'files_sha256':{f.name:sha(f) for f in folder.iterdir() if f.is_file()}})
    assert len(checkouts)==1;checkout=checkouts.pop()
    found=subprocess.run(['git','cat-file','-e',checkout+'^{commit}'],cwd=repo,
                         stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if found.returncode:subprocess.run(['git','fetch','--quiet','--no-write-fetch-head','--refmap=','origin',checkout],cwd=repo,check=True)
    parents=git('show','-s','--format=%P',checkout).split()
    assert len(parents)==2 and parents[1]==push['head']
    tree=git('rev-parse',checkout+'^{tree}')
    # A later official fold may change the live merge after this run. No later
    # functional input may borrow the verdict from this checkout.
    bridge=bool(composition.get('exact_build_voice_id_bridge'))
    if bridge:
        assert prefix=='vegetation-dev-de2' and push['head']=='33fbecd13db916be592c7474d1d44cd8c7e76a5e'
        from vegetation_de2_voice_id_composition import verify_trees
        folded=verify_trees(repo,tree,composition['composition_tree'])
    else:
        folded=verify_folds(repo,tree,composition['composition_tree'])
    source=subprocess.check_output(['git','show',checkout+':chicago/4d/tools/check.sh'],cwd=repo,text=True)
    declared=[]
    for line in source.splitlines():
        m=re.match(r'^\s*(every_part\s+)?(step|selftest) ',line)
        if m:declared.append(bool(m[1]))
    for k,row in enumerate(rows,1):
        expected=sum(every or i%8==k-1 for i,every in enumerate(declared))
        assert row['steps']==expected
    return {'complete':True,'head':push['head'],'run_id':push['ci_runs']['native'],
            'actual_checkout':checkout,'actual_checkout_parents':parents,'actual_checkout_tree':tree,
            'live_composition_tree':composition['composition_tree'],
            'all8_stock_native_parts_complete':True,'declared_steps':len(declared),
            **({'qualified_exact_build_voice_correction_after_tested_checkout':folded} if bridge else {'only_exact_official_folds_after_tested_checkout':folded}),'parts':rows}
