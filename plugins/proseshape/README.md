# ProseShape

**Make prose feel chosen, not defaulted.**

ProseShape is a writing skill for Claude and Codex. It rewrites or writes prose so that each choice reads as made by a person for this reader, not inherited from a model's defaults, while keeping every fact, number, quotation, citation, plot event, and the writer's voice.

It works at two levels:
- **Sentences.** It removes the habits that make text read as generated: staged contrasts, one-line closers, inflated significance and chatbot residue. Then it puts the life back in through the writer's own material.
- **Story structure.** It looks for the narrative defaults that research on AI fiction identifies: stated morals, tidy single-track plots, emotions told through the body, and epiphany or epilogue endings.

## What it does

- **Rewrites** supplied text and keeps every claim, event and ending. It flattens nothing and invents nothing.
- **Light edits.** Already-good writing gets a careful copyedit or is left nearly unchanged.
- **Restructures fiction** when you give it free rein, and reports each structural change so you can reject it.
- **Matches your voice** from a sample of your own writing.
- **Writes from scratch**, choosing against the default version of the piece instead of cleaning it up afterward.
- **Keeps technical text exact.** Code, commands, terms, numbers and citations stay unchanged.

It is built for readers, not AI detectors. It does not try to evade detection, and it does not add typos or fake quirks.

## How to use it

Ask for what you want and paste the text, for example:

- "Humanize this story. Same events, same ending."
- "Light polish only. Keep every fact and citation exactly as is."
- "Here are two things I wrote. Rewrite this draft so it sounds like me."
- "The prose is fine but this story feels AI-shaped. Free rein to restructure; keep the characters and premise."
- "Write a 1,200-word story about a hospice night nurse. No stated moral, no years-later ending."

Claude and Codex use the skill when a request matches. To be sure they do, name it ("use ProseShape"). In Claude Code you can also run `/proseshape:proseshape`; in Codex, pick it from `/skills`.

## What is inside

ProseShape is instructions only: a `SKILL.md`, six reference files, and the manifests and icon that Claude and Codex read. It runs no code, starts no servers, fetches nothing, and sends nothing anywhere.

## Evidence

The skill was developed and tested against a strong ordinary-editor prompt, using held-out texts and a blind judge. Version 1.4.0 led that baseline on AI-shaped drafts and trailed it slightly on text a person had already written well. Pooled over 27 held-out texts, its lead was +0.52 points on a 10-point scale, with a 95% interval of −0.15 to +1.15. The judge found fewer than half as many fact problems in its output (45 against 109). The method, raw outputs and limitations are in the [source repository](https://github.com/Aieda1l/ProseShape).

## License and credits

MIT. ProseShape adapts material from [Humanizer](https://github.com/blader/humanizer) by Siqi Chen (MIT). It draws on Wikipedia's *Signs of AI writing* (CC BY-SA 4.0) and on *StoryScope: Investigating idiosyncrasies in AI fiction* by Russell et al. (arXiv:2604.03136). See `THIRD_PARTY_NOTICES.md`.
