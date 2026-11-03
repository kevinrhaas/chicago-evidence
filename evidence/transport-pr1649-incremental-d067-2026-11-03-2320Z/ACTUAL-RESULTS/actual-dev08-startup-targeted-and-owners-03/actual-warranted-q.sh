set -uo pipefail
# An explicit ask is always honoured: a dispatch names what it wants and
# the nightly schedule is the whole point of the workflow. Only `push`
# is filtered, because only `push` fans out.
if [ "$EV" != "push" ]; then
  echo "bake=1" >> "$GITHUB_OUTPUT"
  echo "::notice::baking — event is $EV, not a push"; exit 0
fi
# `dev` itself always bakes. It is the authoritative copy, and it is the
# run whose output every branch would otherwise duplicate.
if [ "$REF" = "$BASE" ]; then
  echo "bake=1" >> "$GITHUB_OUTPUT"
  echo "::notice::baking — this is $BASE"; exit 0
fi
git fetch origin "$BASE" -q || true
CHANGED=$(git diff --name-only "origin/$BASE...HEAD" -- \
            'chicago/4d/generators/**' \
            'chicago/4d/tools/bake.sh' \
            '.github/workflows/chicago-4d-bake.yml' 2>/dev/null)
RC=$?
# FAIL OPEN, the same way --check-base does. If the diff cannot be taken
# — a shallow clone, a base that never fetched — the safe answer is to
# bake: a redundant bake costs twenty minutes, a skipped one that was
# needed ships stale meshes and the staleness gate then blames the PR.
if [ "$RC" -ne 0 ]; then
  echo "bake=1" >> "$GITHUB_OUTPUT"
  echo "::warning::baking — could not diff against $BASE (exit $RC), so not skipping"; exit 0
fi
if [ -z "$CHANGED" ]; then
  echo "bake=0" >> "$GITHUB_OUTPUT"
  echo "::notice::SKIPPING — nothing this branch owns under generators/, tools/bake.sh"
  echo "::notice::or this workflow differs from $BASE. Any generators change here came"
  echo "::notice::in with the PR lap's merge, and $BASE's own bake covers it."
  exit 0
fi
echo "::notice::this branch's own diff against $BASE touches:"
printf '%s\n' "$CHANGED" | sed 's/^/  /'
# SECOND SCREEN, T-1668: the path filter above says this branch could
# have staled a mesh. Whether it DID is a question the freshness
# register answers in about half a second, and it is the same register
# `check.sh` refuses the tree with — so ask it rather than spending
# twenty-five minutes of Cycles to find out. The rule, its fail-open
# cases and its self-test live in tools/bake_warranted.py; a green pull
# request that could not merge inside its own run is why.
# Glessner's GLBs are ignored outputs restored from the committed
# recovery package. A fresh checkout must materialize that package
# before asking whether an output is missing or stale, just as publish
# does. The recovery verifier refuses mismatched existing bytes; an
# unreadable package keeps the existing fail-open bake decision.
# Keep every native freshness input/output physically present. Discover
# app directories from this HEAD, including future additions; only the
# unrelated docs archives stay sparse. The exact committed Glessner
# recovery package is an input and must be present before materialize.
if ! python3 - <<'PY'
import os, subprocess
names = subprocess.check_output([
    'git', 'ls-tree', '-z', '-d', '--name-only', 'HEAD:chicago/4d'
]).split(b'\0')
directories = {name for name in names if name}
if not {b'assets', b'data', b'generators', b'tools', b'renderers'} <= directories:
    raise SystemExit('Native freshness directories cannot be established')
paths = ['.github', 'chicago/4d/docs/RESEARCH/glessner-v4-recovery']
paths += ['chicago/4d/' + os.fsdecode(name)
          for name in sorted(directories) if name != b'docs']
subprocess.run(['git', 'sparse-checkout', 'set', '--cone', *paths], check=True)
PY
then
  echo "bake=1" >> "$GITHUB_OUTPUT"
  echo "::warning::baking — native freshness files could not be materialized, so not skipping"
  exit 0
fi
if ! python3 chicago/4d/tools/recover_glessner_v4.py --materialize; then
  echo "bake=1" >> "$GITHUB_OUTPUT"
  echo "::warning::baking — committed asset package could not be materialized, so freshness cannot be established"
  exit 0
fi
WHY=$(mktemp)
BAKE=$(printf '%s\n' "$CHANGED" \
         | python3 chicago/4d/tools/bake_warranted.py \
             --decide --base "origin/$BASE" 2>"$WHY") || BAKE=1
# A verdict that is neither answer is not a verdict. Anything else the
# script could have printed — nothing at all, a traceback's tail — is
# unanswerable, and unanswerable bakes.
case "$BAKE" in
  0|1) ;;
  *) BAKE=1; echo "bake_warranted.py answered '$BAKE', which is not 0 or 1" >"$WHY" ;;
esac
echo "bake=$BAKE" >> "$GITHUB_OUTPUT"
if [ "$BAKE" = "1" ]; then
  echo "::notice::$(tr '\n' ' ' <"$WHY")"
else
  echo "::notice::SKIPPING — $(tr '\n' ' ' <"$WHY")"
fi
