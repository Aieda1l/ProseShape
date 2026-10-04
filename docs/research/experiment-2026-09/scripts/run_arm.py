#!/usr/bin/env python3
"""Run one (arm, sample, replicate) through `claude -p` with an isolated, tool-less session."""
import json, os, re, subprocess, sys, time
E = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # experiment root (scripts/ lives inside it)
os.makedirs(os.path.join(E, "sandbox"), exist_ok=True)
REQ = "Please humanize this so it reads like a person wrote it. Keep the facts and meaning the same."
NOTE = ("(Formatting note for this session: after anything else you want to say, put the final version of the text, "
        "and nothing else, between a line containing only <<<FINAL>>> and a line containing only <<<END>>>.)")
ALIASES = {"PSo": ("PS", "claude-opus-5-5"), "Oo": ("O", "claude-opus-5-5"), "PSc": ("PSc", "claude-sonnet-5-5")}
def run(arm, sample, rep=1, model="claude-sonnet-5-5"):
    prompt_arm = arm
    if arm in ALIASES: prompt_arm, model = ALIASES[arm]
    out_dir = os.path.join(E, "outputs", f"r{rep}", arm); os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{sample}.json")
    if os.path.exists(out_path):
        return out_path
    if os.path.exists(os.path.join(E, "STOP")):
        sys.exit(3)
    text = open(os.path.join(E, "corpus", f"{sample}.md"), encoding="utf-8").read().rstrip("\n")
    user = f"{REQ}\n\n<text>\n{text}\n</text>\n\n{NOTE}"
    cmd = ["claude", "-p", user, "--model", model, "--system-prompt-file", os.path.join(E, "arms", f"{prompt_arm}.txt"),
           "--tools", "", "--strict-mcp-config", "--disable-slash-commands", "--setting-sources", "",
           "--no-session-persistence", "--output-format", "json"]
    for attempt in range(3):
        t0 = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(E, "sandbox"), timeout=900)
        try:
            d = json.loads(p.stdout)
        except Exception:
            d = {"is_error": True, "raw_stdout": p.stdout[-2000:], "stderr": p.stderr[-2000:]}
        if not d.get("is_error"):
            break
        time.sleep(10 * (attempt + 1))
    res = d.get("result", "") or ""
    if "spend limit" in res or "usage limit" in res.lower() or d.get("is_error"):
        open(os.path.join(E, "STOP"), "w").write(res[:500] or json.dumps(d)[:500])
        sys.exit(3)
    m = re.search(r"^<<<FINAL>>>\s*\n(.*?)\n<<<END>>>\s*$", res, re.S | re.M)
    rec = {"arm": arm, "sample": sample, "rep": rep, "model": model, "wall_s": round(time.time() - t0, 1),
           "final": m.group(1).strip("\n") if m else None, "extracted": bool(m), "reply": res,
           "is_error": d.get("is_error"), "cost_usd": d.get("total_cost_usd"), "usage": d.get("usage"),
           "modelUsage": list((d.get("modelUsage") or {}).keys()), "user_prompt": user}
    json.dump(rec, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return out_path
if __name__ == "__main__":
    arm, sample = sys.argv[1], sys.argv[2]
    rep = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    print(run(arm, sample, rep))
