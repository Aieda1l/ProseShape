# Changelog

## 1.4.0

Validated on a frozen held-out corpus against a strong ordinary-editor prompt. It scored 8.17 against 7.33, a paired difference of +0.83 [+0.19, +1.54] (see `evals/v1.4-validation/README.md`). Each change targets a failure that the [2026-09 comparison](docs/research/competitive-analysis-2026-09.md) found in 1.3.1.

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
