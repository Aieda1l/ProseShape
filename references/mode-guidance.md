# Mode guidance

## Contents

1. Task variables to settle
2. Choosing the mode
3. Mode procedures
4. Genre voices without a sample
5. Reading a voice sample
6. Return formats

---

## 1. Task variables to settle

Settle these at the start of every task. Most come from the request; infer the rest and state important guesses in the note.

| Variable | Question | Default when unstated |
|---|---|---|
| `{mode}` | Which mode applies? | Rewrite for supplied text; Generate otherwise |
| `{genre}` | What kind of text is this? | Infer from the text |
| `{reader}` | Who reads it, and what do they already know? | The audience the text implies |
| `{purpose}` | What should the reader think, feel, or do afterward? | Infer from the text |
| `{sample}` | Is there genuine writing by the user? | None |
| `{permissions}` | May structure, order, ending, or plot change? | Rewrite keeps events, order, and ending |
| `{must_keep}` | Facts, quotes, citations, terms, plot facts, constraints | Everything factual in the source |

## 2. Choosing the mode

- "Humanize", "make it sound less like AI", "make it natural" with supplied text → **Rewrite**.
- "Light touch", "just polish", "don't change much", "it's mostly fine", or text with only a few tells → **Light edit**.
- "Free rein", "restructure", "the story feels AI-shaped", "fix the plot", "change whatever you need" → **Fiction deep rewrite**.
- Any genuine sample of the user's own writing → add **Voice match** to the mode.
- Documentation, reports, explanations, academic text, anything with citations or technical terms → **Factual/technical**, combined with Rewrite or Light edit.
- A request for new writing → **Generate** (plus Voice match if there is a sample).

Ask one question, then wait, only when all three hold: the change is structural, it could alter something the user may want to keep, and the request does not settle it. Example: "Humanize my story" on a draft whose ending is an epilogue coda. Rewrite the prose and mention the coda in the note rather than cutting it; or ask. Do not ask about sentence-level edits.

## 3. Mode procedures

### Generate
1. Settle the variables.
2. Name the default version (what most models would write). For fiction: the default premise treatment, theme statement, resolution type, ending, opening, and mood. For nonfiction: the default shape (hook, three points, uplifting close).
3. Sketch two or three alternatives in a line each. Choose. The default may win if it fits; then make its details specific.
4. Decide what stays implicit and where the piece should be uneven.
5. Draft in one pass for the reader.
6. Review: Level 1 tells, Level 2 questions, Claude's fingerprint, facts, voice.
7. Return the piece. Keep planning, mode labels, and craft notes out of the reply unless asked; for fiction, nothing goes before or after the story.

For nonfiction generation, use only facts the user supplied or that are common knowledge the piece needs. Mark a spot where a real detail would help ("[a specific example from your team]") only if the user would expect placeholders; otherwise write around the gap and say so in one line.

Avoiding clichés by saying almost nothing is its own failure. Give the writer a stance: what the facts mean to them or to the reader, one honest reaction, a sentence with some warmth or edge. Opinions and feelings in the writer's voice are allowed; invented events, people, and anecdotes are not.

### Rewrite
Run the eight passes in SKILL.md. Keep events, their order, and the ending. After cutting, check that a person is still audible (SKILL.md, "Cut, then give it a person"). In fiction you may cut a lesson line, change how emotions are rendered, trim a sensory survey, give dialogue subtext, and move a description block inside a scene. Flag any structural default (epilogue, epiphany ending, single-track plot) in the note instead of changing it.

### Fiction deep rewrite
1. Inventory plot facts the user wants kept (characters, premise, anything they named). If unclear, keep characters and core premise; everything else is open.
2. Write a short structural diagnosis for yourself: the default realization, the order of disclosure, the resolution type, escalation curve, ending, strands, introductions.
3. Choose the few changes that most improve the story. Two or three strong structural moves beat ten small ones, and the order of disclosure is usually one of them: if your plan still walks the original's scenes in the original order, look again. Keep invented characters as real as the originals; a relative played for laughs as the villain is a caricature, not a complication.
4. Rewrite the whole piece. Then run the surface passes on the new text.
5. Report the structural changes in the note so the user can reject them.

### Light edit
Fix only A1–A5 and E23–E26 tells, plus clear errors. Keep structure, paragraphing, and claims. Add nothing new: no jokes, no details, no events. If the text is good, return it nearly unchanged and say so. Resist the urge to justify the call with changes.

### Voice match
Read the sample first (section 5). The sample overrides Level 1 and Level 2 rules where they conflict. Keep the draft's content; change how it is said.

### Factual/technical
Correctness and directness come first. Keep every term, number, version, command, and citation exactly. Remove staging, inflation, and chatbot residue. Keep structure the reader navigates by (steps, headings in long docs). Add no humor, anecdotes, or first person.

## 4. Genre voices without a sample

| Genre | Voice | Watch especially for | Do not add |
|---|---|---|---|
| Business memo, announcement | Plain, specific, what changes for whom and when | A1, A2, C14, C17, D20 | Metrics, tools, or dates not given |
| Email or chat reply | Lead with the answer or decision; match the thread's register | F27, E23, A4 | Background the reader wrote |
| Personal essay, blog | The writer's opinions, doubts, humor, asides stay; reactions allowed where the writer would have one | G1, G3, lesson endings, A2 | Experiences, people, or places the writer did not mention |
| Technical explanation | Neutral, exact, ordered | A3, A4, C13, D20 | Quirks, jokes, analogies that change the meaning |
| Academic, literature review | Formal, hedged as the evidence requires, citations verbatim | C18 (unsourced "research shows"), B9, A3 | Sources, numbers, or stronger claims |
| Literary fiction | Voice of the POV character and narrative distance | All of Level 2; G1–G8 | Morals, codas, sensory tours |
| Genre fiction | Genre conventions first; still vary emotion and dialogue | G1, G6, flat escalation | Convention-breaking the reader didn't ask for |
| Dialogue-heavy fiction | Distinct speakers, subtext, interruptions | G6, uniform voice, tags that explain feelings | Dialect played for color |
| Children's and fable | Clear, linear, a moral may be stated; repetition and sequence signposts (first, next, finally) are the genre's rhythm, not a tell; distinct voices help reading aloud | Over-elaboration; flattening the read-aloud music | Nonlinear structure, ambiguity, new events |

## 5. Reading a voice sample

Note, briefly, before touching the draft:

- sentence length: typical and range; how often fragments appear
- paragraph length and how paragraphs open (with a claim, a scene, a question, a quote)
- punctuation: dashes per paragraph, semicolons, parentheses, colons, exclamation marks
- register: contractions, profanity, jargon, formality
- figurative density: how often a comparison appears, and what kind
- humor: dry, self-deprecating, absent
- how feelings appear: named, understated, joked about
- how pieces end: a punchline, a plain fact, a question, trailing off
- words and phrases the writer repeats

Write as that person would, keeping the draft's content. Match rates, not just features. If the writer's habits include something this skill would flag (dashes, fragments, "Look,"), keep it at their rate.

Signals that a sample may be machine-written: dense A1–A5 tells, triads in most sentences, uniform paragraph length, bolded labels. If you see several, say so in a sentence and ask whether to follow it.

## 6. Return formats

**Rewrite / deep rewrite**
```
[revised text]

What changed
- [main move, in plain words]
- [structural change or structural default you left and why]
- [anything cut]
- [detail the user should supply, if any]
```
Keep the note to what the user needs to accept or reject the edit: three to five lines. Skip bold labels and do not list what you kept; mention only moves, additions, cuts the user might miss, and gaps to fill.

**Light edit:** revised text, then one line ("Removed the sign-off line and one 'not just X' contrast; left the rest.").

**Generate:** the piece alone. Fiction gets no note at all. Nonfiction gets one line only if the user must supply or confirm something.

**File named:** write the final text to the file, prose only; leave code, commands, paths, frontmatter, data, and link targets unchanged; then a short summary.

**Embedded in another task:** the text alone.
