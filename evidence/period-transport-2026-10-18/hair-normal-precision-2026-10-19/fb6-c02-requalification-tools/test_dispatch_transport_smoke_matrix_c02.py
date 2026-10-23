import importlib.util,pathlib,json,sys,unittest
from unittest.mock import patch
s=importlib.util.spec_from_file_location('d','/workspace/shared/dispatch_transport_smoke_matrix_c02.py');d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
class Dispatcher(unittest.TestCase):
 def test_priority_exact_grid_and_duplicate_negative(self):
  cells=d.cells();self.assertEqual(cells[:4],[('desktop','13'),('desktop','14'),('desktop','9-12'),('mobile','13')]);self.assertEqual(len(set(cells)),18)
  with patch.object(d,'PRIORITY',d.PRIORITY+[('desktop','13')]):
   with self.assertRaises(ValueError):d.cells()
 def test_mock_posts_require_persisted_intent_and_frozen_head(self):
  sha='ab'*20;out=pathlib.Path('/workspace/shared/transport-smoke-dispatch-c02-'+sha[:9]+'.json');self.assertFalse(out.exists());posts=[];heads=[]
  def api(endpoint,body=None):
   if '/git/ref/'in endpoint:heads.append(sha);return {'object':{'sha':sha}}
   if body is not None:
    receipt=json.loads(out.read_text());last=receipt['dispatches'][-1];self.assertFalse(last['post_succeeded']);self.assertEqual((last['viewport'],last['stage']),(body['inputs']['viewport'],body['inputs']['stage']));self.assertEqual(len(heads),len(posts)+2);posts.append(body);return None
   rows=[]if not posts else [{'id':i+1,'head_sha':sha,'run_attempt':1,'status':'queued','conclusion':None,'created_at':'mock','html_url':'mock'}for i in range(18)]
   return {'workflow_runs':rows}
  with patch.object(d,'api',side_effect=api),patch.object(sys,'argv',['dispatch',sha]):d.main()
  self.assertEqual([(p['inputs']['viewport'],p['inputs']['stage'])for p in posts],d.cells());r=json.loads(out.read_text());self.assertTrue(all(p['post_succeeded']for p in r['dispatches']));self.assertEqual(len(r['discovered_runs']),18);out.rename('/workspace/shared/c02-validator-review/mock-dispatch-receipt.json')
 def test_wrong_head_prevents_all_posts(self):
  with patch.object(d,'api',return_value={'object':{'sha':'0'*40}})as api,patch.object(sys,'argv',['dispatch','cd'*20]):
   with self.assertRaises(SystemExit):d.main()
  self.assertEqual(api.call_count,1)
if __name__=='__main__':unittest.main()
