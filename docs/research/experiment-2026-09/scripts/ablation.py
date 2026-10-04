import json, glob, os, random, statistics as st, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A, checks
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # experiment root
ARMS = ["U","O","Oo","PS","PSo","PSc","HS"]
S = A.AI + A.HUMAN
def load(p):
    out = {}
    for f in glob.glob(os.path.join(E,"judgments","r1_ablation",f"p{p}","*.json")):
        d = json.load(open(f)); key=d["key"]; P=d["parsed"]; rank=[key[L] for L in P["ranking"]]
        for L,a in key.items():
            c=P["candidates"][L]; out[(d["sample"],a)]={**{k:c[k] for k in A.DIMS},"rank":rank.index(a)+1,"issues":[i["type"] for i in c.get("issues",[])]}
    return out
J1, J2 = load(1), load(2)
def ps(a, ss, k="overall"): return {s: (J1[(s,a)][k]+J2[(s,a)][k])/2 for s in ss}
def boot(v, n=4000):
    r=random.Random(7); v=list(v); m=sorted(st.mean(r.choice(v) for _ in v) for _ in range(n)); return st.mean(v), m[int(.025*n)], m[int(.975*n)]
md=["### Ablation: executor model and reference files (run 1 outputs; two blind judge passes, Opus 5.5)\n","Arms: U untouched; O ordinary editor (Sonnet 5.5); Oo ordinary editor (Opus 5.5); PS ProseShape full bundle (Sonnet 5.5); PSo ProseShape full bundle (Opus 5.5); PSc ProseShape SKILL.md only, no references (Sonnet 5.5); HS HumanScope (Sonnet 5.5).\n"]
for title, ss in [("All 13", S), ("AI-shaped 10", A.AI), ("Controls 3", A.HUMAN)]:
    md.append(f"\n#### {title}\n\n| Arm | overall mean [95% CI] | facts | meaning | voice | proportionality | mean rank | dropped/added facts flagged (2 passes) |\n|---|---|---|---|---|---|---|---|")
    for a in ARMS:
        m,lo,hi = boot(ps(a,ss).values())
        c = collections.Counter(t for J in (J1,J2) for s in ss for t in J[(s,a)]["issues"])
        md.append(f"| {a} | {m:.2f} [{lo:.2f}, {hi:.2f}] | {st.mean(ps(a,ss,'facts').values()):.2f} | {st.mean(ps(a,ss,'meaning').values()):.2f} | {st.mean(ps(a,ss,'voice').values()):.2f} | {st.mean(ps(a,ss,'proportionality').values()):.2f} | {st.mean(ps(a,ss,'rank').values()):.2f} | {c['dropped_fact']}/{c['added_fact']} |")
md.append("\n#### Paired differences (overall), all 13 samples\n\n| Comparison | mean diff [95% CI] | better/worse/tie |\n|---|---|---|")
for x,y in [("PSo","Oo"),("PSo","PS"),("PS","PSc"),("PS","O"),("PSc","O"),("Oo","O"),("PSo","HS")]:
    a,b=ps(x,S),ps(y,S); d=[a[s]-b[s] for s in S]; m,lo,hi=boot(d)
    md.append(f"| {x} − {y} | {m:+.2f} [{lo:+.2f}, {hi:+.2f}] | {sum(v>0 for v in d)}/{sum(v<0 for v in d)}/{sum(v==0 for v in d)} |")
md.append("\n#### Per-sample overall (mean of 2 passes)\n\n| Sample | " + " | ".join(ARMS) + " |\n|" + "---|"*(len(ARMS)+1))
for s in S: md.append(f"| {s} | " + " | ".join(f"{(J1[(s,a)]['overall']+J2[(s,a)]['overall'])/2:.1f}" for a in ARMS) + " |")
# deterministic for new arms
md.append("\n#### Deterministic checks for ablation arms (run 1)\n\n| Arm | token change AI | token change controls | length ratio AI | numbers added/dropped | cost (13 samples, USD) |\n|---|---|---|---|---|---|")
for a in ["O","Oo","PS","PSo","PSc"]:
    rs=[]; cost=0
    for s in S:
        d=json.load(open(os.path.join(E,"outputs","r1",a,f"{s}.json"))); cost+=d["cost_usd"] or 0
        rs.append((s,checks.check(s,d["final"])))
    ai=[c for s,c in rs if s in A.AI]; hu=[c for s,c in rs if s in A.HUMAN]
    md.append(f"| {a} | {st.mean(c['change_ratio'] for c in ai):.2f} | {st.mean(c['change_ratio'] for c in hu):.2f} | {st.mean(c['len_ratio'] for c in ai):.2f} | {sum(len(c['numbers_added']) for _,c in rs)}/{sum(len(c['numbers_missing']) for _,c in rs)} | {cost:.2f} |")
open(os.path.join(E,"results","summary_ablation.md"),"w").write("\n".join(md)); print("\n".join(md))
