# Evaluation rubric

Use this for the final self-review and for testing the skill. Score what a careful human reader would notice. Do not use AI-detector scores as the target; they measure something else and reward tricks.

## Contents

1. Dimensions and anchors
2. Over-correction red flags
3. Checks that can be done mechanically
4. How to compare two versions

---

## 1. Dimensions and anchors

Score 1 (poor), 3 (acceptable), 5 (excellent). "N/A" where a dimension does not apply to the genre.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Meaning preserved | Claims changed, dropped, or reversed | Minor drift in emphasis | Every supported claim intact |
| Factual integrity | Invented facts, sources, quotes, or experiences | A small unflagged addition | Nothing invented; gaps flagged, not filled |
| Specificity | Generic throughout | Some concrete detail | Details belong to this subject, reader, or character |
| Reader awareness | Written for no one; re-explains what the reader knows | Mostly fits the reader | Every line serves this reader's need |
| Voice consistency | Voice drifts or ignores the sample | Close to the sample or genre | Reads as the writer, including their habits |
| Formulaic rhetoric removed | Strong tells (A1–A5, E) remain | A few weaker tells remain | No staging, closers, triads by rule, or residue |
| Rhythm | Monotone, or alternating by rule | Mostly natural | Length and cadence follow the content |
| Implication | Meaning spelled out, lesson stated | Some explanation remains | The reader is trusted to infer |
| Structural choice (fiction) | Default structure unexamined where it hurts | Some defaults questioned | Structure chosen for this story; defaults kept on purpose |
| Character and narrative complexity (fiction) | Single-note characters, tidy moral | Some ambivalence | People want things, contradict themselves, sound distinct |
| Temporal and revelatory structure (fiction) | Order and reveals follow chronology by reflex | Reasonable | Disclosure order chosen for effect, linear where linear serves |
| No gratuitous quirks | Typos, slang, fake anecdotes, random devices | One ornamental choice | Every irregularity has a job |
| Genre fit | Breaks genre expectations the user didn't ask to break | Mostly fits | Fits genre and audience exactly |
| Edit proportionality | Rewrote good prose or left bad prose | Roughly proportional | Changed exactly what needed changing |
| Overall naturalness | Reads as generated | Mostly natural | A reader would take it as written by a person who cared |

## 2. Over-correction red flags

Any of these is a failure even if the tells are gone:

- a new fact, name, statistic, source, quotation, or personal memory in nonfiction
- a changed plot event, outcome, or character fact in rewrite or light-edit mode
- a flashback, subplot, twist, or "dear reader" aside added to look human
- every emotion now a plain label, every ending now ambiguous, every character now introduced by a line of dialogue
- deliberate errors, dropped punctuation, fake slang
- the writer's own dashes, fragments, or asides removed after a sample showed them
- a technical term simplified into something inaccurate
- a good draft rewritten heavily
- a "What changed" note longer than the edit warrants

## 3. Checks that can be done mechanically

- Every number, date, proper noun, and citation string in the input appears in the output (unless the note says it was cut and why).
- Quoted passages appear verbatim.
- Count em and en dashes against the sample's rate, or against zero for nonfiction without a sample (excluding code, ranges, and interrupted dialogue).
- Search for the A1–A5 and E patterns and the G1–G8 fiction patterns.
- For light edits, a word-level diff should be small.

## 4. How to compare two versions

Blind comparison works best. Strip labels, randomize order, and ask a reader to pick the one that better serves the task, scoring the dimensions above. Look beyond the winner: note which dimension decided it, and whether the loser failed through under-editing (tells left) or over-editing (invention, damage, new defaults).
