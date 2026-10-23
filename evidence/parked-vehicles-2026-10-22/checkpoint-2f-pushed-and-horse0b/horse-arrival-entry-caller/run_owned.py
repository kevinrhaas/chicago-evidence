"""HELD finite caller. Uses the already reviewed native-capture supervisor unchanged."""
import argparse,json,pathlib,sys
sys.path.insert(0,'/workspace/shared/horse-sevket-native-preview-source-20261022')
from ownership_supervisor import run_owned
p=argparse.ArgumentParser();p.add_argument('--lane-released',action='store_true',required=True)
p.add_argument('--phase',choices=['materials','yard-desktop','yard-mobile'],required=True)
p.add_argument('--release-file',required=True);p.add_argument('--output-dir',required=True);a=p.parse_args()
here=pathlib.Path(__file__).resolve().parent;out=pathlib.Path(a.output_dir)
if out.exists():raise SystemExit('Refuse existing capture output; no automatic retry')
whole = 180 if a.phase == 'materials' else 360
r=run_owned(['node',str(here/'capture_smoke.mjs'),'--lane-released',a.phase,str(pathlib.Path(a.release_file).resolve()),str(out)],out.with_name(out.name+'-terminal'),whole_timeout=whole,execution_timeout=whole-10)
print(json.dumps(r,indent=2));raise SystemExit(r['exit_code'])
