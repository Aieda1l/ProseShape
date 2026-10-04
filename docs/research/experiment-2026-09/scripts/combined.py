#!/usr/bin/env python3
"""Combine judgments (r1p1, r1p2, r2p1) and checks (r1, r2); bootstrap CIs over samples."""
import json, os, random, statistics as st, collections
import analyze as A
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # experiment root
S = A.AI + A.HUMAN
Js = {("r1",1): A.load("r1",1), ("r1",2): A.load("r1",2), ("r2",1): A.load("r2",1)}
def per_sample(a, samples, key="overall"):
    # mean over available judgments per sample (r1 avg of 2 passes weighted as one run; r2 as another)
    out = {}
    for s in samples:
        r1 = [Js[("r1",p)][(s,a)][key] for p in (1,2) if (s,a) in Js[("r1",p)]]
        r2 = [Js[("r2",1)][(s,a)][key]] if (s,a) in Js[("r2",1)] else []
        runs = ([st.mean(r1)] if r1 else []) + r2
        if runs: out[s] = st.mean(runs)
    return out
def boot(vals, n=4000, seed=7):
    rnd = random.Random(seed); v = list(vals)
    ms = sorted(st.mean(rnd.choice(v) for _ in v) for _ in range(n))
    return st.mean(v), ms[int(.025*n)], ms[int(.975*n)]
md = ["### Combined blind-judge results (Sonnet 5.5 executor, Opus 5.5 judge; per sample: mean of run 1 [2 judge passes] and run 2 [1 pass])\n"]
for title, samples in [("All 13 samples", S), ("10 AI-shaped samples", A.AI), ("3 human / near-clean controls", A.HUMAN)]:
    md.append(f"\n#### {title}\n\n| Arm | overall (1-10) mean [95% CI] | facts | meaning | voice | naturalness | proportionality | mean rank |\n|---|---|---|---|---|---|---|---|")
    for a in A.ARMS:
        ov = per_sample(a, samples)
        m, lo, hi = boot(ov.values())
        dims = {k: st.mean(per_sample(a, samples, k).values()) for k in ["facts","meaning","voice","naturalness","proportionality"]}
        rk = st.mean(per_sample(a, samples, "rank").values())
        md.append(f"| {a} | {m:.2f} [{lo:.2f}, {hi:.2f}] | {dims['facts']:.2f} | {dims['meaning']:.2f} | {dims['voice']:.2f} | {dims['naturalness']:.2f} | {dims['proportionality']:.2f} | {rk:.2f} |")
md.append("\n#### Paired differences in 'overall' (ProseShape minus comparator), bootstrap over samples\n\n| Comparison | all 13: mean diff [95% CI] | AI-shaped 10 | controls 3 | PS better / worse / tie (samples, all 13) |\n|---|---|---|---|---|")
ps = {g: per_sample("PS", ss) for g, ss in [("all",S),("ai",A.AI),("hum",A.HUMAN)]}
for c in ["O","HS","HZ","B","AAW","SD","KZ","U"]:
    row = []
    for g, ss in [("all",S),("ai",A.AI),("hum",A.HUMAN)]:
        oc = per_sample(c, ss); d = [ps[g][s]-oc[s] for s in ss]
        m, lo, hi = boot(d); row.append(f"{m:+.2f} [{lo:+.2f}, {hi:+.2f}]")
    oc = per_sample(c, S); d = [ps["all"][s]-oc[s] for s in S]
    row.append(f"{sum(x>0 for x in d)} / {sum(x<0 for x in d)} / {sum(x==0 for x in d)}")
    md.append(f"| PS − {c} | " + " | ".join(row) + " |")
# run stability: r1 (avg passes) vs r2 per arm
md.append("\n#### Run-to-run stability (same arm, same sample, new generation; judge 'overall')\n\n| Arm | run 1 mean | run 2 mean | mean abs(run 1 − run 2) per sample |\n|---|---|---|---|")
for a in A.ARMS[1:]:
    r1 = {s: st.mean([Js[("r1",p)][(s,a)]["overall"] for p in (1,2)]) for s in S}
    r2 = {s: Js[("r2",1)][(s,a)]["overall"] for s in S}
    md.append(f"| {a} | {st.mean(r1.values()):.2f} | {st.mean(r2.values()):.2f} | {st.mean(abs(r1[s]-r2[s]) for s in S):.2f} |")
# issue counts over all 3 judgments
types = ["added_fact","dropped_fact","changed_fact","misattribution","quote_altered","format_damage","over_edit","under_edit","voice_loss","new_cliche"]
md.append("\n#### Judge-flagged issues, summed over the 3 judgments (39 sample-judgments per arm)\n\n| Arm | " + " | ".join(types) + " |\n|" + "---|"*(len(types)+1))
for a in A.ARMS:
    c = collections.Counter(t for J in Js.values() for s in S if (s,a) in J for t in J[(s,a)]["issues"])
    md.append(f"| {a} | " + " | ".join(str(c.get(t,0)) for t in types) + " |")
# deterministic
md.append("\n#### Deterministic checks (runs 1 and 2 pooled; 26 outputs per arm)\n\n| Arm | token change, AI samples | token change, controls | length ratio, AI | numbers added | numbers dropped | protected strings not found verbatim* | AAW validator errors | unchanged controls (of 6) | em dashes out (src total 11/run) | lint density out (per 1k; src 21.4) |\n|---|---|---|---|---|---|---|---|---|---|---|")
rows = json.load(open(os.path.join(E,"results","checks_r1.json"))) + json.load(open(os.path.join(E,"results","checks_r2.json")))
by = collections.defaultdict(list)
for r in rows: by[r["arm"]].append(r)
for a in A.ARMS:
    rs = by[a] if a != "U" else [r for r in by[a] if r["rep"]=="r1"]
    ai = [r for r in rs if r["sample"] in A.AI]; hu = [r for r in rs if r["sample"] in A.HUMAN]
    nrun = 1 if a=="U" else 2
    md.append(f"| {a} | {st.mean(r['change_ratio'] for r in ai):.2f} | {st.mean(r['change_ratio'] for r in hu):.2f} | {st.mean(r['len_ratio'] for r in ai):.2f} | {sum(len(r['numbers_added']) for r in rs)} | {sum(len(r['numbers_missing']) for r in rs)} | {sum(len(r['protected_missing']) for r in rs)} | {sum(len(r['aaw_validator']['errors']) for r in rs)} | {sum(r['unchanged'] for r in hu)}{'' if nrun==2 else ' (of 3)'} | {sum(r['emdash_out'] for r in rs)/nrun:.1f} | {st.mean(r['lint_density_out'] for r in rs):.1f} |")
md.append("\n*String presence is literal; manual review of every flagged case is in the experiment README (e.g. '14-day' → 'free for 14 days' is a checker false positive).")
open(os.path.join(E,"results","summary_combined.md"),"w").write("\n".join(md)); print("\n".join(md))
