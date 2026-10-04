"""Tests for scripts/preserve_check.py. Run: python3 -m unittest discover -s scripts/tests"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import preserve_check as pc  # noqa: E402

DOC = """---
title: Sync guide
tags: [sync]
---
# Tidewell 2.4

Tidewell 2.4 is a game-changer — uploads of files up to 2 GB are now 3x faster.
See [the docs](https://example.com/docs/sync) or the `tidewell sync` command.

## Install

```bash
pip install tidewell==2.4
tidewell sync --all
```

| Plan | Price |
|---|---|
| Team | $12 |
"""

GOOD = """---
title: Sync guide
tags: [sync]
---
# Tidewell 2.4

In Tidewell 2.4, files up to 2 GB upload 3x faster.
See [the docs](https://example.com/docs/sync) or the `tidewell sync` command.

## Install

```bash
pip install tidewell==2.4
tidewell sync --all
```

| Plan | Price |
|---|---|
| Team | $12 |
"""

PRESS = ('"Every student in our county deserves a path to higher education, regardless of their '
         'family\'s income," said Dr. Renata Oyelaran. The fund totals $6.2 million and covers '
         'about 300 students.')


def kinds(result, key):
    return " | ".join(result[key])


class CleanRewrite(unittest.TestCase):
    def test_good_rewrite_has_no_errors_or_warnings(self):
        r = pc.check(DOC, GOOD)
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["warnings"], [])
        self.assertEqual(r["metrics"]["dashes_source"], 1)
        self.assertEqual(r["metrics"]["dashes_output"], 0)

    def test_identical_output_is_reported_as_info(self):
        r = pc.check(DOC, DOC)
        self.assertEqual(r["errors"], [])
        self.assertIn("identical", kinds(r, "info"))
        self.assertEqual(r["metrics"]["change_ratio"], 0.0)

    def test_typographic_quotes_do_not_count_as_changes(self):
        src = 'She said "we ship on Thursday at noon" and left.'
        out = "She said “we ship on Thursday at noon” and left."
        self.assertEqual(pc.check(src, out)["errors"], [])


class Numbers(unittest.TestCase):
    def test_changed_figure_is_missing_and_added(self):
        r = pc.check(PRESS, PRESS.replace("$6.2 million", "$6 million"))
        self.assertIn("number missing: 6.2", r["errors"])
        self.assertIn("number added: 6", r["errors"])

    def test_thousands_separator_is_ignored(self):
        self.assertEqual(pc.check("It is 1,100 miles.", "It's 1100 miles.")["errors"], [])

    def test_unit_form_change_is_not_an_error(self):
        self.assertEqual(pc.check("a 14-day trial", "a trial of 14 days")["errors"], [])

    def test_spelled_out_number_is_info_not_error(self):
        r = pc.check("We hired 4 analysts.", "We hired four analysts.")
        self.assertEqual(r["errors"], [])
        self.assertIn("spelled out", kinds(r, "info"))
        r = pc.check("We hired four analysts.", "We hired 4 analysts.")
        self.assertEqual(r["errors"], [])

    def test_invented_number_is_an_error(self):
        r = pc.check("Uploads are faster now.", "Uploads are 40% faster now.")
        self.assertIn("number added: 40", r["errors"])


class Quotations(unittest.TestCase):
    def test_paraphrased_quote_is_an_error(self):
        out = PRESS.replace("regardless of their family's income", "no matter what their family earns")
        r = pc.check(PRESS, out)
        self.assertIn("quotation not verbatim", kinds(r, "errors"))

    def test_trailing_punctuation_inside_quote_may_move(self):
        out = ('Dr. Renata Oyelaran said: "Every student in our county deserves a path to higher '
               'education, regardless of their family\'s income." The fund totals $6.2 million and '
               'covers about 300 students.')
        self.assertEqual(pc.check(PRESS, out)["errors"], [])

    def test_fiction_dialogue_change_is_info(self):
        src = '"I am not selling the orchard to anyone," Marcus said.'
        out = '"Not selling," Marcus said.'
        self.assertIn("quotation not verbatim", kinds(pc.check(src, out), "errors"))
        r = pc.check(src, out, fiction=True)
        self.assertEqual(r["errors"], [])
        self.assertIn("dialogue may change", kinds(r, "info"))

    def test_short_scare_quotes_are_ignored(self):
        self.assertEqual(pc.check('This "humanize" step', "This humanize step")["errors"], [])


class CodeLinksFrontmatter(unittest.TestCase):
    def test_fenced_block_edit_is_an_error(self):
        r = pc.check(DOC, GOOD.replace("tidewell sync --all", "tidewell sync"))
        self.assertIn("fenced code block changed", kinds(r, "errors"))

    def test_inline_code_edit_is_an_error(self):
        r = pc.check(DOC, GOOD.replace("`tidewell sync`", "`tidewell-sync`"))
        self.assertIn("inline code changed or removed: `tidewell sync`", r["errors"])

    def test_link_target_edit_is_an_error(self):
        r = pc.check(DOC, GOOD.replace("https://example.com/docs/sync", "https://example.com/docs"))
        self.assertIn("URL or link target changed", kinds(r, "errors"))

    def test_relative_link_target_is_checked(self):
        r = pc.check("Read [setup](docs/setup.md) first.", "Read the setup guide first.")
        self.assertIn("URL or link target changed or removed: docs/setup.md", r["errors"])

    def test_frontmatter_edit_is_an_error(self):
        r = pc.check(DOC, GOOD.replace("title: Sync guide", "title: Sync Guide"))
        self.assertIn("frontmatter changed or removed", r["errors"])

    def test_numbers_in_code_are_checked_once_code_is_kept(self):
        r = pc.check(DOC, GOOD)
        self.assertNotIn("number", kinds(r, "errors"))


class Structure(unittest.TestCase):
    def test_removed_h1_is_a_warning(self):
        r = pc.check(DOC, GOOD.replace("# Tidewell 2.4\n\n", ""))
        self.assertIn("H1 count changed: 1 -> 0", r["warnings"])
        self.assertEqual(r["errors"], [])

    def test_hash_lines_inside_code_are_not_headings(self):
        src = "## Setup\n\n```sh\n# install\nmake\n```\n"
        self.assertEqual(pc.heading_levels(src), [2])

    def test_table_row_loss_is_a_warning(self):
        r = pc.check(DOC, GOOD.replace("| Team | $12 |\n", "Team costs $12.\n"))
        self.assertIn("table rows changed: 3 -> 2", r["warnings"])

    def test_added_dashes_are_a_warning_but_ranges_and_code_are_not_dashes(self):
        src = "The window is 9–17 June. Run `a --b` then stop."
        self.assertEqual(pc.dash_count(src), 0)
        r = pc.check("We moved the date. It was late.", "We moved the date — it was late.")
        self.assertIn("dashes added: 0 -> 1", kinds(r, "warnings"))

    def test_light_mode_flags_heavy_changes(self):
        src = "The meeting moved to Thursday. Bring the budget draft and the hiring plan."
        out = "Thursday now. Please have budget and hiring documents ready for review."
        r = pc.check(src, out, mode="light")
        self.assertIn("light edit changed", kinds(r, "warnings"))
        self.assertNotIn("light edit", kinds(pc.check(src, out), "warnings"))

    def test_large_cut_is_a_warning(self):
        src = " ".join(["The team shipped the release and documented every change carefully."] * 4)
        out = "The team shipped the release."
        self.assertIn("check for dropped claims", kinds(pc.check(src, out), "warnings"))

    def test_keep_strings(self):
        r = pc.check("Launch is in Q3 for the Henderson account.", "Launch is next quarter.",
                     keep=["Q3", "Henderson"])
        self.assertIn("kept string missing: Henderson", r["errors"])
        self.assertIn("kept string missing: Q3", r["errors"])


class CommandLine(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.src = os.path.join(self.dir.name, "src.md")
        self.out = os.path.join(self.dir.name, "out.md")
        with open(self.src, "w", encoding="utf-8") as f:
            f.write(PRESS)

    def tearDown(self):
        self.dir.cleanup()

    def run_main(self, out_text, *args):
        with open(self.out, "w", encoding="utf-8") as f:
            f.write(out_text)
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = pc.main([self.src, self.out, *args])
        return code, buf.getvalue()

    def test_exit_status_and_report(self):
        code, text = self.run_main(PRESS)
        self.assertEqual(code, 0)
        self.assertIn("0 error(s)", text)
        code, text = self.run_main(PRESS.replace("300", "350"))
        self.assertEqual(code, 1)
        self.assertIn("ERROR  number missing: 300", text)

    def test_json_output(self):
        code, text = self.run_main(PRESS, "--json")
        data = json.loads(text)
        self.assertEqual(code, 0)
        self.assertEqual(set(data), {"errors", "warnings", "info", "metrics"})

    def test_usage_errors(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                pc.main([self.src])
            self.assertEqual(pc.main([self.src, os.path.join(self.dir.name, "nope.md")]), 2)


if __name__ == "__main__":
    unittest.main()
