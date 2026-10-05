# Surface and discourse rules (adapted from Humanizer)

Adapted from blader/humanizer `SKILL.md` v3.1.0 (MIT License, github.com/blader/humanizer), which draws on Wikipedia's "Signs of AI writing." Section numbers in brackets are Humanizer's. Changes from Humanizer are marked **Adapted** or **Added**, with the reason.

## Contents

1. The account behind the patterns
2. How to weigh evidence
3. The patterns (A–F), strongest first
4. Fiction surface patterns (Added)
5. When not to act
6. Details that carry a voice

---

## 1. The account behind the patterns

A model writes whatever is most likely to come next, so it makes the choice that fits the widest range of readers and subjects. A writer chooses for one reader and one subject, so real choices are uneven and specific. Every pattern below is one form of the default choice: staging instead of stating, rhythm by rule, inflation, formatting by rule, leftovers from the chat, and writing for the wrong reader. [Humanizer, "Why AI text sounds the way it does"]

Word habits change with every model release; structural habits persist. That is why structure leads this list, and why StoryScope's narrative layer (see `storyscope-rules.md`) extends it upward.

## 2. How to weigh evidence

- Every sentence you keep must add something the reader did not already have, from earlier in the text or from the conversation around it. [Humanizer]
- A tell counts in proportion to how rarely a careful writer would make that choice on purpose. In text that already shows model defaults, patterns A1–A5 justify an edit on one sighting, and patterns marked *weak alone* need company from other tells in the same passage. [Humanizer] **Adapted:** in text that reads as a person's, every pattern is weak alone; change a sentence only for a fault you can name for the reader.
- Rewrite the sentence or paragraph around its point. Word-by-word patching leaves the shape. [Humanizer]
- Look at paragraph shape as well as sentences: a contrast split across two sentences, three parallel examples, or the same closer after every section is the same tell at a larger scale. [Humanizer]

## 3. The patterns

### A. Staging instead of stating (act on one sighting in text that shows model defaults)

| # | Pattern | Watch for | Fix | Keep when |
|---|---|---|---|---|
| A1 [§1] | Not X but Y | not just/only/merely X but Y; it's not X, it's Y; X rather than Y; "This does not mean X. It means Y."; clipped tail ", no guessing" | State the point directly. "Not just X but Y" asserts both, so a plain version keeps both, usually by dropping only the staging words; in text a person wrote, a lone instance is their emphasis, so leave it; in dialogue, tighten at most | The negative half corrects a belief the reader actually holds, or both halves carry information |
| A2 [§2] | One-line closers and dramatic fragments | a one-sentence paragraph restating the one before; "That distinction matters."; "Let that sink in."; a sentence after an example or scene naming what it showed ("It was a lesson in patience."); rows of fragments; every. single. day. | Cut the closer; merge fragments into one specific claim. If the closer asserts something the paragraph does not (a stake, a scope, "this is only the start"), keep that claim in a plainer sentence | The short sentence adds a new fact or consequence |
| A3 [§3] | Sayings that sound deep | the real question is; at its core; fundamentally; the heart of the matter; X is the language/currency/architecture of Y; X becomes a trap | Replace with the specific claim | It is a quotation or a title |
| A4 [§4] | Staged run-up | Let's dive in; here's what you need to know; Here's the thing; Honestly?; Look,; Real talk | Remove the run-up; start with the point | "honestly" inside a casual sentence is ordinary speech; a signpost that introduces an explanation or a set of steps ("Here's how it works.") is ordinary in explainers and tutorials |
| A5 [§5] | Arguing with no one | This isn't about; I'm not saying; To be clear; Don't get me wrong; A tempting approach would be; You might think... but | Remove the defense; state any real claim | The objection is attributed or answered in full; the rejected option is one a reader would weigh |

### B. Rhythm by rule

| # | Pattern | Fix | Notes |
|---|---|---|---|
| B6 [§6] | Forced triads: three items, three examples, three short facts and a lesson | Use as many items as the meaning has | **Adapted:** includes sensory triads (sight, sound, smell in one breath) and three parallel scene beats |
| B7 [§7] | Repeated sentence openings (She... She... She...) | Merge, change subject, or begin with the action | Deliberate anaphora is fine |
| B8 [§8] | Dashes as the universal connector (*weak alone* for one) | Replace with a period, comma, colon, parentheses, or a rewrite | **Adapted:** Humanizer bans all em and en dashes without a sample. Here: without a sample, replace dashes that recur as the default connector or sit among other tells; a single purposeful dash in otherwise clean prose stays (weak alone). In fiction, keep a dash that marks interrupted or broken-off speech (a typographic convention, not a connector). With a sample, match its rate. Dashes in code, paths, URLs, and number ranges stay. |
| B9 [§9] | Stacked qualifiers (could potentially, might arguably) (*weak alone*) | Keep a qualifier only when the evidence needs it | Keep scope statements, safety notes, real doubt |
| B10 [§10] | Hyphenated compounds after the noun (the report is high-quality) (*weak alone*) | Hyphen before the noun, none after | Dictionary-hyphenated words keep it |
| B11 [§11] | Passive voice and missing subjects (*weak alone*) | Name the actor when that helps | Passive is right when the actor is unknown or unimportant |
| B12 **Added** | Mechanical rhythm alternation: a short punchy sentence after every long one; three-beat paragraphs | Let length follow content | Humanizer's step 4 says "vary sentence length"; varying by rule is the same default |
| B13 **Added** | Humor by formula: the triple gag ("X welcome. Y welcome. Everyone else, also welcome."), a wry aside after every feeling, a punchline closing each paragraph | Keep one joke that comes from the material, or none | Seen in this skill's testing when voice was added too eagerly |

### C. Inflation and borrowed authority (the fact is usually sound; remove the dressing)

| # | Pattern | Watch for | Fix |
|---|---|---|---|
| C13 [§12] | Overused AI words | additionally, align with, bolstered, crucial, delve, enduring, enhance, garner, highlight (verb), interplay, intricate, key (adj.), landscape (abstract), meticulous, pivotal, quietly, robust (figurative), showcase, tapestry, testament, underscore, valuable, vibrant | Plain words. Weak evidence alone; groups of them are stronger |
| C14 [§13] | Inflated significance | marking a pivotal moment; reflects a broader; enduring legacy; setting the stage; evolving landscape; "Despite these challenges... continues to thrive"; "The future looks bright" | Keep the fact, drop the inflation. If the significance carries a real claim (an aim, a purpose, an expected benefit, who it is for), say that claim plainly instead of dropping it |
| C15 [§14] | Vague connection | associated with; in connection with; linked to; tied to | Name the relationship if the source gives it; otherwise keep the vague wording rather than inventing a role |
| C16 [§15] | Shallow -ing riders | highlighting, underscoring, reflecting, symbolizing, fostering, showcasing | Keep the fact; keep the rider only if the source supports it |
| C17 [§16] | Sales language | nestled, in the heart of, breathtaking, rich (figurative), renowned, stunning, must-visit | Say what the thing is |
| C18 [§17] | Borrowed authority | experts argue; industry reports; cited in [list of outlets]; over N followers | Name the real source and what it said, or cut |
| C19 [§18] | Avoiding is/are/has | serves as, stands as, boasts, features, offers | is, are, has |

### D. Formatting by rule

| # | Pattern | Fix | Notes |
|---|---|---|---|
| D20 [§19] | Bold as decoration; bold-label lists | Remove bold scattered through sentences; turn label lists into prose when labels add nothing | **Adapted:** keep structure the reader navigates by: bold labels in feature lists, release notes, docs, and product pages stay (plainer label text is fine), and so do headings and calls to action |
| D21 [§20] | Emoji and arrow decoration, rules between every section, headings written for effect | Remove the decoration; name what the section holds | **Adapted:** Humanizer also converts Title Case to sentence case, which is Wikipedia's house style, not a tell. Keep the draft's heading case unless the user's style guide says otherwise. Fiction and essays usually take no headings at all |
| D22 [§21] | Curly quotes where the target uses straight ones (*weak alone*) | Follow the target format | **Adapted:** manuscripts and published prose often use curly quotes correctly. In supplied text, keep the quotation marks as they are |

### E. Leftovers from the chat and the draft (remove outright)

| # | Pattern | Watch for |
|---|---|---|
| E23 [§22] | Chatbot residue | Great question!; Certainly!; I hope this helps; Let me know if; Would you like me to; Here is a... |
| E24 [§23] | Knowledge-limit disclaimers and guesses | as of my last update; based on available information; not widely documented; likely grew up... |
| E25 [§24] | A heading repeated in the first sentence | "## Performance" then "Speed matters." |
| E26 [§25] | Writing about the document instead of the subject | "This function was added to replace..."; "compiled from..."; "the table below compares..." |

### F. Writing for the wrong reader

| # | Pattern | Fix |
|---|---|---|
| F27 [§26] | A reply that re-explains what the reader already knows and puts the decision last | Lead with the decision; keep only the reasoning that would change whether the reader agrees |

Before and after (A1, A2, C14 together):

> It's not just a tool; it's a new way of working. Teams can finally collaborate in real time. That's the real win.

> Two people can now edit the same file at once and see each other's changes as they type.

(The second version keeps the only claim the first one made. If the draft does not say what the tool does, the rewrite cannot either; ask.)

## 4. Fiction surface patterns (Added)

The sentence-level faces of StoryScope's narrative findings. Use with `storyscope-rules.md`. In rewrite and light-edit modes these fixes change how a beat is told; the beat itself (the feeling, the realization, the weather change, the coda) stays. Cutting one is a deep-rewrite move; offer it in the note.

| # | Pattern | Watch for | Fix | Source |
|---|---|---|---|---|
| G1 | Somatic emotion stock | throat tightened, breath caught, chest ached, jaw clenched, stomach dropped, heat crept up her neck | Rewrite mode: keep every one, even a short stock sentence, reword it lightly at most, and merge only sensations that repeat; never cut one or replace it with an action. Deep rewrite: keep the one specific physical detail; turn the rest into plain naming, action, or speech, or cut | StoryScope 81% vs 38% embodied (Table 16) |
| G2 | Sensory survey | three or more senses in one paragraph, especially at scene openings; stock smells (ozone, petrichor, antiseptic, old books) | Keep the detail this character would notice. In rewrite mode the author's details stay; cut only the adjectives and similes around them | StoryScope sensory density and olfactory rows + Humanizer §6 |
| G3 | Lesson line | "She realized that...", "It was never about the X.", "Maybe that was the point.", "Some things can't be fixed, only carried." | Rewrite mode: shorten it and give it to the character in her own words. Deep rewrite: cut, or turn into a concrete act | StoryScope thematic explicitness + Humanizer §2 |
| G4 | Mirror weather | light breaking, rain easing, dusk falling at emotional peaks and endings | Let the world be indifferent, or make it the character's projection; in rewrite mode keep the weather event and drop the symbolic framing | StoryScope setting as mirror |
| G5 | Vague allusion | "an old song", "a line from a poem she'd once read", "a famous painting" | Name the real thing the character would name, or cut | StoryScope explicit references 47% vs 24% |
| G6 | Thesis dialogue | characters speaking the theme in finished, balanced sentences | Give each speaker a want; let them interrupt and dodge | StoryScope dialogue as philosophical debate 59% vs 34% |
| G7 | Coda | "Years later...", "In the spring that followed...", a final paragraph confirming everyone's fate | Deep rewrite: end where the change lands. Rewrite mode: keep the coda, tighten it, and offer the cut in the note | StoryScope Claude fingerprint |
| G8 | Description-block introduction | a new character's hair, eyes, clothes, and bearing in one paragraph on arrival | Lead with what they say or do | StoryScope 52% vs 30% |
| G9 | Bookend and exact payoff | the last image repeats the first; a planted object returns on cue; a final symbolic wink | End on the act; leave one cost open | This skill's testing; StoryScope tidiness findings |

## 5. When not to act [Humanizer, adapted]

Any pattern can be a deliberate choice. Leave a watched phrase alone inside a quotation, a title, a proper name, or a passage that discusses the phrase instead of using it. Salutations and sign-offs on letters predate chatbots. People who judge by feel do little better than chance, and human writing keeps absorbing AI habits, so several tells together are the safeguard. **Added:** if the text reads well and the tells are few, the right edit is small. Changing prose only to make it different is a failure, not a success. The opposite failure is just as common: cutting every tell and leaving a flat, voiceless text. Humanizer says it directly: removing tells is half the job; the result must still sound like a person. **Added:** removing a tell never removes the claim it was dressing. A contrast whose two halves both carry meaning ("hire for curiosity, not credentials") is a claim, not a tell; keep it.

## 6. Details that carry a voice [Humanizer]

Keep these unless they damage the meaning:

- a specific, unusual detail ("the lawyer who used to work upstairs from my dentist")
- mixed feelings and unresolved tension
- dated, era-bound references: slang, memes, in-jokes
- a first-person choice the writer can explain
- a real aside, parenthesis, or self-correction
