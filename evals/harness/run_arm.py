#!/usr/bin/env python3
"""Run one (arm, sample, run) through an isolated, tool-less `claude -p` session.

  python3 run_arm.py PS14g h01_release_notes 1 --corpus heldout

Reads work/arms/<ARM>.txt as the system prompt and writes work/outputs/r<RUN>/<ARM>/<SAMPLE>.json.
Existing outputs are skipped, so an interrupted batch can be re-run. On an error that looks like a spend or
usage limit, writes work/STOP and exits 3; every script refuses to start while STOP exists.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

from common import CLAUDE_FLAGS, EXECUTOR, FORMAT_NOTE, REQUEST, path, read_sample, sandbox, stop, stopped

FINAL = re.compile(r"^<<<FINAL>>>\s*\n(.*?)\n<<<END>>>\s*$", re.S | re.M)


def run(arm, sample, rep, corpus, model=EXECUTOR):
    out_path = path("outputs", f"r{rep}", arm, f"{sample}.json")
    if os.path.exists(out_path):
        return out_path
    if stopped():
        sys.exit(3)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    user = f"{REQUEST}\n\n<text>\n{read_sample(corpus, sample)}\n</text>\n\n{FORMAT_NOTE}"
    cmd = ["claude", "-p", user, "--model", model, "--system-prompt-file", path("arms", f"{arm}.txt"), *CLAUDE_FLAGS]
    for attempt in range(3):
        t0 = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=sandbox(), timeout=900)
        try:
            d = json.loads(p.stdout)
        except ValueError:
            d = {"is_error": True, "raw_stdout": p.stdout[-2000:], "stderr": p.stderr[-2000:]}
        if not d.get("is_error"):
            break
        time.sleep(10 * (attempt + 1))
    res = d.get("result", "") or ""
    if d.get("is_error") or "spend limit" in res or "usage limit" in res.lower():
        stop(res or json.dumps(d))
        sys.exit(3)
    m = FINAL.search(res)
    rec = {"arm": arm, "sample": sample, "rep": rep, "model": model, "wall_s": round(time.time() - t0, 1),
           "final": m.group(1).strip("\n") if m else None, "extracted": bool(m), "reply": res,
           "cost_usd": d.get("total_cost_usd"), "usage": d.get("usage"), "user_prompt": user}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
    return out_path


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate one output.")
    p.add_argument("arm")
    p.add_argument("sample")
    p.add_argument("rep", type=int, nargs="?", default=1)
    p.add_argument("--corpus", default="heldout", help="'heldout', 'dev', or a directory of <sample>.md files")
    p.add_argument("--model", default=EXECUTOR)
    a = p.parse_args()
    print(run(a.arm, a.sample, a.rep, a.corpus, a.model))
