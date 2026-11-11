from pathlib import Path
import json,os,subprocess,sys
P=Path(__file__).resolve().parent
part=int(sys.argv[1]);assert part in range(1,17)
d=json.loads((P/'FREEZE.json').read_text())
os.chdir(Path(d['root'])/'chicago/4d')
os.environ['C4D_GATE_REQUIRE_READERS']='1'
os.environ['CHECK_TIMINGS']=str(P/f'part{part}.timings.tsv')
subprocess.run([sys.executable,str(P/'verify.py')],check=True)
subprocess.run(['./tools/check.sh','--part',f'{part}/16'],check=True)
subprocess.run([sys.executable,str(P/'verify.py')],check=True)
