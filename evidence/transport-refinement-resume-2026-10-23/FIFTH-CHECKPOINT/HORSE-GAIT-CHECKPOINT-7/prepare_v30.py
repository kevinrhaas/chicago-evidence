from pathlib import Path
import shutil
r=Path(__file__).parent;d=r/'V30-PORTABLE-CREEPING-PROTOTYPE';d.mkdir(exist_ok=False)
shutil.copy2(r/'V29-COHERENT-BASIS-STUDY/analyze_basis.py',d/'basis.py')
print(d)
