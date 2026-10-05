# ProseShape 1.4.2: validation (2026-10-05)

**Result: released, as a small gain.** I tested 1.4.2 once on 16 new held-out texts, with a second judge as a check:
- **Overall.** Under the primary judge it scored **8.02** against 1.4.0's 7.86. The paired difference is **+0.16 [−0.12, +0.48]**: 5 texts better, 5 worse, 6 tied. That interval includes zero, so the overall gain is small and not established by this set alone.
- **Fact problems.** The clearer change is fidelity. The judge flagged 2 fact problems in 1.4.2's output, against 19 for 1.4.0 and 37 for the ordinary-editor prompt.
- **Lead over the editor.** It grew to **+0.58 [+0.19, +1.02]**, from 1.4.0's +0.42 on the same texts.
- **Second judge.** It favored 1.4.2 over 1.4.0 by +0.78 [+0.27, +1.33].

The rule set before the run was: ship if the paired difference against 1.4.0 is above zero under the primary judge, and the second judge agrees in sign. It was met.

**What this set could not show.** The corpus was weighted toward writing a person had already written well, to test whether 1.4.2 stops over-editing it. On it, though, 1.4.0 didn't over-edit either:
- Every arm returned Thoreau, Lincoln and Eisenhower word for word in both runs. Chesterton and the Go blog came back unchanged in seven of eight outputs.
- The four near-clean texts came back nearly unchanged from every arm.

So on human and near-clean text, 1.4.2 and 1.4.0 were level (−0.12 [−0.30, +0.03]). The gain came from AI-shaped text (+0.62 [+0.04, +1.25]). The development corpus did show a gain on human text (+0.48), but the held-out set doesn't confirm it.

**1.4.0 against the ordinary editor, a third time.** On this set 1.4.0 led O by **+0.42 [+0.09, +0.81]** (7 better, 1 worse, 8 tied). Pooled over all three held-out sets (43 texts) the lead is **+0.48 [+0.05, +0.91]**, and the interval now excludes zero:
- On AI-shaped texts (25): +0.76 [+0.16, +1.34].
- On human and near-clean texts (18): +0.10 [−0.51, +0.61]. This is no longer the deficit the 1.4.1 validation reported.

## Method

| Item | Choice |
|---|---|
| Setup | Same harness, request, executor (`claude-sonnet-5-5`), primary judge (`claude-opus-5-5`), rubric v2 and isolation as in [1.4](../v1.4-validation/README.md) and [1.4.1](../v1.4.1-validation/README.md). Five candidates per judgment: U (untouched), O, HS (HumanScope), 1.4.0, and the 1.4.2 candidate. |
| Second judge | `claude-haiku-4-5-20251001`, same rubric and prompt, its own seeded shuffles (round tag `_ho3h`). It was planned as a check on the primary judge, not as an independent family: a judge from another provider wasn't available, and the Fable 5.1 judge had reached its spend limit. |
| Development corpus | 24 texts chosen from the three earlier corpora, weighted toward the gap: 11 human or near-clean texts and 13 AI-shaped ones. O and 1.4.0 outputs were reused from committed runs. |
| Held-out corpus | 16 texts in [`evals/heldout3/`](../heldout3/), committed with `SHA256SUMS` in `458f0e3` before any 1.4.2 edit. Six AI-shaped: talk abstract, real estate listing, museum label, HR policy email, travel itinerary, science fiction scene. Four near-clean human-style: product review, teacher email, stand-up update, memoir. Six human excerpts: Thoreau, Chesterton, Lincoln, Eisenhower, the Kubernetes docs, and the Go blog. O, HS and 1.4.0 outputs were generated while development ran and were not read until validation. |
| Scoring | Per-sample mean over 2 runs × 2 judge passes; bootstrap CIs over samples. |
| Selection | Before round c's results were read, I wrote down the rule for choosing between candidates b and c on development data: c if c − b ≥ 0 on round c. It came out +0.03, so c was validated. |

The held-out texts m01–m10 were written by the agent that edits the skill. m11–m16 are human excerpts and limit that bias.

## What 1.4.2 changed (relative to 1.4.0)

1.4.2 starts from the 1.4.1 candidate (period text, "not just X but Y" asserts both, small words, no invented images) and adds:

- **Patterns are evidence only in clusters.** The model reads the whole draft first. Where several kinds of tell cluster, it rewrites as before. Where the text reads as a person's, a lone contrast, triad, rhetorical question, aphorism or closer is the writer's choice. There the job is the copyedit: fix each sentence where a fault can be named for the reader, and leave the rest. The idea adapts HumanScope's evidence-before-edit rule ([`Anson-Saju-George/HumanScope`](https://github.com/Anson-Saju-George/HumanScope), MIT). The single-sighting rule for A1–A5 now applies only to text that shows model defaults.
- **Lighter contrast fixes.** A contrast whose halves both carry information keeps both claims, usually by dropping only the staging words rather than splitting it into two stiff statements. This replaces 1.4.1's "restate rather than cut".
- **Evaluations and predictions inside hype are claims.** For example, "blazing-fast, lightweight" becomes "fast, lightweight", and "sure to become a family favorite" becomes "likely to become". Pure dressing ("sure to impress") is still not restated.
- **Supported closing generalizations and judgments stay.** In a news story, "sleep plays a vital role…" and "naps deserve a closer look" stay. Only the frame ("one thing is clear") goes.
- **Existing hedges stay.** "Helps you find" is not "finds".
- **Fiction:**
  - every body sensation stays in rewrite mode, even a stock one standing alone, reworded lightly at most and never swapped for an action;
  - fables keep their moral and their read-aloud repetition.
- **Supporting edits:**
  - the light-edit procedure in `mode-guidance.md`;
  - §2, A1 and G1 in `humanizer-rules.md`;
  - the self-review line "your version is close to it: you changed only what you could name a fault in".

## Development rounds (24 texts)

| Round | Candidate | 1.4.0 | O | Candidate − 1.4.0 [95% CI] | Better/worse/tie | Candidate − O | Fact flags: candidate, 1.4.0, O |
|---|---|---|---|---|---|---|---|
| a | 7.93 | 7.66 | 7.39 | +0.27 [−0.22, +0.79] | 8/9/7 | +0.54 [+0.04, +1.11] | 24, 46, 77 |
| b | 8.07 | 7.55 | 7.31 | +0.52 [+0.17, +0.93] | 13/5/6 | +0.76 [+0.26, +1.29] | 15, 52, 87 |
| c | 8.08 | 7.53 | 7.29 | +0.55 [+0.10, +1.01] | 13/4/7 | +0.79 [+0.30, +1.34] | 12, 47, 83 |

Each round fixed what the judge's notes showed in the round before:
- **Round a** added the cluster gate. It edited human text less: the near-clean garden email scored 8.75 against 1.4.0's 4.50, and the children's story 8.50 against 6.50. But it returned some modern human prose word for word, missing a dangling clause in the Python tutorial excerpt. It also dropped evaluations sitting inside hype: "fast, lightweight", "sure to become a staple", "deserves a second look".
- **Round b** turned the gate into "do the copyedit, not pattern removal", and named evaluations, closing judgments and existing hedges as claims. Dropped-fact flags fell from 15 to 8 against candidate a in the same round. It then cut "Her chest tightened." in a fiction scene in all four passes, swapped a lump in the throat for a pause, and reworded the fable's moral.
- **Round c** made body sensations and fable morals explicit. The fiction scene went from 6.00 to 7.75, and the children's story from 6.75 to 8.25.

By group in round c: on human and near-clean texts the candidate led 1.4.0 by +0.48 [−0.09, +1.11] and O by +0.18; on AI-shaped texts, 1.4.0 by +0.62 and O by +1.31. These rounds chose the candidate, so they are not evidence for it. Their differences are about the size that re-judging alone produces (±0.3).

## Held-out results (16 texts, 2 runs, 2 judge passes each)

**Primary judge (Opus 5.5):**

| Arm | Overall [95% CI] | Facts | Meaning | Voice | Natural | Proportion | Format | Mean rank (of 5) |
|---|---|---|---|---|---|---|---|---|
| U untouched | 5.48 [4.12, 6.80] | 5.00 | 5.00 | 3.95 | 3.70 | 2.86 | 5.00 | 3.86 |
| O ordinary editor | 7.44 [7.02, 7.89] | 4.56 | 4.58 | 4.64 | 4.67 | 4.20 | 4.97 | 2.92 |
| HS HumanScope | 7.41 [6.97, 7.86] | 4.55 | 4.52 | 4.66 | 4.70 | 4.19 | 4.98 | 3.12 |
| ProseShape 1.4.0 | 7.86 [7.53, 8.20] | 4.77 | 4.73 | 4.64 | 4.73 | 4.36 | 4.98 | 2.62 |
| **ProseShape 1.4.2** | **8.02** [7.70, 8.31] | 4.95 | 4.92 | 4.75 | 4.67 | 4.48 | 5.00 | 2.47 |

| Paired | Difference [95% CI] | Better/worse/tie |
|---|---|---|
| 1.4.2 − 1.4.0 | +0.16 [−0.12, +0.48] | 5/5/6 |
| 1.4.2 − O | +0.58 [+0.19, +1.02] | 9/2/5 |
| 1.4.2 − HS | +0.61 [+0.20, +1.09] | 8/2/6 |
| 1.4.0 − O | +0.42 [+0.09, +0.81] | 7/1/8 |
| 1.4.0 − O, pooled over three held-out sets (43 texts) | +0.48 [+0.05, +0.91] | 22/9/12 |

| Group | 1.4.2 − 1.4.0 | 1.4.2 − O | 1.4.0 − O |
|---|---|---|---|
| AI-shaped (6) | +0.62 [+0.04, +1.25] | +1.17 [+0.62, +1.71] | +0.54 [+0.08, +1.21] |
| Human and near-clean (10) | −0.12 [−0.30, +0.03] | +0.23 [−0.12, +0.75] | +0.35 [−0.05, +0.90] |

**Judge-flagged issues, all passes (64 judgments per arm):**

| Arm | Added fact | Dropped fact | Changed fact | Total | Over-edit |
|---|---|---|---|---|---|
| O | 9 | 12 | 16 | 37 | 0 |
| HS | 5 | 22 | 3 | 30 | 3 |
| 1.4.0 | 4 | 11 | 4 | 19 | 8 |
| 1.4.2 | 0 | 2 | 0 | 2 | 1 |

**Per text** (primary judge; full table in [`results/summary_ho3.md`](results/summary_ho3.md)):
- **Better than 1.4.0:** talk abstract (9.00 vs 7.25), museum label (8.75 vs 7.50), travel itinerary (8.50 vs 7.50), real estate listing (7.50 vs 7.25), near-clean product review (8.75 vs 8.50).
- **Worse:** teacher email (8.25 vs 9.00), stand-up update (8.50 vs 9.00), HR email (8.00 vs 8.25), science fiction scene (7.75 vs 8.00), memoir (8.75 vs 9.00).
- **Tied:** the six human excerpts. Five came back word for word, or nearly, from every arm, and Kubernetes scored 8.00 for both versions.

**Second judge (Haiku 4.5):**

| Arm | Overall [95% CI] | 1.4.2 minus arm [95% CI] | Better/worse/tie |
|---|---|---|---|
| U | 4.28 [2.89, 5.75] | +2.01 [+0.24, +3.82] | 7/4/5 |
| O | 5.81 [4.80, 6.75] | +0.48 [−0.44, +1.38] | 7/4/5 |
| HS | 5.49 [4.47, 6.48] | +0.80 [−0.31, +1.90] | 7/4/5 |
| 1.4.0 | 5.51 [4.64, 6.27] | +0.78 [+0.27, +1.33] | 8/3/5 |
| 1.4.2 | 6.29 [5.30, 7.20] | | |

Fact flags under the second judge: 1.4.2 had 10, 1.4.0 27, O 36 and HS 22. The two judges agree on the order of the ProseShape versions and on the drop in fact problems. They disagree a good deal on individual texts, in three ways:
- Haiku scores a word-for-word return of the public-domain excerpts very low: Lincoln got 3.00 and Eisenhower 2.25 from every arm, where Opus gave 7.00.
- It docked one near-clean review to 2 out of 10 for changing "every time" to "whenever".
- On this judge 1.4.0 trailed O (−0.30 [−1.08, +0.40]).

Treat it as a robustness check on the version comparison, not as a second measurement of quality.

**What the primary judge's notes show about 1.4.2:**

1. **Stock sensations kept in fiction.** In the science fiction scene, "A chill ran down Rhee's spine, and her heart pounded" survived in both runs (compressed in one), and the judge called it an under-edit. Round c's rule (keep every body sensation, reword lightly at most) protects the author's beats, but here it kept a cliché the corpus expected to be tightened. The next version should say that a stock sensation is reworded, not kept verbatim.
2. **A lone run-up in near-clean text.** The stand-up update kept "Here's the thing:". The cluster gate is working as written. The judge marked it as a small under-edit but still scored the text 8.50.
3. **A few small losses in listings:** "spa-like" dropped from the real estate listing, and some choppy short sentences ("Come see it.").

**Deterministic checks:** `preserve_check.py` found no errors or warnings in any of the four arms' 32 outputs. Mean share of tokens changed: 1.4.2 10%, 1.4.0 11%, HS 9%, O 10%.

## Decision

1.4.2 is released. It met the rule set before the run, and its gain over 1.4.0 has the same sign under both judges and on every development round. What the held-out set supports is narrower than the development rounds suggested, though:
- 1.4.2 is at least as good as 1.4.0 overall, and better on AI-shaped drafts.
- It is much more faithful to the facts.
- It leads the ordinary editor and HumanScope by about 0.6 points.
- Whether it edits human writing better than 1.4.0 is still open, because this set's human texts didn't separate them.

`evals/heldout3/` has now been used, so it becomes development data. A test of the human-writing claim needs human texts that 1.4.0 actually over-edits: modern, plain, and not famous. Recognizable public-domain classics turned out to be the wrong probe, because every arm leaves them alone.

## Limitations

- One model family for executor and both judges, an LLM judge the skill was tuned against, and no human readers.
- The second judge is a smaller model from the same family, not an independent one.
- m01–m10 were written by the agent that edits the skill.
- There are 16 samples, and 6 of them barely discriminated between arms, so the intervals are wide.
- The pooled 1.4.0 − O figure combines three judging rounds whose fifth candidate differed: 1.3.1, the 1.4.1 candidate, and 1.4.2.
- Rewrite mode with one request wording only. Deep rewrite, generation and voice matching were not tested.

## Costs

At list prices as reported by the CLI: generation $8.67 (272 calls, including 96 baseline outputs for the new corpus), judging $20.34 (416 calls, of which 64 were the second judge), total **$29.02**. A spend limit interrupted round c after its generations and before any judging. The run resumed from the saved outputs, and no record was partial.

## Files

- [`results/outputs.jsonl`](results/outputs.jsonl): every generation in this phase not already committed:
  - the three candidates on the development corpus;
  - O, HS, 1.4.0 and 1.4.2 on `heldout3`.
- [`results/judgments.jsonl`](results/judgments.jsonl): the development rounds `_d142a`, `_d142b` and `_d142c`, and the held-out rounds `_ho3` (primary judge) and `_ho3h` (second judge), each for runs `r1` and `r2`.
- Summaries: [`results/summary_dev_a.md`](results/summary_dev_a.md), [`results/summary_dev_b.md`](results/summary_dev_b.md), [`results/summary_dev_c.md`](results/summary_dev_c.md), [`results/summary_ho3.md`](results/summary_ho3.md), [`results/summary_ho3h.md`](results/summary_ho3h.md) and [`results/checks_ho3.md`](results/checks_ho3.md).
- [`results/v142_arm_prompts.json`](results/v142_arm_prompts.json): the three candidates' prompt hashes and commits. PS142c (`1e9eac4c105993ff`, commit `a1d5cee`) is the released skill.

To reproduce without model calls:

```bash
cd evals/harness && python3 seed.py
python3 analyze.py _ho3 PS142c      # identical to results/summary_ho3.md
python3 analyze.py _ho3h PS142c     # identical to results/summary_ho3h.md
python3 build_arm.py PS142c --rev a1d5cee    # 99717 bytes, 1e9eac4c105993ff
```
