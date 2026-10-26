"""CPU-only proposal validation. Does not execute CI, BPy, publishers or browsers."""
from pathlib import Path
import ast, hashlib, json, os, re, shutil, subprocess, tempfile
import yaml

HERE=Path(__file__).parent
ROOT=Path('/tmp/chicago-photo-worker-t1789-20261026')
REL='.github/workflows/chicago-4d-humans.yml'
SOURCE='1cbb1817508593562f99ed378b6932368b5699b9'
base=(ROOT/REL).read_text()
text=(HERE/'chicago-4d-humans.yml').read_text()
doc=yaml.load(text,Loader=yaml.BaseLoader)
old=yaml.load(base,Loader=yaml.BaseLoader)
checks=[]
def require(ok,label):
    checks.append({'check':label,'passed':bool(ok)})
    if not ok:raise AssertionError(label)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

require(subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==SOURCE,'exact checked base HEAD')
require(not subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT,text=True),'checked source and index clean')
applied=subprocess.run(['git','apply','--check',str(HERE/'APPLICATION.diff')],cwd=ROOT,capture_output=True,text=True)
require(applied.returncode==0,'normal native git apply --check; no application')
require(re.findall(r'^\+\+\+ b/(.+)$',(HERE/'APPLICATION.diff').read_text(),re.M)==[REL],'patch modifies only existing registered workflow')
require(doc['on']['pull_request']==old['on']['pull_request'] and doc['on']['push']==old['on']['push'],'PR/push triggers unchanged')
for key in ['permissions','concurrency']:
    require(doc[key]==old[key],key+' unchanged')
for key,value in old['on']['workflow_dispatch']['inputs'].items():
    require(doc['on']['workflow_dispatch']['inputs'][key]==value,'existing input preserved: '+key)
require(doc['on']['workflow_dispatch']['inputs']['build_dress_study']['default']=='false','dress opt-in default false')
require(doc['on']['workflow_dispatch']['inputs']['source_ref']['default']=='','source-ref default empty')
require(set(doc['jobs'])=={'humans','teamster-studies','dress-study'},'exact three-job graph')
male_new={k:v for k,v in doc['jobs']['teamster-studies'].items() if k!='runs-on'}
male_old={k:v for k,v in old['jobs']['teamster-studies'].items() if k!='runs-on'}
require(male_new==male_old,'entire male job unchanged except accepted runner fix')
require(doc['jobs']['teamster-studies']['runs-on']=='ubuntu-24.04','accepted T3169 runner fix explicit')
humans=doc['jobs']['humans']['steps']
require(humans[4:]==old['jobs']['humans']['steps'][1:],'all existing fixture setup/byte/browser/actor steps unchanged')
require(humans[1]['uses']==old['jobs']['humans']['steps'][0]['uses'],'original default checkout action retained')
require(humans[1]['if']=="github.event_name != 'workflow_dispatch' || !inputs.build_dress_study",'default checkout selected on PR/push/non-dress dispatch')
require(humans[2]['with']=={'ref':'${{ steps.study_request.outputs.source_sha }}','persist-credentials':'false'},'study checkout only uses guard output and does not persist credentials')
require(doc['jobs']['dress-study']['needs']=='humans','dress depends on passing same-source full fixture job')
require(doc['jobs']['dress-study']['if']=="github.event_name == 'workflow_dispatch' && inputs.build_dress_study",'dress job only opt-in dispatch')
require(doc['jobs']['dress-study']['steps'][0]['with']=={'ref':'${{ needs.humans.outputs.dress_source_sha }}','persist-credentials':'false'},'dress checkout bound to prerequisite verified source output')
require(doc['permissions']=={'contents':'read'} and 'secrets.' not in text and 'pull_request_target' not in doc['on'],'read-only scope/no secret or privileged PR trigger')
require(all(job['runs-on']=='ubuntu-24.04' for job in doc['jobs'].values()),'all three jobs use explicit accepted Ubuntu24 image')

runner_path=Path('/tmp/chicago-photo-worker-t2793-20261026/chicago/4d/tools/check_runner_images.py')
runner={'__file__':str(runner_path),'__name__':'native_runner_checker_for_external_proposal'}
exec(compile(runner_path.read_text(),str(runner_path),'exec'),runner)
runner_violations=runner['violations'](REL,text)
require(not runner_violations,'native runner-image checker violations() passes actual proposed YAML')
require(bool(runner['violations'](REL,base)),'native runner-image checker detects old base floating job')

inline=[];shell_count=0
with tempfile.TemporaryDirectory(prefix='dress-workflow-static-',dir=HERE) as td:
    scratch=Path(td)
    for jobid,job in doc['jobs'].items():
        for number,step in enumerate(job['steps']):
            script=step.get('run')
            if script is None:continue
            p=scratch/f'{jobid}-{number}.sh';p.write_text(script)
            result=subprocess.run(['bash','-n',str(p)],capture_output=True,text=True)
            require(result.returncode==0,f'bash -n {jobid} step{number}')
            shell_count+=1
            for language,body in re.findall(r"<<'(PY|JS)'\n(.*?)\n\1(?:\n|$)",script,re.S):
                if language=='PY':ast.parse(body)
                else:
                    js=scratch/f'{jobid}-{number}.js';js.write_text(body)
                    result=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
                    require(result.returncode==0,f'node --check {jobid} step{number}')
                inline.append({'job':jobid,'step':number,'language':language,'syntax_passed':True})

    request=humans[0]['run']
    guard=re.search(r"<<'PY'\n(.*?)\nPY(?:\n|$)",request,re.S).group(1)
    require('${{' not in guard,'guard never interpolates inputs as Python/shell source')
    cases=[
        ('default dispatch',False,False,False,'',True),
        ('existing male',False,True,False,'',True),
        ('existing seated',False,False,True,'',True),
        ('existing male plus seated',False,True,True,'',True),
        ('reviewed dress source',True,False,False,SOURCE,True),
        ('empty dress source',True,False,False,'',False),
        ('malformed source',True,False,False,'dev',False),
        ('nonallowlisted immutable SHA',True,False,False,'f'*40,False),
        ('uppercase source',True,False,False,SOURCE.upper(),False),
        ('source without dress',False,False,False,SOURCE,False),
        ('dress mixed with male',True,True,False,SOURCE,False),
        ('dress mixed with seated',True,False,True,SOURCE,False),
        ('shell text in source',True,False,False,'$(touch '+str(scratch/'injection-marker')+')',False),
        ('newline output injection',True,False,False,SOURCE+'\ninjected=value',False),
    ]
    matrix=[]
    for number,(label,dress,male,seated,source,want) in enumerate(cases):
        output=scratch/f'guard-{number}.out'
        env=dict(os.environ,DRESS_ENABLED=str(dress).lower(),TEAMSTERS_ENABLED=str(male).lower(),
                 SEATED_ENABLED=str(seated).lower(),SOURCE_REF=source,GITHUB_OUTPUT=str(output))
        result=subprocess.run(['python3','-c',guard],env=env,capture_output=True,text=True)
        got=result.returncode==0
        require(got==want,'actual inline request guard: '+label)
        contents=output.read_text() if output.exists() else ''
        if want:require(contents=='source_sha='+source+'\n','exact validated output: '+label)
        else:require(not contents,'invalid request emits no checkout source: '+label)
        matrix.append({'case':label,'dress':dress,'teamsters':male,'seated':seated,
            'source_ref':source,'expected_accepted':want,'actual_exit_code':result.returncode,
            'actual_checkout_output':contents,'expected_jobs_after_guard':
            (['humans','dress-study'] if dress else ['humans']+(['teamster-studies'] if male or seated else [])) if want else [],
            'note':'job list is static job-condition analysis; jobs were not executed'})
    require(not (scratch/'injection-marker').exists(),'shell input never executed')

dress_text=text.split('\n  dress-study:\n',1)[1]
for command in ['tools/test_human_dress_components.py','--source-manifest SOURCE-female.json',
                'tools/compile_scene.py --scene 1835','tools/human_teamster_blend.py',
                '--recipe data/humans/recipes/adult_dress_1835.json --variant flynn_mary_1835_dress_study',
                '--experimental-normal-probes','bash tools/human_export.sh --master',
                'tools/human_hierarchy_control.py -- --test-only-parented-control',
                'tools/human_skin_canonicalize.py','tools/audit_human_animation_times.py',
                'tools/check_human_hair.py --assets assets/humans --asset-ids flynn_mary_1835_dress_study',
                'tools/validate_hierarchy_controls.mjs','tools/human_fixture.mjs --write',
                'bash tools/publish.sh','tools/test_human_inspection.mjs',
                '--published --sole-contact','--masters --sole-contact','--frame-samples 21']:
    require(command in dress_text,'required existing native command retained: '+command)
require("for(const dir of ['assets/humans','assets/humans/web'])for(let lod=0;lod<4;lod++)" in dress_text,'Khronos explicitly opens all eight actual new files')
require('cp data/humans/fixture.measure.json /tmp/dress-study/fresh-fixture.measure.json' in dress_text,'only successful fresh measurement copied as artifact')
require('chicago/4d/data/humans/fixture.measure.json' not in dress_text,'failure upload does not include a carried stale measure file')
require('resident-dress-study-${{ needs.humans.outputs.dress_source_sha }}' in dress_text,'artifact name binds actual source SHA, not definition SHA')
require('--sit-drive-study' not in dress_text,'no unsupported dress seated assignment')
require(all('permissions' not in job or job['permissions']=={'contents':'read'} for job in doc['jobs'].values()),'no job permission override expands the read-only token')

report={'scope':'EXTERNAL proposal/static validation only; no workflow edit or service dispatch, BPy, browser, publisher or installs',
    'source_commit':SOURCE,'base_workflow_sha256':hashlib.sha256(base.encode()).hexdigest(),
    'proposed_yaml_sha256':sha(HERE/'chicago-4d-humans.yml'),'patch_sha256':sha(HERE/'APPLICATION.diff'),
    'native_runner_checker':{'path':str(runner_path),'sha256':sha(runner_path),'violations':runner_violations},
    'yaml_parser':'PyYAML '+yaml.__version__+' BaseLoader (on key preserved)',
    'shell_blocks_syntax_checked':shell_count,'inline_blocks':inline,'checks':checks,'request_guard_matrix':matrix,
    'unexecuted':['actionlint not installed; no installation authorized',
        'GitHub workflow schema/expression evaluation and actual job graph execution',
        'whole repository native preflight for any future adopted workflow commit',
        'same-source fixture/BPy/master/export/browser/contact/photo gates',
        'official artifact ingestion while host policy remains unapplied'],
    'clean_after':not subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT,text=True)}
require(report['clean_after'],'app remains clean after external validation')
(HERE/'SOURCE-BOUND-VALIDATION-MATRIX.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(checks),'guard_cases':len(matrix),'shell_blocks':shell_count,
                  'inline_blocks':len(inline),'proposal_sha256':report['proposed_yaml_sha256'],'clean':report['clean_after']}))
