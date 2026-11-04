"""Publish ACTUAL reviewed rootGO BEFORE dispatch. No ticket edits or dispatch."""
from pathlib import Path
import json,hashlib,subprocess,urllib.request
P=Path(__file__).parent;PREFIX='evidence/sauganash-2026-11-04/stacks-native-execution-authorization/'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert not(P/'DISPATCH-ATTEMPT.json').exists(),'No authorization republishing after a POST attempt'
gobytes=(P/'ROOT-GO.json').read_bytes();go=json.loads(gobytes);expected=json.loads((P/'ARTIFACT-HASHES.json').read_bytes());actual={'request':sha((P/'REQUEST.json').read_bytes()),'patch':sha((P/'UNQUALIFIED-DATA-ONLY.patch').read_bytes()),'handoff':sha((P/'HANDOFF.md').read_bytes()),'controller':sha((P/'controller.py').read_bytes())}
assert actual==expected==go.get('artifacts')and go.get('authorized')is True and go.get('feature')=='7b427d130a2cca6ed82c183c74605b965aee1d4e' and go.get('prepared_sha256')==sha((P/'PREPARED.json').read_bytes()),'Exact rootGO required'
Q=P/('GO-PUBLICATION-'+sha(gobytes)[:12]);Q.mkdir(exist_ok=True)
if not(Q/'PUBLISHED.json').exists():
 (Q/'ROOT-GO.json').write_bytes(gobytes)
 (Q/'EXECUTION-AUTHORIZATION.json').write_text(json.dumps({'authorized':True,'root_go_sha256':sha(gobytes),'feature':go['feature'],'target_ticket':'T-2383','lane':'sauganash-stacks-native-20261104','artifacts':actual,'prepared_sha256':go['prepared_sha256'],'matching_reviewed_controller_dispatch_authorizes_bounded_native_execution':True,'no_second_review_needed_for_actual_matching_run':True,'native_only':'GitHub Ubuntu26.04/Blender4.5.3; no shared host GPU'},indent=2)+'\n')
 spec={'prefix':PREFIX,'message':'Publish exact reviewed Sauganash stacks executionGO BEFORE any nativePOST','receipt':str(Q/'PUBLISHED.json'),'files':{n:str(Q/n)for n in ['ROOT-GO.json','EXECUTION-AUTHORIZATION.json']}};(Q/'SPEC.json').write_text(json.dumps(spec,indent=2)+'\n')
 r=subprocess.run(['python','/workspace/shared/publish-evidence-files.py','--manifest',str(Q/'SPEC.json')],timeout=500);assert r.returncode==0
receipt=json.loads((Q/'PUBLISHED.json').read_bytes());assert receipt['files']['ROOT-GO.json']['sha256']==sha(gobytes)
u='https://raw.githubusercontent.com/kevinrhaas/chicago-evidence/'+receipt['commit']+'/'+PREFIX+'ROOT-GO.json'
with urllib.request.urlopen(u,timeout=30)as r:assert r.read()==gobytes
(P/'PUBLIC-GO-RECEIPT.json').write_bytes((Q/'PUBLISHED.json').read_bytes());print(json.dumps({'actual_GO_public_BEFORE_POST':True,'commit':receipt['commit'],'immutable_GO_url':u,'root_go_sha256':sha(gobytes)}),flush=True)
