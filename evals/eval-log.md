# Evaluation log

The record of every tested version, kept in the format Boonstra recommends ("document the various prompt attempts"). Raw outputs, blind gradings, benchmarks, and review viewers were retained in the private build workspace and are not included in this public-ready repository. The summarized results and evaluation fixtures are included here.

Iterations 1–4 (versions 1.0–1.3) used the subagent method below. Version 1.4 used a reproducible harness with a frozen held-out corpus; its raw outputs and judgments are committed (see [Version 1.4](#version-14-2026-10-04-blind-comparison-against-an-ordinary-editor)).

## Method

- **Test set:** 12 cases in `evals.json` (kept in the private build workspace and not included here; the input texts it used are in `evals/files/`) covering the requested categories: generic business prose, a personal essay, technical prose, literary fiction, dialogue-heavy fiction, an intentionally linear story, a writer who uses dashes and fragments, text with citations that must not change, a polished but AI-shaped story (deep rewrite), a text that needs almost no edit, plus fiction and nonfiction generation. The test inputs are different from the skill's own examples to avoid testing on training material.
- **Configurations:** `with_skill` (this skill), `without_skill` (same model, no skill, told not to load any skill), `humanizer` (blader/humanizer v3.1.0 SKILL.md only). Later iterations add earlier versions of this skill.
- **Execution:** each run was an independent subagent (claude-opus-5-5) that saved the exact reply it would send.
- **Grading:** one independent grader subagent per eval saw all outputs under shuffled labels (X/Y/Z or W/X/Y/Z), checked the eval's assertions with quoted evidence, scored 15 dimensions from `references/evaluation-rubric.md`, gave an overall 1 to 10, and ranked the outputs. No detector scores were used.
- **Assertions:** 72 across the 12 cases (preservation of named facts, removal of specific tells, genre constraints, no invention). They turned out to be weakly discriminating, so the blind ranking and quality scores carry most of the signal.

## Summary

| Iteration | Versions compared | Evals | Result |
|---|---|---|---|
| 1 | v1.0, no skill, humanizer | 12 | v1.0 first in 8/12; mean quality 7.75 vs 6.92 (no skill) and 6.67 (humanizer); assertions 71/72 vs 64/72 and 67/72 |
| 2 | v1.1, v1.0, no skill, humanizer | 12 | v1.1 first in 6/12 (v1.0 4, no skill 2, humanizer 0); mean quality 8.25 vs 7.83, 6.42, 6.42; v1.1 above v1.0 in 7/12; assertions 72/72 |
| 3 | v1.2, v1.1, no skill | 6 targeted | v1.2 won the deep rewrite (9/10) and LinkedIn; v1.1 won 4; means 7.83 / 8.00 / 6.67 |
| 4 | v1.3, v1.2, v1.1, no skill | same 6 | each skill version first twice; means 7.50 / 7.50 / 8.00 / 6.50; no skill never first |

**Noise estimate:** baseline and earlier-version outputs were reused across iterations and regraded by new graders. The same outputs moved by up to one point per eval and 0.33 on a six-eval mean. Differences smaller than that are not evidence.

**What the evidence supports:** the skill beats both the no-skill baseline and blader/humanizer by about 1 to 1.8 quality points across iterations, and never falls below the baseline on average. v1.0 to v1.1 was a real improvement on the specific failures it targeted. Changes after v1.1 fixed the deep rewrite and the added-events problem, but their effect on mean quality is within noise.

## Per-eval results

### Iteration 1 (v1.0)
| Eval | Blind ranking | Quality (1-10) |
|---|---|---|
| 01 business memo | v1.0 > hmzr > base | v1.0 8, base 7, hmzr 7 |
| 02 personal essay | base > v1.0 > hmzr | v1.0 7, base 8, hmzr 5 |
| 03 technical (git) | v1.0 > hmzr > base | v1.0 8, base 6, hmzr 7 |
| 04 literary, keep events | v1.0 > base > hmzr | v1.0 8, base 7, hmzr 6 |
| 05 dialogue scene | v1.0 > hmzr > base | v1.0 8, base 6, hmzr 7 |
| 06 linear bedtime story | v1.0 > base > hmzr | v1.0 8, base 7, hmzr 6 |
| 07 voice match | v1.0 > base > hmzr | v1.0 8, base 7, hmzr 6 |
| 08 citations | v1.0 > hmzr > base | v1.0 8, base 5, hmzr 7 |
| 09 deep rewrite | base > v1.0 > hmzr | v1.0 8, base 9, hmzr 7 |
| 10 minimal edit | v1.0 > base > hmzr | v1.0 9, base 8, hmzr 6 |
| 11 generate fiction | hmzr > v1.0 > base | v1.0 8, base 7, hmzr 9 |
| 12 generate LinkedIn | hmzr > base > v1.0 | v1.0 5, base 6, hmzr 7 |

### Iteration 2 (v1.1)
| Eval | Blind ranking | Quality (1-10) |
|---|---|---|
| 01 | v1.0 > v1.1 > hmzr > base | v1.1 8, v1.0 8, base 7, hmzr 7 |
| 02 | v1.1 > v1.0 > base > hmzr | v1.1 9, v1.0 8, base 7, hmzr 4 |
| 03 | v1.0 > v1.1 > hmzr > base | v1.1 8, v1.0 8, base 5, hmzr 7 |
| 04 | v1.1 > v1.0 > base > hmzr | v1.1 8, v1.0 8, base 6, hmzr 5 |
| 05 | v1.0 > v1.1 > hmzr > base | v1.1 8, v1.0 9, base 6, hmzr 7 |
| 06 | v1.0 > base > v1.1 > hmzr | v1.1 7, v1.0 8, base 8, hmzr 6 |
| 07 | base > v1.1 > v1.0 > hmzr | v1.1 8, v1.0 7, base 8, hmzr 6 |
| 08 | v1.1 > v1.0 > hmzr > base | v1.1 9, v1.0 9, base 5, hmzr 7 |
| 09 | base > v1.0 > v1.1 > hmzr | v1.1 8, v1.0 8, base 9, hmzr 7 |
| 10 | v1.1 > v1.0 > hmzr > base | v1.1 9, v1.0 8, base 5, hmzr 6 |
| 11 | v1.1 > hmzr > v1.0 > base | v1.1 9, v1.0 7, base 6, hmzr 8 |
| 12 | v1.1 > hmzr > v1.0 > base | v1.1 8, v1.0 6, base 5, hmzr 7 |

### Iteration 3 (v1.2, targeted)
| Eval | Blind ranking | Quality |
|---|---|---|
| 02 | v1.1 > v1.2 > base | v1.2 8, v1.1 8, base 6 |
| 05 | v1.1 > v1.2 > base | v1.2 8, v1.1 9, base 6 |
| 06 | v1.1 > base > v1.2 | v1.2 7, v1.1 8, base 7 |
| 07 | v1.1 > base > v1.2 | v1.2 7, v1.1 8, base 7 |
| 09 | v1.2 > base > v1.1 | v1.2 9, v1.1 7, base 8 |
| 12 | v1.2 > v1.1 > base | v1.2 8, v1.1 8, base 6 |

### Iteration 4 (v1.3, targeted)
| Eval | Blind ranking | Quality |
|---|---|---|
| 02 | v1.2 > v1.1 > v1.3 > base | v1.3 7, v1.2 8, v1.1 8, base 6 |
| 05 | v1.3 > v1.1 > v1.2 > base | v1.3 9, v1.2 7, v1.1 8, base 6 |
| 06 | v1.1 > base > v1.3 > v1.2 | v1.3 7, v1.2 6, v1.1 9, base 8 |
| 07 | v1.1 > v1.2 > v1.3 > base | v1.3 6, v1.2 7, v1.1 8, base 6 |
| 09 | v1.2 > v1.3 > v1.1 > base | v1.3 8, v1.2 9, v1.1 8, base 7 |
| 12 | v1.3 > v1.2 > v1.1 > base | v1.3 8, v1.2 8, v1.1 7, base 6 |

## Failures found and what changed

| Iteration | Observed failure (grader evidence) | Change |
|---|---|---|
| 1 | "Mode: generate." and similar labels opened 9 of 12 replies | Settle the mode privately; mention it only when it changes what the user should expect |
| 1 | Personal essay "bland and thin"; LinkedIn post "flat and clipped," "avoids clichés by saying very little" | New section "Cut, then give it a person": voice is not invention; get more from the facts; keep the anchors; shorter is not automatically better |
| 1 | A generated story ended with a meta note about its research | Generated fiction returns the story alone |
| 1 | A deep rewrite's new plant-and-payoff "clicks shut"; two of three pharmacist stories bookended their openings | New Level 2 "Closure" question and G9 bookend pattern |
| 1 | A generated story was "very muted," its "inner life almost entirely offstage" | Emotion guidance: implication is not coldness (StoryScope: humans use explicit labels 29% vs 8%); Claude's restraint default added |
| 2 | A rewrite added a new event and a running gag to the bedtime story; a staged triple gag in the newsletter | "Voice, not more material": no new events in rewrites; humor-by-formula check (B13) |
| 2 | Deep rewrite "still follows the original's sequence"; baseline's bolder restructure won twice | Deep rewrite reconsiders disclosure order first; invented characters must not be caricatures |
| 3 | v1.2 read as "fairly flat" and "very spare"; the model copied the skill's example sentence "close to crying" verbatim | Rule reframed as "Put the life in the telling, not in new material"; copyable example removed; children's stories keep read-aloud signposts |
| 4 | v1.3 stacked "about six added quips" into a short essay | "A few well-placed lines of voice beat a quip in every sentence" (v1.3.1, not separately evaluated) |

## Why v1.3.1 ships instead of v1.1

v1.1 scored slightly higher on the six-eval subset in iterations 3 and 4 (8.00 vs 7.50), inside the noise band. Part of its liveliness came from adding small events and gags to rewrites the user asked to preserve (flagged, but still additions). The user's brief ranks preservation above style, so v1.3.1 keeps the no-new-events rule and v1.2's deep-rewrite fix, and asks for life through phrasing. Earlier build snapshots remain in the original development archive but are not included in this public-ready repository.

## Limitations of this evaluation

These apply to iterations 1–4. The 1.4 validation has its own limitations section in [`v1.4-validation/README.md`](v1.4-validation/README.md).

- One run per configuration per eval; run-to-run variance is large for creative tasks.
- Graders are the same model family as the executors, so they may share its priors (for example, a preference for "show, don't tell," which StoryScope finds is itself AI-leaning).
- Blinding was partial: output format can hint at the configuration (Humanizer shows a draft, a critique, and a final version).
- Baseline and earlier-version outputs were reused, not regenerated, in iterations 2 to 4.
- Four iteration-2 runs hit an org spend-limit error after writing complete outputs, so their timing is missing.
- No human readers were involved. The review viewers (`iteration-N/review.html`) are there for that.

## Cost

With the skill, runs averaged about 65,000 to 74,000 subagent tokens and 1.5 to 2.5 minutes, versus about 41,000 tokens and 70 seconds without it. Most of the difference comes from reading the reference files. The deep rewrite is the slowest case (9 to 12 minutes).

## Version 1.4 (2026-10-04): blind comparison against an ordinary editor

The [2026-09 comparison](../docs/research/competitive-analysis-2026-09.md) used a different method from the iterations above: isolated `claude -p` sessions, a Sonnet executor, a blind Opus judge that also saw the untouched source, and a strong ordinary-editor prompt (O) as the bar. Under that method 1.3.1 trailed O by −1.27 [−2.00, −0.62]. Version 1.4 was built to close that gap. It used the same method, with one corpus for iteration and a second, frozen one for validation. The full record is in [`v1.4-validation/README.md`](v1.4-validation/README.md).

| Round | Corpus | Candidate − O (overall, 1–10) [95% CI] | Better/worse/tie |
|---|---|---|---|
| PS14a | dev (13) | −0.46 [−1.12, +0.10] | 4/7/2 |
| PS14b | dev | +0.10 [−0.29, +0.54] | 4/6/3 |
| PS14c | dev | −0.08 [−0.62, +0.42] | 5/5/3 |
| PS14d | dev | +0.19 [−0.21, +0.62] | 6/4/3 |
| PS14e | dev | −0.06 [−0.62, +0.48] | 5/5/3 (reverted) |
| PS14f | dev | −0.15 [−0.63, +0.37] | 4/6/3 |
| PS14g | dev | +0.27 [−0.19, +0.73] | 8/3/2 |
| **PS14g = 1.4.0** | **held-out (12)** | **+0.83 [+0.19, +1.54]** | **7/3/2** |

On held-out, 1.4.0 scored 8.17 [7.79, 8.54], O 7.33, HumanScope 7.27, 1.3.1 5.94 and the untouched source 3.75. The judge flagged 16 fact problems for 1.4.0 and 47 for O. Under `scripts/preserve_check.py`, no output from any arm had an error.

**What moved the score:**

- Keeping the claim inside inflated phrasing, with its owner and strength (PS14b). This turned a −0.46 start into parity.
- Keeping fiction beats and the author's details in rewrite mode (PS14d).
- Rewriting whole paragraphs around their point, then checking every claim across (PS14g). This closed the naturalness gap; word-level patching (PS14e) had made it worse.

**What did not move it:** proportional, phrase-level edits (PS14e, reverted). More examples in the closing-line rule helped fidelity but not the overall score (PS14f).

**Failures still open:**

- period spelling and markup modernized in a Twain excerpt;
- a staged line in a near-clean Slack update deleted instead of restated;
- small meaning-bearing words dropped in a personal essay.

They are listed in the validation README as the 1.4.1 starting point.

## Description optimization

- `trigger-evals.json` holds 20 realistic queries: 10 that should trigger (status email, AI-assisted workshop story, voice-sample blog post, cover letter, generated literary story, stiff novel dialogue, LinkedIn post with fixed numbers, dissertation intro with citations, wedding toast, Substack essay) and 10 near-misses that should not (AI-detection request, proofread-only, translation, paper summary, a dash-counting script, changelog conversion, critique-only notes, formality change, SEO product copy, a craft explanation).
- Skill Creator's `run_loop` ran five iterations with a 60/40 train/test split, three runs per query, and claude-opus-5-5. Every candidate description scored 100% precision and 0 to 11% recall, with no difference between candidates.
- The cause is the test environment, not the descriptions. A direct probe showed the nested `claude -p` session answering a "de-AI this cover letter" request itself, without consulting any skill, including the pre-installed humanizer skills. Skill Creator's docs note that Claude consults skills only for tasks it cannot easily handle alone; in this sandbox, writing requests fall below that bar.
- The final description was therefore written by hand. It keeps the original "what and when" framing and adds two ideas from the optimizer's candidates: explicit preference over plain humanizer skills for fiction, structure, voice matching, and generation, and an explicit list of near-misses to skip. Measured once: 10/10 correct rejections, 0/10 triggers (same ceiling).
- To re-run where triggering is measurable (for example, local Claude Code with the skill installed), from the skill-creator directory: `python -m scripts.run_loop --eval-set <path>/evals/trigger-evals.json --skill-path <path>/proseshape --model <model> --max-iterations 5 --verbose`
