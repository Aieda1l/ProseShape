#!/usr/bin/env python3
"""One blind judging pass over every arm's output for one sample.

  python3 judge.py h01_release_notes r1 1 --arms "U O PS HS PS14g" --tag _ho --corpus heldout

The untouched source (arm U) is always a candidate. Candidates are shuffled with a seed built from the sample,
run, tag and pass, so a re-run reproduces the same order. Writes work/judgments/<RUN><TAG>/p<PASS>/<SAMPLE>.json.
The judge rubric is docs/research/experiment-2026-09/prompts/judge_system.txt (rubric v2).
"""
import argparse
import json
import os
import random
import re
import subprocess
import sys

from common import CLAUDE_FLAGS, JUDGE, PROMPTS, REQUEST, path, read_sample, sandbox, stop, stopped

LETTERS = "ABCDEFGHIJ"


def judge(sample, rep, jpass, arms, tag, corpus, model=JUDGE):
    out = path("judgments", rep + tag, f"p{jpass}", f"{sample}.json")
    if os.path.exists(out):
        return out
    if stopped():
        sys.exit(3)
    src = read_sample(corpus, sample)
    cands = {}
    for a in arms:
        if a == "U":
            cands[a] = src
            continue
        with open(path("outputs", rep, a, f"{sample}.json"), encoding="utf-8") as f:
            d = json.load(f)
        if d.get("extracted"):
            cands[a] = d["final"]
    order = list(cands)
    random.Random(f"{sample}-{rep}{tag}-{jpass}").shuffle(order)
    key = {LETTERS[i]: a for i, a in enumerate(order)}
    body = [f"REQUEST: {REQUEST}\n", "ORIGINAL:\n<<<\n" + src + "\n>>>\n"]
    body += [f"CANDIDATE {L}:\n<<<\n{cands[a]}\n>>>\n" for L, a in key.items()]
    user = "\n".join(body)
    cmd = ["claude", "-p", user, "--model", model, "--system-prompt-file", os.path.join(PROMPTS, "judge_system.txt"), *CLAUDE_FLAGS]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=sandbox(), timeout=1200)
    try:
        d = json.loads(p.stdout)
    except ValueError:
        d = {"is_error": True, "result": p.stderr[-500:]}
    res = d.get("result", "") or ""
    if d.get("is_error") or "spend limit" in res:
        stop(res)
        sys.exit(3)
    m = re.search(r"\{.*\}", res, re.S)
    try:
        parsed = json.loads(m.group(0)) if m else None
    except ValueError:
        parsed = None
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"round": rep + tag, "sample": sample, "rep": rep, "pass": jpass, "model": model, "key": key,
                   "parsed": parsed, "raw": res, "cost_usd": d.get("total_cost_usd"), "user_prompt": user},
                  f, indent=1, ensure_ascii=False)
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Blind-judge one sample.")
    p.add_argument("sample")
    p.add_argument("rep", nargs="?", default="r1", help="output run to judge: r1, r2, ...")
    p.add_argument("jpass", type=int, nargs="?", default=1, help="judge pass number (changes the shuffle)")
    p.add_argument("--arms", default=os.environ.get("JUDGE_ARMS", "U O PS HS"), help="space-separated arm names")
    p.add_argument("--tag", default=os.environ.get("JUDGE_TAG", ""), help="suffix naming this judging round, e.g. _ho")
    p.add_argument("--corpus", default="heldout")
    p.add_argument("--model", default=JUDGE)
    a = p.parse_args()
    print(judge(a.sample, a.rep, a.jpass, a.arms.split(), a.tag, a.corpus, a.model))
