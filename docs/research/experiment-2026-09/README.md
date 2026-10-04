# Rewrite comparison experiment (2026-09-30)

Supporting evidence for [`../competitive-analysis-2026-09.md`](../competitive-analysis-2026-09.md). This directory holds everything needed to audit or re-run the comparison: the corpus, the arm prompts (or the script that rebuilds them from pinned commits), the runner, the judge, the deterministic checks, every raw output, and every judgment.

**One-paragraph summary.** Thirteen short texts were rewritten by ProseShape and five competitor skills, plus a bare model and a one-paragraph "strong ordinary editor" prompt, all on the same model with the same user request. Two independent generation runs were made. A different, stronger model judged every output blind against the untouched source. Under this setup (a preservation-oriented request, a fidelity-strict judge, short texts, rewrite mode only), the ordinary-editor prompt scored highest. HumanScope was close behind. ProseShape landed mid-pack: statistically below the ordinary editor and HumanScope, and indistinguishable from Humanizer, keez97, shir-danishyar and avoid-ai-writing. ProseShape was strong on the human controls, the academic paragraph and the explainer. It was weak on marketing, social and fiction, where it cut stated meaning or added unrequested voice. It disclosed those changes in its notes, and the text-only judge could not see the notes. Switching the executor to Opus 5.5 did not change ProseShape's standing, and neither did removing its reference files.

## Design

| Item | Choice |
|---|---|
| Corpus | 13 texts, 92–342 words ([`corpus/`](corpus/), manifest in [`corpus/manifest.json`](corpus/manifest.json)). 10 are deliberately AI-shaped across genres (civic blog, marketing with Markdown and a link, professional email, technical doc with frontmatter, code, table and URL, explainer, academic with citations and a quotation, LinkedIn post, short story, news article with quotes, Spanish paragraph). 3 are controls: a Python Tutorial excerpt (human-written docs, PSF License), a *Three Men in a Boat* excerpt (1889, public domain, heavy dash use), and a human-style email with one chatbot sign-off appended. All names, citations and quotations in the synthetic texts are fictional. None of the texts overlap ProseShape's own fixtures or examples. |
| User request (identical for every arm) | "Please humanize this so it reads like a person wrote it. Keep the facts and meaning the same." Plus a formatting note asking for the final text between `<<<FINAL>>>` / `<<<END>>>` markers, so each skill could keep its own reply format while yielding one comparable artifact. |
| Arms | **U** untouched source (judged, not generated). **B** bare model ("You are Claude, an AI assistant made by Anthropic."). **O** strong ordinary editor ([`prompts/O.txt`](prompts/O.txt), adapted from HumanScope's O arm). **PS** ProseShape v1.3.1 (`SKILL.md` + the five runtime references). **HZ** blader/humanizer 3.1.0. **HS** HumanScope. **AAW** avoid-ai-writing 3.36.0 (`SKILL.md` + required `references/patterns.md`). **SD** shir-danishyar/humanize (`SKILL.md` + patterns + vocabulary). **KZ** keez97/humanizer 2.9.0. Ablations: **PSo** PS on Opus 5.5, **Oo** O on Opus 5.5, **PSc** ProseShape `SKILL.md` only. |
| Why these competitors | Runnable as prompt-only skills, and together they cover the approaches in the report's taxonomy: pattern catalog (HZ, KZ, SD), restraint/evidence-gated editing (HS), editing contract plus verification (AAW). humanizer-stack, lguz, AshwinSathian and the others were analyzed statically only (see the report). |
| Execution | `claude -p` (Claude Code 2.1.285), `--system-prompt-file <arm>`, `--tools ""`, `--disable-slash-commands`, `--strict-mcp-config`, `--setting-sources ""`, `--no-session-persistence`, run from an empty directory. Each call was a fresh, isolated, tool-less session. Skills were given their reference files inline because they cannot open files without tools. Scripts a skill asks to run (validators, scanners) could not run, and the skills were told so. Executor: `claude-sonnet-5-5` (ablations: `claude-opus-5-5`). Two runs (r1, r2) for the main arms; one run for the ablation arms. |
| Judge | `claude-opus-5-5`, isolated, blind: shown the request, the ORIGINAL, and 9 (or 7) candidates in a seeded random order, with the untouched source among them. Rubric: [`prompts/judge_system.txt`](prompts/judge_system.txt) (1–5 on meaning, facts, voice, naturalness, clarity, proportionality, format; overall 1–10; typed issue list; full ranking). "Sounds AI" and detector outcomes are explicitly excluded as criteria. r1 was judged twice with different shuffles (judge reliability); r2 once; the ablation set twice. |
| Deterministic checks | [`scripts/checks.py`](scripts/checks.py): token-level change ratio (difflib), length ratio, numbers added or dropped, literal presence of manifest-protected strings, em-dash counts, shir-danishyar lint density (descriptive only), and avoid-ai-writing's own before/after preservation validator (`detector/validate.js`, run unmodified via [`scripts/validate_wrap.js`](scripts/validate_wrap.js)). |

### Method amendments (disclosed)

1. **Judge rubric v1 → v2 after one pilot judgment.** The v1 rubric counted deleted courtesy boilerplate ("please don't hesitate to reach out") as a "dropped fact". That penalizes exactly what a humanize request asks for and would have favored timid edits. v2 adds one sentence defining facts as informational content. The discarded pilot judgment is kept in `results/judgments.jsonl` (`round: pilot_rubric_v1_discarded`). No outputs were regenerated.
2. **Spend-limit interruption.** The first r1 launch failed on an organization spend limit. All 102 error records were deleted before the relaunch; no partial outputs were used. The two pilot outputs (PS and HZ on s01) predate the interruption and were kept.
3. **Manifest fix.** One s10 protected string came from a paragraph not included in the excerpt. It was replaced before any analysis.
4. **Ablation arms added after seeing the main results.** They were added to test two explanations for the gap with ProseShape's own evaluation (executor model; reference files). They are exploratory, not pre-registered.

## Results

Full tables: [`results/summary_combined.md`](results/summary_combined.md) (main), [`results/summary_ablation.md`](results/summary_ablation.md) (ablations), [`results/summary_judge.md`](results/summary_judge.md) (per judge pass), [`results/scanner_controls.md`](results/scanner_controls.md) (competitor scanners on the unedited corpus).

**Blind-judge overall score (1–10), all 13 samples, per-sample mean of run 1 (2 judge passes) and run 2 (1 pass), bootstrap 95% CI over samples:**

| Arm | Overall | Facts (1–5) | Voice (1–5) | Proportionality (1–5) | Mean rank (of 9) |
|---|---|---|---|---|---|
| O ordinary editor | **7.96** [7.48, 8.48] | 4.56 | 4.71 | 4.50 | 3.12 |
| HS HumanScope | 7.48 [6.69, 8.19] | 4.60 | 4.60 | 4.29 | 4.02 |
| B bare model | 7.37 [6.79, 7.88] | 4.37 | 4.19 | 4.12 | 4.27 |
| AAW avoid-ai-writing | 7.08 [6.25, 7.87] | 4.75 | 4.38 | 3.83 | 4.35 |
| SD shir-danishyar | 6.96 [6.17, 7.75] | 4.29 | 4.21 | 3.96 | 4.92 |
| KZ keez97 | 6.94 [6.35, 7.62] | 4.13 | 4.25 | 3.83 | 5.29 |
| HZ blader/humanizer | 6.71 [6.04, 7.46] | 4.17 | 4.19 | 3.71 | 5.63 |
| **PS ProseShape** | 6.69 [5.71, 7.62] | 4.15 | 4.23 | 3.77 | 4.92 |
| U untouched | 3.10 [2.37, 4.04] | 5.00 | 3.08 | 1.46 | 8.48 |

**Paired differences, ProseShape minus comparator (overall, 13 samples):** vs O −1.27 [−2.00, −0.62] (PS better on 1 sample, worse on 10); vs HS −0.79 [−1.56, −0.02]; vs HZ −0.02 [−0.75, +0.65]; vs B −0.67 [−1.63, +0.35] (AI-shaped samples only: −1.35 [−2.15, −0.50]; controls: +1.58); vs U +3.60.

**Ablations (separate blind round, run-1 outputs):** PS on Opus minus PS on Sonnet −0.04 [−0.85, +0.81]. PS full bundle minus `SKILL.md`-only +0.04 [−0.62, +0.65], at 2.8× the generation cost ($0.75 vs $0.27 per 13 samples). PS on Opus minus O on Opus −0.46 [−1.38, +0.42].

**Deterministic checks (26 outputs per arm):**
- No arm added or dropped a number in any main-run output. PS on Opus added two derived numbers in s01 (a worked price example) and disclosed them.
- On the three controls, every skill changed 3–10% of tokens. The bare model changed 27%.
- avoid-ai-writing's validator raised errors only for HZ (2) and SD (3), all `heading-count`. Three (HZ ×2, SD ×1, on s04) deleted the H1 that duplicated the frontmatter title, a rule-driven change (Humanizer §20) that loses no content. Two (SD, s02, both runs) deleted the marketing page's only heading. That follows SD's "no headings at all under ~400 words" rule, but it is a structural deletion the genre does not call for.

**Judge-flagged issues over 39 sample-judgments:** PS 27 dropped / 6 added / 8 changed facts; HZ 29 / 0 / 6; KZ 23 / 4 / 11; SD 22 / 0 / 6; HS 13 / 0 / 4; O 8 / 5 / 6; AAW 8 / 0 / 0 (plus 20 "under-edit").

**Reliability:** judge pass 1 vs pass 2 on the same r1 outputs: mean Spearman rank correlation 0.71 (range −0.17 to 0.95; the low values are on controls where several candidates were near-identical), mean |Δ overall| 0.57 points. Run 1 vs run 2 for the same arm: mean per-sample |Δ overall| 0.69–1.12 points. Treat differences under about 0.6 points on the 13-sample mean as noise.

### Manual review of flagged cases

Every deterministic flag was checked by reading the output:

- **Checker false positives:** PS s02 "14-day" appears as "free for 14 days"; B s05 "passive seal" as "ear cushions sealing out sound passively"; B s07 and B s08 are paraphrases with the same content. Literal string matching over-reports loss.
- **Real losses or changes:** B s12 dropped "dentist" (the reason for the constraint). B s11 rewrote about a third of Jerome K. Jerome's text, including the dialogue punctuation. HZ, KZ and SD changed "Hire for curiosity, not credentials" in **6 of 6** outputs across both runs (to "before credentials", "over credentials", "Hire for curiosity. Credentials matter less."): a not-X-but-Y rule firing on a contrast whose two halves both carry meaning. PS, HS, AAW, O and B kept it in 10 of 10.
- **ProseShape-specific, replicated in both runs:**
  - It removed the one em dash from the human-written Python Tutorial, its only edit there, following its no-dash rule for nonfiction without a sample.
  - It cut the story's stated realization and grief line (s08) and kept, and flagged, the "Years later" coda.
  - It added unrequested voice lines ("I still can't say that without grinning", s07), and every one was disclosed in its "What changed" note as removable.
  - On Opus it added a derived worked example and a value judgment (s01), both disclosed.
- **HZ on the Python Tutorial:** it converted curly quotes to straight in 7–10 sentences per run (Humanizer §21, marked *weak alone*).

## Limitations (read before citing any number)

- **One model family.** All executors and the judge are Claude models (Sonnet 5.5 and Opus 5.5). The judge may prefer outputs close to its own defaults. The O prompt and the judge rubric both emphasize preservation, which is a real alignment between that arm and the scoring.
- **One request wording, rewrite mode only.** The request says "keep the facts and meaning the same", which favors conservative arms. ProseShape's distinctive capabilities (fiction deep rewrite with permission, generation from scratch, voice matching from a sample) were **not tested**. Its own development evaluation covered those.
- **Short texts, small n.** 13 samples, 92–342 words; 1–2 generations per arm and sample; bootstrap CIs are over samples only. Long documents were not tested.
- **Text-only judging.** Judges saw only the final text. ProseShape's disclosure behavior (flagging additions, cuts and missing facts in its note), which is useful to an author, earned no credit. This favors arms that are silently conservative.
- **Skills without their scripts.** AAW, KZ and SD were designed to call validators or scanners; in this tool-less setup they could not.
- **No human raters.** Nothing here measures what human readers prefer. The judge is a proxy.
- **Not a detector study.** No detector was used or consulted.

## Reproducing

```bash
# 1. Clone competitors at the pinned commits listed in scripts/build_arms.py into ../comp (or set COMP_DIR)
# 2. Rebuild the arm prompts (hashes should match prompts/arms_meta.json)
python3 scripts/build_arms.py
# 3. Generate (each call is an isolated `claude -p` session; ~$11 total at list prices for everything here)
python3 scripts/run_arm.py PS s01_ai_blog 1
# 4. Judge one sample (writes judgments/r1/p1/<sample>.json)
python3 scripts/judge.py s01_ai_blog r1 1
# Or regenerate the tables from the committed results without any model calls:
python3 scripts/unpack_results.py && python3 scripts/combined.py && COMP_DIR=... python3 scripts/ablation.py
```

Costs at list prices: generation $6.68 (247 calls), judging $4.60 (66 calls incl. one discarded pilot), total **$11.26**.

Attribution: s10 is an excerpt of the Python Tutorial, "Whetting Your Appetite", © Python Software Foundation, used under the PSF License. s11 is from Jerome K. Jerome, *Three Men in a Boat* (1889), public domain (Project Gutenberg #308). avoid-ai-writing's validator is MIT-licensed and is invoked from a local clone, not redistributed.
