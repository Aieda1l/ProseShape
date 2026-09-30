#!/usr/bin/env python3
"""Aggregate blind-judge scores and deterministic checks into summary tables (Markdown)."""
import json, glob, os, statistics as st, collections, itertools, sys
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # experiment root
ARMS = ["U", "B", "O", "PS", "HZ", "HS", "AAW", "SD", "KZ"]
DIMS = ["meaning", "facts", "voice", "naturalness", "clarity", "proportionality", "format", "overall"]
AI = ["s01_ai_blog","s02_marketing","s03_email_pro","s04_tech_docs","s05_explainer","s06_academic","s07_social","s08_fiction","s09_news_quotes","s13_spanish"]
HUMAN = ["s10_human_tech","s11_human_voice","s12_email_nearclean"]

def load(rep, jpass):
    out = {}
    for f in glob.glob(os.path.join(E, "judgments", rep, f"p{jpass}", "*.json")):
        d = json.load(open(f))
        if not d.get("parsed"): continue
        key = d["key"]; p = d["parsed"]
        rank = [key[L] for L in p["ranking"]]
        for L, a in key.items():
            c = p["candidates"][L]
            out[(d["sample"], a)] = {**{k: c[k] for k in DIMS}, "rank": rank.index(a) + 1, "n": len(rank),
                                     "issues": [i["type"] for i in c.get("issues", [])]}
    return out

def spearman(x, y):
    n = len(x)
    rx = {v: i for i, v in enumerate(x)}; ry = {v: i for i, v in enumerate(y)}
    d2 = sum((rx[v] - ry[v]) ** 2 for v in x)
    return 1 - 6 * d2 / (n * (n * n - 1))

def table(J, samples, title):
    lines = [f"\n#### {title} (n={len(samples)} samples)\n", "| Arm | " + " | ".join(DIMS) + " | mean rank | #1 ranks | beats O | beats U |", "|" + "---|" * (len(DIMS) + 5)]
    for a in ARMS:
        rows = [J[(s, a)] for s in samples if (s, a) in J]
        if not rows: continue
        means = [st.mean(r[k] for r in rows) for k in DIMS]
        mr = st.mean(r["rank"] for r in rows)
        firsts = sum(r["rank"] == 1 for r in rows)
        bo = sum(J[(s, a)]["rank"] < J[(s, "O")]["rank"] for s in samples if (s, a) in J and (s, "O") in J and a != "O")
        bu = sum(J[(s, a)]["rank"] < J[(s, "U")]["rank"] for s in samples if (s, a) in J and (s, "U") in J and a != "U")
        lines.append(f"| {a} | " + " | ".join(f"{m:.2f}" for m in means) + f" | {mr:.2f} | {firsts} | {bo if a!='O' else '—'} | {bu if a!='U' else '—'} |")
    return "\n".join(lines)

def issues_table(J, samples):
    types = ["added_fact","dropped_fact","changed_fact","misattribution","quote_altered","format_damage","over_edit","under_edit","voice_loss","new_cliche","other"]
    lines = ["\n| Arm | " + " | ".join(types) + " |", "|" + "---|" * (len(types) + 1)]
    for a in ARMS:
        c = collections.Counter(t for s in samples if (s, a) in J for t in J[(s, a)]["issues"])
        lines.append(f"| {a} | " + " | ".join(str(c.get(t, 0)) for t in types) + " |")
    return "\n".join(lines)

if __name__ == "__main__":
    specs = [("r1", 1), ("r1", 2), ("r2", 1)]
    Js = {sp: load(*sp) for sp in specs}
    md = []
    for sp, J in Js.items():
        if not J: continue
        allS = AI + HUMAN
        md.append(f"\n### Judge {sp[0]} pass {sp[1]}")
        md.append(table(J, allS, "All samples"))
        md.append(table(J, AI, "AI-shaped samples"))
        md.append(table(J, HUMAN, "Human / near-clean controls"))
        md.append("\nJudge-reported issue counts (all samples):" + issues_table(J, allS))
    # inter-pass agreement on r1
    J1, J2 = Js.get(("r1", 1)), Js.get(("r1", 2))
    if J1 and J2:
        rhos, ov_diffs = [], []
        for s in AI + HUMAN:
            r1 = sorted([a for a in ARMS if (s, a) in J1], key=lambda a: J1[(s, a)]["rank"])
            r2 = sorted([a for a in ARMS if (s, a) in J2], key=lambda a: J2[(s, a)]["rank"])
            if set(r1) == set(r2) and r1: rhos.append(spearman(r1, r2))
            ov_diffs += [abs(J1[(s, a)]["overall"] - J2[(s, a)]["overall"]) for a in ARMS if (s, a) in J1 and (s, a) in J2]
        md.append(f"\n### Judge reliability (r1, pass 1 vs pass 2, different shuffles)\n\nMean Spearman rank correlation across samples: {st.mean(rhos):.2f} (min {min(rhos):.2f}, max {max(rhos):.2f}); mean absolute difference in 'overall' (1-10) for the same output: {st.mean(ov_diffs):.2f}; share of identical 'overall' scores: {sum(d==0 for d in ov_diffs)/len(ov_diffs):.0%}.")
        # combined per-arm overall across both passes, per sample for detail
        md.append("\n### Per-sample 'overall' (r1, mean of two judge passes)\n\n| Sample | " + " | ".join(ARMS) + " |\n|" + "---|" * (len(ARMS) + 1))
        for s in AI + HUMAN:
            md.append(f"| {s} | " + " | ".join(f"{(J1[(s,a)]['overall']+J2[(s,a)]['overall'])/2:.1f}" if (s,a) in J1 and (s,a) in J2 else "–" for a in ARMS) + " |")
    open(os.path.join(E, "results", "summary_judge.md"), "w").write("\n".join(md))
    print("\n".join(md))
