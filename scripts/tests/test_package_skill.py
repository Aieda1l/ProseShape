"""Tests for scripts/package_skill.py. Run: python3 -m unittest discover -s scripts/tests"""
import hashlib
import os
import shutil
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import package_skill as ps  # noqa: E402


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class Repository(unittest.TestCase):
    def test_repository_passes_every_check(self):
        self.assertEqual(ps.check(), [])

    def test_zip_layout_and_determinism(self):
        with tempfile.TemporaryDirectory() as d:
            first = ps.build(out_dir=os.path.join(d, "a"))
            second = ps.build(out_dir=os.path.join(d, "b"))
            self.assertEqual(sha(first), sha(second))
            with zipfile.ZipFile(first) as z:
                names = z.namelist()
            self.assertTrue(all(n.startswith("proseshape/") for n in names))
            for required in ("proseshape/SKILL.md", "proseshape/LICENSE", "proseshape/THIRD_PARTY_NOTICES.md",
                             "proseshape/references/humanizer-rules.md", "proseshape/agents/openai.yaml"):
                self.assertIn(required, names)


class OpenAIZip(unittest.TestCase):
    def test_layout_and_determinism(self):
        with tempfile.TemporaryDirectory() as d:
            first = ps.build_openai(out_dir=os.path.join(d, "a"))
            second = ps.build_openai(out_dir=os.path.join(d, "b"))
            self.assertEqual(sha(first), sha(second))
            self.assertTrue(os.path.basename(first).startswith("proseshape-openai-"))
            with zipfile.ZipFile(first) as z:
                names = z.namelist()
        for required in ("plugin.json", "skills/proseshape/SKILL.md", "assets/icon.svg", "README.md", "LICENSE"):
            self.assertIn(required, names)
        self.assertFalse([n for n in names if n.startswith(".claude-plugin")])
        self.assertTrue(all(ps.safe_member(n) for n in names))

    def test_unsafe_member_names_are_refused(self):
        for bad in (".claude-plugin\\plugin.json", "../escape.md", "/abs.md", "a//b.md", "C:/x.md", "./x.md"):
            self.assertFalse(ps.safe_member(bad), bad)
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "f.txt")
            open(src, "w").close()
            with self.assertRaises(ValueError):
                ps.write_zip(os.path.join(d, "out.zip"), [("dir\\f.txt", src)])


class Frontmatter(unittest.TestCase):
    def test_nested_metadata_and_quotes(self):
        fm = ps.frontmatter('---\nname: x\ndescription: "Does a thing."\nmetadata:\n  version: "1.2.3"\n---\nBody\n')
        self.assertEqual(fm["name"], "x")
        self.assertEqual(fm["description"], "Does a thing.")
        self.assertEqual(fm["metadata"]["version"], "1.2.3")

    def test_missing_frontmatter(self):
        self.assertIsNone(ps.frontmatter("# No frontmatter\n"))


class BrokenCopies(unittest.TestCase):
    """Copy the files the checks read into a temporary repository, then break one thing at a time."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        for rel in (".claude-plugin", ".agents", ps.PLUGIN_REL, "LICENSE", "THIRD_PARTY_NOTICES.md"):
            src = os.path.join(ps.REPO, rel)
            dst = os.path.join(self.root, rel)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
        self.assertEqual(ps.check(self.root), [])

    def tearDown(self):
        self.tmp.cleanup()

    def edit(self, rel, old, new):
        path = os.path.join(self.root, rel)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.assertIn(old, text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace(old, new, 1))

    def problems(self):
        return " | ".join(ps.check(self.root))

    def test_description_too_long(self):
        self.edit(os.path.join(ps.SKILL_REL, "SKILL.md"), "description: ", "description: " + "x" * 1100)
        self.assertIn("the limit is 1,024", self.problems())

    def test_version_mismatch(self):
        self.edit(os.path.join(ps.PLUGIN_REL, ".claude-plugin", "plugin.json"), '"version": "', '"version": "9.')
        self.assertIn("differs from SKILL.md metadata.version", self.problems())

    def test_stale_license_copy(self):
        with open(os.path.join(self.root, "LICENSE"), "a", encoding="utf-8") as f:
            f.write("\nchanged\n")
        self.assertIn("differs from LICENSE", self.problems())

    def test_missing_reference_file(self):
        os.remove(os.path.join(self.root, ps.SKILL_REL, "references", "examples.md"))
        self.assertIn("mentions references/examples.md", self.problems())

    def test_large_file_and_system_file(self):
        with open(os.path.join(self.root, ps.PLUGIN_REL, "big.txt"), "w") as f:
            f.write("x" * (ps.MAX_FILE + 1))
        open(os.path.join(self.root, ps.PLUGIN_REL, ".DS_Store"), "w").close()
        found = self.problems()
        self.assertIn("keep plugin files under 256 KiB", found)
        self.assertIn("system file", found)

    def test_claude_icon_must_exist(self):
        self.edit(os.path.join(ps.PLUGIN_REL, ".claude-plugin", "plugin.json"), '"icon": "./assets/icon.svg"',
                  '"icon": "./assets/missing.svg"')
        self.assertIn("icon './assets/missing.svg' must be a ./ path", self.problems())

    def test_codex_manifest_version_mismatch(self):
        self.edit(os.path.join(ps.PLUGIN_REL, "plugin.json"), '"version": "', '"version": "9.')
        self.assertIn("plugin.json: version", self.problems())

    def test_codex_short_description_limit(self):
        self.edit(os.path.join(ps.PLUGIN_REL, "plugin.json"), '"shortDescription": "', '"shortDescription": "' + "y" * 40)
        self.assertIn("interface.shortDescription is", self.problems())

    def test_codex_unknown_top_level_key(self):
        self.edit(os.path.join(ps.PLUGIN_REL, "plugin.json"), '"license": "MIT",', '"license": "MIT", "skills": "./skills/",')
        self.assertIn("'skills' isn't allowed at the top level", self.problems())

    def test_codex_missing_icon(self):
        os.remove(os.path.join(self.root, ps.PLUGIN_REL, "assets", "icon.svg"))
        self.assertIn("interface.composerIcon", self.problems())

    def test_codex_marketplace_policy(self):
        self.edit(os.path.join(".agents", "plugins", "marketplace.json"), '"AVAILABLE"', '"SOMETIMES"')
        self.assertIn("policy.installation must be one of", self.problems())

    def test_short_readme(self):
        with open(os.path.join(self.root, ps.PLUGIN_REL, "README.md"), "w", encoding="utf-8") as f:
            f.write("# ProseShape\n\nToo short.\n")
        self.assertIn("at least 40 words", self.problems())


if __name__ == "__main__":
    unittest.main()
