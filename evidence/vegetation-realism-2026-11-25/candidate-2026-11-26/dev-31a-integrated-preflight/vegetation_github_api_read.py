"""Read GitHub metadata through the environment's existing authenticated route."""
import json,sys,urllib.request
def read(path):
 assert path.startswith(('repos/kevinrhaas/chicago/','repos/kevinrhaas/chicago-tickets/','repos/kevinrhaas/chicago-dev/')),path
 request=urllib.request.Request('https://api.github.com/'+path,headers={'Accept':'application/vnd.github+json','Cache-Control':'no-cache'})
 # The managed connection supplies current authentication. An expired GH_TOKEN
 # must not override it; no credential is copied, created, persisted or printed.
 with urllib.request.urlopen(request,timeout=30) as response:
  assert response.status==200
  return json.load(response)
if __name__=='__main__':
 assert len(sys.argv)==2
 print(json.dumps(read(sys.argv[1])))
