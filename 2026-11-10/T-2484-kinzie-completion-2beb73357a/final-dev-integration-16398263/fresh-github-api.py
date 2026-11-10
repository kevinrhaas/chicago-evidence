"""Use inherited managed proxy/CA and API credentials. No Authorization header.
A stale explicit GH_TOKEN caused401; no route, CA or proxy bypass is used.
"""
import urllib.request,urllib.error,json,time
BASE='https://api.github.com/'
def api(endpoint,data=None,method=None):
 raw=None if data is None else json.dumps(data).encode()
 headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'chicago-t2484-completion'}
 if raw is not None:headers['Content-Type']='application/json'
 for attempt in range(5):
  req=urllib.request.Request(BASE+endpoint,data=raw,headers=headers,method=method or('POST'if data is not None else'GET'))
  try:
   with urllib.request.urlopen(req,timeout=60)as r:return json.load(r)
  except urllib.error.HTTPError as e:
   if e.code not in [429,502,503,504]or attempt==4:raise
   time.sleep(min(int(e.headers.get('Retry-After','2')),10)+attempt)
