#!/bin/bash
# One iteration: build an arm from the working tree, generate two runs, judge two passes per run, summarize.
#
#   ./iterate.sh PSnext _next dev                # iterate on the 2026-09 dev corpus
#   ./iterate.sh PSnext _next_ho heldout         # validate once, at the end, on the frozen held-out corpus
#
# Baseline outputs (O, PS v1.3.1, HS) are read from work/outputs: run seed.py first, or generate them with
# run_arm.py. Set ARMS to change the judged set (default "U O PS HS <ARM>"). Parallelism: JOBS (default 5).
set -euo pipefail
ARM=$1; TAG=$2; CORPUS=${3:-dev}
JOBS=${JOBS:-5}
cd "$(dirname "$0")"
WORK=$(python3 -c 'import common; print(common.WORK)')
SAMPLES=$(python3 -c "import glob,os,common; print(' '.join(sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(common.corpus_dir('$CORPUS'), '*.md')))))")
python3 build_arm.py "$ARM"
rm -f "$WORK/STOP"
for r in 1 2; do for s in $SAMPLES; do echo "$ARM $s $r"; done; done |
  xargs -P "$JOBS" -L 1 sh -c 'python3 run_arm.py "$0" "$1" "$2" --corpus '"$CORPUS"' >/dev/null || true'
[ -f "$WORK/STOP" ] && { cat "$WORK/STOP"; exit 3; }
JUDGE_ARMS=${ARMS:-"U O PS HS $ARM"}
for r in r1 r2; do for p in 1 2; do for s in $SAMPLES; do echo "$s $r $p"; done; done; done |
  xargs -P "$JOBS" -L 1 sh -c 'python3 judge.py "$0" "$1" "$2" --arms "'"$JUDGE_ARMS"'" --tag '"$TAG"' --corpus '"$CORPUS"' >/dev/null || true'
[ -f "$WORK/STOP" ] && { cat "$WORK/STOP"; exit 3; }
python3 analyze.py "$TAG" "$ARM" --details
python3 checks.py --corpus "$CORPUS" --arms ${JUDGE_ARMS/U /}
