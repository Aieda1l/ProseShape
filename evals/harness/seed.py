#!/usr/bin/env python3
"""Unpack committed outputs and judgments into work/, so baselines need not be regenerated and the committed
tables can be reproduced without any model call.

  python3 seed.py                    # the 2026-09 experiment and the 1.4, 1.4.1 and 1.4.2 validations
  python3 seed.py path/to/outputs.jsonl path/to/judgments.jsonl

Existing files in work/ are left alone. The 2026-09 judgments land under their own round names (r1, r2, ...),
the v1.4 ones under r1_it1 ... r2_ho, so `analyze.py _ho PS14g` reads exactly the held-out round.
"""
import json
import os
import sys

from common import EXPERIMENT, REPO, path

DEFAULT = [os.path.join(EXPERIMENT, "results", "outputs.jsonl"), os.path.join(EXPERIMENT, "results", "judgments.jsonl"),
           os.path.join(REPO, "evals", "v1.4-validation", "results", "outputs.jsonl"),
           os.path.join(REPO, "evals", "v1.4-validation", "results", "judgments.jsonl"),
           os.path.join(REPO, "evals", "v1.4.1-validation", "results", "outputs.jsonl"),
           os.path.join(REPO, "evals", "v1.4.1-validation", "results", "judgments.jsonl"),
           os.path.join(REPO, "evals", "v1.4.2-validation", "results", "outputs.jsonl"),
           os.path.join(REPO, "evals", "v1.4.2-validation", "results", "judgments.jsonl")]


def write(p, d):
    if os.path.exists(p):
        return 0
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    return 1


def main(files):
    n = 0
    for fn in files:
        with open(fn, encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                if "round" in d:
                    if d["round"].startswith("pilot"):
                        continue
                    n += write(path("judgments", d["round"], f"p{d['pass']}", f"{d['sample']}.json"), d)
                else:
                    n += write(path("outputs", f"r{d['rep']}", d["arm"], f"{d['sample']}.json"), d)
    print(f"wrote {n} files under {path()}")


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT)
