"""Prepared S2 merged-candidate freeze. ROOT supplies reviewed APPLY and actual DEV SHA."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,json,os,re,stat,subprocess
P=Path(__file__).resolve().parent
S='3d2d9b356db02deed9d406422f754af4de7aa5f0'
PRIMARY='steward/t1789-charles-woven-coat-20261110'
OLD_ENTRY='chicago/4d/changelog.d/T1789.json'
FIXTURE='chicago/4d/data/humans/fixture.measure.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def path_name(name):
    q=PurePosixPath(name);assert not q.is_absolute() and '..' not in q.parts and '.git' not in q.parts and q.as_posix()==name
    return name
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected-head',required=True)
    parser.add_argument('--incoming-dev',required=True)
    parser.add_argument('--apply-receipt',type=Path,required=True)
    parser.add_argument('--apply-receipt-sha256',required=True)
    parser.add_argument('--baseline-freeze',type=Path,default=Path('/tmp/t1789-settler-linen-source-full-gate-prep-20261111/FREEZE.json'))
    a=parser.parse_args();assert a.expected_head==S
    assert re.fullmatch('[0-9a-f]{40}',a.incoming_dev) and a.incoming_dev.startswith('900d')
    assert sha(a.apply_receipt)==a.apply_receipt_sha256
    assert not (P/'FREEZE.json').exists() and not (P/'READY.json').exists()
    baseline=json.loads(a.baseline_freeze.read_text());old={r['file']:r for r in baseline['rows']}
    assert len(old)==baseline['frozen_file_count']==302
    assert sha(a.baseline_freeze)=='ec890f5f94ccc4493f7aa2660abb53cc138f553d40350c537d33cb0e02655528'
    root=Path(baseline['root']);wrapper=Path(baseline['wrapper'])
    assert sha(wrapper)==baseline['wrapper_SHA256']
    env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0')
    def git(*args):return subprocess.check_output(['git','-C',str(root),*args],env=env).decode().strip()
    apply=json.loads(a.apply_receipt.read_text())
    assert apply['head']==S and apply['incoming_dev']==a.incoming_dev
    assert re.fullmatch('[0-9a-f]{40}',apply['index_tree'])
    admitted={};deleted=set(apply.get('deleted_paths',[]))
    for r in apply.get('files',apply.get('rows',[])):
        name=path_name(r.get('file',r.get('path')))
        if r.get('status')=='D':deleted.add(name)
        else:assert name not in admitted;admitted[name]=r
    assert deleted=={OLD_ENTRY} and OLD_ENTRY not in admitted, 'Only explicitly folded old entry is deleted'
    changed=set(admitted)|deleted
    assert git('rev-parse','HEAD')==S and git('rev-parse','HEAD^{tree}')==baseline['index_tree']
    assert git('branch','--show-current')==baseline['branch'] and baseline['branch']!=PRIMARY
    assert git('rev-parse','--verify',baseline['protected_ref'])==baseline['protected_ref_head']
    gitdir=Path(git('rev-parse','--absolute-git-dir'))
    assert (gitdir/'MERGE_HEAD').read_text().strip()==a.incoming_dev
    assert git('ls-files','-u')=='' and git('diff','--name-only')==''
    statuses=dict(line.split('\t',1)[::-1] for line in git('diff','--cached','--name-status').splitlines())
    assert set(statuses)==changed and statuses[OLD_ENTRY]=='D'
    assert all(statuses[p] in ['M','A'] for p in admitted)
    if 'staged_paths' in apply:assert set(apply['staged_paths'])==changed
    assert git('write-tree')==apply['index_tree'];git('diff','--cached','--check')
    protected={path for path in old if '/assets/' in path or path==FIXTURE or path.lower().endswith(('.glb','.png','.jpg','.jpeg','.webp','.ktx2','.bin','.wav','.mp3','.ogg','.opus','.pdf'))}
    assert not protected&changed and FIXTURE in protected
    native8={'chicago/4d/assets/humans/'+prefix+'settler_1812.lod'+str(lod)+'.glb' for prefix in ['', 'web/'] for lod in range(4)}
    assert native8<=protected
    for path in admitted:
        assert '/assets/' not in path and path!=FIXTURE and not path.lower().endswith(('.glb','.png','.jpg','.jpeg','.webp','.ktx2','.bin','.wav','.mp3','.ogg','.opus','.pdf'))
    for path in deleted:assert not (root/path).exists() and not (root/path).is_symlink()
    paths=sorted((set(old)|set(admitted))-deleted);index={}
    for line in git('ls-files','--stage','--',*paths).splitlines():
        meta,path=line.split('\t',1);mode,oid,stage=meta.split();assert stage=='0';index[path]=(mode,oid)
    assert set(index)==set(paths)
    rows=[]
    for path in paths:
        path_name(path);p=root/path;info=p.lstat();assert stat.S_ISREG(info.st_mode) and not p.is_symlink() and p.resolve().is_relative_to(root.resolve())
        mode='100755' if info.st_mode&stat.S_IXUSR else '100644';size=info.st_size
        h=hashlib.sha256();b=hashlib.sha1(b'blob '+str(size).encode()+b'\0')
        with p.open('rb') as f:
            for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk);b.update(chunk)
        row={'file':path,'bytes':size,'sha256':h.hexdigest(),'Git_mode':mode,'Git_blob_OID':b.hexdigest()}
        assert index[path]==(mode,row['Git_blob_OID']),path
        if path in old and path not in changed:assert all(row[k]==old[path][k] for k in ['bytes','sha256','Git_mode']),path
        if path in admitted:
            assert all(row[k]==admitted[path][k] for k in ['bytes','sha256']),path
            if 'Git_mode' in admitted[path]:assert mode==admitted[path]['Git_mode'],path
        rows.append(row)
    freeze={'status':'S2_NORMAL_DEV_MERGE_PLUS_REVIEWED_SOURCE_FIXES_GATE_PENDING','head':S,'incoming_dev':a.incoming_dev,
        'branch':baseline['branch'],'root':str(root),'protected_ref':baseline['protected_ref'],'protected_ref_head':baseline['protected_ref_head'],
        'wrapper':str(wrapper),'wrapper_SHA256':baseline['wrapper_SHA256'],'index_tree':apply['index_tree'],
        'frozen_file_count':len(rows),'rows':rows,'expected_staged_paths':sorted(changed),'deleted_paths':sorted(deleted),
        'deleted_old_entry':old[OLD_ENTRY],'baseline302_SHA256':sha(a.baseline_freeze),'baseline_preserved_except_explicit_staged_paths':True,
        'protected_native_and_fixture_paths':sorted(protected),'old_native8_and_current_fixture_byte_exact':True,
        'old_source_exceptions':sorted(set(old)&changed),'no_new_native_changelog_entry':True,'native_asset_adoption':False,
        'apply_receipt':str(a.apply_receipt),'apply_receipt_SHA256':sha(a.apply_receipt),'parts':16,
        'failed_prior_capture':{'source':S,'run':43000644195,'actual_status':'FIRST_FAILURE_BEFORE_GEOMETRY_LTS_VERSION_LITERAL','new_parents':False},
        'source_gate':'PENDING_ALL16','future_S2_H2_run':'UNKNOWN_UNTIL_ACTUAL_NEW_COMMIT_AND_SEPARATE_REVIEW','native_bake_fixture_pose_photo':'PENDING','commit':False,'push':False}
    (P/'FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
    pin=sha(P/'FREEZE.json');(P/'READY.json').write_text(json.dumps({'freeze_SHA256':pin,'index_tree':apply['index_tree'],'frozen_file_count':len(rows),'parts':16},indent=2)+'\n')
    print(json.dumps({'freeze_SHA256':pin,'parts':16,'files':len(rows),'native8_fixture_unchanged':True}))
