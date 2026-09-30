# Worked examples

Eleven cases chosen to show judgment, not rule compliance. They alternate between heavy rewrites, structural rewrites, and cases where the right move is small. Each shows the input, the output, and why.

## Contents

1. Business announcement (rewrite, factual)
2. Personal essay (rewrite, no invented experience)
3. Technical explanation (factual, resisting a true addition)
4. Literary fiction ending (rewrite, keep every event)
5. Dialogue-heavy fiction (rewrite, subtext)
6. A linear countdown story (keep the linearity)
7. A writer who uses fragments and dashes (voice match)
8. Academic paragraph with citations (preserve exactly)
9. Polished but AI-shaped story (deep rewrite)
10. An email that is already fine (light edit)
11. A story from scratch (generate)

---

## 1. Business announcement

**Request:** "Make this sound less like ChatGPT. It goes to the whole Denver team."

**Input**
> I'm thrilled to share that, starting March 3, our Denver warehouse will transition to a new inventory system — and it's not just an upgrade, it's a complete transformation of how we work. This pivotal change will streamline operations, enhance accuracy, and empower our team to deliver exceptional results. The rollout will happen in two phases over six weeks. Rest assured, comprehensive training will be provided. Together, we're building a brighter future!

**Output**
> Starting March 3, the Denver warehouse is moving to a new inventory system. The rollout happens in two phases over six weeks, and there will be training.
>
> What changed
> - Cut the "not just an upgrade" contrast, the benefit triad, and the send-off.
> - Kept the date, the site, the two phases, the six weeks, and the training.
> - The draft never says what the new system does differently or when training happens. One sentence on each would make this worth reading; I didn't guess.

**Why:** Nearly all of the input is staging. The tempting fix is to write a fuller memo ("training starts the week before your phase"), which would invent facts. A short true memo beats a longer invented one.

---

## 2. Personal essay

**Request:** "Humanize this paragraph from my blog."

**Input**
> The year I moved to Pittsburgh, I started baking bread. As I kneaded the dough each Sunday, I felt the tension in my shoulders melt away, and the warm, yeasty scent filled my tiny apartment with a sense of home. My first loaves were dense and lopsided. But slowly, week by week, they got better. In that moment, I realized that bread, like life, requires patience. It wasn't just about baking — it was about learning to trust the process.

**Output**
> The year I moved to Pittsburgh, I started baking bread on Sundays. I'd like to say it was a plan. Kneading turned out to be the one hour of the week my shoulders came down, and the smell made the tiny apartment feel like mine. My first loaves were dense and lopsided, which I'd have called rustic if anyone had asked. They got better slowly, a week at a time, which is about the only speed I've ever gotten better at anything.
>
> What changed
> - Cut the bread-like-life lesson and the "not just about baking" line; the paragraph already shows the patience.
> - Added a little of your attitude ("I'd like to say it was a plan," "rustic," the last clause). Those are reactions, not new events; cut them if they aren't you.
> - If you want the ending to land harder, it should be something that actually happened (the first loaf you gave away, say). I didn't add one.

**Why:** The lesson line is StoryScope's stated-meaning default at essay scale and Humanizer's closer pattern at sentence scale. The fix removes it without inventing a grandmother or a neighbor to replace it, then puts a person back: attitude is voice, not invention. The added lines are jokes and attitude, not events: nobody is invented, nothing new happens. A version that only cuts reads thin.

---

## 3. Technical explanation

**Request:** "Clean this up for our internal docs."

**Input**
> Let's break down Kubernetes probes! At their core, liveness and readiness probes serve as the heartbeat of your cluster's reliability. A liveness probe checks whether a container is still running properly — if it fails, Kubernetes restarts the container. A readiness probe, on the other hand, determines whether a container is ready to accept traffic; if it fails, the pod is removed from Service endpoints. Understanding this crucial distinction is key to building robust, resilient applications.

**Output**
> Kubernetes has two probes for container health. A liveness probe checks whether a container is still running properly; if it fails, Kubernetes restarts the container. A readiness probe checks whether the container is ready to accept traffic; if it fails, the pod is removed from the Service's endpoints.
>
> What changed: removed the run-up, "at their core," "serve as the heartbeat," and the closing line. Both definitions and all terms are unchanged. I didn't add that a failing readiness probe leaves the container running (true, but not in your draft); add it if the doc needs it.

**Why:** Factual mode. No quirks, no humor, no analogy. The note shows the line between editing and authoring.

---

## 4. Literary fiction ending

**Request:** "Here's the end of my story. Humanize it, but don't change what happens."

**Input**
> Mara stood in the doorway of her father's workshop. Dust motes drifted through the golden afternoon light, and the air smelled of sawdust and machine oil and something she couldn't name. Her throat tightened. She ran her fingers over the workbench, feeling the grooves his tools had worn into the wood over forty years.
>
> She picked up his old hand plane. It was heavier than she remembered.
>
> Outside, the rain that had fallen all week finally stopped, and a thin line of sun broke through the clouds.
>
> She understood now that grief wasn't something to get over. It was something to carry, like the plane in her hands. She would keep it. She would learn to use it. And in that small act, he would remain with her.

**Output**
> Mara stood in the doorway of her father's workshop. It smelled of sawdust and machine oil. She ran her fingers along the workbench, over the grooves his tools had worn into it in forty years.
>
> She picked up his old hand plane. It was heavier than she remembered.
>
> The rain that had fallen all week stopped at some point while she was in there. She didn't notice. She was turning the plane over, looking for how the blade came out, because if she was going to keep it she was going to have to learn how it worked.
>
> What changed
> - Every event stays, including the rain stopping and her decision to keep the plane and learn it.
> - The grief-as-something-to-carry paragraph is gone; her handling of the plane carries it.
> - Cut the dust motes, the unnamed smell, and the tightening throat. The rain no longer breaks into sunlight on cue.

**Why:** Four StoryScope defaults in one page: sensory tour with a stock smell, embodied emotion, setting as mirror, and resolution by stated understanding. The decision survives as her own practical thought, not the narrator's moral.

---

## 5. Dialogue-heavy fiction

**Request:** "The dialogue in this scene feels fake. Fix it."

**Input**
> "I just think Mom would have wanted us to keep the house," Dana said softly. "It's not just a building. It's where all our memories live."
>
> "I understand that," Eli replied, his voice heavy with emotion. "But memories aren't stored in walls, Dana. They're in us. Holding on to the house won't bring her back."
>
> Dana felt tears welling in her eyes. "Maybe you're right. Maybe letting go is its own kind of love."

**Output**
> "Mom would've wanted us to keep the house," Dana said.
>
> "Mom wanted a lot of things." Eli didn't look up from the stack of mail on the counter. "Who's paying the property tax on it? You?"
>
> "I could rent it."
>
> "You'd have to clear out her closets first."
>
> Dana didn't answer. After a while she said, "Maybe you're right," and he had the decency not to agree out loud.
>
> What changed
> - Same positions and the same outcome: Dana wants to keep it, Eli doesn't, and she gives way.
> - They now argue about money and closets instead of about what memories are. The theme is still there, under the talk.
> - The property tax, the mail, and the closets are my additions. Swap in whatever the house really involves in your story.
> - Dropped tags that explained feelings ("softly," "heavy with emotion," "tears welling").

**Why:** StoryScope's debate-dialogue default (59% vs 34%). Small invented details are acceptable in fiction rewrites when they serve an existing beat and are flagged; new events or backstory are not.

---

## 6. A linear countdown story

**Request:** "It's told hour by hour on purpose, counting down to her citizenship interview at 2 p.m. Just humanize the writing."

**Input**
> 9:00 a.m.
>
> Lina reviewed her flashcards one more time. The weight of this day pressed down on her like a heavy blanket — every question, every answer, every hope she had carried for eleven years. She wasn't just preparing for an interview; she was preparing for the rest of her life.
>
> 10:00 a.m.
>
> Her sister called. "You're going to be amazing," she said. Lina smiled, feeling a warmth spread through her chest.

**Output**
> 9:00 a.m.
>
> Lina went through the flashcards again. She had waited eleven years for this interview, and the cards had gone soft at the corners.
>
> 10:00 a.m.
>
> Her sister called to say she was going to be amazing. Lina smiled at the phone and said she knew, which wasn't true.
>
> What changed: kept the hour-by-hour structure and every event. Changed the heavy-blanket simile, the triad, the "not just an interview" contrast, and the warmth in her chest. I did not add a flashback to the eleven years; the countdown is the form, and it works.

**Why:** StoryScope's temporal findings would tempt a flashback. The user's structure and the form both say linear, so the structural pass leaves order alone and works only inside the beats.

---

## 7. A writer who uses fragments and dashes

**Request:** "Rewrite this newsletter intro so it sounds like me. Here's something I wrote last month."

**Sample (the user's)**
> Went to the hardware store for one hinge. Came back with a hinge, a caulk gun, and a strong opinion about the guy in aisle nine — who, to be fair, was right about the caulk. This is how every project starts. Small. Then not.

**Draft**
> In this week's newsletter, I want to share an important lesson I learned while renovating my bathroom. Home improvement projects often begin with a simple goal but can quickly expand in scope. It's essential to plan carefully, set a realistic budget, and be prepared for unexpected challenges along the way.

**Output**
> This week: the bathroom. Every project starts small. Then it doesn't. Plan more than feels necessary, budget for it — and assume something will go sideways, because it will.
>
> What changed: matched your fragments and your roughly one dash per paragraph. The draft has no story in it, only the lesson, so there was nothing concrete to put back. If something specific blew up the bathroom budget, that's the sentence this needs; I'd rather you supply it than have me invent it.

**Why:** Fragments and a dash are tells elsewhere in this skill; here they are the writer's voice, and the sample outranks the pattern rules. The three pieces of advice are real content, so the triad stays.

---

## 8. Academic paragraph with citations

**Request:** "Humanize this lit review paragraph. Don't touch the citations."

**Input**
> It is important to note that sleep deprivation has a profound impact on cognitive performance. Notably, Lim and Dinges (2010) found that total sleep deprivation had the largest effect on simple attention tasks, with a smaller effect on complex reasoning. Furthermore, research shows that even modest restriction — six hours per night for two weeks — produces deficits comparable to one or two nights of total deprivation (Van Dongen et al., 2003). These findings underscore the critical importance of sleep in academic settings.

**Output**
> Sleep deprivation impairs cognitive performance, but not every task suffers equally. Lim and Dinges (2010) found that total sleep deprivation had the largest effect on simple attention tasks and a smaller effect on complex reasoning. Even modest restriction matters: six hours per night for two weeks produced deficits comparable to one or two nights of total deprivation (Van Dongen et al., 2003). Both findings bear directly on academic settings.
>
> What changed: citations, numbers, and findings are unchanged. Removed "It is important to note," "Notably," "Furthermore," and "underscore the critical importance." "Research shows" now points to the study the sentence already cited. The last sentence is still an uncited claim; a source linking sleep to academic outcomes would support it.

**Why:** Factual mode with citations. No new sources, no stronger claims, no quirks. The note flags a weakness instead of fixing it by invention.

---

## 9. Polished but AI-shaped story

**Request:** "The prose in my story is fine but the whole thing feels AI-shaped. Free rein to restructure. Keep Elena, her father, the neighbor, and the maps."

**Input (summary of a 3,000-word draft)**
> Opens on a misty coastal town at dawn, salt and woodsmoke in the air. Elena, 34, auburn hair and green eyes, returns after her father's death. In his study she finds an unfinished map. Each scene yields the next clue: a letter, then a key from the neighbor Mr. Aalto, then a locked drawer. The drawer holds maps of places from her late mother's bedtime stories. Elena realizes her father loved her mother all along and that she must finish the map. She finishes it. Epilogue, a year later: she has opened a map shop, and the town glows at sunset.

**Diagnosis**
- Opening: establishing shot with a sensory tour; hero introduced by description.
- Order: clues in chronological order, first clue to grand reveal; the revelation adds a fact but recasts nothing.
- Resolution: internal understanding followed by a single admirable choice that fixes everything.
- Setting mirrors mood (mist at arrival, glow at the end); a Claude-style epilogue confirms her future.
- Single track; escalation flat.

**Structural changes**
1. Open at the drawer, with Aalto holding out the key. He is introduced by what he says; Elena by what she refuses.
2. Early, Elena mocks one of her mother's place names ("the Salt Stair") as a story her father humored. The drawer's maps recast that scene: he had been surveying the real coastline to find where the stories came from.
3. A second strand from existing material: Aalto wants the drafting table for his granddaughter. Elena says no. It rhymes with her own inheritance without explaining it.
4. She cannot finish the map; the last places are from stories she no longer remembers. She gives Aalto the table. The choice matters but does not resolve the loss.
5. No epilogue. The story ends in the study, the map still unfinished.

**Opening of the revision**
> "He never locked anything," Mr. Aalto said, holding out the key as if it might be the wrong one. "Then last spring, this."
>
> Elena didn't take it. "If it's more of the Salt Stair stuff, I've seen it."

**Why:** This is where Level 2 matters most. The draft's sentences may already be clean, so a surface pass would change little (StoryScope found surface edits barely touch narrative signal). The changes are structural and each has a reason in this story. The note to the user lists them so they can refuse any.

---

## 10. An email that is already fine

**Request:** "My coworker says my emails sound like ChatGPT. Can you fix this one?"

**Input**
> Hi Priya,
>
> Thanks for sending the draft over. I read it on the train this morning and mostly I just want to say: the second section works. The part about the Tuesday pickup schedule confused me a bit. Are we moving it to Wednesdays for everyone or just the east side? Once that's settled I think it's ready.
>
> I hope this helps! Let me know if you have any other questions.
>
> Sam

**Output**
> Hi Priya,
>
> Thanks for sending the draft over. I read it on the train this morning and mostly I just want to say: the second section works. The part about the Tuesday pickup schedule confused me a bit. Are we moving it to Wednesdays for everyone or just the east side? Once that's settled I think it's ready.
>
> Let me know if you have any other questions.
>
> Sam
>
> One change: cut "I hope this helps!" It's the one line that reads like a chatbot, and it doesn't fit a note giving feedback. The rest already sounds like a person: the train, the specific question about pickups, the plain verdict.

**Why:** Light edit. Sign-offs predate chatbots, and the body is specific and uneven in the right ways. Rewriting it to show effort would make it worse.

---

## 11. A story from scratch

**Request:** "Write a 500-word story about a lighthouse keeper."

**Planning (kept private in a real reply)**
- Default version: a lonely keeper, a storm, a ship in danger, a brave rescue, a realization about connection, mist and brine, an epilogue years later.
- Alternatives: (a) the light was automated years ago, and a retired keeper still climbs up to clean the lens because the contractor does it badly; (b) logbook entries from a keeper whose relief is three weeks late, getting shorter; (c) a keeper's teenage son uses the light to flash Morse at someone on the mainland.
- Choice: (a). A conflict with an institution instead of the sea, comedy and loss together, an ending on an act rather than a realization. No storm.

**Opening of the story**
> The contractor came on the second Tuesday of March and October, and Ruth Pellow made a point of being in the garden when his van pulled in, so he could see that she was seventy-eight and had a trowel and no business on the stairs.
>
> "Morning, Mrs. Pellow."
>
> "Kevin."
>
> He always parked on the thyme. She had stopped mentioning it the year he started calling her young lady.

**Why:** The default is named so it can be rejected on purpose. The opening introduces both characters through action and speech, skips the establishing shot, and uses no sensory survey. The reply is the story alone: no mode label before it and no craft note after it.
