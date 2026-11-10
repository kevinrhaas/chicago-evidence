#!/usr/bin/env python3
"""Break the exact predicates actually used by the successful frozen-owner audit."""
from pathlib import Path
import ast,copy,json,subprocess
O=Path(__file__).resolve().parent;tree=ast.parse((O/'audit-retained.py').read_text());audit=next(x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name=='audit')
def predicate(text):
 matches=[]
 for x in ast.walk(audit):
  if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='require'and len(x.args)>1:
   if any(isinstance(v,ast.Constant)and isinstance(v.value,str)and text in v.value for v in ast.walk(x.args[1])):matches.append(x.args[0])
 assert len(matches)==1,(text,len(matches));return compile(ast.Expression(matches[0]),'actual successful native audit predicate','eval')
full=predicate('Retained target sidecar is not actual frozen owner output');binding=predicate('Target sidecar ID/scene/asset binding mismatch')
raw=subprocess.check_output(['git','show','d6076c038f5d7e103c922110b568c3188436ec25:chicago/4d/data/sidecars/1812/kinzie_house_1812.json'],cwd='/tmp/chicago-west-wicket-20261109');expected=json.loads(raw);sid=expected['id'];selected={'asset_key':expected['asset'][5:]};rows=[]
def test(name,sc,ok,pred=full,selection=None):
 value=eval(pred,{'newsc':sc,'sid':sid,'expected_sidecars':{sid:expected},'selected':selection or selected});assert bool(value)==ok,name;rows.append({'case':name,'expected_accept':ok,'actual_accept':bool(value)})
test('entire actual target owner output',copy.deepcopy(expected),True)
for name,edit in [('shifted placement',lambda d:d['placement'].update(local_e=d['placement']['local_e']+1)),('invented height',lambda d:d['attributes']['end_door_height_m'].update(value=2.6)),('rights/confidence upgrade',lambda d:d['attributes']['log_finish'].update(confidence='attested')),('changed explanatory source note',lambda d:d['attributes']['construction'].update(note='unbound rewrite')),('unbound native asset',lambda d:d.update(asset='gltf/not-the-bound-target.glb'))]:
 sc=copy.deepcopy(expected);edit(sc);test(name,sc,False)
test('actual target native binding',expected,True,binding)
test('different selected native MASTER',expected,False,binding,{'asset_key':'other.glb'})
receipt={'status':'PASS_EXACT_SIDECAR_AUDIT_PREDICATE_NEGATIVES','cases':rows,'owner_ground_truth':'Both actual retained sidecars were independently rederived in full from pinned6b compile_scene build_sidecar AST before this predicate test.','claim_limit':'These tests execute the exact full-equality and native-binding predicates in the successful audit; they do not add an allowed path or change source/native verdicts.'};(O/'SIDECAR-NEGATIVE-FIXTURES.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS',len(rows),'actual full-sidecar/binding predicate cases')
