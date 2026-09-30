#!/usr/bin/env python3
"""Run competitors' deterministic scanners on the unedited corpus (incl. genuinely human controls s10/s11/s12).
Requires COMP_DIR with clones at the pinned commits (see build_arms.py) plus NulightJens/humanizer-stack@13f5c02
and ccf/humanize@db51ff3. Writes results/scanner_controls.md."""
import json, os, re, subprocess, sys
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.environ.get("COMP_DIR", os.path.join(E, "..", "comp"))
def run(cmd): return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
rows = ["| Sample | shir-danishyar lint (hits/1k, threshold 5) | humanizer-stack copy_scan hits | humanizer-stack structural_scan hits | keez97 score.py full: result (HARD fails) | keez97 score.py light | ccf surface_scan sentence-length CV (README: 'human 0.5-0.9') |", "|---|---|---|---|---|---|---|"]
for f in sorted(os.listdir(os.path.join(E, "corpus"))):
    if not f.endswith(".md"): continue
    p = os.path.join(E, "corpus", f)
    sd = json.loads(run(["python3", f"{C}/shir-danishyar_humanize/scripts/ai_pattern_lint.py", "--json", p]))
    cs = json.loads(run(["python3", f"{C}/NulightJens_humanizer-stack/scripts/copy_scan.py", "--json", p]))["count"]
    st = list(json.loads(run(["python3", f"{C}/NulightJens_humanizer-stack/skills/structural-humanizer/scripts/structural_scan.py", "--json", p])).values())[0]
    stc = sum(len(st[k]) for k in ["embodied_emotion", "stated_lesson", "tidy_closer", "vague_allusion"])
    kf = run(["python3", f"{C}/keez97_humanizer/score.py", p, "--mode", "full"]); kl = run(["python3", f"{C}/keez97_humanizer/score.py", p, "--mode", "light"])
    kfr = re.search(r"RESULT: (\w+)", kf).group(1); kfh = len(re.findall(r"HARD\) \| FAIL", kf)); klr = re.search(r"RESULT: (\w+)", kl).group(1)
    ccf = run(["python3", f"{C}/ccf_humanize/skills/humanize/scripts/surface_scan.py", "--text", p]); cv = re.search(r"cv ([0-9.]+)", ccf)
    rows.append(f"| {f[:-3]} | {sd['density_per_1000_words']} ({'PASS' if sd['pass'] else 'FAIL'}) | {cs} | {stc} | {kfr} ({kfh}) | {klr} | {cv.group(1) if cv else '–'} |")
open(os.path.join(E, "results", "scanner_controls.md"), "w").write("\n".join(rows) + "\n\ns10, s11 and s12 are human-written (s12 has one chatbot sign-off added). s01-s09 and s13 are deliberately AI-shaped.\n")
print("\n".join(rows))
