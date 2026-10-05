# Design notes (for maintainers)

How the skill's design follows from its sources, and a log format for future iterations. The runtime skill does not need this file.

## Contents

1. Prompt-engineering principles applied
2. Where the three sources disagree, and what won
3. Iteration log

---

## 1. Prompt-engineering principles applied

From Lee Boonstra, *Prompt Engineering* (Google, February 2025), cross-checked against Anthropic's Agent Skills authoring guidance (SKILL.md under 500 lines, references one level deep, a contents list in long reference files, concrete examples over abstract description).

| Principle (page) | How the skill uses it |
|---|---|
| System, contextual, and role prompts serve different purposes (pp.18–24) | SKILL.md holds persistent behavior. Per-task context lives in named variables (`{mode}`, `{genre}`, `{reader}`, `{sample}`, `{permissions}`, `{must_keep}`) in `mode-guidance.md`. No role-play persona is needed; the purpose statement does that work. |
| Design with simplicity; use action verbs (p.55) | Imperative, one idea per line; reasons given briefly instead of stacked MUSTs. |
| Be specific about the output (p.56) | A return format per mode. |
| Prefer instructions to constraints (pp.56–57) | Level 2 is written as questions and moves, not bans. Hard constraints are kept only where the paper says constraints belong: safety and strict requirements (here, preservation and integrity). Word lists are marked weak evidence. |
| Provide examples; 3–5 or more; diverse; include edge cases (pp.15–17, 54) | Eleven examples across genres, including four where the right action is restraint. |
| Mix up the classes in few-shot examples (p.59) | Examples alternate heavy rewrite, structural rewrite, and minimal edit so the model does not learn "always rewrite heavily". |
| Step-back prompting (pp.25–28) | Generation begins by naming the default version, then choosing with or against it. |
| Tree of thoughts / self-consistency (pp.32–37) | Two or three alternative shapes are sketched before a fiction draft. |
| Chain of thought; answer after reasoning (pp.29–31, 64) | Planning and diagnosis stay private; the reply is the text plus a short note. |
| Use variables (p.58) | See the variables table in `mode-guidance.md`. |
| Document attempts; iterate; adapt to model updates (pp.60, 64–65) | The log below. StoryScope's fingerprints are dated to the tested model versions and should be re-checked when models change. |

The whitepaper's sampling advice (temperature, top-K, top-P) does not apply: a skill cannot set sampling parameters.

## 2. Where the sources disagree, and what won

| Conflict | Resolution | Reason |
|---|---|---|
| Humanizer bans all dashes without a sample; fiction uses dashes for interrupted speech | Keep interruption dashes in fiction; ban connective dashes in nonfiction without a sample | Genre convention ranks above generic pattern rules |
| Humanizer: "Fiction is exempt [from the no-invention rule] because invented detail is the task" | Invention allowed in generate and deep-rewrite; small flagged details allowed in rewrite; plot facts preserved | A rewrite belongs to the user's story |
| Humanizer: "Vary sentence length; real writing alternates short and long" | Length follows content; alternation by rule is a tell | Rhythm by rule is Humanizer's own category |
| Craft advice ("show, don't tell"; "the protagonist drives the climax") vs StoryScope (both AI-elevated) | Treat workshop rules as possible model priors; choose per beat | StoryScope Table 16 |
| StoryScope human-side features vs other models' fingerprints | Never add a device to look human | StoryScope Table 17 |
| Detection vs quality | Optimize for readers | StoryScope measures separability only; Humanizer states detector evasion is a non-goal |

## 3. Iteration log

Use one row per tested version (Boonstra's Table 21 template, adapted).

| Version | Date | Goal | Model | Change | Eval result | Notes |
|---|---|---|---|---|---|---|
| 1.0.0 | 2026-09-29 | First draft from the rulebook | claude-opus-5-5 | Initial SKILL.md and six references | Blind 3-way, 12 evals: ranked first 8/12, mean rank 1.42, assertions 71/72 | Losses: thin, under-voiced essay; flat LinkedIn post; meta note after a generated story; a deep rewrite whose new plant-and-payoff "clicks shut". Mode label leaked in 9/12 replies. |
| 1.1.0 | 2026-09-29 | Fix iteration-1 failures | claude-opus-5-5 | Stop announcing the mode; no notes around generated fiction; new "Cut, then give it a person" section (voice is not invention; keep anchors); emotion guidance warns against coldness; new closure question and G9 bookend pattern; shorter change notes; example 2 rewritten to add attitude | Blind 4-way, 12 evals: first 6/12, mean rank 1.67 of 4, quality 8.25 (v1.0: 7.83); above v1.0 in 7/12; assertions 72/72 | Fixed essay, generated story, LinkedIn post, mode leak. New over-correction: added events and a staged gag in rewrites; deep rewrite still too close to original order. |
| 1.2.0 | 2026-09-29 | Balance the voice fix | claude-opus-5-5 | "Voice, not more material" (no new events in rewrites, however small); keep real points under hype; humor-by-formula check (B13); plain feeling means plain; deep rewrite reconsiders disclosure order first; no caricatured invented characters | Targeted blind 3-way on 6 evals vs v1.1 and baseline: first 2/6 (v1.1 4/6); mean 7.83 vs v1.1 8.00 | Deep rewrite fixed (eval-09 first, 9/10). Restraint over-applied: flat bedtime story, weak humor, spare essay. The model copied the example sentence "She was close to crying" verbatim. |
| 1.3.0 | 2026-09-29 | Keep v1.2's structure fix, restore v1.1's liveliness | claude-opus-5-5 | "Put the life in the telling, not in new material" replaces the restraint rule; removed the copyable example sentence; children's genre keeps signposts and read-aloud repetition | Blind 4-way on 6 evals (v1.3, v1.2, v1.1, baseline): v1.3 7.50, v1.2 7.50, v1.1 8.00, baseline 6.50; each skill version first 2/6 | Differences among skill versions are within grader and run noise (regrading identical v1.2 outputs moved their mean 0.33). Baseline last or near last on every eval. |
| 1.3.1 | 2026-09-29 | Wording clarification | claude-opus-5-5 | "A few well-placed lines of voice beat a quip in every sentence" (addresses stacked quips seen in iterations 2 and 4) | Not separately evaluated | Shipped version. Description rewritten by hand after `run_loop` could not discriminate candidates (nested sessions consulted no skills for writing tasks); see `evals/eval-log.md`. |
| 1.3.1 (re-tested) | 2026-09-30 | Independent comparison | claude-sonnet-5-5 executor, claude-opus-5-5 judge | None (competitive analysis) | Blind 9-way on 13 texts: 6.69 vs O (ordinary editor) 7.96, paired −1.27 [−2.00, −0.62] | Cut stated meaning (realizations, aims, characterizations) and added unrequested voice in rewrites; strong on human controls. See `docs/research/competitive-analysis-2026-09.md`. |
| 1.4.0-a | 2026-09-30 | Beat O without trading preservation | same | "Dressing goes; claims stay"; no added attitude in rewrites; genre rows; dash rule *weak alone*; fiction beats kept | Dev 13: −0.46 [−1.12, +0.10] vs O | Clunky restatements, misattributed closers, headings recased, human docs left untouched. |
| 1.4.0-b | 2026-09-30 | Fix a | same | Claim strength, scope, direction and owner; three kinds of dressing; read changed sentences aloud; heading case is house style; light edit = careful copyedit | Dev: +0.10 [−0.29, +0.54] | Stiff restated aims; fiction sensations replaced with invented actions. |
| 1.4.0-c | 2026-09-30 | Fix b | same | Degree words stay; two-sided contrasts become two statements; pronoun check; fiction names sensations as feelings | Dev: −0.08 [−0.62, +0.42] | Fiction still lost author details; human docs returned unchanged. |
| 1.4.0-d | 2026-09-30 | Fix c | same | "Remove the tell, not the move"; rewrite-mode fiction keeps the author's sensations and details; StoryScope findings go in the note | Dev: +0.19 [−0.21, +0.62] | Stiffness kept ("aligning on next steps"). |
| 1.4.0-e | 2026-09-30 | Raise naturalness | same | From d: word-level tells get word-level fixes | Dev: −0.06 [−0.62, +0.48] | Naturalness fell (4.37 vs O 4.81); patched sentences read stitched. Reverted. |
| 1.4.0-f | 2026-10-04 | Raise naturalness | same | From d: closing-line test; "Beyond the list, fix stiffness"; explainer signposts kept | Dev: −0.15 [−0.63, +0.37] | Fewer changed facts; naturalness still behind O. |
| 1.4.0 (g) | 2026-10-04 | Raise naturalness | same | From f: rewrite each paragraph with tells as a whole, then check every claim across | Dev: +0.27 [−0.19, +0.73]. **Held-out 12: 8.17 vs O 7.33, +0.83 [+0.19, +1.54]**; vs 1.3.1 +2.23 | Shipped. Open: period spelling modernized (Twain), staged line cut instead of restated, small words dropped in an essay. See `evals/v1.4-validation/README.md`. |
| 1.4.1-a | 2026-10-04 | Fix the 1.4.0 known issues | claude-sonnet-5-5 executor, claude-opus-5-5 judge | Period text untouched; "not just X but Y" asserts both, restate rather than cut in clean text; keep meaning-bearing small words, no new hedges; no invented images; rubric dash line aligned | Dev 25: +0.11 [−0.24, +0.50] vs 1.4.0; +0.73 vs O; fact flags 12 vs 41 | Known-issue samples fixed (Twain, Slack, fiction dialogue). Naturalness −0.25; modern human docs under-edited. |
| 1.4.1-b | 2026-10-04 | Recover naturalness | same | From a: copyedit scope limited to period/literary text; restate in the fewest words, tighten the line instead if stiffer | Dev: +0.06 [−0.30, +0.42]. **Held-out 2 (15): 7.70 vs 1.4.0 7.70, +0.00 [−0.48, +0.48]**; fact flags 16 vs 29 | Not released. Restatements read clunky; a lone staged contrast in human text should be left alone. 1.4.0 vs O replicated at only +0.27 on the new set. See `evals/v1.4.1-validation/README.md`. |
| 1.4.2-a | 2026-10-05 | Stop over-editing human writing | claude-sonnet-5-5 executor, claude-opus-5-5 judge | From 1.4.1-b: patterns are evidence only in clusters (HumanScope's evidence-before-edit idea); a lone staged line in a person's text is left; lighter contrast fixes; supported news takeaways stay; fable repetition kept | Dev 24: +0.27 [−0.22, +0.79] vs 1.4.0; +0.54 vs O; fact flags 24 vs 46 | Near-clean garden email 8.75 vs 4.50. Returned some modern human prose verbatim; dropped evaluations inside hype ("fast, lightweight", "sure to become a staple"). |
| 1.4.2-b | 2026-10-05 | Fix a | same | Human text gets the copyedit, not nothing; evaluations, predictions, closing judgments and existing hedges are claims | Dev: +0.52 [+0.17, +0.93]; fact flags 15 vs 52 | Cut a stand-alone body sensation in all passes, swapped one for a pause, reworded a fable's moral. |
| 1.4.2 (c) | 2026-10-05 | Fix b | same | Every body sensation stays in rewrite mode; fables keep their moral; stories may need nothing | Dev: +0.55 [+0.10, +1.01]. **Held-out 3 (16): 8.02 vs 1.4.0 7.86, +0.16 [−0.12, +0.48]**; vs O +0.58; fact flags 2 vs 19; second judge (Haiku 4.5) +0.78 [+0.27, +1.33] | Shipped. Gain on AI-shaped text; human excerpts were left untouched by every arm, so the human-writing claim is untested. Open: stock sensations now survive verbatim. See `evals/v1.4.2-validation/README.md`. |
