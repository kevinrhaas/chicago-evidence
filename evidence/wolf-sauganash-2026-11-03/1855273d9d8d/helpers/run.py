"""Combined Wolf Images/Sauganash current exterior/arrival probe. --prepare only writes a draft; root separately releases it."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,stat,subprocess,sys
P=Path(__file__).resolve().parent
R=Path('/workspace/chicago-bridge-increment-20261102');A=R/'chicago/4d';S=R/'site/4d'
EXPECTED_CAMERA_SOURCE_IDS=["andreas_1884_wolf_point_1830_view","anonymous_19c_wolf_point_pair","colbert_chamberlin_1871_chicago_1833","miller_davis_1857_wolf_point_vignette","widney_hammon_c1908_chicago_1833","blanchard_shober_1867_wolf_point"]
PICTURE_ID_BY_CAMERA_SOURCE={sid:sid for sid in EXPECTED_CAMERA_SOURCE_IDS}
PICTURE_ID_BY_CAMERA_SOURCE['blanchard_shober_1867_wolf_point']='early-blanchard-shober-1867-wolf-point'
EXPECTED_PICTURE_IDS=[PICTURE_ID_BY_CAMERA_SOURCE[sid]for sid in EXPECTED_CAMERA_SOURCE_IDS]

sha=lambda b:hashlib.sha256(b).hexdigest()
pf=lambda p:sha(Path(p).read_bytes())
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
E=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],env=E)
def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
def metadata():
    result={k:sha(git(*args)) for k,args in {'index_stage':['ls-files','--stage','-z'],'index_flags':['ls-files','-v','-z'],'refs':['for-each-ref','--format=%(refname) %(objectname)'],'config':['config','--local','--list','--null'],'untracked':['ls-files','--others','--exclude-standard','-z']}.items()}
    result['head']=git('rev-parse','HEAD').decode().strip()
    for name in ['index','HEAD','MERGE_HEAD','MERGE_MSG','ORIG_HEAD']:
        q=Path(git('rev-parse','--path-format=absolute','--git-path',name).decode().strip())
        result[name]=dict(sha256=pf(q),mode=stat.S_IMODE(q.stat().st_mode),mtime_ns=q.stat().st_mtime_ns,ctime_ns=q.stat().st_ctime_ns)if q.exists()else None
    return result
def inputs():
    files=set((A/'renderers/web/js').rglob('*.js'))|set((S/'walk/js').rglob('*.js'))
    views=A/'data/reference_views/wolf_point_tavern'
    files|=set(views.glob('*.json'))
    files|={A/'data/structures/wolf_point_tavern.json',A/'data/sidecars/1835/wolf_point_tavern.json',S/'data/sidecars/1835/wolf_point_tavern.json',A/'data/pictures/1835.json',S/'data/pictures/1835.json',S/'walk/index.html'}
    cameras=[p for p in views.glob('*.json')if not p.name.endswith('.match.json')]
    assert len(cameras)==7
    assert set(json.loads(p.read_bytes())['source_id']for p in cameras)==set(EXPECTED_CAMERA_SOURCE_IDS)
    for camera in cameras:
        c=json.loads(camera.read_bytes());m=json.loads(camera.with_suffix('.match.json').read_bytes())
        photo=(views/c['photo']).resolve();model=A/m['glb'];sideby=A/m['side_by_side']
        assert pf(camera)==m['camera_sha256']and pf(photo)==m['photo_sha256']and pf(model)==m['glb_sha256']and m['verdict']=='matches'
        files|={photo,model,sideby,A/'data/sources'/f"{c['source_id']}.json"}
        if c['source_id']=='blanchard_shober_1867_wolf_point':assert c['library_image']==PICTURE_ID_BY_CAMERA_SOURCE[c['source_id']]
    sidecar=json.loads((S/'data/sidecars/1835/wolf_point_tavern.json').read_bytes());asset=Path(sidecar['asset'])
    assert not asset.is_absolute()and '..'not in asset.parts
    files|={A/'assets/web'/asset.name,S/'data'/asset}
    assert (A/'assets/web'/asset.name).read_bytes()==(S/'data'/asset).read_bytes()
    for source,published in [(A/'renderers/web/js/main.js',S/'walk/js/main.js'),(A/'data/pictures/1835.json',S/'data/pictures/1835.json')]:assert source.read_bytes()==published.read_bytes()
    rows=json.loads((S/'data/pictures/1835.json').read_bytes())['by_structure']['wolf_point_tavern']
    assert set(EXPECTED_PICTURE_IDS)<=set(r['id']for r in rows)
    assert all(not r.get('spot')for r in rows if r['id']in EXPECTED_PICTURE_IDS)
    nypl=next(r for r in rows if r['id']==PICTURE_ID_BY_CAMERA_SOURCE['blanchard_shober_1867_wolf_point'])
    assert nypl['library']and nypl['url']==json.loads((A/'data/sources/blanchard_shober_1867_wolf_point.json').read_bytes())['url']
    files|={A/'tools/compile_pictures.py',A.parent/'prairie_1904_v1/data/images.json'}
    for sid in ['sauganash_hotel','philo_carpenter_log_shop']:
        files|={A/f'data/structures/{sid}.json',A/f'data/sidecars/1835/{sid}.json',S/f'data/sidecars/1835/{sid}.json'}
        source_record=json.loads((A/f'data/sidecars/1835/{sid}.json').read_bytes())
        shipped_record=json.loads((S/f'data/sidecars/1835/{sid}.json').read_bytes())
        if source_record.get('residents'):
            # Official publication defers household notes; its native check is bound below.
            household_file=S/f'data/sidecars/1835/households/{sid}.json'
            households=json.loads(household_file.read_bytes())
            assert households=={'id':source_record['id'],'residents':source_record['residents']}
            assert dict(shipped_record,residents=households['residents'])==source_record
            files.add(household_file)
        else:assert shipped_record==source_record
        files|={A/'tools/defer_household_notes.mjs',P/'household-contract.log',P/'household-contract-REAPER.json'}
        contract=json.loads((P/'household-contract-REAPER.json').read_bytes())
        assert contract['command_exit']==0 and contract['all_children_reaped']and not contract['leftover_cleanup']
        assert 'record(s) ship slim, and their households ship whole beside them'in(P/'household-contract.log').read_text()
        row=json.loads((A/f'data/sidecars/1835/{sid}.json').read_bytes());asset=Path(row['asset'])
        assert not asset.is_absolute()and '..'not in asset.parts
        files|={A/'assets'/asset,A/'assets/web'/asset.name,S/'data'/asset}
        assert (A/'assets/web'/asset.name).read_bytes()==(S/'data'/asset).read_bytes()
    assert pf(A/'assets/gltf/sauganash_hotel__frame_1831.glb')=='a369598aafec6a868b0ec3e04ba591a821e4518174a1e75ac2bdba790ffbe5ec'
    assert pf(A/'assets/web/sauganash_hotel__frame_1831.glb')=='5f7d8a54f1c805d53bdb558506dc18ce237c9c0fb180a7cd274dec7d64ad480e'
    for rel in ['data/enclosures/town_entrance_aprons.json','data/yard/town_trade_goods.json']:
        files|={A/rel,S/rel};assert (A/rel).read_bytes()==(S/rel).read_bytes()
    for camera in (A/'data/reference_views/philo_carpenter_log_shop').glob('*.json'):
        if camera.name.endswith('.match.json'):continue
        m=json.loads(camera.with_suffix('.match.json').read_bytes());c=json.loads(camera.read_bytes());photo=(camera.parent/c['photo']).resolve()
        assert m['verdict']=='matches'and m['group_sha256']=='a8fe7c17dbf1f39cc42ee95cb05d42801be41f127254dbb5908ac7333694232d'
        assert pf(camera)==m['camera_sha256']and pf(photo)==m['photo_sha256']
        files|={camera,camera.with_suffix('.match.json'),photo,A/m['side_by_side'],A/'data/sources'/f"{c['source_id']}.json"}
    return {str(f):dict(sha256=pf(f),bytes=f.stat().st_size,mode=stat.S_IMODE(f.stat().st_mode))for f in sorted(files)}
ap=argparse.ArgumentParser();ap.add_argument('--prepare',type=Path);ap.add_argument('--plan',type=Path);ap.add_argument('--plan-sha256');ap.add_argument('--run',action='store_true');args=ap.parse_args()
if args.prepare:
    assert not args.run and not args.prepare.exists()
    bindings=inputs()
    plan={'root_approved':False,'saug_reference_camera':json.loads((A/'data/reference_views/philo_carpenter_log_shop/trowbridge-1902.json').read_bytes()),'saug_entrance':next(x for x in json.loads((A/'data/enclosures/town_entrance_aprons.json').read_bytes())['entrances']if x['id']=='sauganash_hotel__door_1'),'expected_picture_ids':EXPECTED_PICTURE_IDS,'expected_camera_source_ids':EXPECTED_CAMERA_SOURCE_IDS,'picture_id_by_camera_source':PICTURE_ID_BY_CAMERA_SOURCE,'source_check_parts_and_publish_closed':False,'source_root':str(R),'site_parent':str(R/'site'),'output':'/workspace/combined-wolf-saug-both-actual-20261102','TMP':'/tmp/combinedws1102','expected_head':git('rev-parse','HEAD').decode().strip(),'input_bindings':bindings,'source_scope_sha256':sha(canonical(bindings)),'metadata':metadata(),'helpers':{'run.py':pf(P/'run.py'),'probe.mjs':pf(P/'probe.mjs')},'reaper_sha256':pf('/workspace/shared/run-with-reaping.py'),'scope':'Actual published Wolf visible credited Images card and Sauganash curated flying exterior/native arrival. Root releases after all source/publisher writers close. No calibrated source-camera pose, door traversal, full-size viewer, whole-body or original-ticket closure claim.'}
    args.prepare.write_text(json.dumps(plan,indent=2)+'\n');print('Draft only. Root must set both approval booleans true after source/publication writers close.');sys.exit(0)
assert args.run and args.plan and args.plan_sha256 and pf(args.plan)==args.plan_sha256
plan=json.loads(args.plan.read_bytes());assert plan['root_approved']is True and plan['source_check_parts_and_publish_closed']is True
assert plan['source_root']==str(R)and plan['site_parent']==str(R/'site')
assert plan['helpers']=={'run.py':pf(P/'run.py'),'probe.mjs':pf(P/'probe.mjs')}
assert plan['reaper_sha256']==pf('/workspace/shared/run-with-reaping.py')
assert plan['source_scope_sha256']==sha(canonical(plan['input_bindings']))
assert inputs()==plan['input_bindings']and metadata()==plan['metadata']and git('rev-parse','HEAD').decode().strip()==plan['expected_head']
O=Path(plan['output']);T=Path(plan['TMP']);assert O.is_relative_to('/workspace')and T.is_relative_to('/tmp')and not O.is_relative_to(R)and not T.is_relative_to(R)and not O.exists()and not T.exists()
O.mkdir();T.mkdir(mode=0o700);os.sched_setaffinity(0,{0,1,3,4});os.nice(19)
def save(n,value):(O/n).write_text(json.dumps(value,indent=2)+'\n')
def floor():
    v={x:shutil.disk_usage(x).free for x in ['/workspace','/tmp']};assert v['/workspace']>=536870912 and v['/tmp']>=1800000000,v;return v
run_env=dict(E,TMPDIR=str(T),TMP=str(T),TEMP=str(T),NODE_COMPILE_CACHE=str(T/'node-cache'),OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK='1',WOLF_PROBE_PLAN=str(args.plan))
for k in ['SMOKE_ROOT','SMOKE_ENTRY','SMOKE_TARGET','SMOKE_YEAR','SMOKE_PORT','SMOKE_STAGE','SMOKE_VIEWPORT','SMOKE_SHOTS']:run_env.pop(k,None)
before=metadata();steps=[];error=None;closure=None
save('OWNER.json',dict(pid=os.getpid(),at=now(),head=plan['expected_head'],plan=str(args.plan),plan_sha256=args.plan_sha256,resources=floor(),scope=plan['scope']))
try:
    for viewport in ['desktop','mobile']:
        assert metadata()==before and inputs()==plan['input_bindings'];floor()
        env=dict(run_env,WOLF_PROBE_VIEWPORT=viewport,WOLF_PROBE_OUT=str(O/viewport))
        receipt=O/(viewport+'-REAPER.json');log=O/(viewport+'.log')
        command=['python3','/workspace/shared/run-with-reaping.py',str(receipt),'--','timeout','--signal=TERM','--kill-after=15s','600s','nice','-n','19','taskset','-c','0,1,3,4','node',str(P/'probe.mjs')]
        with log.open('xb')as handle:q=subprocess.run(command,cwd=A,env=env,stdout=handle,stderr=subprocess.STDOUT)
        rr=json.loads(receipt.read_bytes());steps.append(dict(viewport=viewport,exit=q.returncode,reaper=rr,reaper_sha256=pf(receipt),log=str(log),log_sha256=pf(log)));save('STEPS.json',steps)
        assert q.returncode==rr['command_exit']==0 and rr['all_children_reaped']and not rr['leftover_cleanup']and rr['interrupted_signal']is None,steps[-1]
        assert json.loads((O/viewport/'RESULT.json').read_bytes())['status']=='ACTUAL_PUBLISHED_COMBINED_WOLF_SAUG_PASS'
        assert metadata()==before and inputs()==plan['input_bindings'];floor()
except BaseException as exc:error=repr(exc)
finally:
    try:
        closure=dict(metadata_unchanged=metadata()==before,selected_source_and_published_inputs_unchanged=inputs()==plan['input_bindings'],plan_unchanged=pf(args.plan)==args.plan_sha256,helpers_unchanged=plan['helpers']=={'run.py':pf(P/'run.py'),'probe.mjs':pf(P/'probe.mjs')},resources=floor())
        assert all(closure[k]for k in ['metadata_unchanged','selected_source_and_published_inputs_unchanged','plan_unchanged','helpers_unchanged'])
    except BaseException as exc:error=(error+'; 'if error else '')+'Closure: '+repr(exc)
save('RESULT.json',dict(status='FOCUSED_PUBLISHED_COMBINED_WOLF_SAUG_BOTH_PASS'if error is None and len(steps)==2 else'FOCUSED_PUBLISHED_COMBINED_WOLF_SAUG_NOT_QUALIFIED',at=now(),head=plan['expected_head'],source_scope_sha256=plan['source_scope_sha256'],steps=steps,closure=closure,error=error,no_retry=True,scope=plan['scope']))
print(json.dumps({'status':json.loads((O/'RESULT.json').read_bytes())['status'],'error':error,'output':str(O)}));sys.exit(1 if error else 0)
