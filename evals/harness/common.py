"""Shared paths and settings for the evaluation harness."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.environ.get("PROSESHAPE_WORK", os.path.join(HERE, "work"))
EXPERIMENT = os.path.join(REPO, "docs", "research", "experiment-2026-09")
PROMPTS = os.path.join(EXPERIMENT, "prompts")

# The request every arm receives. Changing it makes results incomparable with the committed ones.
REQUEST = "Please humanize this so it reads like a person wrote it. Keep the facts and meaning the same."
FORMAT_NOTE = ("(Formatting note for this session: after anything else you want to say, put the final version of the text, "
               "and nothing else, between a line containing only <<<FINAL>>> and a line containing only <<<END>>>.)")

EXECUTOR = os.environ.get("PROSESHAPE_EXECUTOR", "claude-sonnet-5-5")
JUDGE = os.environ.get("PROSESHAPE_JUDGE", "claude-opus-5-5")

# Isolated, tool-less, settings-free `claude -p` session.
CLAUDE_FLAGS = ["--tools", "", "--strict-mcp-config", "--disable-slash-commands", "--setting-sources", "",
                "--no-session-persistence", "--output-format", "json"]


def path(*parts):
    return os.path.join(WORK, *parts)


def sandbox():
    p = path("sandbox")
    os.makedirs(p, exist_ok=True)
    return p


def stopped():
    return os.path.exists(path("STOP"))


def stop(reason):
    os.makedirs(WORK, exist_ok=True)
    with open(path("STOP"), "w", encoding="utf-8") as f:
        f.write(reason[:500])


def corpus_dir(name):
    """Accept a path, or the short names 'dev', 'heldout' (1.4.0), 'heldout2' (1.4.1) and 'heldout3' (1.4.2)."""
    short = {"heldout": os.path.join(REPO, "evals", "heldout"), "heldout2": os.path.join(REPO, "evals", "heldout2"),
             "heldout3": os.path.join(REPO, "evals", "heldout3"), "dev": os.path.join(EXPERIMENT, "corpus")}
    return os.path.abspath(short.get(name, name))


def read_sample(corpus, sample):
    with open(os.path.join(corpus_dir(corpus), f"{sample}.md"), encoding="utf-8") as f:
        return f.read().rstrip("\n")
