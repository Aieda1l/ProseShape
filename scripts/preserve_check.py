#!/usr/bin/env python3
"""Check that a rewrite kept what a rewrite must keep.

Compares a source text with an edited version and reports what changed that
should not have: numbers, quotations, URLs and link targets, inline code,
fenced code blocks, YAML frontmatter, and any strings you name with --keep.
It also reports structure (headings, table rows), how much of the text
changed, length, and dash use.

This is a preservation check, not a quality score and not an AI detector.
A clean report means nothing protected was lost; it says nothing about
whether the rewrite reads well.

Usage:
  python3 scripts/preserve_check.py SOURCE OUTPUT [options]
  python3 scripts/preserve_check.py draft.md revised.md --mode light
  python3 scripts/preserve_check.py story.md rewrite.md --fiction
  python3 scripts/preserve_check.py memo.md new.md --keep "Q3 launch" --json

Use "-" for one of the paths to read it from stdin.
Exit status: 0 no errors, 1 errors found, 2 usage problem.
Standard library only; Python 3.8+.
"""
import argparse
import difflib
import json
import re
import sys

NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
    "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
    "nineteen": "19", "twenty": "20", "thirty": "30", "forty": "40",
    "fifty": "50", "sixty": "60", "seventy": "70", "eighty": "80",
    "ninety": "90", "hundred": "100",
}
WORDS_FOR = {v: k for k, v in NUMBER_WORDS.items()}

FENCE = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[ \t]*$", re.S | re.M)
FRONTMATTER = re.compile(r"\A---[ \t]*\n.*?\n---[ \t]*(?:\n|\Z)", re.S)
INLINE_CODE = re.compile(r"`[^`\n]+`")
URL = re.compile(r"https?://[^\s<>()\[\]\"'`]+")
LINK_TARGET = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
NUMBER = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")
QUOTE = re.compile(r"\"([^\"\n]+)\"")
HEADING = re.compile(r"^(#{1,6})[ \t]+\S", re.M)
TABLE_ROW = re.compile(r"^[ \t]*\|.*\|[ \t]*$", re.M)
DASH = re.compile(r"[—–]|(?<=\s)--(?=\s)")
RANGE_DASH = re.compile(r"(?<=\d)[–—-](?=\d)")
WORD = re.compile(r"\w+(?:'\w+)*")
TOKEN = re.compile(r"\w+(?:'\w+)*|[^\w\s]")


def normalize(text):
    """Fold typographic quotes and spaces so they do not count as changes."""
    return (text.replace("’", "'").replace("‘", "'")
                .replace("“", '"').replace("”", '"')
                .replace(" ", " ").replace("\r\n", "\n"))


def squash(text):
    return re.sub(r"\s+", " ", text).strip()


def frontmatter(text):
    m = FRONTMATTER.match(text)
    return m.group(0).rstrip("\n") if m else None


def fenced_blocks(text):
    return [m.group(0).rstrip() for m in FENCE.finditer(text)]


def without_fences(text):
    return FENCE.sub("\n", text)


def without_code(text):
    """Text with frontmatter, fenced blocks, and inline code removed."""
    fm = frontmatter(text)
    if fm:
        text = text[len(fm):]
    return INLINE_CODE.sub(" ", without_fences(text))


def prose_only(text):
    """Text with code and URLs removed: the part a prose editor should touch."""
    return URL.sub(" ", without_code(text))


def numbers(text):
    """Digit sequences in prose and code, commas dropped ("1,100" == "1100")."""
    out = []
    for n in NUMBER.findall(text):
        n = n.rstrip(",.").replace(",", "")
        if n:
            out.append(n)
    return out


def number_words(text):
    found = set()
    for w in WORD.findall(text.lower()):
        if w in NUMBER_WORDS:
            found.add(NUMBER_WORDS[w])
    return found


def quotations(text, min_words=3):
    """Double-quoted passages of at least min_words words, outside code."""
    out = []
    for q in QUOTE.findall(without_code(text)):
        if len(WORD.findall(q)) >= min_words:
            out.append(squash(q).rstrip(",.;:!? "))
    return out


def urls(text):
    found = [u.rstrip(".,;:!?") for u in URL.findall(text)]
    found += [t for t in LINK_TARGET.findall(text) if not t.startswith("http")]
    return found


def heading_levels(text):
    return [len(h) for h in HEADING.findall(without_fences(text))]


def table_rows(text):
    return len(TABLE_ROW.findall(without_fences(text)))


def dash_count(text):
    prose = RANGE_DASH.sub(" ", prose_only(text))
    return len(DASH.findall(prose))


def word_count(text):
    return len(WORD.findall(text))


def change_ratio(a, b):
    """Share of word-level tokens that differ: 0.0 identical, 1.0 nothing shared."""
    ta, tb = TOKEN.findall(a), TOKEN.findall(b)
    if not ta and not tb:
        return 0.0
    return round(1 - difflib.SequenceMatcher(a=ta, b=tb, autojunk=False).ratio(), 3)


def check(source, output, mode="rewrite", fiction=False, keep=(),
          light_change_limit=0.2, min_length=0.7, max_length=1.15):
    """Return {"errors", "warnings", "info", "metrics"} for one source/output pair."""
    src, out = normalize(source), normalize(output)
    errors, warnings, info = [], [], []

    fm_src, fm_out = frontmatter(src), frontmatter(out)
    if fm_src is not None and fm_src != fm_out:
        errors.append("frontmatter changed or removed")

    out_blocks = fenced_blocks(out)
    for block in fenced_blocks(src):
        if block not in out_blocks:
            first = block.splitlines()[0] if block else ""
            errors.append(f"fenced code block changed or removed (starts {first!r})")

    for code in dict.fromkeys(INLINE_CODE.findall(without_fences(src))):
        if code not in out:
            errors.append(f"inline code changed or removed: {code}")

    out_urls = set(urls(out))
    for u in dict.fromkeys(urls(src)):
        if u not in out_urls and u not in out:
            errors.append(f"URL or link target changed or removed: {u}")

    src_nums, out_nums = numbers(src), numbers(out)
    src_words, out_words = number_words(src), number_words(out)
    for n in dict.fromkeys(src_nums):
        if n in out_nums:
            continue
        if n in out_words:
            info.append(f"number {n} now spelled out ({WORDS_FOR.get(n, n)})")
        else:
            errors.append(f"number missing: {n}")
    for n in dict.fromkeys(out_nums):
        if n in src_nums:
            continue
        if n in src_words:
            info.append(f"number {n} was spelled out in the source")
        else:
            errors.append(f"number added: {n}")

    out_flat = squash(without_code(out))
    for q in dict.fromkeys(quotations(src)):
        if q in out_flat:
            continue
        msg = f"quotation not verbatim: \"{q[:70]}{'...' if len(q) > 70 else ''}\""
        (info if fiction else errors).append(msg + (" (dialogue may change in fiction)" if fiction else ""))

    out_squashed = squash(out)
    for k in keep:
        if squash(normalize(k)) not in out_squashed:
            errors.append(f"kept string missing: {k}")

    h_src, h_out = heading_levels(src), heading_levels(out)
    if h_src != h_out:
        if h_src.count(1) != h_out.count(1):
            warnings.append(f"H1 count changed: {h_src.count(1)} -> {h_out.count(1)}")
        warnings.append(f"heading levels changed: {h_src} -> {h_out}")
    t_src, t_out = table_rows(src), table_rows(out)
    if t_src != t_out:
        warnings.append(f"table rows changed: {t_src} -> {t_out}")

    ratio = change_ratio(src, out)
    w_src, w_out = word_count(prose_only(src)), word_count(prose_only(out))
    length = round(w_out / w_src, 2) if w_src else None
    d_src, d_out = dash_count(src), dash_count(out)

    if src.strip() == out.strip():
        info.append("output is identical to the source")
    if mode == "light" and ratio > light_change_limit:
        warnings.append(f"light edit changed {ratio:.0%} of tokens (limit {light_change_limit:.0%})")
    if length is not None and mode != "light":
        if length < min_length:
            warnings.append(f"output is {length:.0%} of the source's length (below {min_length:.0%}); check for dropped claims")
        elif length > max_length:
            warnings.append(f"output is {length:.0%} of the source's length (above {max_length:.0%}); check for added material")
    if d_out > d_src:
        warnings.append(f"dashes added: {d_src} -> {d_out} (outside code, URLs, and number ranges)")

    metrics = {
        "change_ratio": ratio,
        "length_ratio": length,
        "words_source": w_src,
        "words_output": w_out,
        "dashes_source": d_src,
        "dashes_output": d_out,
        "dashes_per_100_words_output": round(100 * d_out / w_out, 2) if w_out else 0.0,
        "numbers_source": len(set(src_nums)),
        "quotations_source": len(set(quotations(src))),
        "headings_source": len(h_src),
        "headings_output": len(h_out),
    }
    return {"errors": errors, "warnings": warnings, "info": info, "metrics": metrics}


def read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


def format_report(result):
    lines = []
    for label, key in (("ERROR", "errors"), ("WARN", "warnings"), ("INFO", "info")):
        lines += [f"{label}  {m}" for m in result[key]]
    m = result["metrics"]
    lines.append(
        f"changed {m['change_ratio']:.0%} of tokens; length {m['length_ratio']}; "
        f"dashes {m['dashes_source']} -> {m['dashes_output']}; "
        f"{len(result['errors'])} error(s), {len(result['warnings'])} warning(s)")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="Check that a rewrite kept numbers, quotations, code, links, and structure.")
    p.add_argument("source")
    p.add_argument("output")
    p.add_argument("--mode", choices=("rewrite", "light"), default="rewrite",
                   help="light: warn when more than --light-limit of the tokens changed")
    p.add_argument("--fiction", action="store_true", help="report changed dialogue as info, not as an error")
    p.add_argument("--keep", action="append", default=[], metavar="TEXT", help="a string that must survive (repeatable)")
    p.add_argument("--light-limit", type=float, default=0.2)
    p.add_argument("--min-length", type=float, default=0.7)
    p.add_argument("--max-length", type=float, default=1.15)
    p.add_argument("--json", action="store_true", help="print the full result as JSON")
    a = p.parse_args(argv)
    if a.source == "-" and a.output == "-":
        p.error("only one of SOURCE and OUTPUT can be '-'")
    try:
        source, output = read(a.source), read(a.output)
    except OSError as e:
        print(f"preserve_check: {e}", file=sys.stderr)
        return 2
    result = check(source, output, mode=a.mode, fiction=a.fiction, keep=a.keep,
                   light_change_limit=a.light_limit, min_length=a.min_length, max_length=a.max_length)
    print(json.dumps(result, indent=1, ensure_ascii=False) if a.json else format_report(result))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
