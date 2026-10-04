#!/usr/bin/env python3
"""Summarize one judging round: per-arm scores with bootstrap CIs, paired differences, per-sample table.

  python3 analyze.py _ho PS14g             # reproduces evals/v1.4-validation/results/summary_ho.md after seed.py
  python3 analyze.py _it7 PS14g --details  # also print every issue the judge raised against the candidate

A sample's score for an arm is the mean over runs of the mean over judge passes. Confidence intervals are a
percentile bootstrap over samples (4,000 resamples, fixed seed), so they say nothing about judge or run noise
beyond what the per-sample means already average out.
"""
import collections
import glob
import json
import os
import random
import statistics as st
import sys

from common import path

DIMS = ["meaning", "facts", "voice", "naturalness", "clarity", "proportionality", "format", "overall"]
BASE_ORDER = ["U", "B", "O", "PS", "HS"]


def load(tag):
    J = collections.defaultdict(list)  # (sample, arm, run) -> one dict per judge pass
    for f in glob.glob(path("judgments", f"r*{tag}", "p*", "*.json")):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        key, P = d["key"], d["parsed"]
        if not P:
            continue
        rank = [key[L] for L in P["ranking"]]
        for L, a in key.items():
            c = P["candidates"][L]
            J[(d["sample"], a, d["rep"])].append({
                **{k: c[k] for k in DIMS}, "rank": rank.index(a) + 1,
                "issues": [i["type"] for i in c.get("issues", [])],
                "details": [i["type"] + ": " + i["detail"] for i in c.get("issues", [])]})
    return J


def score(J, s, a, k="overall"):
    reps = sorted({r for (ss, aa, r) in J if ss == s and aa == a})
    return st.mean(st.mean(x[k] for x in J[(s, a, r)]) for r in reps)


def boot(v, n=4000):
    r = random.Random(7)
    v = list(v)
    m = sorted(st.mean(r.choice(v) for _ in v) for _ in range(n))
    return st.mean(v), m[int(.025 * n)], m[int(.975 * n)]


def main(tag, cand, details=False):
    J = load(tag)
    if not J:
        sys.exit(f"no judgments found under {path('judgments')} for tag {tag!r}")
    samples = sorted({s for (s, a, r) in J})
    arms = sorted({a for (s, a, r) in J}, key=lambda a: BASE_ORDER.index(a) if a in BASE_ORDER else 9)
    print(f"# {tag}: {len(samples)} samples, arms {arms}\n")
    print("| arm | overall [95% CI] | facts | meaning | voice | natural | proportion | format | mean rank |\n|---|---|---|---|---|---|---|---|---|")
    for a in arms:
        m, lo, hi = boot([score(J, s, a) for s in samples])
        print(f"| {a} | {m:.2f} [{lo:.2f}, {hi:.2f}] | " + " | ".join(
            f"{st.mean(score(J, s, a, k) for s in samples):.2f}"
            for k in ["facts", "meaning", "voice", "naturalness", "proportionality", "format", "rank"]) + " |")
    print("\n| paired | diff [95% CI] | better/worse/tie |\n|---|---|---|")
    for b in [x for x in arms if x != cand]:
        d = [score(J, s, cand) - score(J, s, b) for s in samples]
        m, lo, hi = boot(d)
        print(f"| {cand} − {b} | {m:+.2f} [{lo:+.2f}, {hi:+.2f}] | {sum(x > 0 for x in d)}/{sum(x < 0 for x in d)}/{sum(x == 0 for x in d)} |")
    print("\n| sample | " + " | ".join(arms) + " |\n|" + "---|" * (len(arms) + 1))
    for s in samples:
        print(f"| {s} | " + " | ".join(f"{score(J, s, a):.2f}" for a in arms) + " |")
    print("\nissue counts (all passes):")
    for a in arms:
        c = collections.Counter(t for (s, aa, r), xs in J.items() if aa == a for x in xs for t in x["issues"])
        print(f"  {a}: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
    if details:
        for (s, a, r), xs in sorted(J.items()):
            if a == cand:
                for x in xs:
                    if x["details"]:
                        print(f"  [{s} {r}] ov={x['overall']} " + " || ".join(d[:150] for d in x["details"]))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], "--details" in sys.argv[3:])
