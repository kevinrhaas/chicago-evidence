"""Unarmed by default: reviewed SOURCE push, cancel its own auto bake, one scoped POST.

No workflow edits. No operation is authorized by this file alone. Full local
SOURCE/metadata qualification, public immutable intent and exact root GO are
mandatory; the pending template deliberately cannot execute.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import time
import datetime
from urllib.parse import quote

P = Path(__file__).parent
REPO = "repos/kevinrhaas/chicago/"
BRANCH = "codex/t2383-finite-signoff-review-20261104"
WORKFLOW = "chicago-4d-bake.yml"
PR = 1705
sha = lambda b: hashlib.sha256(b).hexdigest()
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["prepare", "execute", "dispatch-after-cancel"], default="prepare")
parser.add_argument("--intent", type=Path, default=P / "SOURCE-INTENT.template.json")
parser.add_argument("--prepared", type=Path, default=P / "PREPARED.json")
parser.add_argument("--go", type=Path)
parser.add_argument("--go-sha256")
parser.add_argument("--public-go-url")
parser.add_argument("--public-intent-url")
args = parser.parse_args()
intent_bytes = args.intent.read_bytes()
I = json.loads(intent_bytes)
if not re.fullmatch(r"[0-9a-f]{40}", I.get("source_head") or ""):
    raise SystemExit("UNARMED: full local SOURCE/fast-owner qualification has not been prepared")
H, T = I["source_head"], I["source_tree"]
assert re.fullmatch(r"[0-9a-f]{40}", T)
assert I["branch"] == BRANCH and I["parent_pr"] == PR
assert I["family_output_count"] == 25 and I["non_hotel_control_count"] == 24
assert len(I["only_ids"]) == len(set(I["only_ids"])) == 23
assert I["only_ids"] == sorted(I["only_ids"])
BODY = {"ref": BRANCH, "inputs": {"only": ",".join(I["only_ids"])}}
assert BODY == I["exact_dispatch_body"]
R = Path(I["local_source_repo"])
A = R / "chicago/4d"
E = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_OPTIONAL_LOCKS="0", PYTHONDONTWRITEBYTECODE="1")
O = P / ("attempt-" + H)
O.mkdir(exist_ok=True)


def save(name, value):
    (O / name).write_text(json.dumps(value, indent=2) + "\n")


def reserve(name, value):
    fd = os.open(O / name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(value, f, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())


def api(endpoint):
    r = subprocess.run(["gh", "api", "-H", "Cache-Control: no-cache", REPO + endpoint], capture_output=True, timeout=20)
    if r.returncode:
        raise RuntimeError(r.stderr.decode())
    return json.loads(r.stdout)


def proper_command(command, label, limit):
    receipt = O / (label + "-REAPER.json")
    assert not receipt.exists()
    helper = "/workspace/shared/run-with-reaping.py"
    r = subprocess.run(["python", helper, str(receipt), "--", "timeout", "--signal=TERM", "--kill-after=10s", str(limit) + "s", *command], capture_output=True, timeout=limit + 30, env=E)
    closed = json.loads(receipt.read_bytes())
    assert closed["all_children_reaped"] and not closed["leftover_cleanup"]
    return r


def post_once(endpoint, body, expected_status, reservation, result_name):
    reserve(reservation, {"source_head": H, "endpoint": endpoint, "body": body, "reserved_unix": time.time(), "retry_forbidden": True})
    payload = O / (result_name + ".request.json")
    payload.write_text(json.dumps(body))
    try:
        r = proper_command(["gh", "api", "--include", REPO + endpoint, "--method", "POST", "--input", str(payload)], result_name, 40)
        ok = r.returncode == 0 and re.search(rb"^HTTP/\S+\s+" + str(expected_status).encode() + rb"(?:\s|\r|\n|$)", r.stdout, re.M) is not None
        result = {"accepted": ok, "returncode": r.returncode, "stdout": r.stdout.decode(errors="replace"), "stderr": r.stderr.decode(errors="replace")}
    except BaseException as exc:
        ok = False
        result = {"accepted": False, "unknown": True, "error": repr(exc)}
    result.update({"endpoint": endpoint, "source_head": H, "one_invocation": True, "retry_forbidden": True})
    save(result_name, result)
    return ok


def git(*argv):
    return subprocess.check_output(["git", "-C", str(R), *argv], env=E)


def local_guards():
    assert git("rev-parse", "HEAD").decode().strip() == H
    assert git("rev-parse", H + "^{tree}").decode().strip() == T
    assert git("symbolic-ref", "--short", "HEAD").decode().strip() == BRANCH
    assert not git("status", "--porcelain"), "SOURCE must be clean and immutable"
    origin = git("remote", "get-url", "origin").decode().strip()
    allowed_urls = {"https://github.com/kevinrhaas/chicago.git", "https://github.com/kevinrhaas/chicago", "git@github.com:kevinrhaas/chicago.git", "ssh://git@github.com/kevinrhaas/chicago.git"}
    assert origin in allowed_urls, "Origin fetch URL is not Chicago"
    push_urls = git("remote", "get-url", "--push", "--all", "origin").decode().splitlines()
    assert len(push_urls) == 1 and push_urls[0] in allowed_urls, "Effective push URL is not one guarded Chicago destination"
    # Before native, SOURCE may not replace ANY tracked asset from its prepared base.
    assert not git("diff", "--name-only", I["protected_asset_base_head"], H, "--", "chicago/4d/assets")
    assert len(I["before_family_asset_sha256"]) == 50
    for path, digest in I["before_family_asset_sha256"].items():
        assert sha(git("show", H + ":" + path)) == digest
        assert sha((R / path).read_bytes()) == digest

    subprocess.run(["git", "-C", str(R), "merge-base", "--is-ancestor", I["remote_parent_head"], H], env=E, check=True)
    approved = {
        "chicago/4d/generators/archetypes/frame_tavern.py": "f8127662bd79b44825f5ba829945a884207c5ed343f1cc6c5ca80f919b6f0127",
        "chicago/4d/generators/archetypes/frame_tavern_params.py": "94a6311dfc4bff5a1c2557f2e09e7e796ad360880b13438771666f47073a3a1a",
        "chicago/4d/data/structures/sauganash_hotel.json": "044b670978290c1190ddf1ce6e8d593f09bb38f7ca3a310aef9ae4a963e85d33",
    }
    for path, digest in approved.items():
        assert sha(git("show", H + ":" + path)) == digest, path
    required = set(approved) | {"chicago/4d/docs/LIBERTIES.md", "chicago/4d/data/liberties.json", "chicago/4d/tools/compile_liberties.py", "chicago/4d/tools/compile_source_use.py", "chicago/4d/tools/validate.py", "chicago/4d/tools/audit_confidence.py"}
    assert required <= set(I["source_blob_oids"])
    changed = git("diff", "--name-only", I["protected_asset_base_head"], H).decode().splitlines()
    assert sorted(changed) == sorted(I["expected_changed_paths"])
    for path in changed:
        assert not path.startswith((".github/", "chicago/4d/tools/", "chicago/4d/schemas/"))
        assert not path.startswith("chicago/4d/generators/") or path in approved
        assert not path.startswith("chicago/4d/data/structures/") or path in approved
    for path, oid in I["source_blob_oids"].items():
        assert git("rev-parse", H + ":" + path).decode().strip() == oid, path
    assert sha(git("show", H + ":.github/workflows/" + WORKFLOW)) == I["workflow_sha256"]
    pin = git("show", H + ":chicago/4d/generators/blender.pin")
    assert sha(pin) == I["blender_pin_sha256"] and b"BLENDER_VERSION=4.5.3\n" in pin
    receipt_path = Path(I["full_fast_owner_receipt"])
    raw = receipt_path.read_bytes()
    assert sha(raw) == I["full_fast_owner_receipt_sha256"]
    fast = json.loads(raw)
    assert fast["status"] == "ACTUAL_FULL_DATA_FAST_OWNERS_PASS_EXPECTED_25_NATIVE_STALE"
    assert fast["source_blob_oids"] == I["source_blob_oids"]
    assert fast["expected_stale_family_outputs"] == 25
    actual = {"structures": len(list((A / "data/structures").glob("*.json"))), "sources": len(list((A / "data/sources").glob("*.json")))}
    assert actual == fast["actual_dataset_counts"] and actual["structures"] >= 1000 and actual["sources"] >= 500
    files = sorted(list((A / "data/structures").glob("*.json")) + list((A / "data/sources").glob("*.json")))
    dataset = {str(f.relative_to(A)): sha(f.read_bytes()) for f in files}
    assert sha(json.dumps(dataset, sort_keys=True).encode()) == fast["full_dataset_guard_sha256"]
    required = {"liberties-build", "liberties-check", "source-use-build", "source-use-check", "all-data-validate-params", "strict-confidence"}
    assert required <= {s["label"] for s in fast["steps"]}
    for step in fast["steps"]:
        assert step["exit"] == 0
        assert sha(Path(step["log"]).read_bytes()) == step["sha256"]
    reap = json.loads(Path(fast["proper_reaper"]).read_bytes())
    assert reap["command_exit"] == 0 and reap["all_children_reaped"] and not reap["leftover_cleanup"]
    return {"actual_dataset_counts": actual, "fast_receipt_sha256": sha(raw), "source_head": H, "source_tree": T}


def public_go():
    assert args.go and args.go_sha256
    raw = args.go.read_bytes()
    assert sha(raw) == args.go_sha256
    g = json.loads(raw)
    expected = {"action": "SOURCE_PUSH_CANCEL_OWN_AUTO_THEN_ONE_SCOPED25_DISPATCH", "source_head": H, "source_tree": T, "branch": BRANCH, "parent_pr": PR, "controller_sha256": sha(Path(__file__).read_bytes()), "intent_sha256": sha(intent_bytes), "prepared_sha256": sha(args.prepared.read_bytes()), "exact_dispatch_body": BODY}
    for key, value in expected.items():
        assert g[key] == value, key
    # URLs are external arguments: embedding an immutable GO commit URL in
    # that same GO would create an impossible content/commit self-reference.
    assert args.public_go_url and args.public_intent_url
    for url, content in [(args.public_go_url, raw), (args.public_intent_url, intent_bytes)]:
        assert re.fullmatch(r"https://raw\.githubusercontent\.com/kevinrhaas/chicago-evidence/[0-9a-f]{40}/evidence/sauganash-[^\s]+", url)
        r = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--max-time", "20", url], capture_output=True, timeout=25)
        assert r.returncode == 0 and r.stdout == content, "Immutable public authorization differs"
    return g


def original_claim_guard():
    endpoint = "repos/kevinrhaas/chicago-tickets/contents/T-2250-2499/T-2383-match-the-sauganash-hotel-to-its-pictures.md?ref=main"
    raw = subprocess.check_output(["gh", "api", "-H", "Cache-Control: no-cache", endpoint], timeout=20)
    row = json.loads(raw)
    text = base64.b64decode(row["content"]).decode()
    fields = {s.split(":", 1)[0]: s.split(":", 1)[1].strip() for s in text.split("---", 2)[1].splitlines() if ":" in s}
    assert fields["state"] == "claimed" and fields["claimed_by"] == I["expected_claimed_by"] and fields["claimed_run"] == "null"
    age = time.time() - datetime.datetime.fromisoformat(fields["claimed_at"].replace("Z", "+00:00")).timestamp()
    assert -120 <= age < 10800, "Original claim needs normal renewal before execution"
    return {"blob": row["sha"], "claimed_by": fields["claimed_by"], "claimed_at": fields["claimed_at"], "age_seconds": age}


def remote_guards(expected_head):
    claim = original_claim_guard()
    pr = api("pulls/" + str(PR))
    ref = api("git/ref/heads/" + BRANCH)
    assert pr["state"] == "open" and pr["draft"] and not pr["auto_merge"]
    assert pr["base"]["ref"] == "dev" and pr["head"]["ref"] == BRANCH
    assert pr["head"]["sha"] == ref["object"]["sha"] == expected_head
    workflow = api("contents/.github/workflows/" + WORKFLOW + "?ref=" + expected_head)
    assert sha(base64.b64decode(workflow["content"])) == I["workflow_sha256"]
    # The PR is isolated; a foreign dev move is recorded, not overwritten or frozen.
    return {"parent_pr": PR, "draft": True, "auto_merge": False, "branch_head": expected_head, "observed_dev": api("git/ref/heads/dev")["object"]["sha"], "original_claim": claim}


def own_runs(event):
    path = "actions/workflows/" + WORKFLOW + "/runs?branch=" + quote(BRANCH, safe="") + "&head_sha=" + H + "&event=" + event + "&per_page=100"
    rows = api(path)["workflow_runs"]
    return [r for r in rows if r["head_sha"] == H and r["head_branch"] == BRANCH and r["event"] == event]


if args.mode == "prepare":
    assert not args.prepared.exists(), "Prepared receipt already frozen; use a new reviewed path for a new preparation"
    local = local_guards()
    remote = remote_guards(I["remote_parent_head"])
    result = {"status": "PREPARED_NOT_EXECUTED", "controller_sha256": sha(Path(__file__).read_bytes()), "intent_sha256": sha(intent_bytes), "source_head": H, "source_tree": T, "local": local, "remote": remote, "exact_dispatch_body": BODY}
    args.prepared.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    raise SystemExit(0)

prepared = json.loads(args.prepared.read_bytes())
assert prepared["source_head"] == H and prepared["source_tree"] == T
assert prepared["controller_sha256"] == sha(Path(__file__).read_bytes()) and prepared["intent_sha256"] == sha(intent_bytes)
if args.mode == "execute":
    local_guards()
    go = public_go()
    before = remote_guards(I["remote_parent_head"])
    save("SOURCE-PUSH-FRESH-GUARDS.json", before)
    reserve("SOURCE-PUSH-RESERVED.json", {"source_head": H, "old_remote": I["remote_parent_head"], "ordinary_FF_only": True, "root_GO_sha256": args.go_sha256, "one_push_only": True})
    try:
        r = proper_command(["git", "-C", str(R), "push", "origin", H + ":refs/heads/" + BRANCH], "SOURCE-PUSH-COMMAND", 60)
        save("SOURCE-PUSH-RESPONSE.json", {"returncode": r.returncode, "stdout": r.stdout.decode(errors="replace"), "stderr": r.stderr.decode(errors="replace"), "one_push_only": True})
    except BaseException as exc:
        save("SOURCE-PUSH-RESPONSE.json", {"unknown": True, "error": repr(exc), "retry_forbidden": True})
    # Contain the exact own automatic run FIRST. PR head propagation can lag
    # behind a successful push and must not delay cancellation. An exact
    # push-event run at H/ref itself proves the push reached this feature.
    deadline = time.monotonic() + 90
    auto = []
    while time.monotonic() < deadline:
        auto = own_runs("push")
        save("OWN-AUTO-RUNS.json", auto)
        if auto:
            break
        time.sleep(5)
    assert len(auto) == 1, "No/ambiguous own automatic run: stop without dispatch"
    run = auto[0]
    assert run["status"] != "completed", "Unexpected completed automatic result needs review, not a blind dispatch"
    save("OWN-AUTO-SUPERSEDED.json", {"id": run["id"], "source_head": H, "branch": BRANCH, "event": "push", "reason": "SUPERSEDED_BY_ONE_SCOPED25_NATIVE_RUN"})
    post_once("actions/runs/" + str(run["id"]) + "/cancel", {}, 202, "OWN-AUTO-CANCEL-RESERVED.json", "OWN-AUTO-CANCEL-RESPONSE.json")
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        actual = api("actions/runs/" + str(run["id"]))
        assert actual["head_sha"] == H and actual["head_branch"] == BRANCH and actual["event"] == "push"
        save("OWN-AUTO-CANCEL-ACTUAL.json", actual)
        if actual["status"] == "completed":
            break
        time.sleep(5)
    assert actual["status"] == "completed" and actual["conclusion"] == "cancelled", "Actual cancellation unresolved: no manual POST"
    print(json.dumps({"status": "SOURCE_PUSHED_OWN_AUTO_TERMINAL_CANCELLED_MANUAL_NOT_DISPATCHED", "source_head": H, "cancelled_run": run["id"]}), flush=True)
    raise SystemExit(0)  # Separate properly reaped <=570s manual-dispatch leg follows.

else:
    assert (O / "SOURCE-PUSH-RESERVED.json").exists() and (O / "OWN-AUTO-CANCEL-RESERVED.json").exists()
    prior = json.loads((O / "OWN-AUTO-SUPERSEDED.json").read_bytes())
    actual = api("actions/runs/" + str(prior["id"]))
    assert actual["head_sha"] == H and actual["head_branch"] == BRANCH and actual["event"] == "push"
    assert actual["status"] == "completed" and actual["conclusion"] == "cancelled"
    save("OWN-AUTO-CANCEL-ACTUAL-RECOVERY.json", actual)

local_guards()
public_go()
remote = remote_guards(H)
all_rows = own_runs("push") + own_runs("workflow_dispatch")
assert not any(r["status"] != "completed" for r in all_rows), "An active same-head/ref native run exists"
assert not own_runs("workflow_dispatch"), "An earlier same-head manual dispatch exists; no retry"
save("MANUAL-DISPATCH-FRESH-GUARDS.json", {"remote": remote, "exact_body": BODY, "root_GO_sha256": args.go_sha256, "own_auto_terminal_cancelled": True})
ok = post_once("actions/workflows/" + WORKFLOW + "/dispatches", BODY, 204, "MANUAL-DISPATCH-ONEPOST-RESERVED.json", "MANUAL-DISPATCH-ONEPOST-RESPONSE.json")
if not ok:
    raise SystemExit("Manual POST uncertain/rejected: never retry; inspect actual GitHub state")
deadline = time.monotonic() + 90
while time.monotonic() < deadline:
    runs = own_runs("workflow_dispatch")
    if runs:
        assert len(runs) == 1, "Ambiguous actual dispatch run"
        save("ACTUAL-SCOPED-NATIVE-RUN.json", runs[0])
        print(json.dumps({"status": "ACTUAL_RUN_IDENTIFIED_NOT_NATIVE_PASS", "id": runs[0]["id"], "source_head": H, "only": BODY["inputs"]["only"]}), flush=True)
        raise SystemExit(0)
    time.sleep(5)
save("ACTUAL-RUN-PENDING.json", {"accepted_HTTP204": True, "actual_run": "NOT_YET_IDENTIFIED", "retry_forbidden": True})
raise SystemExit(3)
