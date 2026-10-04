# ProseShape 1.4.0 validation (2026-10-04)

**Result.** On 12 held-out texts written and frozen before any 1.4 change, ProseShape 1.4.0 scored **8.17** [7.79, 8.54] from a blind judge. The strong ordinary-editor prompt (O) scored **7.33**, HumanScope 7.27, and ProseShape 1.3.1 5.94. The paired difference against O is **+0.83 [+0.19, +1.54]**: 1.4.0 was better on 7 samples, worse on 3, and tied on 2. The judge flagged 16 fact problems in 1.4.0's held-out outputs (1 added, 12 dropped, 3 changed) and 47 in O's (8, 22, 17). A deterministic preservation check found no errors in any output.

> **Replication, 2026-10-04.** On a second set of 15 fresh texts ([`evals/heldout2/`](../heldout2/)), 1.4.0's lead over O was +0.27 [−0.78, +1.22] (8 better, 5 worse, 2 tied). Pooled over both held-out sets (27 texts), it was +0.52 [−0.15, +1.15]. ProseShape led O on AI-shaped texts and trailed it on human-written and near-clean ones. Treat the +0.83 below as one sample's result, not as the size of the effect. Details: [`../v1.4.1-validation/README.md`](../v1.4.1-validation/README.md).

This is the experiment behind the 1.4.0 release. It uses the same setup as the [2026-09 comparison](../../docs/research/experiment-2026-09/README.md), where 1.3.1 trailed O by −1.27 [−2.00, −0.62]. Read the limitations before quoting a number: one model family, an LLM judge, and a margin whose lower bound is close to zero.

## Method

| Item | Choice |
|---|---|
| Setup | Identical to 2026-09. Same user request ("Please humanize this so it reads like a person wrote it. Keep the facts and meaning the same."), executor `claude-sonnet-5-5`, judge `claude-opus-5-5`, judge rubric v2 ([`judge_system.txt`](../../docs/research/experiment-2026-09/prompts/judge_system.txt)), O prompt ([`O.txt`](../../docs/research/experiment-2026-09/prompts/O.txt)), and isolated tool-less `claude -p` sessions. Each skill is given inline as a system prompt: `SKILL.md` plus its five runtime references. |
| Dev corpus (iteration only) | The 13 samples of the 2026-09 corpus. Baseline outputs (O, PS 1.3.1, HS) were reused from the 2026-09 runs. Every round judged U, O, PS, HS and the candidate together, blind, with 2 passes per run, so the baselines were re-scored alongside each candidate. |
| Held-out corpus (validation only) | 12 new samples in [`evals/heldout/`](../heldout/): release notes, cover letter, support reply, README, op-ed, press release with quotations, personal essay, fiction dialogue, grant abstract, a Rust Book excerpt, a Mark Twain excerpt (1872), and a near-clean Slack update. They were committed with `SHA256SUMS` in `696dcf0` before the first skill change (`a32e244`) and were not opened during iteration. They were run once, on the final candidate. O, PS 1.3.1, HS and 1.4.0 were all generated fresh (2 runs each) and judged 2 passes per run. |
| Candidates | PS14a–PS14g. Each was frozen once built; sizes and hashes are in [`results/v14_arm_prompts.json`](results/v14_arm_prompts.json). PS14g is byte-identical to the shipped 1.4.0 runtime files (`python3 evals/harness/build_arm.py PS14g --rev a32e244` gives `f8f69d4fa85aeb3c`). |
| Scoring | A sample's score is the mean over 2 runs of the mean over 2 judge passes (overall, 1–10). Confidence intervals come from a percentile bootstrap over samples. Paired differences are taken per sample. |
| Deterministic checks | [`scripts/preserve_check.py`](../../scripts/preserve_check.py) (numbers, quotations, code, links, frontmatter, headings, length) and the 2026-09 checks (protected strings, numbers, em dashes, avoid-ai-writing's `validate.js`). |

## Iteration history (dev corpus)

Same 13 samples, same baseline outputs, re-judged each round. "O" is O's score in that round, which shows how much a fixed set of outputs moves between rounds (7.90 to 8.21).

| Candidate | What changed | Candidate | O | Candidate − O [95% CI] | Better/worse/tie | What the judge's issues showed |
|---|---|---|---|---|---|---|
| PS14a | First 1.4 draft from the [report's roadmap](../../docs/research/competitive-analysis-2026-09.md): "Dressing goes; claims stay"; voice from the writer's own material instead of added attitude; genre rows; dash rule made *weak alone*; rewrite-mode fiction keeps every beat | 7.71 | 8.17 | −0.46 [−1.12, +0.10] | 4/7/2 | Restated claims read clunky; a writer's editorial closer became the city's statement; headings recased; human docs left untouched when a copyedit was wanted |
| PS14b | Claims keep their strength, scope, direction and owner; three kinds of dressing named; changed sentences read aloud; heading case left alone (D21); light edit on human text means a careful copyedit | 8.10 | 8.00 | +0.10 [−0.29, +0.54] | 4/6/3 | Restated aims stiff and clause-heavy; a stilted "They don't only block sound"; "pivotal and hotly debated" softened; fiction sensations replaced with invented actions ("Her chest tightened" became a new gesture) |
| PS14c | Degree that carries information stays; a two-sided contrast becomes two statements; pronoun check; fiction names stock sensations as feelings, with no replacement action | 8.06 | 8.13 | −0.08 [−0.62, +0.42] | 5/5/3 | Fiction still lost the author's details ("rain and old brass") and changed reactions; the human docs sample came back unchanged (scored 5–6); "might seem like magic" and "every single week" cut as tells |
| PS14d | "Remove the tell, not the move"; rewrite-mode fiction keeps the author's sensations and details (reword lightly, merge only repeats), with most StoryScope findings offered in the note; light edit fixes stiff sentences | 8.23 | 8.04 | +0.19 [−0.21, +0.62] | 6/4/3 | Fiction mostly fixed (small words only); stiff phrasing kept ("aligning on next steps"); human docs still barely edited; "represents a step" turned into an aim |
| PS14e | From d: edits in proportion to the tell (word-level tells get word-level fixes) | 8.08 | 8.13 | −0.06 [−0.62, +0.48] | 5/5/3 | Naturalness fell to 4.37 (O 4.81); patched sentences read stitched. **Reverted** |
| PS14f | From d: closing-line test (what does it say once the inflation is gone?); "Beyond the list, fix stiffness"; explainer signposts kept | 8.06 | 8.21 | −0.15 [−0.63, +0.37] | 4/6/3 | Changed facts down to 1, but naturalness still 4.42 (O 4.73): stiff constructions kept, awkward joins, a vague "It" antecedent |
| **PS14g** | From f: pass 4 rewrites each paragraph that has tells as a whole, then checks every claim of the original paragraph against the inventory | **8.17** | 7.90 | **+0.27 [−0.19, +0.73]** | 8/3/2 | Naturalness 4.60 (O 4.71); fewest fact issues of any arm |

No dev round cleared zero. PS14g was chosen for having the best point estimate and win count on dev, and for closing the naturalness gap that pooling b–f had identified (−0.27 against O). It was then run once on the held-out corpus. Nothing was changed after that run.

## Held-out results (12 samples, 2 runs, 2 judge passes each)

| Arm | Overall [95% CI] | Facts | Meaning | Voice | Natural | Proportion | Format | Mean rank (of 5) |
|---|---|---|---|---|---|---|---|---|
| U untouched | 3.75 [2.81, 4.90] | 5.00 | 5.00 | 3.35 | 2.73 | 1.65 | 5.00 | 4.52 |
| O ordinary editor | 7.33 [6.88, 7.79] | 4.27 | 4.35 | 4.44 | 4.56 | 4.19 | 4.98 | 2.52 |
| PS ProseShape 1.3.1 | 5.94 [5.12, 6.75] | 3.60 | 3.58 | 3.90 | 4.44 | 3.15 | 4.50 | 3.75 |
| HS HumanScope | 7.27 [6.58, 7.90] | 4.50 | 4.52 | 4.38 | 4.33 | 4.00 | 5.00 | 2.38 |
| **ProseShape 1.4.0** | **8.17 [7.79, 8.54]** | 4.75 | 4.81 | 4.65 | 4.60 | 4.67 | 4.96 | 1.83 |

| Paired (1.4.0 minus) | Difference [95% CI] | Better/worse/tie |
|---|---|---|
| O | **+0.83 [+0.19, +1.54]** | 7/3/2 |
| HS | +0.90 [+0.06, +1.75] | 9/2/1 |
| PS 1.3.1 | +2.23 [+1.21, +3.25] | 9/1/2 |
| U | +4.42 [+3.00, +5.62] | 11/1/0 |

Per sample (full table in [`results/summary_ho.md`](results/summary_ho.md)), 1.4.0 beat O on the release notes, cover letter, README, op-ed, fiction dialogue (8.25 vs 6.25), grant abstract and Rust excerpt. It lost on the press release (7.50 vs 7.75), the personal essay (7.25 vs 7.75) and the Twain excerpt (7.50 vs 8.50). It tied on the support reply and the Slack update.

**Judge-flagged issues, all passes (48 judgments per arm):**

| Arm | Added fact | Dropped fact | Changed fact | Format damage | Voice loss | Over-edit | Under-edit |
|---|---|---|---|---|---|---|---|
| O | 8 | 22 | 17 | 0 | 1 | 0 | 8 |
| PS 1.3.1 | 12 | 48 | 18 | 14 | 11 | 19 | 0 |
| HS | 5 | 19 | 5 | 0 | 1 | 1 | 13 |
| 1.4.0 | 1 | 12 | 3 | 2 | 3 | 0 | 2 |

**Deterministic checks (24 outputs per arm):**

- `preserve_check.py`: no errors for any arm. Warnings: 1.4.0 0, O 0, HS 3, PS 1.3.1 4. The warnings were an extra heading added to the release notes, and support replies cut to 57–69% of their length. Mean share of tokens changed: 1.4.0 18%, HS 18%, O 19%, PS 1.3.1 30%.
- No arm added or dropped a number.
- avoid-ai-writing's validator reported `heading-count` errors for PS 1.3.1 (release notes, both runs) and HS (one run). It reported none for 1.4.0 or O.
- Every arm made the same dash choices: it removed the lone dash in four nonfiction texts and kept the press release's dash and Twain's three.
- Protected strings that 1.4.0 rephrased, all checked by reading the output:
  - "approximately 300" became "about 300" (O did the same in both runs);
  - "plays a gatekeeper role by refusing" became "acts as a gatekeeper: it refuses";
  - Twain's "*homely*!" became "*homely!*" (see known issues).

## Known issues in 1.4.0

These came out of the held-out run. They were left unpatched so that the shipped version is exactly the one validated. They are the starting list for 1.4.1.

1. **Period text gets copyedited.** In the Twain excerpt, one run modernized "cayote" to "coyote". The other changed `*homely*!` to `*homely!*` and replaced curly quotes with straight ones. The 1.4 rule "give it the copyedit a careful editor would" overrode "unusual phrasing is the voice". Proposed fix: never modernize period spelling, punctuation, quotation marks, or markup.
2. **A staged line in otherwise clean text is cut, not restated.** In both runs on the Slack update, 1.4.0 deleted "We're not just migrating servers here, we're setting the foundation for how the whole team works going forward." All four judge passes counted that as a dropped claim. The same move cut "It's not just land" from a character's dialogue in both fiction runs. Proposed fix: in light edits and in dialogue, restate a not-X-but-Y line plainly ("This also sets how the team works from here on") instead of deleting it.
3. **Small words that carry the writer's meaning go missing in personal writing.** In the essay, "finally decided" lost "finally" and "quietly ashamed" lost "quietly", and one run added an "I think" hedge to the closing line. The fiction runs softened "Sometimes" to "Maybe" and "knew" to "thought".
4. **One invented image.** One support-reply run added "open a box and find the wrong item", a small concrete scene not in the source.
5. **Rubric inconsistency.** `references/evaluation-rubric.md` §3 still says to count dashes "against zero for nonfiction without a sample". That conflicts with the *weak alone* dash rule in `SKILL.md` and `humanizer-rules.md` B8. It was part of the validated prompt, so it stays until 1.4.1.

## Limitations

- **One model family.** The executors and the judge are Claude models. The judge may prefer outputs close to its own defaults.
- **The skill was tuned against this judge.** Seven dev rounds used the same rubric and judge model that scored the held-out run. The held-out corpus guards against overfitting to the samples, not to the judge's taste. No human readers were involved.
- **Small n, and a lower bound near zero.** There are 12 held-out samples. The CI lower bound against O is +0.19, and on dev the same prompt scored +0.27 [−0.19, +0.73]. The honest claim is that 1.4.0 is at least as good as O under this judge, and probably better.
- **Part of the held-out margin is O doing worse.** O scored 7.33 on held-out against 7.90–8.21 on dev, with 17 changed-fact flags. 1.4.0 scored 8.17 on both corpora, so its own level held steady. The gap widened mostly because O lost ground on the new texts.
- **One request, rewrite mode only.** The wording ("keep the facts and meaning the same") favors conservative edits. Deep rewrite, generation and voice matching were not tested here.
- **Text-only judging.** The judge saw only the final text, never the "What changed" notes.
- **Not a detector study.** No detector was used or consulted.

## Costs

At list prices: generation $10.68 (278 calls), judging $19.80 (412 calls), total **$30.48**. One dev iteration costs about $3.60.

## Files

- [`results/outputs.jsonl`](results/outputs.jsonl): every generation in this phase, with the full reply, the extracted text, cost and usage. Dev baselines live in the 2026-09 results.
- [`results/judgments.jsonl`](results/judgments.jsonl): every judgment, with the letter-to-arm key and the parsed scores. Rounds are named `r1_it1`…`r2_it7` (dev) and `r1_ho`, `r2_ho` (held-out).
- [`results/summary_it1.md`](results/summary_it1.md)–[`summary_it7.md`](results/summary_it7.md) and [`summary_ho.md`](results/summary_ho.md): one per round. Each has the per-arm table, paired differences, per-sample scores and issue counts.
- [`results/checks_heldout.json`](results/checks_heldout.json): the 2026-09 deterministic checks on the held-out outputs.
- [`results/v14_arm_prompts.json`](results/v14_arm_prompts.json): size and SHA-256 prefix of each candidate prompt.

To reproduce every table without a model call, run `cd evals/harness && python3 seed.py && python3 analyze.py _ho PS14g`. See [`../harness/README.md`](../harness/README.md).
