#!/usr/bin/env python3
"""Run scripts/preserve_check.py over every output for a corpus and summarize by arm.

  python3 checks.py --corpus heldout --arms O PS14g [--json out.json] [--show]

Fiction and literary samples (category mentions fiction, essay, or literary in the corpus manifest) are checked
with --fiction, so changed dialogue is reported as info rather than as an error.
"""
import argparse
import collections
import glob
import json
import os
import sys

from common import REPO, corpus_dir, path, read_sample

sys.path.insert(0, os.path.join(REPO, "scripts"))
import preserve_check  # noqa: E402


def fiction_samples(corpus):
    try:
        with open(os.path.join(corpus_dir(corpus), "manifest.json"), encoding="utf-8") as f:
            man = json.load(f)["samples"]
    except (OSError, KeyError, ValueError):
        return set()
    return {s for s, m in man.items() if any(w in m.get("category", "").lower() for w in ("fiction", "essay", "literary"))}


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--corpus", default="heldout")
    p.add_argument("--arms", nargs="+", required=True)
    p.add_argument("--json")
    p.add_argument("--show", action="store_true", help="print each output's errors and warnings")
    a = p.parse_args()
    names = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(corpus_dir(a.corpus), "*.md"))}
    fiction = fiction_samples(a.corpus)
    rows, totals = [], collections.defaultdict(collections.Counter)
    for arm in a.arms:
        for f in sorted(glob.glob(path("outputs", "r*", arm, "*.json"))):
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
            if d["sample"] not in names:
                continue
            t = totals[arm]
            t["outputs"] += 1
            if not d.get("extracted"):
                t["not_extracted"] += 1
                continue
            r = preserve_check.check(read_sample(a.corpus, d["sample"]), d["final"], fiction=d["sample"] in fiction)
            t["errors"] += len(r["errors"])
            t["warnings"] += len(r["warnings"])
            t["with_errors"] += bool(r["errors"])
            t["change_ratio_x1000"] += int(1000 * r["metrics"]["change_ratio"])
            rows.append({"arm": arm, "sample": d["sample"], "rep": d["rep"], **r})
            if a.show and (r["errors"] or r["warnings"]):
                print(f"{arm} {d['sample']} r{d['rep']}: " + "; ".join(r["errors"] + r["warnings"]))
    print("| arm | outputs | not extracted | outputs with errors | errors | warnings | mean change |\n|---|---|---|---|---|---|---|")
    for arm in a.arms:
        t = totals[arm]
        checked = t["outputs"] - t["not_extracted"]
        mean = f"{t['change_ratio_x1000'] / 1000 / checked:.0%}" if checked else "-"
        print(f"| {arm} | {t['outputs']} | {t['not_extracted']} | {t['with_errors']} | {t['errors']} | {t['warnings']} | {mean} |")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
