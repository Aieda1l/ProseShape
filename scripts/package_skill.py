#!/usr/bin/env python3
"""Check the ProseShape plugin (Claude and Codex) and skill, then build the release zips.

  python3 scripts/package_skill.py            # check, then write both zips to dist/
  python3 scripts/package_skill.py --check    # checks only (CI)
  python3 scripts/package_skill.py --out DIR  # write the zips somewhere else

Two zips:
- proseshape-<version>.zip: one top-level folder, proseshape/, with SKILL.md, the reference files, LICENSE, and
  THIRD_PARTY_NOTICES.md. This is the layout claude.ai's Customize > Skills upload and other Agent Skills tools expect.
- proseshape-openai-<version>.zip: the plugin folder's contents with plugin.json at the zip root, for upload at
  platform.openai.com/plugins. The Claude-only .claude-plugin/ folder is left out; Codex reads the portable manifest.

Member names always use forward slashes, even on Windows. Zips made with Windows' built-in "Compressed folder" or
older Compress-Archive use backslashes, which OpenAI rejects as unsafe paths. Both archives are deterministic: the
same files always give the same bytes.

The checks cover what the Agent Skills specification, claude.ai, the Claude plugin directory, and Codex require of
the files: name, description length, referenced files, versions that agree across the Claude and portable (Codex)
manifests, both marketplace files, Codex interface limits and icons, README and license, and file sizes. They do not
replace `claude plugin validate --strict plugins/proseshape`, a Codex install, or either directory's own validation.
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
PORTABLE_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PORTABLE_KEYS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license",
                 "keywords", "extensions"}
# Codex interface limits from OpenAI's plugin submission guide.
CODEX_LIMITS = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}
CODEX_INSTALLATION = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
CODEX_AUTHENTICATION = {"ON_INSTALL", "ON_USE"}
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

    problems += check_codex(root, name, version, (market or {}).get("name"))

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


def check_codex(root, name, version, claude_market_name):
    """Checks for the portable plugin.json (read by Codex) and .agents/plugins/marketplace.json."""
    problems = []
    rel = os.path.join(PLUGIN_REL, "plugin.json")
    m = load_json(root, rel, problems)
    if m:
        if m.get("$schema") != PORTABLE_SCHEMA:
            problems.append(f"{rel}: $schema must be {PORTABLE_SCHEMA}")
        for key in sorted(set(m) - PORTABLE_KEYS):
            problems.append(f"{rel}: {key!r} isn't allowed at the top level; put client data under extensions")
        if m.get("name") != name:
            problems.append(f"{rel}: name {m.get('name')!r} differs from the skill name {name!r}")
        if m.get("version") != version:
            problems.append(f"{rel}: version {m.get('version')!r} differs from SKILL.md metadata.version {version!r}")
        ui = ((m.get("extensions") or {}).get("com.openai") or {}).get("interface")
        if not isinstance(ui, dict):
            problems.append(f"{rel}: add extensions.com.openai.interface for Codex")
            ui = {}
        for field, limit in CODEX_LIMITS.items():
            value = ui.get(field, "")
            if not value:
                problems.append(f"{rel}: set interface.{field}")
            elif len(value) > limit:
                problems.append(f"{rel}: interface.{field} is {len(value)} characters; the limit is {limit}")
        if not ui.get("category"):
            problems.append(f"{rel}: set interface.category")
        if not isinstance(ui.get("capabilities"), list):
            problems.append(f"{rel}: set interface.capabilities to a list (it may be empty)")
        for field in ("composerIcon", "logo"):
            icon = ui.get(field)
            path = os.path.join(root, PLUGIN_REL, icon) if icon else None
            if not icon:
                problems.append(f"{rel}: set interface.{field}")
            elif not icon.startswith("./") or not os.path.exists(path):
                problems.append(f"{rel}: interface.{field} {icon!r} must be a ./ path to a file in the plugin")
            elif icon.endswith(".svg"):
                with open(path, encoding="utf-8") as f:
                    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', f.read())
                if not vb or vb.group(1) != vb.group(2) or float(vb.group(1)) < 48:
                    problems.append(f"{rel}: interface.{field} must be square and at least 48 by 48")

    rel = os.path.join(".agents", "plugins", "marketplace.json")
    market = load_json(root, rel, problems)
    if market:
        if claude_market_name and market.get("name") != claude_market_name:
            problems.append(f"{rel}: name {market.get('name')!r} should match the Claude marketplace name {claude_market_name!r}")
        entries = [p for p in market.get("plugins", []) if p.get("name") == name]
        if not entries:
            problems.append(f"{rel}: no plugin entry named {name!r}")
        else:
            e = entries[0]
            src = e.get("source") or {}
            if src.get("source") != "local" or os.path.normpath(src.get("path", "")) != os.path.normpath(PLUGIN_REL):
                problems.append(f"{rel}: the entry's source should be local, path ./{PLUGIN_REL.replace(os.sep, '/')}")
            policy = e.get("policy") or {}
            if policy.get("installation") not in CODEX_INSTALLATION:
                problems.append(f"{rel}: policy.installation must be one of {sorted(CODEX_INSTALLATION)}")
            if policy.get("authentication") not in CODEX_AUTHENTICATION:
                problems.append(f"{rel}: policy.authentication must be one of {sorted(CODEX_AUTHENTICATION)}")
            if not e.get("category"):
                problems.append(f"{rel}: set the entry's category")
    return problems


def safe_member(name):
    """True for a relative, forward-slash zip member name with no empty, '.' or '..' parts."""
    parts = name.split("/")
    return ("\\" not in name and not name.startswith("/") and ":" not in parts[0]
            and all(p not in ("", ".", "..") for p in parts))


def files_under(base):
    """(path relative to base with forward slashes, full path) for every file, in a stable order."""
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            out.append((os.path.relpath(full, base).replace(os.sep, "/"), full))
    return out


def write_zip(out, entries):
    bad = [arc for arc, _ in entries if not safe_member(arc)]
    if bad:
        raise ValueError(f"unsafe zip member names: {bad}")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for arcname, full in sorted(entries):
            info = zipfile.ZipInfo(arcname, date_time=ZIP_DATE)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(full, "rb") as f:
                z.writestr(info, f.read())
    return out


def _name_version(root):
    manifest = json.loads(read(root, os.path.join(PLUGIN_REL, ".claude-plugin", "plugin.json")))
    return manifest["name"], manifest["version"]


def build(root=REPO, out_dir=None):
    """Write the skill zip (one top-level folder named after the skill) and return its path."""
    name, version = _name_version(root)
    out_dir = out_dir or os.path.join(root, "dist")
    os.makedirs(out_dir, exist_ok=True)
    entries = [(f"{name}/{rel}", full) for rel, full in files_under(os.path.join(root, SKILL_REL))]
    for rel in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        entries.append((f"{name}/{rel}", os.path.join(root, PLUGIN_REL, rel)))
    return write_zip(os.path.join(out_dir, f"{name}-{version}.zip"), entries)


def build_openai(root=REPO, out_dir=None):
    """Write the OpenAI plugin zip (plugin.json at the zip root, no .claude-plugin/) and return its path."""
    name, version = _name_version(root)
    out_dir = out_dir or os.path.join(root, "dist")
    os.makedirs(out_dir, exist_ok=True)
    entries = [(rel, full) for rel, full in files_under(os.path.join(root, PLUGIN_REL))
               if not rel.startswith(".claude-plugin/")]
    return write_zip(os.path.join(out_dir, f"{name}-openai-{version}.zip"), entries)


def main(argv=None):
    p = argparse.ArgumentParser(description="Check the ProseShape plugin and build the release zips.")
    p.add_argument("--check", action="store_true", help="run the checks only")
    p.add_argument("--out", help="directory for the zips (default: dist/)")
    a = p.parse_args(argv)
    problems = check()
    for pr in problems:
        print(f"PROBLEM  {pr}")
    if problems:
        return 1
    print("checks passed")
    if a.check:
        return 0
    for out in (build(out_dir=a.out), build_openai(out_dir=a.out)):
        with open(out, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        with zipfile.ZipFile(out) as z:
            count = len(z.namelist())
        shown = os.path.relpath(out)
        print(f"wrote {out if shown.startswith('..') else shown} ({count} files, sha256 {digest[:16]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
