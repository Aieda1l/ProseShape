# Evaluation harness

The scripts used to develop and validate ProseShape 1.4.0 through 1.4.2. They reproduce the setup of the [2026-09 comparison](../../docs/research/experiment-2026-09/README.md): the same request, executor, judge rubric and isolation flags, so new results can be compared with the committed ones.

Everything the scripts write goes to `work/` (gitignored; set `PROSESHAPE_WORK` to move it). Running models needs the `claude` CLI, logged in. Analysis and checks need only Python 3.8+.

| Script | What it does |
|---|---|
| `build_arm.py NAME [--rev REV]` | Inlines `SKILL.md` and the five runtime references from `plugins/proseshape/skills/proseshape/` (or from the repository root, for commits before the plugin layout) into one system prompt, `work/arms/NAME.txt`, and prints its size and SHA-256 prefix. It also copies the O (ordinary editor) and B (bare) prompts. It refuses to overwrite an arm with different content, so a name always means one prompt. |
| `run_arm.py ARM SAMPLE RUN --corpus C` | Runs one isolated, tool-less `claude -p` session (default executor `claude-sonnet-5-5`) and saves the reply and the text between `<<<FINAL>>>` and `<<<END>>>`. |
| `judge.py SAMPLE RUN PASS --arms "..." --tag T` | One blind pass (default judge `claude-opus-5-5`; `--model` picks another, as the 1.4.2 second judge did). The judge sees the request, the original, and every arm's text in a seeded shuffle, with the untouched source (U) among them. |
| `analyze.py TAG ARM [--details]` | Prints per-arm scores with bootstrap CIs, paired differences against `ARM`, per-sample scores, and issue counts. |
| `checks.py --corpus C --arms ...` | Runs [`scripts/preserve_check.py`](../../scripts/preserve_check.py) on every output: numbers, quotations, code, links, frontmatter, headings, and length. |
| `seed.py` | Unpacks the committed outputs and judgments into `work/` so baselines need not be regenerated. |
| `iterate.sh ARM TAG CORPUS` | One full iteration: build, generate 2 runs, judge 2 passes per run, analyze, check. |

Corpora: `dev` is the 13-sample 2026-09 corpus (`docs/research/experiment-2026-09/corpus/`). `heldout` is the 12-sample corpus frozen for 1.4.0 (`evals/heldout/`), and `heldout2` is the 15-sample corpus frozen for 1.4.1 (`evals/heldout2/`). Both have been used for validation, so treat them as development data. `heldout3` is the 16-sample corpus frozen for 1.4.2 (`evals/heldout3/`), weighted toward human and near-clean writing. All three have now been used for validation, so treat them as development data. Each has its own `SHA256SUMS`. Freeze a new corpus before the next round. You can also pass any directory of `<sample>.md` files.

## Reproduce the committed tables without model calls

```bash
cd evals/harness
python3 seed.py
python3 analyze.py _ho PS14g    # identical to ../v1.4-validation/results/summary_ho.md
python3 analyze.py _it7 PS14g   # identical to ../v1.4-validation/results/summary_it7.md
python3 analyze.py _ho3 PS142c  # identical to ../v1.4.2-validation/results/summary_ho3.md
python3 checks.py --corpus heldout --arms O PS HS PS14g --show
```

## Rebuild the exact arm prompts

```bash
python3 build_arm.py PS14g --rev a32e244                      # 94909 bytes, f8f69d4fa85aeb3c (ProseShape 1.4.0)
python3 build_arm.py PS --rev 57d58e4 --blank-lines 2         # 84096 bytes, 68f2520c6a1b4312 (1.3.1, as run in 2026-09)
python3 build_arm.py PSc --rev 57d58e4 --blank-lines 2 --skill-only   # 426df8696068c4f9
python3 build_arm.py PS141b --rev 5ada957                     # 97061 bytes, a573b93257d1122b (1.4.1 candidate)
python3 build_arm.py PS142c --rev a1d5cee                     # 99717 bytes, 1e9eac4c105993ff (ProseShape 1.4.2)
```

The 1.4 iterations put one blank line between the wrapper paragraph and the first file, and the 2026-09 experiment put two. That one byte is the only difference in how the two experiments built prompts. HumanScope and the other competitor arms are rebuilt from pinned clones by [`docs/research/experiment-2026-09/scripts/build_arms.py`](../../docs/research/experiment-2026-09/scripts/build_arms.py) (`ARMS_OUT=evals/harness/work/arms`).

## Test a change to the skill

```bash
python3 seed.py                       # baselines: O, PS 1.3.1 and HS on both corpora
./iterate.sh PSnext _next dev         # about $3.60 per iteration at list prices ($1.15 generation, $2.45 judging)
```

Iterate on `dev` only. Run `heldout` once, on the version you intend to ship, and report that number whatever it is. If the held-out corpus is used to choose between versions, it stops being held out: freeze a new one before the next round (write it, commit it with `SHA256SUMS`, then edit the skill).

Rules of thumb from the 1.4 work:

- Re-judging identical outputs moves an arm's 13-sample mean by up to about 0.3 points (O ranged from 7.90 to 8.21 across seven rounds with the same outputs). Treat smaller differences as noise.
- Read the `--details` issue list before changing anything. Most gains came from fixing a specific, repeated failure the judge described, not from reacting to the overall score.
- A version that wins `dev` by a small margin can lose `heldout`, and the reverse can happen too. The CI on the paired difference is the number to quote.
