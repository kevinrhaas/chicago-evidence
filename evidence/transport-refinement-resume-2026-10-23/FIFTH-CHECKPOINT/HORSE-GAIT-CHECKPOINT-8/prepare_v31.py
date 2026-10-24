from pathlib import Path
import shutil
r=Path(__file__).parent;d=r/'V31-SPLIT-PORTABLE-CREEPING-PROTOTYPE';d.mkdir(exist_ok=False)
for name in ['read_native_mixer.mjs','check_actual_readback.py']:shutil.copy2(r/'V30-PORTABLE-CREEPING-PROTOTYPE'/name,d/name)
print(d)
