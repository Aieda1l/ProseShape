# StoryScope rules: narrative defaults in AI fiction

Source: Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. "StoryScope: Investigating idiosyncrasies in AI fiction." COLM 2026, arXiv 2604.03136v6. Page and table numbers below refer to that PDF.

## Contents

1. How to use this file
2. What the study did
3. Core evidence (Table 16 at a glance)
4. Complications you must respect
5. Principles, one per finding (plus 5.18 from testing)
6. Claude's fingerprint
7. Other models' fingerprints
8. Transfer to nonfiction

Labels: **Finding** = printed in the paper. **Reading** = my interpretation. **Practice** = a writing recommendation derived from both. Findings are about fiction only.

---

## 1. How to use this file

Each principle names a model default, the question to ask, and the moves available. Use it diagnostically: if the default is the best choice for this story, keep it. Never aim at the paper's percentages. A story that hits every "human-side" feature is just a new template.

The strongest single lesson (Finding, p.20–21, Table 8): no one narrative dimension is sufficient or necessary to separate human from AI stories. The AI profile is a cluster of co-occurring choices (linear plot, tight causality, explicit theme, narrow cast). Revise the whole story, not one feature.

## 2. What the study did

- 10,272 human short stories from Books3 anthologies; a writing prompt reverse-engineered from each; five models (Claude Sonnet 4.6, GPT-5.4, Gemini 3 Flash, DeepSeek V3.2, Kimi K2.5) wrote a story from each prompt. 61,608 stories, about 5,000 words each (p.3).
- Each story was converted into a structured narrative template along ten NarraBench dimensions (agents, social network, events, plot, structure, setting, time, revelation, perspective, style) so comparison worked on content, not wording (p.4, Fig. 8).
- GPT-5.1 compared sources and proposed 304 discrete features; Gemini 3 Flash assigned them to every story (p.4–5). Human–model agreement κ = 0.84; human–human κ = 0.74 (p.19, Table 7).
- XGBoost + SHAP identified 30 **core** features (stable human-vs-AI separators) and 75 **fingerprint** features (specific to one source) (p.5).

Results (Findings): narrative features alone 93.2% macro-F1 for human vs AI; 96.0% with style; 68.4% for six-way attribution (p.6 Table 2; p.8 Table 3). Surface edits with LAMP moved detection from 95.5 to 93.9 (p.8). Human stories are rarer in feature space (mean rarity percentile 0.71 vs 0.49, d = 0.83) (p.9, p.23).

## 3. Core evidence (Table 16, p.26)

Scales are 1–5 means; ordinal rows are means over integer codes; arrows are prevalence of one option.

| Theme | Feature | Human | AI |
|---|---|---|---|
| Thematic over-determination (AI) | Thematic explicitness and moralizing | 3.28 | 3.94 |
| | Moral/philosophical weighting | 3.26 | 3.68 |
| | Thematic unity | 4.41 | 4.74 |
| | Narratorial thematic commentary → yes | 52% | 77% |
| | Dialogue function → philosophical debate | 34% | 59% |
| | Reference explicitness → implicit echoes | 50% | 72% |
| Sensory and embodied performativity (AI) | Emotional expression → embodied | 38% | 81% |
| | Setting as psychological mirror | 3.58 | 4.07 |
| | Environmental and ecological emphasis | 2.83 | 3.21 |
| | Sensory modalities → olfactory | 57% | 82% |
| | Sensory density | 3.66 | 3.93 |
| | Depth of interior access | 3.67 | 3.93 |
| Structural streamlining (AI) | Causal chain continuity | 3.92 | 4.20 |
| | Spatial granularity (ord.) | 2.27 | 2.53 |
| | Agency in resolution → protagonist choice | 46% | 69% |
| | Character introduction → external description | 30% | 52% |
| | Subplot integration → no subplots | 57% | 79% |
| | Resolution mode → internal understanding | 27% | 47% |
| | Opening spatial grounding (ord.) | 2.12 | 2.33 |
| | Pre-threat character investment | 2.76 | 2.99 |
| Intertextual richness (human) | Intertextual strategy → explicit named reference | 47% | 24% |
| | Reference explicitness → balanced mix | 37% | 16% |
| Reader engagement (human) | Fourth-wall permeability (ord.) | 0.67 | 0.39 |
| | Direct reader address (ord.) | 0.28 | 0.07 |
| Temporal complexity (human) | Depth of recontextualization after surprise | 3.28 | 2.95 |
| | Chronological discontinuity | 2.40 | 2.12 |
| | Nonlinear framing for delayed disclosure | 1.96 | 1.68 |
| | Anachrony intensity | 2.58 | 2.31 |
| Narrative diversity (human) | Location variety scope (ord.) | 1.34 | 1.08 |
| | Dialogue-to-narration proportion | 2.95 | 2.70 |
| | Subplot integration → thematically parallel | 42% | 21% |
| | Moral polarity → ambivalent/mixed | 59% | 38% |
| | Emotional expression → explicit labels | 29% | 8% |

## 4. Complications you must respect

1. **Distributions overlap.** Human and AI rarity distributions "overlap substantially," and AI stories appear in every rarity tail (Finding, p.23 Fig. 5, Table 13). No feature proves authorship of one text.
2. **Humans are mostly linear and unified too.** Thematic unity 4.41/5, causal continuity 3.92/5, chronological discontinuity 2.40/5 (Finding, Table 16). Practice: most stories should stay mostly chronological and coherent.
3. **"Human" devices are other models' habits.** Frequent flashbacks are a Gemini fingerprint; in medias res and in-action introductions are Kimi's; subverting expectations is GPT's (Finding, p.9, p.27 Table 17). Reading: adding devices from a list moves a text toward another AI, not toward a person.
4. **Reader address is rare even for humans.** Table 16 gives ordinal means (0.28 vs 0.07), which the p.7 prose reports as "28% vs. 7%"; and a human fingerprint is "narrator address mode → no direct address" (Table 17). Reading: never add "dear reader" asides to seem human.
5. **The emotion finding is about monotony.** Human dominant modes split roughly 38% embodied, 29% labels, and the rest behavioral cues or ambiguous; AI is 81% embodied (Finding + arithmetic, Table 16). Reading: the fix is a mix, not labels everywhere.
6. **Smell is normal.** 57% of human stories have smell among their dominant senses (Finding). The AI signal is near-universality (82%).
7. **Craft advice can be the model prior.** "The protagonist must drive the climax" matches the AI-elevated feature (69% vs 46%). So do more interiority (3.93 vs 3.67) and more setup before the threat (2.99 vs 2.76). Reading: workshop rules are not automatically human.
8. **Distinguishable is not better.** StoryScope measures separability, not quality; it ran no reader-preference study. Its human stories are published and edited; its AI stories are single zero-shot drafts (Reading, from p.3 and Figs. 6–7). Optimize for the reader; use the findings to question defaults.
9. **Scope limits.** No limitations section appears in the paper. Limits implied by the method: fiction only; about 5,000-word stories; English-language anthologies; one draft per model; model versions from early 2026; features assigned by an LLM. Length, topic, and memorization were checked and did not explain the results (App. F–G). Fingerprints may shift with new model versions.
10. **Surface edits do not touch structure** (Finding, p.8, tested on 278 Gemini stories rewritten by Gemini). Practice: a structural pass has to be separate from the surface pass.

## 5. Principles, one per finding (plus 5.18 from testing)

Format: **Default** (what models do) · **Ask** · **Moves** · **Leave it when** · **Overdone looks like**.

### 5.1 Stated meaning (Table 14 #1, #10; p.7)
- **Default:** the narrator names the theme; a grieving character's arc ends with the lesson stated (the paper's own example, p.7).
- **Ask:** where does the text tell the reader what the story means? Check the last paragraph and the beat after each key scene.
- **Moves:** cut the statement; replace it with an action, image, or line of dialogue that implies it; or give the interpretation to a character who could be wrong.
- **Leave it when:** fable, parable, children's story, satire, or a retrospective narrator whose reflecting is the form.
- **Overdone:** a story with no discoverable point. Half of human stories still include some commentary.

### 5.2 Debate dialogue and moral weighting (Table 14 #12, #15)
- **Default:** characters articulate the story's question in complete sentences.
- **Ask:** what does each speaker want from the other in this scene?
- **Moves:** route the argument through a concrete disagreement (the house, the money, who drives); let people interrupt, dodge, answer a different question; let the large question stay under the talk.
- **Leave it when:** novels of ideas, trials, seminars, a character whose lecturing is who they are.
- **Overdone:** trivializing a story whose subject is an argument.

### 5.3 Single track (Table 14 #3, #14; Table 15 #7)
- **Default:** every scene serves the main line; no secondary strand.
- **Ask:** is the piece long enough (roughly 2,500 words or more) to hold a second strand that sees the theme from another angle?
- **Moves (deep rewrite or generation):** grow a small parallel line from material already present, such as a minor character's own trouble. Human subplots are nearly always thematically parallel, not unrelated (Reading from 57% none + 42% parallel). Do not tie it off neatly.
- **Leave it when:** flash fiction, single-scene pieces, a user outline.
- **Overdone:** padding; a subplot that exists for the rule.

### 5.4 Emotion through the body (Table 14 #2; Table 15 #12; p.7)
- **Default:** "show, don't tell" everywhere: throat tightens, chest aches, breath catches, stomach drops.
- **Ask:** which beats carry the story? Which feelings are incidental?
- **Moves:** name incidental feelings plainly ("She was afraid of him, a little."); give key beats to action or speech; let one feeling stay unclear to the character; keep a physical detail only when it is specific to this person.
- **Leave it when:** genres that run on physical response (thriller, romance) or stories about bodies. Vary it anyway.
- **Overdone:** labels everywhere; or, the opposite failure, feeling cut so hard the character seems absent. Humans use explicit labels far more than models (29% vs 8%), and Claude's default is already restraint (§6). In testing this skill, over-applying implication produced a muted story that readers found cool.

### 5.5 Sensory tours and stock smells (Table 14 #4, #8)
- **Default:** scene openings that visit light, sound, smell, and touch; smell almost always present.
- **Ask:** what would this character notice now, and which detail does work (characterizes, sets up, contradicts)?
- **Moves:** keep one or two load-bearing details; cut stock atmosphere (ozone, petrichor, antiseptic, "coffee and something else"; this list is my addition).
- **Leave it when:** food, nature, or place writing; a deliberately lush sample; a character defined by perception.
- **Overdone:** sterile rooms.

### 5.6 Setting as mirror (Table 14 #6, #17)
- **Default:** rain for grief, light breaking through at the resolution.
- **Ask:** at emotional peaks and at the ending, does the weather or light agree with the feeling?
- **Moves:** let the world go on indifferently (a delivery truck idles; the game on TV keeps going); or make the correspondence the character's own projection.
- **Leave it when:** gothic, fairy tale, lyric modes.
- **Overdone:** irony as a reflex.

### 5.7 Interior access (Table 14 #20)
- **Default:** narration explains thoughts and motives, often right after the action showed them.
- **Moves:** cut the explanation; leave one important motive unstated.
- **Leave it when:** stream of consciousness, confessional first person.
- **Overdone:** blank characters.

### 5.8 Causal tidiness (Table 14 #7; p.7)
- **Default:** each event causes the next; every setup pays off.
- **Moves:** let something from outside the chain interrupt; allow an event that matters for character without advancing the plot; leave one thread open when that is truer.
- **Leave it when:** fair-play mystery, thriller, children's story, very short fiction.
- **Overdone:** randomness passed off as life.

### 5.9 Resolution by the protagonist's choice (Table 14 #9)
- **Default:** one decisive, usually admirable choice fixes everything.
- **Ask:** in this world, what would actually resolve this?
- **Moves:** let the choice matter without controlling the outcome: too late, partial, overridden, or changing only the protagonist. Other people, institutions, and chance can decide things.
- **Leave it when:** quest and adventure forms; the user's outline.
- **Overdone:** a passive protagonist; coincidence that feels unearned.

### 5.10 Resolution by realization (Table 14 #18)
- **Default:** "She finally understood..." closes the story.
- **Moves:** show the change through a concrete act; or leave the understanding incomplete.
- **Leave it when:** an epiphany the whole story has earned.
- **Overdone:** forcing plot events into a quiet story.

### 5.11 Moral polarity (Table 15 #11)
- **Default:** the protagonist is clearly good or clearly wronged, and the narration confirms it.
- **Moves:** remove narration that excuses or justifies; let one act or motive stand without a verdict.
- **Leave it when:** children's fiction, heroic genres, the user's character notes.
- **Overdone:** gratuitous unpleasantness; "gray" as a template.

### 5.12 Introductions (Table 14 #5; Table 17 human #1)
- **Default:** hair, eyes, clothes, and bearing on first appearance.
- **Moves:** introduce a person through what they first say or do that matters; add appearance as the observer would notice it, later if at all. Human authors distinctively introduce characters in dialogue (Finding, Table 17).
- **Leave it when:** the description is the narrator's voice (a noir once-over).
- **Overdone:** every character entering on a line of dialogue.

### 5.13 Openings (Table 14 #11, #13, #19)
- **Default:** an establishing shot of place, light, and weather; a warm-up of routine before trouble.
- **Moves:** open on whatever gives the reader the right question: a voice, a situation, a line, a wrong note. Let place arrive when needed; let the reader meet people under pressure.
- **Leave it when:** place is the subject; the reader would be lost.
- **Overdone:** in medias res by reflex (Kimi's fingerprint).

### 5.14 Order of information (Table 15 #8, #10, #13; Table 17 human #4; p.7)
- **Default:** information order equals event order, "from first clue to the grand reveal" (p.7).
- **Ask:** what must the reader not know yet? Where does meaning concentrate? Would starting at a consequence create a better question than starting at the cause?
- **Moves (deep rewrite or generation):** open at a later point and return; hold back a fact the characters know; place a key revelation late ("back-loaded" pacing is a human fingerprint). Keep chronology when it serves.
- **Leave it when:** fairy tales, journeys, procedurals, countdowns, children's stories, a plot the user made linear on purpose.
- **Overdone:** confusion; flashbacks as decoration (Gemini's fingerprint).

### 5.15 Surprises that recast (Table 15 #4)
- **Default:** a surprise adds a fact and the plot moves on.
- **Moves:** plant details that read one way before the revelation and another way after it.
- **Leave it when:** the story has no surprise. Do not manufacture one.
- **Overdone:** twist-hunting (GPT's fingerprint).

### 5.16 Range: places, talk, named things (Table 15 #1, #3, #5, #9; Table 14 #16)
- **Default:** one or two locations; narration summarizing conversations; "an old song," "a poem she'd once read."
- **Moves:** let the story move when the story moves; play key conversations as dialogue; name the specific song, street, book, or brand a character would name. It must be real and accurately described, or plainly invented.
- **Leave it when:** timeless fables; secondary worlds (use in-world names).
- **Overdone:** name-dropping; invented titles passed off as real; quoting lyrics.

### 5.17 Reader address (Table 15 #2, #6; Table 17 human #3)
- **Practice:** add reader address only when the story implies a listener (a letter, a confession, a tale told aloud) or the sample does it.

### 5.18 Closure that clicks shut (Practice; related findings: Gemini's tidiest endings and Claude's closure fingerprint, p.9, Table 17)
- **Default:** a bookend that echoes the opening image; a planted detail that pays off exactly; every thread tied; a symbolic wink in the last lines.
- **Ask:** after the last scene, is anything still owed, costly, or open? Does the final image repeat the first one for symmetry's sake?
- **Moves:** end on the act, not the echo; leave one cost unpaid; drop the wink.
- **Leave it when:** the form wants a clean close (fable, comic caper, a mystery's solution).
- **Note:** this principle comes from this skill's own tests (two of three independently written stories ended by echoing their openings) and from the paper's tidiness findings; StoryScope has no single "bookend" feature.

### 5.19 Convergence (p.9; Table 13)
- **Default:** the first story anyone would write from this prompt. Claude's stories fall in the rarest tails least often of all sources (33 of 1,377 in the top 5%).
- **Practice:** before drafting, name that default story, then look for the choice this material suggests. Keep the default if it is best, knowingly.

## 6. Claude's fingerprint (p.9; p.27 Table 17)

StoryScope tested Claude Sonnet 4.6. Claude is the most distinct AI source in the discriminant projection (p.7 Fig. 2) and "keeps it cool."

| Finding | Evidence | Ask | Leave it when |
|---|---|---|---|
| Event intensity escalates less than in any other source | Table 17 #1, uniqueness 22.4 (highest in the table) | Plot each scene's intensity. Where should consequences compound or become irreversible? | Restraint is the point. Never add melodrama. |
| Event-type diversity is a Claude fingerprint; direction not reported | Table 17 #2, largest SHAP | Are all events the same kind (talks, realizations)? Would a physical, social, or accidental event serve? | Treat as a check, not a finding. |
| Endings reach forward in time: epilogue or flash-forward | Table 17 #3; p.9 | Does the coda add anything the last scene did not? | Frame stories; forms that expect a coda. |
| Dreams and visions as temporal distortion: no | Table 17 #4 | Awareness only. | Do not add dream sequences. |
| Setting mood: uncanny or haunted | Table 17 #5 | Was the hush chosen? | Horror, gothic. |
| Narrative voice is the most uniform | p.9 | Do characters sound different from each other and from the narrator? | Deliberately uniform narration. |
| Reverent toward convention (62% vs 39–56%) | p.9 | Which convention carries the story? Fulfil, bend, or break it on purpose. | Subverting everything is GPT's habit. |
| Quiet endings over "avalanche" endings | p.9 | Does the ending release pressure too gently for what came before? | A quiet close the story earns. |

## 7. Other models' fingerprints (p.9; Table 17)

Useful when the text you rewrite came from another model.

- **GPT:** gossip and rumor drive plot (64% vs 44–55%); distant retrospective narration; expectation subversion (41% vs 27–36%); ambiguous reconciliations; no habitual narration.
- **Gemini:** tidiest endings; extended denouements; bleak, oppressive settings (88%); frequent flashbacks; siege or ordeal plots; direct speech dominates.
- **DeepSeek:** front-loads context other sources hold back; visible narrator; behavioral cues for emotion; backstory interleaved evenly.
- **Kimi:** in medias res entry; in-action character introductions; avoids explicit trait labels; otherwise sits at the generic center of the AI cluster.
- **Human fingerprints (for contrast, not imitation):** in-dialogue introductions; single focal character; no direct address; back-loaded revelations; crossover genre ambition.

## 8. Transfer to nonfiction (Reading and Practice; untested by StoryScope)

| Principle | Personal essay / memoir | Business, technical, academic |
|---|---|---|
| Stated meaning (5.1) | Applies to endings: do not announce the lesson; keep reflection the writer owns | Does not apply; state the thesis |
| Emotion through the body (5.4) | Applies to the writer's own feelings | Rarely relevant |
| Sensory tours (5.5) | Applies | Does not apply |
| Resolution by realization (5.10) | Applies: a tidy epiphany ending is a default | Does not apply |
| Order of information (5.14) | Possible, only with the writer's real events | Use logical or step order |
| Named specifics (5.16) | Only names the writer supplied | Only names the source supplied |
| Everything that invents detail | Never | Never |
