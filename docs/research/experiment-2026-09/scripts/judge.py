#!/usr/bin/env python3
"""Blind LLM-judge pass for one sample: shuffle candidates (incl. untouched source), ask Opus for JSON scores."""
import json, os, random, re, subprocess, sys, time
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # experiment root (scripts/ lives inside it)
os.makedirs(os.path.join(E, "sandbox"), exist_ok=True)
REQ = "Please humanize this so it reads like a person wrote it. Keep the facts and meaning the same."
import os as _os
ARMS = _os.environ.get("JUDGE_ARMS", "U B O PS HZ HS AAW SD KZ").split()
TAG = _os.environ.get("JUDGE_TAG", "")
def judge(sample, rep="r1", jpass=1, model="claude-opus-5-5"):
    out = os.path.join(E, "judgments", rep + TAG, f"p{jpass}", f"{sample}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out) or os.path.exists(os.path.join(E, "STOP")):
        return out
    src = open(os.path.join(E, "corpus", f"{sample}.md"), encoding="utf-8").read().rstrip("\n")
    cands = {}
    for a in ARMS:
        if a == "U":
            cands[a] = src; continue
        f = os.path.join(E, "outputs", rep, a, f"{sample}.json")
        d = json.load(open(f))
        if d.get("extracted"): cands[a] = d["final"]
    order = list(cands); random.Random(f"{sample}-{rep}{TAG}-{jpass}").shuffle(order)
    letters = "ABCDEFGHIJ"
    key = {letters[i]: a for i, a in enumerate(order)}
    body = [f"REQUEST: {REQ}\n", "ORIGINAL:\n<<<\n" + src + "\n>>>\n"]
    for L, a in key.items():
        body.append(f"CANDIDATE {L}:\n<<<\n{cands[a]}\n>>>\n")
    user = "\n".join(body)
    cmd = ["claude", "-p", user, "--model", model, "--system-prompt-file", os.path.join(E, "judge_system.txt"),
           "--tools", "", "--strict-mcp-config", "--disable-slash-commands", "--setting-sources", "",
           "--no-session-persistence", "--output-format", "json"]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(E, "sandbox"), timeout=1200)
    d = json.loads(p.stdout)
    res = d.get("result", "") or ""
    if d.get("is_error") or "spend limit" in res:
        open(os.path.join(E, "STOP"), "w").write(res[:500]); sys.exit(3)
    m = re.search(r"\{.*\}", res, re.S)
    parsed = json.loads(m.group(0)) if m else None
    json.dump({"sample": sample, "rep": rep, "pass": jpass, "model": model, "key": key, "parsed": parsed,
               "raw": res, "cost_usd": d.get("total_cost_usd"), "user_prompt": user}, open(out, "w"), indent=1, ensure_ascii=False)
    return out
if __name__ == "__main__":
    print(judge(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "r1", int(sys.argv[3]) if len(sys.argv) > 3 else 1))
