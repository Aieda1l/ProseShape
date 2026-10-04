# ProseShape 1.4.1 candidate: validation (2026-10-04)

**Result: not an overall improvement.** I tested the 1.4.1 candidate once on 15 new held-out texts. It scored **7.70**, the same as 1.4.0 (7.70). The paired difference is **+0.00 [−0.48, +0.48]**: 6 texts better, 7 worse, 2 tied. Judge-flagged fact problems fell by half, from 29 for 1.4.0 to 16 (the ordinary editor had 62). The candidate also fixed most of 1.4.0's known issues on the development texts. It read less naturally, though, at 4.45 against 4.67. Development showed the same trade. The candidate is not released. It is preserved at commit `5ada957`.

**A correction to 1.4.0's headline.** This run is also an independent replication of 1.4.0 against the ordinary-editor prompt (O). The result was **+0.27 [−0.78, +1.22]** (8/5/2), much smaller than the +0.83 [+0.19, +1.54] from the first held-out set. Pooled over both sets (27 texts), it is **+0.52 [−0.15, +1.15]**, and that interval includes zero. The split is consistent. On the 10 AI-shaped texts here, ProseShape led O by about +0.6 (both versions). On the 5 human-written and near-clean texts, it trailed O by about −0.4, because the editor prompt leaves good writing alone more often.

## Method

| Item | Choice |
|---|---|
| Setup | Same harness, request, executor (`claude-sonnet-5-5`), judge (`claude-opus-5-5`), rubric v2 and isolation as in [1.4](../v1.4-validation/README.md). Five candidates per judgment: U (untouched), O, HS (HumanScope), 1.4.0, and the 1.4.1 candidate. 1.4.0 took the slot 1.3.1 had held. |
| Development corpus | 25 texts: the 2026-09 corpus (13) and the retired 1.4.0 held-out set (12). O, HS and 1.4.0 outputs were reused from committed runs. |
| Held-out corpus | 15 texts in [`evals/heldout2/`](../heldout2/), committed with `SHA256SUMS` in `80617c2` before any 1.4.1 edit. Ten are AI-shaped across genres not used before: postmortem, fundraising appeal, recipe, job posting, science news with hedges and quotes, book review, wedding toast, children's story, fiction scene, help article. Two are near-clean human-style texts. Three are human excerpts: Austen, Rob Pike's "Errors are values", and Cory Doctorow. O, HS and 1.4.0 outputs were generated while development was still running and were not read until validation. |
| Scoring | Same as 1.4: per-sample mean over 2 runs × 2 judge passes; bootstrap CIs over samples. |

The held-out texts were written by the same agent that edits the skill, after 1.4.0's known issues were known. Several deliberately probe those issues:
- period spelling;
- a lone staged line in near-clean text;
- small words in personal writing;
- a staged contrast in dialogue.

The other ten check for regressions. The three human excerpts limit the authorship bias but do not remove it.

## What the candidate changed (relative to 1.4.0)

- **Period and literary text.** Never modernize spelling, punctuation, quotation marks, hyphenation, or italics. Fix only plain mistakes. Modern plain prose still gets the full copyedit, a scope added in round b.
- **Staged contrasts.** "Not just X but Y" asserts both X and Y. In otherwise clean text, restate a staged line rather than cut it. Round b added: restate it in the fewest plain words, and if the restatement reads stiffer than the line, tighten the line instead. In dialogue, tighten at most.
- **Small words.** Time, degree and manner words stay ("finally", "quietly", "softly"). No new hedges, and no softening of certainty.
- **No invented images** or little scenes in rewrites.
- **Supporting edits:**
  - pass 6 names deleted contrasts and dropped small words as common losses;
  - A1 and D22 (keep supplied quotation marks) were updated in `humanizer-rules.md`, and the light-edit and personal-essay guidance in `mode-guidance.md`;
  - rubric §3's dash line now matches the *weak alone* rule, and the rubric points to `scripts/preserve_check.py`.

## Development rounds (25 texts)

| Round | Candidate | 1.4.0 | O | Candidate − 1.4.0 [95% CI] | Better/worse/tie | Candidate − O | Fact flags, candidate vs 1.4.0 | Naturalness, candidate vs 1.4.0 |
|---|---|---|---|---|---|---|---|---|
| a | 7.97 | 7.86 | 7.24 | +0.11 [−0.24, +0.50] | 9/12/4 | +0.73 [+0.21, +1.28] | 12 vs 41 | 4.38 vs 4.63 |
| b | 7.94 | 7.88 | 7.24 | +0.06 [−0.30, +0.42] | 12/7/6 | +0.70 [+0.17, +1.25] | 15 vs 41 | 4.45 vs 4.67 |

The targeted fixes worked on the samples that showed the 1.4.0 issues (round b, candidate vs 1.4.0):
- Twain: 8.25 vs 7.25. The text now comes back untouched.
- Slack near-clean update: 8.00 vs 5.75. The staged line is now kept and restated.
- Fiction dialogue: 8.50 vs 7.50.
- Explainer contrast: 7.50 vs 6.75.
- Clock-shop story: 8.00 vs 7.50.

By group, the candidate gained on human and near-clean texts (+0.58 overall) and was flat to slightly down on AI-shaped texts (−0.11). Naturalness fell about 0.2 in both groups. Round a also left modern human docs almost untouched (Rust Book excerpt, 6.75 against 7.75), and round b's scoping fixed that (7.50 against 7.50).

Both rounds' overall differences sit inside the ±0.3 that re-judging alone produces. I stopped at round b and chose it as the candidate because its scoping is the more principled of the two, not because it scored higher.

## Held-out results (15 texts, 2 runs, 2 judge passes each)

| Arm | Overall [95% CI] | Facts | Meaning | Voice | Natural | Proportion | Format | Mean rank (of 5) |
|---|---|---|---|---|---|---|---|---|
| U untouched | 4.98 [3.58, 6.38] | 5.00 | 5.00 | 3.65 | 3.33 | 2.50 | 5.00 | 4.12 |
| O ordinary editor | 7.43 [6.73, 8.13] | 4.27 | 4.40 | 4.40 | 4.70 | 4.25 | 4.88 | 2.93 |
| HS HumanScope | 7.68 [7.15, 8.20] | 4.53 | 4.50 | 4.48 | 4.67 | 4.30 | 4.95 | 2.78 |
| ProseShape 1.4.0 | 7.70 [7.10, 8.23] | 4.57 | 4.55 | 4.33 | 4.67 | 4.32 | 4.90 | 2.53 |
| ProseShape 1.4.1 candidate | 7.70 [7.30, 8.08] | 4.77 | 4.70 | 4.33 | 4.45 | 4.42 | 4.93 | 2.63 |

| Paired | Difference [95% CI] | Better/worse/tie |
|---|---|---|
| 1.4.1 − 1.4.0 | +0.00 [−0.48, +0.48] | 6/7/2 |
| 1.4.1 − O | +0.27 [−0.63, +1.08] | 8/7/0 |
| 1.4.1 − HS | +0.02 [−0.60, +0.57] | 7/5/3 |
| 1.4.0 − O | +0.27 [−0.78, +1.22] | 8/5/2 |
| 1.4.0 − O, pooled with the first held-out set (27 texts) | +0.52 [−0.15, +1.15] | 15/8/4 |

**Judge-flagged issues, all passes (60 judgments per arm):**

| Arm | Added fact | Dropped fact | Changed fact | Total | Format damage |
|---|---|---|---|---|---|
| O | 17 | 21 | 24 | 62 | 6 |
| HS | 1 | 19 | 15 | 35 | 1 |
| 1.4.0 | 2 | 23 | 4 | 29 | 6 |
| 1.4.1 candidate | 0 | 14 | 2 | 16 | 4 |

**Per text, candidate against 1.4.0** (full table in [`results/summary_ho2.md`](results/summary_ho2.md)):
- Better on the fiction scene (8.25 vs 7.00), book review (8.50 vs 7.50), job posting (8.00 vs 7.00), children's story (7.50 vs 6.25), near-clean garden email (6.00 vs 5.00) and postmortem (7.75 vs 7.25).
- Worse on the recipe (6.75 vs 8.50), fundraising appeal (7.00 vs 8.75), toast (8.00 vs 8.50), near-clean piano essay (8.50 vs 9.00), Doctorow (8.00 vs 8.75), help article (7.75 vs 8.25) and science news (6.50 vs 6.75).
- Tied on Austen (9.00 each; both versions left it alone) and the Go blog excerpt (8.00 each).

**What the judge's notes show:**

1. **Restatements read clunky.** In the appeal, "she wasn't just looking for groceries — she was looking for hope" became "She came to us for groceries, and she came looking for hope". In the recipe, the dressing "sure to impress" was restated as "tastes good and impresses people". The same thing happened on development (s07, h01). This is the main source of the naturalness loss.
2. **A lone staged contrast in human writing is the writer's line.** In the garden email, "This garden isn't just a few rows of tomatoes, it's the one place on this street where neighbors actually talk to each other" scored 9.00 untouched, and O and HS left it alone. 1.4.0 cut it (5.00). The candidate flattened it to "is a few rows of tomatoes, but it's also…" (6.00). Both versions treat a single "not just X, it's Y" as a tell to act on. In text a person wrote, it should count as *weak alone*.
3. **News takeaways get cut.** Both versions removed the science article's closing paragraph. The judge counted "sleep plays a vital role in healthy aging" as a dropped claim in all four of the candidate's passes. O kept it and scored 8.75.
4. **Read-aloud repetition gets trimmed.** The candidate cut "One by one" and shortened "Then the second ship heard him" in the children's story. The untouched story scored 8.75.

**Deterministic checks:** `preserve_check.py` found no errors or warnings in any of the four arms' 30 outputs. Mean share of tokens changed: candidate 10%, 1.4.0 11%, HS 11%, O 12%.

## Decision and next step

The 1.4.1 candidate is a trade, not an improvement: roughly half the fact problems on both corpora, slightly less natural prose, and the same overall score. It is not released, and 1.4.0 remains the version the plugin ships. The candidate's files are preserved at commit `5ada957`. `python3 evals/harness/build_arm.py PS141b --rev 5ada957` rebuilds its exact prompt (`a573b93257d1122b`).

The held-out notes point to a 1.4.2 that keeps the fidelity gains and removes their cost:

- In otherwise clean, human-written text, treat a lone staged contrast as *weak alone* and leave it.
- In AI-shaped text, carry a contrast's content in lighter wording rather than splitting it into two stiff statements. Never restate pure dressing ("sure to impress").
- Apply the closing-line test to news takeaways. A general claim in plain words stays.
- Keep read-aloud repetition in children's stories.

`evals/heldout2/` has now been used, so it becomes development data. A clean claim for 1.4.2 needs a third corpus, frozen before the edits.

## Limitations

- One model family for executor and judge, an LLM judge the skill was tuned against, and no human readers.
- The held-out texts were written by the agent that edits the skill, and some probe known issues by design.
- There are only 15 samples, so the intervals are wide.
- The pooled 1.4.0 − O figure combines two judging rounds whose fifth candidate differed (1.3.1 in the first, the 1.4.1 candidate in the second). Relative judging can shift scores between rounds.
- Rewrite mode with one request wording only. Deep rewrite, generation and voice matching were not tested.

## Costs

At list prices: generation $6.72 (250 calls, including 90 baseline outputs for the new corpus), judging $13.53 (260 calls), total **$20.25**. One session spend limit interrupted the run. All records were checked, none were partial, and the run resumed where it stopped.

## Files

- [`results/outputs.jsonl`](results/outputs.jsonl): every generation in this phase. That covers both candidates on the development corpus, and O, HS, 1.4.0 and the candidate on `heldout2`.
- [`results/judgments.jsonl`](results/judgments.jsonl): rounds `r1_d141a`, `r2_d141a`, `r1_d141b`, `r2_d141b` (development) and `r1_ho2`, `r2_ho2` (held-out).
- [`results/summary_dev_a.md`](results/summary_dev_a.md), [`results/summary_dev_b.md`](results/summary_dev_b.md), [`results/summary_ho2.md`](results/summary_ho2.md), [`results/checks_ho2.md`](results/checks_ho2.md), [`results/v141_arm_prompts.json`](results/v141_arm_prompts.json) (PS141b, `a573b93257d1122b`, is the committed skill).

To reproduce without model calls: `cd evals/harness && python3 seed.py && python3 analyze.py _ho2 PS141b`.
