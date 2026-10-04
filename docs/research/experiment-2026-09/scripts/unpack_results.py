#!/usr/bin/env python3
"""Expand results/outputs.jsonl and results/judgments.jsonl into the outputs/ and judgments/ trees that
analyze.py, combined.py and ablation.py read. Run from anywhere: python3 scripts/unpack_results.py"""
import json, os
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for line in open(os.path.join(E, "results", "outputs.jsonl"), encoding="utf-8"):
    d = json.loads(line); p = os.path.join(E, "outputs", f"r{d['rep']}", d["arm"], f"{d['sample']}.json")
    os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for line in open(os.path.join(E, "results", "judgments.jsonl"), encoding="utf-8"):
    d = json.loads(line)
    if d["round"].startswith("pilot"): continue
    p = os.path.join(E, "judgments", d["round"], f"p{d['pass']}", f"{d['sample']}.json")
    os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("unpacked")
