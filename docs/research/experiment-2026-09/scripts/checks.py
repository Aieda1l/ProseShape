#!/usr/bin/env python3
"""Deterministic checks on each arm's final text vs the source. Neutral measurements, not quality scores."""
import json, os, re, glob, difflib, subprocess, sys, tempfile, statistics
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # experiment root
C = os.environ.get("COMP_DIR", os.path.join(E, "..", "comp"))
MAN = json.load(open(os.path.join(E, "corpus", "manifest.json")))["samples"]
sys.path.insert(0, os.path.join(C, "shir-danishyar_humanize", "scripts"))
import ai_pattern_lint as lint

def norm(s):
    return (s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
             .replace(" ", " "))
def words(s): return re.findall(r"\w+(?:['’]\w+)*|[^\w\s]", s)
NUM = re.compile(r"(?<![\w.])\$?\d[\d,.]*%?")
def nums(s): return [n.rstrip('.,') for n in NUM.findall(s)]

def check(sample, final):
    src = open(os.path.join(E, "corpus", f"{sample}.md"), encoding="utf-8").read().rstrip("\n")
    ns, nf = norm(src), norm(final)
    ws, wf = words(ns), words(nf)
    sm = difflib.SequenceMatcher(a=ws, b=wf, autojunk=False)
    prot = MAN[sample]["protected"]
    missing = [p for p in prot if norm(p) not in nf]
    sn, fn = set(nums(ns)), set(nums(nf))
    lw_s = len(re.findall(r"\w+", ns)); lw_f = len(re.findall(r"\w+", nf))
    with tempfile.TemporaryDirectory() as td:
        a, b = os.path.join(td, "a.md"), os.path.join(td, "b.md")
        open(a, "w").write(src + "\n"); open(b, "w").write(final + "\n")
        try:
            v = json.loads(subprocess.run(["node", os.path.join(E, "scripts", "validate_wrap.js"),
                os.path.join(C, "conorbronsdon_avoid-ai-writing", "detector", "validate.js"), a, b],
                capture_output=True, text=True, timeout=60).stdout)
        except Exception as ex:
            v = {"ok": None, "errors": [f"validator-failed:{ex}"], "warnings": []}
    hs, wcs = lint.lint_text(src); hf, wcf = lint.lint_text(final)
    return {
        "unchanged": final.strip() == src.strip(),
        "change_ratio": round(1 - sm.ratio(), 3),
        "len_ratio": round(lw_f / max(lw_s, 1), 2),
        "protected_total": len(prot), "protected_missing": missing,
        "numbers_added": sorted(fn - sn), "numbers_missing": sorted(sn - fn),
        "emdash_src": src.count("—"), "emdash_out": final.count("—"),
        "lint_density_src": round(len(hs) / max(wcs, 1) * 1000, 1), "lint_density_out": round(len(hf) / max(wcf, 1) * 1000, 1),
        "aaw_validator": v,
    }

if __name__ == "__main__":
    rep = sys.argv[1] if len(sys.argv) > 1 else "r1"
    rows = []
    for f in sorted(glob.glob(os.path.join(E, "outputs", rep, "*", "*.json"))):
        d = json.load(open(f))
        if not d.get("extracted"): continue
        r = {"arm": d["arm"], "sample": d["sample"], "rep": rep, **check(d["sample"], d["final"])}
        rows.append(r)
    for s in MAN:  # the untouched arm, for reference
        src = open(os.path.join(E, "corpus", f"{s}.md"), encoding="utf-8").read().rstrip("\n")
        rows.append({"arm": "U", "sample": s, "rep": rep, **check(s, src)})
    json.dump(rows, open(os.path.join(E, "results", f"checks_{rep}.json"), "w"), indent=1, ensure_ascii=False)
    print(len(rows), "rows")
