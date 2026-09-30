# ProseShape

**Make prose feel chosen, not defaulted.**

ProseShape is an agent skill for writing and rewriting prose while preserving the writer's facts, voice, and intent. It works at two levels: sentence-level patterns that make text feel generic or model-shaped, and narrative-level defaults such as over-explained themes, tidy single-track plots, embodied-emotion repetition, and overly resolved endings.

It is built for readers, not AI detectors. The goal is better, more deliberate prose—not detector evasion.

## What it does

- Rewrites prose without inventing facts, names, numbers, quotations, citations, or personal experiences.
- Matches a supplied writing sample when voice matching matters.
- Handles fiction at both the prose and story-structure level.
- Supports light edits, ordinary rewrites, deep fiction restructuring, and generation from scratch.
- Preserves technical meaning in factual and technical writing.
- Uses an evaluation suite with preservation checks and blind comparisons.

## Why ProseShape

Most "humanizer" tools focus on surface wording. ProseShape combines that layer with research on narrative structure. The result is a writing skill that asks not only *which words sound generic?* but also *which choices in the piece were inherited from a model's defaults?*

The core principle is simple: a language model tends toward choices that work for many possible readers and situations; a writer chooses for this reader, this situation, and this piece.

## Install

### Claude Code

Clone the repository into your skills directory:

```bash
git clone https://github.com/Aieda1l/ProseShape.git ~/.claude/skills/proseshape
```

Then invoke it with:

```text
/proseshape
```

You can also place the repository under `.claude/skills/proseshape` for a project-local installation.

### Other Agent Skills-compatible tools

The runtime entry point is `SKILL.md`, with supporting guidance in `references/`. Copy the repository into the skill directory expected by your agent.

## Example prompts

```text
Humanize this story. Same events, same ending. [paste]
```

```text
The prose is fine but this story feels AI-shaped. Free rein to restructure; keep the characters and premise. [paste]
```

```text
Here are two things I wrote: [samples]. Rewrite this draft so it sounds like me: [draft]
```

```text
Light polish only. Keep every fact and citation exactly as-is. [paste]
```

```text
Write a 1,200-word story about a hospice night nurse. No stated moral, no years-later ending.
```

## Repository layout

```text
.
├── SKILL.md
├── references/
│   ├── humanizer-rules.md
│   ├── storyscope-rules.md
│   ├── mode-guidance.md
│   ├── examples.md
│   ├── evaluation-rubric.md
│   └── prompt-engineering-notes.md
├── evals/
│   ├── evals.json
│   ├── trigger-evals.json
│   ├── eval-log.md
│   └── files/
├── docs/
│   ├── BUILD_REPORT.md
│   └── rulebook.md
├── THIRD_PARTY_NOTICES.md
└── LICENSE
```

The large raw evaluation workspace from development is intentionally omitted from this public-ready tree. The evaluation definitions, fixtures, methodology, and summarized results remain in `evals/` and `docs/`.

## Evidence base

ProseShape combines and adapts two main sources:

1. **Humanizer** by Siqi Chen (`blader/humanizer`, MIT), for sentence- and discourse-level patterns, preservation rules, and the idea of editing away generic model defaults.
2. **StoryScope: Investigating idiosyncrasies in AI fiction** by Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, and John Wieting (2026), for research on discourse-level narrative differences in AI and human fiction.

StoryScope paper: https://arxiv.org/abs/2604.03136  
StoryScope code: https://github.com/jenna-russell/storyscope  
Humanizer: https://github.com/blader/humanizer

StoryScope findings are population-level observations, not rules for what human writing must look like. ProseShape uses them to question defaults, not to enforce quotas or manufacture randomness.

## Evaluation

The development process used 12 evaluation cases covering business prose, personal essays, technical writing, fiction rewrites, dialogue, voice matching, citation preservation, deep story restructuring, minimal editing, and generation. See `evals/eval-log.md` and `docs/BUILD_REPORT.md` for methodology and results.

## License

ProseShape is released under the MIT License. Portions are adapted from `blader/humanizer`, also MIT-licensed; see `THIRD_PARTY_NOTICES.md` for the required notice and research attribution.
