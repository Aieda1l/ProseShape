#!/usr/bin/env python3
"""Rebuild the skill-arm system prompts used in this experiment.

Competitor skills are not redistributed here. Clone each repository at the pinned commit
into COMP_DIR (default: ../comp relative to the experiment directory), then run this script.
The SHA-256 prefixes it prints should match prompts/arms_meta.json.

  blader/humanizer                      225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8 -> COMP_DIR/blader_humanizer
  Anson-Saju-George/HumanScope          51b343ac96d9f8be10ad76955e01a9e9beb4661c -> COMP_DIR/Anson-Saju-George_HumanScope
  conorbronsdon/avoid-ai-writing        9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43 -> COMP_DIR/conorbronsdon_avoid-ai-writing
  shir-danishyar/humanize               024aa193966341e0706e96f0277f914092bed2c7 -> COMP_DIR/shir-danishyar_humanize
  keez97/humanizer                      2d9a116fa9caee2c3466a7c7d419cbe02b35a470 -> COMP_DIR/keez97_humanizer
ProseShape itself is read from PS_DIR (default: the repository root, commit 57d58e4f860c95b29a028c157a33dde07de09021).
"""
import hashlib, json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.environ.get("COMP_DIR", os.path.join(HERE, "..", "comp"))
PS = os.environ.get("PS_DIR", os.path.abspath(os.path.join(HERE, "..", "..", "..")))
OUT = os.environ.get("ARMS_OUT", os.path.join(HERE, "arms"))
WRAP = ("The following agent skill is installed and has been invoked for this request. Follow its instructions. "
        "Its SKILL.md and the reference files it tells you to read are reproduced below in full. "
        "You have no tools in this session: you cannot read files or run scripts. Wherever the skill says to read a file, use the copy below; "
        "wherever it says to run a script or command, skip that step (you may say it was not run).\n\n")
ARMS = {
 "PS":  [(PS, "SKILL.md"), (PS, "references/humanizer-rules.md"), (PS, "references/storyscope-rules.md"),
         (PS, "references/mode-guidance.md"), (PS, "references/examples.md"), (PS, "references/evaluation-rubric.md")],
 "PSc": [(PS, "SKILL.md")],
 "HZ":  [(f"{C}/blader_humanizer", "SKILL.md")],
 "HS":  [(f"{C}/Anson-Saju-George_HumanScope", "SKILL.md")],
 "AAW": [(f"{C}/conorbronsdon_avoid-ai-writing", "SKILL.md"), (f"{C}/conorbronsdon_avoid-ai-writing", "references/patterns.md")],
 "SD":  [(f"{C}/shir-danishyar_humanize", "SKILL.md"), (f"{C}/shir-danishyar_humanize", "references/patterns.md"),
         (f"{C}/shir-danishyar_humanize", "references/vocabulary.md")],
 "KZ":  [(f"{C}/keez97_humanizer", "SKILL.md")],
}
os.makedirs(OUT, exist_ok=True)
for arm, files in ARMS.items():
    parts = [WRAP] + [f"=== FILE: {rel} ===\n" + open(os.path.join(root, rel), encoding="utf-8").read().rstrip() + "\n" for root, rel in files]
    txt = "\n".join(parts)
    if arm == "PSc":  # PSc is the PS prompt truncated before the first reference file
        txt = txt.rstrip() + "\n"
    open(os.path.join(OUT, f"{arm}.txt"), "w", encoding="utf-8").write(txt)
    print(arm, len(txt.encode()), hashlib.sha256(txt.encode()).hexdigest()[:16])
for name in ("B.txt", "O.txt"):
    src = os.path.join(HERE, "prompts", name)
    open(os.path.join(OUT, name), "w").write(open(src).read())
