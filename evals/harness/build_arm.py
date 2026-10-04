#!/usr/bin/env python3
"""Build a ProseShape arm prompt (SKILL.md plus the runtime references, inlined) and the baseline prompts.

  python3 build_arm.py PSnext                        # from the working tree
  python3 build_arm.py PS14g --rev a32e244           # from a commit: f8f69d4fa85aeb3c, 94909 bytes
  python3 build_arm.py PS --rev 57d58e4 --blank-lines 2   # v1.3.1 as built for the 2026-09 experiment: 68f2520c6a1b4312

Writes work/arms/<NAME>.txt, plus O.txt and B.txt copied from the 2026-09 experiment. An arm file is never
silently replaced: if <NAME>.txt exists with different content, the script stops, so a name always means one prompt.
Competitor arms (HS, HZ, ...) come from docs/research/experiment-2026-09/scripts/build_arms.py with ARMS_OUT=work/arms.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

from common import PROMPTS, REPO, path

WRAP = ("The following agent skill is installed and has been invoked for this request. Follow its instructions. "
        "Its SKILL.md and the reference files it tells you to read are reproduced below in full. "
        "You have no tools in this session: you cannot read files or run scripts. Wherever the skill says to read a file, use the copy below; "
        "wherever it says to run a script or command, skip that step (you may say it was not run).\n")
RUNTIME_FILES = ["SKILL.md", "references/humanizer-rules.md", "references/storyscope-rules.md",
                 "references/mode-guidance.md", "references/examples.md", "references/evaluation-rubric.md"]
# Where the skill folder lives: the plugin layout first, then the repository root (commits before the move).
SKILL_DIRS = ["plugins/proseshape/skills/proseshape", ""]


def read(rel, rev):
    for d in SKILL_DIRS:
        rel_path = f"{d}/{rel}" if d else rel
        if rev:
            p = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{rel_path}"], capture_output=True, text=True)
            if p.returncode == 0:
                return p.stdout
        elif os.path.exists(os.path.join(REPO, rel_path)):
            with open(os.path.join(REPO, rel_path), encoding="utf-8") as f:
                return f.read()
    sys.exit(f"{rel} not found{' at ' + rev if rev else ''} under {SKILL_DIRS}")


def build(rev=None, blank_lines=1, files=RUNTIME_FILES):
    parts = [WRAP + "\n" * (blank_lines - 1)] + [f"=== FILE: {rel} ===\n" + read(rel, rev).rstrip() + "\n" for rel in files]
    return "\n".join(parts)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("name", help="arm name, e.g. PSnext")
    p.add_argument("--rev", help="git revision to read the skill from (default: working tree)")
    p.add_argument("--blank-lines", type=int, default=1, help="blank lines after the wrapper (1 for the v1.4 runs, 2 for the 2026-09 runs)")
    p.add_argument("--skill-only", action="store_true", help="SKILL.md alone, no references")
    a = p.parse_args()
    txt = build(a.rev, a.blank_lines, RUNTIME_FILES[:1] if a.skill_only else RUNTIME_FILES)
    os.makedirs(path("arms"), exist_ok=True)
    out = path("arms", f"{a.name}.txt")
    if os.path.exists(out):
        with open(out, encoding="utf-8") as f:
            if f.read() != txt:
                sys.exit(f"{out} exists with different content; pick a new arm name so results stay attributable")
    else:
        with open(out, "w", encoding="utf-8") as f:
            f.write(txt)
    for name in ("O.txt", "B.txt"):
        if not os.path.exists(path("arms", name)):
            shutil.copy(os.path.join(PROMPTS, name), path("arms", name))
    print(a.name, len(txt.encode()), hashlib.sha256(txt.encode()).hexdigest()[:16])


if __name__ == "__main__":
    main()
