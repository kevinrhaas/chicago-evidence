import sys,pathlib,json,os
sys.path.insert(0,"/workspace/shared");import owned_child_reaper_20261023 as o
o.enable();d=pathlib.Path(__file__).parent/"LIVE-JOBS-ONCE";d.mkdir(exist_ok=False)
try:
 for r in [40004752292,40004752222]:
  f=d/(str(r)+".json");v=o.run(["gh","api",f"repos/kevinrhaas/chicago/actions/runs/{r}/jobs?per_page=100"],"/workspace/chicago-waistcoat",os.environ.copy(),f,90);assert v["returncode"]==0
  j=json.loads(f.read_text());print(r,[{"job":x["name"],"status":x["status"],"conclusion":x["conclusion"],"steps":[(s["name"],s["status"],s["conclusion"])for s in x.get("steps",[])if s["status"]!="queued"]}for x in j["jobs"]],flush=True)
finally:(d/"CLEANUP.json").write_text(json.dumps(o.finish()))
