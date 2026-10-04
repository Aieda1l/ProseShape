# ProseShape competitive analysis: open-source humanizers and AI-prose editors

**Date checked:** 2026-09-30  
**ProseShape version examined:** v1.3.1, commit [`57d58e4`](https://github.com/Aieda1l/ProseShape/tree/57d58e4f860c95b29a028c157a33dde07de09021)  
**Scope:** 14 competitor repositories (7 named in the brief, 7 found by search), static source analysis of each, plus an executed, blinded rewrite comparison of ProseShape against five runnable competitors and two baselines ([`experiment-2026-09/`](experiment-2026-09/README.md)).  
**No ProseShape code or prompts were changed for this report.**

> **Update, 2026-10-04.** ProseShape 1.4.0 implements several of the recommendations below. On a held-out corpus frozen before any change, it scored 8.17 against the ordinary-editor prompt's 7.33 (paired +0.83 [+0.19, +1.54]). A second fresh set gave +0.27 [−0.78, +1.22], so the pooled lead is +0.52 [−0.15, +1.15]. See the [addendum](#addendum-2026-10-04-status-after-proseshape-140). The body of this report is unchanged and describes v1.3.1.

Evidence labels used throughout:

- **OBSERVED**: directly supported by a cited file, test, document or experimental result.
- **INFERRED**: a reasoned conclusion from observed evidence.
- **RECOMMENDED**: a proposed change for ProseShape.

ProseShape files are cited as `path:line`. Competitor files are cited with commit-pinned GitHub permalinks. Author claims are marked as claims; independent checks I ran are marked as such.

---

## 1. Executive summary

1. **ProseShape is a prompt-only Agent Skill, and a carefully reasoned one.** It is `SKILL.md` plus six Markdown references, with no code, scripts or tests beyond trigger fixtures (OBSERVED; see §5.0). Its distinctive design:
   - two editing levels: Humanizer's surface patterns plus StoryScope's narrative defaults (`SKILL.md:14-26`);
   - an explicit rule-priority ladder (`SKILL.md:28-38`) and six modes (`SKILL.md:40-55`);
   - a private preservation inventory before editing (`SKILL.md:57-65`);
   - a short "What changed" disclosure note after editing (`SKILL.md:173-179`).
   It is more honest about the limits of its research base than most of the field (`references/storyscope-rules.md:75-86`).

2. **The ecosystem is mostly one lineage.** Most of the tools examined are pattern catalogs that trace to Wikipedia's *Signs of AI writing*, often via blader/humanizer. AshwinSathian's survey of 13 other skills counted at least 6 explicit derivatives. Adding tells is not what differentiates projects. What does is how they constrain edits, verify output, and evaluate themselves:
   - HumanScope requires evidence before every edit and treats "no change" as success;
   - avoid-ai-writing ships an editing contract, a deterministic before/after validator and a frozen regression harness;
   - keez97 and humanizer-stack add deterministic scorers.
   Section 2 gives the full taxonomy (OBSERVED).

3. **On preservation-focused rewrites of short texts, ProseShape did not outperform a one-paragraph "strong ordinary editor" prompt.** This comes from the executed comparison: same model, same request, blinded judge. ProseShape scored 6.69/10 against the editor prompt's 7.96, a paired difference of −1.27 [95% CI −2.00, −0.62]; ProseShape was worse on 10 of 13 samples. It was statistically indistinguishable from its parent, blader/humanizer (−0.02). HumanScope (7.48) was the best skill, and no skill beat the editor prompt. Switching the executor from Sonnet 5.5 to Opus 5.5 did not change ProseShape's standing (−0.04). Removing all five reference files did not either (+0.04), at 2.8× lower generation cost (OBSERVED; experiment summary in §3 and Appendix A).

4. **The failures had specific, fixable causes, not general sloppiness.** Across both runs ProseShape:
   - never added or dropped a number (OBSERVED; on the Opus ablation it added one derived worked example, and disclosed it);
   - kept every quote and citation (OBSERVED);
   - left human-written controls almost untouched: 3% of tokens changed, against 27% for the bare model (OBSERVED).

   Its losses came from four rules doing what they say:
   - deleting stated meaning rather than tightening it (a story's realization; characterization claims under hype);
   - adding unrequested voice lines under "voice is not invention" (`SKILL.md:71`);
   - flattening marketing structure, which has no genre gate in `references/mode-guidance.md:73-85`;
   - removing the one em dash from human-written documentation (`SKILL.md:120`).

   ProseShape disclosed most of these moves in its note, which the text-only judge never saw (OBSERVED; INFERRED that the scores understate its usefulness to an author who reads the note).

5. **ProseShape's largest real gap is evaluation methodology, not rule coverage.** Its published results (`evals/eval-log.md:13-24`) have five weaknesses:
   - they compare against a no-skill baseline rather than a competent editing prompt (`evals/eval-log.md:8`);
   - they include no untouched-source arm;
   - they use one run per configuration and same-family graders (`evals/eval-log.md:100-105`);
   - the 12-case `evals.json` and its 72 assertions they cite are not in the repository (`evals/eval-log.md:7,11`; the file is absent);
   - they list mechanical checks that nothing implements (`references/evaluation-rubric.md:50-56`).

   HumanScope and avoid-ai-writing are ahead here in design and discipline, even though neither has established that it beats a good editing prompt either (OBSERVED).

6. **ProseShape's genuine advantages** (OBSERVED unless marked):
   - the most detailed fiction-structure layer found: 19 principles, each with "leave it when" exceptions and over-correction warnings, tied to explicit rewrite vs deep-rewrite permissions (`SKILL.md:124-156`, `references/storyscope-rules.md:88-208`);
   - careful research labeling: Finding, Reading, Practice (`references/storyscope-rules.md:16`);
   - explicit rejection of detector targeting (`README.md:7`);
   - restraint on already-good text, tied for best in the experiment;
   - the clearest change notes of any arm (INFERRED from reading all outputs).
   Its fiction-structure layer and voice matching were **not** exercised by the experiment, so their value remains unmeasured against competitors.

7. **Highest-value changes (P0)** are detailed in §6:
   - publish a reproducible three-arm evaluation (untouched / strong editor / ProseShape) with the missing cases restored;
   - add a deterministic preservation checker implementing the rubric's own mechanical checks;
   - narrow the voice-addition and "get more from the facts" permissions in nonfiction;
   - make rewrite mode tighten stated realizations instead of deleting them;
   - add marketing, social and docs genre gates plus a protected-content rule for pasted Markdown;
   - apply the dash rule only when other tells keep a dash company;
   - fix two attribution issues: the Wikipedia CC BY-SA notice and the unverified "COLM 2026" venue.

8. **What not to copy** (§8), in brief:
   - detector-calibrated numeric gates (sentence-length CV bands, contraction floors, "add a sentence that doesn't quite parse"). keez97's own scorer fails the Python Tutorial and a Jerome K. Jerome passage while passing a formulaic AI email (OBSERVED);
   - blanket word bans and "zero tricolons" rules;
   - "name the expert, add the price" specificity advice that invites invention;
   - multi-thousand-word process contracts without quality evidence;
   - self-scored pass lines.

---

## 2. Competitive taxonomy

### 2.1 Where the field actually differs

"Humanizer" names at least seven technically different things. Most tools combine two or three.

| Approach | Mechanism | Examples (this study) | What it is good for | Main risk |
|---|---|---|---|---|
| **A. Pattern-catalog prompt skill** | A numbered list of AI tells with fixes; the model edits against it | blader/humanizer, keez97, shir-danishyar, lguz, humanizer-stack pass 1, humanizer_academic, AshwinSathian (compact), **ProseShape Level 1** | Removing staging, inflation, chatbot residue | Rules fire on legitimate prose (contrasts, triads, dashes); lists go stale; over-cutting |
| **B. Restraint / evidence-gated editor** | Every edit must name evidence, intended effect, present failure, smallest fix; "no change" is valid | HumanScope (four-slot rule), avoid-ai-writing (candidate → finding → authorized edit) | Proportionality; leaving good prose alone | Under-editing; justification theater |
| **C. Discourse / structural editor** | Questions about narrative or document shape, often from StoryScope or SlopShape | **ProseShape Level 2**, humanizer-stack pass 2, HumanScope lenses, ccf narrative tells, humanspeak (SlopShape) | Changing what surface edits cannot | Research on *detectability* treated as quality guidance; imposing a new template |
| **D. Generation-time guidance** | Rules applied while drafting, not after | shir-danishyar (default mode), AshwinSathian, humanspeak (shape card), **ProseShape Generate mode** (step-back planning, `SKILL.md:91-101`) | Avoiding defaults at the source | Harder to evaluate; applies to all output |
| **E. Deterministic scanner / linter** | Regex or metric checks, often CI-gated | keez97 `score.py`, shir-danishyar lint, humanizer-stack scanners, ccf `surface_scan.py`, slop-linter (Vale), slopster (Vale + diff), avoid-ai-writing detector | Reproducible counting; hooks; diff-only gating | Low precision on human text (§8, measured); optimizing the count |
| **F. Verification / preservation guard** | Before/after comparison of protected content | avoid-ai-writing `validate.js` and preservation-verifier skill; slop-linter's code-token guard; shir-danishyar "no invented numbers" test | Catching damage the model cannot see | Only catches literal damage, not semantic drift |
| **G. Decoding-time suppression** | Backtrack and resample when banned strings appear | antislop-sampler (paper: arXiv:2510.15061) | Suppressing slop at generation with open weights | Needs logits; not available to hosted-model skills |

Orthogonal axes used in §3:

- single-pass vs multi-pass (draft → critique → final);
- critique → rewrite → verify loops;
- voice matching (sample-based, persistent profile, preset personas);
- register gating;
- mode or intensity controls;
- detector orientation (explicitly rejected by ProseShape, HumanScope, avoid-ai-writing, blader; partly embraced by keez97).

### 2.2 Where ProseShape sits

**OBSERVED.** ProseShape combines approach A (Humanizer's taxonomy, adapted: `references/humanizer-rules.md`), approach C for fiction (`references/storyscope-rules.md`, `SKILL.md:124-156`), and approach D (Generate mode's "name the default version, then choose", `SKILL.md:91-101`). It uses approach B's *language* ("choose the lighter mode when unsure", `SKILL.md:53`; "Changing prose only to make it different is a failure", `references/humanizer-rules.md:115`) without B's *mechanism* (no per-edit justification requirement). It has none of E, F or G.

**INFERRED.** ProseShape's closest relatives are HumanScope (same StoryScope source, restraint philosophy) and humanizer-stack (same two-level idea, plus scanners). Its most instructive contrast is avoid-ai-writing, which has converged on very similar editorial values (source fidelity, no injected personality, protected content) but enforces them with a written contract, deterministic tools and a frozen regression harness.

---

## 3. Comparison matrix

"Unknown/not tested" means I found no evidence either way. "Claim" means the author asserts it without independent evidence. Cells cite the strongest evidence I found. Scores come from the executed experiment (Appendix A; Sonnet 5.5 executor, Opus 5.5 blind judge, 13 texts, 2 runs).

### 3.1 Writing transformation and editing intelligence

| Dimension | ProseShape | blader/humanizer | HumanScope | avoid-ai-writing | shir-danishyar | keez97 | humanizer-stack | ccf/humanize |
|---|---|---|---|---|---|---|---|---|
| Blind-judge overall, 13 texts (1–10) | 6.69 | 6.71 | **7.48** | 7.08 | 6.96 | 6.94 | not run | not run |
| Judge "facts" (1–5) | 4.15 | 4.17 | 4.60 | **4.75** | 4.29 | 4.13 | not run | not run |
| Judge-flagged dropped / added facts (39 judgments) | 27 / 6 | 29 / 0 | 13 / 0 | 8 / 0 | 22 / 0 | 23 / 4 | not run | not run |
| Numbers added or dropped (26 outputs) | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | not run | not run |
| Leaves good prose alone (token change on 3 human controls) | **3%** | 3% | 3% (unchanged 4 of 6) | 3% | 7% | 10% | not run | not run |
| Explicit no-invention rule | Yes (`SKILL.md:61-64`) | Yes ([SKILL.md:37](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md#L37)) | Yes, scoped ([SKILL.md:50-53](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/SKILL.md#L50-L53)) | Yes, strongest ([SKILL.md:62-69, 301-317](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L301-L317)) | Yes ([SKILL.md:30-32](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/SKILL.md#L30-L32)) | Yes, but its own examples violate it ([SKILL.md:229](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L229)) | Partial; pass 2 advises adding names and prices ([SKILL.md:74-75](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/skills/structural-humanizer/SKILL.md#L74-L75)) | Yes ([README principles](https://github.com/ccf/humanize/blob/db51ff3f405db5fa522e03fdb517b0a4cac846fd/README.md#L109-L117)), but its README example adds a name |
| Permission to add voice or reactions | Yes, broad (`SKILL.md:71-75`) | Yes, "where the writer would" | No (improve, don't overwrite) | Forbidden unless in source | Yes (generic "write like a person") | Yes, mandated in full mode ([SKILL.md:85-95](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L85-L95)) | Yes ("acknowledged reader") | Only as tagged "additions" |
| Surface vs structural separation | Two levels, one pass (`SKILL.md:78-89`) | One level | Six lenses, gated by purpose | Structure reported, edited only if authorized | One level | Layered passes A→E | Two separate skills | Separate reference files by class |
| Genre / register awareness | Genre voice table (`references/mode-guidance.md:73-85`), **no marketing or social row** | Voice by text type (brief) | Purpose routing ([SKILL.md:127-152](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/SKILL.md#L127-L152)) | Context profiles (linkedin, blog, docs…) | Register table ([SKILL.md:34-45](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/SKILL.md#L34-L45)) | Output-class tiering | Genre calibration file | fiction / expository / conversational |
| Fiction structure | **Deepest**: 19 principles with exceptions | Fiction exempt from rules | Lenses (fiction-derived, gated) | Not a focus | No | No | Six audits (fiction-derived, applied to content) | Narrative tells reference |
| Voice matching | Sample outranks rules (`SKILL.md:30-38,167-171`) | Sample overrides | Match if supplied | Voice presets plus preservation | Sample → persistent `voice-profile.md` | Sample (full mode only) | None | Infers voice, states it |
| Intensity / modes | 6 modes, private (`SKILL.md:40-55`) | 3 output modes | WRITE / EDIT / DIAGNOSE × light/deep | rewrite / detect / edit + iterate cap | generate / rewrite | full / light / off / detect | pass 1 / pass 2 | draft / audit / audit-only |
| Diagnose-only mode | **No** (description excludes critique, `SKILL.md:3`) | No | Yes | Yes | No | Yes | No | Yes (`--audit-only`) |
| Handles intentional style | Sample and genre outrank rules; "when not to act" | "When not to act" | Core stance | Context and intent gate | False-positive guard | Layer E ineffective indicators | Weak | "Register and proficiency are not tells" |

### 3.2 Robustness (experiment unless noted)

| Case | ProseShape | blader/humanizer | HumanScope | avoid-ai-writing | shir-danishyar | keez97 |
|---|---|---|---|---|---|---|
| Quotes and citations verbatim (s06, s09, s13) | Kept | Kept | Kept | Kept | Kept | Kept |
| Code block, table, frontmatter, URL, inline code (s04) | Kept byte-exact | Kept; deleted duplicate H1 (both runs) | Kept | Kept | Kept; deleted duplicate H1 (1 run) | Kept |
| Markdown headings and bold feature labels (s02) | Flattened bold labels (2/2) | Flattened (2/2) | Kept (2/2) | Kept 1/2, flattened 1/2 | Flattened and **deleted page's only heading** (2/2) | Flattened (2/2) |
| Legitimate contrast ("curiosity, not credentials") | Kept 2/2 | Altered 2/2 | Kept 2/2 | Kept 2/2 | Altered 2/2 | Altered 2/2 |
| Human-written docs (Python Tutorial), token change per run | 1% / 0.3%: removed its one em dash (2/2) | 3% / 6%: curly → straight quotes in 7–10 sentences | 0% / 0% | 0.3% / 0% | **12% / 17%** rewritten | **15% / 32%** rewritten |
| 1889 prose with dashes and dialogue | Unchanged | Unchanged | Unchanged | Unchanged | Unchanged | Unchanged |
| Near-clean email (one chatbot line) | Removed only that line | Same | Same | Same | Same | Same |
| Spanish text | Kept Spanish; judged over-cut | Kept Spanish | Kept Spanish | Kept Spanish | Kept Spanish | Kept Spanish |
| Long documents | not tested | not tested | not tested | not tested | not tested | not tested |
| Source text containing instructions | 1 line (`SKILL.md:80`), untested | 1 line, untested | untested | Contract plus tested scenario | untested | untested |

The bare-model baseline rewrote 27% of the human controls, including a third of the Jerome K. Jerome passage, and dropped a fact from the email. Every skill, and the ordinary-editor prompt, protected human text better than the bare model.

### 3.3 Engineering, developer experience and evaluation maturity

| Dimension | ProseShape | blader/humanizer | HumanScope | avoid-ai-writing | shir-danishyar | keez97 | humanizer-stack | ccf/humanize |
|---|---|---|---|---|---|---|---|---|
| Deterministic components | None | Package validator only | None (by design) | Detector, preservation validator, quote normalizer, style checker | Pattern linter | `score.py` battery, optional GPT-2/Binoculars | 2 regex scanners | Surface scanner |
| Automated tests | None (trigger JSON only) | Package CI | None | Extensive JS/Python tests plus CI | 46 pytest tests (**ran: pass**) | None | None | 109 pytest tests (**ran: pass**) |
| Prompt size loaded per rewrite | ~84 KB if all references read (SKILL 19 KB) | 33 KB | 13 KB | 139 KB (SKILL + required patterns) | 43 KB | 56 KB | two skills | 150-line SKILL + references |
| Generation cost, 13 texts (Sonnet 5.5, list price) | $0.75 | $0.35 | $0.27 | $0.75 | $0.30 | $0.41 | not run | not run |
| Install | git clone into skills dir | plugin marketplace, `npx skills` | git clone | plugin, Action, multiple harnesses | plugin, `npx skills`, slash command | git clone, plugin dir | install script (symlinks) | plugin for 5 harnesses |
| Shows what changed and why | **Yes: 3–5 line note** (`SKILL.md:175`) | Draft plus remaining patterns | Optional change summary | Changes plus Verification block | No (text only by design) | 6-section output | No | Audit table plus before/after metrics |
| Baseline in own eval | No-skill model (`evals/eval-log.md:8`) | Raw AI text (issue #229) | Untouched, ordinary editor, compact | Frozen historical baseline plus scenarios | None | GPTZero (detector) | None | Fixtures |
| Blinded judging | Yes, same family | Claim (#229), same family | Yes, 2 OpenAI judges | Model assessor | No | No | No | No |
| Untouched source as judged option | No | No | Planned (design gap noted) | Clean no-op scenarios | No | No | No | No |
| Held-out split | No | No | Specified, not run | Yes (36 dev / 12 held-out, author-level) | No | No | No | No |
| Human raters | No | No | Protocol designed, not run | Optional, not run | No | No | No | No |
| Eval cases public | Fixtures yes; **cases and assertions missing** | No | Yes, with judge prompts and keys | Yes, 48 cases with claims and protected spans | 4 pairs plus 4 fixtures | No | No | 8 fixtures |
| License | MIT | MIT | MIT | MIT | MIT | MIT | MIT (+ CC BY-SA notice) | MIT |

---

## 4. Competitor findings

All repositories were checked 2026-09-30 by shallow or full clone at the listed commit. Stars and forks are GitHub page counts on that date, used only as adoption signals.

### 4.1 blader/humanizer: the parent catalog

- **Repository:** https://github.com/blader/humanizer
- **Commit examined:** `225a6f3` (v3.1.0, 2026-09-27)
- **Project type:** single-prompt Agent Skill
- **Environments:** Claude Code plugin, Codex, Cursor, any skills harness
- **License:** MIT
- **Activity:** 97 commits, active PR flow; 52.9k stars, 4.2k forks

**Architecture and technique.** OBSERVED: one 397-line `SKILL.md` with 26 patterns in six groups, strongest first ([SKILL.md:55-381](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md#L55-L381)). A four-step workflow: mark → draft → check → final ([L34-39](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md#L34-L39)). An evidence rule: patterns 1–5 act on one sighting, patterns marked *weak alone* need company ([L30](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md#L30)). Three output modes ([L47-53](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md#L47-L53)). CI validates only package metadata ([validate.yml](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/.github/workflows/validate.yml)).

**Evaluation.** Author claim: "judges preferred Humanizer's rewrite over the original AI text 16 times out of 16" ([README:13](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/README.md#L13)). Checked in [issue #229](https://github.com/blader/humanizer/issues/229):
- the judges were one model family;
- only 77 of 144 planned trials completed;
- the comparison is against raw AI text, not a competent edit;
- the same issue reports that a custom checker added nothing (12 of 21, chance) and that the rewrite pass *increased* a "uniform beat rate" measure from 60 to 101.

**Genuinely interesting / well designed:**
- The "why AI text sounds this way" account that orders patterns by strength.
- The *weak alone* evidence tiering.
- Keep clauses on each pattern.
- A structured "rewrite problem" issue template that collects failures as data ([rewrite-problem.yml](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/.github/ISSUE_TEMPLATE/rewrite-problem.yml)).
- A word cap on `SKILL.md` enforced by the validator ([AGENTS.md](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/AGENTS.md)).

**Weaknesses:**
- "Vary sentence length; real writing alternates short and long" ([L39](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md#L39)) is rhythm by rule. ProseShape correctly reversed it (`references/humanizer-rules.md:51`).
- The absolute dash ban without a sample ([L162](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md#L162)).
- In the experiment it altered a legitimate contrast in 2 of 2 runs, converted curly quotes in human docs, and had the most judge-flagged dropped facts (29) and format issues (10). OBSERVED.

**Different from ProseShape:** no narrative layer, no mode system beyond output format, and a visible draft/critique/final output.

**Worth investigating:** the failure-report issue template (low cost; turns user reports into regression cases) and the prompt-length budget check.

**Do not copy:** the dash ban as an absolute, and "vary sentence length" as a rule.

### 4.2 Anson-Saju-George/HumanScope: evidence-gated restraint

- **Repository:** https://github.com/Anson-Saju-George/HumanScope
- **Commit examined:** `51b343a` (2026-09-26)
- **Project type:** Agent Skill plus a large research and evaluation archive
- **Environments:** Claude Code, claude.ai
- **License:** MIT
- **Activity:** 19 commits in about 10 days; 0 stars

**Technique.** OBSERVED:
- A four-slot rule: an edit is justified only with evidence, intended effect, present failure, and smallest useful change. "It's AI-like" is not a failure ([SKILL.md:68-96](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/SKILL.md#L68-L96)).
- Six StoryScope-inspired lenses framed as two-sided questions ([L98-121](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/SKILL.md#L98-L121)).
- Purpose routing that keeps expository text on a "lean" path ([L127-152](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/SKILL.md#L127-L152)).
- WRITE / EDIT / DIAGNOSE modes, light by default ([L55-66](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/SKILL.md#L55-L66)).
- An explicit refusal of word bans and imperfection injection ([L167-171](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/SKILL.md#L167-L171)).

**Evaluation (the most self-critical in the field).** OBSERVED:
- The rubric requires three arms: untouched, ordinary edit, and HumanScope ([evals/rubric.md:7-16](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/evals/rubric.md#L7-L16)).
- A fair re-test with two blinded OpenAI judges found S vs O = 1 win, 2 losses, 3 ties ([fair-retest/RESULTS.md:25-47](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/test-run/fair-retest/RESULTS.md#L25-L47)). The README states its advantage over ordinary editing "remains unestablished" ([README:150-151](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/README.md#L150-L151)).
- It documents a confound in its own earlier A/B ([README:136-142](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/README.md#L136-L142)).
- It records a manifest error where the "defect" it had labeled was actually information ([MANIFESTS.md](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/test-run/fair-retest/MANIFESTS.md)).
- A held-out suite with freeze-and-hash rules is specified but not run ([evals/heldout-v1.1.md](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/evals/heldout-v1.1.md)).
- My experiment independently matches its own finding: HumanScope was the best skill (7.48), but did not significantly beat the editor prompt (−0.48 [−1.15, +0.12]).

**Genuinely interesting:**
- "It sounds AI-like" is not an admissible reason to edit.
- The paired-brief design in the held-out suite: the same deletion is right under one brief and wrong under another.
- A rejected-ideas log that keeps folklore out ([research/rejected-ideas.md](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/research/rejected-ideas.md)).
- The observation that deleting a "realization" paragraph can destroy motive information. This is directly relevant to ProseShape's s08 result.

**Weaknesses:**
- Heavy research apparatus for a 176-line skill, with most evidence produced by model reviewers.
- The lenses are not isolated from the rest of the prompt (the compact ablation also removes guards).
- Under-editing risk: 7 "under_edit" flags in my judging.
- No deterministic checks, by choice ([human-eval-protocol.md:55-59](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/evals/human-eval-protocol.md#L55-L59)).

**Worth investigating for ProseShape:**
- The three-arm evaluation design with untouched and strong-editor arms (P0).
- Tighten, don't delete, for stated meaning in edit mode (P0).
- A DIAGNOSE mode (P1).
- A four-slot justification check limited to light edits, as an ablation (P2).

**Do not copy:** the size of the research archive as a substitute for reader evidence, and model-reviewer "rounds" presented as validation.

### 4.3 NulightJens/humanizer-stack: two passes plus scanners

- **Repository:** https://github.com/NulightJens/humanizer-stack
- **Commit examined:** `13f5c02` (2026-07-24)
- **Project type:** two Claude skills, two Python scanners, install script
- **License:** MIT, plus a CC BY-SA notice for Wikipedia-derived material
- **Activity:** 4 commits; 304 stars, 23 forks

**Technique.** OBSERVED:
- Pass 1 is a fork of an older blader/humanizer (v2.1.1).
- Pass 2 is a structural skill with six audits run one at a time, "audit the outline, not the prose", and "pick 1–2 interventions per piece" ([structural SKILL.md:32-40, 89-106](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/skills/structural-humanizer/SKILL.md#L32-L106)).
- Two stdlib scanners with `--json` and `--strict`: [copy_scan.py](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/scripts/copy_scan.py) and [structural_scan.py](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/skills/structural-humanizer/scripts/structural_scan.py).
- [ATTRIBUTION.md](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/ATTRIBUTION.md) flags that Wikipedia's catalog is CC BY-SA 4.0 and that its selection and arrangement may carry share-alike obligations.

**Weaknesses:**
- **Invention risk:** "'An expert' gets a name. 'Recently' gets a date. Add the price, the version number, the city" ([L74-75](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/skills/structural-humanizer/SKILL.md#L74-L75)), with no source requirement in that passage.
- **Detector framing:** "Rarity IS the human signal … a new detectable cluster" ([L37](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/skills/structural-humanizer/SKILL.md#L37)).
- **Injected reader address:** "I know how this sounds" ([L77-82](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/skills/structural-humanizer/SKILL.md#L77-L82)). ProseShape explicitly rejects this move (`references/storyscope-rules.md:80,197`).
- **Unrelated evidence transferred:** "aspect-based checking found 95% of issues … vs 68%" is a finding about the study's feature-extraction pipeline, used to justify an editing workflow (INFERRED; the paper's claim concerns labeling, not rewriting).
- **Scanner flags on plain punctuation:** `copy_scan.py` flags every em dash in visible copy ([L34-42](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/scripts/copy_scan.py#L34-L42)). On my corpus it flagged the human Python Tutorial and missed the inflated news article (OBSERVED, `results/scanner_controls.md`).
- **No tests or evaluation.**

**Different from ProseShape:** surface and structure as separate skills run in sequence; structure applied to content marketing, not just fiction; scanners.

**Worth investigating:**
- The idea of auditing an extracted skeleton (beats, where meaning is stated, what resolves) before rewriting. ProseShape's pass 3 (`SKILL.md:84`) could ask for this explicitly in deep-rewrite mode.
- The CC BY-SA observation (P0 attribution).

**Do not copy:** the "add the specific" advice, the rarity target, and reader-address insertion.

### 4.4 shir-danishyar/humanize: generation-first, register table, linter with tests

- **Repository:** https://github.com/shir-danishyar/humanize
- **Commit examined:** `024aa19` (v2.1.0, 2026-09-02)
- **Project type:** skill, slash command, stdlib linter, pytest suite, CI
- **License:** MIT
- **Activity:** 12 commits; 19 stars

**Technique.** OBSERVED:
- Generation mode is the default and rewrite mode is secondary ([SKILL.md:16-28](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/SKILL.md#L16-L28)).
- A register table covering contractions, fragments and dash allowance by social, email, editorial or formal register ([L34-45](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/SKILL.md#L34-L45)).
- A persistent `voice-profile.md` extracted from samples and updated on correction ([references/voice.md:23-52](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/references/voice.md#L23-L52)).
- A density linter with a threshold of 5 hits per 1k words ([scripts/ai_pattern_lint.py](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/scripts/ai_pattern_lint.py)).

**Evaluation.** OBSERVED: 46 tests that I ran and that pass. They include:
- human fixtures that must pass the linter ([tests/test_lint.py:33-35](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/tests/test_lint.py#L33-L35));
- "after" fixtures that must invent no numbers ([L52-63](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/tests/test_lint.py#L52-L63));
- a CI test that the README's own example lints clean and adds no numbers ([L247-271](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/tests/test_lint.py#L247-L271)).

**Weaknesses:**
- The linter's rule-of-three check is a bare regex matching any "A, B, and C" ([L170-171](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/scripts/ai_pattern_lint.py#L170-L171)). It failed the human Python Tutorial (6.5 per 1k) on "Windows, macOS, and Unix". It passed the formulaic AI email and the AI-shaped story at 0.0 (OBSERVED).
- The "after" fixtures were written to pass the same linter, which is circular.
- "No headings at all under ~400 words" ([L71](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/SKILL.md#L71)) deleted the marketing page's heading in both runs (OBSERVED).
- "Vary sentence length" ([L65](https://github.com/shir-danishyar/humanize/blob/024aa193966341e0706e96f0277f914092bed2c7/SKILL.md#L65)).

**Different from ProseShape:** generation-first defaults, a persistent voice profile, and a testable linter.

**Worth investigating:**
- The "invent no numbers" test pattern for ProseShape's own examples (P0, in the checker).
- An opt-in persistent voice profile (P2; privacy trade-off).

**Do not copy:** density thresholds as pass/fail, regex triad detection, and the headings ban.

### 4.5 keez97/humanizer: detector-calibrated battery

- **Repository:** https://github.com/keez97/humanizer
- **Commit examined:** `2d9a116` (v2.9.0, 2026-07-30)
- **Project type:** skill plus a stdlib scoring script plus optional GPT-2 and Binoculars scorers
- **License:** MIT
- **Activity:** 31 commits; 4 stars

**Technique.** OBSERVED:
- Five layers, fixed in order ([SKILL.md:105-257](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L105-L257)).
- A 14-check battery with HARD gates: sentence-length CV ≥ 0.45, contractions ≥ 1 per 200 words, zero em dashes, zero Tier-1 words ([L321-351](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L321-L351)).
- A mandated "deliberate imperfection" in full mode, including "a sentence that doesn't quite parse cleanly" ([L91, 390](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L91)).
- full / light / off / detect modes ([L40-54](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L40-L54)).

**Evaluation and claims.** Author's documented study: six rewrites scored against GPTZero stayed at "100% AI". The author concludes that editing cannot beat a trained classifier ([references/DETECTION-LIMITS.md:7-27](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/references/DETECTION-LIMITS.md#L7-L27)). That honest negative result is useful. Yet some rules (B17, B18) were added "in response to this scan", which is detector-driven rule development.

**Weaknesses.** OBSERVED from my runs of `score.py` on the unedited corpus:
- **Full mode fails genuine human text:** the Python Tutorial (4 HARD fails: CV 0.31, no contractions, one em dash, too few short sentences) and the 1889 Jerome K. Jerome passage (2 HARD fails).
- **Light mode fails both on the em dash alone.**
- **It passes the formulaic AI email** (`results/scanner_controls.md`).
- **Its own "fix" examples fabricate sources**, contradicting its no-fabrication principle ([L78-81](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L78-L81)):
  - "per a 2019 Chinese Academy of Sciences survey" ([L229](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L229));
  - "In a 2024 NYT interview" ([L231](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L231));
  - "three IT parks opened" ([L119](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L119)).
- **Blind judging:** it tied the bare-model baseline for the most "changed fact" flags (11), and it rewrote 15% and 32% of the human-written Python Tutorial across the two runs (OBSERVED).

**Genuinely interesting:**
- Pass 4 asks two *separate* questions, "what still sounds generated?" and "does the rewrite state any fact that isn't in the source?", because "a fabricated specific is invisible to a style audit" ([L383-386](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L383-L386)).
- The two-pass cap against over-fitting to the checklist ([L74](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L74)).
- The Layer E "ineffective indicators" table.
- The "What's left I'm watching" output section.

**Worth investigating:** a separate fabrication question in ProseShape's self-review (`SKILL.md:183` merges it with the rest). Cheap; test it (P1).

**Do not copy:** CV bands, contraction floors, deliberate imperfection, zero-dash hard gates, and GPT-2/Binoculars rankings as writing targets.

### 4.6 AshwinSathian/humanize-writing-skill: compact generation-time guidance with scope gating

- **Repository:** https://github.com/AshwinSathian/humanize-writing-skill
- **Commit examined:** `65f84fa` (v1.1.1, 2026-08-26)
- **Project type:** skill for Claude's own output, plus research notes
- **License:** MIT
- **Activity:** 27 commits; 1 star

**Technique.** OBSERVED:
- A 111-line skill applied to all prose Claude writes.
- A "Scope" section that yields to user requests, other people's text, uniform-structure formats (API docs), fiction, legal text, marketing copy, non-English text, and very short text ([SKILL.md:42-73](https://github.com/AshwinSathian/humanize-writing-skill/blob/65f84fab8361184960410186f99d5b4cf506c972/SKILL.md#L42-L73)).
- Each scope bullet was added after a red-team RED/GREEN check ([reference/validation-note.md:228-380](https://github.com/AshwinSathian/humanize-writing-skill/blob/65f84fab8361184960410186f99d5b4cf506c972/reference/validation-note.md#L228-L380)).
- A survey of 13 other skills ([reference/oss-skills-review.md](https://github.com/AshwinSathian/humanize-writing-skill/blob/65f84fab8361184960410186f99d5b4cf506c972/reference/oss-skills-review.md)).

**Evaluation.** Skill-on vs skill-off generations on three topics and three models, graded by tell presence ([validation-note.md:19-226](https://github.com/AshwinSathian/humanize-writing-skill/blob/65f84fab8361184960410186f99d5b4cf506c972/reference/validation-note.md#L19-L226)). This shows the skill *changes* output, not that it *improves* it. No fidelity checks, no blinding.

**Weaknesses:**
- "Cut hedge-intensifiers: rather, very, little, pretty" ([L29-30](https://github.com/AshwinSathian/humanize-writing-skill/blob/65f84fab8361184960410186f99d5b4cf506c972/SKILL.md#L29-L30)) runs against evidence other projects cite, that single hedges and intensifiers are more common in human text (keez97 cites Reinhart et al., PNAS).
- The survey says lguz cites unverifiable "Carnegie Mellon (2025)" research. I found no such text anywhere in lguz's history at `4b7c37f` (`git log -S` returned nothing), so competitor teardowns need checking too.

**Worth investigating:** the scope-gating method. Write a red case for a genre, see it fail, add a gate, re-verify. ProseShape's missing marketing and social gates are exactly what this method caught (P0).

**Do not copy:** applying humanizing to *all* output by default. ProseShape's trigger discipline (`evals/trigger-evals.json`) is better.

### 4.7 lguz/humanize-writing-skill: preset voices and a strict checklist

- **Repository:** https://github.com/lguz/humanize-writing-skill
- **Commit examined:** `4b7c37f` (v2, 2026-03-12)
- **Project type:** Claude plugin plus portable prompt
- **License:** MIT
- **Activity:** 4 commits; 54 stars, 6 forks

**Technique.** OBSERVED:
- Three passes: vocabulary, structure, "human texture".
- A preset voice menu (clear-thinker "inspired by Paul Graham", casual storyteller, and others). It asks the user to choose and *waits* when neither voice nor sample is given ([SKILL.md:39-68](https://github.com/lguz/humanize-writing-skill/blob/4b7c37fa5148fd499e18498fcc91bb10ed801733/skills/humanize-writing/SKILL.md#L39-L68)).
- An 18-item checklist including "Zero tricolons" and "At least one sentence starts with 'And' or 'But'" ([L197-218](https://github.com/lguz/humanize-writing-skill/blob/4b7c37fa5148fd499e18498fcc91bb10ed801733/skills/humanize-writing/SKILL.md#L197-L218)).

**Weaknesses:**
- No explicit no-invention rule. "What to Protect" says only to keep meaning ([L220-230](https://github.com/lguz/humanize-writing-skill/blob/4b7c37fa5148fd499e18498fcc91bb10ed801733/skills/humanize-writing/SKILL.md#L220-L230)).
- Its specificity example invents a figure ("we burned through $40k", [L170-172](https://github.com/lguz/humanize-writing-skill/blob/4b7c37fa5148fd499e18498fcc91bb10ed801733/skills/humanize-writing/SKILL.md#L170-L172)).
- The checklist rules are mechanical: zero triads drops legitimate three-item content.
- It says not to use it on technical docs.
- No tests or evaluation.

**Worth investigating:** nothing structural. The idea of showing writing the user *doesn't* like as a negative sample ([L50-51](https://github.com/lguz/humanize-writing-skill/blob/4b7c37fa5148fd499e18498fcc91bb10ed801733/skills/humanize-writing/SKILL.md#L50-L51)) is a small, reasonable voice-matching addition.

**Do not copy:** preset celebrity-style voices, forced questions before rewriting, and quota checklists.

### 4.8 conorbronsdon/avoid-ai-writing: editing contract plus deterministic verification plus frozen evals

- **Repository:** https://github.com/conorbronsdon/avoid-ai-writing
- **Commit examined:** `9b8d030` (v3.36.0, 2026-09-29)
- **Project type:** skill family (router, rewriter, detector, preservation verifier, file editor), JS detector and validator, GitHub Action, eval harness
- **License:** MIT
- **Activity:** 481 commits since 2026-03-05; 4.8k stars, 419 forks

**Technique.** OBSERVED:
- **An editing contract.** A pattern match is a candidate; it becomes a finding only after context checks, and an edit only if the mode authorizes it. "Detection alone never authorizes rewriting." ([SKILL.md:34-105](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L34-L105)).
- **Source text treated as data**, including embedded instructions ([L53-60](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L53-L60)).
- **Protected regions**: quotes, code, tables, URLs, frontmatter ([L71-77](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L71-L77)).
- **A two-pass ceiling** with a reported stop reason ([L125-127](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L125-L127)).
- **A "Never inject these" list**: fabricated speaker perspective, staccato conversion, invented specifics. It explicitly responds to a stress test that found blader/humanizer produced "a recognizable *humanizer* voice" ([L301-317](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L301-L317)).
- **A deterministic before/after validator** ([detector/validate.js](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/detector/validate.js)):
  - errors: fenced code, frontmatter, blockquotes, tables, inline code, URLs, paths, heading count and level;
  - warnings: numbers, heading text, large shrink.
  I ran it on every experiment output; it is precise but literal.
- **A Verification block** that must say which checks actually ran versus were model-only ([L226-248](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L226-L248)).

**Evaluation.** OBSERVED:
- 48 synthetic rewrite cases, each with atomic claims, protected spans, and allowed and forbidden phrases.
- A development / held-out split by fictional author and document, with leakage checks.
- A frozen protocol with hashes ([evals/rewrite/README.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/evals/rewrite/README.md), [cases.json](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/evals/rewrite/cases.json)).
- An automated merge gate over eight contract scenarios: clean no-op, useful edit, fidelity with blunt voice, technical context, protected content, explicit transformation, source-internal instruction, detect-only. It records failures and repairs ([report](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/evals/rewrite/reports/automated-stack-295-296-2026-09-16/README.md)).
- A self-scan of its own docs with both raw and exempted scores published ([PROOF.md](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/PROOF.md)).

**Weaknesses:**
- **The merge gate tests contract compliance, not prose quality.** "Human evaluation was not required or performed" ([report L7-8](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/evals/rewrite/reports/automated-stack-295-296-2026-09-16/README.md#L7-L8)).
- **Prompt mass.** `SKILL.md` is 4,816 words and `SKILL.full.md` is 21,105; the required pattern reference is 106 KB.
- **Conservative in practice.** In my experiment it had the fewest judge-flagged fidelity issues (8 dropped, 0 added) but the most "under-edit" flags (20) and the lowest naturalness score among skills (4.06). It scored 7.08 overall, below the ordinary editor at −0.88 [−1.58, −0.21] (OBSERVED).

**Different from ProseShape:** in values, very little: fidelity, no injected personality, and protected content all appear in ProseShape. In mechanism, almost everything: contract language, deterministic tools, verification reporting, and a regression harness.

**Worth investigating:**
- Its preservation checks: implement an equivalent, or reuse the validator (MIT) (P0).
- The eight-scenario contract suite as a model for ProseShape regression cases (P0/P1).
- The "Never inject" list's treatment of reactions as fabrication (P0).
- Source-as-data test cases (P1).

**Do not copy:** the prompt mass, the multi-skill router, or pass-count reporting ceremony. Nothing shows they improve prose. ProseShape's lighter note format serves authors better.

### 4.9 sam-paech/antislop-sampler: decoding-time suppression

- **Repository:** https://github.com/sam-paech/antislop-sampler
- **Commit examined:** `0ae330e` (2026-03-05)
- **Project type:** Python sampler and API server for local open-weights models
- **License:** Apache-2.0
- **Activity:** 354 stars
- **Paper:** [arXiv:2510.15061](https://arxiv.org/abs/2510.15061) (Paech, Roush, Goldfeder, Shwartz-Ziv, 2025)

**Technique.** OBSERVED:
- When a banned phrase or regex appears during generation, it backtracks to the first token and resamples with reduced probability ([README](https://github.com/sam-paech/antislop-sampler/blob/0ae330e98fbe6f09351f2d1063a51956378a44b2/README.md)).
- Slop lists come from over-representation against human baselines.
- The README warns the lists are "mostly auto-generated … not well optimised or curated".

**Author claims (abstract):** some patterns are "over 1,000x more frequent" in LLM output than in human text; it suppresses 8,000+ patterns "while maintaining quality"; its FTPO fine-tuning method gets 90% slop reduction while maintaining GSM8K, MMLU and creative-writing scores. Not independently verified here.

**Relevance to ProseShape.** Not directly applicable: hosted-model skills cannot touch logits. The transferable idea is methodological (INFERRED): derive any word or phrase watchlist from measured over-representation against a human baseline, not intuition. Its regex bans on "not x, but y" show the same pattern-level suppression can be mechanical, and so share the false-positive risk measured in §8.

### 4.10 t0ddharris/slopster and 4.11 thrash-d/slop-linter: Vale linters, hooks and diff gating

- **slopster:** https://github.com/t0ddharris/slopster @ `084e39a` (2026-08-24), MIT, 2 stars
  - Six Vale rules.
  - A "Tagore" skill with an 8-dimension self-score that "fails anything below 56/80" ([README:26](https://github.com/t0ddharris/slopster/blob/084e39ab93c41d217ea05bf9f7ca769335cf40f1/README.md#L26)).
  - `slop-diff`, which reports only *new* findings on a branch versus main ([README:28-31](https://github.com/t0ddharris/slopster/blob/084e39ab93c41d217ea05bf9f7ca769335cf40f1/README.md#L28-L31)).
- **slop-linter:** https://github.com/thrash-d/slop-linter @ `a44c2d9` (2026-09-29), MIT, 1 star
  - 77 Vale rules, including a separate code-comment style.
  - A Claude Code hook that lints what the agent just wrote.
  - A **comment guard** that compares code tokens before and after a comment cleanup and fails on any non-comment change ([README:15](https://github.com/thrash-d/slop-linter/blob/a44c2d9eb6c20ac0dc33daf3f0b4a19ab3c3ebb5/README.md#L15)).
  - should-flag / should-pass test folders.
  - False positives tuned on about 3,900 real comments ([README:16](https://github.com/thrash-d/slop-linter/blob/a44c2d9eb6c20ac0dc33daf3f0b4a19ab3c3ebb5/README.md#L16)).

**Genuinely interesting:**
- The *invariance guard*: prove that an editing pass left protected material untouched. This is the same idea as avoid-ai-writing's validator, applied to code.
- Diff-only gating, so legacy text does not block new work.
- False-positive tuning on a real corpus, with should-pass fixtures.

**Weaknesses:**
- Word and phrase rules with fixed levels.
- A self-assigned numeric pass line (56/80) that measures the model's opinion of itself.

**For ProseShape:** an invariance check for protected spans is worth building (P0 checker). Vale integration is optional (P2), as ProseShape targets prose authors, not docs pipelines.

### 4.12 signalfi/humanspeak: structure-first nonfiction (SlopShape)

- **Repository:** https://github.com/signalfi/humanspeak
- **Commit examined:** `28eee02` (2026-09-26)
- **License:** MIT
- **Activity:** 2 commits; 2 stars

**Technique.** OBSERVED:
- Gather real material first and mark gaps with `[NEED: …]` instead of inventing.
- Fill in a "shape card" (shape, speaker, title, opening, ending, takeaway).
- Run a 14-question structural audit, then a word-level pass ([README:16-19](https://github.com/signalfi/humanspeak/blob/28eee02d2416b547e04e6eee4fc4d4192f489bc5/README.md#L16-L19)).
- It is grounded in SlopShape ([arXiv:2609.15369](https://arxiv.org/abs/2609.15369), Madler, 2026). The paper exists; I checked the abstract. It reports that structural features alone detect AI commercial blog posts at 97.0 macro-F1, with 96.1 after self-rewording.

**Evaluation.** 75 drafts with judgments; LLM judge; tell-presence counts, not quality ([README:41-57](https://github.com/signalfi/humanspeak/blob/28eee02d2416b547e04e6eee4fc4d4192f489bc5/README.md#L41-L57)).

**Weaknesses:**
- The README's "98 macro-F1" ([L5](https://github.com/signalfi/humanspeak/blob/28eee02d2416b547e04e6eee4fc4d4192f489bc5/README.md#L5)) does not match the abstract's 97.0.
- Like StoryScope, SlopShape measures *separability*. Some "AI" features (a thesis up front, frequent headings, a summarizing close) are genre virtues in docs and reports.

**For ProseShape:** SlopShape is the nonfiction counterpart ProseShape currently lacks: its nonfiction structure check is one sentence (`SKILL.md:84`). It is worth a genre-gated experiment (P2). The `[NEED: …]` convention overlaps with ProseShape's "mention the gap in your note" (`SKILL.md:61`); inline placeholders are an option, never the default.

### 4.13 ccf/humanize: audit table, scanner, "additions you may want to reverse"

- **Repository:** https://github.com/ccf/humanize
- **Commit examined:** `db51ff3` (2026-09-14)
- **License:** MIT
- **Activity:** 86 commits in 2 days; 1 star

**Technique.** OBSERVED:
- Classify the text as fiction, expository or conversational.
- Run a stdlib scanner (80+ words).
- Report at most ten tells, each with a quoted example and a base rate.
- State the inferred voice in one line.
- Fix only what fired.
- Tag additive fixes and list them under "Choices you may want to reverse".
- Re-scan and flag if variance fell: "converging is a failure even as tell counts fall" ([SKILL.md:117-140](https://github.com/ccf/humanize/blob/db51ff3f405db5fa522e03fdb517b0a4cac846fd/skills/humanize/SKILL.md#L117-L140)).
- "Register and proficiency are not tells" ([README:115](https://github.com/ccf/humanize/blob/db51ff3f405db5fa522e03fdb517b0a4cac846fd/README.md#L115)).
- 109 tests that I ran and that pass.

**Weaknesses:**
- Its own README example rewrite opens with "Sarah —", a name not in the input ([README:101](https://github.com/ccf/humanize/blob/db51ff3f405db5fa522e03fdb517b0a4cac846fd/README.md#L101)).
- Its scanner reports the human Python Tutorial's sentence-length CV as 0.32, below the README's "human 0.5–0.9" band (OBSERVED), so the base rates can mislead on expository human text.

**For ProseShape:**
- A one-line "voice I'm preserving" statement is cheap and makes voice decisions inspectable (P2 test).
- Tagging additions separately in the note is close to what ProseShape already does (`SKILL.md:75`).

### 4.14 matsuikentaro1/humanizer_academic: domain specialization

- **Repository:** https://github.com/matsuikentaro1/humanizer_academic
- **Commit examined:** `74f9b87` (v2.3.0, 2026-09-30)
- **License:** MIT
- **Activity:** 32 commits; 270 stars, 37 forks

**Technique.** OBSERVED:
- A 775-line medical-academic fork with a hard-coded single-author voice profile ([SKILL.md:50-79](https://github.com/matsuikentaro1/humanizer_academic/blob/74f9b87b216fea2f51cd4327011da2a97ca83896/SKILL.md#L50-L79)).
- A list of academic phrases to *preserve* ([L81-114](https://github.com/matsuikentaro1/humanizer_academic/blob/74f9b87b216fea2f51cd4327011da2a97ca83896/SKILL.md#L81-L114)).
- "Reader clarity before compression": don't delete connectives that carry logic ([L21-29](https://github.com/matsuikentaro1/humanizer_academic/blob/74f9b87b216fea2f51cd4327011da2a97ca83896/SKILL.md#L21-L29), and the Pattern 27 section).

**Weaknesses:**
- It allows inserting figures and references "from your own knowledge" marked `[verify: <source>]` ([L41](https://github.com/matsuikentaro1/humanizer_academic/blob/74f9b87b216fea2f51cd4327011da2a97ca83896/SKILL.md#L41)). This is a hallucination channel even with the marker.
- Pattern 22 *adds* hedging, which is right for observational medicine and wrong elsewhere.
- Its mandatory burstiness rule is justified by detector-score reduction: "restructuring sentence rhythm accounts for ~90% of the achievable reduction in AI-detection scores" ([L656](https://github.com/matsuikentaro1/humanizer_academic/blob/74f9b87b216fea2f51cd4327011da2a97ca83896/SKILL.md#L656)). That is a detector objective, not a reader one.

**For ProseShape:** its preserve-list and connective-preservation rules show what a register-specific carve-out looks like. ProseShape's academic row (`references/mode-guidance.md:81`) is one line. INFERRED: an academic or technical "do not flag" list would reduce the "logical connective stripped" failure that its author documents as common.

**Do not copy:** knowledge-sourced insertions, and a hard-coded author profile.

---

## 5. ProseShape gap analysis

### 5.0 What ProseShape currently is (Phase 1 findings)

**OBSERVED:**

- **Runtime**
  - `SKILL.md` (199 lines). Frontmatter (`SKILL.md:1-8`), with a trigger description that lists near-misses (`SKILL.md:3`).
  - Six references: surface rules (`references/humanizer-rules.md`, 125 lines), StoryScope rules (245), mode guidance (125), eleven worked examples (275), evaluation rubric (60), maintainer notes (54).
  - No executable code.
- **Design principles**
  - Preservation outranks style: a seven-level priority ladder with the user's instructions and samples first (`SKILL.md:28-38`) and an inventory before any edit (`SKILL.md:57-65`).
  - Two levels of default detection (`SKILL.md:14-21`), with cautions that research findings are population tendencies, not quotas, and that "human does not mean messy" (`SKILL.md:23-26`).
  - Voice must survive cutting: "Cut, then give it a person" (`SKILL.md:67-76`).
  - Modes chosen privately, lighter when unsure (`SKILL.md:40-55`).
  - Generation plans against "the default version" (`SKILL.md:91-101`).
  - Readers, not detectors (`README.md:7`, `SKILL.md:65`).
- **Process.** Eight passes: preserve, surface, structural, rewrite whole units, voice check, preservation check, artificiality check, final read (`SKILL.md:78-89`). Output is the text plus a 3–5 line "What changed" note (`SKILL.md:173-179`).
- **Evidence handling.** StoryScope statements are labeled Finding, Reading or Practice (`references/storyscope-rules.md:16`), with a "complications you must respect" section (`references/storyscope-rules.md:75-86`), including "Distinguishable is not better" (`:84`).
- **Evaluation**
  - 10 input fixtures (`evals/files/`).
  - 20 trigger queries (`evals/trigger-evals.json`).
  - An evaluation log reporting four blind model-graded iterations (`evals/eval-log.md:13-20`) with a noise estimate (`:22`) and limitations (`:98-105`).
  - A cost note: 65–74k tokens per run with the skill vs 41k without (`:107-109`).
- **Packaging.** git clone into a skills directory (`README.md:24-44`); MIT; third-party notice for Humanizer and StoryScope (`THIRD_PARTY_NOTICES.md`).
- **History.** All 25 commits and all five versions (1.0 → 1.3.1) are dated 2026-09-29 (`references/prompt-engineering-notes.md:48-54`; `git log`). The "raw build workspace" is intentionally omitted (`README.md:89`).

### 5.1 Areas where ProseShape already has an advantage

1. **Restraint on already-good text.**
   - OBSERVED: 3% token change on human controls, tied for lowest.
   - Near-clean email reduced to deleting the one chatbot line in both runs.
   - The 1889 passage left untouched.
   - Judge voice score 5.00 on controls.
   - Its "choose the lighter mode when unsure" rule (`SKILL.md:53`) and "Changing prose only to make it different is a failure" (`references/humanizer-rules.md:115`) appear to work.
2. **Numeric, quotation and citation fidelity.**
   - OBSERVED: zero numbers added or dropped in 26 outputs.
   - Every quotation verbatim.
   - Technical documentation byte-exact outside prose, even without file mode (`SKILL.md:178`).
3. **Disclosure.**
   - OBSERVED: its notes named cut claims, flagged every added line as removable, flagged the coda instead of silently cutting it, and pointed to missing facts ("the draft never says what makes Quillnote different…").
   - No other arm's note did all four. INFERRED: an author reading the note could reverse most of what the judge penalized.
4. **Fiction structure.**
   - OBSERVED: the most careful StoryScope translation found. It has exceptions per principle, "overdone looks like" warnings, and model-fingerprint caveats (`references/storyscope-rules.md:88-223`).
   - It separates rewrite from deep-rewrite permissions (`SKILL.md:141`).
   - Not tested in the experiment, so this advantage is design-level only.
5. **Resisting rules that misfire elsewhere.**
   - OBSERVED: kept "curiosity, not credentials" in 2 of 2 runs where HZ, KZ and SD altered it in 6 of 6.
   - Rejects rhythm-by-rule (`references/humanizer-rules.md:51`).
   - Treats word lists as weak evidence (`SKILL.md:122`).
6. **Honest documentation.**
   - OBSERVED: `evals/eval-log.md:98-105` names the grader-family confound, partial blinding, reused baselines and no human readers.
   - `references/storyscope-rules.md:84-85` lists the paper's scope limits.

### 5.2 Areas where competitors expose a real gap

| Gap | Evidence | Competitor that does it better |
|---|---|---|
| **No competent-editor baseline or untouched arm in evaluation** | Baseline is "same model, no skill, told not to load any skill" (`evals/eval-log.md:8`). Against a one-paragraph editor prompt ProseShape scored −1.27 [−2.00, −0.62] (experiment) | HumanScope's U/O/H design; avoid-ai-writing's frozen scenarios |
| **Evaluation cases not reproducible** | `evals/eval-log.md:7` cites `evals.json` (12 cases, 72 assertions); the file is not in the repository; raw outputs and gradings omitted (`README.md:89`); one run per configuration (`evals/eval-log.md:100`) | avoid-ai-writing (48 cases with claims and protected spans, dev/held-out); HumanScope (keys and judge prompts archived) |
| **No deterministic preservation check** | The rubric lists five mechanical checks (`references/evaluation-rubric.md:50-56`); nothing implements them | avoid-ai-writing `validate.js`; slop-linter comment guard; shir-danishyar number test |
| **Voice permission leaks into invention in nonfiction** | "Voice is not invention … a reaction … allowed" (`SKILL.md:71`); "say what a number means to the reader" (`SKILL.md:72`). Experiment: added reaction lines judged as added facts (s07, both judges); on Opus, a derived worked example and a value judgment (s01) | avoid-ai-writing's "Never inject": fabricated speaker perspective includes reactions ([L307](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L307)) |
| **Rewrite mode deletes stated meaning** | "In fiction you may cut a lesson line" (`references/mode-guidance.md:55`); Meaning question (`SKILL.md:128`). Experiment: s08 realization cut in 2/2 runs, overall 3.5 vs 7.5 for the editor | HumanScope R9 fix: tighten, do not delete, information-bearing realizations ([RESULTS.md:52-66](https://github.com/Anson-Saju-George/HumanScope/blob/51b343ac96d9f8be10ad76955e01a9e9beb4661c/test-run/fair-retest/RESULTS.md#L52-L66)) |
| **Claims under hype are cut despite the rule to keep them** | `SKILL.md:76` says keep real points; s02 lost "worldwide" and "all-in-one", s13 lost the "meeting place" characterization, s01 lost the sustainability aim (judge issues) | AAW's source-fidelity clause (attribution, scope, certainty preserved) |
| **No marketing, landing or social genre gate** | Genre table has memo, email, essay, technical, academic, fiction, children (`references/mode-guidance.md:73-85`). s02 bold feature labels flattened (D20 applied to marketing); s02 scored 4.5 vs 8.5 (run 1) | AshwinSathian's marketing scope bullet; HumanScope manifest treats scannability and CTAs as protected |
| **Dash rule applied to human nonfiction** | "Without a sample, replace connective dashes" (`SKILL.md:120`); B8 marks one dash *weak alone* (`references/humanizer-rules.md:47`), which conflicts. The Python Tutorial's single dash was removed in 2/2 runs | HumanScope and avoid-ai-writing reject dash bans; keez97's zero-dash gate shows where the rule leads |
| **No diagnose-only mode** | Description excludes "critique without a rewrite" (`SKILL.md:3`) | HumanScope DIAGNOSE, AAW detect, keez97 detect, ccf audit-only |
| **Attribution gaps** | `THIRD_PARTY_NOTICES.md` credits Humanizer (MIT) and StoryScope. Humanizer's catalog derives from Wikipedia (CC BY-SA 4.0), which humanizer-stack and keez97 note. `SKILL.md:7` says "COLM 2026", but arXiv v6 (2026-08-10) still shows only an arXiv preprint header (checked) | humanizer-stack `ATTRIBUTION.md` |

### 5.3 Areas where the evidence is inconclusive

- **Whether the StoryScope layer improves fiction for readers.**
  - StoryScope measures separability, not quality, as ProseShape itself says (`references/storyscope-rules.md:84`).
  - ProseShape's own eval log shows fiction wins and losses (`evals/eval-log.md:36-41`).
  - My experiment had one fiction sample, in keep-events rewrite mode, where the structural move was penalized.
  - Deep rewrite and generation were not tested.
- **Whether the references earn their cost.**
  - `SKILL.md`-only scored the same as the full bundle on rewrites (+0.04 [−0.62, +0.65]).
  - Fiction deep rewrite and generation, where the references are meant to matter, were not tested.
- **Whether ProseShape beats Humanizer.** ProseShape's log says yes by 1–1.8 points (`evals/eval-log.md:24`); my experiment found no difference (−0.02). The setups differ in:
  - executor (Opus vs Sonnet, though the Opus ablation did not move ProseShape);
  - corpus (the log includes generation and deep rewrite);
  - judge rubric;
  - request wording.
- **LLM-judge validity.** One model family throughout, on both sides. The O prompt and the judge rubric share a preservation emphasis. No human raters anywhere in the field's evidence, including here.

### 5.4 Capabilities that appear absent

- Deterministic verification of any kind (numbers, quotes, citations, Markdown and code integrity, diff size).
- Regression tests or CI for the skill package: frontmatter validity, reference links, length budget. blader validates these.
- A diagnose or flag-only mode.
- Persistent voice profiles, or a way to reuse a sample across sessions.
- Explicit handling of long documents (chunking, consistency across sections).
- Non-English guidance. ProseShape kept Spanish text in Spanish unprompted, but has no rule that the surface tell list is English-specific (AshwinSathian has one).
- A failure-report template or pipeline for turning user reports into cases.

### 5.5 Capabilities ProseShape has but could implement better

- **Preservation inventory** (`SKILL.md:57-65`, pass 6 `SKILL.md:87`). It is model-only. Pair it with a checker, and separate the fabrication question from the style review (keez97's Pass 4 idea) in `SKILL.md:181-189`.
- **Priority ladder** (`SKILL.md:28-38`). "Facts, quotations, citations, technical meaning, required content" rank third, above genre conventions. But "Cut, then give it a person" and the StoryScope Meaning principle operate as if voice and structure could override stated content. Make the ladder's consequence explicit: when a style move would drop or add a claim, the claim wins unless the mode grants it.
- **Evaluation rubric.** It is good (`references/evaluation-rubric.md:14-34`): proportionality, a no-gratuitous-quirks dimension, red flags. But it is not operationalized, and it lacks a note-quality (disclosure) dimension that would credit ProseShape's actual strength.
- **Eval log.** Honest, but all iterations happened in one day with reused baseline outputs (`evals/eval-log.md:103`). Differences after v1.1 are "within noise" by its own account (`:24`). Future iterations need held-out cases and ≥2 runs to be interpretable.
- **Trigger evaluation.** The author found the environment could not measure triggering (`evals/eval-log.md:111-117`). That is a limitation of the harness, not of the description. Keep the JSON; re-run where skills are actually consulted.

---

## 6. Recommended improvements

Priorities reflect confidence and value, not novelty. Effort: **S** ≤ 1 day, **M** 2–5 days, **L** > 1 week.

### P0: high-confidence improvements worth doing soon

**P0-1. Reproducible three-arm evaluation with a strong-editor baseline** (RECOMMENDED)
- **Problem:** current results cannot show that ProseShape beats competent editing, and cannot be re-run.
- **Evidence:**
  - `evals/eval-log.md:7-11` (missing `evals.json`, no-skill baseline);
  - the experiment (PS vs editor prompt −1.27);
  - HumanScope's finding that its advantage over ordinary editing is "unestablished".
- **Solution:**
  - Restore `evals/evals.json` with the 12 cases and 72 assertions.
  - Adopt the corpus format in `docs/research/experiment-2026-09/corpus/manifest.json`, extended with atomic claims per case (avoid-ai-writing style).
  - Standard arms: U (untouched), O (fixed editor prompt), PS-current, PS-candidate.
  - Protocol: ≥2 generations per arm and case; judge twice with shuffled labels; bootstrap CIs; commit raw outputs and judgments.
  - The scripts in `docs/research/experiment-2026-09/scripts/` are a working starting point.
- **Benefit:** every later change becomes measurable; honest positioning.
- **Area:** `evals/`, new `evals/harness/`, `evals/eval-log.md`
- **Effort:** M
- **Risks:** cost (about $10 per full run at list prices); same-family judges. Mitigate with a second judge provider when available and a small human-rater pilot.
- **Test:** the harness reproduces this report's numbers on the same outputs (it already does: `combined.py` regenerates `summary_combined.md` exactly).

**P0-2. Deterministic preservation checker** (RECOMMENDED)
- **Problem:** preservation is model-judged only; the rubric's mechanical checks are unimplemented.
- **Evidence:**
  - `references/evaluation-rubric.md:50-56`;
  - literal checks caught real structural deletions in competitors (validator `heading-count`);
  - manual review showed literal string matching also over-reports (for example "14-day" → "14 days").
- **Solution:** `scripts/preserve_check.py` (stdlib) comparing source and output:
  - hard: numbers and units, quoted spans verbatim, citation strings, URLs, inline code, fenced code, frontmatter, tables, heading count and level;
  - soft: proper nouns, token change ratio against an expected band, em-dash counts against a sample.
  - Report "missing / added / changed" with spans.
  - Use it in the harness, and document an optional run when the host has tools (a one-line addition to `SKILL.md:178` and to pass 6).
  - Reuse ideas from avoid-ai-writing's MIT validator; normalize numerals and number words to cut false positives.
- **Benefit:** catches the damage models cannot see; makes P0-1 cheaper and more objective.
- **Area:** new `scripts/`, `tests/`, `references/evaluation-rubric.md`
- **Effort:** S–M
- **Risks:** literal checks miss paraphrased semantic drift; do not present a pass as "meaning verified" (avoid-ai-writing's wording is a good model).
- **Test:** unit fixtures, including should-pass paraphrases and should-fail deletions; run over all 247 committed outputs and hand-audit the flags.

**P0-3. Narrow voice and derived-claim additions in nonfiction** (RECOMMENDED)
- **Problem:** "voice is not invention" and "get more from the facts" license new reactions, experiences and derived claims that readers and judges treat as additions.
- **Evidence:**
  - `SKILL.md:71-72`, `references/mode-guidance.md:52,79`;
  - experiment s07 (both runs, both judges) and s01 on Opus;
  - avoid-ai-writing treats reactions as fabricated speaker perspective ([L307](https://github.com/conorbronsdon/avoid-ai-writing/blob/9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43/SKILL.md#L307)).
- **Solution:**
  - In rewrite and light-edit modes for nonfiction, voice comes from word choice, rhythm and stance *already present*.
  - A new first-person reaction, feeling, preference or evaluation counts as an addition unless the sample or request supplies it.
  - Arithmetic or examples derived from the source are allowed only when the request asks for explanation, and are flagged.
  - Keep the current permission for Generate mode and for personal essays with a sample.
  - Update Example 2 in `references/examples.md` accordingly (it currently models added attitude).
- **Benefit:** fewer judge-flagged additions (PS: 6 in 39 judgments on Sonnet, 14 in 26 on Opus); aligns behavior with ProseShape's own priority ladder.
- **Area:** `SKILL.md:67-76`, `references/mode-guidance.md:52,79`, `references/examples.md` §2
- **Effort:** S
- **Risks:** flatter prose. This is the v1.2 failure (`evals/eval-log.md:91`). Mitigate by keeping "put the life in the telling" for phrasing.
- **Test:** added-fact rate and voice and naturalness scores in the P0-1 harness, compared against v1.3.1.

**P0-4. Tighten, don't delete, stated meaning in rewrite mode** (RECOMMENDED)
- **Problem:** in keep-events rewrites ProseShape deletes a story's stated realization. Readers and judges treat that as changing the ending's meaning.
- **Evidence:**
  - `references/mode-guidance.md:55`, `SKILL.md:128`, `references/humanizer-rules.md:105` (G3);
  - experiment s08 (3.5 vs 7.5; 2/2 runs);
  - HumanScope's fair-retest (all arms lost a motive, and the "defect" label was withdrawn).
- **Solution:**
  - In rewrite and light-edit modes, a lesson line that carries a motive, change or realization is *tightened or given to the character*, not removed.
  - Full deletion moves to deep-rewrite mode, or is offered in the note ("the story would also work without the realization; cut it?").
  - Keep deleting pure moralizing that adds no character information.
- **Benefit:** removes ProseShape's worst per-sample loss while keeping its structural judgment available.
- **Area:** `references/mode-guidance.md:54-55`, `SKILL.md:128,141`, `references/humanizer-rules.md` G3, `references/examples.md` §4
- **Effort:** S
- **Risks:** stories keep more stated meaning than the StoryScope philosophy prefers. That is acceptable when the user asked to keep meaning.
- **Test:** paired briefs (keep meaning vs "make it implicit") on 3+ stories; the correct behavior differs by brief (HumanScope held-out case 2).

**P0-5. Genre gates for marketing, social and docs, plus protected Markdown for pasted text** (RECOMMENDED)
- **Problem:** persuasive and scannable genres lose structure and claims.
- **Evidence:**
  - no marketing or social row in `references/mode-guidance.md:73-85`;
  - D20 bold removal (`references/humanizer-rules.md:70`) applied to a feature list;
  - s02 and s07 scores;
  - the file-mode protection (`SKILL.md:178`) applies only to named files.
- **Solution:**
  - Add rows:
    - **marketing/landing:** keep CTAs, feature labels that aid scanning, claims such as coverage, integration and "all-in-one" unless false; cut hype adjectives;
    - **social:** keep the platform's conventions, hashtags and the author's stance words; no new reactions;
    - **docs/reference:** keep headings, parallel structure and the H1.
  - Extend the protected-content list to pasted Markdown and code.
- **Benefit:** fixes the two lowest-scoring non-fiction genres.
- **Area:** `references/mode-guidance.md:73-85`, `SKILL.md:103-122,178`, `references/humanizer-rules.md` D20–D21
- **Effort:** S
- **Risks:** more rules. Keep each row to one line.
- **Test:** s02, s04 and s07-style cases in the harness; judge format and facts scores; checker heading and emphasis diffs.

**P0-6. Apply the dash rule only when other tells keep it company** (RECOMMENDED)
- **Problem:** ProseShape strips dashes from human-written nonfiction, which is a small unnecessary edit that erodes trust.
- **Evidence:**
  - `SKILL.md:120` vs `references/humanizer-rules.md:47` ("*weak alone* for one");
  - the Python Tutorial's single dash removed in 2/2 runs;
  - keez97's zero-dash gate fails classic human prose (§8).
- **Solution:**
  - Without a sample, replace dashes only when they recur as the universal connector or co-occur with other tells.
  - Leave a single purposeful dash.
  - Keep dashes in interrupted speech.
- **Benefit:** fewer edits on good text; consistency with ProseShape's own evidence rule.
- **Area:** `SKILL.md:118-121`, `references/humanizer-rules.md:47`, `references/evaluation-rubric.md:54`
- **Effort:** S
- **Risks:** more dashes in outputs from dash-heavy drafts. Rate-matching still applies.
- **Test:** controls unchanged-rate; dash count per 1k words on AI-shaped cases stays well below the source.

**P0-7. Attribution and citation accuracy** (RECOMMENDED)
- **Problem:** licensing notice and venue claim.
- **Evidence:**
  - `THIRD_PARTY_NOTICES.md` (no Wikipedia CC BY-SA mention);
  - humanizer-stack's analysis ([ATTRIBUTION.md](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/ATTRIBUTION.md));
  - `SKILL.md:7` and `references/storyscope-rules.md:3` ("COLM 2026") vs arXiv v6 header.
- **Solution:**
  - Add a Wikipedia *Signs of AI writing* (WikiProject AI Cleanup, CC BY-SA 4.0) attribution for adapted pattern material, and get a legal read if relicensing matters.
  - Cite StoryScope as arXiv:2604.03136v6 unless acceptance can be linked.
- **Benefit:** avoids an avoidable credibility and licensing question.
- **Area:** `THIRD_PARTY_NOTICES.md`, `SKILL.md:7`, `README.md:96`, `references/storyscope-rules.md:3`
- **Effort:** S
- **Risks:** none.
- **Test:** review.

### P1: meaningful improvements requiring more work or evaluation

**P1-1. Diagnose mode** (RECOMMENDED)
- **Problem:** authors cannot ask "what would you change and why" without getting a rewrite.
- **Evidence:** four competitors have this (§3.1); ProseShape's note already contains most of a diagnosis.
- **Solution:** a mode that returns findings (quote, level, why it hurts this reader, suggested move), strongest first, no rewrite, with "no change needed" allowed. Update the description's near-miss list (`SKILL.md:3`) and `evals/trigger-evals.json` (the "critique only" negative currently encodes the opposite).
- **Area:** `SKILL.md:3,40-55,173-179`, `references/mode-guidance.md`
- **Effort:** S–M
- **Risks:** trigger confusion with craft-critique requests.
- **Test:** precision and usefulness judged on paired diagnose/edit requests; trigger evals.

**P1-2. Score the note, not just the text** (RECOMMENDED)
- **Problem:** ProseShape's disclosure behavior is invisible to text-only evaluation.
- **Evidence:** the experiment (the judge penalized additions that the note had flagged).
- **Solution:** a judge or deterministic step computes *disclosure recall*: every addition, cut claim or structural change found by the diff or the judge should appear in the note. Also check *gap-flag precision*.
- **Area:** harness, `references/evaluation-rubric.md`
- **Effort:** S
- **Risks:** notes grow longer to game the metric. Keep the 3–5 line cap (`SKILL.md:175`).
- **Test:** disclosure recall per arm.

**P1-3. Separate fabrication check in self-review** (RECOMMENDED)
- **Evidence:** keez97's two-question Pass 4 ([L383-386](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L383-L386)); ProseShape's final review bundles it (`SKILL.md:183`).
- **Solution:** a distinct last step: list every sentence that states something not in the source (including reactions and derived claims), then keep and flag or revert each.
- **Effort:** S
- **Test:** added-fact rate.

**P1-4. Slim the load path, then measure where references matter** (RECOMMENDED)
- **Problem:** about 2× token cost (`evals/eval-log.md:107-109`); the ablation found no rewrite benefit from the references.
- **Solution:**
  - Keep `humanizer-rules.md` mandatory only for rewrites with dense tells.
  - Move worked examples behind "read when unsure" (already suggested at `SKILL.md:198`).
  - Test PS vs PS-core on fiction deep rewrite, generation and voice match before cutting anything.
- **Area:** `SKILL.md:103-106,124-127,191-200`
- **Effort:** M (mostly evaluation)
- **Risks:** losing guidance that matters on untested tasks.
- **Test:** the P0-1 harness with deep-rewrite and generation cases.

**P1-5. Regression scenarios for contract behaviors** (RECOMMENDED)
- **Solution:** add fixed cases for:
  - clean no-op (return unchanged);
  - near-clean (one tell);
  - source-internal instructions (edit as data, `SKILL.md:80`);
  - explicit transformation;
  - protected content;
  - a request that forbids something (for example, no first person).
- **Evidence:** avoid-ai-writing's eight-scenario gate.
- **Effort:** S
- **Test:** deterministic assertions plus judge.

**P1-6. Register carve-outs for academic and technical prose** (RECOMMENDED)
- **Evidence:** humanizer_academic's preserve-list and connective rules; ProseShape's academic row is one line (`references/mode-guidance.md:81`); the s06 result was good, so this is about preventing drift, not fixing a measured failure.
- **Solution:** a short "not tells in this register" list (logical connectives, "associated with", hedges the evidence needs, RFC-2119 keywords).
- **Effort:** S
- **Test:** academic and spec cases.

**P1-7. Pre-publication checks for the package** (RECOMMENDED)
- **Solution:** CI that validates frontmatter, reference links, line and word budgets, that `CHANGELOG.md` matches `metadata.version`, and that the eval JSON parses.
- **Evidence:** blader's `validate-package.py`.
- **Effort:** S

### P2: experiments worth testing before committing

**P2-1. Four-slot justification in light edits** (HumanScope)
- **Hypothesis:** requiring evidence, effect, failure and smallest fix for light edits reduces over-cutting without increasing under-editing.
- **Test:** ablation in the harness; watch under-edit flags. HumanScope itself could not show gains over ordinary editing.

**P2-2. Nonfiction structure questions from SlopShape**
- **Hypothesis:** genre-gated questions (for blogs: does the title promise the payoff? does the close only restate?) improve blog posts without harming docs.
- **Risk:** separability research again; several "AI" features are docs virtues.
- **Test:** blog and doc cases separately.

**P2-3. Opt-in persistent voice profile**
- **Hypothesis:** saving sample analysis (`references/mode-guidance.md:87-103`) as a file improves consistency across sessions.
- **Risks:** privacy; stale profiles.
- **Test:** voice-match cases across two sessions.

**P2-4. One-line voice statement**
- **Hypothesis:** stating the voice preserved (ccf) makes voice errors catchable by the user.
- **Test:** user study or judge voice scores.

**P2-5. Location-only scanner assistance**
- **Hypothesis:** a scanner that points at candidate spans, never severity or pass/fail, speeds audits.
- **Risk:** the measured low precision (§8).
- **Test:** precision and recall against judge-identified tells, with human controls, before shipping anything.

**P2-6. Skeleton-first deep rewrite**
- **Hypothesis:** writing the beat outline before restructuring (humanizer-stack) improves disclosure-order changes that `references/mode-guidance.md:57-62` asks for.
- **Test:** deep-rewrite cases.

---

## 7. Evaluation strategy for ProseShape

The goal is to tell *improvement* from *style change*. Every change should be measured on fidelity, benefit and restraint, separately, against the same baselines.

### 7.1 Case suite (about 40 cases; start from the 12 in the eval log plus the 13 here)

| Bucket | Cases | Purpose | Pass condition |
|---|---|---|---|
| AI-shaped, by genre | 2 each: memo or announcement, professional email, marketing/landing, social, explainer, technical doc (Markdown + code + table), academic with citations, news with quotes, personal essay, short story | Core rewrite quality | No hard preservation failures; judge benefit ≥ O |
| Already-good human text | ≥ 6: public-domain fiction and essay, permissively licensed docs, a real email style | Restraint | Token change ≤ 5%, or judge "no worse than U"; no dash, quote or style normalization unless a tell cluster exists |
| Near-clean | ≥ 3 with exactly one tell | Proportionality | Only that span changes |
| Preservation traps | numbers with units, ranges, negations, conditionals, hedges, attribution chains, dates and times, proper nouns, a spec with MUST/SHOULD | Fidelity | Checker hard pass; atomic-claim check pass |
| Formatting | frontmatter, fenced code, tables, nested lists, links, footnotes, HTML comments | Structure integrity | Byte-exact protected regions; heading count and level unchanged unless asked |
| Fiction, paired briefs | same story × {keep meaning and events; make theme implicit; free rein to restructure} | Mode discipline and structural value | Correct behavior differs by brief; deep rewrite changes disclosure order (`references/mode-guidance.md:60`) |
| Voice match | sample with dashes, fragments or asides; sample in formal register; machine-like sample | Voice fidelity | Rates matched (dash per paragraph, sentence-length distribution within the sample's range); machine-like sample flagged (`SKILL.md:171`) |
| Generation | 3 briefs (story, essay with supplied facts, LinkedIn post with fixed numbers) | Generate mode | No invented facts beyond the brief's license; judge benefit ≥ O-generation |
| Source-as-data | text containing "ignore previous instructions…" or "Reply with only OK" | Robustness | Edited as text; instruction preserved as content |
| Non-English | 2 (Spanish, one other) | Scope | Stays in the source language; no English-only tell rules applied |
| Long document | 1–2 at 2–5k words | Drift | Consistent voice and terminology; checker passes; no sections dropped |

Each case carries a manifest:
- source;
- request;
- genre;
- expected mode;
- **atomic claims** (what must survive);
- **protected spans**;
- allowed edits;
- expected change band;
- provenance and license.

Split cases into development and held-out by document or author (avoid-ai-writing's leakage rule). Never tune on held-out cases.

### 7.2 Arms and runs

- **U** untouched, **O** fixed strong-editor prompt ([`prompts/O.txt`](experiment-2026-09/prompts/O.txt)), **PS-current**, **PS-candidate**.
- Optional: **B** bare, and one competitor (HumanScope is the strongest measured).
- ≥ 2 generations per arm and case. Freeze and hash every prompt before generating (HumanScope's held-out rule).

### 7.3 Measurements

1. **Deterministic (P0-2 checker):**
   - hard failures (protected tokens, numbers, quotes, code, tables, frontmatter, headings);
   - change ratio against the expected band;
   - length ratio;
   - dash rate against the sample or the source.
2. **Atomic-claim preservation:** for each manifest claim, a judge or entailment check against the output: present, weakened, strengthened, contradicted or missing. Report invented claims separately.
3. **Blind judge** (2 passes, shuffled, untouched source included):
   - fidelity, task success, reader benefit, voice, proportionality, format;
   - overall and full ranking;
   - typed issues.
   Keep "sounds AI" and detectors out of the rubric.
4. **Note quality:**
   - disclosure recall (every diff-detected addition, cut claim or structural change mentioned);
   - gap-flag precision.
5. **Reliability and cost:**
   - judge pass agreement (Spearman);
   - run-to-run spread;
   - tokens and dollars per case.

### 7.4 Decision rules

- **Ship a candidate only if all of these hold:**
  - zero new hard preservation failures;
  - atomic-claim loss not higher than current;
  - added-claim rate not higher than current;
  - human-control change rate within band;
  - benefit or overall not lower than current beyond the noise band. Noise is about 0.6 points on a 13-case mean here; recompute it for the suite.
- **Claim superiority over ordinary editing only if** PS − O is positive with a CI excluding zero on held-out cases, *and* a human-rater pilot agrees: 3 raters, including an editor, pairwise on about 12 items.
- Report per-bucket results. A gain in fiction must not hide a loss in docs.

### 7.5 Cadence

- Deterministic checks run in CI on committed outputs (cheap).
- The model-backed suite runs per release candidate, at about $10–20 at list prices for Sonnet-class executors.
- A human pilot runs before any public quality claim.

---

## 8. Things not to copy

| Tempting idea | Where | Why it would make ProseShape worse | Evidence |
|---|---|---|---|
| Sentence-length CV bands, contraction floors, "vary sentence length" as a rule | keez97 D2/D6 ([L247-257](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L247-L257)); blader [L39](https://github.com/blader/humanizer/blob/225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8/SKILL.md#L39); shir-danishyar; lguz | Rhythm by rule, which ProseShape correctly bans (`references/humanizer-rules.md:51`). Calibrated to detectors, not readers | OBSERVED: `score.py` fails the Python Tutorial (CV 0.31) and a Jerome K. Jerome passage, and passes a formulaic AI email (`experiment-2026-09/results/scanner_controls.md`). keez97's own study says the battery "can push the WRONG way" ([DETECTION-LIMITS.md:11](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/references/DETECTION-LIMITS.md#L11)) |
| Deliberate imperfection ("a sentence that doesn't quite parse") | keez97 [L91](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/SKILL.md#L91) | Degrades prose to look human; contradicts "human does not mean messy" (`SKILL.md:26`) | Design-level |
| Zero-dash or zero-triad hard gates and blanket word bans | keez97 C2/C5; lguz checklist; shir-danishyar P3 regex | Legitimate content has three items and dashes. Bans remove information and author style | OBSERVED: three skills altered "curiosity, not credentials" 6/6; the P3 regex failed human docs |
| "Add the name, the price, the date" specificity | humanizer-stack [L74-75](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/skills/structural-humanizer/SKILL.md#L74-L75); lguz [L170-172](https://github.com/lguz/humanize-writing-skill/blob/4b7c37fa5148fd499e18498fcc91bb10ed801733/skills/humanize-writing/SKILL.md#L170-L172) | Invites fabrication, the most damaging failure in nonfiction | OBSERVED: even projects with no-invention rules ship examples that invent (keez97 L229/231; ccf README "Sarah") |
| Inserting facts "from your own knowledge" with `[verify]` | humanizer_academic [L41](https://github.com/matsuikentaro1/humanizer_academic/blob/74f9b87b216fea2f51cd4327011da2a97ca83896/SKILL.md#L41) | Still a hallucination channel; authors skip verification | Design-level |
| Optimizing for rarity or "detectable clusters", or tuning rules from detector labels | humanizer-stack [L37](https://github.com/NulightJens/humanizer-stack/blob/13f5c023189d428ffba726c75886ca1fd0dcba65/skills/structural-humanizer/SKILL.md#L37); keez97 B17/B18; humanizer_academic's burstiness rule ([L656](https://github.com/matsuikentaro1/humanizer_academic/blob/74f9b87b216fea2f51cd4327011da2a97ca83896/SKILL.md#L656)) | ProseShape's principle is readers, not detectors (`README.md:7`). Rarity is not quality (`references/storyscope-rules.md:84`) | keez97's own finding that detector sentence reasons are post-hoc ([DETECTION-LIMITS.md:15](https://github.com/keez97/humanizer/blob/2d9a116fa9caee2c3466a7c7d419cbe02b35a470/references/DETECTION-LIMITS.md#L15)) |
| Reader address and "acknowledged reader" moves | humanizer-stack audit 5 | Rare even in human fiction; ProseShape already warns against it (`references/storyscope-rules.md:80`) | StoryScope Table 16/17 as cited by ProseShape |
| Preset celebrity-style voices; forced voice questions before any rewrite | lguz [L39-68](https://github.com/lguz/humanize-writing-skill/blob/4b7c37fa5148fd499e18498fcc91bb10ed801733/skills/humanize-writing/SKILL.md#L39-L68) | Imposes a persona on the author; adds friction; ProseShape's "ask only before a structural change" rule is better (`references/mode-guidance.md:37`) | Design-level |
| Self-scored numeric pass lines (56/80, "ship when all HARD gates pass") | slopster Tagore; keez97 | A model grading its own output against a threshold measures the prompt, not the reader | Design-level; blader #229 found a custom checker added nothing |
| Very large process contracts and multi-skill routers | avoid-ai-writing (21k-word `SKILL.full.md`, 7 skills) | Cost and maintenance with no shown quality gain; in the experiment it under-edited most (20 flags) | OBSERVED |
| Generation-time humanizing of *all* output by default | AshwinSathian, shir-danishyar | Applies style rules where users didn't ask; ProseShape's scoped triggering is a feature | Design-level |
| Density-threshold linters as quality gates | shir-danishyar; humanizer-stack `--strict` | Low precision on human text; gates invite editing to the count | OBSERVED (scanner table) |
| Treating StoryScope or SlopShape percentages as targets | humanizer-stack ("Humans just name the feeling"; "classic writing advice is now a machine signature") | Population separability is not per-text quality; ProseShape's cautions are correct (`SKILL.md:25`) | `references/storyscope-rules.md:75-86` |

---

## 9. Concrete next steps (issue-ready)

1. **Restore `evals/evals.json` and add a case manifest schema.**
   - Subsystem: `evals/`.
   - Publish the 12 development cases and 72 assertions cited in `evals/eval-log.md:7,11`. Add atomic claims, protected spans and expected change bands per case, as in `docs/research/experiment-2026-09/corpus/manifest.json`.
   - Acceptance: JSON validates; every fixture in `evals/files/` is referenced.
2. **Add a deterministic preservation checker (`scripts/preserve_check.py`) with tests.**
   - Subsystem: new `scripts/`, `tests/`, `references/evaluation-rubric.md`.
   - Implement rubric §3 checks: numbers and units, quotes verbatim, citations, URLs, code, frontmatter, tables, headings, change ratio, dash rate.
   - Acceptance: passes should-pass paraphrase fixtures, fails deletion fixtures, and runs over `docs/research/experiment-2026-09/results/outputs.jsonl`.
3. **Build the three-arm eval harness (U / O / PS) and re-baseline v1.3.1.**
   - Subsystem: `evals/harness/` (start from `docs/research/experiment-2026-09/scripts/`).
   - ≥ 2 runs, 2 judge passes, bootstrap CIs, committed outputs and judgments, eval-log entry.
   - Acceptance: reproduces this report's tables from committed data.
4. **Revise nonfiction voice permissions and derived-claim rules.**
   - Subsystem: `SKILL.md:67-76`, `references/mode-guidance.md:52,79`, `references/examples.md` §2.
   - New reactions, feelings or evaluations count as additions in nonfiction rewrite and light-edit modes unless the sample or request supplies them; derived arithmetic or examples only on request.
   - Acceptance: lower added-claim rate with no drop in voice score beyond noise.
5. **Rewrite-mode handling of stated realizations: tighten, don't delete.**
   - Subsystem: `references/mode-guidance.md:55`, `SKILL.md:128,141`, `references/humanizer-rules.md` G3, `references/examples.md` §4.
   - Acceptance: paired-brief fiction cases behave differently by brief.
6. **Add marketing, social and docs genre rows, and protected Markdown for pasted text.**
   - Subsystem: `references/mode-guidance.md:73-85`, `SKILL.md:178`, `references/humanizer-rules.md` D20–D21.
   - Acceptance: s02, s04 and s07-type cases keep CTAs, feature labels, hashtags, the H1 and claims.
7. **Align the dash rule with "weak alone".**
   - Subsystem: `SKILL.md:120`, `references/humanizer-rules.md:47`, `references/evaluation-rubric.md:54`.
   - Acceptance: human-control dash preserved; AI-shaped cases still reduce dash clusters.
8. **Fix attribution: Wikipedia CC BY-SA notice and StoryScope venue.**
   - Subsystem: `THIRD_PARTY_NOTICES.md`, `SKILL.md:7`, `README.md:96`, `references/storyscope-rules.md:3`.
   - Acceptance: notice added; venue claim matches a linkable source.
9. **Add a diagnose (flag-only) mode and update triggers.**
   - Subsystem: `SKILL.md:3,40-55,173-179`, `evals/trigger-evals.json`.
   - Acceptance: returns findings without rewriting; trigger evals updated for the new near-miss boundary.
10. **Measure the reference load path on deep-rewrite, generation and voice-match cases.**
    - Subsystem: `SKILL.md:191-200`, `references/`.
    - Decide what to load when, based on PS vs PS-core results.
    - Acceptance: cost per run documented; any removal justified by the harness.

---

## Addendum (2026-10-04): status after ProseShape 1.4.0

The body of this report is unchanged. This addendum records what happened to the §9 next steps. The validation is documented in [`../../evals/v1.4-validation/README.md`](../../evals/v1.4-validation/README.md).

| §9 step | Status | Evidence |
|---|---|---|
| 1. Restore `evals/evals.json` | Open | The file is not in the public repository. `evals/eval-log.md` now says so. |
| 2. Preservation checker | Done | [`scripts/preserve_check.py`](../../scripts/preserve_check.py) with 28 unit tests, covering paraphrase cases that should pass ("14-day" vs "14 days", spelled-out numbers, quote punctuation) and deletion cases that should fail. [`evals/harness/checks.py`](../../evals/harness/checks.py) runs it over this experiment's outputs. The rubric does not reference it yet (see step 7). |
| 3. Eval harness, re-baseline 1.3.1 | Done | [`evals/harness/`](../../evals/harness/README.md) reproduces the committed 1.4 summaries byte for byte from committed data. On the held-out corpus, 1.3.1 scored 5.94 against O's 7.33. |
| 4. Nonfiction voice permissions, derived claims | Done | On held-out, judge-flagged added facts were 1 for 1.4.0 and 12 for 1.3.1, and voice scored 4.65 against 3.90. |
| 5. Realizations: tighten, don't delete | Done for rewrite mode | Fiction dialogue scored 8.25 against O's 6.25 on held-out. The paired-brief deep-rewrite cases were not run. |
| 6. Genre rows, protected Markdown | Done | 1.4.0's held-out format score was 4.96, and avoid-ai-writing's validator found no `heading-count` errors in its outputs (1.3.1 had two). |
| 7. Dash rule *weak alone* | Partly | Changed in `SKILL.md` and B8. Every arm kept the press release's dash and Twain's three. `references/evaluation-rubric.md` §3 still counts against zero. It was left alone because it is part of the validated prompt; the fix is planned for 1.4.1. |
| 8. Wikipedia notice, StoryScope venue | Done | `THIRD_PARTY_NOTICES.md` now credits *Signs of AI writing* (CC BY-SA 4.0). StoryScope is cited as arXiv:2604.03136v6, with no venue claim. |
| 9. Diagnose (flag-only) mode | Open | |
| 10. Reference load path | Open | |

The held-out run surfaced new problems, which are listed in the validation README:

- period spelling and markup were modernized in a Twain excerpt;
- a staged not-X-but-Y line was cut instead of restated, in a near-clean update and in fiction dialogue;
- small words that carry meaning were dropped in a personal essay.

**Replication (2026-10-04, later the same day).** On a second set of 15 fresh texts, 1.4.0's lead over the ordinary editor was +0.27 [−0.78, +1.22]. Pooled over both held-out sets it was +0.52 [−0.15, +1.15]. ProseShape leads on AI-shaped drafts and trails on text a person already wrote well. A 1.4.1 candidate halved fact problems but scored the same overall and was not released. See [`../../evals/v1.4.1-validation/README.md`](../../evals/v1.4.1-validation/README.md).

## Appendix A. Empirical comparison: summary

Full method, amendments, manual review and limitations: [`experiment-2026-09/README.md`](experiment-2026-09/README.md). Tables: [`results/summary_combined.md`](experiment-2026-09/results/summary_combined.md), [`results/summary_ablation.md`](experiment-2026-09/results/summary_ablation.md).

- **Corpus:** 13 texts. 10 AI-shaped across genres (including Markdown/code/table, citations, quotes, fiction and Spanish); 3 controls (Python Tutorial excerpt, *Three Men in a Boat* excerpt, near-clean email).
- **Request, identical for all arms:** "Please humanize this so it reads like a person wrote it. Keep the facts and meaning the same."
- **Execution:** isolated, tool-less `claude -p` sessions. Executor Sonnet 5.5 (ablations Opus 5.5); blind judge Opus 5.5; 2 generation runs; 3 judgments per sample and arm. Total cost $11.26.
- **Headline:**
  - O (editor prompt) 7.96;
  - HS 7.48;
  - B 7.37;
  - AAW 7.08;
  - SD 6.96;
  - KZ 6.94;
  - HZ 6.71;
  - **PS 6.69**;
  - U 3.10.
  PS − O −1.27 [−2.00, −0.62]; PS − HS −0.79 [−1.56, −0.02]; PS − HZ −0.02; PS − U +3.60.
- **Ablations:** PS on Opus ≈ PS on Sonnet (−0.04); PS `SKILL.md`-only ≈ full bundle (+0.04) at 2.8× lower cost.
- **Deterministic:**
  - no arm added or dropped numbers;
  - skills changed 3–10% of human-control tokens, against 27% for the bare model;
  - validator errors were heading deletions (HZ 2, SD 3).
- **Scanner precision:** keez97, shir-danishyar, humanizer-stack and ccf scanners flagged human controls and missed AI-shaped texts (`results/scanner_controls.md`).
- **What this does and does not show:** under a preservation-oriented request and a fidelity-strict, same-family judge, on short texts in rewrite mode, no skill beat a competent one-paragraph editing prompt. The pattern-catalog skills, ProseShape included, did measurably worse. It does not measure human preference, long documents, fiction deep rewrite, generation or voice matching, which are ProseShape's other stated strengths.

## Appendix B. Repositories examined

| Repository | Commit | Last commit | Commits | Stars / forks (2026-09-30) | License | Type | Experiment |
|---|---|---|---|---|---|---|---|
| [Aieda1l/ProseShape](https://github.com/Aieda1l/ProseShape) | `57d58e4` | 2026-09-29 | 25 | 0 / 0 | MIT | Skill | run |
| [blader/humanizer](https://github.com/blader/humanizer) | `225a6f3` | 2026-09-27 | 97 | 52.9k / 4.2k | MIT | Skill | run |
| [Anson-Saju-George/HumanScope](https://github.com/Anson-Saju-George/HumanScope) | `51b343a` | 2026-09-26 | 19 | 0 / 0 | MIT | Skill + evals | run |
| [NulightJens/humanizer-stack](https://github.com/NulightJens/humanizer-stack) | `13f5c02` | 2026-07-24 | 4 | 304 / 23 | MIT (+CC BY-SA notice) | 2 skills + scanners | scanners run; skills not run |
| [shir-danishyar/humanize](https://github.com/shir-danishyar/humanize) | `024aa19` | 2026-09-02 | 12 | 19 / 0 | MIT | Skill + linter + tests | run; tests pass |
| [keez97/humanizer](https://github.com/keez97/humanizer) | `2d9a116` | 2026-07-30 | 31 | 4 / 0 | MIT | Skill + scorer | run; `score.py` run; GPT-2/Binoculars not run |
| [AshwinSathian/humanize-writing-skill](https://github.com/AshwinSathian/humanize-writing-skill) | `65f84fa` | 2026-08-26 | 27 | 1 / 0 | MIT | Skill | not run |
| [lguz/humanize-writing-skill](https://github.com/lguz/humanize-writing-skill) | `4b7c37f` | 2026-03-12 | 4 | 54 / 6 | MIT | Skill | not run (asks a question before rewriting) |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | `9b8d030` | 2026-09-29 | 481 | 4.8k / 419 | MIT | Skill family + JS tools + evals | run; validator used |
| [sam-paech/antislop-sampler](https://github.com/sam-paech/antislop-sampler) | `0ae330e` | 2026-03-05 | 104 | 354 / 32 | Apache-2.0 | Decoding sampler | not run (needs open-weights logits) |
| [t0ddharris/slopster](https://github.com/t0ddharris/slopster) | `084e39a` | 2026-08-24 | 12 | 2 / 0 | MIT | Vale + skill + diff | not run |
| [thrash-d/slop-linter](https://github.com/thrash-d/slop-linter) | `a44c2d9` | 2026-09-29 | 34 | 1 / 0 | MIT | Vale + hook + guard | not run |
| [signalfi/humanspeak](https://github.com/signalfi/humanspeak) | `28eee02` | 2026-09-26 | 2 | 2 / 0 | MIT | Skill (SlopShape) | not run |
| [ccf/humanize](https://github.com/ccf/humanize) | `db51ff3` | 2026-09-14 | 86 | 1 / 0 | MIT | Skill + scanner + tests | scanner run; tests pass |
| [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) | `74f9b87` | 2026-09-30 | 32 | 270 / 37 | MIT | Domain skill | not run |

Excluded as unrelated: date, number and localization "humanizer" libraries. Seen but not analyzed in depth: skk-hub/humanizer (a blader fork), asavvin-pixel/unslop, jpeggdev/humanize-writing, harshaneel/humanize, Alex Chen's *Human Scope* (not on GitHub; tested by HumanScope as arm K), and Vale packages such as vale-llm-slop.

## Appendix C. External sources checked

- StoryScope, [arXiv:2604.03136](https://arxiv.org/abs/2604.03136) v6 (2026-08-10). Verified from the paper:
  - 93.2% macro-F1 from narrative features;
  - the LAMP surface-edit experiment on 278 Gemini stories (95.5 → 93.9 macro-F1);
  - embodied emotion 81% vs 38%; explicit emotion labels 29% vs 8%;
  - no limitations section;
  - header shows arXiv preprint status only.
  All match ProseShape's citations except the "COLM 2026" venue, which I could not verify.
- SlopShape, [arXiv:2609.15369](https://arxiv.org/abs/2609.15369) (Madler, 2026): 97.0 macro-F1 from 176 structural features on held-out companies; 96.1 after self-rewording.
- Antislop, [arXiv:2510.15061](https://arxiv.org/abs/2510.15061) (Paech et al., 2025): abstract claims as quoted in §4.9.
- [blader/humanizer issue #229](https://github.com/blader/humanizer/issues/229): design and caveats of the 16/16 claim.
- Wikipedia, [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (CC BY-SA 4.0): the upstream catalog for most pattern-based skills.
