<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner.svg" alt="ProseShape: Make prose feel chosen, not defaulted." width="100%">
  </picture>
</p>

ProseShape is an agent skill for writing and rewriting prose while preserving the writer's facts, voice, and intent. It works at two levels: sentence-level patterns that make text feel generic or model-shaped, and narrative-level defaults such as over-explained themes, tidy single-track plots, embodied-emotion repetition, and overly resolved endings.

It is built for readers, not AI detectors. The goal is better, more deliberate prose—not detector evasion.

## What it does

- Rewrites prose without inventing facts, names, numbers, quotations, citations, or personal experiences.
- Matches a supplied writing sample when voice matching matters.
- Handles fiction at both the prose and story-structure level.
- Supports light edits, ordinary rewrites, deep fiction restructuring, and generation from scratch.
- Preserves technical meaning in factual and technical writing.
- Ships with a preservation checker, a frozen held-out corpus, and a reproducible blind-evaluation harness.

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
├── SKILL.md                      # the skill (runtime entry point)
├── references/                   # loaded by the skill as needed
│   ├── humanizer-rules.md
│   ├── storyscope-rules.md
│   ├── mode-guidance.md
│   ├── examples.md
│   ├── evaluation-rubric.md
│   └── prompt-engineering-notes.md   # maintainers only
├── scripts/
│   ├── preserve_check.py         # did a rewrite keep numbers, quotes, code, links, structure?
│   └── tests/
├── evals/
│   ├── eval-log.md               # every tested version and its result
│   ├── trigger-evals.json
│   ├── files/                    # inputs for the 1.0–1.3 evaluations
│   ├── heldout/                  # frozen 12-text corpus for validation (SHA256SUMS)
│   ├── harness/                  # generate, blind-judge, analyze, check
│   └── v1.4-validation/          # method, results, raw outputs and judgments for 1.4.0
├── docs/research/                # competitive analysis and the 2026-09 experiment
├── assets/                       # README banner (light and dark)
├── CHANGELOG.md
├── THIRD_PARTY_NOTICES.md
└── LICENSE
```

Only `SKILL.md` and `references/` are needed at runtime. Raw outputs and judgments for the 1.0–1.3 iterations stayed in the private build workspace. For the 2026-09 comparison and the 1.4 validation they are committed, so every table can be reproduced without a model call.

## Evidence base

ProseShape combines and adapts two main sources:

1. **Humanizer** by Siqi Chen (`blader/humanizer`, MIT), for sentence- and discourse-level patterns, preservation rules, and the idea of editing away generic model defaults.
2. **StoryScope: Investigating idiosyncrasies in AI fiction** by Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, and John Wieting (2026), for research on discourse-level narrative differences in AI and human fiction.

StoryScope paper: https://arxiv.org/abs/2604.03136  
StoryScope code: https://github.com/jenna-russell/storyscope  
Humanizer: https://github.com/blader/humanizer

StoryScope findings are population-level observations, not rules for what human writing must look like. ProseShape uses them to question defaults, not to enforce quotas or manufacture randomness.

## Evaluation

ProseShape is measured against the edit a capable model makes when simply told to edit well. Detector scores are not the benchmark.

**1.4.0 against a strong ordinary-editor prompt.** There were 12 held-out texts, frozen before any 1.4 change: release notes, a cover letter, a support reply, a README, an op-ed, a press release with quotations, a personal essay, fiction dialogue, a grant abstract, and three human-written controls. Every arm got the same request and the same executor model, and a stronger model judged the outputs blind, with the untouched source among the candidates.

| Arm | Overall (1–10) [95% CI] | Fact problems flagged |
|---|---|---|
| **ProseShape 1.4.0** | **8.17** [7.79, 8.54] | 16 |
| Ordinary-editor prompt | 7.33 [6.88, 7.79] | 47 |
| HumanScope | 7.27 [6.58, 7.90] | 29 |
| ProseShape 1.3.1 | 5.94 [5.12, 6.75] | 78 |
| Untouched source | 3.75 [2.81, 4.90] | 0 |

Against the ordinary editor, the paired difference is +0.83 [+0.19, +1.54], better on 7 texts, worse on 3, tied on 2. The executor and the judge are both Claude models, and no human readers were involved. The method, the per-text results, the known issues and the limitations are in [`evals/v1.4-validation/README.md`](evals/v1.4-validation/README.md). The [competitive analysis](docs/research/competitive-analysis-2026-09.md) explains how the ordinary-editor bar was chosen and how 1.3.1 compared with other open-source humanizers.

**Check a rewrite yourself.** `scripts/preserve_check.py` compares a source with its rewrite. It flags changed or missing numbers, quotations, inline and fenced code, links, and frontmatter, and reports heading, table, length and dash changes. It is standard-library Python and is not a quality score.

```bash
python3 scripts/preserve_check.py draft.md revised.md            # add --mode light, --fiction, --keep "text", --json
python3 -m unittest discover -s scripts/tests
```

Versions 1.0–1.3 were developed on 12 cases covering business prose, personal essays, technical writing, fiction rewrites, dialogue, voice matching, citation preservation, deep story restructuring, minimal editing, and generation. See [`evals/eval-log.md`](evals/eval-log.md). Deep rewrite, generation and voice matching have not yet been re-tested under the 1.4 harness.

## License

ProseShape is released under the MIT License. Portions are adapted from `blader/humanizer`, also MIT-licensed; see `THIRD_PARTY_NOTICES.md` for the required notice and research attribution.
