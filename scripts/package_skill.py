#!/usr/bin/env python3
"""Check the ProseShape plugin and skill, then build the skill zip for claude.ai and other Agent Skills tools.

  python3 scripts/package_skill.py            # check, then write dist/proseshape-<version>.zip
  python3 scripts/package_skill.py --check    # checks only (CI)
  python3 scripts/package_skill.py --out DIR  # write the zip somewhere else

The zip holds one top-level folder, proseshape/, with SKILL.md, the reference files, LICENSE, and
THIRD_PARTY_NOTICES.md, which is the layout claude.ai's Customize > Skills upload expects. The archive is
deterministic: the same files always give the same bytes.

The checks cover what the Agent Skills specification, claude.ai, and the Claude plugin directory require of the
files (name, description length, referenced files, versions that agree, README and license, file sizes). They do
not replace `claude plugin validate --strict plugins/proseshape` or the directory portal's own validation.
Standard library only; Python 3.8+. Exit status: 0 clean, 1 problems found.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PLUGIN_REL = os.path.join("plugins", "proseshape")
SKILL_REL = os.path.join(PLUGIN_REL, "skills", "proseshape")
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SYSTEM_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}
MAX_FILE = 256 * 1024
MAX_FILES = 512
ZIP_DATE = (1980, 1, 1, 0, 0, 0)


def frontmatter(text):
    """Parse the simple YAML frontmatter ProseShape uses: top-level keys and one level of nested keys."""
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    data, parent = {}, None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        km = re.match(r"^(\s*)([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not km:
            continue
        indent, key, value = km.groups()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if indent and parent is not None:
            data[parent][key] = value
        elif value == "":
            parent = key
            data[key] = {}
        else:
            parent = None
            data[key] = value
    return data


def words_outside_code(text):
    return len(re.findall(r"\w+", re.sub(r"```.*?```", " ", text, flags=re.S)))


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return f.read()


def load_json(root, rel, problems):
    try:
        return json.loads(read(root, rel))
    except (OSError, ValueError) as e:
        problems.append(f"{rel}: {e}")
        return None


def plugin_files(root):
    base = os.path.join(root, PLUGIN_REL)
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames.sort()
        for fn in sorted(filenames):
            yield os.path.join(dirpath, fn)


def check(root=REPO):
    """Return a list of problems; an empty list means the plugin and skill are ready to package."""
    problems = []
    skill_md = os.path.join(SKILL_REL, "SKILL.md")
    try:
        text = read(root, skill_md)
    except OSError:
        return [f"{skill_md} is missing"]
    fm = frontmatter(text)
    if fm is None:
        return [f"{skill_md}: no YAML frontmatter"]
    name, desc = fm.get("name", ""), fm.get("description", "")
    version = (fm.get("metadata") or {}).get("version", "") if isinstance(fm.get("metadata"), dict) else ""
    if not NAME_RE.match(name):
        problems.append(f"{skill_md}: name {name!r} must be lowercase letters, digits, and hyphens, at most 64 characters")
    if name != os.path.basename(SKILL_REL):
        problems.append(f"{skill_md}: name {name!r} must match its folder name {os.path.basename(SKILL_REL)!r}")
    if not 1 <= len(desc) <= 1024:
        problems.append(f"{skill_md}: description is {len(desc)} characters; the limit is 1,024")
    if text.count("\n") > 500:
        problems.append(f"{skill_md}: {text.count(chr(10))} lines; keep SKILL.md under 500")
    for ref in sorted(set(re.findall(r"references/[A-Za-z0-9_.-]+\.md", text))):
        if not os.path.exists(os.path.join(root, SKILL_REL, ref)):
            problems.append(f"{skill_md} mentions {ref}, which does not exist")

    manifest_rel = os.path.join(PLUGIN_REL, ".claude-plugin", "plugin.json")
    manifest = load_json(root, manifest_rel, problems)
    if manifest:
        if manifest.get("name") != name:
            problems.append(f"{manifest_rel}: name {manifest.get('name')!r} differs from the skill name {name!r}")
        if manifest.get("version") != version:
            problems.append(f"{manifest_rel}: version {manifest.get('version')!r} differs from SKILL.md metadata.version {version!r}")
        for field in ("description", "author", "license"):
            if not manifest.get(field):
                problems.append(f"{manifest_rel}: set {field}")

    market_rel = os.path.join(".claude-plugin", "marketplace.json")
    market = load_json(root, market_rel, problems)
    if market:
        entries = [p for p in market.get("plugins", []) if p.get("name") == (manifest or {}).get("name")]
        if not entries:
            problems.append(f"{market_rel}: no plugin entry named {(manifest or {}).get('name')!r}")
        elif os.path.normpath(entries[0].get("source", "")) != os.path.normpath(PLUGIN_REL):
            problems.append(f"{market_rel}: the entry's source should be ./{PLUGIN_REL.replace(os.sep, '/')}")

    for rel in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        copy = os.path.join(PLUGIN_REL, rel)
        try:
            if read(root, rel) != read(root, copy):
                problems.append(f"{copy} differs from {rel}; copy it again")
        except OSError as e:
            problems.append(f"{copy}: {e.strerror}")
    try:
        if words_outside_code(read(root, os.path.join(PLUGIN_REL, "README.md"))) < 40:
            problems.append(f"{PLUGIN_REL}/README.md needs at least 40 words outside code blocks")
    except OSError:
        problems.append(f"{PLUGIN_REL}/README.md is missing")

    files = list(plugin_files(root))
    if len(files) > MAX_FILES:
        problems.append(f"{PLUGIN_REL} has {len(files)} files; the directory reviews plugins over {MAX_FILES}")
    for path in files:
        rel = os.path.relpath(path, root)
        if os.path.basename(path) in SYSTEM_FILES or "__MACOSX" in rel.split(os.sep):
            problems.append(f"{rel}: system file; delete it")
        if os.path.islink(path):
            problems.append(f"{rel}: symbolic link; commit a regular file")
        elif os.path.getsize(path) > MAX_FILE:
            problems.append(f"{rel}: {os.path.getsize(path)} bytes; keep plugin files under 256 KiB")
    return problems


def build(root=REPO, out_dir=None):
    """Write the skill zip and return its path."""
    manifest = json.loads(read(root, os.path.join(PLUGIN_REL, ".claude-plugin", "plugin.json")))
    name, version = manifest["name"], manifest["version"]
    out_dir = out_dir or os.path.join(root, "dist")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{name}-{version}.zip")
    entries = []
    skill_dir = os.path.join(root, SKILL_REL)
    for dirpath, dirnames, filenames in os.walk(skill_dir):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            entries.append((f"{name}/" + os.path.relpath(full, skill_dir).replace(os.sep, "/"), full))
    for rel in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        entries.append((f"{name}/{rel}", os.path.join(root, PLUGIN_REL, rel)))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for arcname, full in sorted(entries):
            info = zipfile.ZipInfo(arcname, date_time=ZIP_DATE)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(full, "rb") as f:
                z.writestr(info, f.read())
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Check the ProseShape plugin and build the skill zip.")
    p.add_argument("--check", action="store_true", help="run the checks only")
    p.add_argument("--out", help="directory for the zip (default: dist/)")
    a = p.parse_args(argv)
    problems = check()
    for pr in problems:
        print(f"PROBLEM  {pr}")
    if problems:
        return 1
    print("checks passed")
    if a.check:
        return 0
    out = build(out_dir=a.out)
    with open(out, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    with zipfile.ZipFile(out) as z:
        count = len(z.namelist())
    shown = os.path.relpath(out)
    print(f"wrote {out if shown.startswith('..') else shown} ({count} files, sha256 {digest[:16]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
