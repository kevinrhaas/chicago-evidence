from pathlib import Path
import sys,json,copy
F=Path('/tmp/chicago-west-wicket-20261109/chicago/4d');O=Path('/tmp/nov10-cobweb-complete/yard-rederive');sys.path.insert(0,str(F/'tools'))
import generate_woodpiles as g
import check_structure_clearance as c
# Check the exact official rederived JSON using the real CLI against FULL inputs.
# OUT's basename stays the original basename, preserving exclusion of this layer
# from its own obstacles; only the destination/readback path is external.
g.OUT=O/'town_woodpiles.json';sys.argv=['generate_woodpiles.py','--check'];assert g.main()==0
# Run the existing full clearance self-test with only the generated layer
# replaced in its fixture loader. Every other input and assertion stays actual.
original=c.layer_files;after=json.loads(g.OUT.read_text())
def corrected_layers():
    layers=original();layers['yard/town_woodpiles.json']=copy.deepcopy(after);return layers
c.layer_files=corrected_layers
assert c.self_test()==0
