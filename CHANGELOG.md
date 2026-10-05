# Changelog

## OpenAI upload package (2026-10-05)

- `scripts/package_skill.py` also builds `proseshape-openai-<version>.zip`, the package OpenAI's plugin directory takes as an upload. It contains the plugin folder's contents with `plugin.json` at the root, and leaves out the Claude-only `.claude-plugin/`.
- ZIP member names are checked and always use forward slashes. A ZIP made by hand on Windows writes backslashes, such as `.claude-plugin\plugin.json`, which OpenAI rejects as an unsafe path.
- The release workflow attaches both zips to every GitHub release.
- OpenAI takes ZIP uploads only and doesn't follow GitHub, so each new version is uploaded again. `docs/publishing.md` covers this.
- Two new tests bring the total to 45.

## Icon (2026-10-04)

ProseShape has an icon: a pilcrow (¶), the mark for a paragraph, set in Instrument Serif. Its bowl is filled in the banner's terracotta, standing for prose with one deliberate choice in it. It replaces the earlier "Ps" monogram, which could be mistaken for another product's icon.

- `plugins/proseshape/assets/icon.svg` is the light version, used as the plugin icon by Claude and Codex.
- `assets/icon.svg` and `assets/icon-dark.svg` are the vector files, and `assets/icon.png` and `assets/icon-dark.png` are 1024 px PNGs with transparent corners, for places that need a raster image.

## Codex support (2026-10-04)

ProseShape now installs as a Codex plugin too: `codex plugin marketplace add Aieda1l/ProseShape`, then `codex plugin add proseshape@proseshape`. The skill is unchanged 1.4.0.

- `plugins/proseshape/plugin.json` is a portable [Agent Plugins](https://agent-plugins.org) manifest. Its `extensions` → `com.openai` → `interface` block carries Codex's display name, descriptions, category, example prompts, brand color and icon.
- `.agents/plugins/marketplace.json` lists the plugin for Codex under the same name, `proseshape@proseshape`.
- `skills/proseshape/agents/openai.yaml` sets how Codex's skill picker shows the skill.
- `package_skill.py` checks the Codex files, including OpenAI's field limits and a square icon. Five new tests bring the total to 43.
- A new CI job installs the plugin in both Claude Code and Codex from the checkout. It checks that Claude loads the skill and that Codex exposes it to the model.
- The README and `docs/publishing.md` cover installing in Codex and submitting to OpenAI's plugin directory.

## Packaging (2026-10-04)

ProseShape now installs as a plugin. The skill itself is unchanged 1.4.0, byte for byte the validated prompt.

- The skill moved to `plugins/proseshape/skills/proseshape/`. `plugins/proseshape/` is a Claude plugin with its own `plugin.json`, listing README and license copies, and `.claude-plugin/marketplace.json` lets anyone install it from this repository.
  - Claude Code: `/plugin marketplace add Aieda1l/ProseShape`, then `/plugin install proseshape@proseshape`.
  - claude.ai: add the same marketplace under **Customize > Plugins**.
- `scripts/package_skill.py` checks the plugin against the Agent Skills, claude.ai and directory requirements, and builds a deterministic `proseshape-<version>.zip` for claude.ai's skill upload and other agents. It has tests.
- GitHub workflows run the tests, the plugin checks, the held-out checksums and the table reproduction on every push and pull request. Pushing a `vX.Y.Z` tag publishes a release with the zip.
- `docs/publishing.md` covers the release checklist and submission to Anthropic's directory.
- Upgrading: if you installed by cloning the whole repository into `~/.claude/skills/proseshape`, remove that folder and reinstall with one of the methods in the README.

## 1.4.1 (candidate, not released)

I validated this candidate once on 15 new held-out texts (`evals/heldout2/`, frozen in `80617c2`). It scored the same as 1.4.0, at 7.70 each (paired +0.00 [−0.48, +0.48]). Judge-flagged fact problems fell from 29 to 16, but the text read slightly less naturally (4.45 against 4.67). 1.4.0 remains the release. The candidate is preserved at commit `5ada957`; `evals/harness/build_arm.py PS141b --rev 5ada957` rebuilds it exactly. See `evals/v1.4.1-validation/README.md`.

- Period and literary text keeps its spelling, punctuation, quotation marks, hyphenation and italics. Modern plain prose still gets a full copyedit.
- "Not just X but Y" asserts both X and Y. In otherwise clean text, a staged line is restated rather than cut, and tightened instead if the restatement reads stiffer. In dialogue, it is tightened at most.
- Small words that carry meaning ("finally", "quietly", "softly") stay. No new hedges and no softened certainty.
- No invented images or little scenes in rewrites.
- `references/evaluation-rubric.md` §3 matches the *weak alone* dash rule and points to `scripts/preserve_check.py`.

The held-out run also re-tested 1.4.0 against the ordinary-editor prompt: +0.27 [−0.78, +1.22], and +0.52 [−0.15, +1.15] pooled over both held-out sets. Planned for 1.4.2:
- leave a lone staged contrast in human-written text alone;
- carry contrasts in AI-shaped text in lighter wording;
- keep plain news takeaways;
- keep read-aloud repetition.

## 1.4.0

Validated on a frozen held-out corpus against a strong ordinary-editor prompt. It scored 8.17 against 7.33, a paired difference of +0.83 [+0.19, +1.54] (see `evals/v1.4-validation/README.md`). A second held-out set later gave +0.27 [−0.78, +1.22], and pooled over all 27 texts the lead is +0.52 [−0.15, +1.15] (see `evals/v1.4.1-validation/README.md`). Each change targets a failure that the [2026-09 comparison](docs/research/competitive-analysis-2026-09.md) found in 1.3.1.

- "Dressing goes; claims stay." Rewrites remove staging and inflation but keep the claim inside, with its strength, scope, direction and owner. Soft claims (aims, characterizations, scope words) are part of the preservation inventory, and a test decides whether a closing significance line says anything.
- Rewrite and light-edit modes add no reactions, feelings or opinions. Voice comes from the writer's own material. Added attitude is for Generate mode or on request, and is flagged.
- Paragraphs with tells are rewritten as a whole and checked claim by claim. Stiffness that no pattern names is fixed in the writer's register. "Remove the tell, not the move": a hook or emphasis the writer chose can stay without its stock wording.
- The draft's order, headings, lists, sign-off and rough length are kept, and so is structure readers navigate in pasted Markdown.
- Light edit on text a person wrote is a careful copyedit, not a pass-through.
- In fiction rewrite mode every beat stays, including stated realizations and the author's sensory details. Structural cuts move to deep rewrite and are offered in the note.
- New genre rows: customer support, marketing and landing pages, release notes and docs, press releases, social posts, cover letters.
- Dashes are replaced only when they recur or sit among other tells. Heading case is house style, not a tell.
- Self-review checks separately for lost claims and for additions.
- StoryScope is cited as arXiv:2604.03136v6. Wikipedia's *Signs of AI writing* is credited.
- New tooling (not loaded by the skill):
  - `scripts/preserve_check.py`, a standard-library preservation checker with tests;
  - `evals/harness/`, the scripts that iterated and validated this release;
  - `evals/heldout/`, the frozen 12-text corpus.

Known issues, left unpatched so that the shipped files match the validated prompt byte for byte:
- period spelling and markup get modernized (a Twain excerpt);
- a staged not-X-but-Y line in otherwise clean text is cut instead of restated;
- small meaning-bearing words go missing in personal writing;
- `references/evaluation-rubric.md` §3 still counts dashes against zero.

## 1.3.1

- Reduced stacked quips in short rewrites.
- Kept the preservation-first behavior introduced in 1.2–1.3.

## 1.3

- Restored liveliness through phrasing rather than invented events.
- Removed a copyable example that a model reproduced too literally.
- Preserved useful read-aloud signposts in children's writing.

## 1.2

- Prohibited adding new events during ordinary rewrites.
- Added a check against humor-by-formula.
- Strengthened deep-rewrite guidance so restructuring can change disclosure order.

## 1.1

- Kept mode selection private instead of leaking labels into replies.
- Added guidance to preserve personality while cutting generic prose.
- Added closure and bookend checks.
- Clarified generated-fiction return behavior.

## 1.0

- Initial two-level writing skill combining surface/discourse editing with narrative-structure guidance.
